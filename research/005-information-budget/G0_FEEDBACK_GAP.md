# Study 005 — G0-E: Separating Feedback Loss from the Shared-Reuse Relaxation

**Date:** 2026-11-24  
**Status:** Restricted mathematical feasibility result for H5-B. No G1 approval or verified originality claim.  
**Predecessor:** [G0-D row envelope](G0_ROW_ENVELOPE.md).

> **G0-F follow-up:** [Poisson-regime result](G0_POISSON_GAP.md) proves a nonvanishing lower bound for the relative information gap when R=2, K=1 and (M-1)/B approaches a positive constant. The M=3 gap fraction p^2 below must not be extrapolated to this joint scaling. The exact scalar optimum and novelty clearance remain unresolved.

## 1. Scope

Retain the classical additive insertion-only CMS with a fixed absent target, R rows, B buckets, independent uniform hashes, and M unit insertions. No candidate is pre-queried, no hash internals are initially revealed, and the domain has at least M admissible non-target identifiers. Let p=1/B, a=1-p. Restrict this audit to **at most one repeat (K=1)** and observations after each insertion except the last. Each previously unseen identifier has an independent R-dimensional Bernoulli(p) collision vector. Only terminal normalized collision error Y is optimized, not intermediate regret or another objective.

Compare three quantities for the same terminal objective:
- Scalar-feedback optimum S: only the minimum target bucket count is observed, with perfect recall.
- Row-feedback optimum O: a hypothetical stronger interface reports every target row count. This is an analytical relaxation, not a proposed deployment or a description of normal CMS.
- Row-envelope upper bound E: the G0-D independent-row relaxation, summed over integer thresholds for the mean.

For each threshold, the scalar and row-feedback optima are defined separately by supremizing its event probability. For the mean, optimize the expected value directly. In either case S <= O <= E. The two gaps distinguish the value of extra observation from looseness of the independent-row reuse relaxation.

## 2. Reduction to a terminal repeat decision

**Lemma.** For K=1, under either observation interface and for any terminal objective depending only on the final minimum, a policy can be replaced without reducing its expected objective by a policy that inserts M-1 fresh identifiers before deciding whether the final insertion is fresh or repeated.

Proof: Consider the first intended repeat of any causal policy. If it occurs before the last insertion, all subsequent insertions under that policy must be fresh. Instead of executing the intended repeat, store its identifier, insert fresh keys for the remaining preterminal slots, and execute the stored repeat in the last slot. Conditional on the past, the requisite future fresh collision vectors are independent with the same law as in the original policy, even if their labels would have been selected adaptively. Addition commutes, so the final minimum has the same conditional law. The transformed policy ignores later observations on that branch. If there is no intended early repeat, it can emulate the original policy up to its last decision. This construction is causal and does not increase the reuse budget; arbitrary recall is allowed. Thus restricting to this class does not decrease the supremum. The reverse inequality holds by inclusion. QED.

This is a distributional equivalence, not equality for a fixed externally chosen hash map and arbitrary identifier labels. It fails as a general statement for K>1, limited memory, intermediate objectives, or access to already probed but uninserted identifiers.

## 3. Exact row-feedback optimum, arbitrary number of rows

Let L=M-1. After L fresh insertions, denote their row-collision totals by c_j and m=min_j c_j. Let J={j:c_j=m}. Define A to be the event that among the L observed collision vectors, at least one has a collision in every row in J.

Given the observed vectors, the best final minimum equals m+1 with conditional probability

\[
\alpha=\mathbf 1_A+(1-\mathbf 1_A)p^{|J|},
\]

and otherwise equals m. Reason: a repeat can increase the minimum iff its vector covers all current bottleneck rows. If this is impossible, a fresh vector increases the minimum with probability p^|J|. All entries are binary, so the minimum cannot increase by more than one. The same comparison is optimal for every monotone terminal reward. By Section 2 this solves the row-observation relaxation for arbitrary R and M with K=1.

Hence the exact optimal row-observation tail and mean are

\[
O_z=\Pr(m\ge z)+\mathbb E[\mathbf 1_{\{m=z-1\}}\alpha],
\qquad
O=\frac{\mathbb E[m+\alpha]}{M}.
\]

The expectation is over L independent collision vectors only. In contrast to G0-D, this respects the shared repeat budget; in contrast to scalar feedback, it grants individual row observations. It remains an upper bound for scalar feedback.

### 3.1 Explicit two-row expression

Let b_s=Pr(Binomial(L,p)=s), G_z=Pr(Binomial(L,p)>=z), and

\[
D_s=\frac{\binom{L-s}{s}}{\binom Ls},
\quad s=0,\ldots,L,
\]

where the numerator is zero when 2s>L. Conditional on equal row counts s, the row support sets are independent uniformly chosen s-subsets of the L identifiers, so D_s is their probability of being disjoint. For s=z-1, the exact tail becomes

\[
O_z=G_z^2+2b_sG_z\,\beta_s
+b_s^2[1-(1-p^2)D_s],
\quad
\beta_s=\begin{cases}p&s=0,\\1&s>0.\end{cases}
\]

If counts differ, only the smaller row is a bottleneck; when its count is positive a previously seen collision exists. If tied, both rows must be covered, and a repeat can do this precisely when their support sets intersect. Sum O_z for z=1,...,M and divide by M for the exact mean.

The earlier envelope is strictly looser for R=2, M>=3 and 0<p<1: for example, the first L vectors can consist of one (1,0), one (0,1), and zeros otherwise. Both independent row envelopes permit terminal minimum 2, while the row-aware terminal decision reaches 2 only with probability p^2. The conditional optimum never exceeds the independent-row relaxation on the coupled fresh vectors; the positive-probability event yields a strict gap.

## 4. Exact decomposition in the smallest nontrivial two-row case

Fix M=3, K=1, R=2. Write S,O,E for optimal expected normalized scalar-feedback error, row-feedback error, and the G0-D envelope mean, respectively.

\[
\boxed{O-S=\frac{2p^4(1-p)^2}{3}},
\qquad
\boxed{E-O=\frac{2p^2(1-p)^2(1-p^2)}{3}}.
\]

Thus E-S=2p^2(1-p)^2/3, and the fraction of this particular bound gap attributable to observation loss is p^2.

**Proof of first identity.** By Section 2 the first two inserts can be fresh. Let their scalar observations be y_1,y_2. If y_1=1, a vector covering both rows is known and row observation adds no value. If y_2=0, at least one row has no collisions, so no repeat can improve the minimum and both interfaces favor a fresh final vector. The remaining ambiguous history is (y_1,y_2)=(0,1).

The possible vector pairs on this history form three classes:
- (00,11), probability a^2 p^2;
- (10,11) or (01,11), aggregate probability 2p^3 a;
- (10,01) or (01,10), aggregate probability 2p^2 a^2.

These are unconditional weights of disjoint histories. The row-feedback optimum can attain the increment with certainty in the first two classes, and with probability p^2 in the third. Under scalar feedback, the repeat of the first vector never increases the minimum in this history. The repeat of the second vector contributes an increment in the first two classes; a fresh vector has weighted increment 3p^4a^2+2p^4a. The weighted difference between the second-vector repeat and the fresh choice is p^2 a^2(1+2p-3p^2)=p^2 a^3(1+3p)>0. Therefore scalar optimality loses only the third-class probability times p^2. Divide by the three inserts for the first identity.

**Proof of second identity.** On the same two fresh vectors, the G0-D envelope and the row-feedback optimum coincide in their tail at z=1 and z=3. At z=2 they differ exactly on the complementary single-collision class: the envelope reaches 2 with certainty there, while a fresh final vector raises both rows with probability p^2. This gives 2p^2a^2(1-p^2) before dividing by three. QED.

For B=2: S=27/64, O=83/192, E=89/192. The information gap is 1/96 and the independent-row relaxation gap is 1/32. These are exact expected normalized values for an artificial finite model, not empirical production-security measurements.

**Important:** The gap fraction p^2 is proved only for M=3, K=1, R=2. In this case it tends to zero as B grows. It is not a general claim that the minimum operator always contributes little security.

## 5. Exact computational checks

The local standard-library verifier enumerates weighted collision patterns and optimizes all deterministic causal scalar-feedback policies via a belief-state dynamic program. The finite domain has M potential identifiers; unseen keys are exchangeable. Posterior weights are inherited from the independent Bernoulli distribution; all results use integer/rational arithmetic. Independent randomized policies cannot improve the supremum of the linear expected reward. The stronger row-feedback comparator uses the analytical formula in Section 3. Each mean and threshold is independently optimized in the scalar model.

Executed results:
- 33 configurations: M=2..5, R=1..3, B in {2,3,4}, with R*M<=12, K=1.
- 144 mean/threshold comparisons: all passed S<=O<=E; R=1 equality verified.
- 15 configurations with strict mean S<O, and 15 with strict mean O<E.
- 18 additional exact comparisons of the two gap formulas in Section 4, for B=2..10: all passed.

Selected B=2, R=2 mean results:

| M | Scalar optimum S | Row-feedback optimum O | Row envelope E |
|--:|--:|--:|--:|
| 2 | 13/32 | 13/32 | 13/32 |
| 3 | 27/64 | 83/192 | 89/192 |
| 4 | 449/1024 | 471/1024 | 489/1024 |
| 5 | 2281/5120 | 479/1024 | 2449/5120 |

Run the verifier from the repository root:

    python research/005-information-budget/code/verify_feedback_gap.py

Local execution completed on 2026-11-24. No external system or published attack reproduction was involved. This verification supports the restricted analytical claims but is not itself a general proof.

## 6. Literature and decision

Partial monitoring and information-directed decision-making are established mathematical fields, e.g. Kirschner, Lattimore and Krause, *Information Directed Sampling for Linear Partial Monitoring*, COLT 2020, https://proceedings.mlr.press/v125/kirschner20a.html ; and *Linear Partial Monitoring for Sequential Decision Making: Algorithms, Regret Bounds and Applications*, JMLR 2023, https://jmlr.org/papers/v24/22-1248.html . Their general frameworks are not novel to this project. The target-specific terminal objective and hard repeat cap differ from their usual regret objectives, but that distinction does not certify originality.

Relevant CMS prior art remains CCS 2023 (https://doi.org/10.1145/3576915.3623216) and KDD 2025 (https://doi.org/10.1145/3711896.3737152 ; bibliographic record https://dblp.uni-trier.de/rec/conf/kdd/RistacheO25.html). The definitive KDD full text and preprint lineage remain unresolved from earlier gates. This targeted search did not establish that the exact decomposition is absent from published work.

**Decision:** H5-B now has a precise and nonzero information gap in a restricted mathematical model, and an exact stronger row-feedback comparator for K=1 and arbitrary R. The result is useful for evaluating how much protection comes from the interface rather than the resource budget. It does not establish a general sharp scalar-feedback bound, a new defense, or publication originality. The next candidate is the asymptotic size of S versus O for a fixed reuse budget, particularly whether the information gap persists beyond the minimal case in regimes relevant to sketch sizing. First investigate K=1 for growing M and B, rather than jump immediately to general K or a production benchmark. Formal G1 remains blocked by novelty clearance.
