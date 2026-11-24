# Study 005 — Internal Proof and Reproducibility Audit

**Date:** 2026-11-24  
**Verdict:** Suitable for independent mathematical review as a working manuscript. Not a novelty or publication sign-off.  
**Manuscript:** [paper.md](paper.md).  
**Reviewed historical revision:** [eb2e9f5b4f8e6fd9210392ae9a7dc07928b1a9e8](https://github.com/PauloHSOliveira/adaptive-systems-research/tree/eb2e9f5b4f8e6fd9210392ae9a7dc07928b1a9e8/research/005-information-budget).

This audit is an internal second-pass review, not an independent referee report. No external reviewer was contacted. The formal G1 gate and publication originality remain unapproved. The six source documents and six verifiers were retrieved from the repository; all source blobs used in the rerun matched their pinned Git blob IDs.

## 1. Claim ledger

| ID | Claim | Review finding | Required assumptions / remaining concerns |
|---|---|---|---|
| C01 | Mutual-information expectation and KL event transfer | Algebra and conditioning checked; finite relaxed-selector verifier passes | Fixed target, independent random hashes, deterministic concentration ceiling; standard prior art |
| C02 | Transcript-size information ceiling | Valid for fixed query schedule and hash-independent private randomness | Must not infer private-memory-bit ceiling; all other disclosure channels excluded |
| C03 | Fresh-vector and repeat-budget stochastic envelope | Deferred-decision coupling and pathwise row inequalities checked | Enough fresh keys; no pre-query of candidates; ideal hashes; cap holds on every realization |
| C04 | One-row full-feedback optimum | Upper envelope attainment and tail sum checked | Arbitrary recall, complete feedback; not general R |
| C05 | Terminal-repeat reduction | Conditional equality in distribution checked | Only K=1, terminal objective, full recall, enough keys; no equality claim for fixed arbitrary hash maps |
| C06 | Exact row-feedback comparator | Bottleneck support condition and conditional fresh probability checked | Hypothetical row observation, K=1 |
| C07 | M=3 two-row gap identities | Ambiguous history and weighted comparisons checked; finite tests pass | Not a general gap fraction |
| C08 | Finite lower bound and shared-budget identity | Disjoint event weights and discrete Poisson limit checked | R=2, K=1; normalized gap vanishes |
| C09 | Exact Poisson-regime information gap | Excursion-sign symmetry, last-visible comparison, hidden-slot symmetry, uniform error control and final walk enumeration checked internally | Strongest result; ask independent reviewer to scrutinize conditioning, policy measurability and uniformity of error bound |
| C10 | Finite no-double comparator gap | **Presentation correction required**; see Section 2 | Earlier displayed values are excursion term only, not the complete finite regret |
| C11 | Originality | **Unresolved** | Definitive KDD 2025 full text inaccessible; prior-art search not exhaustive |
| C12 | Production relevance | **Not demonstrated** | No deployment, production benchmark, unrestricted attack evaluation, or cryptographic guarantee |

The original G0-C numerical table uses only three admissible non-target identifiers and four inserts; it is a separately declared finite domain where K>=1 is necessary. Its values must not be combined with the M-key models in G0-D onward as if the domains were equal. No mathematical contradiction follows from the different optima. A finite test's passing does not prove a general proposition.

## 2. Correction to G0-G finite comparison

The asymptotic formula is unchanged. The earlier G0-G numerical evaluation labeled as "conditional no-double last-visible regret" actually computed only

\[
g_{L,p}=\tfrac12\Pr(C\mid D_0).
\]

Here D0 excludes double collisions among the preterminal L fresh vectors. C is the event that the terminal minimum is positive, the terminal rows are unequal, and the final unfinished excursion has no visible step. The **full** conditional expected difference between the row-aware optimum and the last-visible comparator equals

\[
g_{L,p}+p^2\Pr(c_1=c_2>0\mid D_0).
\]

On a positive terminal tie the comparator repeats a known visible key, which covers just one row on D0; a fresh final insertion succeeds with probability p^2 for the row-aware optimum. At terminal minimum zero the comparator and oracle both choose a fresh insertion. On unequal positive rows the excursion term already accounts for the entire conditional difference. The final fresh vector is not conditioned to exclude double collisions.

The omitted correction is at most p^2, hence tends to zero. The G0-G limit and proof of convergence remain valid; the finite labels need this qualification. The consolidated manuscript incorporates the corrected identity.

With L=B (lambda approximately 1):

| B | Excursion term (earlier table) | Omitted tie term | Full conditional gap |
|--:|--:|--:|--:|
| 16 | 0.061746415549 | 0.000683763288 | 0.062430178837 |
| 64 | 0.066314113653 | 0.000042389334 | 0.066356502988 |
| 256 | 0.067432403491 | 0.000002644130 | 0.067435047621 |
| 1024 | 0.067710552900 | 0.000000165178 | 0.067710718078 |
| 4096 | 0.067780002057 | 0.000000010322 | 0.067780012380 |

These are numerical series evaluations, not interval-certified decimals. The exact identity was checked in 28 finite configurations using rational weights over all 3^L no-double sequences. See [audit_exact_gap.py](code/audit_exact_gap.py).

## 3. Reproduction record

Python 3.13.5, standard library only; all six historical files matched the Git blob hashes below using git hash-object. Direct raw-GitHub network access from the local runtime failed DNS, so the source was retrieved using the GitHub connector and exact local copies reconstructed/verified against the hashes. Each file was executed locally and exited with status 0. The table records the actual pinned historical source; no later unverified version is represented as tested.

| File | Git blob SHA-1 | Observed result |
|---|---|---|
| verify_finite_selectors.py | ae014c97d9aa4d2d11139b51687eea7a2949354d | 65,536 selectors; max success 0.4375; max KL minus I 0 |
| verify_operational_model.py | 3a794c2a5e837b17e72a5023a292c5634f413360 | 9 mean and 36 tail checks; transcript capacities 2947.311479 and 1528.397820 nats |
| verify_row_envelope.py | 98145e1f749c7760b647037163d766f925b3dfeb | PASS: 210 one-row and 76 two-row comparisons |
| verify_feedback_gap.py | f7f593bd0a1f7c6ce5f888ecc7d51590420bdf10 | 144 mean/tail checks and 18 closed-form comparisons; 15 strict mean gaps in each comparison |
| verify_poisson_gap.py | 28a585da42f5456698a2be8306ee00b120006c97 | PASS: 28 exact finite configurations |
| verify_poisson_exact.py | 7c962644ad81ca22850522356a39ee81ed2f5920 | PASS: 15 exact walk counts and 28 finite comparisons |

The original last script's finite output labels should be interpreted using Section 2. The marked-walk enumeration verifies the count of C, not a general independently derived proof of optimality. The convergence-error inequality is checked on small models, not established by those checks alone. The finite-selector entropy and numerical series checks use floating point; all finite collision objective comparisons use integer/rational arithmetic. The comparison counts are not independent statistical samples and should not be aggregated into a p-value.

To reproduce from the pinned revision (or use current versions while checking any changes):

    for f in research/005-information-budget/code/verify_*.py; do
      python "$f" || exit 1
    done

Additional correction verification:

    python research/005-information-budget/code/audit_exact_gap.py

The extra script was run locally and printed PASS: 28 exact conditional-gap identities. The raw outputs are not a peer-reviewed dataset.

## 4. Targeted prior-art audit

Rechecked current metadata and accessible abstracts for the following during consolidation:

- Russo and Zou (2016), https://proceedings.mlr.press/v51/russo16.html : mutual-information adaptive bias; Proposition 1 is a specialization.
- Cohen et al. (2022), https://proceedings.mlr.press/v162/cohen22a.html : adaptive robustness of CountSketch, a distinct estimator.
- Ben-Eliezer, Onak and Silwal (2026), https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ITCS.2026.16 : bounded-memory adaptive adversaries. Full recall in this study is not a low-memory guarantee.
- Ristache and Onak (2025), https://dblp.uni-trier.de/rec/conf/kdd/RistacheO25.html and https://ristache.com/publications/ : official bibliographic record and author page; the related anonymous manuscript at https://openreview.net/pdf?id=IuEBdNsWKb does not authenticate the final KDD text. The current search did not resolve the earlier full-text blocker.
- Markelon et al. (2023), https://doi.org/10.1145/3576915.3623216 : adaptive frequency estimators, previously inspected pinned artifact; no general first-attack or first-robustness claim.

Search terms included combinations of Count-Min Sketch, adaptive feedback, minimum, collision, row counter, reuse/repeat, information, and Poisson. No exact result matching the restricted formula was found in the surfaced records. This is not a systematic review or evidence that it is new. Classical marked walks, Poisson limits, information bounds and partial monitoring are established tools. The paper does not require attributing unverified detailed theorem statements to the KDD publication.

## 5. Independent referee checklist

A qualified reviewer should be given the manuscript, this ledger, the scripts, and the primary sources. Ask for a written decision on each of the following, including explicit counterexamples if possible:

1. Is the fresh-vector coupling valid with causal label choices, after conditioning on the target hashes and private randomness?
2. Does postponing the only repeat preserve the conditional terminal law for every terminal objective, and are the observations/label choices sufficiently restricted?
3. Is the full-row comparator exact when bottleneck rows are tied? Are all zero-count cases handled correctly?
4. Is the conditional excursion-sign symmetry applicable to every visible choice measurable from the scalar history?
5. Do the hidden-slot placements remain uniform given the stated information, and does the short-block union bound cover adjacent visible steps and endpoints? Is the approximation bound genuinely uniform over all scalar policies?
6. Are the finite tie correction and double-collision error treated separately, and does their total vanish under Lp->lambda?
7. Does the marked-walk count enumerate disjoint last-zero events without double-counting, and is the interchange of limits and expectations justified?
8. Is the exact formula or an equivalent theorem already present in CMS adaptive robustness, reservoir bandits, partial-monitoring, or random-walk literature?
9. Does the one-repeat, full-recall, fixed-absent-target model represent a sufficiently meaningful theoretical contribution on its own? Identify which extension would be necessary if it does not.

**Acceptance rule:** a referee's mathematical approval is necessary but not sufficient for a novelty claim. Obtain the definitive KDD paper through lawful access or author-supplied manuscript and compare its model/results. Address all critical proof objections before moving to new experiments, and do not label the manuscript accepted or peer reviewed. If no meaningful novelty survives, archive as an internally verified exploratory note. The next stage is external review, not additional unchecked mathematical expansion.
