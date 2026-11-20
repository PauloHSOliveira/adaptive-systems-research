"""DATE research diagnostic v0.1. Offline proxy evaluation, NOT a live cache policy.

Causal feature collection uses two independent exponentially decayed Count-Min
sketches and an LRU reference cache. Counterfactual lookahead is used only in
`label_events`, a separate post-simulation step.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import OrderedDict
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline


@dataclass(frozen=True)
class Event:
    t: int
    cand: int
    victim: int
    cost_c: float
    cost_v: float
    p_sc: float
    p_sv: float
    p_lc: float
    p_lv: float
    margin_s: float
    margin_l: float
    action_s: int
    action_l: int
    err_s: float
    err_l: float
    hit_ema: float


class DecayedCMS:
    """Positive-update CMS with global lazy exponential decay and bounded array.

    Frequencies are normalized by decayed request mass; CMS collision bias means
    point estimates are not guaranteed to sum to one over distinct IDs.
    """
    def __init__(self, width=128, depth=4, tau=64.0, seed=19):
        if min(width, depth, tau) <= 0:
            raise ValueError('width, depth, tau must be positive')
        self.width, self.depth = int(width), int(depth)
        self.gamma = float(np.exp(-1.0 / tau))
        self.arr = np.zeros((self.depth, self.width), dtype=np.float64)
        rg = np.random.default_rng(seed)
        self.a = rg.integers(1, 2147483647, size=depth, dtype=np.int64)
        self.b = rg.integers(0, 2147483647, size=depth, dtype=np.int64)
        self.scale = 1.0
        self.mass = 0.0

    @property
    def memory_bytes(self):
        return int(self.arr.nbytes + self.a.nbytes + self.b.nbytes + 16)

    def _indices(self, obj):
        key = int(obj)
        # Python ints avoid platform-dependent overflow in the hash product.
        return [(key * int(a) + int(b)) % 2147483647 % self.width
                for a, b in zip(self.a, self.b)]

    def prob(self, obj):
        if self.mass == 0:
            return 0.0
        ix = self._indices(obj)
        return float(min(self.arr[i, j] for i, j in enumerate(ix)) * self.scale / self.mass)

    def update(self, obj):
        self.scale *= self.gamma
        self.mass = self.gamma * self.mass + 1.0
        if self.scale < 1e-8:
            self.arr *= self.scale
            self.scale = 1.0
        inv = 1.0 / self.scale
        for i, j in enumerate(self._indices(obj)):
            self.arr[i, j] += inv


def generate_trace(n=10000, t=30000, scenario='stationary', seed=42):
    rg = np.random.default_rng(seed)
    rank = np.arange(1, n + 1, dtype=np.float64)
    probs = rank ** (-1.18)
    probs /= probs.sum()
    trace = np.empty(t, dtype=np.int32)
    if scenario == 'uniform':
        trace[:] = rg.integers(0, n, size=t, dtype=np.int32)
    elif scenario == 'stationary':
        trace[:] = rg.choice(n, size=t, p=probs)
    elif scenario == 'shift':
        split = t // 2
        trace[:split] = rg.choice(n, size=split, p=probs)
        trace[split:] = (rg.choice(n, size=t - split, p=probs) + n // 3) % n
    elif scenario == 'cycling':
        block = 1200
        for start in range(0, t, block):
            end = min(start + block, t)
            shift = (start // block % 4) * (n // 4)
            trace[start:end] = (rg.choice(n, size=end - start, p=probs) + shift) % n
    else:
        raise ValueError(scenario)
    # Costs are fixed by object ID, not indexed by request time.
    costs = np.clip(rg.lognormal(0.0, 0.6, size=n), 1.0, 8.0)
    return trace, costs


def collect_events(trace, costs, k=100, short_tau=64.0, long_tau=512.0,
                   width=128, seed=1):
    """Only reads the current request and history. No future label access."""
    s = DecayedCMS(width=width, tau=short_tau, seed=seed)
    l = DecayedCMS(width=width, tau=long_tau, seed=seed)
    cache = OrderedDict()
    events = []
    err_s = err_l = 0.0
    hit_ema = 0.0
    prev_probe = None
    decay = 0.02
    for t, obj_np in enumerate(trace):
        obj = int(obj_np)
        hit = obj in cache
        if not hit and len(cache) >= k:
            victim = next(iter(cache))
            # Causal estimates BEFORE current request contributes to sketches.
            p_sc, p_sv = s.prob(obj), s.prob(victim)
            p_lc, p_lv = l.prob(obj), l.prob(victim)
            cc, cv = float(costs[obj]), float(costs[victim])
            ms = cc * p_sc - cv * p_sv
            ml = cc * p_lc - cv * p_lv
            events.append(Event(t, obj, victim, cc, cv, p_sc, p_sv,
                                p_lc, p_lv, ms, ml, int(ms > 0), int(ml > 0),
                                err_s, err_l, hit_ema))
        # A probe was selected BEFORE observing obj, so its Brier score is valid.
        if prev_probe is not None:
            ps, pl = s.prob(prev_probe), l.prob(prev_probe)
            observed = float(obj == prev_probe)
            err_s = (1 - decay) * err_s + decay * (ps - observed) ** 2
            err_l = (1 - decay) * err_l + decay * (pl - observed) ** 2
        hit_ema = (1 - decay) * hit_ema + decay * float(hit)
        if hit:
            cache.move_to_end(obj)
        else:
            if len(cache) >= k:
                cache.popitem(last=False)
            cache[obj] = None
        s.update(obj)
        l.update(obj)
        prev_probe = obj
    online_bytes = s.memory_bytes + l.memory_bytes + 8 * 4 + k * 16
    return events, online_bytes


def label_events(events, trace, horizon=32):
    """OFFLINE ONLY: produces realized single-swap, fixed-set proxy loss.

    A future request is counted for only candidate and victim. This does not
    represent the full performance of diverging dynamic cache states.
    """
    out = []
    for ev in events:
        if ev.t + horizon >= len(trace):
            continue
        future = trace[ev.t + 1:ev.t + horizon + 1]
        d = ev.cost_c * np.count_nonzero(future == ev.cand) - \
            ev.cost_v * np.count_nonzero(future == ev.victim)
        best = int(d > 0)  # for d==0, both losses are zero
        ls = float(abs(d)) if d != 0 and ev.action_s != best else 0.0
        ll = float(abs(d)) if d != 0 and ev.action_l != best else 0.0
        out.append((ev, ls, ll))
    return out


def features(ev, mode='base'):
    f = [ev.err_s, ev.err_l, ev.hit_ema, ev.cost_c, ev.cost_v,
         ev.action_s, ev.action_l, ev.action_s * ev.action_l]
    if mode == 'margin':
        f += [ev.margin_s, ev.margin_l, abs(ev.margin_s - ev.margin_l),
              abs(ev.margin_s) + abs(ev.margin_l)]
    return f


class Selector:
    def __init__(self, records, mode, seed=1):
        self.mode = mode
        self.seed = seed
        self.base_short = sum(ls for _, ls, _ in records) < sum(ll for _, _, ll in records)
        if mode not in ('base', 'margin', 'placebo'):
            self.model = None
            return
        effective = [(i, ev, ls, ll) for i, (ev, ls, ll) in enumerate(records)
                     if abs(ls - ll) > 1e-12]
        self.model = None
        self.constant = self.base_short
        if not effective:
            return
        idx, evs, ls, ll = zip(*effective)
        y = np.array([int(a < b) for a, b in zip(ls, ll)])
        w = np.array([abs(a - b) for a, b in zip(ls, ll)])
        if len(set(y)) < 2:
            self.constant = bool(y[0])
            return
        X = self._array(list(evs), list(idx))
        self.model = Pipeline([
            ('scale', StandardScaler()),
            ('lr', LogisticRegression(C=1.0, max_iter=300, random_state=seed)),
        ])
        self.model.fit(X, y, lr__sample_weight=w)

    def _array(self, evs, indices):
        data = np.array([features(ev, 'margin' if self.mode == 'margin' else 'base')
                         for ev in evs], dtype=np.float64)
        if self.mode == 'placebo':
            # Fixed pseudo-random uninformative features; not identifier hashes.
            r = np.random.default_rng(self.seed + 709)
            # One deterministic vector per event timestamp, stable across splits.
            extra = np.empty((len(evs), 4))
            for j, ev in enumerate(evs):
                rg = np.random.default_rng((self.seed * 103 + ev.t * 1009) % (2**32))
                extra[j] = rg.standard_normal(4)
            data = np.hstack((data, extra))
        return data

    def choose(self, events):
        if self.mode == 'fixed':
            return np.full(len(events), int(self.base_short), dtype=np.int8)
        if self.mode == 'error':
            return np.array([int(ev.err_s < ev.err_l) for ev in events], dtype=np.int8)
        if self.model is None:
            return np.full(len(events), int(self.constant), dtype=np.int8)
        X = self._array(events, list(range(len(events))))
        return (self.model.predict_proba(X)[:, 1] >= 0.5).astype(np.int8)

    @property
    def parameter_bytes(self):
        if self.model is None:
            return 8
        reg = self.model.named_steps['lr']
        scaler = self.model.named_steps['scale']
        return int(reg.coef_.nbytes + reg.intercept_.nbytes +
                   scaler.mean_.nbytes + scaler.scale_.nbytes)


def analyze(trace, costs, seed=42, horizon=32, k=100, width=128,
            short_tau=64, long_tau=512):
    events, bytes_base = collect_events(trace, costs, k=k, width=width,
                                        short_tau=short_tau, long_tau=long_tau,
                                        seed=seed)
    labeled = label_events(events, trace, horizon)
    n = len(trace)
    # Development ends at 60%; an unused buffer separates development/test.
    dev = [(ev, a, b) for ev, a, b in labeled if ev.t + horizon < int(.60 * n)]
    test = [(ev, a, b) for ev, a, b in labeled if ev.t >= int(.80 * n)]
    if not dev or not test:
        raise ValueError('Insufficient event count')
    res = {'n_requests': n, 'dev_events': len(dev), 'test_events': len(test),
           'disagreement_fraction': float(np.mean([ev.action_s != ev.action_l
                                                   for ev, _, _ in test])),
           'sketch_and_cache_bytes_estimated': bytes_base,
           'trace_sha256': hashlib.sha256(trace.tobytes()).hexdigest(),
           'controllers': {}}
    for mode in ('fixed', 'error', 'base', 'placebo', 'margin'):
        sel = Selector(dev, mode, seed=seed)
        choices = sel.choose([e for e, _, _ in test])
        loss = [a if short else b for short, (_, a, b) in zip(choices, test)]
        res['controllers'][mode] = {'loss_mean': float(np.mean(loss)),
                                    'loss_sum': float(np.sum(loss)),
                                    'model_bytes': sel.parameter_bytes,
                                    'online_bytes_estimated': bytes_base + sel.parameter_bytes}
    b = res['controllers']['base']['loss_mean']
    m = res['controllers']['margin']['loss_mean']
    res['relative_gain_margin_vs_base'] = None if b == 0 else (b - m) / b
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--t', type=int, default=30000)
    ap.add_argument('--n', type=int, default=10000)
    ap.add_argument('--seeds', type=int, default=3)
    ap.add_argument('--width', type=int, default=128)
    ap.add_argument('--horizon', type=int, default=32)
    ap.add_argument('--output', default='results.json')
    args = ap.parse_args()
    rows = []
    for scenario in ('stationary', 'uniform', 'shift', 'cycling'):
        for i in range(args.seeds):
            seed = 41 + i
            trace, costs = generate_trace(args.n, args.t, scenario, seed)
            row = analyze(trace, costs, seed=seed, width=args.width, horizon=args.horizon)
            row['scenario'], row['seed'] = scenario, seed
            rows.append(row)
    payload = {'scope': 'SYNTHETIC_DIAGNOSTIC_OFFLINE_PROXY_NOT_END_TO_END',
               'config': vars(args), 'results': rows}
    Path(args.output).write_text(json.dumps(payload, indent=2), encoding='utf-8')
    print(f'Wrote {args.output} with {len(rows)} runs')
    for scenario in ('stationary', 'uniform', 'shift', 'cycling'):
        s = [r for r in rows if r['scenario'] == scenario]
        b = np.mean([r['controllers']['base']['loss_mean'] for r in s])
        m = np.mean([r['controllers']['margin']['loss_mean'] for r in s])
        p = np.mean([r['controllers']['placebo']['loss_mean'] for r in s])
        disagreement = np.mean([r['disagreement_fraction'] for r in s])
        print(f'{scenario:11} C2={b:.4f} C3={m:.4f} placebo={p:.4f} '
              f'disagreement={disagreement:.1%}')


if __name__ == '__main__':
    main()
