# Study 003 — Adversarially Robust Streaming Algorithms

**Status:** Closed — negative / exploratory (2026-11-22).  
**Novelty:** No original algorithm, general impossibility theorem, or solution of the ITCS 2026 \(F_0\) open question is claimed.

## Canonical material

- [Technical report](paper.md) — the complete English manuscript, proofs, limitations, and references.
- [Claim ledger](CLAIMS.md) — ten-round traceability and rejected assertions.
- [Exact-math verifier](code/verify_report.py) — verifies the reflected-walk first/second-moment recurrences and the explicit-list churn example without third-party packages.
- [Unit tests](tests/test_report.py) — small deterministic consistency checks.

## Reproduce the checks

From this directory:

    python3 code/verify_report.py
    python3 -m unittest discover -s tests -p 'test_*.py' -v

The checks use Python's standard library and do not execute attacks, stochastic sampling, or production benchmarks. They certify only finite arithmetic identities and examples that the manuscript proves analytically.

## Study scope

The investigation considered deterministic point-frequency queries, set-valued heavy-hitter outputs, and distinct-element \(F_0\) streams against bounded-memory adversaries. The final focus was Question 33 of:

Omri Ben-Eliezer, Krzysztof Onak, and Sandeep Silwal, *Robust Streaming Against Low-Memory Adversaries*, ITCS 2026. https://doi.org/10.4230/LIPIcs.ITCS.2026.16

It did **not** solve that question. In particular, an exact-feedback memoryless construction is not a robust attack against every multiplicatively accurate estimator.

## Naming note

The repository's historical paper archive contains a file named [003-H-DATE-2.md](../../papers/003-H-DATE-2.md). That file is the earlier **Study 002A** follow-up, not this Study 003. This directory is the canonical location for Study 003.

## Lifecycle

**Proved under stated assumptions:** deterministic point-query bound, elementary explicit-list churn, elementary \(O(\log m)\) adversarial schedule, restricted exact-feedback random-walk analysis, and prefix-state indistinguishability.

**Refuted:** two proposed point-query impossibility formulations and an overbroad list-aggregation impossibility.

**Not tested:** physical systems, independent experiment replications, full literature exhaustiveness, or end-to-end adversarial benchmarking.

**Decision:** close and preserve negative findings. Reopen only for a precisely scoped new theorem or independently validated experimental question.
