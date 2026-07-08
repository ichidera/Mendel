"""
Gradient check for the attention primitives added in this pass: batched
matmul (both transpose_b=0 and transpose_b=1), standalone softmax, and the
full self_attention composite end to end. Same principle as
test_gradients.py: analytic backward() must match numerical finite-difference
gradients, or the C math is wrong regardless of how plausible training looks.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "python"))

import random
import math
import mendel_core as core


def numerical_gradient(forward, tensor, eps=1e-3):
    grads = []
    for i in range(tensor.n):
        orig = tensor.ptr[i]
        tensor.ptr[i] = orig + eps
        loss_plus = forward().ptr[0]
        tensor.ptr[i] = orig - eps
        loss_minus = forward().ptr[0]
        tensor.ptr[i] = orig
        grads.append((loss_plus - loss_minus) / (2 * eps))
    return grads


def check(name, forward, tensors_by_name, tol=2e-2):
    for t in tensors_by_name.values():
        t.zero_grad()
    loss = forward()
    loss.backward()

    max_abs_err = 0.0
    ok = True
    for tname, t in tensors_by_name.items():
        analytic = t.grad_list()
        numeric = numerical_gradient(forward, t)
        err = max(abs(a - n) for a, n in zip(analytic, numeric))
        max_abs_err = max(max_abs_err, err)
        print(f"  {tname}: max |analytic-numeric| = {err:.6f}")
        if err >= tol:
            ok = False

    status = "PASS" if ok else "FAIL"
    print(f"[{name}] {status} (overall max abs error: {max_abs_err:.6f})\n")
    return ok


def test_batched_matmul_no_transpose():
    random.seed(1)
    batch, m, k, n = 2, 3, 4, 5
    A = core.Tensor((batch * m, k))
    A.set([random.gauss(0, 1) for _ in range(A.n)])
    B = core.Tensor((batch * k, n))
    B.set([random.gauss(0, 1) for _ in range(B.n)])
    target = core.Tensor((batch * m, n))
    target.set([random.gauss(0, 1) for _ in range(target.n)])

    def forward():
        out = core.batched_matmul(A, B, batch, m, k, n, transpose_b=0)
        diff_sq = 0.0
        loss = core.Tensor((1,))
        vals = [(out.ptr[i] - target.ptr[i]) ** 2 for i in range(out.n)]
        loss.ptr[0] = sum(vals) / len(vals)
        loss._prev = (out,)

        def _backward():
            m_ = out.n
            for i in range(m_):
                out.grad[i] += 2.0 * (out.ptr[i] - target.ptr[i]) / m_

        loss._backward = _backward
        return loss

    return check("batched_matmul (transpose_b=0)", forward, {"A": A, "B": B})


def test_batched_matmul_transpose():
    random.seed(2)
    batch, m, k, n = 2, 3, 4, 5
    A = core.Tensor((batch * m, k))
    A.set([random.gauss(0, 1) for _ in range(A.n)])
    B = core.Tensor((batch * n, k))  # transpose_b=1 -> B stored as (n,k) per batch
    B.set([random.gauss(0, 1) for _ in range(B.n)])
    target = core.Tensor((batch * m, n))
    target.set([random.gauss(0, 1) for _ in range(target.n)])

    def forward():
        out = core.batched_matmul(A, B, batch, m, k, n, transpose_b=1)
        loss = core.Tensor((1,))
        vals = [(out.ptr[i] - target.ptr[i]) ** 2 for i in range(out.n)]
        loss.ptr[0] = sum(vals) / len(vals)
        loss._prev = (out,)

        def _backward():
            m_ = out.n
            for i in range(m_):
                out.grad[i] += 2.0 * (out.ptr[i] - target.ptr[i]) / m_

        loss._backward = _backward
        return loss

    return check("batched_matmul (transpose_b=1)", forward, {"A": A, "B": B})


def test_softmax():
    random.seed(3)
    m, n = 4, 5
    X = core.Tensor((m, n))
    X.set([random.gauss(0, 1) for _ in range(X.n)])
    target = core.Tensor((m, n))
    target.set([random.gauss(0, 1) for _ in range(target.n)])

    def forward():
        probs = core.softmax(X)
        loss = core.Tensor((1,))
        vals = [(probs.ptr[i] - target.ptr[i]) ** 2 for i in range(probs.n)]
        loss.ptr[0] = sum(vals) / len(vals)
        loss._prev = (probs,)

        def _backward():
            m_ = probs.n
            for i in range(m_):
                probs.grad[i] += 2.0 * (probs.ptr[i] - target.ptr[i]) / m_

        loss._backward = _backward
        return loss

    return check("softmax (standalone)", forward, {"X": X})


def test_self_attention_end_to_end():
    random.seed(4)
    batch, seq_len, d_model, vocab = 3, 3, 4, 6
    X = core.Tensor((batch * seq_len, d_model))
    X.set([random.gauss(0, 1) for _ in range(X.n)])
    Wq = core.param((d_model, d_model), fan_in=d_model)
    Wk = core.param((d_model, d_model), fan_in=d_model)
    Wv = core.param((d_model, d_model), fan_in=d_model)
    Wout = core.param((seq_len * d_model, vocab), fan_in=seq_len * d_model)
    bout = core.zeros((vocab,))
    labels = [random.randrange(vocab) for _ in range(batch)]

    def forward():
        attended = core.self_attention(X, Wq, Wk, Wv, batch, seq_len, d_model)
        # pool: concat all positions per example back into one vector, like
        # the CharAttn model will -- attended is already (batch*seq_len, d_model)
        # in batch-major row order, so we just need to view it per example.
        pooled = core.Tensor((batch, seq_len * d_model))
        for b in range(batch):
            for pos in range(seq_len):
                for d in range(d_model):
                    pooled.ptr[b * seq_len * d_model + pos * d_model + d] = \
                        attended.ptr[(b * seq_len + pos) * d_model + d]
        pooled._prev = (attended,)

        def _pooled_backward():
            for b in range(batch):
                for pos in range(seq_len):
                    for d in range(d_model):
                        attended.grad[(b * seq_len + pos) * d_model + d] += \
                            pooled.grad[b * seq_len * d_model + pos * d_model + d]

        pooled._backward = _pooled_backward

        logits = core.add_bias(core.matmul(pooled, Wout), bout)
        loss = core.softmax_cross_entropy(logits, labels)
        return loss

    return check("self_attention (end-to-end through cross-entropy)", forward,
                 {"Wq": Wq, "Wk": Wk, "Wv": Wv, "Wout": Wout, "bout": bout})


if __name__ == "__main__":
    results = [
        test_batched_matmul_no_transpose(),
        test_batched_matmul_transpose(),
        test_softmax(),
        test_self_attention_end_to_end(),
    ]
    if all(results):
        print("ALL PASS")
    else:
        print("SOME TESTS FAILED")
        sys.exit(1)
