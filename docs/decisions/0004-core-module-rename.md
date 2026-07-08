# ADR 0004: Rename engine's `core.py` to `mendel_core.py`

**Status:** accepted
**Date:** Phase 1, post-eval-harness fix
**Related requirement(s):** `docs/requirements/non-functional/reliability.md`, `docs/requirements/non-functional/extensibility.md`

## Context

After merging the engine, architecture, and eval deliverables into a real local repo, `eval/baseline/test_regression.py` failed with an `AttributeError` on `core.param` — the `core` module it imported didn't have the function `engine/python/core.py` defines. Every file (`architecture/model.py`, `engine/examples/train_char_mlp.py`, `engine/tests/test_gradients.py`, `eval/baseline/run.py`) imported the engine's autograd module via a bare `import core`.

`core` is a dangerously generic, collision-prone module name. Python caches imported modules by name in `sys.modules`; if anything else reachable on `sys.path` — a third-party package, a stale compiled file, another same-named file anywhere else in a larger merged repo — is imported as `core` before our engine's `core.py` is, every subsequent `import core` anywhere in the process silently returns that *other* module instead, with no error. The symptom (a real function missing on the module) matches this exactly.

## Decision

Rename `engine/python/core.py` to `engine/python/mendel_core.py`. Every consuming file now does `import mendel_core as core` — the alias keeps the rest of each file's code unchanged (still reads as `core.param(...)`, `core.matmul(...)`, etc.), while the actual imported name is specific enough to make a real collision essentially impossible.

Updated files:
- `architecture/model.py`
- `engine/examples/train_char_mlp.py`
- `engine/tests/test_gradients.py`
- `eval/baseline/run.py`

## Alternatives considered

- **Debug the exact collision source in the reporter's environment first.** Rejected as the primary fix: even if we'd identified the exact colliding package/file, the underlying fragility (a one-word, generic module name for a core piece of infrastructure) would remain and could resurface with a different collision later. Fix the class of bug, not just this instance.
- **Turn `engine/python/` into a proper installable package** (with an `__init__.py` and a project-qualified import path like `from mendel.engine import core`) instead of a rename. More correct long-term, but a bigger structural change than this bug warranted right now — tracked as a future open item rather than done here.

## Consequences

- No behavior changed — verified bit-identical results on the gradient check, the example training script, and the eval baseline regression test before and after the rename.
- Any new file added to `engine/`, `architecture/`, or `eval/` that needs the autograd engine should use `import mendel_core as core`, not `import core`.
- `bindings.py` was left as-is; its name is generic too but lower collision risk in practice, and it's only ever imported from within `mendel_core.py` itself, not scattered across the repo. Worth revisiting under the same logic if it ever causes a similar issue.

## Open follow-up

Consider the proper-package restructuring (`__init__.py`, project-qualified imports) mentioned above once `engine/` stabilizes past Phase 1 — it would remove this whole class of naming-collision risk permanently, rather than mitigating it file by file.
