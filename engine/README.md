# engine/

The raw tensor math and autograd substrate everything else is built on: hand-written C for every numerical operation, a thin Python autograd layer that only orchestrates *when* to call C, never doing arithmetic itself.

**This module doesn't appear in the original repo layout.** It surfaced as a real gap once Phase 1 work actually started: `architecture/` defines the model's shape, `inference/` runs a *finished* checkpoint, but neither owns the forward/backward compute primitives both training and running actually need. Rather than wedge this into either, it gets its own top-level directory. See `docs/decisions/0002-engine-module.md` for the full reasoning — this note is a summary, not the record.

## Responsible for
- Raw C math kernels: matmul, bias-add, ReLU, embedding lookup, softmax cross-entropy — each with both a forward and a hand-derived backward implementation (`csrc/`)
- A minimal autograd engine in Python (`python/core.py`) that builds a computation graph and calls the right C forward/backward function at the right time — no math happens in this file, only graph bookkeeping
- ctypes bindings (`python/bindings.py`) exposing the compiled `libmendel.so` to Python with correct types
- Correctness verification: every backward pass is checked against numerical (finite-difference) gradients before being trusted (`tests/test_gradients.py`)

## Not responsible for
- **Model architecture** — what layers exist and how they're wired into a full transformer is `architecture/`'s job; this module only supplies the primitive ops a model gets built from
- **Training curricula, data pipelines, or distillation targets** — that's `distillation/`
- **Running a finished, quantized checkpoint on target hardware** — that's `inference/`. Once a model is trained, hand-tuned hardware-specific kernels (SIMD, CUDA) belong there, not here
- **GPU support** — this engine is deliberately CPU-only for now (see Phase 1 scope decision); a CUDA backend is a real, separate future addition, not assumed by this module's current design

## A real bug worth reading, not just knowing about

Early in building this, `test_gradients.py` failed with wildly wrong gradients. The actual bug: `Tensor.__del__` originally freed the C-side buffer automatically whenever Python's refcounting dropped a `Tensor` to zero references. An expression like `forward().ptr[0]` drops the temporary `Tensor`'s refcount to zero the instant `.ptr` is fetched — *before* the `[0]` index runs — so the buffer was freed, then read through a dangling pointer, silently returning garbage instead of erroring.

The fix: `Tensor` no longer frees anything automatically. Call `.free()` explicitly when you're done with a tensor. This engine leaks memory by default in exchange for never silently reading freed memory — a deliberate tradeoff for a Phase 1 correctness-first engine, revisit once memory pressure actually matters (see `docs/decisions/`).

## Files

```
engine/
├── csrc/
│   ├── tensor_ops.h      # the C API surface
│   └── tensor_ops.c      # every forward + backward implementation
├── Makefile              # builds libmendel.so
├── python/
│   ├── bindings.py       # ctypes signatures — no logic, just types
│   └── core.py           # Tensor, autograd graph, ops, SGD optimizer
├── tests/
│   └── test_gradients.py # numerical gradient check — run this before trusting anything
└── examples/
    ├── tiny_corpus.txt
    └── train_char_mlp.py # proof the engine trains a real (tiny) model
```

## Running it

```bash
make                                  # builds libmendel.so
python3 tests/test_gradients.py       # verify correctness first
python3 examples/train_char_mlp.py    # then prove it actually learns
```

## What's next

This engine currently supports enough ops for an embedding + MLP language model — no attention yet. Adding a self-attention op (and its backward) is the next real piece of Phase 1, living in this module's `csrc/` and wired into `architecture/attention/` once it exists there. GPU support (a CUDA kernel backend behind the same C API) is a natural follow-up once CPU correctness and the fuller architecture are both solid.
