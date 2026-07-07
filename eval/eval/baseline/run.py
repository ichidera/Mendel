"""
Runs the Phase 1 baseline (architecture/model.py's CharMLP) to completion
and reports train/val loss and val perplexity.

Scope note, flagged deliberately: this file owns a training loop, which is
arguably not eval/'s job per eval/README.md ("this directory only measures,
it doesn't build"). It lives here anyway, for now, because no other module
currently owns "plain baseline training with no teacher model" -- see
docs/decisions/0003-eval-owns-baseline-training-temporarily.md. Once Phase 2
distillation work exists, this training loop should move there, and this
file should shrink down to just loading a checkpoint and measuring it.
"""
import sys
import os
import math
import json
import time
import random

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "architecture"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "engine", "python"))
import core  # noqa: E402
from model import CharMLP, CharMLPConfig  # noqa: E402

from config import BaselineConfig  # noqa: E402
import data  # noqa: E402


def compute_loss(model, X, Y):
    """Forward-only loss on a (possibly held-out) dataset. No backward call,
    no optimizer step -- this is a pure measurement, safe to call on val
    data without ever letting gradients touch it."""
    logits = model.forward(X)
    loss = core.softmax_cross_entropy(logits, Y)
    return loss.ptr[0]


def run_baseline(config: BaselineConfig, verbose=True):
    random.seed(config.seed)  # core.param() draws from the global `random` module --
                               # without this, model init is silently different every process
    lines = data.load_lines()
    vocab, stoi, itos = data.build_vocab(lines)
    train_lines, val_lines = data.split_lines(lines, config.val_fraction, config.seed)

    X_train, Y_train = data.build_pairs(train_lines, stoi, config.context_size)
    X_val, Y_val = data.build_pairs(val_lines, stoi, config.context_size)

    if verbose:
        print(f"vocab size: {len(vocab)} | train lines: {len(train_lines)} "
              f"({len(X_train)} pairs) | val lines: {len(val_lines)} ({len(X_val)} pairs)")

    model_config = CharMLPConfig(len(vocab), config.context_size, config.embed_dim, config.hidden)
    model = CharMLP(model_config)
    opt = core.SGD(model.parameters(), lr=config.lr)

    history = []
    for epoch in range(1, config.epochs + 1):
        opt.zero_grad()
        logits = model.forward(X_train)
        loss = core.softmax_cross_entropy(logits, Y_train)
        loss.backward()
        opt.step()

        if epoch == 1 or epoch % config.eval_every == 0 or epoch == config.epochs:
            train_loss = loss.ptr[0]
            val_loss = compute_loss(model, X_val, Y_val)
            history.append({"epoch": epoch, "train_loss": train_loss, "val_loss": val_loss})
            if verbose:
                print(f"  epoch {epoch:4d}  train_loss {train_loss:.4f}  val_loss {val_loss:.4f}")

    final_train_loss = history[-1]["train_loss"]
    final_val_loss = history[-1]["val_loss"]
    val_perplexity = math.exp(final_val_loss)

    return {
        "config": config.as_dict(),
        "vocab_size": len(vocab),
        "train_pairs": len(X_train),
        "val_pairs": len(X_val),
        "final_train_loss": final_train_loss,
        "final_val_loss": final_val_loss,
        "val_perplexity": val_perplexity,
        "history": history,
    }


def main():
    config = BaselineConfig()
    metrics = run_baseline(config)

    print(f"\nfinal train loss: {metrics['final_train_loss']:.4f}")
    print(f"final val loss:   {metrics['final_val_loss']:.4f}")
    print(f"val perplexity:   {metrics['val_perplexity']:.4f}")

    results_dir = os.path.join(os.path.dirname(__file__), "results")
    os.makedirs(results_dir, exist_ok=True)
    out = dict(metrics)
    out["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    with open(os.path.join(results_dir, "latest.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nwrote {os.path.join(results_dir, 'latest.json')}")


if __name__ == "__main__":
    main()
