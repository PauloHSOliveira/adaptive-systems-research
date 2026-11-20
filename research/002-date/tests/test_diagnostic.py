import dataclasses
import numpy as np
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from diagnostic import (DecayedCMS, generate_trace, collect_events,
                        label_events, features, analyze, Event)


def example():
    return Event(5, 2, 1, 2., 1., .6, .4, .6, .4,
                 .8, .8, 1, 1, .1, .2, .5)


def test_margin_cost_aware():
    x = example()
    assert x.margin_s == 0.8
    assert features(x, 'margin')[-4] == 0.8


def test_collision_error_nonnegative():
    s = DecayedCMS(width=3, depth=2, tau=10, seed=8)
    for x in [5, 1, 5, 9, 2, 2, 2, 5]:
        s.update(x)
    assert 0 <= s.prob(5) <= 1 + 1e-12


def test_prefix_causality():
    base, cost = generate_trace(n=300, t=1500, scenario='stationary', seed=8)
    future = np.concatenate((base[:1100], np.full(400, 99, dtype=np.int32)))
    a, _ = collect_events(base, cost, k=10, width=32, seed=8)
    b, _ = collect_events(future, cost, k=10, width=32, seed=8)
    assert [dataclasses.asdict(e) for e in a if e.t < 1100] == [
        dataclasses.asdict(e) for e in b if e.t < 1100]


def test_no_future_in_collection():
    from diagnostic import label_events as labeling
    base, costs = generate_trace(n=100, t=200, seed=4)
    events, _ = collect_events(base, costs, k=5, width=32, seed=4)
    assert len(events) > 0
    # Only this separate function accesses future slices.
    assert labeling(events, base, horizon=10)


def test_agreeing_actions_equal_loss():
    obj = example()
    trace = np.array([9,9,9,9,9,9,2,2,1,2,2,2,9,9], dtype=np.int32)
    pair = label_events([obj], trace, horizon=6)[0]
    assert pair[1] == pair[2]


def test_offline_lookahead_excludes_current_request():
    e = dataclasses.replace(example(), t=2, cand=2, victim=1, action_s=1, action_l=0)
    tr = np.array([9,9,2,1,1,1,9,9], dtype=np.int32)
    res = label_events([e], tr, horizon=3)
    assert res[0][1] == 3.0 and res[0][2] == 0.0


def test_seed_determinism():
    a, ca = generate_trace(n=200, t=2000, seed=21)
    b, cb = generate_trace(n=200, t=2000, seed=21)
    assert np.array_equal(a, b) and np.array_equal(ca, cb)
    ra, _ = collect_events(a, ca, k=10, seed=5, width=32)
    rb, _ = collect_events(b, cb, k=10, seed=5, width=32)
    assert ra == rb


def test_temporal_train_test_embargo():
    T, H = 10000, 32
    assert int(.60*T)-H < int(.80*T)
    x, costs = generate_trace(n=500, t=T, seed=4)
    r = analyze(x, costs, seed=4, k=20, width=32, horizon=H)
    assert r['dev_events'] > 0 and r['test_events'] > 0


def test_memory_bound_estimate():
    s = DecayedCMS(width=128, depth=4)
    assert s.memory_bytes == s.arr.nbytes + s.a.nbytes + s.b.nbytes + 16
    tr, costs = generate_trace(n=300, t=1000)
    _, mem = collect_events(tr, costs, k=20, width=128)
    assert mem < 16000
