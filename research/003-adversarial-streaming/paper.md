---
title: "Adversarially Robust Streaming Algorithms: A Negative-Novelty Investigation"
subtitle: "Point Queries, Combinatorial Heavy-Hitter Outputs, and Low-Memory Adversaries for F0"
author: "Paulo H. S. Oliveira"
date: "2026-11-22"
lang: en
keywords:
  - adversarially robust streaming
  - bounded-memory adversaries
  - distinct elements
  - frequency estimation
  - heavy hitters
  - negative results
---

**Research series:** Adaptive Systems Research · Study 003.  
**Status:** Closed — negative / exploratory technical report; not peer-reviewed.  
**Research process:** Ten rounds of hypothesis generation and critical examination in a GPT-6 / DeepSeek discussion, followed by a corrective audit. The discussion is not independent verification or an experiment.  
**Evidence:** Elementary mathematical arguments, a corrected random-walk proof, small exact-arithmetic recurrence checks, and a targeted literature review. **No streaming implementation, attack benchmark, or independent novelty validation was performed.**

# Abstract

**Background.** Randomized compact frequency estimators can be vulnerable to adaptively chosen streams, but adversarial robustness depends on the output interface, target functional, stream model, and adversary's information and memory. **Objective.** Determine whether a defensible new theorem or algorithm arises from (i) point-frequency queries, (ii) robustification of combinatorial heavy-hitter outputs, or (iii) low-memory adversaries generating high-density, high-flip-number streams for the distinct-elements functional \(F_0\). **Methods.** We audited proposed lower bounds against constructive counterexamples and prior work; established a deterministic evaluation-code point-query bound; examined explicit-output costs and randomized aggregation; and corrected a reflected-random-walk hitting-time and concentration calculation. **Results.** Two proposed point-query lower bounds and a general impossibility claim for list aggregation were rejected. A polynomial-evaluation sketch offers simultaneous deterministic point-query error at most \(\varepsilon\|f\|_1\) in strict turnstile with polylogarithmic domain dependence, but is based on established coding/sketching techniques. Explicit heavy-hitter output churn has an elementary lower bound that does not imply a space lower bound. An adversary with \(O(\log m)\) persistent bits can construct a dense, high-flip-number \(F_0\) stream by a fixed schedule. With exact \(F_0\) feedback, a memoryless prefix-preserving reflected walk has expected crossing time \(H^2\), variance \(\frac23H^2(H^2-1)\), and a high-probability lower bound on the number of crossings. This construction is not proved robust to arbitrary multiplicatively valid feedback. **Conclusion.** No original algorithm, universal impossibility theorem, or resolution of Question 33 of ITCS 2026 was established. Study 003 is closed as an exploratory investigation with negative novelty assessment.

**Keywords:** adaptive data streams; distinct elements; \(F_0\); heavy hitters; point queries; random walks; negative results.

# 1. Research question and scope

We investigated three progressively narrower questions:

1. Can the memory cost of adaptive point-frequency estimation be shown to exceed polylogarithmic space under bounded-memory adversaries?
2. Can a generic black-box transform preserve the efficiency of randomized heavy-hitter algorithms under adaptive, memoryless access to combinatorial outputs?
3. Can a memoryless adversary force both polynomial density and polynomial multiplicative flip number for \(F_0\) in a turnstile stream?

These are **different problems**. A point estimate \(\widehat f(x)\), a set-valued heavy-hitter report, a scalar frequency moment \(F_p\), and the combinatorial behavior of an adversary cannot be treated as interchangeable. A construction for one task is not a theorem for another.

We intentionally did not introduce a new sketch or conduct a performance benchmark. The stopping criterion was the absence of a mathematically coherent, literature-surviving claim after ten review rounds.

# 2. Definitions and methodological cautions

Let the universe be \([n]\), and let a stream of \(m\) unit updates \((x_t,\Delta_t)\) define frequency vector \(f^{(t)}\in\mathbb Z^n\). In **general turnstile**, signed frequencies are allowed. In **strict turnstile**, every coordinate remains nonnegative. The stronger restriction that every coordinate is in \(\{0,1\}\) is a separate binary-frequency invariant.

The distinct-elements functional is

\[
F_0(f)=|\{x:f_x\ne0\}|.
\]

The **density** of a frequency vector is its support size; for this functional it coincides with \(F_0\), but the density of an entire stream must be qualified by the time interval over which the bound holds.

For multiplicative flip number, we use the **standard selected-subsequence interpretation**: count the maximum number of selected observation times for which successive selected values differ by more than a prescribed multiplicative tolerance. The printed index expression in Definition 9 of Ben-Eliezer–Onak–Silwal (ITCS 2026) is potentially ambiguous; see the original source before using its notation as a formal certificate [5]. In this report, every explicit flip-number lower bound is witnessed by crossings between \(H\) and \(2H\), which differ by a factor of two.

In the bounded-memory model of [5], the adversary receives only the previous public estimate, has \(b\) bits of persistent memory, may use fresh independent randomness and temporary work memory within a round, and does not observe the round index unless it can infer or store it. Zero persistent bits means *memoryless*. The algorithm's tracking guarantee in [5] is primarily a unilateral multiplicative approximation, not an exact report. The original model permits general integer turnstile streams. We do not silently transfer strict-turnstile proofs to the general model.

**Quantifier discipline.** The following are not equivalent:

- There exist an estimator and an adversary for which a difficult stream occurs.
- There exists an adversary that succeeds against **every** estimator whose outputs remain correct.
- There exists an adversary that succeeds against **every numerically valid sequence** of outputs, whether or not it comes from a streaming algorithm.

A result for the first regime does not establish the second. Theorem 16 of [5] is a strong adversarial construction for \(F_2\), conditional on the estimator's correctness. Its proof does not automatically apply to \(F_0\).

# 3. Related work and provenance

Adversarially robust streaming was systematically developed in Ben-Eliezer, Jayaram, Woodruff and Yogev [1]. Markelon, Filić and Shrimpton [2] studied adaptive attacks and mitigations for compact frequency estimators. Li and Nakos [3] provided deterministic heavy-hitter sketches with sublinear query time, underscoring that deterministic turnstile methods must be considered before proposing a universal robustness impossibility. Woodruff and Zhou [4] established further robust dense–sparse tradeoffs via heavy hitters.

Ben-Eliezer, Onak and Silwal [5] studied memoryless and low-memory adversaries. Their **Question 32** concerns large, combinatorial output spaces; their **Question 33** asks whether bounded-memory adversaries can force both high density and high flip number for \(F_0\). They prove the analogous construction for \(F_2\) (Theorem 16), not the desired \(F_0\) result.

Ristache and Onak [6] analyzed safe and unsafe adaptive use of Count-Min Sketch. *Lifting Linear Sketches* [7] proves strong limitations for robust **norm approximation by linear sketches**, not a blanket ban on linear state for every point-frequency query. The FOCS 2026 work of Gribelyuk and coauthors [8] supplies polylogarithmic-space adversarially robust approximations for \(F_p\), including \(F_0\), but the existence of a robust *estimator* is not the same question as the ability of a memoryless *adversary* to generate a dense, high-flip-number stream. We did not establish that no work after [5] addresses Question 33; the literature search was targeted rather than systematic.

# 4. Rejected conjectures

## 4.1 An incorrectly scaled point-query lower bound

An initial proposed impossibility asserted that every sub-\(m^{1/3}\)-space estimator would incur error \(\omega(\varepsilon\|f\|_1)\) for any fixed constant \(\varepsilon\in(0,1/2)\).

The always-zero estimator obeys, for nonnegative \(f\),

\[
|\widehat f(x)-f(x)|=f(x)\le\|f\|_1.
\]

Therefore its error ratio relative to \(\varepsilon\|f\|_1\) is at most \(1/\varepsilon\) when the denominator is nonzero. **For fixed \(\varepsilon>0\)** that ratio cannot diverge with \(m\). This refutes the universal super-constant-error-ratio claim; it does not establish that the zero estimator meets the useful target error \(\varepsilon\|f\|_1\).

Also, if \(n\) is small, exact counts need only \(O(n\log(m+1))\) bits. A lower bound solely in \(m\) requires a stated relationship between \(n\) and \(m\).

A follow-up conjecture assumed \(\|f^{(t)}\|_1\ge m/2\) at **every** step of a length-\(m\) stream starting empty. At \(t=1\), unit updates give \(\|f^{(1)}\|_1\le1\). For \(m>2\), this defines an empty class of streams. It cannot serve as a meaningful lower bound.

## 4.2 Deterministic evaluation-code counterexample

For \(n\ge2\) and \(0<\varepsilon<1\), let \(q\) be the smallest power of two at least \(\max(2,\lceil\log_2 n\rceil/\varepsilon)\), and let \(k=\lceil\log_q n\rceil\). Assign every \(x\in[n]\) a distinct degree-\(<k\) polynomial \(P_x\) over \(\mathbb F_q\). Maintain \(q^2\) signed counters

\[
C[a,z]=\sum_{x:P_x(a)=z}f_x,\qquad a,z\in\mathbb F_q.
\]

Update the \(q\) counters indexed by \((a,P_x(a))\) for an update to \(x\), and query

\[
\widehat f(x)=\min_{a\in\mathbb F_q}C[a,P_x(a)].
\]

For distinct \(x,y\), the polynomials \(P_x,P_y\) agree at at most \(k-1\) evaluation points. If \(f\ge0\), each counter is at least \(f_x\), and averaging the nonnegative collision error over \(a\) yields

\[
0\le\widehat f(x)-f_x
\le\frac{k-1}{q}\sum_{y\ne x}f_y
\le\varepsilon\|f\|_1.
\]

The bound holds **deterministically, simultaneously for all queries and all times** in strict turnstile, even if updates are chosen adaptively. The state \(C=Af\) is a **linear sketch**; its minimum decoder is nonlinear. These are distinct properties.

There are \(q^2=O((\log n/\varepsilon)^2)\) counters, each requiring \(O(\log(m+1))\) bits for a length-\(m\) unit-update stream. Thus the counter space is \(O((\log n/\varepsilon)^2\log(m+1))\) bits, ignoring lower-order uniform-code-description overhead. A straightforward update performs \(q\) counter accesses and \(O(qk)\) field operations using Horner evaluation; it is **not** generally \(O(q)\) bit operations. This is an illustrative application of standard polynomial-code collision bounds, **not a new algorithm or an assertion that [3] uses exactly this matrix**.

# 5. Combinatorial heavy-hitter outputs: useful corrections, no new barrier

Fix \(0<\eta<\phi<1\). A valid heavy-hitter list \(L\) for a nonnegative vector \(f\) with \(\|f\|_1>0\) satisfies

\[
\{x:f_x\ge\phi\|f\|_1\}\subseteq L
\subseteq\{x:f_x\ge(\phi-\eta)\|f\|_1\}.
\]

Its size is at most \(\lfloor1/(\phi-\eta)\rfloor\). For \(k\) at most this size, the number of *possible* lists is at most \(\sum_{j=0}^{k}\binom{n}{j}=n^{O(k)}\), polynomial in \(n\) for constant \(k\), not exponential in \(n\).

An explicit-list churn example uses \(\phi=1/k\) and \(\eta=1/[2k(k+1)]\). Start with \(k\) distinct elements at frequency one. Their list is forced to be \(X\). Insert a new element \(z\): now all \(k+1\) frequencies equal one and the exclusion threshold exceeds one, so the only valid list is empty. Removing \(z\) restores \(X\). Repetition forces symmetric differences of size \(k\) per update.

This imposes an \(\Omega(k)\) **explicit-output materialization** cost when an entire size-\(k\) list must be written. It is **not** a lower bound on internal update time or memory, and not a bound of \(k\log n\) new communication bits for every transition: the receiver might know \(X\) and only need a state bit.

The attempted impossibility of robust black-box list aggregation was also wrong. Consider an algorithm that initially chooses a correct deterministic heavy-hitter implementation with probability \(3/4\) and a faulty implementation otherwise. With \(r\) independent copies, majority voting over list membership succeeds for the entire adaptive execution whenever more than half chose the correct implementation. Hoeffding gives a failure probability at most \(\exp(-r/8)\). This **refutes a universal claim of impossibility for list-only aggregation**, but does not demonstrate a cost-preserving transform for arbitrary randomized sketches. No such transform was proved in this study.

# 6. An elementary \(O(\log m)\)-memory adversary for \(F_0\)

Let \(H=\lfloor m^c\rfloor\), \(0<c<1\), and \(n\ge2H\). Starting from the empty vector:

1. Insert the first \(H\) distinct identifiers.
2. Repeatedly insert the next \(H\) identifiers and delete the same \(H\) identifiers, using a phase flag and an index.

The adversary needs \(O(\log H)=O(\log m)\) persistent bits and does not rely on estimates. After setup, \(H\le F_0\le2H\), and for fixed multiplicative tolerance sufficiently below one the \(H\leftrightarrow2H\) cycles witness \(\Omega(m/H)=\Omega(m^{1-c})\) selected multiplicative changes.

This is a simple schedule with a stored counter. It does not answer the \(b=o(\log m)\) or zero-persistent-memory part of Question 33. The ITCS authors themselves mention the relevance of \(O(\log m)\)-space simulation to that question [5]; no novelty is claimed.

# 7. Exact-feedback memoryless construction and corrected probability argument

This section is **explicitly conditional on a much stronger observation interface**: after every update, the algorithm outputs the *exact* value \(h=F_0\). This exact-output interface is allowed by a multiplicative accuracy *promise*, but a general approximator need not reveal this information. Thus it cannot establish a universal adversary for Question 33.

Let \(H=\lfloor m^c\rfloor\), \(0<c<1/2\), and \(n\ge2H\). Starting from the empty stream, the adversary takes action based only on the last exact public output \(h\):

- if \(h\le H\), insert element \(h+1\);
- if \(h\ge2H\), delete element \(h\);
- otherwise, toss a fair fresh coin and either insert \(h+1\) or delete \(h\).

After \(H\) initial updates, the support remains a binary prefix and \(h\) walks on \([H,2H]\), reflecting at the endpoints. No private persistent memory or clock is used. The construction is strict turnstile.

## 7.1 Hitting-time moments

Translate the interval to \(\{0,\ldots,H\}\); let \(T\) be the first hitting time of \(H\), starting at \(0\), with deterministic movement \(0\to1\). Define \(f_i=\mathbb E_i[T]\) and \(g_i=\mathbb E_i[T^2]\), with \(f_H=g_H=0\). First-step analysis gives

\[
f_0=1+f_1,\qquad
f_i=1+\frac{f_{i-1}+f_{i+1}}2\quad(1\le i<H).
\]

Therefore \(f_i=H^2-i^2\) and \(\mathbb E[T]=H^2\).

The **correct** second-moment recurrences are

\[
g_0=1+2f_1+g_1,\qquad
g_i=2f_i-1+\frac{g_{i-1}+g_{i+1}}2\quad(1\le i<H).
\]

In particular, the previously proposed interior recurrence with \(1+2f_i\) is incorrect. Solving yields

\[
g_i=\frac{i^4+(2-6H^2)i^2+5H^4-2H^2}{3},
\]

so

\[
\boxed{\mathbb E[T]=H^2,\quad
\mathbb E[T^2]=\frac{5H^4-2H^2}{3},\quad
\operatorname{Var}(T)=\frac23H^2(H^2-1).}
\]

The polynomial expressions satisfy all boundary and interior recurrences exactly. The accompanying standard-library Python checks verify these identities for several finite \(H\); this is algebra checking, not a claim of an independent proof of a new theorem.

## 7.2 A valid concentration bound

By symmetry and the strong Markov property, successive full crossings between opposite endpoints have independent, identically distributed durations \(T_1,T_2,\ldots\), each distributed as \(T\). Write \(S_r=\sum_{j=1}^rT_j\) and let \(M=m-H\) be the post-preparation update budget.

**The previous argument selected \(r\approx a m/H^2\) with \(a>1\) and then claimed that \(S_r\le m\) with high probability. This is an invalid reversal of a Chebyshev tail event: the mean would already exceed the budget.**

Instead choose

\[
r=\left\lfloor\frac{M}{2H^2}\right\rfloor.
\]

Then \(\mathbb E[S_r]=rH^2\le M/2\), and

\[
\operatorname{Var}(S_r)
=r\frac23 H^2(H^2-1)
\le\frac13MH^2.
\]

Chebyshev therefore implies

\[
\boxed{\Pr(S_r>M)
\le\frac{\operatorname{Var}(S_r)}{(M-\mathbb E[S_r])^2}
\le\frac{4H^2}{3M}.}
\]

For \(H=\lfloor m^c\rfloor\), \(0<c<1/2\), we have \(M/H^2\to\infty\). Thus, with probability at least \(1-O(H^2/m)\), at least \(r=\Omega(m/H^2)=\Omega(m^{1-2c})\) complete endpoint crossings occur. Each crossing is a factor-two change and witnesses a multiplicative flip for a fixed tolerance small enough to count doubling and halving.

This is a correct, restricted probability statement for **exact feedback**; it says nothing universal about approximately accurate outputs.

# 8. Why approximate feedback was not solved

For a unilateral \((1+\varepsilon)\)-valid scalar estimate \(y\), the integers \(h\) and \(h+1\) may share an output whenever \(h>1/\varepsilon\): for example \(y=h+1\) can satisfy both approximation intervals.

In binary-prefix state \(S_h=\{1,\ldots,h\}\), the only unit actions preserving a binary prefix are insertion of \(h+1\) and deletion of \(h\). In \(S_{h+1}\), the admissible prefix-preserving actions are insertion of \(h+2\) and deletion of \(h+1\). These sets are disjoint. Therefore, given a shared output \(y\), no deterministic memoryless policy can preserve the binary-prefix invariant in *both* states; for randomized policies, at least one state has success probability at most \(1/2\).

This is a **restricted indistinguishability lemma**. Inserting an already present element is not illegal under strict turnstile; it simply breaks the binary-prefix invariant. Other supports, larger signed frequencies, or strategies that abandon prefixes were not ruled out.

The rounded oracle \(O_\varepsilon(h)=(1+\varepsilon)^{\lceil\log_{1+\varepsilon}h\rceil}\) hides exact values across rounding bins, but a multiplicatively accurate estimator need not use this oracle. We have not proved that all algorithms conceal enough information to block a memoryless attack, nor have we constructed an adversary that succeeds for all valid feedback.

# 9. Claim audit across the ten rounds

| Round | Candidate | Outcome | Novelty assessment |
|:--|:--|:--|:--|
| 1 | Superconstant normalized-error point-query lower bound | Refuted for fixed \(\varepsilon\) | None |
| 2 | General memoryless point-query impossibility | Refuted by deterministic counterexample and invalid nonempty-stream precondition | None |
| 3 | Polynomial-code point-query sketch | Mathematically valid under stated assumptions | Standard techniques |
| 4 | Cost-preserving black-box robustification for heavy hitters | Not proved | Open idea only |
| 5 | Universal impossibility for public-list aggregation | Refuted | None |
| 6 | Majority-vote aggregation counterexample | Correct counterexample to overbroad claim | Elementary |
| 7 | \(O(\log m)\)-bit adversarial \(F_0\) schedule | Correct restricted construction | Elementary |
| 8 | Exact-feedback reflected walk for \(F_0\) | Correct restricted construction | Classical walk |
| 9 | Binary-prefix indistinguishability | Correct restricted lemma | Elementary |
| 10 | Hitting-time second-moment and concentration corrections | Corrected proof, exact checks | Classical probability |

**Proved in this report (under explicit assumptions):** polynomial-code point-query guarantee, explicit-list churn example, counterexample to the asserted universal list-aggregation impossibility, \(O(\log m)\)-memory schedule, exact-feedback random-walk formulas, and restricted prefix indistinguishability.

**Refuted:** the original point-query lower-bound formulations, a universal list-aggregation impossibility, the claimed \(O(k^2)\) second moment for certain partial hitting times, and the incorrect direction of the final Chebyshev argument.

**Observed numerically:** none of the claimed streaming/adversarial effects; only deterministic arithmetic checks of recurrence identities.

**Not tested:** real streaming traces, real attackers, cryptographic hash models, comparative throughput/memory, fresh-sample simulation, and external reproduction.

**Open relative to this study:** a general adversarial strategy or impossibility for \(F_0\) with \(o(\log m)\) persistent memory and approximately correct feedback, as posed in Question 33 of [5].

# 10. Limitations, interpretation, and decision

The source material was a ten-round exploratory AI-assisted critical discussion, not a preregistered experiment or a formal systematic review. Intermediate proposed proofs contained logical and mathematical errors; these have been retained as **rejected claims**, not rewritten as successful results. The direct random-walk correction is mathematically useful for reproducibility but is elementary. We have neither shown that Question 33 is still globally open after every later publication nor established that our particular formulation is publishably novel.

**Final decision: C — Closed, negative / exploratory.** No new robust streaming algorithm, new universal lower bound, or resolution of Question 33 is claimed. A separate research project on information-limited adversaries would require a genuinely new, precisely quantified theorem or a new validated empirical contribution before reopening the line.

# References

1. Omri Ben-Eliezer, Rajesh Jayaram, David P. Woodruff, and Eylon Yogev. *A Framework for Adversarially Robust Streaming Algorithms*. PODS 2020 / Journal of the ACM. https://arxiv.org/abs/2003.14265
2. Markelon, Mia Filić, and Thomas Shrimpton. *Compact Frequency Estimators in Adversarial Environments*. ACM CCS 2023. https://eprint.iacr.org/2023/1366
3. Yi Li and Vasileios Nakos. *Deterministic Heavy Hitters with Sublinear Query Time*. APPROX/RANDOM 2018. https://doi.org/10.4230/LIPIcs.APPROX-RANDOM.2018.18
4. David P. Woodruff and Samson Zhou. *Adversarially Robust Dense-Sparse Tradeoffs via Heavy-Hitters*. NeurIPS 2024. https://arxiv.org/abs/2412.05807
5. Omri Ben-Eliezer, Krzysztof Onak, and Sandeep Silwal. *Robust Streaming Against Low-Memory Adversaries*. ITCS 2026. https://doi.org/10.4230/LIPIcs.ITCS.2026.16
6. Dragos-Florian Ristache and Krzysztof Onak. *The Adaptive Use of Count-Min Sketch: What is Safe and What is Not?* KDD 2025. https://doi.org/10.1145/3711896.3737152
7. *Lifting Linear Sketches: Optimal Bounds and Adversarial Robustness*. STOC 2025. https://arxiv.org/abs/2503.19629
8. Elena Gribelyuk, Honghao Lin, David P. Woodruff, Huacheng Yu, and Samson Zhou. *Adversarial Robustness for Small Frequency Moments and a Weak Equivalence Theorem for Turnstile Streams*. FOCS 2026. https://arxiv.org/abs/2607.06312
