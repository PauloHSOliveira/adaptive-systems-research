# Study 002 — DATE

**Status:** The original DATE engineering direction is suspended. The H-DATE-2 mathematical follow-up is closed, with no claim of a novel general-purpose cache algorithm.

## Research documents

- [Original DATE exploratory paper](paper.md) — temporal frequency-estimator selection, synthetic diagnostic, negative/inconclusive outcomes, and experimental limitations.
- [H-DATE-2 final mathematical working paper](h-date-2/paper.md) — exact HMM results, counterexamples, literature audit and closeout.
- [H-DATE-2 reproducibility guide](h-date-2/REPRODUCIBILITY.md) — independent code and evidence.
- [H-DATE-2 claim ledger](h-date-2/data/claims.csv) — proved, certified, refuted and open claims.

## Original synthetic diagnosis

The original study used two decayed Count-Min Sketch horizons and compared sign/feedback features against margin features. Its offline static-swap loss is **not** end-to-end cache miss cost. Twelve scenario/seed runs were exploratory and did not establish a stable improvement. No public trace evaluation or faithful upstream W-TinyLFU integration was completed.

Original code: [code](code/). Original data: [data](data/). Do not treat the pre-holdout instrumentation as a production integration.

## H-DATE-2 conclusion

A finite symmetric binary HMM provides a valid example where margin magnitudes have strictly positive **Bayes decision value** after conditioning on the two decision signs. However, this result is model-specific, and larger feature value need not lead to lower total risk across different window pairs.

Crucially, the optimal rare-transition filtering rate of order `q log(1/q)` was established in prior literature (Khasminskii–Zeitouni 1996; Nair–Ordentlich–Weissman 2005). The mathematical follow-up was therefore closed as a research exploration rather than presented as a new algorithm or previously undiscovered asymptotic theorem.

Run the maintained H-DATE-2 checks:

```bash
cd research/002-date/h-date-2
python -m pip install -r requirements.txt
PYTHONPATH=code python -m unittest discover -s tests -v
```
