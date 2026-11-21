---
title: "Decision-Margin Information and Temporal Window Selection in a Binary Hidden Markov Model"
subtitle: "Exact Counterexamples, Risk Bounds, and a Literature-Based Negative Novelty Assessment"
author: "Paulo H. S. Oliveira"
date: "20 November 2026"
lang: en
keywords:
  - hidden Markov models
  - Bayesian value of information
  - temporal windows
  - cache admission
  - exact arithmetic
  - rare transitions
  - negative results
---

**Research series:** Adaptive Systems Research · Study 002, H-DATE-2 follow-up.  
**Manuscript status:** Exploratory technical report / working paper; not peer-reviewed.  
**Evidence status:** Exact calculations for a finite stylized model, computer-assisted certificate for a specific root inequality, and literature-backed asymptotic facts. No end-to-end cache experiment or novelty claim.

# Abstract {.unnumbered}

**Background:** A temporal cache-admission controller may use either the signs or the magnitudes of competing short- and long-window estimates. Whether magnitude provides additional *decision value*, rather than merely additional statistical information, depends on what the baseline controller observes and on the downstream loss. **Objective:** Characterize this distinction in an explicitly specified symmetric binary hidden Markov model (HMM), audit temporal-window selection claims, and separate case-specific findings from previously published filtering theory. **Methods:** We analyze a two-state chain of persistence $r$, a binary symmetric emission channel of accuracy $\alpha$, and odd-length empirical-mean windows. We derive a conditional Bayes-risk identity, enumerate finite HMM probabilities with exact rational arithmetic, check a monotonicity assertion by certified rational intervals, and compare the resulting risk bounds with rare-transition filtering literature. **Results:** For window pair $(1,5)$ and $(\alpha,r)=(0.8,0.9)$, the incremental value of margin magnitudes is exactly $84{,}231/7{,}812{,}500=0.010781568$ per decision opportunity in this model. It vanishes for a different persistence regime despite nonconstant conditional loss. A fixed-window risk surface is not unimodal: two strict local minima occur at long windows 5 and 9 in an exact counterexample. For $r\le\alpha$, the most recent emission gives the full-history Bayes-optimal one-step action. A majority window of order $\log(1/q)$, where $q=1-r$, achieves excess risk $O_\alpha(q\log(1/q))$ relative to a *state-aware emission oracle*. The matching order of optimal HMM filtering error, however, is not new: it was established by Khasminskii and Zeitouni (1996) and recovered with an explicit coefficient by Nair, Ordentlich and Weissman (2005). **Conclusion:** Decision-margin value can be strictly positive, but the original H-DATE-2 problem does not yet establish a generalizable new theorem or an operational cache improvement. We close the investigation as an exploratory negative-novelty case study, preserving exact artifacts and unresolved questions.

**Keywords:** hidden Markov model; value of information; temporal estimation; cache admission; exact enumeration; rare transitions; scientific reproducibility.

# Introduction

Frequency-based online caching commonly uses estimates obtained from historical requests. Under a changing popularity distribution, a short window reacts quickly but exhibits greater sampling noise, while a long window can be more stable yet lag behind regime changes. A controller might use the two estimated *signs* of the candidate–victim score difference, or additionally use the estimated *magnitudes* as a measure of confidence.

The crucial scientific issue is not whether more features change predictions, but whether they improve a clearly specified decision under a clearly specified information set. H-DATE-2 arose after an earlier synthetic diagnosis of temporal controllers failed to demonstrate consistent gains in admission-decision loss. The present follow-up isolates a mathematical case, avoiding a claim that this is already a competitive caching algorithm.

The study asks three questions. First, when can margin magnitudes alter the Bayes-optimal selection between two estimators after their signs are known? Second, how does the choice of the two temporal windows affect *total* Bayes risk, as opposed to the incremental value of magnitude features? Third, which of the apparent risk results constitute new findings, given the existing theory of HMM filtering with rare transitions?

**Main contributions of this working report:** (i) an explicit conditional decision-value formulation and finite exact examples; (ii) reproducible counterexamples to universal window unimodality and to using incremental value as a proxy for total risk; (iii) a restricted one-step optimality result for the latest observation; (iv) a reproducible computer-assisted monotonicity certificate for a particular five-observation example; and, centrally, (v) a corrective novelty audit identifying the previously published asymptotic filtering rate. These are **not** claims of a new general-purpose algorithm or a previously unknown rare-transition rate.

# Related work and scientific provenance

The classical Blackwell comparison of experiments places the benefit of an extra observation in a decision-theoretic framework [1]. The use of Jensen's inequality to compare optimal risks with nested information sets is elementary and should not be presented as a novel information-theoretic inequality.

Khasminskii and Zeitouni [2] analyzed asymptotic filtering of finite-state Markov chains. Nair, Ordentlich and Weissman [3, Theorem 3.1] specifically considered a symmetric binary Markov chain through a binary symmetric channel and established the leading rare-transition behavior of the optimal filtering error. Consequently, its $\Theta(q\log(1/q))$ scaling cannot be attributed to the present investigation. The derivation of one-step emission-prediction risk from that state-filtering result is an algebraic corollary, not a new asymptotic discovery.

Count-based cache admission has an established literature including TinyLFU [4] and adaptations of aging and replacement. These are context for the original motivation, **not tested baselines** in this mathematical study. Studies of cache policies such as S3-FIFO and SIEVE illustrate that end-to-end hit rate, cost, memory, and CPU cannot be inferred from a single stationary one-step selection problem [5,6].

The broader literature on contextual decision-making, stochastic bandits, and approximate filtering is relevant to partial-feedback learning and resource budgets. We do not claim that a controller which learns per-context risks by sample means is a new online-learning algorithm. Any future paper on constrained filtering must survey those specialized results before asserting novelty.

# Probability model, actions, and information sets

## Hidden state and emissions

Let $S_t\in\{A,B\}$ be a stationary symmetric Markov chain with transition probability $q=1-r$ per step, $1/2<r<1$. Let the observed emission $Y_t\in\{+1,-1\}$ be generated conditionally independently given $S_t$, with

$$
P(Y_t=+1\mid S_t=A)=P(Y_t=-1\mid S_t=B)=\alpha,\quad 1/2<\alpha<1.
$$

The stationary distribution of the hidden state is $(1/2,1/2)$. Interpret $Y=+1$ as a request for a candidate item $C$ and $Y=-1$ as a request for an incumbent $V$. A capacity-one cache, unit miss costs, and a one-step forecast yield a stylized admit/retain decision. There is no physical cache-state simulation beyond this local decision.

For odd window lengths $1\le s<w$ define empirical margins and actions

$$
m_{s,t}=\frac1s\sum_{j=0}^{s-1}Y_{t-j},\quad
m_{w,t}=\frac1w\sum_{j=0}^{w-1}Y_{t-j},\quad
A_h(t)=\mathbf1[m_{h,t}>0].
$$

As $s,w$ are odd, ties do not occur. Define the *sign-only* controller context $Z_t=(A_s,A_w)$ and the additional magnitude features $M_t=(|m_s|,|m_w|)$. Both are causal summaries of observed emissions. The one-step loss for taking an admission action is 1 if the next request is for the displaced resident; for retention, it is 1 if the next request is for the rejected candidate.

## The conditioning-set trap

If a baseline controller's information $Z_t$ includes the entire raw history $\mathcal H_t=\sigma(Y_1,\ldots,Y_t)$ (and costs), both margins are deterministic $\mathcal H_t$-measurable functions. In that interpretation, $\sigma(M_t)\subseteq\sigma(Z_t)$ and magnitude cannot have *additional* Bayes value:

$$
E[L_s-L_w\mid Z,M]=E[L_s-L_w\mid Z].
$$

**Proposition 1 (literal redundancy).** If $M$ is measurable with respect to $Z$, adding $M$ changes no conditional Bayes risk. The proof follows from the defining property of conditional expectation. Positive incremental value is possible only after fixing a coarser baseline representation $Z$ that does not already recover the magnitudes.

This distinction is conceptual, not an implementation trick: a fair evaluation must compare precisely specified feature budgets, not an artificially weakened baseline against a controller given all raw observations.

# Decision-theoretic formulation

Let $L_s,L_w$ denote the potential one-step losses from following the short and long decisions. Define

$$
d(Z,M)=E[L_s-L_w\mid Z,M],\qquad d(Z)=E[L_s-L_w\mid Z].
$$

The ideal Bayes risk with information $\mathcal I$ is

$$
R(\mathcal I)=E\left[\min\{E[L_s\mid\mathcal I],E[L_w\mid\mathcal I]\}\right].
$$

For nested information sets, elementary algebra gives

$$
\boxed{V_M=R(Z)-R(Z,M)=\frac12\big(E|d(Z,M)|-E|d(Z)|\big)\ge0.}
$$

This nonnegativity follows from conditional Jensen. For a finite two-action problem, strict positivity occurs only when some positive-probability context $Z=z$ contains positive conditional probability of *both* strictly positive and strictly negative values of $d(z,M)$. A difference in magnitude with no change in the preferred action can be statistically predictive yet worthless for this decision.

**Important identity:** $R(Z,M)=R(Z)-V_M$, **not** $R(Z)-2V_M$. The $1/2$ has already been included in the representation of $V_M$.

Here $V_M$ is the value to an **ideal** selector with known conditional risks. It does not include finite-sample learning error, sketch noise, memory, CPU, dynamic cache state, or switching costs.

# Methods: exact enumeration and finite certificates

## Exact dynamic programming

For rational $\alpha,r$, finite-window joint probabilities are rational. We enumerate aggregate sufficient counters, not Monte Carlo paths. At position $j$, the dynamic-programming state records $(n_{-,w},n_{-,s},S_j)$: the number of negative observations in the long and short windows and the current hidden state. Markov transitions and emission probabilities update the joint masses exactly using Python's `fractions.Fraction`.

At the final observation, each count pair determines the two estimated actions. Transitioning the posterior one additional step gives the distribution of the next emission; expected losses are accumulated separately for both actions. Grouping cells first by $(A_s,A_w)$ and then by $(A_s,A_w,|m_s|,|m_w|)$ computes the two risks:

$$
R(Z)=\sum_z\min\{P(Z=z,L_s=1),P(Z=z,L_w=1)\},
$$

$$
R(Z,M)=\sum_{z,m}\min\{P(Z=z,M=m,L_s=1),P(Z=z,M=m,L_w=1)\}.
$$

All displayed finite-window comparisons below were checked by integer/rational arithmetic. Floating-point figures are only decimal renderings of those rational outputs.

## A separate computer-assisted certificate

For $(s,w)=(1,5)$, a symbolic reduction uses $u=(2\alpha-1)^2$ and $p=2r-1$ to define

$$
F_3(p,u)=p^4+(1-2u)p^3+(1-2u+2u^2)p^2+p-2,
$$

$$
F_4(p,u)=p^4+(1+u)p^3+(1-u^2)p^2+(1-3u)p-1.
$$

The critical persistence boundaries are $r_i=(1+p_i(u))/2$, where $p_1$ and $p_2$ are the relevant positive roots of $F_4$ and $F_3$. Their existence and uniqueness can be established analytically: Descartes' rule for $F_4$, and the identity

$$
\partial_pF_3=1+p+\frac74p^3+p\left(2u-1-\frac32p\right)^2>0
$$

for $p>0$. The reported strict monotonicity of $r_2(\alpha)-r_1(\alpha)$ was established by a **computer-assisted certificate**, not a closed-form proof: rational root brackets and implicit-derivative interval bounds cover $u\in[0,1]$ in 128 and 256 slabs. Trust in that result requires independently auditing the certificate implementation and the polynomial reduction; we provide the code to make that review possible.

# Finite exact findings

## Positive incremental value, and a zero-value control

For $(s,w)=(1,5)$ and $\alpha=4/5$, $r=9/10$, the model produces

$$
\boxed{V_M=\frac{84231}{7812500}=0.010781568>0.}
$$

Within the sign-disagreement cell $(A_s,A_w)=(1,0)$, the number $K$ of negative emissions in the preceding four observations is either 3 or 4. The magnitudes reveal that distinction. Correctly applying the extra hidden-state transition gives:

| Quantity | $K=3$ | $K=4$ |
|:--|--:|--:|
| $P(K\mid A_s=1,A_w=0)$ | 0.639930 | 0.360070 |
| $P(S_{t+1}=B\mid A_s=1,A_w=0,K)$ | 0.443496 | 0.599602 |
| $E[L_s-L_w\mid A_s=1,A_w=0,K]$ | -0.067805 | +0.119522 |

The conditional risk difference crosses zero, so the ideal selector changes its action according to the magnitude. Its conditional value in this cell is approximately 0.043036, but this **is not the global value**; the global figure above includes all sign cells and their probabilities.

At persistence $r=3/5$, the corresponding differences retain the same sign for all informative magnitude cells; exact enumeration gives $V_M=0$ globally. Magnitudes can change the predicted *size* of a loss advantage without changing the optimal action.

## Window comparison: incremental value is not total risk

For $\alpha=0.8$, $r=0.9$, the exact risks are:

| Window pair $(s,w)$ | $R(Z)$ | $R(Z,M)$ | $V_M$ |
|:--|--:|--:|--:|
| $(1,3)$ | 0.345056000 | **0.345056000** | 0 |
| $(1,5)$ | 0.356000000 | 0.345218432 | **0.010781568** |

Although the second pair gains more from the magnitude features, it has **higher total decision risk**. The sign-only baseline itself depends on the window pair. Therefore optimization of $V_M$ across pairs is not equivalent to optimization of $R(Z,M)$.

## Two strict local minima disprove unimodality

With $\alpha=3/5$, $r=9/10$, and $s=1$:

| Long window $w$ | Exact Bayes risk $R(Z,M)$ |
|--:|--:|
| 3 | 0.480736000000 |
| **5** | **0.480343936000** |
| 7 | 0.480488047360 |
| **9** | **0.480462187674** |
| 11 | 0.480884624047 |
| 13 | 0.481505479510 |

Because $R(1,5)$ is smaller than its neighbors at 3 and 7, while $R(1,9)$ is smaller than its neighbors at 7 and 11, the same coordinate section has two strict local minima. The universal claim of coordinate-wise unimodality is false. This does not imply two different *global* minima.

## A finite-budget short-window counterexample

With $\alpha=0.8$, $r=0.99$, and odd windows constrained to $w\le11$:

| Window pair | $V_M$ | $R(Z,M)$ |
|:--|--:|--:|
| $(1,11)$ | 0 | 0.239762591324 |
| $(5,11)$ | 0.004061701207 | **0.235700890117** |

All permitted pairs of the form $(1,w)$ with $w\in\{3,5,7,9,11\}$ have $V_M=0$. Within that **finite budget**, a short window greater than 1 can improve risk. No assertion about the optimizer over *unbounded* window lengths follows.

## Monotonicity of the critical interval in the five-observation example

The computer-assisted certificate reports that the width $r_2(\alpha)-r_1(\alpha)$ of the positive-value persistence interval is strictly decreasing on $\alpha\in(1/2,1)$ for $(1,5)$.

At $\alpha=0.8$, the boundaries are approximately $r_1=0.841230$, $r_2=0.931575$. As $\alpha\to1/2^+$, their width approaches approximately 0.1112404 while the **value magnitude** tends to zero. As $\varepsilon=1-\alpha\to0^+$, the boundary expansions are

$$
r_1=1-\varepsilon+\varepsilon^2+O(\varepsilon^3),\quad
r_2=1-4\varepsilon^2+O(\varepsilon^3),
$$

so the width is $\varepsilon-5\varepsilon^2+O(\varepsilon^3)$. The width vanishes *linearly*, not quadratically. The support of positive value and its expected magnitude are distinct quantities.

# A region with a full-history optimal short window

**Proposition 2 (one-step optimality when $r\le\alpha$).** If $1/2<r\le\alpha<1$, the most recent emission determines the Bayes-optimal prediction of the next emission even with access to the entire observed past. Hence for any odd $w>1$,

$$
V_M(\alpha,r;1,w)=0,
\qquad R(Z,M;1,w)=\frac{1-(2\alpha-1)^2(2r-1)}2.
$$

**Proof.** Before observing $Y_t$, the conditional probability of $S_t=A$ lies in $[1-r,r]$ regardless of the observed past. Even at the least favorable prior $1-r$, a positive emission gives posterior odds favoring $A$ when $\alpha(1-r)\ge(1-\alpha)r$, equivalent to $\alpha\ge r$. A negative emission symmetrically favors $B$. The transition to $S_{t+1}$ preserves the preference sign because $r>1/2$. Thus following the latest emission achieves the full-history Bayes action. The displayed risk equals $P(Y_{t+1}\ne Y_t)$, obtained from the product of the two state/emission correlations. $\square$

This is a result for **one-step 0–1 prediction in the specified symmetric HMM**, not a theorem about dynamic cache hit rate.

# Rare transitions: published theory and a restricted upper bound

Let $q=1-r\to0$ with fixed $\alpha\in(1/2,1)$. If the latent state were directly observed, the irreducible next-emission error would approach $1-\alpha$. But the actual causal controller sees only noisy emissions.

Nair, Ordentlich and Weissman [3, Theorem 3.1], recovering earlier results [2], prove for the optimal **current-state filter**:

$$
E_{\mathrm{filter}}(q)
=\frac{q\log(1/q)}{D(1-\alpha\Vert\alpha)}(1+o(1)),
$$

where

$$
D(1-\alpha\Vert\alpha)
=(2\alpha-1)\log\frac\alpha{1-\alpha}.
$$

The paper's BSC parameter is the *bit-flip probability* $\delta=1-\alpha$, not the correct-emission probability. The symmetric binary KL divergence has the same value under reversal of its arguments in this complementary case.

The optimal probability of mispredicting $S_{t+1}$ after observing $Y_{\le t}$ is $q+(1-2q)E_{\mathrm{filter}}(q)$. Therefore the optimal risk of predicting the next **observed emission** is the elementary corollary

$$
\boxed{
R_{\mathrm{full}}(q,\alpha)=1-\alpha+
\frac{q\log(1/q)}{\log(\alpha/(1-\alpha))}(1+o(1)).
}
$$

This rate and its coefficient **are not novel contributions of H-DATE-2**.

An independent upper-bound argument considers majority vote in an odd window $w$. With $\eta=\alpha-1/2$, one state transition in the relevant window is a failure event of probability at most $wq$. Conditional on no transition, Hoeffding gives probability of an incorrect majority at most $e^{-2w\eta^2}$. Thus the risk of following the long-window majority satisfies

$$
R(1,w)\le1-\alpha+(2\alpha-1)
\big[wq+e^{-2w(\alpha-1/2)^2}\big].
$$

Choosing $w=O_\alpha(\log(1/q))$ yields $R-(1-\alpha)=O_\alpha(q\log(1/q))$, matching the known *order* of the full-history optimum. However, this does **not** prove that the finite-window excess $R(1,w)-R_{\mathrm{full}}$ is $O(q)$, nor that the window pair is exactly optimal. A bound on absolute excess relative to the state-aware oracle cannot decide the smaller difference relative to the full-history Bayes filter.

# Rejected assertions, unresolved questions, and model limitations

## Rejected or unsupported assertions

1. **More information always provides operational improvement.** False without accounting for statistical learning, resource costs, and state dynamics. Bayes information value is only a nonnegative *ideal conditional* quantity.
2. **A larger $V_M$ identifies the better window pair.** Refuted by the exact risks in Section 6.2.
3. **Risk is coordinate-wise unimodal in window lengths.** Refuted by the exact finite counterexample in Section 6.3.
4. **Every finite-gap instance has a universal $\Omega(\sqrt T)$ bandit regret.** False; fixed-gap stochastic instances admit logarithmic regret with appropriate algorithms. Minimax and instance-dependent claims cannot be conflated.
5. **There is an HMM window transition at $\alpha_c=1/2+1/(2\sqrt2)$.** The stated derivation is arithmetically invalid: if $d=\alpha-1/2\in(0,1/2)$, then $2d^2<1/2$ throughout the domain. This only refutes that *argument*, not every possible transition.
6. **A two-window rule attains $R-(1-\alpha)=O(q)$ for fixed noisy $\alpha$.** Contradicted by the published full-information filtering lower bound in Section 8.
7. **An $O(q\log(1/q))$ rate for rare-transition binary filtering is new.** False; see [2,3].
8. **A finite search establishes a global optimizer over unbounded windows.** False; the range of search is part of each finite result.

## Open problems not settled here

- Whether the excess $R_{\mathrm{two}}(q,\alpha)-R_{\mathrm{full}}(q,\alpha)$ can be $O(q)$ for an explicitly restricted class of two-window decision rules, with correctly specified memory and computational costs.
- Existence and asymptotic location of a *global* minimizer over all odd window pairs without a maximum permitted length.
- Optimal risk under a formally specified bit-memory budget $B(q)$ and a precise representation model. This requires a survey of approximate HMM filtering and finite-memory prediction; we do not assert that it is new.
- Identifiability of end-to-end cache-policy counterfactual losses with multi-step state coupling, in contrast to the one-step exogenous request toy model.

The proposed threshold $\limsup [R_{\mathrm{two}}-R_{\mathrm{full}}]/[q\log(1/q)]<1$ is not by itself a proof of a better *order*: a constant such as $1/2$ satisfies it yet leaves the same $\Theta(q\log(1/q))$ scaling. Testing an $O(q)$ gap would constitute a more stringent and interpretable mathematical statement.

## Scope and threats to validity

No public production trace was downloaded or evaluated in this follow-up. No faithfully integrated W-TinyLFU or Evolving Sketch was benchmarked. The physical cache state is limited to a single local candidate–victim comparison, so it does not model evictions, readmissions, changing opportunities, or policy-induced counterfactual trajectories. The optimal selectors assume knowledge of conditional risks. Statistical detectability and finite-sample online learning were not validated. Memory accounting for raw sliding-window histories and online estimation has not been equalized in bits or bytes. The certificate code, while deterministic and exact-arithmetic-based, has not been independently peer-reviewed.

Consequently the finite-HMM results cannot be interpreted as a practical improvement to weighted miss cost, cache hit rate, CPU use, or memory efficiency.

# Reproducibility and data provenance

The repository preserves:

- `code/exact_window_certificates.py`: exact rational dynamic programming for risks of arbitrary finite odd window pairs.
- `code/round2_exact_enumeration.py`: explicit original $w=5$ posterior calculations.
- `code/certify_monotonic_width.py`: computer-assisted interval certificate for the width monotonicity assertion.
- `code/hmm_window_value.py`: independent fast numerical dynamic programming, used only as a cross-check.
- `code/verify_round9.py`: exact finite-risk identities and numerical illustrations of asymptotic bounds.
- `tests/test_round6.py` and `tests/test_round8.py`: exact regression tests.
- `data/*`: recorded deterministic outputs, including rational values, certificate summaries, and bound evaluations.

The exact finite-window tests use the Python standard library; the numerical cross-check and floating-point root proposals require NumPy and SciPy. See `README.md` and `REPRODUCIBILITY.md`. Source scripts from earlier exploratory stages are preserved for audit and may use historical file paths, which are documented rather than silently changed.

# Scientific conclusion and continuation decision

H-DATE-2 establishes, within a finite symmetric HMM, that decision-margin magnitudes can have strictly positive value conditional on a coarsened baseline information set and that window choices can yield non-unimodal risk. These results are mathematically checkable but model-specific. The stronger asymptotic rate targeted during the investigation was already published; a rediscovery must not be portrayed as originality.

**Decision:** close H-DATE-2 as an exploratory theoretical investigation. Preserve the manuscript, executable checks, references, and rejected conjectures. Do not propose a DATE production architecture or publish a competitive algorithm claim on the basis of this evidence. A future research direction should begin with a dedicated literature audit of finite-memory approximate filtering and a new falsifiable question, not with a relabeling of the established $q\log(1/q)$ rate.

# References {.unnumbered}

[1] D. Blackwell. "Equivalent Comparisons of Experiments." *Annals of Mathematical Statistics*, 24(2), 265–272, 1953. https://doi.org/10.1214/aoms/1177729032

[2] R. Z. Khasminskii and O. Zeitouni. "Asymptotic filtering for finite state Markov chains." *Stochastic Processes and their Applications*, 63(1), 1–10, 1996. (Cited in [3].)

[3] C. Nair, E. Ordentlich, and T. Weissman. "Asymptotic Filtering and Entropy Rate of a Hidden Markov Process in the Rare Transitions Regime." *Proceedings of the IEEE International Symposium on Information Theory (ISIT)*, 2005. https://doi.org/10.1109/ISIT.2005.1523663. Author-hosted PDF: https://web.stanford.edu/~tsachy/pdf_files/On%20asymptotic%20filtering%20and%20entropy%20rate%20for%20a%20hidden%20Markov.pdf

[4] G. Einziger, R. Friedman, and B. Manes. "TinyLFU: A Highly Efficient Cache Admission Policy." *ACM Transactions on Storage*, 13(4), 2017. https://doi.org/10.1145/3149371

[5] J. Yang et al. "FIFO Queues Are All You Need for Cache Eviction." *Proceedings of SOSP*, 2023. https://s3fifo.com/

[6] J. Yang et al. "SIEVE Is Simpler than LRU: An Efficient Cache Eviction Algorithm for Web Caches." *USENIX NSDI*, 2024. https://www.usenix.org/conference/nsdi24/presentation/zhang-yazhuo

# Appendix A. Research claim ledger

| Claim | Classification | Evidence |
|:--|:--|:--|
| Margins have positive Bayes value at $(0.8,0.9;1,5)$ | Exactly verified in finite model | Rational DP, 0.010781568 |
| Magnitudes are redundant if determined by baseline history | Elementary theorem | Conditional expectation |
| Larger magnitude value implies lower total risk across window pairs | Refuted | Exact pairwise comparison |
| Window risk is unimodal | Refuted | Two strict local minima |
| Short window 1 is full-history optimal for $r\le\alpha$ | Proved under model | Posterior odds argument |
| Critical persistence interval width decreases in $\alpha$ | Computer-assisted certified | Rational intervals, with code-review caveat |
| Rare-transition Bayes filtering rate $q\log(1/q)$ | Previously published | Khasminskii–Zeitouni 1996; Nair et al. 2005 |
| End-to-end cache improvement | Not investigated | No public traces / physical-cache integration |

# Appendix B. Terminology and accounting

- **Filtering:** infer $S_t$ from noisy emissions observed up to time $t$.
- **Prediction:** infer $Y_{t+1}$ from observations through time $t$.
- **State-aware oracle:** knows the relevant hidden state and has irreducible emission error $1-\alpha$.
- **Full-history Bayes predictor:** sees all *observable* past emissions, but not hidden states; incurs an additional rare-transition filtering penalty.
- **Sign-only controller:** observes $(\operatorname{sign}m_s,\operatorname{sign}m_w)$.
- **Magnitude-aware controller:** additionally observes $(|m_s|,|m_w|)$.
- **Bayes information value:** risk of sign-only minus risk of magnitude-aware controller *for the same window pair*.
- **Exact evidence:** finite enumerations using rational arithmetic; no statistical confidence interval is applicable to such exact finite probabilities.
- **Empirical evidence:** in the earlier DATE exploratory study, synthetic runs were conducted but do not establish a cache-policy gain; they are not reused as evidence for this HMM result.