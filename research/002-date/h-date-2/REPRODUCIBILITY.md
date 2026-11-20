# Reproducibility protocol — H-DATE-2

## Environment

- Python 3.11+ recommended; the code uses `fractions.Fraction`, `collections`, `math`, `argparse`, and `unittest`.
- Optional for independent fast-DP cross-checks and floating-point root proposals: `numpy`, `scipy`.
- CPU only, no network, no private data, no third-party API.

```bash
python -m pip install -r requirements.txt
PYTHONPATH=code python -m unittest discover -s tests -p 'test_*.py' -v
```

The historical exact root-certificate script first proposes brackets by floating-point calculations, but verifies all accepted brackets and derivative inequalities with rational arithmetic. Always distinguish the *untrusted proposal* from the *certified check*.

## Reproduce the reported analyses

```bash
python code/certify_monotonic_width.py --intervals 128
python code/certify_monotonic_width.py --intervals 256
python code/exact_window_certificates.py
python code/hmm_window_value.py --output data/window_results_reproduced.json
python code/verify_round9.py --output data/round9_verification_reproduced.json
```

`code/round2_exact_enumeration.py` and `code/symbolic_roots.py` are preserved exploratory scripts with historical output conventions. Treat those outputs as provenance; the authoritative checked risks for general finite pairs are from `exact_window_certificates.py` and the tests.

## Result-to-evidence mapping

| Claim | Reproduction source |
|:--|:--|
| $V_M(0.8,0.9;1,5)=84231/7812500$ | `test_round6.py`, `test_round8.py`, `round2_exact_results.json` |
| Non-unimodal $R(0.6,0.9;1,w)$ | `test_round8.py::test_two_distinct_strict_local_minima` |
| Window 5 vs. sign-only window 1 under $w\le11$ | `test_round6.py::test_window_short_five_positive_at_r099`, `test_round8.py` |
| Critical interval width decreases with $\alpha$ for $(1,5)$ | `certify_monotonic_width.py` with `--intervals 128` and `256` |
| Rare-transition $\Theta(q\log(1/q))$ | **External theorem**: Nair et al. 2005, Theorem 3.1; not a numerical result |

## Integrity and interpretation

- The model's input probabilities and each displayed finite-risk comparison are rational; rounding affects only how values are printed.
- The monotonicity certificate is an exact-arithmetic proof *conditional on the provided symbolic reduction and correct software*. Independent code review is still necessary.
- Exact probabilities are not independent trials; confidence intervals are inappropriate for these finite symbolic computations.
- The asymptotic theorem is **literature-derived**. The included script evaluates example bounds but does not reprove the published coefficient.
- No holdout, real cache trace, memory-equalized system comparison, or production benchmark was performed.
- Scientific manuscripts cite upstream literature explicitly; do not claim the rediscovered filtering rate is original.