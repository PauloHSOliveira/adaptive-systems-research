# Research 004 — Gate G0: Prior-Art and Experiment Audit

> **Final decision (2026-11-24): G0 CLOSED — NO-GO for H4-A2 as original research.** The earlier HOLD status below is historical and superseded by the [final G0 decision](G0_DECISION.md). No G1 or confirmatory experiment was approved; independent CCS 2023 replication remains a separately scoped option.

**Audit date:** 2026-11-23  
**Hypothesis:** H4-A — workload ordering / abrupt frequency-distribution shift × public-feedback adaptivity for Count-Min Sketch (CMS).  
**Gate decision:** **NOT PASSED — HOLD AND REFORMULATE**. No approval of originality or G1 implementation.

**Technical-text addendum (2026-11-23):** A complete but **anonymous** related Count-Min Sketch preprint is now accessible at [OpenReview](https://openreview.net/pdf?id=IuEBdNsWKb). Its value-based attacks, hashing assumptions and experiments have been examined in [KDD_PREPRINT_AUDIT.md](KDD_PREPRINT_AUDIT.md). Its identity with the final KDD 2025 article has **not** been authenticated. H4-A has been narrowed to [H4-A2, feedback-mediated terminal target error](H4-A2_REFORMULATION.md). The gate remains **NOT PASSED**. This addendum supplements (does not erase) the original access limitations below.  
**Evidence:** Primary GitHub experiment scripts from CCS 2023 and NDSS 2026, published abstracts and available article text for KDD 2025 and NDSS 2023, and an algebraic structural check. No new benchmarks or independent replication ran in G0.

This is a targeted audit, not an exhaustive systematic review. Failure to locate an experiment in the inspected source does not prove that the effect has never been published.

## 1. Original hypothesis and its claim

The [Study 004 proposal](../004-proposal.md) defines

\[
\theta=(\mu_{D=1,A=1}-\mu_{D=1,A=0})-(\mu_{D=0,A=1}-\mu_{D=0,A=0}),
\]

where D indicates abrupt workload drift versus stationary ordering, A indicates a feedback-adaptive attacker versus a precommitted attacker, and the original outcome was a peak CMS normalized point-frequency overestimate over several checkpoints.

The two honest workload arms were supposed to consist of **the exact same multiset**, reordered differently. The goal was to test whether access to public estimates makes adaptive attacks more effective during abrupt changes than during stationary arrivals.

This exact interaction was not identified in the particular CCS 2023 scripts inspected, but **its novelty has not been certified**. Previous work has already investigated attacks, changes in frequency distributions, and traffic-background influences on detector performance.

## 2. Source-to-experiment comparison

### CCS 2023: Markelon, Filić and Shrimpton — Compact Frequency Estimators in Adversarial Environments

**Pinned upstream revision:** [5e511f60015c2c1d3a10a950d94c58d2c988cc46](https://github.com/smarky7CD/cfe-in-adv-envs/commit/5e511f60015c2c1d3a10a950d94c58d2c988cc46). [MIT license](https://github.com/smarky7CD/cfe-in-adv-envs/blob/5e511f60015c2c1d3a10a950d94c58d2c988cc46/LICENSE).

**Inspected original scripts:**

- [experiments/attacks/private_private.py](https://github.com/smarky7CD/cfe-in-adv-envs/blob/5e511f60015c2c1d3a10a950d94c58d2c988cc46/experiments/attacks/private_private.py): feedback-driven CMS, HK and CK attacks, cover discovery, repeated inserts. The embedded main routine uses 100 trials, parameter pairs (2048,4) and (4096,8) for CMS, and 2^20 insertion budget.
- [experiments/attacks/public_public.py](https://github.com/smarky7CD/cfe-in-adv-envs/blob/5e511f60015c2c1d3a10a950d94c58d2c988cc46/experiments/attacks/public_public.py): a distinct stronger hash-public attack interface with direct hasher access and fixed key. The main routine specifies 2^20 insertions; a historical inline results comment refers to a different 2^16 budget. Do not conflate them.
- [experiments/test-cfes/run_experiments.py](https://github.com/smarky7CD/cfe-in-adv-envs/blob/5e511f60015c2c1d3a10a950d94c58d2c988cc46/experiments/test-cfes/run_experiments.py): honest CMS/HK/CK trials on retail, kosarak and novel workloads. Order is randomly shuffled and final per-item errors are reported. Artifact uses 50 trials; the README describes 1,000 trials per grouping in the paper.
- [streams/process_stream.py](https://github.com/smarky7CD/cfe-in-adv-envs/blob/5e511f60015c2c1d3a10a950d94c58d2c988cc46/streams/process_stream.py): retail/kosarak stream flattening and shuffling.
- [experiments/flag-ck/attack_experimemts.py](https://github.com/smarky7CD/cfe-in-adv-envs/blob/5e511f60015c2c1d3a10a950d94c58d2c988cc46/experiments/flag-ck/attack_experimemts.py): CK attack-flag behavior was already evaluated.

**Overlap:** High. Generic CMS adaptive attacks, public/private hash settings, CK defenses and simple attack budgets are prior art. A **factorial time-order × feedback interaction** was not identified in the audited scripts, but the literature search cannot prove its absence. Crucially, the upstream attack's budgets and feedback mechanisms are very different from our proposed 256 query / 10,000 insertion limits.

### KDD 2025: Ristache and Onak — The Adaptive Use of Count-Min Sketch: What is Safe and What is Not?

[DOI](https://doi.org/10.1145/3711896.3737152); [author's publication list](https://onak.pl/papers/). The publisher's full article was inaccessible in this environment. The accessible abstract reports positive findings for a random-oracle / cryptographic-hash regime and a constrained universal-hash regime, as well as value-based attacks and efficient collision techniques. These are abstract-level findings, **not a verified audit of the full theorem hypotheses, datasets or experiments**. No public source revision was pinned.

**Overlap:** High for attack techniques and for the hash-security model. **Blocking gap:** the complete paper and experiment definitions must be read before G0 can approve novelty.

### NDSS 2026: Da Dalt and Perrig — Strategic Games and Zero Shot Attacks on Heavy-Hitter Network Flow Monitoring

**Pinned revision:** [3e3b9a7246806fd01252d3cc6c800e343c55cf4d](https://github.com/FrancescoDaDalt/HHNFM/commit/3e3b9a7246806fd01252d3cc6c800e343c55cf4d).

- [paper_code/config/default.json](https://github.com/FrancescoDaDalt/HHNFM/blob/3e3b9a7246806fd01252d3cc6c800e343c55cf4d/paper_code/config/default.json): traffic simulation with num_DSA=1000, SWA.hhdcounters=100, NTA.blindmode=false and noacks=false.
- [paper_code/scripts/run_NTA_training.sh](https://github.com/FrancescoDaDalt/HHNFM/blob/3e3b9a7246806fd01252d3cc6c800e343c55cf4d/paper_code/scripts/run_NTA_training.sh): detector-specific one-sided adaptive attack training for nine detection systems.
- [paper_code/scripts/run_ZSA_evaluation.sh](https://github.com/FrancescoDaDalt/HHNFM/blob/3e3b9a7246806fd01252d3cc6c800e343c55cf4d/paper_code/scripts/run_ZSA_evaluation.sh): cross-detector zero-shot evaluation, including a real background traffic trace option.
- [Official paper summary](https://www.ndss-symposium.org/ndss-paper/strategic-games-and-zero-shot-attacks-on-heavy-hitter-network-flow-monitoring/): detector/attacker co-training, up to 299% bandwidth-cap breaches, 2.2x improvement through co-training and zero-shot evasion in 8/9 detection systems. Published experiment results discuss synthetic versus captured real background traffic effects.

**Overlap:** Substantial for the broader claim that *traffic context changes adaptive attack effectiveness*. Not equivalent to H4-A's CMS point-query error metric, because this work evaluates switch-level monitoring and rate limiting.

**License/reproduction:** The [LICENSE.md](https://github.com/FrancescoDaDalt/HHNFM/blob/3e3b9a7246806fd01252d3cc6c800e343c55cf4d/LICENSE.md) text grants MIT-style permission, but the pinned README retains obsolete language about a temporary artifact-evaluation license. Resolve any ambiguity before redistributing code. The repository uses a git submodule and optional MOSEK; README quickstart mentions some scripts absent from the pinned repository tree.

### NDSS 2023: Kim et al. — A Robust Counting Sketch for Data Plane Intrusion Detection

[Official publisher page](https://www.ndss-symposium.org/ndss-paper/a-robust-counting-sketch-for-data-plane-intrusion-detection/).

Count-Less studies changing frequency-size distributions (FSDs) within a stream and during attack traffic and designs a data-plane counting sketch to tolerate diverse skew without reconfiguration. Figures and discussion explicitly describe distributions changing across time windows and between benign/attack traces.

**Overlap:** The drift/FSD dimension is prior art. This is **not evidence** that the exact CMS adaptive-feedback interaction in H4-A was previously measured. The implementation and full experiment matrix were not pinned here.

### Additional contextual sources

[Time Adaptive Sketches](https://cs.rice.edu/~as143/Papers/16-ada-sketches.pdf) investigates time/recency-dependent sketching; [CountSketch robustness](https://proceedings.mlr.press/v162/cohen22a.html) studies adaptive inputs for a distinct sketch; [ITCS 2026](https://doi.org/10.4230/LIPIcs.ITCS.2026.16) formalizes memoryless versus bounded-memory attackers. These prevent broad novelty or adversary-model claims.

## 3. A structural flaw in the proposed experiment

For ordinary insertion-only CMS with fixed hash functions h_j,

\[
C_{j,b}(t)=\sum_x f_x(t)\mathbf{1}[h_j(x)=b],
\quad
\widehat f_t(x)=\min_j C_{j,h_j(x)}(t).
\]

If two runs have **identical final frequency vectors and identical hash functions**, their final counter states and point queries are **exactly equal**, no matter the order of updates.

Therefore:

1. With the same full multiset of honest updates and the same precommitted attack multiset, **terminal CMS error is order-invariant**. There is no intrinsic terminal "drift sensitivity" for this configuration.
2. Intermediate checkpoint states can differ between stationary and drift-order runs because their **partial frequency vectors are different**. A checkpoint error difference is not, by itself, proof that drift increases adaptive vulnerability.
3. Only if the feedback-adaptive attack uses intermediate information to choose **different future updates** can different orderings induce different terminal point-frequency error. That is a much narrower causal question about *feedback-mediated attack trajectories*.
4. The original peak-over-checkpoints primary outcome risks comparing unmatched partial frequency vectors and denominators.
5. A public hash function, a fixed seeded hash function and a cryptographically hidden hash function are different threat models. A random seed alone does not establish secrecy or cryptographic resistance.

**Required reformulation:** Fix an attack target identifier *before* hash-seed sampling; equalize total update counts and honest multisets; measure terminal normalized target error as primary endpoint; preserve matched public query schedules and separate benign probes/checkpoints as secondary endpoints. Explicitly label attacker transcript memory and hashed-interface access. The original H4-A requires a new preregistration; do not patch it silently after observing confirmation outcomes.

## 4. Budget feasibility warning

The CCS 2023 reference attack code uses up to 2^20 insertion operations in the displayed configurations and repeatedly queries for collision discovery. Our initial proposal specifies 10,000 attacker insertions and 256 public queries. The smaller budgets may yield no measurable error even if the tested vulnerability is real.

A negative outcome under such budgets is not a refutation of published adaptive attacks. Before any confirmatory study, **measure attack feasibility in a separate, non-confirmatory budget pilot** and freeze the selected budget without consulting held-out results.

## 5. Gate decision

| Requirement | Result | Rationale |
|:--|:--|:--|
| Identify and pin main experiment repos | PARTIAL PASS | CCS 2023 and NDSS 2026 commits pinned; KDD full paper and NDSS 2023 artifacts incomplete |
| Check exact experiment overlap | INCOMPLETE | No full KDD experimental methods review |
| Show an original question | UNPROVEN | Adaptive attacks, FSD changes and traffic-context sensitivity all already studied |
| Establish identifiable, valid primary metric | FAIL AS WRITTEN | CMS order-invariance and checkpoint differences undermine the proposed interpretation |
| Verify feasible attack budget | NOT TESTED | Proposed budget much smaller than principal CCS examples |
| Confirm licensing and reproducibility prerequisites | PARTIAL PASS | Relevant licenses and dependency caveats documented |

**Overall: G0 NOT PASSED. H4-A is ON HOLD, not approved for G1.**

This is not a proof that the narrowly reformulated interaction is already in the literature, nor a claim that no useful replication exists. It is a decision that the present evidence is insufficient to approve the study as original.

## 6. Recommended next decision

1. **Do not implement the full benchmark yet.** Obtain/inspect the complete KDD 2025 article or an authorized author manuscript and finish its source-to-experiment audit.
2. Evaluate a refined, narrowly specified question: do different *time permutations of the same honest multiset* lead a fixed feedback-adaptive attacker to produce measurably different **terminal target errors**, with the attack's future inserted multiset allowed to change?
3. If the effect and novelty cannot be distinguished from existing works, either close H4-A or explicitly run a **replication-only** project. Replication is valuable but is not a novel algorithm.

No experimental outcomes or publication originality claims are asserted.

## Evidence access limits

Primary CCS/NDSS experiment scripts and their commits were inspected directly. Some journal PDFs and visual screenshots were not retrievable, and KDD 2025 detailed methods were not available. The official paper abstracts plus pinned source code support the overlap assessment; they do not constitute a complete independent review.
