# ADR 0003: Baseline training lives in eval/ temporarily, and a reproducibility bug it surfaced

**Status:** accepted
**Date:** Phase 1, eval harness pass
**Related requirement(s):** `docs/requirements/non-functional/reliability.md`, `docs/requirements/non-functional/extensibility.md`

## Context

Building a regression harness for the Phase 1 baseline required a training loop to exist somewhere. `eval/README.md` states this directory only measures, it doesn't build. But checking `distillation/README.md`, that module is scoped specifically to *teacher-student* training — and `ROADMAP.md` confirms Phase 1 doesn't list `distillation/` as an owner at all. There is currently no module whose stated job is "train a model from scratch on raw data, no teacher involved."

Separately, while building this harness, `test_regression.py` caught real non-determinism: three runs of the identical config (`seed=0`) produced three different final val losses (2.4897, 2.4240, 2.5467).

## Decision

**On training ownership:** `eval/baseline/run.py` owns the Phase 1 training loop for now, explicitly flagged in that file's docstring and in `eval/baseline/README.md` as temporary. When Phase 2 distillation work lands, this loop moves there, and `eval/baseline/` reverts to only measuring a checkpoint someone else produced.

**On the reproducibility bug:** root cause was `architecture/model.py`'s `CharMLP` calling `core.param()`, which draws from Python's *global* `random.gauss()`. `eval/baseline/config.py`'s `seed` was only ever passed to `data.split_lines()`'s locally-scoped `random.Random(seed)` instance — the global module state used for weight initialization was never seeded at all, so it inherited whatever state a fresh Python process's `random` module auto-seeds itself with from OS entropy. Fixed by calling `random.seed(config.seed)` at the top of `run_baseline()`, before model construction. Verified: two independent process runs now produce bit-identical metrics.

## Alternatives considered

- **Add a new `training/` top-level module now**, rather than temporarily housing this in `eval/`. Rejected for the moment: premature to build a whole new module's scaffolding (README, ownership, CODEOWNERS entry) for a training loop that's explicitly a stepping stone to the real thing in Phase 2. Revisit if Phase 2 turns out to be far off and this "temporary" arrangement outlives its welcome.
- **Pass an explicit `Random` instance through `core.param()` instead of relying on the global module.** This is arguably the more correct long-term fix — global mutable RNG state is a known footgun — but it's a larger API change to `engine/python/core.py` touching every call site. Deferred; tracked as an open item below rather than done as part of this pass.

## Consequences

- `eval/baseline/results/baseline.json` reflects the *post-fix* deterministic run (final train loss 2.0984, final val loss 2.4648, val perplexity 11.76) — not the earlier non-deterministic numbers seen during debugging, which were never valid baselines to begin with.
- Any future contributor adding new randomized behavior to `engine/` or `architecture/` should check whether it draws from the global `random` module and, if so, make sure `run_baseline()`'s seeding actually covers it — this class of bug is easy to reintroduce silently.
- `docs/requirements/non-functional/reliability.md` should note reproducibility (same seed, same result) as an explicit acceptance criterion given this was a real, caught regression risk, not a hypothetical one.

## Open follow-up

Replace global-`random`-module reliance in `engine/python/core.py`'s `param()` with an explicitly-passed RNG instance, so reproducibility doesn't depend on every caller remembering to seed a global module correctly.

## Related eval

`eval/baseline/test_regression.py` — this is simultaneously the decision record's justification and the thing that will catch anyone regressing this fix in the future.
