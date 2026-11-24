# Research 005 — Information, Frequency Concentration, and Adaptive CMS Error

**Date:** 2026-11-24  
**Stage:** G0 candidate / mathematical feasibility audit.  
**Decision:** Proceed only with a narrow prior-art and operational-information audit; no originality sign-off, no full benchmark, and no new defense claim.  
**Predecessor:** [Study 004 G0 decision](../004-gate0/G0_DECISION.md).

> **G0-C update (2026-11-24):** [Operational model and exact finite diagnostic](G0_OPERATIONAL_MODEL.md) now gives a fixed-target transcript-size bound and a deterministic reuse-budget binomial tail bound. Exact finite-policy optimization passed 36 tail checks and nine mean checks. This passes the restricted operational-model gate, not novelty clearance. G0-B remains incomplete and formal G1 is not approved.

## 1. Research question

Can we establish a useful, nontrivial quantitative relationship between the information disclosed by public estimator responses, the concentration of final inserted frequencies (including reuse of identifiers), and terminal estimation error in a fixed-hash Count-Min Sketch (CMS)?

The first goal is **not** to rediscover that CMS can be attacked. Nor is it to claim that using information theory for adaptive analysis is novel. The possible research contribution would have to improve on generic information-theoretic selection bounds by accounting for the *actual query interface*, allowed memory, and temporal structure of permitted updates.

## 2. Literature audit: established tools and blockers

- Daniel Russo and James Zou, *Controlling Bias in Adaptive Data Analysis Using Information Theory*, AISTATS 2016, https://proceedings.mlr.press/v51/russo16.html . Mutual-information bounds on adaptive selection bias are established prior art.
- Cynthia Dwork et al., *Generalization in Adaptive Data Analysis and Holdout Reuse*, NeurIPS 2015, https://arxiv.org/abs/1506.02629 . Short-description-length and max-information generalization techniques are established prior art.
- Sam A. Markelon, Mia Filić and Thomas Shrimpton, *Compact Frequency Estimators in Adversarial Environments*, CCS 2023, https://doi.org/10.1145/3576915.3623216 . Adaptive attacks and Count-Keeper are established prior art; artifacts: https://github.com/smarky7CD/cfe-in-adv-envs .
- Dragos-Florian Ristache and Krzysztof Onak, *The Adaptive Use of Count-Min Sketch: What is Safe and What is Not?*, KDD 2025, https://doi.org/10.1145/3711896.3737152 . The accessible abstract explicitly identifies disclosure of sketch randomness and value-based attacks; it reports positive results for random-oracle and certain universal-hashing regimes. The definitive full text is still not authenticated or accessible in this environment; see Study 004.
- Omri Ben-Eliezer, Krzysztof Onak and Sandeep Silwal, *Robust Streaming Against Low-Memory Adversaries*, ITCS 2026, https://doi.org/10.4230/LIPIcs.ITCS.2026.16 . Bounded persistent memory and memoryless attackers are formalized; a bound on persistent bits is **not automatically a bound on the information contained in all earlier actions**.
- Edith Cohen et al., *On the Robustness of CountSketch to Adaptive Inputs*, ICML 2022, https://proceedings.mlr.press/v162/cohen22a.html . Adaptive sketch robustness is already studied in a different frequency-sketch model.
- Elena Gribelyuk et al., *Adaptive Data Analysis and Adversarial Robustness on Insertion-Deletion Streams*, preprint, 5 November 2026, https://arxiv.org/abs/2611.08699 . Recent work connects adaptive data analysis and robust F2 estimation. Its abstract is relevant to the general direction, but F2 moment estimation is not CMS point-query estimation.

This is a targeted literature audit, not a systematic novelty clearance. In particular, the KDD 2025 full-text blocker remains. The propositions below are **derived baseline consequences of standard tools**, not claimed original theorems.

## 3. Precise model

Use a finite universe, a fixed target identifier x*, R independent rows and B >= 2 buckets per row. Each hash assignment for a distinct identifier and row is independent and uniform. This is idealized fully random hashing, not a claim that arbitrary seeded or cryptographic hash functions implement the model.

The classical insertion-only CMS uses nonnegative integer frequencies, ordinary additive updates, no decay or counter overflow. Let H denote the complete random hash map and F the random terminal frequency vector produced by any causal adaptive process. Assume F(x*)=0, fixed total mass M>0, and a deterministic concentration ceiling

\[
w_i=F_i/M,\quad \sum_{i\ne x^*}w_i=1,\quad
\sum_i w_i^2\le v,\qquad 0<v\le1.
\]

The ceiling must hold for every vector in the support of F, not just its empirical mean or one realized stream. Define p=1/B and terminal normalized collision error

\[
Y(H,F)=\min_{j=1}^{R}\sum_{i\ne x^*}w_i\,\mathbf1[h_j(i)=h_j(x^*)].
\]

Write I=I(H;F), measured in **nats**. The result concerns terminal error on a fixed target, not uniform tracking over all times or adaptively selected targets.

## 4. Baseline proposition: expected error

For the model in Section 3,

\[
\boxed{\mathbb E[Y]\le
\min\left\{1,\frac1B+\sqrt{\frac{vI(H;F)}{2R}}\right\}.}
\]

**Proof.** Let P be the joint law of (H,F), and Q=P_H times P_F its product of marginals. Define the average across rows

\[
Z(H,F)=\frac1R\sum_j\sum_i w_i\mathbf1[h_j(i)=h_j(x^*)].
\]

Pointwise Y <= Z. Under Q, conditional on F and the target hashes, the collision indicators are independent Bernoulli(p); the conditional mean of Z is p. Hoeffding's lemma, applied to terms with ranges w_i/R, gives

\[
\log\mathbb E_Q e^{\lambda(Z-p)}
\le\frac{\lambda^2 v}{8R}.
\]

The bound is uniform in the conditioned F and target hashes, so it remains valid after averaging them out. The relative-entropy variational inequality implies, for lambda>0,

\[
\mathbb E_P[Z]-p\le
\frac{D(P\|Q)}{\lambda}+\frac{\lambda v}{8R}
=\frac{I}{\lambda}+\frac{\lambda v}{8R}.
\]

Optimizing over lambda yields the claimed square-root expression for I>0. For I=0 take lambda down to zero. Use 0<=Y<=1 to clip the upper bound. QED.

**Interpretation:** v is a concentration ceiling (the reciprocal of an effective number of equally weighted identifiers). It is not the number of repeated inserts and must not be described as a complete measure of reuse. For equal weights on s keys, v=1/s; if one key carries all mass, v=1. Information and concentration enter jointly. The ceiling may be too weak for concentrated streams, and the bound may be vacuous for large I.

**Provenance:** This is an application of Hoeffding's lemma and the standard relative-entropy/mutual-information method used in adaptive data analysis. It does not establish originality.

## 5. Baseline proposition: information required for a bad terminal event

Fix a threshold e with p<e<=1. Under Q and for each fixed F, the independent rows satisfy

\[
Q(Y\ge e\mid F)\le
\exp\left(-\frac{2R(e-p)^2}{v}\right).
\]

This follows by applying weighted Hoeffding to each row and multiplying their bounds. Write q=Q(Y>=e), a=P(Y>=e), and L=2R(e-p)^2/v. By data processing of relative entropy through the event indicator,

\[
I(H;F)\ge d_{\mathrm{Ber}}(a\|q).
\]

If 0<q<1, expand binary relative entropy to obtain

\[
I\ge a\log(1/q)-h_{\mathrm{Ber}}(a)
\ge aL-\log 2.
\]

If q=0, absolute continuity gives a=0 (or the information bound is infinite); no division-by-zero inference is needed. Therefore

\[
\boxed{P(Y\ge e)\le
\min\left\{1,\frac{I(H;F)+\log2}{L}\right\}.}
\]

With exact or sharper fixed-input probability q, the binary-divergence inequality can be more informative than the displayed coarse bound. This is a standard change-of-measure argument. It does not establish a new achievable attack, matching lower bound, or optimal robust CMS configuration.

## 6. Important distinction: operational information budget versus memory

Let U be independent private random coins, and T the sequence of q public responses, each from a fixed alphabet of size at most A. If the entire final vector is a deterministic function of U,T and fixed public inputs independent of H, then

\[
I(H;F)\le I(H;U,T)=I(H;T\mid U)
\le q\log A.
\]

The q-response assumption is fixed. For early stopping, a padded transcript needs a specified alphabet and accounting for the stopping signal. Other disclosure channels and external side information cannot be silently ignored. This upper bound is a description-length ceiling and can be loose by many orders of magnitude.

**Do not replace I(H;F) with the adversary's b persistent bits.** F encodes all prior selected updates, not merely its final private state. Even if each private state has only b bits, the external stream can contain information accumulated through many rounds. An operational bound must establish how the actual channel, state and actions constrain this dependence.

The problem is therefore not solved by choosing a nominal memory budget or counting how many identifiers are reused.

## 7. Finite verification (relaxed selection model, not a CMS attack)

Two independent rows, two buckets, two candidate identifiers, one fixed absent target. The four collision indicators have 16 equally likely configurations. A deterministic selector chooses one of two identifiers as its entire final unit-frequency vector. Enumerate all 2^16 = 65,536 deterministic selectors, including selectors granted **full access** to the hash pattern. This is a relaxation of the black-box interface, not a realistic attacker or a reproduction of an attack.

For each selector, compute:
- I(H;F)=entropy of its binary selection (deterministic selection).
- a=probability both row collisions occur for the chosen identifier; Y is zero or one.
- q=1/4 under the independent-marginals law.
- Verify both the expected-error inequality and the exact event KL inequality to numerical tolerance 1e-12.

Actual local Python check on 2026-11-24:
- Enumerated selectors: 65,536.
- Fixed-selection event probability: 0.25.
- Largest event probability over the relaxed selector class: 0.4375.
- Maximum observed d_Ber(a||0.25)-I: 0.0.
- All checked expected-error and KL inequalities passed.

The counts and probabilities are finite exact rational counts; logarithms and square roots are floating-point evaluations. This checks a toy case and does **not** prove general validity, novelty or practical attack feasibility.

## 8. Candidate H5: the operational information gap

**Question:** For a declared public-response interface, finite query budget and restriction on frequency concentration, can we prove a materially stronger error guarantee than the generic substitution I <= q log A, by exploiting the interaction of permitted observations, retained private memory and reuse of identifiers?

A meaningful contribution would require at least one of:
- an interface-specific information bound with a provably stronger parameter dependence than the generic ceiling and relevant prior art;
- a rigorous separation between the generic relaxed selection model and policies realizable under the specified streaming interface;
- a new matching impossibility or a tight quantitative characterization, rather than another generic application of mutual information.

No such result has been established. There is no claim that this exact question is open in the published literature. In particular, the final KDD 2025 theorem assumptions and existing query-budget bounds must be compared before calling any candidate novel.

## 9. Gates and stop criteria

| Gate | Current state | Required outcome |
|:--|:--|:--|
| G0a mathematical baseline | Passed at elementary proposition level | Explicit hypotheses, proof and finite check; no novelty claim |
| G0b prior art | Incomplete | Compare against KDD 2025 full technical text, existing information-generalization bounds and low-memory streaming |
| G0c operational model | Pending | Fix response channel, what counts as an observation, state and action budgets, and the allowed frequency concentration |
| G1 finite model | Not approved | Specify an exact finite-policy optimization problem and compare attainable error with generic bounds without treating unrestricted selectors as black-box policies |
| G2 theorem/validation | Not approved | Prove a genuinely sharper result or close without novelty |

**Stop early if:** the proposed bound follows immediately from a known theorem, relies on an invalid equivalence between persistent memory and transcript information, cannot improve the generic ceiling in any meaningful regime, or duplicates existing CMS results.

## Conclusion

Study 005 is a candidate for a narrow theoretical investigation, not an approved original research project. The initial proofs establish a sound baseline linking mutual information and frequency concentration to expected and tail error, under an idealized fixed-target CMS model. Their mathematical techniques are known. The scientifically meaningful next step is to assess whether the actual public-feedback interface admits a substantially stronger information bound, and to complete the prior-art comparison before committing to larger experiments.
