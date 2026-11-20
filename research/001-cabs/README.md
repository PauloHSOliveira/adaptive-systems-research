# Study 001 — CABS

**Status:** Completed as an exploratory study. Development was stopped as a principal algorithmic research direction.

See [the scientific working paper](paper.md), [reference implementation](code/cabs/), [tests](tests/) and [reproduced synthetic results](data/benchmarks_reproduced.json).

CABS uses the condition `lower(candidate) > upper(victim)` to certify dominance of **historical weighted frequency** at a fixed state and epoch. The certificate does not imply better future cache behavior. The closest point-estimate baseline uses the same Weighted Space-Saving estimator and resident metadata; it is **not** a faithful W-TinyLFU baseline.

Across 4 synthetic workloads × 3 seeds × 5 policies (60 runs), CABS incurred **8.38% higher weighted miss cost** under fast hot-set drift relative to the point-estimate baseline; other comparisons showed small or mixed effects. The experimental generator named `reset_churn` did not enter its next phase within the 10,000-request run and cannot be presented as a tested multi-epoch reset scenario.

## Reproduce

```bash
cd research/001-cabs/code
PYTHONPATH=. python -m unittest discover -s ../tests -v
PYTHONPATH=. python -m cabs.bench --n 10000 --seeds 3 --k 100 --m 500 --epoch 10000 --output ../data/reproduction_local.json
```

No public trace evaluation, memory-equalized production baseline, or statistically confirmatory superiority result is available. This is a scientifically useful negative result, not a universal impossibility theorem.
