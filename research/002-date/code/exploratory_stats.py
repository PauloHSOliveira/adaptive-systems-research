"""Exploratory paired moving-block bootstrap indexed by raw request time.

Does not claim that block length H ensures independence. Validity of intervals
requires suitable weak dependence / approximate stationarity within the segment.
"""
from __future__ import annotations
import math
import numpy as np


def paired_moving_block_ci(times, losses_a, losses_b, start, stop, block_length=256,
                           n_boot=300, seed=2026, alpha=0.05):
    """Return CI for mean(loss_a-loss_b) per opportunity.

    Blocks are overlapping raw-request intervals and are sampled with replacement.
    Request-time indexing maintains local clustering and the number of events/block.
    """
    times = np.asarray(times, dtype=np.int64)
    a = np.asarray(losses_a, dtype=np.float64)
    b = np.asarray(losses_b, dtype=np.float64)
    if len(times) != len(a) or len(times) != len(b):
        raise ValueError('mismatched event arrays')
    if start >= stop or not (0 < block_length <= stop-start) or n_boot < 2:
        raise ValueError('invalid span, length or repetitions')
    if np.any((times < start) | (times >= stop)) or len(times) == 0:
        raise ValueError('timestamps outside interval or no events')
    n = stop - start
    ds = np.zeros(n, dtype=np.float64)
    ct = np.zeros(n, dtype=np.int64)
    np.add.at(ds, times - start, a - b)
    np.add.at(ct, times - start, 1)
    prefix_d = np.concatenate(([0.0], np.cumsum(ds)))
    prefix_n = np.concatenate(([0], np.cumsum(ct)))
    obs = float(np.sum(a-b) / len(a))
    rng = np.random.default_rng(seed)
    possible_starts = n - block_length + 1
    n_blocks = math.ceil(n / block_length)
    boots = []
    for _ in range(n_boot):
        starts = rng.integers(0, possible_starts, size=n_blocks)
        ends = starts + block_length
        # last block is shorter: bootstrap sample has exactly n raw time steps.
        ends[-1] = starts[-1] + n - (n_blocks-1)*block_length
        diff = np.sum(prefix_d[ends] - prefix_d[starts])
        n_ev = np.sum(prefix_n[ends] - prefix_n[starts])
        if n_ev > 0:
            boots.append(float(diff/n_ev))
    if len(boots) < n_boot*0.9:
        raise ValueError('too few events in bootstrap replications')
    lo, hi = np.quantile(np.asarray(boots), [alpha/2, 1-alpha/2])
    return {'delta_a_minus_b': obs, 'ci_low': float(lo), 'ci_high': float(hi),
            'block_length': int(block_length), 'n_boot': n_boot,
            'opportunities': int(len(times)), 'request_span': int(n),
            'method': 'moving_block_bootstrap_overlapping_candidate_blocks',
            'interpretation': 'exploratory conditional on segment, not cross-trace generalization'}
