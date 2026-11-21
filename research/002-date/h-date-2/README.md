# H-DATE-2 — Decision-Margin Information and Temporal Window Selection

**Research 002 companion study · Final status: closed (exploratory, no novelty or deployment claim).**

This directory archives a mathematical investigation of whether candidate–victim decision-margin magnitudes add value to a sign-only two-window selector. The model is a **symmetric two-state HMM with one-step binary prediction**, not a production cache. The core rare-transition filtering asymptotics were already published by Khasminskii and Zeitouni (1996) and Nair, Ordentlich and Weissman (2005).

## Read first

- [Corrected PDF (10 pages)](papers/H-DATE-2-Scientific-Report.pdf) — single section-numbering hierarchy, readable equations and tables.
- [Print-ready Markdown source](papers/print-source.md) — removes hard-coded heading numbers; use Pandoc's --number-sections only once.
- [Scientific working paper](paper.md) — definitions, proofs, exact risk tables, prior-art audit, open questions and a negative-novelty conclusion.
- [Reproducibility guide](REPRODUCIBILITY.md) — environment, deterministic commands and known limits.
- [References](references.bib) — BibTeX including the original 2005 filtering theorem.
- [Claim ledger](data/claims.csv) — explicit proven, certified, refuted and unresolved status.

## Reproducible evidence

| Item | What it verifies | Classification |
|:--|:--|:--|
| `code/round2_exact_enumeration.py` | The original fixed-window example and the global exact value 0.010781568 | Exact finite enumeration |
| `code/exact_window_certificates.py` | Bayes risks for finite odd window pairs | Exact rational arithmetic |
| `code/certify_monotonic_width.py` | Strict width monotonicity for the **specific (1,5)** construction | Computer-assisted rational-interval certificate |
| `code/hmm_window_value.py` | Independent numerical dynamic-programming cross-check | Numerical validation only |
| `code/verify_round9.py` | Risk comparison and analytic bound examples | Exact finite + numerical inequalities |
| `tests/` | Regression checks for displayed values and counterexamples | Unit tests |
| `data/` | Snapshot JSON artifacts from earlier calculations | Audit trail |

## Quick verification

Run from this directory:

```bash
PYTHONPATH=code python -m unittest discover -s tests -p 'test_*.py' -v
python code/certify_monotonic_width.py --intervals 128
python code/certify_monotonic_width.py --intervals 256
python code/verify_round9.py --output data/round9_verification_reproduced.json
```

Some checks require `numpy` and `scipy`; see the reproducibility guide. Output paths are intentionally configurable for local runs.

**Scope limits:** No traces, no integrated TinyLFU benchmark, no physical-cache multi-step counterfactuals, no statistical claim of online learning gains, and no peer review. Publication of exact code is **not** evidence of novelty or real-world effectiveness.