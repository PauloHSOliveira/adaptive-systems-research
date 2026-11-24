---
title: "The Value of Row-Level Feedback in Count-Min Sketch Under a Single-Reuse Constraint"
author: "Paulo H. S. Oliveira"
date: "2026-11-24"
lang: en
status: "Working manuscript — internally audited, originality and independent review pending"
keywords: [count-min sketch, adaptive streaming, value of information, Poisson limit, random walk, repeat budget]
---

# The Value of Row-Level Feedback in Count-Min Sketch Under a Single-Reuse Constraint

## Abstract

We study a restricted terminal decision problem for the classical insertion-only Count-Min Sketch (CMS) with fully independent uniform hashes, a fixed absent target and a deterministic cap on repeated identifiers. The central question is how much the scalar minimum observation reduces attainable terminal overestimation relative to a hypothetical interface exposing all target-row counts. We first derive information-theoretic and reuse-budget bounds using standard concentration and change-of-measure techniques, then obtain a row-wise stochastic envelope that is attained for one row with complete feedback. With at most one repeat, a terminal-repeat reduction yields an exact row-feedback comparator for arbitrary row count. For two rows and three insertions the feedback gap and the independent-row relaxation gap admit closed forms. Our principal restricted result characterizes both gaps in the joint sparse limit: if the width B grows, the preterminal number L of fresh insertions satisfies L/B -> lambda > 0, and exactly two rows and at most one repeat are allowed, the count-scale information gap converges to a positive series obtained by counting excursions of a symmetric marked walk. A uniform approximation bound for hidden-slot decisions justifies convergence of optimal values, rather than relying only on weak convergence of the underlying process. Six existing finite-model verifiers were rerun against exact repository blobs, and an additional conditional-gap identity was checked. The result describes a narrow mathematical model; neither practical robustness nor originality relative to the complete adversarial CMS literature has been certified.

## 1. Introduction and relationship to prior work

The standard CMS estimator reports the minimum among several bucket counters. For a fixed stream this decreases collision overestimation, but public answers can also influence future insertions. We distinguish the statistical effect of taking a minimum from the *value of additional observations* available to a causal decision maker with a shared update budget.

Prior literature already establishes adaptive attacks and robust compact frequency estimators [2,3], information-theoretic control of adaptive selection bias [4,5], adaptive robustness of other sketches [6], and bounded-memory streaming adversaries [7]. The proofs below use classical probability and decision theory, including partial monitoring [8]. We do not claim these techniques are novel. In particular the final KDD 2025 full text [3] could not be independently inspected; the anonymous related manuscript does not establish provenance of that final version. A targeted search did not identify the precise sparse one-repeat formula, but this is insufficient to establish its absence from the literature.

The paper consolidates the restricted results of Study 005, replacing the feasibility-stage organization with a theorem-first presentation. The mathematical question concerns attainable terminal error under a specified interface, not a new general sketch or attack against deployed systems.

## 2. Model and notation

Consider a finite domain with at least M non-target identifiers, a target x* chosen independently of the hashes and never inserted, R>=1 rows, B>=2 buckets in each row, and ordinary additive unit updates. The hash assignments of different identifiers and rows are independent uniform variables, fixed throughout the stream. Set p=1/B, a=1-p. There are no deletions, resets, conservative updates, overflow, side channels or hash disclosures. The only queries report the estimate of x*, not the estimates of arbitrary keys. Uninserted candidate keys have not been probed. The policy may store its full history and use independent private random coins.

Each stream contains exactly M unit inserts. A repeat is any insertion after the first occurrence of the same identifier. At most K repeats are allowed on *each realization*, with 0<=K<M. The policy can select keys based only on permitted observations. This is a fixed-target full-recall decision model, not the memoryless adversary model and not the standard unrestricted adversarial-streaming model.

### Lemma 0 (deferred decisions at fresh-identifier times)

Let H* denote the target hash vector and U the complete independent private random tape of the policy. On an auxiliary probability space, sample

\[
 V_1,\ldots,V_M\overset{\mathrm{iid}}{\sim}\operatorname{Bernoulli}(p)^{\otimes R}
\]

independently of H* and U. At the first insertion of each distinct non-target identifier, assign the next unused vector; on a repeat, use that identifier's already assigned vector. Since a fresh label is chosen using only previous permitted observations and private randomness, and its hash assignments have not been disclosed, deferred decisions give precisely the conditional product Bernoulli law of the original ideal-hash model. The auxiliary construction therefore reproduces the joint law of the actual insertions and target-counter observations. Unused vectors serve only as analytical padding.

Write N for the total number of distinct identifiers inserted over the fixed M-update horizon. The realized collision vectors are the prefix V_1,...,V_N. For the analytical filtration

\[
 \mathcal F_n=\sigma(H^*,U,V_1,\ldots,V_n),\qquad 0\le n\le M,
\]

the event {N<=n} is measurable: simulate the policy with the first n assigned vectors until it either completes all M updates or requests a new identifier requiring V_(n+1). The latter request is determined before revealing that next vector. Thus N is a bounded stopping time in this filtration. This is an enlarged analytical filtration, not the information available to the actual scalar-feedback policy.

Independence is asserted for the complete auxiliary array, **not for the realized prefix conditional on N**. For instance, take R=1, B=2, M=3 and K=1. Insert two distinct keys, then repeat the first if V_1=V_2 and otherwise insert a third distinct key. The second target count suffices to implement this decision. Then {N=2}={V_1=V_2}, and conditional on N=2 each of V_1,V_2 has marginal probability 1/2 of being one, while their joint probability of both being one is 1/2 rather than 1/4. In particular, no argument below assumes independence of adaptive final counts or conditions the auxiliary row envelope on N.

The ideal-hash assumption excludes all information channels revealing uninserted candidate hashes. Pairwise independence of hash assignments is insufficient. For example, over F_2^2 the pairwise independent family h_(a,b)(x)=a dot x+b (uniform independent a and b) has target 0 and three distinct non-target keys (1,0), (0,1), (1,1). Their collision indicators satisfy V_3=1_{V_1=V_2}, violating mutual independence. For the fixed horizon, (M+1)-wise independent uniform hash assignments within each row, with independent row families and the same disclosure restrictions, are sufficient by the same deferred-decisions argument (the target plus at most M distinct keys). This is a sufficient condition, not a necessary one or an equivalence between hash-family independence and collision-vector independence. The manuscript retains fully random hashes as its stated model.

Let C_j be the final target bucket counts and define

\[
 Y=\frac{\min_{1\le j\le R} C_j}{M}.
\]

Because the true target frequency is zero, Y is the normalized overestimate. All probabilities and expectations average over the hash map and independent policy coins.

We use the symbols S and O for the maximal expected Y with complete scalar minimum observations and complete individual target-row observations, respectively. Complete feedback means observations after every insertion except the last. Row feedback is a hypothetical stronger interface used only for comparison. The row-envelope mean E defined in Section 4 is an upper bound for O. Thus S<=O<=E. In asymptotic results M times these quantities is expressed in **counts**, not normalized percentages.

## 3. Baseline information and operational bounds

### Proposition 1 (mutual-information mean and tail bounds)

Let H be the hash map, F the terminal frequency vector, and w_i=F_i/M for non-target keys. Suppose that the deterministic ceiling sum_i w_i^2<=v holds almost surely. Put I=I(H;F) in nats. Then

\[
\mathbb E[Y]\le \min\{1,p+\sqrt{vI/(2R)}\}.
\]

For e>p let J=2R(e-p)^2/v. Then

\[
 \Pr(Y\ge e)\le\min\{1,(I+\log 2)/J\}.
\]

Proof. Write P for the joint law of (H,F) and Q for the product of its marginals. The row-average collision error Z dominates Y. Under Q, conditional on F and the target hashes, Z is the weighted sum of independent Bernoulli(p) indicators with term ranges w_i/R. Its mean is p, and Hoeffding's lemma gives log E_Q exp(t(Z-p))<=t^2 v/(8R). The entropy variational inequality yields E_P Z-p<=I/t+tv/(8R); minimize over t>0 and clip at one. For the tail, independent rows under Q and weighted Hoeffding give Q(Y>=e)<=exp(-J). By binary data processing, I>=d_Ber(P(Y>=e)||Q(Y>=e))>=P(Y>=e)J-log 2. If Q assigns zero mass to the event, P does also when I is finite. QED.

This proposition uses established information-theoretic methods. v is concentration of the *terminal vector*, not a measure of private memory. For equal frequencies on s keys v=1/s.

Two standard refinements are worth separating from the coarse closed forms. Directly applying the entropy variational inequality to the minimum gives
\[
 \mathbb E_P[Y]\le \inf_{t>0}\frac{I+\log\mathbb E_Q e^{tY}}{t}.
\]
Since Y<=Z, this is no weaker than the Hoeffding-based mean bound (also clip at one). Conditional on a fixed F under Q, the minimum has tail equal to the R-th power of the single-row tail. This refinement may be computationally expensive and requires the marginal law of F or a uniform bound on its moment generating function.

For e>p and q_0=exp(-J), the exact binary-KL inversion yields
\[
 \Pr_P(Y\ge e)\le \sup\{u\in[q_0,1]:d_{\rm Ber}(u\|q_0)\le I\}.
\]
If the actual event probability is at most q_0 the claim is immediate; otherwise binary KL is nonincreasing in its second argument up to that actual probability, so the original data-processing inequality implies the displayed restriction. At I=0 the bound is q_0. For fixed I>0 as J tends to infinity, the inverse is asymptotic to I/J, not exponentially small: the coarse linear bound first gives u=O(1/J), hence binary entropy h(u)=o(1); then d_Ber(u||q_0)=uJ-h(u)-(1-u)log(1-q_0) implies limsup Ju<=I. Conversely u=I/J is admissible for sufficiently large J because h(I/J) dominates -log(1-q_0). These are statements about the information-theoretic upper bound, not the realized CMS tail. Neither refinement is claimed original.

### Proposition 2 (fixed-target transcript size)

Suppose the scalar query times are fixed t_1<...<t_q<=M. Let t_0=0 and delta_i=t_i-t_(i-1). The scalar estimate increases by zero or one per unit insertion, so there are at most A=product_i(delta_i+1) feasible transcript values. Conditional on independent private coins U, the terminal vector is a deterministic function of the transcript. Writing T for the finite transcript, data processing and U independent of H give
\[
 I(H;F)\le I(H;U,T)=I(H;T\mid U)\le H(T\mid U)\le\log A.
\]
This proof does not require finite entropy of the complete private random tape. Proposition 1 applies with this ceiling.

The same description-length argument gives the stronger tail transfer

\[
 \Pr(Y\ge e)\le\min\{1,A\exp[-2R(e-p)^2/v]\}.
\]

Indeed, for each fixed realization of the coins, at most A fixed terminal vectors are reachable. Union bound the ordinary fixed-vector tail over them and then average over the coins. There is no assumption that the realized vector is independent of H. For q=0 the transcript count is one. If the last query cannot influence F it may be omitted. By concavity log A<=q log(1+t_q/q) for q>0. This reasoning does not equate the adversary's private state size with mutual information of the complete stream. For example, with R=1 and M=2n, use n preassigned disjoint pairs of fresh candidate labels, one pair per two-update block. Query after every update. Insert the first label, then repeat it if it collided, otherwise insert the second label. The first collision indicator is recoverable from the change in parity of the cumulative target count; a previous parity bit suffices for that local observation. With the block schedule and labels supplied independently of H, a constant amount of private decision state suffices, yet F identifies all n independent Bernoulli(p) decisions and I(H;F)=n h_Ber(p) nats. The cap K=n is satisfied on every realization. This example uses a public schedule and does not claim constant total storage for generating arbitrary labels or storing an unbounded clock. Adaptive times and uncounted side information require separate accounting.

## 4. A row-wise stochastic envelope

Let L_0=M-K. For integer 1<=z<=M define

\[
 T(z)=\begin{cases}
 1-a^{M-z+1},&z\le K+1,\\
 \Pr(\mathrm{Binomial}(L_0,p)\ge z-K),&z>K+1.
 \end{cases}
\]

### Theorem 1 (universal repeat-budget envelope)

For any admissible policy, Pr(MY>=z)<=T(z)^R. Set E=M^{-1} sum_{z=1}^M T(z)^R.

Proof. Couple all fresh vectors as in Section 2. For row j let X_j be the number of collisions among the first L_0 vectors and J_j the first collision index among M vectors, infinity if none. If X_j>0, C_j<=X_j+K: at least L_0 distinct identifiers must be inserted and at most K updates remain. If X_j=0, the first J_j-1 distinct inserts (if reached) are noncollisions, so C_j<=M-J_j+1 if J_j is finite, and zero if not. Define W_j by these respective upper bounds. The row variables W_j are independent, regardless of the correlation among the actual adaptive counts C_j. For z<=K+1, W_j>=z exactly when J_j<=M-z+1. For z>K+1 it occurs exactly when X_j>=z-K. Taking the minimum across the independent envelope variables gives the result. QED.

If X_j=0 and J_j>N, all realized identifiers are noncollisions in that row and C_j=0, even when J_j is finite. No conditioning on N or on a global policy-dependent variable is used in the independence of the W_j.

For a real threshold e in (0,1] take z=ceil(Me). This strictly improves the earlier crude binomial repeat bound for 1<=z<=K (when K>0). For K=0 the distribution is exact in all rows.

### Remark (a policy-dependent refinement without conditional independence)

Let r_i denote the number of repeats of realized fresh identifier i and K_0=sum_{i:V_i=0} r_i, where zero means no collision in any row. The same counting proof gives C_j<=X_j+K-K_0 for every row. For integer z>K and fixed k in {0,...,K}, the event MY>=z is contained in the union of K_0<k and min_j X_j>=z-K+k. Consequently,
\[
 \Pr(MY\ge z)\le \min\{T(z)^R,\ \min_{0\le k\le K}[\Pr(K_0<k)+T(z+k)^R]\},
\]
with T(u)=0 for u>M. The second term is useful only if a policy-specific bound on K_0 is available. In contrast, the proposed replacement by E[T(z+K_0)^R] is false: for R=1, M=2, K=1, B=2 and an unconditional repeat of the first identifier, MY=2V_1 and K_0=1-V_1. At z=2 the true probability is 1/2 but the proposed bound equals 1/4. Moreover conditioning on K_0 can induce dependence between rows even for this nonadaptive repeat policy with R=2. This rejected strengthening is not part of Theorem 1.

### Corollary 1 (one-row optimum)

When R=1 and observations are complete, the envelope is attained for every monotone terminal objective. With full row information, each fresh collision indicator is known as soon as it is inserted. If a collision exists among L_0 fresh identifiers, the remaining K slots can attain K collisions. If the first collision occurs later, the total possible collision count is M-J_1+1, achieved without exceeding the cap. If none occurs the result is zero. This attains W_1. Summing its tails,

\[
 S=O=E=\frac{L_0p+K-a^{L_0+1}(1-a^K)/p}{M}.
\]

Without observations the one-row mean is p for every admissible fixed-mass policy. In multiple rows the envelope relaxation does not require a common repeat choice across rows and is generally loose.

## 5. One repeat: exact row-feedback comparator

For Sections 5–7 assume K=1 and let L=M-1.

### Lemma 1 (terminal-repeat reduction)

For any terminal objective depending only on the minimum count, restricting policies to L fresh insertions followed by one fresh or repeated insertion does not change the optimal expected objective under either complete observation interface.

Proof. If an admissible policy first intends an early repeat, it can use no further repeats thereafter. Replace that intended repeat with a fresh insertion, retain the intended repeated identifier, execute the necessary remaining fresh inserts and perform the retained repeat last. Conditional on the history at that first intended repeat, subsequent fresh vectors have the same independent law in the original and transformed policies, even if their labels differ. The final sums commute. The transformed policy may ignore later observations and has the same conditional terminal law. If no early repeat is intended, simply emulate the policy to the last slot. The transformed policy is causal and satisfies the cap. The reverse inequality follows by inclusion. QED.

This is distributional equivalence, not pathwise equality for arbitrary fixed hash maps. It requires sufficient fresh identifiers and full recall. It makes no claim for K>1.

### Theorem 2 (exact row-feedback value)

Let c_j be the row totals after L fresh inserts, m=min_j c_j and J={j:c_j=m}. Let A be the event that at least one prior vector has a collision in every row in J. Then the maximal conditional probability of increasing the minimum on the last insertion is

\[
 \alpha=\mathbf 1_A+(1-\mathbf 1_A)p^{|J|}.
\]

Indeed a repeat increases the minimum exactly if it covers every current bottleneck row. Otherwise a fresh vector succeeds with probability p^|J|. Since the increase is either zero or one, this choice is optimal for every monotone terminal objective. Thus O=E[m+alpha]/M and the exact optimal tail at integer z equals Pr(m>=z)+E[1_{m=z-1}alpha].

For two rows let b_s=Pr(Binomial(L,p)=s), G_z=Pr(Binomial(L,p)>=z), and d_s=binom(L-s,s)/binom(L,s) with numerator zero if 2s>L. Conditional on equal row totals s, their collision supports are independent uniform s-subsets; d_s is their disjointness probability. Put beta_0=p and beta_s=1 for s>0. With s=z-1 the row-feedback tail is

\[
 O_z=G_z^2+2b_s G_z\beta_s+
 b_s^2[1-(1-p^2)d_s].
\]

This comparator respects the common repeat budget; it grants strictly more information than scalar feedback. It is an exact intermediate quantity, not a production interface recommendation.

### Proposition 3 (smallest nontrivial two-row instance)

For R=2, M=3, K=1,

\[
 O-S=2p^4(1-p)^2/3,\qquad
 E-O=2p^2(1-p)^2(1-p^2)/3.
\]

Proof. Apply Lemma 1. If the first scalar value is one then a double-collision key is known; if the second scalar value is zero, a fresh last key is optimal under both interfaces. For the remaining history (0,1), the first two vectors are (00,11), a singleton followed by 11, or opposite singletons, with respective unconditional probabilities a^2p^2, 2p^3a, 2p^2a^2. The row-aware increment succeeds certainly in the first two cases and with probability p^2 in the third. Scalar feedback chooses the second key, since the weighted advantage of that choice over a fresh vector is p^2a^3(1+3p)>0 and repeating the first never succeeds. The lost increment is therefore 2p^4a^2. The row envelope overstates the attainable shared-repeat increment only for opposite singletons, where the gap is 1-p^2. Divide by M. QED.

In this fixed-size example the share (O-S)/(E-S) equals p^2. This is not the answer in a joint growing-stream regime.

## 6. Two-row sparse-limit characterization

Assume R=2, K=1, and let B grow with L/B->lambda in (0,infinity). We derive the exact limit of the count-scale gaps. All convergence is over the specified ideal-hash models.

### Theorem 3 (shared-budget gap)

For every finite L,

\[
 M(E-O)=(1-p^2)\sum_{s=1}^{\lfloor L/2\rfloor}
 \binom Ls\binom{L-s}s p^{2s}a^{2L-2s}.
\]

To prove this, compare the row envelope on the common L fresh vectors and one further independent vector with the optimum of Theorem 2. If m=0, both require a fresh collision in each empty row. If m>0 and one row is the unique bottleneck, both attain m+1. If the rows are tied at s>0, the envelope attains s+1; the actual row-aware policy does so with certainty when the supports intersect, and otherwise with probability p^2. The event of equal positive totals and disjoint supports has the displayed probability. Under the scaling, the two row totals converge independently to Poisson(lambda); the probability of any double collision among L fresh keys is at most Lp^2->0. Truncate the totals at a fixed cutoff, use convergence of each discrete probability and then let the cutoff grow (their means are bounded). This gives

\[
 \boxed{D(\lambda):=\lim M(E-O)=
 e^{-2\lambda}\sum_{s\ge1}\lambda^{2s}/(s!)^2.}
\]

### Theorem 4 (exact scalar-feedback loss)

Under the same hypotheses,

\[
 \boxed{G(\lambda):=\lim M(O-S)=
 e^{-2\lambda}\sum_{k\ge1}\sum_{\ell\ge1}
 \binom{2k}{k}\frac{\lambda^{2k+\ell}}{(2k+\ell)!}.}
\]

Proof.

**Step 1 — Conditional marked walk.** By Lemma 1 restrict to L fresh inserts and a final decision. Let D0 be the event of no double collisions among the L fresh vectors. Its complement has probability at most Lp^2. Conditional on D0, the L slots are independent, active (one collision) with probability r=2p/(1+p); given the active positions their marks are independent fair signs indicating the row. The number N of active slots has Binomial(L,r) law and converges to Poisson(2lambda). Let Z_n be the sum of the first n signs. The minimum after n active slots is (n-|Z_n|)/2. A visible slot, defined by an increase in the scalar minimum, corresponds exactly to a step toward zero from a nonzero position.

Let A be the event that the terminal difference is nonzero and the terminal minimum positive. On A the row-aware final increment can be one with certainty. On its complement no single-collision prior vector covers all bottleneck rows, and a fresh vector is required, with success probability at most p.

**Step 2 — Excursion signs.** Conditional on the entire absolute walk and active positions, signs of its excursions from zero (including the unfinished last excursion) are independent fair signs. Flipping any excursion's sign preserves the absolute walk, the visible slots and the probability of the path. Returning steps belong to the excursion they complete. On A, a visible slot within the final unfinished excursion necessarily belongs to the terminal bottleneck row. A visible slot in an earlier excursion belongs to that row with conditional probability 1/2 by the independent sign symmetry. Consequently, among visible choices the last visible slot has the maximal conditional expected increment; it is an admissible function of the scalar transcript. Define C as A together with the absence of visible steps in the final excursion. The last-visible comparator has expected increment on A equal to Pr(A|D0)-Pr(C|D0)/2. If no visible slot exists, use a fresh final key.

For precision at finite L, the *actual* conditional row-aware minus last-visible increment is
\[
 \tfrac12\Pr(C\mid D0)+p^2\Pr(c_1=c_2>0\mid D0).
\]
On a positive terminal tie the comparator repeats a single-collision key and gains zero, whereas the row-aware policy can gain one with probability p^2 by using a fresh key. On zero terminal minimum both use a fresh key. This finite correction was identified during consolidation; it vanishes in the limit.

**Step 3 — Uniform control of hidden choices.** Partition the slots into blocks of nonvisible positions separated by visible positions. Given the visible positions, the number of hidden active positions in each block, and the ordered active marks, hidden active placements are uniform subsets within their block: all rearrangements within the block preserve the mark order, visible positions and Bernoulli probability. A policy's coins are independent, and its chosen slot is a function of its scalar observations and coins.

For an integer w between 1 and L, a block of length less than w implies an active slot within w slots of an endpoint or a pair of active slots at distance at most w. This includes zero-length blocks conservatively; if no visible slot occurs the unique block has length L. A union bound gives probability at most 2wr+Lwr^2 of a short block. On the remaining event the probability of any chosen hidden slot being active is at most N/w, conditional on the preceding information. Integrating, the probability of a successful hidden repeat is at most 2wr+Lwr^2+Lr/w uniformly over admissible policies. Fresh decisions yield at most p. On D0, for every visible choice the comparison in Step 2 is valid even under conditioning on the absolute walk, since the policy cannot see excursion signs. Therefore the count-scale gain of the scalar optimum over the last-visible comparator is at most
\[
 \eta=Lp^2+2wr+Lwr^2+Lr/w+p.
\]
The first term allows any terminal increment on the complement of D0. Taking w=floor(sqrt(L)), bounded below by one, yields eta->0 since Lp->lambda. This establishes convergence of optimal decision values, not only a distributional approximation of the counts.

**Step 4 — Counting the limit.** Conditional on N=n, event C occurs exactly when the last zero of Z is at step 2k with k>=1 and the subsequent ell=n-2k>=1 marks are all equal. The prefix may be any bridge of length 2k; the suffix can have either sign. Different last-zero indices define disjoint events. Thus
\[
 \Pr(C\mid N=n)=2^{1-n}\sum_{1\le k\le(n-1)/2}\binom{2k}{k}.
\]
Since the conditional expression is bounded by one, convergence of the discrete binomial distribution to Poisson(2lambda) transfers its expectation (truncate N using its bounded mean). The finite tie correction is at most p^2 and vanishes; so does the contribution from the complement of D0 and the decision approximation eta. Substituting the Poisson probabilities into one half of Pr(C) gives the claimed nonnegative convergent double series. QED.

### Corollary 2 (relative value of the minimum-only interface)

Both limiting functions are strictly positive for lambda>0. Therefore

\[
 \lim\frac{O-S}{E-S}=\frac{G(\lambda)}{G(\lambda)+D(\lambda)}.
\]

The absolute normalized difference is O(1/M), because at most one terminal count can be gained. The relative share is not a percentage improvement in production security or a claim that all attack errors fall by that percentage. It quantifies a specific decomposition of an analytical envelope gap.

## 7. Finite checks and numerical evaluation

The computation is based on exact finite collision-pattern enumeration and belief-state optimization, not measurement of a production sketch. In a finite domain of M keys, assign each R*M-bit collision pattern integer weight (B-1)^(number of zero entries) and denominator B^(R*M). A belief state retains the patterns compatible with past observations and the current frequency vector. At a new observation, split the weighted pattern set by the reported answer; maximize expected terminal reward over admissible next actions. Independent randomization cannot increase a linear maximum. Unseen keys are exchangeable; only one fresh representative action need be considered. For K=1 Lemma 1 permits enumerating L fresh vectors, grouping by their scalar histories, then optimizing the final decision per history. Means and different tail objectives are optimized separately where appropriate.

All six published scripts were re-executed on Python 3.13.5, with source bytes matched to Git blob identifiers from revision eb2e9f5b4f8e6fd9210392ae9a7dc07928b1a9e8. All exited zero. See [reproduction audit](REVIEW_AUDIT.md) for hashes, counts and limitations. The extra finite tie-correction check in Theorem 4 passed 28 exact conditional identities.

Selected exact normalized mean values (R=2, B=2, K=1):

| M | Scalar S | Row observation O | Envelope E |
|--:|--:|--:|--:|
| 2 | 13/32 | 13/32 | 13/32 |
| 3 | 27/64 | 83/192 | 89/192 |
| 4 | 449/1024 | 471/1024 | 489/1024 |
| 5 | 2281/5120 | 479/1024 | 2449/5120 |

Numerical evaluation of the asymptotic series:

| lambda | G(lambda) (counts) | D(lambda) (counts) | Relative share |
|--:|--:|--:|--:|
| 0.25 | 0.003397798 | 0.038504611 | 8.1088% |
| 0.5 | 0.018091803 | 0.097880166 | 15.6002% |
| 1 | 0.067803144 | 0.173173039 | 28.1369% |
| 1.5 | 0.114771426 | 0.193213286 | 37.2653% |
| 2 | 0.145101347 | 0.188686282 | 43.4712% |
| 3 | 0.163780537 | 0.164178680 | 49.9393% |
| 5 | 0.141940633 | 0.127787937 | 52.6235% |

These decimal values are floating-point series evaluations with truncation at 200 terms in the Poisson mixture; the original script checks numerical mass near one, not interval-certified rounding. The symbolic formulas and exact rational finite checks carry the mathematical claims.

## 8. Limitations and discussion

- The strongest characterization assumes R=2, K=1, full target-only scalar feedback, perfect recall, an absent fixed target, independent ideal hashes and L/B->lambda. Generalizing to multiple repeats, arbitrary rows, weighted or turnstile streams, adaptive targets, candidate probes or bounded persistent memory requires additional mathematics.
- The result compares information interfaces within the same abstract policy class. It does not prove cryptographic secrecy of real hash functions, an operational limit against unrestricted attackers, or that the scalar interface supplies a practical defense.
- The general bounds in Sections 3 and 4 derive from known concentration and deferred-decisions techniques. The exact sparse formula is the principal candidate for novelty review, not a certified new theorem in the literature.
- All computations use small abstract models; no real traces, external services or published attack reproduction are evaluated. Full-recall optimal finite policies do not establish production feasibility.
- The KDD 2025 final technical text remains unavailable. The related anonymous manuscript's authorship/version lineage is not authenticated. Searches for combinations of CMS, feedback, repeats, row information and Poisson excursions did not resolve originality. No peer review or independent referee sign-off has taken place.

The difference of scales matters: a positive count-scale gap does not imply a positive limiting normalized gap. A finite identity at M=3 does not determine the joint sparse asymptotic. Both points constrain the interpretation of the results.

## 9. Conclusion

Within a fixed-target, ideal-hash insertion model, we obtain a stochastic repeat-budget envelope, its exact one-row attainment, a row-observation comparator for one repeat, and a two-row sparse-limit characterization of the additional value of row feedback. The key proof compares visible decisions by excursion symmetry and controls hidden-slot choices uniformly. This is a coherent restricted analytical result, subject to independent proof scrutiny and a complete prior-art review. Further generalization is deferred until those two requirements are met.

## References

1. Graham Cormode and S. Muthukrishnan. *An Improved Data Stream Summary: The Count-Min Sketch and Its Applications*. Journal of Algorithms 55(1), 58–75, 2005. https://doi.org/10.1016/j.jalgor.2003.12.001
2. Sam A. Markelon, Mia Filić, Thomas Shrimpton. *Compact Frequency Estimators in Adversarial Environments*. CCS 2023. https://doi.org/10.1145/3576915.3623216
3. Dragos-Florian Ristache, Krzysztof Onak. *The Adaptive Use of Count-Min Sketch: What is Safe and What is Not?* KDD 2025, 2432–2443. https://doi.org/10.1145/3711896.3737152 (bibliographic record confirmed; full text not independently reviewed).
4. Daniel Russo, James Zou. *Controlling Bias in Adaptive Data Analysis Using Information Theory*. AISTATS 2016. https://proceedings.mlr.press/v51/russo16.html
5. Cynthia Dwork et al. *Generalization in Adaptive Data Analysis and Holdout Reuse*. NeurIPS 2015. https://arxiv.org/abs/1506.02629
6. Edith Cohen, Xin Lyu, Jelani Nelson, Tamás Sarlós, Moshe Shechner, Uri Stemmer. *On the Robustness of CountSketch to Adaptive Inputs*. ICML 2022. https://proceedings.mlr.press/v162/cohen22a.html
7. Omri Ben-Eliezer, Krzysztof Onak, Sandeep Silwal. *Robust Streaming Against Low-Memory Adversaries*. ITCS 2026. https://doi.org/10.4230/LIPIcs.ITCS.2026.16
8. Johannes Kirschner, Tor Lattimore, Andreas Krause. *Information Directed Sampling for Linear Partial Monitoring*. COLT 2020. https://proceedings.mlr.press/v125/kirschner20a.html

## Supplementary material

[Information baseline](G0_PROPOSAL.md), [operational bounds](G0_OPERATIONAL_MODEL.md), [row envelope](G0_ROW_ENVELOPE.md), [finite feedback gap](G0_FEEDBACK_GAP.md), [Poisson lower bound](G0_POISSON_GAP.md), [exact Poisson result](G0_POISSON_EXACT.md), [review audit and reproduction instructions](REVIEW_AUDIT.md), [verification code](code/).
