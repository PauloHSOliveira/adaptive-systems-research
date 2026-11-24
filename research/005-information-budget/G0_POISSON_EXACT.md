# Study 005 — G0-G: Exact Poisson-Regime Feedback Gap

**Date:** 2026-11-24  
**Status:** Restricted analytical characterization, derived and checked internally; originality not certified; formal G1 remains blocked.  
**Predecessor:** [G0-F nonvanishing relative feedback gap](G0_POISSON_GAP.md).

> **Consolidation and correction:** [working manuscript](paper.md) and [internal review audit](REVIEW_AUDIT.md) record the complete proof and reproducibility rerun. The finite values formerly described as conditional no-double last-visible regret are only the excursion contribution, one half of Pr(C|D0). The full conditional regret also includes p^2 Pr(c1=c2>0|D0). This correction is at most p^2 and does not alter the asymptotic result. See the [additional verifier](code/audit_exact_gap.py). Independent review remains pending.

## 1. Scope

Keep the G0-F model: classical additive insertion-only Count-Min Sketch, two rows (R=2), B buckets per row, a fixed absent target independent of the fully random hashes, M unit insertions, at most one repeat (K=1), full scalar feedback after each insertion except the last, perfect recall, enough fresh identifiers, no pre-probed keys, no external hash leakage, and no resets or overflow. Let L=M-1 and p=1/B. We study B tending to infinity with Lp tending to a fixed lambda in (0,infinity).

S and O are the optimal expected normalized terminal errors under scalar minimum feedback and under the stronger row-counter feedback, respectively. E is the G0-D row-envelope mean. Multiplication by M converts these errors to counts. By the terminal-repeat reduction in G0-E, it suffices to analyze L fresh independent collision vectors followed by one decision to insert a fresh or repeated key. The common preterminal minimum cancels in M(O-S). No production system is involved.

## 2. Result

\[
\boxed{\lim M(O-S)=G(\lambda)=e^{-2\lambda}\sum_{k=1}^{\infty}\sum_{\ell=1}^{\infty}\binom{2k}{k}\frac{\lambda^{2k+\ell}}{(2k+\ell)!}.}
\]

Together with the earlier shared-budget identity,

\[
D(\lambda)=\lim M(E-O)=e^{-2\lambda}\sum_{k\ge1}\frac{\lambda^{2k}}{(k!)^2},
\]

this gives the exact relative gap

\[
\lim \frac{O-S}{E-S}=\frac{G(\lambda)}{G(\lambda)+D(\lambda)}.
\]

Both functions are positive for lambda>0. This is a characterization in the specified joint scaling and does not give a nonvanishing absolute normalized error: each gap is at most 1/M. The result extends G0-F's lower bound, not its threat model.

## 3. Reduction to a marked walk

The probability of at least one double collision among L fresh keys is at most Lp^2, which vanishes. Condition on the event D0 of no double collisions. The slot vectors are then still independent, and each slot is active (one collision) with probability r=2p/(1+p). Conditional on active slots their row marks are independent fair signs. Let N denote the number of active slots; N has Binomial(L,r) law conditional on D0. Its limit is Poisson(2lambda). The embedded difference of row counts is the simple symmetric walk Z_n, with Z_0=0 and increments equal to the row signs. At step n the minimum is (n-|Z_n|)/2. A visible step (minimum increases) is exactly a step toward zero from a nonzero position. Row feedback identifies all marks; scalar feedback identifies visible slots only.

When the terminal walk is at zero, no previously inserted single-collision key increases both tied rows. When its terminal minimum is zero, no earlier key covers the empty bottleneck row. Otherwise (event A: nonzero terminal difference and positive minimum), the row-aware optimal repeat increases the minimum by one with certainty. In the remaining cases the best fresh-insert increment probability is at most p. Thus the limiting row-feedback incremental value is P(A).

## 4. Visible decisions and excursion symmetry

An excursion is the segment of the walk from a departure from zero until its next return, or the terminal unfinished segment. Assign the step returning to zero to the excursion that ends there. Conditional on the entire absolute walk and active slots, the signs of its excursions are independent fair signs: flipping any subset of excursion signs preserves the absolute walk and gives an equally likely marked path. This is a direct counting symmetry, not an assumption about independent scalar observations.

On event A, a repeat of a visible slot increases the terminal minimum if the collision occurred in the terminal bottleneck row. Each visible step is in the lagging row of its own excursion. If the visible step belongs to the final unfinished excursion, it belongs to the terminal bottleneck row with certainty. Otherwise, its excursion sign is independent of the terminal excursion sign, and the success probability is 1/2 conditional on the absolute walk and active slots.

Consequently, among visible choices the **last visible slot** maximizes the conditional expected increment: it belongs to the final excursion whenever any visible step does. This comparison is valid even if the scalar policy cannot see the absolute walk, because its last-visible choice is a measurable function of the scalar history. On A's complement no visible repeat can succeed. Let C be the event A and no visible step in the final unfinished excursion. The expected increment of a last-visible repeat, on D0, is exactly P(A|D0)-(1/2)P(C|D0). If no visible slot exists, use a fresh final key; this adds at most p to the value. This is a mathematical comparator, not an assertion of exact finite optimality for the original CMS.

## 5. Why hidden-slot choices cannot improve the limit

A scalar policy can select a previously inserted key at a nonvisible slot as well. We must bound this option, rather than infer convergence of optimal values from weak convergence alone.

Condition on D0. Partition the L slots into blocks of nonvisible slots separated by visible slots, including the initial and terminal blocks. Fix the visible positions, the number of hidden active slots in each block, and the ordered active row marks (or equivalently the corresponding ordered walk increments). Given this information, the placements of the hidden active slots within each block are uniform over subsets of the required size. To see this, moving a hidden active step across zero-collision slots within its own block changes neither the order of the nonzero marks nor any visible position. All configurations with that order and those counts have equal Bernoulli probability. Conditioning on independent private policy coins preserves the symmetry.

For an integer w>=1 with w<=L, consider the event that all nonempty-choice blocks (blocks containing nonvisible slots) have length at least w; an empty block may also be counted as short for the following conservative bound. A short block implies an active slot within w slots of either endpoint, or two active slots at distance at most w. If there are no visible slots the sole block has length L. By a union bound, the probability of a short block is at most 2wr+Lwr^2. On the complement, the conditional probability that any chosen nonvisible slot is active is at most N/w, where N is the total active count. Therefore, uniformly over scalar policies, the probability of a successful hidden repeat is at most

\[
2wr+Lwr^2+Lr/w.
\]

The action of inserting a fresh key has increment probability at most p. For any scalar policy, condition on the absolute walk and active slots when comparing its visible choices to the last visible choice. For the hidden choices apply the preceding uniform bound instead; for fresh choices use p. Since the last-visible comparator's expected contribution is nonnegative, these bounds imply that the gain of the scalar optimum over the last-visible comparator, in counts, is at most

\[
\eta_{L,p}=Lp^2+2wr+Lwr^2+Lr/w+p.
\]

The first term permits arbitrary behavior on the event of a double collision, where any terminal decision improves the minimum by at most one. Taking w=floor(sqrt(L)) (at least one) yields eta tending to zero for Lp tending to lambda. This proves convergence of the actual optimal *decision value*. It does not assert that an exactly optimal finite policy always selects a visible slot.

Thus the limiting information gap is (1/2)P(C) in the Poisson-marked walk. This argument uses the original full-recall scalar model; it does not apply to adaptive query times, more than one repeat, pre-probed keys, correlated hashing or additional side information.

## 6. Counting the relevant event

Conditional on N=n, marks are fair and independent. Event C occurs exactly when the walk has a last zero at step 2k with k>=1, and the remaining ell=n-2k>=1 marks are all equal. Indeed, any step toward zero after the last tie is visible. The positive terminal minimum requires at least one completed excursion if there are no visible steps in the final one.

There are binom(2k,k) prefixes ending at zero and two possible constant-sign suffixes. These events are disjoint for different last-zero indices. Consequently

\[
\Pr(C\mid N=n)=2^{1-n}\sum_{1\le k\le (n-1)/2}\binom{2k}{k}.
\]

This is bounded by one, so convergence of the binomial count law to Poisson transfers the expectation (truncate n at a fixed cutoff and bound the omitted probability using the uniformly bounded mean). Substitute Poisson(2lambda) probabilities and multiply by one half. The factors of two cancel to give the series in Section 2. All terms are nonnegative and the series converges, as it is half a probability. QED.

This also gives the scalar optimum in counts if desired: the preterminal minimum has limiting expectation E[min(N1,N2)] for independent Poisson(lambda) counts, and the scalar incremental value tends to P(N1 != N2, min(N1,N2)>0)-G(lambda). Uniform integrability of the preterminal minimum follows from bounded second moments of the binomial row counts. The row-aware incremental value tends to the same probability without subtraction.

## 7. Reproducible checks

The standard-library verifier was executed locally on 2026-11-24:
- 15 exact combinatorial checks for marked-walk lengths 0 through 14: every sign sequence enumerated and the last-zero event count verified.
- 28 exact finite decision comparisons, L=2..8 and B in {2,3,4,8}, enumerating all 4^L collision-vector sequences with integer probability weights and grouping by the entire scalar history. The checks verify last-visible value <= scalar optimum <= row-aware optimum, plus the finite bound eta. All passed.
- Numerical evaluation of the convergent Poisson series and the conditional no-double excursion contribution at larger B. The latter is not the exact finite scalar optimum and is not mislabeled as such.

| lambda | G(lambda), counts | D(lambda), counts | Exact limiting relative information share |
|--:|--:|--:|--:|
| 0.25 | 0.003397798 | 0.038504611 | 8.1088% |
| 0.5 | 0.018091803 | 0.097880166 | 15.6002% |
| 1 | 0.067803144 | 0.173173039 | 28.1369% |
| 1.5 | 0.114771426 | 0.193213286 | 37.2653% |
| 2 | 0.145101347 | 0.188686282 | 43.4712% |
| 3 | 0.163780537 | 0.164178680 | 49.9393% |
| 5 | 0.141940633 | 0.127787937 | 52.6235% |

For lambda=1, the conditional no-double excursion contribution converges numerically from 0.06174642 (L=B=16) to 0.06778000 (L=B=4096). The proved error bound between last-visible and optimal values justifies the same limit; these evaluations do not measure the exact finite optimum for large B.

Run from the repository root:

    python research/005-information-budget/code/verify_poisson_exact.py

## 8. Prior art and scientific decision

Classical simple symmetric walk properties and excursion symmetry are established mathematical tools; see Aldous and Fill, *Reversible Markov Chains and Random Walks on Graphs*, https://www.stat.berkeley.edu/~aldous/RWG/Book_Ralph/Ch5.S1.html ; *Lengths and heights of random walk excursions*, https://www.researchgate.net/publication/221423038_Lengths_and_heights_of_random_walk_excursions . Relevant observation-limited decision theory includes the partial-monitoring references in G0-E. The published CMS adversarial literature includes Markelon, Filić and Shrimpton, CCS 2023, DOI 10.1145/3576915.3623216, and Ristache and Onak, KDD 2025, DOI 10.1145/3711896.3737152; bibliographic record https://dblp.uni-trier.de/rec/conf/kdd/RistacheO25.html . Targeted literature search did not establish whether the exact application and formula are new, and the definitive KDD 2025 technical text remains unverified.

**Decision:** the restricted mathematical characterization is complete in this asymptotic regime. Preserve the result and request an independent proof audit and targeted prior-art comparison before expanding to general K or R. Formal G1 remains blocked. No independent reviewer has certified the proof or originality; no general defense, deployed benchmark or practical risk reduction is claimed. The operational assumptions are deliberately narrow and the absolute normalized gap vanishes. The next scientific step is a consolidated manuscript and rigorous external critical review of this result, not indefinite expansion of the feasibility gates.
