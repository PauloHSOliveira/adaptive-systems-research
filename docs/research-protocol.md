# Experimental Research Protocol

## 1. Formulate a falsifiable question

For each study, document its ID, precise estimand, null and alternative hypotheses, claimed novelty, relevant prior work, eligible workloads, computational budget, and clear success or stop criteria **before** interpreting results. Separate algorithm novelty, analysis, replication and engineering variations.

## 2. Evidence hierarchy

1. Precisely scoped propositions with explicit assumptions and proofs.
2. Implementation invariants, property-based tests and exact numerical checks where applicable.
3. Synthetic exploratory benchmarks, labeled as exploratory.
4. Faithful independent baselines with pinned upstream versions.
5. Pre-registered comparisons on public traces or suitable held-out datasets.
6. Independent reproduction, transparent resource accounting and external review.

## 3. Causal temporal validation

A feature used at time `t` must not depend on labels or observations later than `t`. Offline counterfactual labels must be constructed **after** logging causal opportunities. In dynamic caches, a local one-step replacement loss is not the counterfactual total loss of two diverging cache policies. Distinguish static one-swap labels from full trajectories.

## 4. Fair comparisons

- Match physical cache capacity and loss models.
- Report all online metadata in **bytes**, including feature trackers and controller parameters.
- Measure CPU on comparable implementations and hardware; Python timing is not a substitute for native performance measurements.
- Pin exact baseline commits, configuration, seeds, and workload preprocessing.
- Include placebo and matched-capacity feature controls when testing information value.
- Avoid changing the primary comparator after looking at held-out results.

## 5. Statistical discipline

Define the statistic and comparison before evaluating the holdout. For correlated losses and overlapping future labels, use a justified dependent-data method and sensitivity analyses. Do **not** assume block length equal to the label horizon implies independent blocks or that `effective_n = T/H` universally. For a required relative gain of `g`, formulate the null around `loss_treatment-(1-g)*loss_control`, not a zero-gain test. Distinguish confidence intervals, failure to reject, equivalence tests, and engineering stop decisions.

## 6. Exact mathematics and external results

Separate proofs by hand from computer-assisted proofs with runnable certificates. Report which inequalities were checked by exact arithmetic and which approximations were merely numerical. Verify paper parameters and theorem hypotheses before claiming a new asymptotic rate. Reproduction of a previously published theorem must be cited as such.

## 7. Reproducibility archive

Store manifests, source code, tests, commands, dependence versions, random seeds, metadata budgets, raw outputs, observed failures, and license constraints. Retain negative results and unresolved concerns. Prefer self-contained source and public evidence to unsupported summaries.

## 8. Study lifecycle

Each new `research/NNN-slug/` should include:

- `paper.md` — current scientific working manuscript;
- `README.md` — status, commands and scope;
- `code/` and `tests/` — implementations and checks;
- `data/` — deterministic outputs and provenance;
- `references.bib` and `CITATION.cff` when useful.

A conclusion must state **proved**, **observed**, **not tested**, **refuted**, **open**, and **continuation decision** separately.
