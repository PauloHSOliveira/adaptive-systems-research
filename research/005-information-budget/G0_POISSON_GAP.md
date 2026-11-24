# Study 005 — G0-F: A Nonvanishing Relative Feedback Gap in the Poisson Regime

**Date:** 2026-11-24  
**Status:** Restricted mathematical result; originality not certified; formal G1 remains blocked.  
**Predecessor:** [G0-E: Feedback-gap decomposition](G0_FEEDBACK_GAP.md).

## 1. Model and question

Use the G0-E model without modification: classical additive insertion-only Count-Min Sketch, two rows (R=2), B>=2 buckets per row, a fixed absent target independent of the fully random hashes, M total unit insertions, at most one repeat (K=1), no pre-probed identifiers or other hash disclosures, and full scalar feedback after each insertion except the last. The policy has perfect recall and enough available identifiers. Every fresh identifier's two collision indicators are independent Bernoulli(p), p=1/B, conditional on prior revelations and target hashes. No production system is involved.

Write L=M-1, a=1-p. Let S be the optimal expected normalized terminal error with scalar minimum feedback; O the corresponding optimum in the stronger hypothetical row-observation interface; E the G0-D row-envelope mean. They depend on M,B. Thus S<=O<=E. Multiplication by M gives errors in counts.

By the terminal-repeat reduction in G0-E, the optima S and O can be computed with L distinct inserts followed by a single terminal choice of a fresh identifier or a repeat. Fresh vectors may be labeled by their insertion order, without loss of generality; adaptive label selection does not change the conditional distribution of a new vector. Independent private randomization cannot improve a linear expected-reward optimum.

The earlier identity (O-S)/(E-S)=p^2 was proved only for M=3. We ask whether the relative gap still vanishes when both B and M grow, with

\[
 B\to\infty,\qquad L/B\to\lambda\in(0,\infty).
\]

## 2. A finite lower bound on the value of row feedback

Let V_i be the collision vector at fresh insertion i. Consider disjoint events indexed by 2<=t<=L-1:

- Exactly three fresh vectors are nonzero, all singleton collisions.
- One is at i<t in one row; the second is at t in the other row; the third is at k>t in that same other row.
- All remaining vectors are (0,0).

The orientation of the rows can be either of the two possibilities. Each event has probability

\[
 w_t=2(t-1)(L-t)p^3a^{2L-3}.
\]

The entire scalar history is zero before t and one from t onward. The final row totals are (1,2) up to permutation. The row-observing policy can obtain one additional count with certainty, because the sole collision in the bottleneck row has been identified.

Conditional on the specified event and t, the index i of that sole bottleneck collision is uniform among the t-1 earlier indices. The scalar transcript is identical for all these indices. A repeated index can therefore increase the minimum with conditional probability at most 1/(t-1). A fresh final vector increases it with probability p. This bound holds even for a policy that knows the event occurred; conditioning on independent private coins does not reveal i. Thus every scalar policy has expected regret relative to the optimal row-aware decision at least 1-max(p,1/(t-1)) on this event. Regret relative to that row-aware decision is nonnegative on every other configuration, after averaging over the independent final fresh vector. Consequently,

\[
 M(O-S)\ge \sum_{t=2}^{L-1} w_t[1-\max(p,1/(t-1))].
\]

This is a lower bound, not a formula for the optimum scalar policy. In particular, using max(x,y)<=x+y and summing,

\[
 \boxed{M(O-S)\ge
 \max\{0,\ 2\binom{L}{3}p^3a^{2L-3}(1-p-3/L)\}.}
\]

For L<3 the event sum is empty and the lower bound is zero. For L>=3 the identity sum_{t=2}^{L-1}(L-t)=binom(L-1,2) proves the 3/L term. The stronger finite sum is used in the exact diagnostic.

## 3. Exact finite shared-budget gap

Let c_1,c_2 be the row totals after the L fresh inserts, m=min(c_1,c_2). The row-envelope random variables for K=1 are W_j=c_j+1 if c_j>0, and the additional independent fresh collision indicator if c_j=0.

If m=0, the expected minimum envelope equals the row-aware optimum: a fresh vector is necessary to cover all zero-count rows. If m>0 and the row totals differ, a repeat can certainly cover the unique bottleneck, and the envelope and row-aware optimum both yield m+1. If c_1=c_2=s>0, the envelope yields s+1; the row-aware optimum does so with certainty only if some fresh identifier collided in both rows, and otherwise with probability p^2. Consequently the exact identity is

\[
 \boxed{M(E-O)=(1-p^2)
 \sum_{s=1}^{\lfloor L/2\rfloor}
 \binom Ls\binom{L-s}s p^{2s}a^{2L-2s}.}
\]

The sum is the probability of equal positive row totals with disjoint collision supports. This is another derivation of the relevant consequence of the G0-E row-aware formula, and does not assert that row feedback is available in ordinary CMS.

## 4. Asymptotic result

### 4.1 Information gap

Since Lp->lambda and p->0,

\[
 2\binom L3 p^3(1-p)^{2L-3}(1-p-3/L)
 \longrightarrow \frac{\lambda^3e^{-2\lambda}}3=:g(\lambda)>0.
\]

Therefore

\[
 \boxed{\liminf M(O-S)\ge g(\lambda).}
\]

The exact value of the scalar optimum or limit of M(O-S) is not established here.

### 4.2 Shared-repeat gap

The independent row totals converge jointly to independent Poisson(lambda) random variables N_1,N_2. The probability of any double collision among the first L vectors is at most Lp^2->0. Thus the finite probability of equal positive counts with disjoint support converges to P(N_1=N_2>=1), and

\[
 \boxed{\lim M(E-O)=
 d(\lambda)=e^{-2\lambda}\sum_{s=1}^\infty \frac{\lambda^{2s}}{(s!)^2}>0.}
\]

To justify the equality-event convergence, use joint convergence of the discrete count probabilities and truncate both counts at a fixed integer cutoff; the omitted mass is uniformly small by the bounded expectations. This uses the classical binomial-to-Poisson limit, not a new probability theorem.

### 4.3 Relative significance

By monotonicity of x/(x+y) in x>=0 and continuity at positive y,

\[
 \boxed{\liminf\frac{O-S}{E-S}
 \ge\frac{g(\lambda)}{g(\lambda)+d(\lambda)}>0.}
\]

The denominator is positive for sufficiently large B by the lower bounds above. The normalized absolute gaps are O(1/M): after L fresh updates, at most one more count can be gained. Thus the result is about a nonvanishing **relative** contribution and a count-scale gap, not a constant normalized error rate. It cannot be extrapolated to arbitrary K, R, query schedules, memory limits, nonideal hashing, or production risk.

For example, lambda=1 yields g=0.0451117611 counts and d=0.1731730393 counts; the lower bound on the relative contribution is 0.2066646922. At lambda=1.5 this lower bound is approximately 0.22474. These are lower bounds, not exact proportions.

## 5. Computational validation

Local standard-library Python execution on 2026-11-24:
- 28 configurations: L=2..8 and B in {2,3,4,8}.
- Exact enumeration of all 4^L collision-vector sequences (integer probability weights). Group sequences by their entire scalar history, sum terminal-decision rewards, and maximize the weighted expected increment over admissible actions for each group. This computes S exactly under the G0-E reduction; O is computed by maximizing with row observations.
- All 28 checks of the finite lower bounds and exact shared-budget identity passed. Fractions are exact; asymptotic values and larger finite formula evaluations use floating point.
- Evaluate the finite formulas also at L=B in {16,64,256,1024,4096}. No enumeration or Monte Carlo was used for these large values.

| B=L | Simplified lower bound on M(O-S) | Exact shared-gap formula M(E-O), numerically evaluated |
|--:|--:|--:|
| 16 | 0.03155632 | 0.16377568 |
| 64 | 0.04161925 | 0.17089282 |
| 256 | 0.04423263 | 0.17260752 |
| 1024 | 0.04489161 | 0.17303195 |
| 4096 | 0.04505670 | 0.17313778 |
| limit | 0.04511176 | 0.17317304 |

These verify finite algebra and illustrate convergence of the **bounds/formulas**, not numerical convergence of the unknown scalar optimum.

Reproduce:

    python research/005-information-budget/code/verify_poisson_gap.py

## 6. Scientific interpretation, prior art and next gate

The earlier small-M result does not support general extrapolation that minimum-only feedback becomes negligible as B grows. In the sparse regime with L/B->lambda, the present lower bound shows that feedback can account for a nonvanishing relative share of the total row-envelope gap, even with one repeat.

This is a restricted theorem about value of information in a collision model. The method uses elementary conditional exchangeability, the terminal-repeat reduction, and standard Poisson limits. Related background includes the G0-E partial-monitoring literature and the classical Poisson process/counting theory (e.g. Gallager, Discrete Stochastic Processes, chapter 2: https://eng.libretexts.org/Bookshelves/Probability_Theory_and_Modeling/Discrete_Stochastic_Processes_%28Gallager%29/02%3A_Poisson_Processes/2.03%3A_Combining_and_Splitting_Poisson_Processes ; see also https://www.probabilitycourse.com/chapter11/11_1_3_merging_and_splitting_poisson_processes.php). CMS prior art includes CCS 2023, DOI 10.1145/3576915.3623216, and KDD 2025, DOI 10.1145/3711896.3737152. Bibliographic record and author publication list remain available, but the definitive KDD technical text was not acquired or authenticated. Targeted search did not certify originality.

**Decision:** preserve the proofs and exact finite checks. Do not claim a new defense, general optimum, certified novelty, or production security impact. The next substantive question is whether the exact limit of M(O-S) can be characterized through the posterior distribution of the bottleneck row given the observed minimum trajectory in the two-independent-Poisson-process limit. A proof would need to justify convergence of optimal decision values, not merely weak convergence of counting processes. Formal G1 remains blocked by prior-art clearance.

No empirical attack or deployment benchmark was performed.
