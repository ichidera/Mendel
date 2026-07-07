"""
The single most important test in this repo for a hand-rolled autograd
engine: does analytic backward() actually match the true gradient?

We build a small MLP (matmul -> add_bias -> relu -> matmul -> add_bias ->
softmax_cross_entropy), run backward(), then perturb every parameter by a
tiny epsilon and re-run the forward pass to get the numerical gradient.
If these disagree by more than a small tolerance, the C backward math is
wrong — no amount of successful training afterward would be trustworthy.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "python"))

import random
import core


def build_mlp(seed=0):
    random.seed(seed)
    m, in_dim, hidden, out_dim = 4, 5, 6, 3
    X = core.Tensor((m, in_dim))
    X.set([random.gauss(0, 1) for _ in range(X.n)])
    labels = [random.randrange(out_dim) for _ in range(m)]

    W1 = core.param((in_dim, hidden), fan_in=in_dim)
    b1 = core.zeros((hidden,))
    W2 = core.param((hidden, out_dim), fan_in=hidden)
    b2 = core.zeros((out_dim,))

    params = [W1, b1, W2, b2]

    def forward():
        h = core.relu(core.add_bias(core.matmul(X, W1), b1))
        logits = core.add_bias(core.matmul(h, W2), b2)
        loss = core.softmax_cross_entropy(logits, labels)
        return loss

    return forward, params


def numerical_gradient(forward, param, eps=1e-3):
    grads = []
    for i in range(param.n):
        orig = param.ptr[i]

        param.ptr[i] = orig + eps
        loss_plus = forward().ptr[0]

        param.ptr[i] = orig - eps
        loss_minus = forward().ptr[0]

        param.ptr[i] = orig  # restore
        grads.append((loss_plus - loss_minus) / (2 * eps))
    return grads


def test_gradients(tol=2e-2):
    forward, params = build_mlp()

    for p in params:
        p.zero_grad()
    loss = forward()
    loss.backward()

    max_abs_err = 0.0
    max_rel_err = 0.0
    for name, p in zip(["W1", "b1", "W2", "b2"], params):
        analytic = p.grad_list()
        numeric = numerical_gradient(forward, p)
        for a, n in zip(analytic, numeric):
            abs_err = abs(a - n)
            rel_err = abs_err / (abs(n) + 1e-8)
            max_abs_err = max(max_abs_err, abs_err)
            max_rel_err = max(max_rel_err, rel_err)
        print(f"{name}: max |analytic-numeric| = {max(abs(a - n) for a, n in zip(analytic, numeric)):.6f}")

    print(f"\nOverall max abs error: {max_abs_err:.6f}")
    print(f"Overall max rel error: {max_rel_err:.6f}")
    assert max_abs_err < tol, "Gradient check FAILED — backward math does not match forward math."
    print("\nPASS — analytic gradients match numerical gradients.")


if __name__ == "__main__":
    test_gradients()
