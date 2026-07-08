# eval/baseline/

The regression harness for Mendel's Phase 1 baseline model (`architecture/model.py`'s `CharMLP`). This is the thing any future architecture change — attention, MoE, anything else — has to run against before it's allowed to replace what's here.

## What this actually measures

Not one of the seven functional capabilities in `docs/requirements/functional/` yet — those (reasoning, planning, tool-use, etc.) all assume a model capable of much more than next-character prediction. This benchmark measures something more basic and more foundational: **can the engine correctly train a model that generalizes at all**, on held-out data, reproducibly. Every capability in `functional/` depends on that being true first. Think of this as the substrate check, not a capability check — `docs/requirements/` doesn't have a home for it yet, which is itself worth resolving once Phase 1 wraps.

## Scope note: this directory currently owns a training loop

`eval/README.md` says this directory only measures, it doesn't build. `run.py` violates that, on purpose, for now: it runs a full training loop, not just an evaluation. That's because no other module currently owns "plain baseline training with no teacher model" — `distillation/README.md` is scoped to teacher-student training specifically, and `ROADMAP.md` doesn't list `distillation/` as a Phase 1 owner at all. See `docs/decisions/0003-baseline-training-and-reproducibility.md` for the full reasoning. Once Phase 2's distillation pipeline exists, the training loop in `run.py` should move there, and this directory should shrink back down to loading a checkpoint and measuring it, as originally intended.

## Files

```
eval/baseline/
├── corpus.txt          # larger than engine/examples' tiny demo corpus -- needs
│                          enough lines for a meaningful train/val split
├── config.py            # BaselineConfig -- the one place hyperparameters live
├── data.py               # line-based train/val split + context/target pair building
├── run.py                # trains the model, reports train/val loss and perplexity
├── test_regression.py    # CI check: compares a fresh run against results/baseline.json
└── results/
    ├── baseline.json      # checked-in reference metrics -- the thing test_regression.py compares against
    └── latest.json        # overwritten by every run.py invocation, gitignore-able
```

## Why line-based splitting, not random pair splitting

Splitting individual (context, target) pairs randomly would let a val example be three characters away from a training example the model already memorized — a weak, misleadingly optimistic generalization check. Splitting whole lines means every val line is a genuinely unseen sequence. Still a small, toy-scale corpus — this isn't a rigorous ML claim, just a meaningfully more honest one than the alternative.

## Running it

```bash
python3 run.py               # trains, prints metrics, writes results/latest.json
python3 test_regression.py   # re-runs the same config, fails if it regressed vs. baseline.json
```

## Updating the baseline

If a change is a deliberate, understood improvement (not a regression), re-run `run.py` and copy `results/latest.json` over `results/baseline.json` — but do this in the same PR as the change that caused the improvement, with the reasoning in the PR description or a new entry in `docs/decisions/`, so "the baseline changed" always has a paper trail.
