# ADR 0007: Switch regression metric to best-epoch val loss, refresh all baselines

**Status:** accepted
**Date:** Phase 1, eval methodology fix
**Related requirement(s):** `docs/requirements/non-functional/reliability.md`, `docs/requirements/functional/reasoning.md`

## Context

ADR 0006 flagged, as an open item, that `run.py`/`run_attention.py` and `results/baseline.json` compared models on **final-epoch** val loss, despite both models visibly overfitting within their training budgets. That makes the comparison partly measure "how well-matched is the fixed epoch count," not purely "how good can this model get" — a real methodology gap, not a footnote.

## Decision

Switched the primary comparison metric to **best-epoch val loss** (the minimum val loss seen at any checkpoint during training, with its epoch recorded) — equivalent to what any real training pipeline would get from early stopping. Changes made:

- `config.py`: widened `epochs` from 600 to 2000 and tightened `eval_every` from 50 to 25, so the harness can actually observe a curve turn upward rather than being cut off before doing so.
- `run.py` / `run_attention.py`: both now compute and return `best_val_loss` / `best_val_epoch` / `best_val_perplexity` alongside the existing final-epoch metrics (final-epoch numbers are kept, not removed — still useful context, just no longer the comparison metric).
- `test_regression.py`: now asserts on `best_val_loss` regression against `results/baseline.json`, not `final_val_loss`.
- `results/baseline.json`: regenerated under the new config. **This changes what "regression" means** going forward — flagged explicitly here rather than done silently, per this project's own stated discipline.

## Refreshed numbers

**Official Phase 1 baseline (CharMLP, context_size=3):** true minimum val loss is **2.4045 at epoch 950** (perplexity 11.07) — clearly visible U-curve, val loss rises to 2.6355 by epoch 2000. The old final-epoch-600 reading (2.4648) that `test_regression.py` previously guarded was leaving real accuracy on the table by stopping before the actual optimum.

**CharAttn vs. CharMLP, context_size=3, both at best epoch:**

| | best val loss | best epoch |
|---|---|---|
| CharMLP | 2.4045 | 950 |
| CharAttn | 2.6737 | 1100 |

CharAttn still regresses (+0.2692 nats), consistent with ADR 0005's finding — reassuring that the earlier conclusion wasn't an artifact of unfair final-epoch comparison; it holds up under the more rigorous methodology too.

**CharAttn vs. CharMLP, context_size=10, both at best epoch:**

| | best val loss | best epoch | source |
|---|---|---|---|
| CharMLP | 2.6964 | 500 | freshly re-run through the fixed harness |
| CharAttn | 2.8126 | ~1000 | ADR 0006's prior ad hoc diagnostic run, not re-verified through this harness |

CharMLP's number matches the earlier ad hoc finding almost exactly, which is a good consistency check on the fix. CharAttn's number is carried over rather than freshly reproduced — see Limitations below.

## Limitations of this pass

Re-running `CharAttn` at `context_size=10` through the updated harness (2000 epochs, `eval_every=25`) exceeded the available execution time budget in this working session, twice, even after reducing to 1500 and then 1300 epochs with coarser `eval_every=50`. The context=10 CharAttn number in this ADR is therefore carried over from ADR 0006's diagnostic run rather than independently reproduced here. That run used the same underlying methodology (tracking val loss across many checkpoints and taking the minimum), so it's methodologically consistent — but it predates this specific harness change and hasn't been bit-for-bit re-verified against it. Worth a clean re-run whenever more time/compute is available, ideally in smaller batches that fit within whatever execution constraints apply.

## Alternatives considered

- **Keep final-epoch comparison, just tune epoch count until it roughly matches best-epoch.** Rejected: fragile and indirect — any future config change would silently break the "roughly matches" assumption. Tracking best-epoch directly is more honest and doesn't depend on picking the right fixed epoch count in advance.
- **Add early stopping to the training loop itself** (stop automatically once val loss stops improving for N checks), rather than running a fixed long budget and taking the post-hoc minimum. More realistic for an actual training pipeline, but adds a stopping-patience hyperparameter and changes training dynamics (e.g., interacts with learning rate schedules, if those get added later). Deferred — post-hoc best-epoch tracking gets the same comparison honesty without that added complexity, for now.

## Consequences

- `results/baseline.json` and `results/latest.json` now carry `best_val_loss`/`best_val_epoch`/`best_val_perplexity` fields; anything reading these files should use those, not `final_val_loss`, for regression purposes.
- Training runs now take longer by default (2000 epochs vs. 600), which is why the context=10 CharAttn re-run hit session time limits — worth keeping in mind when scoping future experiments in similarly time-boxed environments.
- The CharMLP baseline itself changed (2.4045 vs. the old 2.4648) — this is an improvement in what we're measuring, not a regression in the model itself; the model didn't get worse, we just stopped measuring it unfairly.

## Open follow-up

- Re-run `CharAttn` at `context_size=10` through the fixed harness in a properly time-boxed way (e.g., checkpointing progress across multiple shorter sessions) to fully close the gap flagged in Limitations.
- Consider real early stopping in the training loop itself, per the rejected alternative above, if post-hoc best-epoch tracking proves insufficient once training schedules get more complex (learning rate decay, etc.).
- ADR 0005's still-open hypotheses (corpus size, regularization) remain untested.

## Related eval

`eval/baseline/test_regression.py` (updated), `eval/baseline/results/baseline.json` (regenerated).
