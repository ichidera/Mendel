"""
Experiment, not part of the CI regression suite: does attention's advantage
show up with a longer context window? The official Phase 1 baseline
(config.py, context_size=3) stays untouched so test_regression.py keeps
comparing against a stable target -- this script builds its own config with
a longer context and runs both models against it, isolating exactly one
variable (context length) versus the original comparison in ADR 0005.
"""
import sys
import os
import time

sys.path.insert(0, os.path.dirname(__file__))
from config import BaselineConfig  # noqa: E402
from run import run_baseline  # noqa: E402
from run_attention import run_attention  # noqa: E402

CONTEXT_SIZE = 10


def main():
    config = BaselineConfig()
    config.context_size = CONTEXT_SIZE

    print(f"=== CharMLP, context_size={CONTEXT_SIZE} ===")
    t0 = time.time()
    mlp_metrics = run_baseline(config, verbose=True)
    print(f"({time.time() - t0:.1f}s)\n")

    print(f"=== CharAttn, context_size={CONTEXT_SIZE} ===")
    t0 = time.time()
    attn_metrics = run_attention(config, verbose=True)
    print(f"({time.time() - t0:.1f}s)\n")

    print("=== comparison ===")
    print(f"CharMLP  val loss: {mlp_metrics['final_val_loss']:.4f}  "
          f"(perplexity {mlp_metrics['val_perplexity']:.4f})")
    print(f"CharAttn val loss: {attn_metrics['final_val_loss']:.4f}  "
          f"(perplexity {attn_metrics['val_perplexity']:.4f})")
    delta = attn_metrics["final_val_loss"] - mlp_metrics["final_val_loss"]
    verdict = "CharAttn IMPROVED" if delta < 0 else "CharAttn REGRESSED" if delta > 0 else "UNCHANGED"
    print(f"delta: {delta:+.4f} nats ({verdict})")


if __name__ == "__main__":
    main()
