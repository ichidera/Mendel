# ADR 0005: Attention memory lifecycle fix, and an honest first result

**Status:** accepted
**Date:** Phase 1, first attention implementation pass
**Related requirement(s):** `docs/requirements/functional/reasoning.md`, `docs/requirements/non-functional/reliability.md`, `docs/requirements/non-functional/footprint.md`

## Part 1: the memory lifecycle bug

Testing `CharAttn` (the new self-attention model) at higher epoch counts to distinguish "undertrained" from "genuinely worse" caused the process to be OOM-killed at both 2000 and 1200 epochs. Root cause: every intermediate tensor `self_attention` and the rest of the forward/backward pass create (Q, K, V, scores, probs, attended, and everything in the surrounding MLP layers) is a fresh allocation, and per ADR 0002/0004's `engine/` design, nothing frees automatically — `Tensor.__del__` was deliberately removed to avoid the dangling-pointer hazard documented there. That tradeoff was fine for short gradient checks and a few hundred training epochs; it is not fine for a training loop of any real length. Estimated leak: roughly 3MB/epoch for `CharAttn` on this toy corpus, meaning 2000 epochs projects to several GB, which exceeded the available memory.

**Fix:** added a tensor registry (`_ALL_TENSORS`) and `free_all_except(keep_tensors)` to `engine/python/mendel_core.py`. Every `Tensor` registers itself on construction; `free_all_except()` frees everything in the registry except the tensors passed in (in practice, a model's parameters) and resets the registry. Both `eval/baseline/run.py` and `run_attention.py` now call `core.free_all_except(model.parameters())` once per epoch, after extracting any scalar values (loss, val loss) as plain Python floats — extracting first, freeing second, matches the exact hazard `.free()`'s docstring already warns about.

**Verified:** `CharAttn` at 2000 epochs now completes in ~117s with peak RSS of ~20MB, versus an OOM kill before the fix. `Tensor.free()` also gained a double-free guard (`_freed` flag) since the sweep now calls it automatically and a caller might still call it manually too.

## Part 2: the actual experiment result

With the memory fix in place, `CharAttn` was compared against the `CharMLP` baseline under identical config (same seed, data split, hidden size, learning rate) at two epoch counts:

| | 600 epochs | 2000 epochs |
|---|---|---|
| CharMLP val loss | 2.4648 | 2.6355 |
| CharAttn val loss | 2.7504 | 2.9917 |

**CharAttn is worse than CharMLP at every comparison point, and more training time widens the gap rather than closing it** — train loss for CharAttn dropped sharply (2.60 → 1.41) while val loss got worse (2.75 → 2.99), a textbook overfitting signature, and a clearly worse one than CharMLP shows over the same epoch increase (2.46 → 2.64).

## Interpretation — what this does and doesn't mean

This is **not** evidence that attention is broken or that the implementation is wrong — the gradient checks in `engine/tests/test_attention_gradients.py` independently confirm the math is correct. The likely explanation is scale mismatch, not correctness:

- `CharAttn` adds real parameters (`Wq`, `Wk`, `Wv`, 768 extra floats) that `CharMLP` doesn't have, on a corpus of under 1,000 training pairs — more capacity than this amount of data can justify.
- The context window is only 3 characters. Plain concatenation already preserves full positional information losslessly at that length; attention's actual advantage (flexible, content-dependent weighting across longer or more variable-length context) has essentially no room to pay for its added capacity here.
- This matches a well-known pattern in the broader literature: attention-based architectures tend to be more data-hungry than simpler architectures with stronger built-in inductive bias, and often need more data or longer sequences before their advantage shows up.

**This should not be read as "abandon attention."** It should be read as "this specific toy-scale comparison doesn't yet give attention a fair chance to show its value" — exactly the kind of finding an honest eval harness is supposed to produce, rather than either hiding it or over-claiming a win.

## Decision

- Ship the memory lifecycle fix as a correctness requirement, not optional cleanup — any future model addition to `architecture/` needs `free_all_except()` wired into its training loop before being tested at any real epoch count.
- Do **not** promote `CharAttn` to replace `CharMLP` as the Phase 1 baseline. Keep both, with `run_attention.py` remaining an explicit comparison tool against `results/baseline.json`, per `eval/baseline/README.md`'s existing design.
- Record this result plainly rather than tuning hyperparameters until attention wins, which would defeat the purpose of an honest comparison.

## Open follow-up

- Test whether a longer or more variable-length context (where attention's actual advantage should manifest) changes this result — current corpus/context design may be structurally unfavorable to attention regardless of tuning.
- Test with a larger corpus, where `Wq`/`Wk`/`Wv`'s added capacity has enough data to be justified rather than immediately overfitting.
- Consider regularization (weight decay, dropout-equivalent) before concluding anything definitive about capacity mismatch versus a fixable overfitting problem.
- The scale-mismatch interpretation above is a reasonable hypothesis given the literature, not a proven cause — it should be tested, not assumed, before being treated as settled.

## Related eval

`eval/baseline/run_attention.py`, `eval/baseline/results/attention_latest.json` (600-epoch run). The 2000-epoch comparison run was a diagnostic check, not saved to a results file — worth formalizing into the harness if longer-horizon comparisons become routine.
