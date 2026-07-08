"""
Mendel's autograd engine. This file tracks the computation graph and decides
*when* to call into C — it contains no numerical math itself. Every actual
number gets touched only inside bindings.py -> libmendel.so. That boundary is
deliberate: if you're doing arithmetic in this file, it probably belongs in
tensor_ops.c instead.
"""
import ctypes
import math
import random

import bindings

# Every Tensor registers itself here on creation. Since __del__ deliberately
# does nothing (see the note in Tensor.free below), this registry is how we
# reclaim memory at natural step boundaries instead: call free_all_except()
# once per training step with the tensors you need to keep (model
# parameters), and everything else created since the last sweep gets freed.
# See docs/decisions/0005-attention-eval-and-memory-lifecycle.md for why
# this was necessary, not optional, once training ran longer than a few
# hundred steps.
_ALL_TENSORS = []


def free_all_except(keep_tensors):
    """Free every Tensor created since the last sweep, except those in
    keep_tensors. Call this once per training step, after you've extracted
    any scalar values you need (e.g. loss.ptr[0]) into plain Python floats --
    anything still referencing a freed Tensor's buffer after this call will
    read garbage, same hazard as the __del__ bug this design avoids."""
    global _ALL_TENSORS
    keep_ids = {id(t) for t in keep_tensors}
    remaining = []
    for t in _ALL_TENSORS:
        if id(t) in keep_ids:
            remaining.append(t)
        else:
            t.free()
    _ALL_TENSORS = remaining


class Tensor:
    """A buffer of floats backed by C-allocated memory, plus enough graph
    bookkeeping (parents + a backward closure) to support .backward()."""

    def __init__(self, shape, fill=None):
        self.shape = tuple(shape)
        self.n = 1
        for d in self.shape:
            self.n *= d
        self.ptr = bindings.alloc(self.n)
        self.grad = bindings.alloc(self.n)
        if fill is not None:
            self.set(fill)
        self._prev = ()
        self._backward = lambda: None
        _ALL_TENSORS.append(self)

    def set(self, values):
        assert len(values) == self.n, f"expected {self.n} values, got {len(values)}"
        for i, v in enumerate(values):
            self.ptr[i] = v

    def tolist(self):
        return [self.ptr[i] for i in range(self.n)]

    def grad_list(self):
        return [self.grad[i] for i in range(self.n)]

    def zero_grad(self):
        ctypes.memset(ctypes.cast(self.grad, ctypes.c_void_p), 0, self.n * 4)

    def free(self):
        """Explicitly release the C-side buffers. Not called automatically.

        We deliberately do NOT free memory in __del__. CPython's refcounting
        is immediate, not deferred -- an expression like forward().ptr[0]
        drops the temporary Tensor's refcount to zero the instant .ptr is
        fetched, before the [0] index runs. An automatic __del__ there
        would free the buffer and then read through a dangling pointer,
        silently returning garbage instead of raising an error. We'd rather
        leak memory in this Phase 1 engine than fail silently and wrong.
        Call .free() explicitly once done with a tensor, or don't bother yet
        -- this is a training-loop toy engine, not a production allocator."""
        if getattr(self, "_freed", False):
            return
        bindings.free(self.ptr)
        bindings.free(self.grad)
        self._freed = True

    def backward(self):
        topo, visited = [], set()

        def build(v):
            if id(v) not in visited:
                visited.add(id(v))
                for p in v._prev:
                    build(p)
                topo.append(v)

        build(self)
        for v in reversed(topo):
            v._backward()


def param(shape, fan_in=None):
    """A leaf tensor with He-style random init, for trainable parameters."""
    t = Tensor(shape)
    scale = 1.0 / math.sqrt(fan_in if fan_in else shape[-1])
    t.set([random.gauss(0.0, scale) for _ in range(t.n)])
    return t


def zeros(shape):
    t = Tensor(shape)
    t.set([0.0] * t.n)
    return t


# ---- ops: each builds one node, wiring a C forward call to a C backward call ----

def matmul(A, B):
    m, k = A.shape
    k2, n = B.shape
    assert k == k2, f"matmul shape mismatch: {A.shape} @ {B.shape}"
    out = Tensor((m, n))
    bindings.matmul_forward(A.ptr, B.ptr, out.ptr, m, k, n)
    out._prev = (A, B)

    def _backward():
        bindings.matmul_backward(A.ptr, B.ptr, out.grad, A.grad, B.grad, m, k, n)

    out._backward = _backward
    return out


def add_bias(X, b):
    m, n = X.shape
    out = Tensor((m, n))
    bindings.add_bias_forward(X.ptr, b.ptr, out.ptr, m, n)
    out._prev = (X, b)

    def _backward():
        bindings.add_bias_backward(out.grad, X.grad, b.grad, m, n)

    out._backward = _backward
    return out


def relu(X):
    out = Tensor(X.shape)
    bindings.relu_forward(X.ptr, out.ptr, X.n)
    out._prev = (X,)

    def _backward():
        bindings.relu_backward(X.ptr, out.grad, X.grad, X.n)

    out._backward = _backward
    return out


def embedding(table, idx_list, dim):
    """table: Tensor of shape (vocab, dim). idx_list: python list of ints."""
    vocab = table.shape[0]
    batch = len(idx_list)
    idx_arr = (ctypes.c_int * batch)(*idx_list)
    out = Tensor((batch, dim))
    bindings.embedding_forward(table.ptr, idx_arr, out.ptr, batch, vocab, dim)
    out._prev = (table,)

    def _backward():
        bindings.embedding_backward(table.grad, idx_arr, out.grad, batch, dim)

    out._backward = _backward
    return out


def softmax_cross_entropy(logits, labels):
    """Returns a scalar-shaped Tensor holding the mean loss. Calling
    .backward() on it fills logits.grad directly."""
    m, n = logits.shape
    label_arr = (ctypes.c_int * m)(*labels)
    probs = bindings.alloc(m * n)
    loss_per_row = bindings.alloc(m)
    bindings.softmax_cross_entropy_forward(logits.ptr, label_arr, loss_per_row, probs, m, n)
    loss_val = sum(loss_per_row[i] for i in range(m)) / m
    bindings.free(loss_per_row)

    loss = Tensor((1,))
    loss.ptr[0] = loss_val
    loss._prev = (logits,)

    def _backward():
        bindings.softmax_cross_entropy_backward(probs, label_arr, logits.grad, m, n)
        bindings.free(probs)

    loss._backward = _backward
    return loss


def concat_last_dim(tensors):
    """Concatenate a list of (m, d_i) tensors into one (m, sum(d_i)) tensor.
    Pure bookkeeping, not math -- plain Python loops, no C call needed."""
    m = tensors[0].shape[0]
    dims = [t.shape[1] for t in tensors]
    total = sum(dims)
    out = Tensor((m, total))

    for i in range(m):
        offset = 0
        for t, d in zip(tensors, dims):
            for j in range(d):
                out.ptr[i * total + offset + j] = t.ptr[i * d + j]
            offset += d

    out._prev = tuple(tensors)

    def _backward():
        for i in range(m):
            offset = 0
            for t, d in zip(tensors, dims):
                for j in range(d):
                    t.grad[i * d + j] += out.grad[i * total + offset + j]
                offset += d

    out._backward = _backward
    return out


def softmax_probs(logits):
    """Inference-only softmax (no gradient). Reuses the cross-entropy forward
    kernel with dummy labels purely to get probabilities out of it, rather
    than duplicating a plain-softmax C function for one call site."""
    m, n = logits.shape
    dummy_labels = (ctypes.c_int * m)(*([0] * m))
    loss_per_row = bindings.alloc(m)
    probs = bindings.alloc(m * n)
    bindings.softmax_cross_entropy_forward(logits.ptr, dummy_labels, loss_per_row, probs, m, n)
    result = [probs[i] for i in range(m * n)]
    bindings.free(loss_per_row)
    bindings.free(probs)
    return result


def batched_matmul(A, B, batch, m, k, n, transpose_b):
    """Per-batch matmul: out[b] = A[b] @ (B[b]^T if transpose_b else B[b]).
    A, B are flat Tensors whose buffers are interpreted with explicit batch/
    m/k/n strides -- see tensor_ops.h for the exact layout. Used as the two
    matmuls inside self_attention (Q@K^T and attn_weights@V)."""
    out = Tensor((batch * m, n))
    bindings.batched_matmul_forward(A.ptr, B.ptr, out.ptr, batch, m, k, n, transpose_b)
    out._prev = (A, B)

    def _backward():
        bindings.batched_matmul_backward(A.ptr, B.ptr, out.grad, A.grad, B.grad,
                                          batch, m, k, n, transpose_b)

    out._backward = _backward
    return out


def softmax(X):
    """Row-wise softmax, no labels -- distinct from softmax_cross_entropy,
    which fuses softmax with the loss. Used inside attention for turning
    scores into weights."""
    m, n = X.shape
    out = Tensor((m, n))
    bindings.softmax_forward(X.ptr, out.ptr, m, n)
    out._prev = (X,)

    def _backward():
        bindings.softmax_backward(out.ptr, out.grad, X.grad, m, n)

    out._backward = _backward
    return out


def self_attention(X, Wq, Wk, Wv, batch, seq_len, d_model):
    """Single-head scaled dot-product self-attention, no causal mask.

    Scope note: this attends bidirectionally over a small fixed context
    window that predicts a single next token -- it is NOT yet the causal,
    arbitrary-length self-attention a full autoregressive transformer needs
    (see architecture/attention/README.md). That's real follow-up work; this
    is deliberately the simpler, gradient-checkable first step.

    X: Tensor (batch*seq_len, d_model), rows ordered batch-major (all
       positions of example 0, then example 1, ...) -- the same order
       embedding() + concat_last_dim() already produce.
    Wq, Wk, Wv: Tensor (d_model, d_model) parameters. Single head, so
       d_head == d_model -- no separate head-splitting yet.
    Returns: Tensor (batch*seq_len, d_model), same flat layout as X.
    """
    n = seq_len
    scale = 1.0 / math.sqrt(d_model)

    Q = matmul(X, Wq)
    K = matmul(X, Wk)
    V = matmul(X, Wv)

    scores = Tensor((batch * n, n))
    bindings.batched_matmul_forward(Q.ptr, K.ptr, scores.ptr, batch, n, d_model, n, 1)
    for i in range(scores.n):
        scores.ptr[i] *= scale

    probs = Tensor((batch * n, n))
    bindings.softmax_forward(scores.ptr, probs.ptr, batch * n, n)

    attended = Tensor((batch * n, d_model))
    bindings.batched_matmul_forward(probs.ptr, V.ptr, attended.ptr, batch, n, n, d_model, 0)

    attended._prev = (Q, K, V)

    def _backward():
        d_probs = bindings.alloc(batch * n * n)
        bindings.batched_matmul_backward(probs.ptr, V.ptr, attended.grad,
                                          d_probs, V.grad, batch, n, n, d_model, 0)

        d_scores = bindings.alloc(batch * n * n)
        bindings.softmax_backward(probs.ptr, d_probs, d_scores, batch * n, n)
        bindings.free(d_probs)

        for i in range(batch * n * n):
            d_scores[i] *= scale

        bindings.batched_matmul_backward(Q.ptr, K.ptr, d_scores, Q.grad, K.grad,
                                          batch, n, d_model, n, 1)
        bindings.free(d_scores)

    attended._backward = _backward
    return attended


class SGD:
    def __init__(self, params, lr):
        self.params = list(params)
        self.lr = lr

    def step(self):
        for p in self.params:
            bindings.sgd_step(p.ptr, p.grad, self.lr, p.n)

    def zero_grad(self):
        for p in self.params:
            p.zero_grad()
