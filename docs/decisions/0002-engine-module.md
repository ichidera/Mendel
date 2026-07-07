# ADR 0002: Add a top-level `engine/` module

**Status:** accepted
**Date:** Phase 1, first implementation pass
**Related requirement(s):** `docs/requirements/non-functional/extensibility.md`, `docs/requirements/functional/reasoning.md` (the baseline this engine trains toward)

## Context

Starting Phase 1's "first trainable baseline" surfaced a real gap in the original repo layout. `architecture/README.md` states it owns model definition (layers, forward pass) but explicitly disclaims training and running on hardware. `inference/README.md` owns running a *finished* checkpoint. Neither owns the actual tensor math and autograd machinery — the forward/backward compute primitives — that both training and inference ultimately sit on top of. Writing the Phase 1 baseline meant either wedging raw C tensor ops into `architecture/` (which isn't what that module's README promises) or inventing a new home for it.

Separately, the chosen implementation approach for this compute layer was hand-written C (no PyTorch/NumPy/JAX), called from Python via `ctypes`, per the decision to prioritize genuine understanding of the C/Python boundary over framework convenience, and CPU-only for this first pass, deferring GPU/CUDA to a later phase.

## Decision

Add a new top-level module, `engine/`, responsible for:
- Raw C math kernels (forward + hand-derived backward) for every tensor operation the baseline model needs
- A Python autograd layer that builds a computation graph and dispatches to the C kernels, doing no arithmetic itself
- ctypes bindings between the two
- Correctness verification via numerical gradient checking, treated as a gate before any training claim is trusted

`architecture/README.md` and `inference/README.md` are unchanged — this module fills the gap between them rather than redefining either.

## Alternatives considered

- **Put it inside `architecture/`.** Rejected: `architecture/`'s stated job is model *shape*, not the underlying compute substrate; conflating the two would make that module's README inaccurate on day one.
- **Put it inside `inference/`.** Rejected: `inference/` is explicitly about running a *finished, trained* checkpoint. The engine needs to support backward passes for training, which `inference/` has no reason to own.
- **Use NumPy for the math instead of hand-written C.** Considered and rejected for this phase specifically because the project's stated interest (see earlier project discussion) was in genuinely understanding the C/Python boundary, not just training a model as fast as possible. Revisit if development velocity on later phases is bottlenecked by this choice.

## Consequences

- `docs/requirements/non-functional/extensibility.md` should have its module list updated to include `engine/` alongside the others once a maintainer reviews this ADR.
- Future architecture work (attention, full transformer blocks) depends on `engine/csrc/` growing new ops (attention forward/backward) before `architecture/attention/` can be implemented against them.
- GPU support is deferred; when it's tackled, it likely extends `engine/`'s C API with a CUDA backend behind the same function signatures, rather than requiring a new module.

## A related bug worth recording here too

Building this engine's first version surfaced a genuine correctness bug, not just a design question: `Tensor.__del__` originally freed C buffers automatically on Python garbage collection. Because CPython's refcounting is immediate (not deferred), an expression like `forward().ptr[0]` freed the temporary Tensor's buffer the instant `.ptr` was accessed, before the subsequent index read it — silently returning garbage instead of erroring. Fixed by removing automatic freeing entirely in favor of an explicit `.free()` method; the engine leaks memory by default now, deliberately, in exchange for never silently reading freed memory. Full detail in `engine/README.md`. Recording it here too because it's exactly the kind of failure that would otherwise get quietly re-discovered by the next person who touches this code.

## Related eval

None yet — Phase 1 baseline behavior (loss decreasing over training on the tiny char-MLP example) was checked manually via `engine/examples/train_char_mlp.py`, not yet formalized as an `eval/` benchmark. Formalizing that is open follow-up work.
