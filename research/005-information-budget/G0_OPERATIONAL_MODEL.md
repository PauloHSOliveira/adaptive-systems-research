# Study 005 — G0-C: Operational Information and Reuse Bounds

**Date:** 2026-11-24
**Decision:** G0-C passed for a restricted, precisely specified operational model. G0 novelty clearance remains incomplete. An exact finite-model diagnostic was run, not a production benchmark or an approved confirmatory G1 study.

## 1. Model and scope

Let H be an ideal fully random hash map, independently uniform on B buckets for each identifier in each of R rows. A conventional additive CMS starts at zero and processes exactly M positive unit inserts. No deletions, resets, conservative updates, overflow, external hash disclosure or side channel. Fix the absent target x* independently of H before the interaction; it is never inserted. All allowed identifiers other than x* have independent hash assignments conditional on the target hash.

The policy may adapt inserts to scalar public responses, use private coins independent of H, and retain arbitrary history. It receives only exact CMS estimates of the fixed target, at predetermined insertion counts 0<t_1<...<t_q<=M. It is not given the hash map or exact internal counters. For the results in Section 3, the policy must additionally never have accessed a new key's hash before its first insertion (this follows from the fixed-target-only query interface).

The terminal normalized error is Y=min_j C_j/M, where C_j is the final target bucket count in row j. Since the target is absent, this equals the normalized overestimate.

This is a restricted mathematical model, not the general bounded-memory adversary model, arbitrary point queries, a real-world security assessment or a cryptographic guarantee.

## 2. Operational transcript information bound

Set t_0=0 and Delta_i=t_i-t_(i-1). For the public answers y_i, y_0=0, each difference y_i-y_(i-1) is an integer between 0 and Delta_i: each unit insert increases every target bucket by either 0 or 1, and the minimum across rows is monotone and 1-Lipschitz for this increment.

Thus the public transcript has at most

\[
L=\prod_{i=1}^{q}(\Delta_i+1)
\]

possible values. If U denotes the independent private random coins, the terminal vector F is a function of U and the response transcript T, with fixed hash-independent public inputs. Therefore

\[
I(H;F)\le I(H;T\mid U)\le \log L
=\sum_{i=1}^q\log(\Delta_i+1).
\]

Use natural logarithms. This bound is no larger than q log(M+1); it can be much smaller. By concavity, it is also at most q log(1+t_q/q) for q>0. If q=0, use L=1 and information zero. A final observation after all inserts need not be counted if it cannot affect F.

Example: for M=100,000 and q=256 with evenly spaced queries including the final checkpoint, the old ceiling is 2947.311479 nats, versus 1528.397820 nats using increments. These are ceilings, not measured information leakage.

Combining with the previous proposition in G0_PROPOSAL.md, assuming the deterministic concentration bound sum_i (F_i/M)^2<=v holds for every realized terminal vector,

\[
\mathbb E[Y]\le \min\{1,1/B+\sqrt{v\log L/(2R)}\}.
\]

### Stronger tail transfer by counting transcripts

Condition on the policy's complete independent coins U. Each possible transcript determines at most one fixed terminal vector. Only count reachable transcripts; for each such vector the concentration ceiling holds. Under the original random-hash distribution, the ordinary fixed-vector CMS row errors have independent collision indicators and independent rows. For e>p=1/B, weighted Hoeffding yields a fixed-vector tail at most exp(-2R(e-p)^2/v). A union bound over the fixed vectors associated with reachable transcripts (not a claim of independence of F and H) yields

\[
\Pr(Y\ge e)\le \min\{1,L\exp[-2R(e-p)^2/v]\}.
\]

The bound is uniform in U, so unconditioning preserves it. Any sharper valid fixed-vector tail may replace the Hoeffding expression. This is a standard bounded-description-length argument applied to the monotonic CMS interface; it is not a newly discovered information-generalization technique. It can be numerically vacuous for large L.

Adaptive query times, changing target identifiers, weighted updates, stopping-time information, and uncounted side channels require a different transcript count.

## 3. Query-independent bound from a deterministic reuse budget

Define a repeat as an insertion of an identifier already inserted at least once in the current stream. Suppose every realization has at most K repeats, 0<=K<=M-1. This is a worst-case cap, not an expected cap or an empirical average. The identifier universe must have enough keys to admit the policy.

Let p=1/B and let V_l be the R-dimensional collision vector of the l-th first-time insertion. Conditional on previously revealed hash assignments, the fixed target's hashes, and the independent policy randomness, the next previously unaccessed identifier has a fresh independent uniform hash in each row. Consequently the V_l can be coupled to a sequence of M i.i.d. product Bernoulli(p) vectors, padding with independent dummy vectors if necessary. This is the deferred-decisions property; the padding is for analysis, not extra inserts.

If the realized number of repeats is k<=K, then there are M-k first-time identifiers. In row j, every repeat contributes at most one additional collision, so pathwise

\[
 C_j \le k+\sum_{\ell=1}^{M-k} V_{\ell,j}
 \le K+\sum_{\ell=1}^{M-K}V_{\ell,j}.
\]

The second inequality follows because the omitted K-k Bernoulli variables sum to at most K-k. It does not assume that the adaptive number k is independent of the hashes. Taking minima gives the stochastic domination

\[
 MY \preceq_{\mathrm{st}} K+\min_{1\le j\le R} X_j,
 \qquad X_j\stackrel{\mathrm{iid}}{\sim}\operatorname{Binomial}(M-K,p).
\]

More precisely, the displayed pathwise coupling exists. For integer z=ceil(Me), the resulting tail ceiling is

\[
 \boxed{\Pr(Y\ge e)\le
 [\Pr(\operatorname{Binomial}(M-K,1/B)\ge z-K)]^R.}
\]

For z<=K the bound is 1, and for z>M the event is impossible. At K=0 there are exactly M distinct insertions and the distribution is an equality. The expected-error ceiling follows by summing the upper bounds on the integer tails z=1,...,M and dividing by M.

**Interpretation:** This separates fresh random collisions from a worst-case deterministic repeat contribution. It can be useful for very small repeat fractions even when the transcript bound is vacuous. It is independent of q and of persistent memory in this restricted model. It does not justify a blanket claim of robustness: concentrated repeat-heavy streams can make the bound uninformative. Pre-queried candidates or hidden hash dependencies invalidate the fresh-assignment argument. The analysis does not measure whether all repeats can attain their worst-case contribution, and no sharpness is claimed for K>0.

For the declared fixed-target interface both tail bounds hold simultaneously, so their minimum is valid. The first depends on the response schedule and concentration; the second on repeat count and the ideal hash model.

## 4. Exact finite diagnostic of realizable feedback policies

We tested a deliberately small abstract collision model: B=2, R=2, three possible non-target identifiers, M=4 inserts. The target collision vectors of the three identifiers have 2^6=64 equiprobable patterns. The policy chooses an identifier based only on its previous choices and fixed-target answers, with perfect recall. Its terminal objective is either expected normalized error or the probability of exceeding a separately specified integer threshold. No external system or published attack was used.

The exact finite dynamic program has state (frequency vector, posterior set of compatible collision patterns). Since all patterns initially have equal probability and observations are deterministic, the posterior is uniform over its compatible set. At each step it maximizes the sum of terminal rewards over possible next actions; after a query it splits the set by the observed answer and sums the branch optima. Insertion actions that would exceed K repeats are inadmissible. All terminal rewards and results use integer or rational arithmetic.

The search covers every deterministic causal policy in this finite model; independent randomized policies cannot improve a linear expected-reward objective. It allows full recall, not b-bit memory. The optimal policies for mean and each tail objective need not be the same.

Results of the executed verifier:

| Repeat cap K | No public queries | Query after insert 2 | Queries after inserts 1,2,3 |
|:--:|:--:|:--:|:--:|
| 1 | 21/64 | 93/256 | 105/256 |
| 2 | 21/64 | 51/128 | 63/128 |
| 3 | 21/64 | 53/128 | 69/128 |

These are exact optimal expected normalized errors for the toy model, not observed error rates on a production CMS. The verifier also checks the four integer-threshold optimal tail probabilities for all nine configurations against Section 3, and the implied expected-error bounds. All 36 tail checks and nine mean checks passed. For example with K=1 and three observations, the optimal mean is 105/256, compared with 21/64 without feedback. The maximum mean need not be achieved by any single policy optimal for all thresholds.

The result verifies finite realizability, not tightness in general. It demonstrates the expected distinction between arbitrary hash-aware selectors and policies with limited observations, but does not establish novelty.

Run the standard-library script from the repository root:

    python research/005-information-budget/code/verify_operational_model.py

## 5. Prior art and gate outcome

- Russo and Zou, AISTATS 2016, https://proceedings.mlr.press/v51/russo16.html : information-theoretic adaptive selection bias.
- Dwork et al., NeurIPS 2015, https://arxiv.org/abs/1506.02629 : description length and max-information bounds. The counting/union-bound technique in Section 2 is explicitly prior art.
- Esposito, Gastpar and Issa, https://arxiv.org/abs/1903.01777 : maximal leakage based generalization, another established approach to transferring fixed-input bounds.
- Ben-Eliezer, Onak and Silwal, ITCS 2026, https://doi.org/10.4230/LIPIcs.ITCS.2026.16 : formal low-memory streaming adversaries. The full-recall diagnostic is not this model, and the external stream cannot be identified with private persistent memory.
- Ristache and Onak, KDD 2025, https://doi.org/10.1145/3711896.3737152 : adaptive CMS robustness, value leakage and hash assumptions. The full published technical text remains unverified; do not assert the repeat bound is novel or absent from their proofs.

**G0-C:** operational model established for the fixed-target, insertion-only ideal-hash regime. The transcript compression and fresh-key coupling are elementary derivations from established tools.

**G0-B:** unresolved novelty. Targeted literature checks confirm substantial prior art; a full comparison with KDD 2025 is still missing.

**G1:** no formal approval for a new research contribution. The small exact diagnostic was executed as a G0 feasibility check, not a confirmatory study.

**Next candidate question:** determine whether a nontrivial upper/lower characterization of attainable error under fixed-target feedback exists jointly in R, B, q, K, and the query schedule, rather than simply bounding all repeats by their maximum possible contribution. A meaningful result would need a nontrivial improvement over both ceilings and a comparison with published CMS robustness theorems. Do not infer a new result merely from the finite table. If a substantially sharper claim cannot be formulated or prior art already supplies it, close Study 005 as an exploratory study.

No authorship or version lineage of the anonymous KDD-related preprint has been authenticated. No production benchmark, new defense, or independent novelty validation has been carried out.
