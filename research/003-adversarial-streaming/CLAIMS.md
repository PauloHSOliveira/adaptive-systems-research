# Study 003 — Claim and Correction Ledger

**Status:** Closed — negative / exploratory. Updated 2026-11-22.

This file distinguishes mathematical results, failed hypotheses, and literature-supported statements. A proof of an elementary lemma is **not** a claim of research novelty.

| ID | Origin / round | Candidate claim | Decision | Evidence and limitation |
|:--|:--|:--|:--|:--|
| C01 | 1 | All sub-\(m^{1/3}\)-space point estimators have error \(\omega(\varepsilon\|f\|_1)\). | **Refuted for fixed \(\varepsilon\)** | Always-zero estimator has normalized error at most \(1/\varepsilon\) for nonnegative \(f\). |
| C02 | 2 | Impossibility for point queries with a nonempty-stream condition at every step. | **Refuted / vacuous** | Initial unit update cannot satisfy \(\|f^{(1)}\|_1\ge m/2\) for \(m>2\). |
| C03 | 2–3 | Deterministic evaluation-code point-query estimate with error \(\le\varepsilon\|f\|_1\). | **Proved, standard technique** | Collision-root bound and nonnegative frequencies in strict turnstile; no algorithmic novelty. |
| C04 | 3 | Heavy-hitter outputs inherently violate order invariance. | **Refuted** | Order invariance concerns internal state for fixed randomness, not stability of list output. |
| C05 | 4–5 | Every black-box list aggregator is impossible to robustify. | **Refuted** | Majority aggregation of independently seeded, globally correct/faulty implementations is a counterexample. |
| C06 | 4–6 | \(k\) explicit-list changes imply a new streaming memory lower bound. | **Refuted** | Output-materialization cost does not lower-bound internal update time or state space. |
| C07 | 6–7 | A counter/phase adversary with \(O(\log m)\) bits can generate \(F_0\in[H,2H]\) and \(\Omega(m/H)\) multiplicative flips. | **Proved, elementary** | Fixed schedule over \(2H\) identifiers after setup; does not imply memoryless success. |
| C08 | 7 | Monotone random insertions yield polynomial multiplicative flip number for fixed \(\varepsilon\). | **Refuted** | Monotonicity gives only \(O(\log m/\log(1+\varepsilon))\) selected multiplicative increases for \(F_0\le m\). |
| C09 | 8–9 | Exact-feedback memoryless reflected walk crosses \(H\leftrightarrow2H\) \(\Omega(m/H^2)\) times with high probability. | **Proved for exact feedback** | Correct hitting-time moments, strong Markov property, post-setup Chebyshev bound; not universal over approximate feedback. |
| C10 | 9 | Rounded output hides adjacent prefix lengths, restricting binary-prefix policies. | **Proved in restricted model** | Disjoint sets of prefix-preserving unit actions; no general memory lower bound. |
| C11 | 9–10 | \(\mathbb E[T_k^2]=O(k^2)\) for each partial crossing in the cited proof. | **Not established; argument rejected** | Replace faulty decomposition with exact full-crossing second-moment recurrence. |
| C12 | 10 | Choosing \(r\approx a m/H^2\) with \(a>1\) yields \(S_r\le m\) with high probability. | **Refuted** | Mean already exceeds budget; corrected choice is \(r=\lfloor(m-H)/(2H^2)\rfloor\). |
| C13 | 10 | This study solves ITCS 2026 Question 33 for memoryless \(F_0\). | **Not proved** | Exact feedback and prefix restrictions do not establish adversarial success for all correct approximators. |
| C14 | 10 | Study 003 establishes an original asymptotic theorem. | **Not supported** | Elementary results and corrective analysis; no independent novelty audit or peer review. |

## Mathematical corrections retained

### Second moment of reflected-walk crossing time

For walk \(0\to H\) with reflection at 0 and absorption at H, define \(f_i=\mathbb E_i[T]\), \(g_i=\mathbb E_i[T^2]\). The correct recurrences are

\[
f_0=1+f_1,\qquad f_i=1+\tfrac12(f_{i-1}+f_{i+1}),
\]

\[
g_0=1+2f_1+g_1,\qquad
g_i=2f_i-1+\tfrac12(g_{i-1}+g_{i+1}).
\]

Their solutions give

\[
\mathbb E[T]=H^2,\qquad
\mathbb E[T^2]=\frac{5H^4-2H^2}{3},\qquad
\operatorname{Var}(T)=\frac23H^2(H^2-1).
\]

Do not reuse the erroneous interior recurrence \(g_i=1+2f_i+\ldots\).

### Concentration must use a feasible target count

After \(H\) preparation updates set \(M=m-H\) and \(r=\lfloor M/(2H^2)\rfloor\). Let \(S_r\) be the sum of \(r\) i.i.d. crossing times. Then

\[
\mathbb E[S_r]\le M/2,\quad
\operatorname{Var}(S_r)\le MH^2/3,\quad
\Pr(S_r>M)\le\frac{4H^2}{3M}.
\]

This is meaningful when \(H^2=o(M)\). The previously suggested \(r\) with coefficient greater than one has the wrong tail direction.

## External sources

See the [references in the canonical technical report](paper.md#references). The original ITCS 2026 [Question 33](https://doi.org/10.4230/LIPIcs.ITCS.2026.16) is a published *question*, not a new question formulated by this study.

## Continuation decision

**Closed.** The ten-round discussion is retained as a negative-result record. Any proposed continuation must state new quantifiers, a precise model, a proof goal, comparable published results, and an independent validation plan.
