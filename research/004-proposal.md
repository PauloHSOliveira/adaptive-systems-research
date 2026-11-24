---
title: "Research 004 — Experimental Audit of Adaptive Frequency Estimation"
subtitle: "Literature-first proposal, candidate hypotheses, and preregistration gates"
author: "Paulo H. S. Oliveira"
date: "2026-11-23"
lang: en
status: "proposed — not approved for a full study"
keywords:
  - adaptive streaming
  - count-min sketch
  - adversarial frequency estimation
  - concept drift
  - reproducibility
  - experimental design
---

# Research 004 — Experimental Audit of Adaptive Frequency Estimation

> **Final decision (2026-11-24): G0 CLOSED — NO-GO for H4-A2 as original research.** The earlier HOLD status below is historical and superseded by the [final G0 decision](004-gate0/G0_DECISION.md). No G1 or confirmatory experiment was approved; independent CCS 2023 replication remains a separately scoped option.

**Stage:** Proposal / targeted prior-art audit. **No Research 004 experiment has yet been run.**  
**G0 audit outcome (2026-11-23): NOT PASSED / HOLD.** **Further G0 review:** an [anonymous, related CMS preprint audit](004-gate0/KDD_PREPRINT_AUDIT.md) now documents strong overlap in value-based adaptive attacks, but no authenticated identity with the final KDD paper. The original H4-A design is superseded by the [H4-A2 reformulation](004-gate0/H4-A2_REFORMULATION.md), which explicitly tests feedback-mediated differences in **terminal target error** across two time permutations of the **same benign insertion multiset**. This refined candidate **also remains unapproved**. The initial H4-A design is **not authorized for G1**. See the [pinned prior-art and experiment audit](004-gate0/PRIOR_ART_AUDIT.md) and [source comparison matrix](004-gate0/SOURCE_MATRIX.csv). The preliminary preference for H4-A below reflects the **pre-audit proposal** and is superseded by this G0 decision.  
**Decision:** Prioritize candidate H4-A **conditionally**, after an upstream-experiment overlap check.  
**Scientific claim:** None. The proposal defines testable questions, not new results.  
**Scope:** Frequency sketches on insertion-only streams in the initial pilot. This is not a new result for general turnstile streams, \(F_0\), or all heavy-hitter detectors.

## 1. Motivation and relationship to prior studies

Studies 001–003 generated useful corrections and negative findings but did not establish a competitive new streaming algorithm or a general robustness theorem. Study 003 also showed how easy it is to propose an impossibility already refuted by deterministic sketches or by invalid assumptions. Research 004 therefore changes the order of operations:

1. Inspect primary literature and its experiment/source repositories.
2. State a measurable *interaction or comparative effect* rather than a generic robustness conjecture.
3. Freeze the workload, attacker model, counters, query budget, compute budget, and evaluation before examining held-out runs.
4. Reproduce at least one primary baseline or clearly document why faithful reproduction was not possible.
5. Run a small, paired pilot; **stop** if a meaningful result or a defensible originality angle is absent.

We intentionally **do not claim** that adaptive attacks, Count-Min Sketch weaknesses, Count-Keeper, evaluation frameworks, or heavy-hitter evasion are new.

## 2. Targeted literature audit (as of 2026-11-23)

| Source | Relevant result already established | Implication for our proposal | Audit status |
|:--|:--|:--|:--|
| Markelon, Filić, Shrimpton, CCS 2023 [1] | Concrete adaptive attacks and an adversarially robust Count-Keeper structure; public/private hash and query-budget experimental artifacts are available. | Generic CMS-vs-HeavyKeeper attacks, disclosure controls, and simple query-budget sweeps are **not** new. | Primary paper metadata and upstream code README checked; individual configurations still require inspection. |
| Ristache, Onak, KDD 2025 [2] | Studies which adaptive uses of Count-Min Sketch are safe or unsafe. | A new attack or rule must be compared to their actual formal regimes before any novelty claim. | Proceedings metadata and accessible overview checked; full technical assumptions **not yet audited**. |
| Da Dalt, Perrig, NDSS 2026 [3] | An open-source, end-to-end heavy-hitter network-monitoring framework with adaptive and zero-shot attacks and adversarial co-training. | Claiming to be the first adaptive or transfer-attack benchmark for heavy hitters would be false. Their framework may serve as a later independent comparison. | Official conference abstract and code README checked; precise experimental sweeps **not yet audited**. |
| Ben-Eliezer, Onak, Silwal, ITCS 2026 [4] | Formal memoryless/low-memory adversaries; separate theory for functions with small versus combinatorial output spaces. | We must state exactly what the attacker can remember, query, and observe. An engineering attacker with a large transcript **is not memoryless**. | Primary HTML paper reviewed during Study 003. |
| Ahmadian, Cohen, ICML 2024 [5] | Adaptive-input attacks against cardinality sketches, including empirical HLL++ attacks. | Do not transfer CMS error conclusions or query-complexity claims directly to distinct-count sketches. | Proceedings abstract checked. |
| Cohen, Nelson, Sarlós, Singhal, Stemmer, SODA 2026 [6] | General adaptive attacks and quadratic query bounds for several cardinality-sketch classes. | Do not propose generic query-budget lower bounds as novel; cardinality is a separate task. | Publisher/author abstract checked. |
| Drift benchmark literature [7] | Established evaluation protocols for detection under concept drift. | Changing workload distributions is not a new idea; a defensible contribution would require an independently validated **interaction** with adaptive sketch feedback. | Abstract checked; specific frequency-sketch overlap requires deeper audit. |

**Provisional, not demonstrated gap.** The targeted search did not establish whether *the interaction of non-stationary workload ordering and output-adaptive frequency-sketch attacks, under resource-matched baselines*, was already measured in the upstream experiments. **This must be checked before H4-A is approved as original.** The absence of an item from an abstract is not evidence that the experiment has not been performed.

**Primary implementations to audit before experiments:**

- CCS 2023: https://github.com/smarky7CD/cfe-in-adv-envs — inspect \`experiments/\`, \`streams/\`, \`cfes/\`, attack-model configurations, query budgets, and licensing.
- NDSS 2026: https://github.com/FrancescoDaDalt/HHNFM — inspect \`paper_code/config/\`, training/evaluation scripts, attack capabilities, and licensing.
- Do not silently copy upstream code or reimplement baselines with different semantics. Pin commits before replication.

## 3. Three falsifiable candidate hypotheses

### H4-A — Workload drift × feedback adaptivity interaction (recommended, conditional)

**Question.** Does abrupt change in stream composition alter the *additional* normalized point-query error induced by adaptive feedback, compared with an otherwise matched stationary-order stream?

**Domain.** Insertion-only frequency streams; Count-Min Sketch (CMS), starting with one faithful, fixed-memory implementation. Other sketches are secondary and require their own independent comparator analysis.

**Factorial design.**

- Workload factor \(D\in\{\mathrm{stationary},\mathrm{abrupt\ drift}\}\).
- Attacker factor \(A\in\{\mathrm{precommitted/oblivious},\mathrm{feedback\ adaptive}\}\).
- The stationary and drift conditions use the **same honest-update multiset** per seed, but different orderings. In the drift case, two groups of popular identifiers dominate successive phases; in the stationary case, the same updates are interleaved. This controls total honest-update counts while allowing temporal order to change.
- Both attackers receive the same insertion and query budgets. Only the adaptive policy may use previous public answers to select subsequent allowed actions. Explicitly report persistent attacker memory; do not label an arbitrary transcript-storing attacker memoryless.
- Use exact frequency counters as ground truth, updated on each realized stream, including attacker insertions.

Define, at specified evaluation checkpoints, \(e=\max_{x\in E_t}(\widehat f_t(x)-f_t(x))/\max(1,\|f_t\|_1)\) for CMS on insertion-only streams, where \(E_t\) is a preregistered probe set independent of the test-run seed and attacker observations. Report **attacker-selected probe error separately**; do not optimize and report the same selected set as an unbiased holdout. For CMS this is a nonnegative overestimate under ordinary counter semantics.

Write \(\mu_{D,A}\) for the across-seed expectation of the per-run *peak across preregistered checkpoints* of \(e\). The primary interaction estimand is

\[
\theta=(\mu_{\mathrm{drift,adaptive}}-\mu_{\mathrm{drift,oblivious}})
      -(\mu_{\mathrm{stationary,adaptive}}-\mu_{\mathrm{stationary,oblivious}}).
\]

**Falsifiable working hypothesis:** \(\theta>0\). A practical relevance gate requires a point estimate of at least \(0.0005\) in normalized count error *and* a paired confidence interval excluding zero in the predicted direction. This threshold is a **proposed preregistration parameter**, not a measured effect; revise it only using training/pilot data and then freeze it for an untouched confirmation set.

**Null / possible negative result:** \(\theta\le0\), or any effect smaller than the preregistered practical threshold; no evidence that drift amplifies adaptive error under the selected interface. This is a defensible reason to close, not to tune until positive.

**Novelty risk:** Medium-to-high. CCS 2023 already explores attack budgets and leakage; NDSS 2026 already evaluates adaptive attacks against monitors. An interaction effect must be checked against their actual experiments, not merely their abstracts.

**Why prioritize:** It is falsifiable using CPU-only infrastructure, builds directly on prior work without inventing a theorem, and yields useful negative results under a controlled design. Priority is **conditional** on confirming the specific interaction is not already established and that the attack is sensitive to the budget chosen.

### H4-B — Public-answer granularity and attack effectiveness

**Question.** At a fixed attack-query budget, how do exact-frequency responses, rounded responses, and heavily quantized responses affect adaptive frequency-estimation error and utility for benign queries?

**Working hypothesis:** Coarsening public answers decreases successful adaptive targeting more than it decreases benign accuracy at the same memory and CPU budget.

**Measurable endpoints:** adversarial error, benign query absolute error, latency, result-resolution loss, and leakage interface; preregister rounds and quantization thresholds. Avoid treating public output as an information-theoretically private mechanism.

**Fast refutation:** If matched defenses have no improvement in attack outcomes, or benign utility costs dominate, stop. **High prior-art overlap**: the CCS 2023 work already explores public/private information and query budgets. Detailed review is required before even calling this a candidate original contribution.

### H4-C — Resource-matched robustness/accuracy/throughput frontier

**Question.** After matching *actual resident bytes and update CPU*, how much error and attack success differ among CMS, HeavyKeeper, and Count-Keeper under one declared attacker interface?

**Working hypothesis:** The relative ordering of methods at equal physical resources differs from a ranking based on nominal sketch parameter settings.

**Measurable endpoints:** actual resident bytes including metadata and hash state, CPU time per update, point-query error, adaptively selected target error, and attack success rates. Baseline code must be pinned and audited for equivalence of update/query semantics.

**Fast refutation:** If the primary published benchmarks already match the same resources or reproduce the same ordering without a meaningful discrepancy, classify as replication/engineering, not a new research claim. **Very high prior-art overlap** with CCS 2023. It may remain valuable as reproducibility work but is not prioritized as a novelty claim.

## 4. Intended minimal experiment for H4-A — not executed

### Model and fairness controls

- **Stream:** insertion-only, unit-weight updates; fixed length \(m=100{,}000\) per run.
- **Honest/adversarial updates:** 90,000 honest insertions plus up to 10,000 adversarial insertions. The interleaving schedule is fixed before seeing final-test results; all updates count toward ground truth and the stated stream length.
- **Universe:** \(n=100{,}000\) distinct integer keys, deterministic keyed hashing with a recorded seed. The attacker has no direct access to private hash state in the black-box arm.
- **Query budget:** at most 256 public estimator queries per run, with identical query opportunity schedules across adaptive and oblivious arms. A query and an insertion are different resources and are counted separately.
- **CMS counter memory:** start with a 64 KiB raw counter budget and a secondary 256 KiB budget, fixed row count and allocated widths. Report **physical resident memory** including seeds, buffer allocations, any counter metadata, attack state, and exact-oracle metadata separately. Do not equate logical counter memory with total process RSS.
- **Seeds:** at least 30 paired seeds in the confirmation stage, with the same honest-update multiset and hash seeds across appropriate pairs; report paired difference distributions. Pilot seeds used to fix parameters must be excluded from final inference.
- **Workload:** two dominant-key groups, switched at the midpoint in the abrupt-drift arm and interleaved in the stationary arm; fixed marginal honest-update multiset per pair. A second, independently designed workload family is needed before a broad conclusion.
- **Attacker baselines:** (i) no adversarial insertions, (ii) nonadaptive/precommitted insertion and query schedule with the same budget, and (iii) feedback-adaptive budget-matched policy. A random-query baseline is useful but not a faithful substitute for a published attack.
- **Evaluation:** checkpoints fixed in advance, seed-independent fixed probe set for the primary error metric, and separate attacker-selected probe set as a secondary *attack* metric. Keep both worst-case and average errors; one max statistic can be unstable.

Do not claim that controlling the honest-update multiset means the **realized** streams are identical across adaptive arms: the adversary changes future updates and therefore the exact frequency vector. Exact ground truth must be recomputed for each realized arm.

### Statistics and precommitment

- **Primary endpoint:** paired interaction estimate \(\widehat\theta\) above, with a justified confidence interval over **independent seeds**. Within-run updates/checkpoints are temporally dependent and are *not* independent samples.
- **Secondary endpoints:** threshold exceedance probabilities at declared \(\varepsilon\), adversary-targeted error, attack query count, update throughput, resident memory, and benign-query error.
- **No cherry-picking:** define the probe set, checkpoints, attack stopping rule, search parameters, threshold, and principal comparator before exposing confirmatory results.
- **Comparability:** do not compare algorithms with different query semantics or target estimands; disclose hash implementation, counter overflow handling, update cost, and any language-dependent speed differences.
- **Practical stopping rule:** if the 30-seed paired confirmation shows no practically material positive interaction under two budgets, close H4-A. If positive only for one workload or budget, report narrowly; do not extrapolate.
- **Independence:** reproduce a published attack or canonical artifact first; run a faithful no-adaptivity control before interpreting any new attack.
- **Resource budget:** CPU-first (no GPU required), lightweight enough for a 2-vCPU / ~12 GiB RAM notebook or equivalent local runner. This is an engineering estimate, not a verified run-time guarantee.

### Implementation staging (approval gates)

| Gate | Required artifact | Pass criterion | If it fails |
|:--|:--|:--|:--|
| G0 — Prior art | Source-to-experiment matrix for [1], [2], [3]; pinned versions and licenses | Demonstrate that H4-A's specific *interaction estimand* is not already established | Reframe as replication or close |
| G1 — Reproduction | One faithful implementation/test of a published attack + exact oracle + no-adaptive baseline | Reproduces qualitative published behavior without mixing different attacker capabilities | Fix comparator or stop |
| G2 — Pilot | Small paired 2×2 factorial trial using training seeds only | Variation/budget sensitivity is measurable; code checks and exact ground truth pass | Rework within preregistered bounds or stop |
| G3 — Pre-registration | Frozen YAML/JSON manifest, hypotheses, workloads, seeds, primary metric and threshold | Independent review of leakage and fairness assumptions | Do not run confirmatory experiment |
| G4 — Confirmation | 30+ held-out paired seeds; resource accounting; raw data; CI | Predeclared scientific criteria assessed without post-hoc comparator changes | Publish negative result if unconfirmed |
| G5 — Publication audit | Re-check late-2026 literature and original upstream configurations | Any novelty claim supported beyond an obvious benchmark replication | Archive as technical replication |

**Immediate next step:** complete G0, not a new speculative ten-round debate and not a large implementation.

## 5. Decision and scientific integrity

**Recommended candidate:** H4-A (interaction between drift and adaptive feedback), **provisionally**. The project is *not yet accepted* as an original research study.

**Why not H4-B or H4-C first?** Both overlap directly with published disclosure-attack and comparative-estimator experiments. The safest contribution may be a careful replication or negative finding rather than a new algorithm.

**Acceptance criteria for a new research claim:** original, verified estimand or methodological contribution; reproducibility with pinned sources; matched baseline budgets; no leakage of final-test choices into the pilot; evidence under independent runs; clear limitations. A negative result is publishable here as a working technical report, without asserting it disproves the general phenomenon.

## References

[1] Sam A. Markelon, Mia Filić and Thomas Shrimpton (2023), *Compact Frequency Estimators in Adversarial Environments*, CCS. https://doi.org/10.1145/3576915.3623216 ; code https://github.com/smarky7CD/cfe-in-adv-envs

[2] Dragos-Florian Ristache and Krzysztof Onak (2025), *The Adaptive Use of Count-Min Sketch: What is Safe and What is Not?*, KDD. https://doi.org/10.1145/3711896.3737152

[3] Francesco Da Dalt and Adrian Perrig (2026), *Strategic Games and Zero Shot Attacks on Heavy-Hitter Network Flow Monitoring*, NDSS. https://doi.org/10.14722/ndss.2026.241301 ; code https://github.com/FrancescoDaDalt/HHNFM

[4] Omri Ben-Eliezer, Krzysztof Onak and Sandeep Silwal (2026), *Robust Streaming Against Low-Memory Adversaries*, ITCS. https://doi.org/10.4230/LIPIcs.ITCS.2026.16

[5] Sara Ahmadian and Edith Cohen (2024), *Unmasking Vulnerabilities: Cardinality Sketches under Adaptive Inputs*, ICML. https://proceedings.mlr.press/v235/ahmadian24a.html

[6] Edith Cohen, Jelani Nelson, Tamás Sarlós, Mihir Singhal and Uri Stemmer (2026), *One Attack to Rule Them All: Tight Quadratic Bounds for Adaptive Queries on Cardinality Sketches*, SODA. https://research.google/pubs/one-attack-to-rule-them-all-tight-quadratic-bounds-for-adaptive-queries-on-cardinality-sketches/

[7] Daniel Lukats, Oliver Zielinski, Axel Hahn and Frederic Stahl (2024), *A benchmark and survey of fully unsupervised concept drift detectors on real-world data streams*. https://doi.org/10.1007/s41060-024-00620-y

---

**Editorial note:** This proposal is deliberately literature-first. The existing CCS 2023 and NDSS 2026 experimental repositories make an unqualified "first adversarial frequency-sketch benchmark" claim untenable. No numerical results have been fabricated.
