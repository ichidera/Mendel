"""
Thin ctypes bridge to libmendel.so. This file's only job is to expose the raw
C functions to Python with correct argument/return types. No autograd, no
graph — that's core.py. If you're looking for tensor.backward(), it's not here.
"""
import ctypes
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_LIB_PATH = os.path.join(_HERE, "..", "libmendel.so")

_lib = ctypes.CDLL(_LIB_PATH)

F = ctypes.c_float
FP = ctypes.POINTER(ctypes.c_float)
IP = ctypes.POINTER(ctypes.c_int)

_lib.mendel_alloc.argtypes = [ctypes.c_int]
_lib.mendel_alloc.restype = FP

_lib.mendel_free.argtypes = [FP]
_lib.mendel_free.restype = None

_lib.matmul_forward.argtypes = [FP, FP, FP, ctypes.c_int, ctypes.c_int, ctypes.c_int]
_lib.matmul_forward.restype = None

_lib.matmul_backward.argtypes = [FP, FP, FP, FP, FP, ctypes.c_int, ctypes.c_int, ctypes.c_int]
_lib.matmul_backward.restype = None

_lib.add_bias_forward.argtypes = [FP, FP, FP, ctypes.c_int, ctypes.c_int]
_lib.add_bias_forward.restype = None

_lib.add_bias_backward.argtypes = [FP, FP, FP, ctypes.c_int, ctypes.c_int]
_lib.add_bias_backward.restype = None

_lib.relu_forward.argtypes = [FP, FP, ctypes.c_int]
_lib.relu_forward.restype = None

_lib.relu_backward.argtypes = [FP, FP, FP, ctypes.c_int]
_lib.relu_backward.restype = None

_lib.softmax_cross_entropy_forward.argtypes = [FP, IP, FP, FP, ctypes.c_int, ctypes.c_int]
_lib.softmax_cross_entropy_forward.restype = None

_lib.softmax_cross_entropy_backward.argtypes = [FP, IP, FP, ctypes.c_int, ctypes.c_int]
_lib.softmax_cross_entropy_backward.restype = None

_lib.embedding_forward.argtypes = [FP, IP, FP, ctypes.c_int, ctypes.c_int, ctypes.c_int]
_lib.embedding_forward.restype = None

_lib.embedding_backward.argtypes = [FP, IP, FP, ctypes.c_int, ctypes.c_int]
_lib.embedding_backward.restype = None

_lib.sgd_step.argtypes = [FP, FP, ctypes.c_float, ctypes.c_int]
_lib.sgd_step.restype = None

_lib.batched_matmul_forward.argtypes = [FP, FP, FP, ctypes.c_int, ctypes.c_int,
                                          ctypes.c_int, ctypes.c_int, ctypes.c_int]
_lib.batched_matmul_forward.restype = None

_lib.batched_matmul_backward.argtypes = [FP, FP, FP, FP, FP, ctypes.c_int, ctypes.c_int,
                                           ctypes.c_int, ctypes.c_int, ctypes.c_int]
_lib.batched_matmul_backward.restype = None

_lib.softmax_forward.argtypes = [FP, FP, ctypes.c_int, ctypes.c_int]
_lib.softmax_forward.restype = None

_lib.softmax_backward.argtypes = [FP, FP, FP, ctypes.c_int, ctypes.c_int]
_lib.softmax_backward.restype = None


def alloc(n):
    return _lib.mendel_alloc(n)


def free(ptr):
    _lib.mendel_free(ptr)


def matmul_forward(A, B, out, m, k, n):
    _lib.matmul_forward(A, B, out, m, k, n)


def matmul_backward(A, B, dOut, dA, dB, m, k, n):
    _lib.matmul_backward(A, B, dOut, dA, dB, m, k, n)


def add_bias_forward(X, b, out, m, n):
    _lib.add_bias_forward(X, b, out, m, n)


def add_bias_backward(dOut, dX, db, m, n):
    _lib.add_bias_backward(dOut, dX, db, m, n)


def relu_forward(X, out, n):
    _lib.relu_forward(X, out, n)


def relu_backward(X, dOut, dX, n):
    _lib.relu_backward(X, dOut, dX, n)


def softmax_cross_entropy_forward(logits, labels, loss_per_row, probs, m, n):
    _lib.softmax_cross_entropy_forward(logits, labels, loss_per_row, probs, m, n)


def softmax_cross_entropy_backward(probs, labels, dLogits, m, n):
    _lib.softmax_cross_entropy_backward(probs, labels, dLogits, m, n)


def embedding_forward(table, idx, out, batch, vocab, dim):
    _lib.embedding_forward(table, idx, out, batch, vocab, dim)


def embedding_backward(dTable, idx, dOut, batch, dim):
    _lib.embedding_backward(dTable, idx, dOut, batch, dim)


def sgd_step(param, grad, lr, n):
    _lib.sgd_step(param, grad, lr, n)


def batched_matmul_forward(A, B, out, batch, m, k, n, transpose_b):
    _lib.batched_matmul_forward(A, B, out, batch, m, k, n, int(transpose_b))


def batched_matmul_backward(A, B, dOut, dA, dB, batch, m, k, n, transpose_b):
    _lib.batched_matmul_backward(A, B, dOut, dA, dB, batch, m, k, n, int(transpose_b))


def softmax_forward(X, out, m, n):
    _lib.softmax_forward(X, out, m, n)


def softmax_backward(probs, dOut, dIn, m, n):
    _lib.softmax_backward(probs, dOut, dIn, m, n)
