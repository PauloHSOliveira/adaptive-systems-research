# G0 Addendum — Technical Preprint Audit for KDD 2025 Count-Min Sketch Research

**Study:** Research 004 / Gate G0  
**Date:** 2026-11-23  
**Status:** Partial technical-text access; **not** a verification of the final KDD proceedings text.  
**Decision:** Prior-art overlap confirmed in attacks and information leakage; **H4-A2 not yet approved**.

## 1. Provenance and identity limitation

Published bibliographic record:

- Dragos-Florian Ristache and Krzysztof Onak, *The Adaptive Use of Count-Min Sketch: What is Safe and What is Not?*, KDD 2025, pp. 2432–2443. DOI: https://doi.org/10.1145/3711896.3737152 .
- Authors and publication also confirmed at https://onak.pl/papers/ and https://ristache.com/ .

**New accessible technical source:**

- *Adversarial Robustness of Count-Min Sketch*, anonymous double-blind manuscript, https://openreview.net/pdf?id=IuEBdNsWKb .
- The manuscript's abstract, topic, technical results, and attack methods closely match the published KDD 2025 abstract. It may be an earlier manuscript version. **Authorship, version lineage, and identity with the final proceedings paper have not been independently authenticated.**
- Consequently, refer to it as a **related accessible manuscript**, not as "the verified full KDD final paper." Parameter statements below refer to the actual manuscript, not necessarily to the definitive conference text.

The original G0 audit documented that the KDD final full text was not accessible. That limitation is **narrowed** by the manuscript but not eliminated.

## 2. Technical results found in the accessible manuscript

### 2.1 Positive robustness guarantees — prior art

**Theorem 6 (random-oracle model).** For a Count-Min Sketch with B buckets per row and R rows, the manuscript states that if B is at least 2/epsilon and R is at least

\[
(12/\epsilon)\ln Q+(6/\epsilon)\ln(1/\delta),
\]

then all estimates from at most Q accesses are epsilon-estimates with probability at least 1-delta in its random-oracle model. The model assumes fresh independent, unpredictable hash outputs for previously unseen identifiers. It is not a statement about arbitrary deterministic seeded hashes; cryptographic security and the random-oracle idealization must not be conflated.

**Theorem 7 (universal hashing).** With a finite domain of size S, k an integer, and independently selected universal hash functions, the manuscript establishes a simultaneous-for-all-point-queries bound using approximately O((k/epsilon) log_S(1/delta)) rows and O(S^(1/k)/epsilon) buckets per row. Its published conditions involve explicit constants; do not paraphrase these as "all universal hash families are robust with unchanged default CMS parameters."

**Consequences for H4-A2:** The adversarial weakness under test cannot be presented as unavoidable for correctly overprovisioned, robust parameter choices. Keep secure/high-row CMS as an intentionally protected reference condition, and conventional/underprovisioned CMS as a distinct measured baseline.

### 2.2 Attacks and information leakage — prior art

**Section 4** defines a "cover set" for a target key and describes algorithms that find collision-inducing keys by querying the CMS as the adversary inserts keys.

**Section 4.2** exploits the **numeric values** of query results and the use of large/variable update weights to identify collision contributors. The core approach is already a value-based feedback attack; merely using numeric public answers to guide future inserts is **not new**.

**Section 5** evaluates these attacks:

- 100 trials for each tested bucket configuration;
- B ranges from 2,000 to 200,000, with R set in relation to log2(B);
- approximately 20%–30% fewer queries to find a cover set using the value-based attack in the reported configurations;
- additional investigations of double collisions, hash recovery, and behavior of Apache Spark CMS.

These are manuscript-reported results; **we did not reproduce them**.

### 2.3 Model mismatch with our initial proposal

| Dimension | Accessible manuscript | Initial H4-A proposal | Scientific consequence |
|:--|:--|:--|:--|
| Frequency stream | Strict turnstile; supports add/remove; weighted updates used in attack | Insertion-only unit updates | A direct attack comparison may not be faithful |
| Hash secrecy | Random oracle / independently sampled universal hash; attacks include hash disclosure and learning | Intended private keyed hashing | Must model exact disclosure and computational power |
| Query interface | Scalar count estimates and repeated target probes | 256 public probes | Attack power may be insufficient at this budget |
| Attacker objective | Construct target cover sets; force target overestimation | Interaction between temporal ordering and terminal error | Cover sets and value-based exploitation are prior art |
| Honest background | Attack experiments focus on constructing covers; temporal burst vs interleaved fixed multiset is not an identified factor | Same honest multiset in different temporal orders | Specific factorial interaction **not observed**, but still not certified as novel |
| Evaluation | Operations/queries to break, cover sets, hash recovery, Spark experiments | Difference-in-differences on terminal normalized target error | Not directly interchangeable outcomes |

**Important:** A basic static CMS is order-invariant for a fixed total multiset; a possible terminal difference between honest order permutations requires changes in the **attack-generated** multiset, caused by feedback-conditioned decisions.

## 3. What this adds to the existing G0

**Previously uncertain:** Whether a rigorous technical treatment of value-based feedback exploits and secure hash regimes was accessible for KDD 2025.

**Now confirmed from the related manuscript:** Theorems with explicit hash assumptions and resource thresholds; numerical-value leakage techniques; operation/query experiments. The final paper's identity and any revision differences are **not confirmed**.

**Not established:** An original workload-order x adaptive-feedback effect; direct equivalence of the anonymous manuscript to the KDD publication; a valid 256-query pilot; a new defense or a new mathematical theorem.

**Recommended next gate action:** Do not request immediate approval of G1. First determine whether the author's final manuscript can be obtained or whether the related manuscript's provenance can be authoritatively established; then run the already permitted *G0-level feasibility/overlap design review* with explicitly pinned attack model and query/update units. If the specific interaction is still distinguishable and feasible, seek approval for a G1 **replication of an existing attack**, not a new research result.

## 4. Primary source register

- Published KDD DOI: https://doi.org/10.1145/3711896.3737152
- KDD metadata: https://dblp.org/rec/conf/kdd/RistacheO25
- Onak publications: https://onak.pl/papers/
- Ristache publications: https://ristache.com/publications/
- Related anonymous manuscript: https://openreview.net/pdf?id=IuEBdNsWKb
- Prior comparison: [PRIOR_ART_AUDIT.md](PRIOR_ART_AUDIT.md)
- Revised candidate: [H4-A2_REFORMULATION.md](H4-A2_REFORMULATION.md)

**Research integrity:** Nothing in this document proves that the final conference paper is fully covered by the anonymous manuscript, nor that the proposed H4-A2 is scientifically original.
