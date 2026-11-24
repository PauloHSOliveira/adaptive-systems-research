# Adaptive Systems Research

A repository for reproducible explorations in **online algorithms, probabilistic data structures, caching decisions, temporal estimation, and adaptive systems**.

Each study separates mathematical claims, experimental results, implementation artifacts, prior work, unresolved questions, and practical applicability. Negative results are preserved.

> **Research status:** The papers are exploratory working reports, not peer-reviewed articles. No production-cache improvement, original rare-transition filtering rate, or novel adversarial-streaming theorem has been demonstrated.

## Research index

| ID | Study | Central question | Evidence | Status |
|:--|:--|:--|:--|:--|
| 001 | [CABS — Historical certificates for cache admission](research/001-cabs/paper.md) | Does strict historical-frequency certification reduce future miss cost? | Formal invariants; 60 synthetic policy/workload/seed runs; 7 tests; +8.38% cost under fast drift versus the closest point-estimate baseline | **Closed as a principal algorithmic direction** |
| 002 | [DATE — Decision-aware temporal estimation](research/002-date/paper.md) | Do decision-margin magnitudes improve temporal estimator selection beyond feedback and decision signs? | Twelve synthetic scenario/seed trials; exploratory evidence was inconclusive | **Engineering direction suspended** |
| 002A | [H-DATE-2 — Margin information and temporal windows](research/002-date/h-date-2/paper.md) | When do magnitude features have Bayes decision value, and what window choices minimize risk? | Exact rational HMM enumeration; counterexamples; certified interval analysis; published-prior-art audit | **Closed; theoretical exploratory follow-up** |
| 003 | [Adversarially Robust Streaming Algorithms](research/003-adversarial-streaming/paper.md) | Do point queries, combinatorial outputs, or low-memory adversaries yield new robustness theorems? | Corrected constructive counterexamples; explicit-list churn; exact random-walk recurrences and concentration; claim ledger | **Closed; negative / exploratory; no novel theorem** |

## Research materials

- **H-DATE-2 manuscript:** [paper](research/002-date/h-date-2/paper.md) · [reproducibility](research/002-date/h-date-2/REPRODUCIBILITY.md) · [code and tests](research/002-date/h-date-2/) · [claim ledger](research/002-date/h-date-2/data/claims.csv).
- **CABS manuscript and code:** [study 001](research/001-cabs/).
- **DATE synthetic diagnosis and code:** [study 002](research/002-date/).
- **Study 003 (closed):** [technical report](research/003-adversarial-streaming/paper.md) · [claim ledger](research/003-adversarial-streaming/CLAIMS.md) · [reproducibility checks](research/003-adversarial-streaming/README.md).
- **Study 004 — closed at G0:** [original proposal](research/004-proposal.md) · [prior-art audit](research/004-gate0/PRIOR_ART_AUDIT.md) · [final G0 decision and mathematical checks](research/004-gate0/G0_DECISION.md). **H4-A2 not approved as original research; CCS 2023 replication remains a separate option.**
- **Study 003 continuous verification:** [GitHub Actions workflow](.github/workflows/research-003-validation.yml) · [latest run](https://github.com/PauloHSOliveira/adaptive-systems-research/actions/workflows/research-003-validation.yml).
- **Research standards:** [Experimental research protocol](docs/research-protocol.md).

### H-DATE-2: key distinction

The incremental value of margin features is the **difference in Bayes risks for the same window pair**:

```text
V_M = R(signs only) - R(signs and magnitudes)
```

It is not the end-to-end cache improvement and is not a fair objective for comparing different window pairs without accounting for their changing baseline risk.

The key rare-transition state-filtering asymptotic is **prior art**: Khasminskii and Zeitouni (1996) and Nair, Ordentlich and Weissman (2005), *Asymptotic Filtering and Entropy Rate of a Hidden Markov Process in the Rare Transitions Regime*, [DOI: 10.1109/ISIT.2005.1523663](https://doi.org/10.1109/ISIT.2005.1523663).

## Reproduce the H-DATE-2 checks

```bash
cd research/002-date/h-date-2
python -m pip install -r requirements.txt
PYTHONPATH=code python -m unittest discover -s tests -p 'test_*.py' -v
python code/certify_monotonic_width.py --intervals 128
```

## Scientific publication policy

The canonical sources are Markdown documents with code, deterministic outputs, and explicit bibliographic provenance. Historical rendered exports may reflect older manuscript versions; prefer the linked Markdown sources for the current research status. Do not claim that scripts or exact calculations constitute independent novelty validation.

**Licensing:** Reuse permissions for this research collection have not yet been specified in a repository license. Public availability alone does not grant broad reuse rights.
