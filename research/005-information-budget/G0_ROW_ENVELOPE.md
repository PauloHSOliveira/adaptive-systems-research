# Study 005 — G0-D: Row-Wise Envelope and Exact One-Row Optimum

**Status:** Restricted mathematical feasibility result; G0 novelty clearance incomplete. No approved G1 or production benchmark.  
**Predecessor:** [G0-C operational model](G0_OPERATIONAL_MODEL.md).

## 1. Scope and definitions

Retain the G0-C model: classical additive insertion-only Count-Min Sketch (CMS), an absent fixed target chosen independently of the hashes, R rows, B >= 2 buckets, fully independent uniform hashes per identifier and row, M >= 1 unit inserts, no prior observations of fresh keys, no external disclosure, no resets or overflow, at most K repeats on every realization (0 <= K < M), and enough identifiers to insert M distinct keys. A repeat is any insertion of an identifier already inserted in this stream. The policy may observe exact target estimates at fixed checkpoints, and has arbitrary private recall. All probabilities include the random hash map and private policy randomness independent of it.

Set p=1/B, a=1-p, L=M-K, and C_j equal to the final collision count in row j. Let Y=min_j C_j/M.

## 2. Refined universal tail envelope

For integer z in [1,M], define

\[
T(z)=
\begin{cases}
1-a^{M-z+1},&z\le K+1,\\
\Pr(\operatorname{Binomial}(L,p)\ge z-K),&z>K+1 .
\end{cases}
\]

Then, for any admissible policy,

\[
\boxed{\Pr(MY\ge z)\le T(z)^R.}
\]

For real epsilon in (0,1], use z=ceil(M epsilon). The bound is one for z<=0 and zero for z>M. It is never weaker than the earlier G0-C repeat bound: the two coincide for z>=K+1, and the earlier bound is trivial for 1<=z<=K.

### Proof

By deferred decisions, couple first-time insertions to M independent R-dimensional vectors V_l whose entries are independent Bernoulli(p) variables. Unused vectors are analysis-only padding. The coupling is valid for causal selection of previously unaccessed keys under fully random hashing; it need not hold under general seeded hashing or prior candidate queries.

In each row, let S_j=sum_{l=1}^L V_{l,j} and J_j=min{l: V_{l,j}=1}, with J_j=infinity if all M entries are zero. Define a random envelope W_j as K+S_j when S_j>0, as M-J_j+1 when S_j=0 and J_j<=M, and as zero otherwise.

There are at least L distinct inserted identifiers. If S_j>0, the previous pathwise bound gives C_j<=K+S_j: every repeat contributes at most one, and each extra distinct key beyond L contributes at most one. If S_j=0 and J_j<=M, at least J_j-1 first-time insertions must be noncollisions before the first row collision, whenever it is reached. Hence C_j<=M-J_j+1; if that first collision is never reached, C_j=0. If no collision exists among the padded M vectors, C_j=0. Thus C_j<=W_j pathwise.

The W_j depend on independent row sequences, so they are independent even though actual row counts C_j can be correlated by the adaptive policy. For z<=K+1, W_j>=z iff J_j<=M-z+1. For z>K+1, W_j>=z iff S_j>=z-K. These two cases yield T(z). Take the minimum across rows to conclude. QED.

This is an elementary strengthening of the earlier bound, not a new general robustness theorem. A valid independent transcript-size bound remains available in G0-C; their minimum may be used. No independence of actual adaptive row counts is claimed.

## 3. Exact optimum for one row with complete feedback

When R=1 and the policy observes the target count after every insertion except the last, the envelope is attainable simultaneously for every monotone terminal objective. In the fully observed one-row model the first-time collision indicator is directly observable as an increment. If a collision is available among the first L distinct identifiers, the remaining K insertions can contribute K with certainty. If not, the best achievable result is the number of remaining insertions including the first later collision, or zero if none occurs. The full-feedback policy class can realize both branches without access to unrevealed hashes. All strategies remain subject to the same hard repeat cap.

The upper envelope thus gives the exact optimal distribution, not merely a bound on its mean. Summing its integer tails yields

\[
\sup_\pi\mathbb E[Y]
=\frac{Lp+K-a^{L+1}(1-a^K)/p}{M}.
\]

For K=0 this reduces to p; for no observations the optimal expected one-row error is p for any K because the final vector is independent of the hashes. The latter statement does not imply equality of tail distributions across nonadaptive policies. For R>1, the scalar minimum does not disclose each row's indicator and the independently constructed row envelopes cannot generally be attained by a common sequence of updates.

## 4. Exact finite verification

A standard-library exhaustive belief-state dynamic program was executed locally. It enumerates independent collision patterns for M potential keys, with integer weights (B-1)^(R*M-number_of_ones) and common denominator B^(R*M). The frequency vector and compatible pattern subset define the state. A fixed-target query partitions the subset by the minimum row count. Each branch is optimized separately and each possible next admissible choice is considered. Unused identifiers are exchangeable. The finite search computes exact expected normalized error and exact optimal threshold probabilities; it does not simulate a deployed estimator.

Executed results:

- R=1, M=1..5, B in {2,3,4}, K=0..M-1: 210 checks (means and all integer thresholds), all equal to the analytical optimum.
- R=2, M=2..4, B in {2,3}, K=0..M-1: 76 checks, all bounded by the refined envelope. These include 18 means and 58 threshold checks.

Selected R=2 results with M=4, full feedback and B=2:

| K | Exact optimal expected normalized error | Refined envelope mean |
|---:|---:|---:|
| 1 | 449/1024 | 489/1024 |
| 2 | 533/1024 | 581/1024 |
| 3 | 581/1024 | 629/1024 |

The strict gaps demonstrate that this row-wise relaxation is not generally tight. The numerical values are exact rational arithmetic and are not measurements of an external system. The earlier diagnostic in G0-C used a three-key domain; the present verification uses M possible distinct keys and is not directly the same experiment.

Reproduce from the repository root:

    python research/005-information-budget/code/verify_row_envelope.py

## 5. Prior-art and scientific decision

The one-row fully observed abstraction is closely related to deterministic-reward reservoir bandits, in which an item's sampled reward is fixed and revealed on selection. The field predates this report: see *Refined Algorithms for Infinitely Many-Armed Bandits with Deterministic Rewards* (2015), https://cris.technion.ac.il/en/publications/refined-algorithms-for-infinitely-many-armed-bandits-with-determi/ . The present finite repeat constraint and CMS translation are not claimed to be new. This targeted search does not establish whether the exact formula has already appeared.

The closely related CMS literature includes Markelon, Filić and Shrimpton, CCS 2023, https://doi.org/10.1145/3576915.3623216 , and Ristache and Onak, KDD 2025, https://doi.org/10.1145/3711896.3737152 . The final KDD text is still not verified; the anonymous related OpenReview manuscript cannot be treated as its authenticated equivalent. The original novelty blocker persists.

**Decision:** preserve the tighter bound and one-row equality as useful reference mathematics. Do not approve a new theorem claim or formal G1 on this basis. A plausible next feasibility question is whether an upper bound can exploit the shared minimum-only observations and a single global repeat budget, eliminating the independent-row relaxation gap. Compare any proposed improvement with the existing literature and simpler information bounds before claiming novelty. No such sharper general characterization has yet been demonstrated.
