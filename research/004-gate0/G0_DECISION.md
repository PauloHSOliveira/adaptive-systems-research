# Research 004 — Gate G0 Final Decision

**Date:** 2026-11-24  
**Decision:** **NO-GO for H4-A2 as a standalone original research claim. G0 closed without approval for G1.**  
**Alternative:** A narrowly scoped replication of CCS 2023 remains possible as a separate engineering exercise, not a novelty claim.  
**Evidence:** Targeted literature/provenance recheck, elementary algebra and probability, and exact enumeration of a four-case toy example. No full published attack was reproduced. No confirmatory experiment was run.

## 1. Final-paper provenance

The definitive KDD 2025 paper is confirmed by DBLP and both authors' publication pages:

- Dragos-Florian Ristache and Krzysztof Onak, *The Adaptive Use of Count-Min Sketch: What is Safe and What is Not?*, KDD 2025, pp. 2432–2443. DOI: https://doi.org/10.1145/3711896.3737152 .
- DBLP: https://dblp.uni-trier.de/rec/conf/kdd/RistacheO25.html (access listed as closed).
- Author lists: https://onak.pl/papers/ and https://ristache.com/publications/ .

ACM returned HTTP 403 in the current environment. Neither publication list linked an authenticated author manuscript. The OpenReview forum and direct PDF URL returned a browser-verification page, and the public note API was inaccessible. Two separately indexed OpenReview PDF attachments were accessible as extracted text:

- https://openreview.net/notes/edits/attachment?id=b8pids4yvC&name=pdf
- https://openreview.net/notes/edits/attachment?id=f1Fvavh0fO&name=pdf

Both are associated by title with *Adversarial Robustness of Count-Min Sketch*; the accessible later attachment explicitly labels its authors anonymous. Screenshot retrieval failed for both attachments. Technical similarity to KDD 2025 is substantial, but neither authorship nor version lineage was authenticated. Do not attribute their precise theorem statements to the final KDD version. The previous [preprint audit](KDD_PREPRINT_AUDIT.md) remains a provisional technical comparison.

No request was sent to the authors, and no access restriction was bypassed.

## 2. An elementary zero-effect result

The [H4-A2 formulation](H4-A2_REFORMULATION.md) asks whether benign ordering can change the final target error by changing the choices of an adaptive policy. We now delimit one regime in which the expected effect is exactly zero.

### Proposition (fresh, unprobed keys)

Fix a target x* and a finite benign multiset H, independently of the sketch hashes. Let P0 and P1 be two permutations of H. Use a conventional Count-Min Sketch (CMS) with R rows, B buckets per row, and a completely random hash map, independently sampled in each row. There are no resets, decay, conservative updates, or counter overflow. Choose a fixed number K of adversarial unit insertions. Assume the domain has sufficient unused identifiers.

The adaptive policy may observe previous scalar query responses and use private randomness. Every adversarial insertion must be of a distinct identifier, outside the entire benign support and different from x*, whose hash has never been used in any earlier update or query. The policy may not access unseen hash values or future randomness. The full benign multiset and its order are fixed independently of the hash and policy random choices. The attacker is not allowed to adapt the number K of insertions.

Then the final target-frequency estimate has the same distribution under P0 and P1. In particular, the difference of expected terminal normalized errors is zero.

**Proof.** Condition on the entire hash assignments of x* and the fixed benign support. Their total contributions to each target bucket are fixed and equal for P0 and P1. Reveal other hash assignments lazily, including assignments used in earlier queries. Conditional on all hash assignments revealed so far, and on the policy's private random choices so far, an admissible newly chosen insertion identifier has a fresh independent uniform hash in each row. The collision indicator vector for that insertion is therefore a product of R Bernoulli(1/B) variables, independent of the previous such vectors. This remains true when the selection of the fresh identifier is a causal function of the transcript. By induction the K collision vectors are i.i.d. under either ordering, conditional on the fixed benign and target hashes. Thus their sum, added to the identical benign target-bucket counts, has the same joint distribution in both arms. Taking the minimum across rows preserves equality in distribution. Both arms have equal total update count, and the target's exact frequency is fixed by the benign multiset, so normalized error distributions agree. Integrate over the conditioned hash assignments. QED.

**Limitations:** This is not pathwise equality under arbitrary coupled seeds; it is equality in distribution. It does not cover repeated insertions, pre-probed candidates, adaptive stopping, hash dependencies, or nonstandard CMS update rules. It is a straightforward deferred-decisions argument, not a new cryptographic or streaming theorem. It does not establish zero effect for the published CCS cover-finding policy, which can reuse identifiers.

## 3. Exact existence check in a tiny model

Conversely, an ordering effect is possible once the insertion policy may reuse identifiers. The bare existential claim of H4-A2 is therefore too weak to justify a large experiment.

Use a toy CMS with one row and two buckets. Fix a target x* and distinct benign identifiers a,b, all assigned independently uniform buckets. The target never occurs. There are two honest unit inserts (a,b or b,a), one intermediate target query after the first insert, and one adaptive unit insertion selected by the same fixed policy in both arms. The policy has the two candidate identifiers as fixed parameters and chooses between them using the intermediate response; it does not receive the hash assignments or any future input. Reuse of a or b is expressly allowed in this toy model. This is **not a reproduction of a published attack**, nor evidence about a production implementation.

Let u and v be the binary indicators that a and b, respectively, share the target bucket. Each of the four pairs has probability 1/4.

| u | v | Terminal estimate P0 (a then b) | Terminal estimate P1 (b then a) | P0 minus P1 |
|:--:|:--:|:--:|:--:|:--:|
| 0 | 0 | 0 | 0 | 0 |
| 0 | 1 | 2 | 1 | 1 |
| 1 | 0 | 2 | 1 | 1 |
| 1 | 1 | 3 | 3 | 0 |

The table follows from the fixed selection rule: the first target-query response selects a when it equals one and b otherwise. Terminal counts are u+v plus the selected identifier's collision indicator. The exact expected estimates are 7/4 and 5/4, respectively. Since each arm has three total insertions and zero true target frequency, the expected normalized gap is 1/6. Swapping the labels of P0/P1 reverses its sign; changing to a precommitted update makes the gap zero. This illustrates why a general positive directional claim requires meaningful additional assumptions.

These four cases were enumerated using integer arithmetic in the assistant's computation environment on 2026-11-24. This is complete finite enumeration, **not** Monte Carlo or measured attack performance.

## 4. A universal budget-scale sanity bound

Let H be the common final honest frequency vector, A0 and A1 the final adversarial frequency vectors, each of mass K, and M=||H||_1+K. For any fixed CMS hash map and any fixed target x* absent from both complete streams, define its terminal error e_i=estimate_i(x*)/M.

For each row, the difference of its target bucket counts is a subset sum of A1-A0, whose coordinates sum to zero. Each subset sum has absolute value at most ||A1-A0||_1/2. The minimum operator is 1-Lipschitz with respect to the maximum coordinate difference. Consequently,

\[
|e_1-e_0|\le \frac{\|A_1-A_0\|_1}{2M}\le \frac{K}{M}.
\]

This inequality holds pathwise regardless of adaptive policy or hash distribution under the stated equal-budget assumptions. It is a coarse ceiling, not an estimate of the attainable gap and not a novel result. It provides a useful consistency check for any subsequent replication. If the target is allowed to receive direct inserts, the proof must be stated for collision-only error excluding the target and must account for the altered mass convention.

## 5. Published replication baseline and budget assessment

Select the previously audited, MIT-licensed CCS 2023 implementation as the reference if a separate reproduction project is requested:

Markelon, Filić and Shrimpton, *Compact Frequency Estimators in Adversarial Environments*, CCS 2023. DOI https://doi.org/10.1145/3576915.3623216 .

Pinned commit: https://github.com/smarky7CD/cfe-in-adv-envs/commit/5e511f60015c2c1d3a10a950d94c58d2c988cc46 .

Relevant artifact: https://github.com/smarky7CD/cfe-in-adv-envs/blob/5e511f60015c2c1d3a10a950d94c58d2c988cc46/experiments/attacks/private_private.py .

The source's historical inline results for 100 trials report the following CMS configurations and aggregate operation counts. These are upstream values, not measurements produced by this study.

| Width | Rows | Configured insertion ceiling | Mean reported queries | Mean reported rs. insertions |
|---:|---:|---:|---:|---:|
| 2048 | 4 | 2^20 | 11,064.35 | 17,999.91 |
| 4096 | 8 | 2^20 | 35,332.18 | 44,134.92 |

The earlier proposed 256-query ceiling is substantially smaller than either upstream mean. Likewise, 10,000 insertions is below the reported mean research-stage insertion counts for both. These comparisons are descriptive, not lower bounds on required budgets: a different configuration or policy could require fewer operations. The source may use slightly different accounting at budget boundaries, so its configured insertion ceiling is not assumed to be an exact count without an instrumentation audit.

The artifact uses Python and ordinary CPU execution. Its authors describe reference implementations not optimized for throughput. The computational memory capacity of a modest CPU notebook is plausibly adequate for these sketch sizes, but actual runtime, peak RSS, dependencies, and trial-level reproducibility have not been measured here. No claim of a successful reproduction is made.

If independent replication is later authorized, start with upstream semantics and provenance, validate exact oracle counts and operation accounting, and record actual execution resources before deciding whether a low-budget condition has statistical power. Do not use a null result at 256 queries to refute the published attack.

## 6. Final gate decision

| Criterion | Outcome |
|---|---|
| Publication identity | Confirmed for the KDD bibliographic record; anonymous manuscript lineage unresolved |
| Bare existence of order-mediated error | True in an elementary toy example |
| General positive effect | Not established; zero-effect regime proved and sign depends on policy/order labels |
| Novel nontrivial rate or defense | Not established |
| Faithful CCS baseline identified | Yes, pinned MIT source |
| Actual replication and runtime | Not performed |
| Approval for G1 as original research | No |

**Stop H4-A2 as an original-research candidate in its present form.** We cannot conclude that a sufficiently specific quantitative question is impossible or already solved. But an elementary existence example, an elementary zero-effect case, and unresolved prior-art provenance do not meet the research protocol's novelty requirement.

The next research candidate would need a genuinely nontrivial estimand or theorem, e.g. a justified bound linking feedback information, reusable identifiers and final error under a specific model, beyond the elementary budget bound above. That suggestion is not yet a verified open question or an approved new study.

Preserve Research 004 as a **closed pre-experimental G0 investigation**; any independent reproduction of CCS 2023 should be explicitly classified as replication rather than an automatic G1 continuation. This decision supersedes earlier HOLD language. No benchmark, new defense, or discovery is claimed.
