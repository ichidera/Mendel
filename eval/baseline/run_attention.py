"""
Runs the same eval harness as run.py, same config, same data, same seeding
discipline -- the only thing that changes is swapping CharMLP for CharAttn.
This isolates exactly one variable: does self-attention over the context
help, compared to the plain-concatenation baseline, holding everything else
(hidden layer size, learning rate, data split, seed) constant.
"""
import sys
import os
import math
import json
import time
import random

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "architecture"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "engine", "python"))
import mendel_core as core  # noqa: E402
from model import CharAttn, CharMLPConfig  # noqa: E402

from config import BaselineConfig  # noqa: E402
import data  # noqa: E402


def compute_loss(model, X, Y):
    logits = model.forward(X)
    loss = core.softmax_cross_entropy(logits, Y)
    return loss.ptr[0]


def run_attention(config: BaselineConfig, verbose=True):
    random.seed(config.seed)
    lines = data.load_lines()
    vocab, stoi, itos = data.build_vocab(lines)
    train_lines, val_lines = data.split_lines(lines, config.val_fraction, config.seed)

    X_train, Y_train = data.build_pairs(train_lines, stoi, config.context_size)
    X_val, Y_val = data.build_pairs(val_lines, stoi, config.context_size)

    if verbose:
        print(f"vocab size: {len(vocab)} | train lines: {len(train_lines)} "
              f"({len(X_train)} pairs) | val lines: {len(val_lines)} ({len(X_val)} pairs)")

    model_config = CharMLPConfig(len(vocab), config.context_size, config.embed_dim, config.hidden)
    model = CharAttn(model_config)
    opt = core.SGD(model.parameters(), lr=config.lr)

    history = []
    t0 = time.time()
    for epoch in range(1, config.epochs + 1):
        opt.zero_grad()
        logits = model.forward(X_train)
        loss = core.softmax_cross_entropy(logits, Y_train)
        loss.backward()
        opt.step()
        train_loss = loss.ptr[0]

        do_eval = (epoch == 1 or epoch % config.eval_every == 0 or epoch == config.epochs)
        val_loss = compute_loss(model, X_val, Y_val) if do_eval else None

        # See run.py's identical comment: this bounds memory growth, which
        # matters a great deal more here -- CharAttn allocates several more
        # intermediate tensors per step (Q, K, V, scores, probs, attended)
        # than CharMLP does, so it hits the same unbounded-leak wall much
        # sooner. Discovered by literally OOM-killing a longer test run.
        core.free_all_except(model.parameters())

        if do_eval:
            history.append({"epoch": epoch, "train_loss": train_loss, "val_loss": val_loss})
            if verbose:
                elapsed = time.time() - t0
                print(f"  epoch {epoch:4d}  train_loss {train_loss:.4f}  "
                      f"val_loss {val_loss:.4f}  ({elapsed:.1f}s elapsed)")

    final_train_loss = history[-1]["train_loss"]
    final_val_loss = history[-1]["val_loss"]
    val_perplexity = math.exp(final_val_loss)

    return {
        "model": "CharAttn",
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
    metrics = run_attention(config)

    print(f"\nfinal train loss: {metrics['final_train_loss']:.4f}")
    print(f"final val loss:   {metrics['final_val_loss']:.4f}")
    print(f"val perplexity:   {metrics['val_perplexity']:.4f}")

    with open(os.path.join(os.path.dirname(__file__), "results", "baseline.json")) as f:
        baseline = json.load(f)

    print(f"\n--- comparison vs. CharMLP baseline ---")
    print(f"CharMLP  val loss: {baseline['final_val_loss']:.4f}  "
          f"(perplexity {baseline['val_perplexity']:.4f})")
    print(f"CharAttn val loss: {metrics['final_val_loss']:.4f}  "
          f"(perplexity {metrics['val_perplexity']:.4f})")
    delta = metrics["final_val_loss"] - baseline["final_val_loss"]
    verdict = "IMPROVED" if delta < 0 else "REGRESSED" if delta > 0 else "UNCHANGED"
    print(f"delta: {delta:+.4f} nats ({verdict})")

    results_dir = os.path.join(os.path.dirname(__file__), "results")
    out = dict(metrics)
    out["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    with open(os.path.join(results_dir, "attention_latest.json"), "w") as f:
        json.dump(out, f, indent=2)


if __name__ == "__main__":
    main()
