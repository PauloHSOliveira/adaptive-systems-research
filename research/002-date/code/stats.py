"""Exploratory MBB-based one-sided minimum-benefit test for a fixed trace.

Requires within-trace weak dependence and stable mean over the target interval.
Uses time-indexed sums AND counts so opportunity density is correctly weighted.
Not valid automatically for non-stationary / long-range-dependent series.
"""
from __future__ import annotations
from dataclasses import dataclass
import math
import numpy as np

@dataclass(frozen=True)
class MinimumBenefitTest:
    n_opportunities: int
    mean_loss_baseline: float
    mean_loss_treatment: float
    estimated_relative_benefit: float
    mean_null_loss_difference: float
    block_length: int
    bootstrap_reps: int
    p_one_sided: float
    centered_se: float


def minimum_benefit_test(
    timestamp: np.ndarray, loss_baseline: np.ndarray,
    loss_treatment: np.ndarray, *, n_requests: int, min_benefit: float = 0.02,
    block_length: int = 256, reps: int = 1999, seed: int = 2026
) -> MinimumBenefitTest:
    """H0: E[loss_treatment - (1-tau)*loss_baseline] >= 0.

    Finite-sample p-values are NOT exact; calibration depends on block choice,
    stationarity/weak mixing, label overlap, and number of opportunities.
    """
    t = np.asarray(timestamp, dtype=np.int64)
    l2 = np.asarray(loss_baseline, dtype=np.float64)
    l3 = np.asarray(loss_treatment, dtype=np.float64)
    if t.ndim != 1 or l2.shape != t.shape or l3.shape != t.shape:
        raise ValueError('all input vectors must be one-dimensional and equal length')
    if n_requests <= 0 or not 0 < block_length < n_requests or reps < 99:
        raise ValueError('invalid n_requests/block_length/reps')
    if len(t) == 0 or np.any(t < 0) or np.any(t >= n_requests):
        raise ValueError('no opportunities or timestamps out of bounds')
    if np.any(np.diff(t)<0) or np.any(~np.isfinite(l2)) or np.any(~np.isfinite(l3)):
        raise ValueError('timestamps unsorted or nonfinite loss')
    if np.any(l2 < 0) or np.any(l3 < 0) or not 0 <= min_benefit < 1:
        raise ValueError('losses must be nonnegative; min_benefit in [0,1)')

    per_req_count = np.bincount(t, minlength=n_requests).astype(np.float64)
    per_req_test = np.bincount(t, weights=l3-(1-min_benefit)*l2, minlength=n_requests)
    mean_l2 = float(l2.mean())
    mean_l3 = float(l3.mean())
    if mean_l2 <= 0:
        raise ValueError('baseline mean loss is zero: relative benefit undefined')
    observed_test_mean = float(per_req_test.sum()/per_req_count.sum())

    # Each candidate moving block includes all events in a request-time interval.
    # Efficient prefix sums avoid copying events during bootstrap.
    b = block_length
    def rolling_sums(x):
        prefix = np.concatenate(([0.0], np.cumsum(x, dtype=np.float64)))
        return prefix[b:] - prefix[:-b]
    block_total = rolling_sums(per_req_test)
    block_count = rolling_sums(per_req_count)
    starts = len(block_total)
    n_draws = int(math.ceil(n_requests/b))
    rng = np.random.default_rng(seed)
    boot_means=[]
    for _ in range(reps):
        ix = rng.integers(0, starts, size=n_draws)
        # Last selected block may make resample slightly longer than source;
        # standard MBB boundary approximation (O(b/T)).
        denom = block_count[ix].sum()
        if denom > 0:
            boot_means.append(float(block_total[ix].sum()/denom))
    boots=np.asarray(boot_means)
    if boots.size < reps//2:
        raise ValueError('too few bootstrap samples with admission opportunities')
    # Critically center the bootstrap statistic under the null boundary.
    centered = boots-observed_test_mean
    p = (1+np.count_nonzero(centered <= observed_test_mean))/(len(centered)+1)
    return MinimumBenefitTest(
        n_opportunities=len(t),mean_loss_baseline=mean_l2,
        mean_loss_treatment=mean_l3,
        estimated_relative_benefit=(mean_l2-mean_l3)/mean_l2,
        mean_null_loss_difference=observed_test_mean,
        block_length=b,bootstrap_reps=len(boots),p_one_sided=float(p),
        centered_se=float(np.std(centered,ddof=1)))


def partial_conjunction_2_of_3(p_values):
    p=np.asarray(p_values,dtype=float)
    if p.shape!=(3,) or np.any(~np.isfinite(p)) or np.any((p<0)|(p>1)):
        raise ValueError('exactly three valid p-values required')
    return float(min(1.0, 2.0*np.sort(p)[1]))
