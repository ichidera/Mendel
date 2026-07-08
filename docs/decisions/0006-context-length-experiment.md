# ADR 0006: Longer context doesn't flip the attention comparison, and a metric gap it exposed

**Status:** accepted
**Date:** Phase 1, attention follow-up experiment
**Related requirement(s):** `docs/requirements/functional/reasoning.md`, `docs/requirements/non-functional/reliability.md`

## Context

ADR 0005 found `CharAttn` underperforming `CharMLP` at `context_size=3` and flagged, as open follow-up, that a longer context window was the condition where attention's actual advantage (flexible, content-dependent weighting) should have room to show up. This ADR records that follow-up experiment.

`eval/baseline/experiment_context_length.py` runs both models at `context_size=10` (corpus lines are 48-66 characters, so this is well within range), keeping everything else — corpus, seed, hidden size, learning rate — identical to isolate context length as the one changed variable, per the project's evaluation discipline. The official `config.py` (`context_size=3`) was left untouched so `test_regression.py` keeps comparing against a stable target.

## Result

At `context_size=10`, 600 epochs (matching the original comparison's budget):

| | val loss |
|---|---|
| CharMLP | 2.7216 |
| CharAttn | 2.8945 |

CharAttn still regressed (+0.17 nats), a similar margin to the `context_size=3` result in ADR 0005. But the *shape* of the curves differed meaningfully: at `context_size=3`, CharAttn overfit quickly (train loss dropping, val loss rising from very early). At `context_size=10`, CharAttn's train loss plateaued around 2.78-2.9 through epoch 600 while val loss was still slowly decreasing — a convergence-speed signature, not an overfitting one.

Extending to 2500 epochs to check whether CharAttn would eventually catch up: val loss reached its actual minimum at epoch ~1000 (2.8126), then overfit severely past that point (val loss 7.68 by epoch 2500, train loss collapsed to 0.24). **CharAttn's best achievable point, with ideal early stopping, was still worse than CharMLP's best achievable point at the same context length** (CharMLP's minimum was ~2.6964, around epoch 500).

## Interpretation

Longer context did not flip the result. It changed *how* CharAttn loses (slow convergence then eventual overfitting, rather than immediate overfitting), but the ceiling on how well it can generalize on this corpus, at this scale, is still below CharMLP's. This weakens (without fully ruling out) the "context length is the missing condition" hypothesis from ADR 0005 — the more likely remaining candidates are corpus size and/or regularization, both still untested.

## A methodology gap this surfaced

Both `run.py`'s and `run_attention.py`'s harnesses, and the checked-in `results/baseline.json`, currently compare models using the **final epoch's** val loss, not the **best** val loss achieved during training. Given both models visibly overfit within a large enough epoch budget, final-epoch comparison is somewhat arbitrary — it partly measures "how well-matched is the fixed epoch count to this specific model," not purely "how good can this model get." Standard practice (and a fairer comparison) would track and report best-val-loss-with-early-stopping as the primary metric.

This wasn't changed as part of this ADR — changing what `test_regression.py` measures is a real decision affecting what "regression" means, not something to do silently inside an experiment writeup. Flagged as open follow-up.

## Decision

- Keep the ADR 0005 decision in place: `CharAttn` remains a comparison tool, not the Phase 1 baseline.
- Do not conclude the "attention needs more data" and "attention needs regularization" hypotheses from ADR 0005 are ruled out — this experiment only tested context length, and ruled that variable out specifically, not the others.

## Open follow-up

- Test corpus size as the remaining ADR 0005 hypothesis (more data to justify `Wq`/`Wk`/`Wv`'s added capacity).
- Test regularization (weight decay or equivalent) before concluding capacity mismatch is unfixable at this scale.
- Consider adding best-val-loss (with early stopping) as a tracked metric in `run.py`/`run_attention.py`, alongside or instead of final-epoch loss, given both models visibly overfit within currently-used epoch budgets. This would change what `results/baseline.json` represents and needs a deliberate decision, not a silent change.

## Related eval

`eval/baseline/experiment_context_length.py` (new, this ADR). Diagnostic 2500-epoch run was ad hoc, not saved to a results file, same as ADR 0005's diagnostic run.
