"""
CI-facing regression test. Re-runs the exact baseline config and compares
against the checked-in results/baseline.json. Fails loudly if:
  (a) the model no longer learns at all (sanity floor on train loss), or
  (b) best-epoch val loss regresses beyond tolerance vs. the recorded baseline.

Compares on BEST-epoch val loss (with implicit early stopping), not the
final epoch's val loss. See docs/decisions/0007-best-epoch-metric.md: both
models visibly overfit within a long enough epoch budget, so final-epoch
comparison was partly measuring "how well-matched is the epoch count," not
purely "how good can this model get." Best-epoch is the fairer comparison
and the one any real training pipeline would actually use (early stopping).

This is the file attention (or any future architecture change) needs to
pass before it's allowed to replace this baseline model. Run it before and
after any change to engine/ or architecture/ to know whether you improved
or regressed things.
"""
import sys
import os
import json

sys.path.insert(0, os.path.dirname(__file__))
from config import BaselineConfig  # noqa: E402
from run import run_baseline  # noqa: E402

# How much worse best-epoch val loss is allowed to get before we call it a
# regression, rather than normal run-to-run noise.
VAL_LOSS_TOLERANCE = 0.05          # absolute nats
SANITY_MAX_TRAIN_LOSS = 2.5        # if train loss can't beat this, something's broken


def load_baseline():
    path = os.path.join(os.path.dirname(__file__), "results", "baseline.json")
    with open(path) as f:
        return json.load(f)


def test_regression():
    baseline = load_baseline()
    config = BaselineConfig()  # must match the config baseline.json was recorded with
    metrics = run_baseline(config, verbose=False)

    print(f"baseline best_val_loss:  {baseline['best_val_loss']:.4f}  "
          f"(epoch {baseline['best_val_epoch']})")
    print(f"current  best_val_loss:  {metrics['best_val_loss']:.4f}  "
          f"(epoch {metrics['best_val_epoch']})")
    print(f"baseline final_train_loss: {baseline['final_train_loss']:.4f}")
    print(f"current  final_train_loss: {metrics['final_train_loss']:.4f}")

    assert metrics["final_train_loss"] < SANITY_MAX_TRAIN_LOSS, (
        f"Sanity check failed: final train loss {metrics['final_train_loss']:.4f} "
        f"did not beat {SANITY_MAX_TRAIN_LOSS} -- the model may not be learning at all."
    )

    regression = metrics["best_val_loss"] - baseline["best_val_loss"]
    assert regression < VAL_LOSS_TOLERANCE, (
        f"Regression detected: best-epoch val loss got worse by {regression:.4f} nats "
        f"(tolerance is {VAL_LOSS_TOLERANCE}). Baseline: {baseline['best_val_loss']:.4f}, "
        f"current: {metrics['best_val_loss']:.4f}."
    )

    print("\nPASS -- no regression vs. checked-in baseline (best-epoch comparison).")


if __name__ == "__main__":
    test_regression()
