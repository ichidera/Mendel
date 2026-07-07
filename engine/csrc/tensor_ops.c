#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "tensor_ops.h"

float* mendel_alloc(int n) {
    return (float*)calloc((size_t)n, sizeof(float));
}

void mendel_free(float* p) {
    free(p);
}

void matmul_forward(const float* A, const float* B, float* out, int m, int k, int n) {
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            float acc = 0.0f;
            for (int p = 0; p < k; p++) {
                acc += A[i * k + p] * B[p * n + j];
            }
            out[i * n + j] = acc;
        }
    }
}

void matmul_backward(const float* A, const float* B, const float* dOut,
                      float* dA, float* dB, int m, int k, int n) {
    /* dA(m,k) += dOut(m,n) @ B^T(n,k) */
    for (int i = 0; i < m; i++) {
        for (int p = 0; p < k; p++) {
            float acc = 0.0f;
            for (int j = 0; j < n; j++) {
                acc += dOut[i * n + j] * B[p * n + j];
            }
            dA[i * k + p] += acc;
        }
    }
    /* dB(k,n) += A^T(k,m) @ dOut(m,n) */
    for (int p = 0; p < k; p++) {
        for (int j = 0; j < n; j++) {
            float acc = 0.0f;
            for (int i = 0; i < m; i++) {
                acc += A[i * k + p] * dOut[i * n + j];
            }
            dB[p * n + j] += acc;
        }
    }
}

void add_bias_forward(const float* X, const float* b, float* out, int m, int n) {
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            out[i * n + j] = X[i * n + j] + b[j];
        }
    }
}

void add_bias_backward(const float* dOut, float* dX, float* db, int m, int n) {
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            dX[i * n + j] += dOut[i * n + j];
            db[j] += dOut[i * n + j];
        }
    }
}

void relu_forward(const float* X, float* out, int n) {
    for (int i = 0; i < n; i++) {
        out[i] = X[i] > 0.0f ? X[i] : 0.0f;
    }
}

void relu_backward(const float* X, const float* dOut, float* dX, int n) {
    for (int i = 0; i < n; i++) {
        dX[i] += (X[i] > 0.0f ? dOut[i] : 0.0f);
    }
}

void softmax_cross_entropy_forward(const float* logits, const int* labels,
                                    float* loss_per_row, float* probs, int m, int n) {
    for (int i = 0; i < m; i++) {
        const float* row = logits + i * n;
        float maxv = row[0];
        for (int j = 1; j < n; j++) if (row[j] > maxv) maxv = row[j];
        float sum = 0.0f;
        for (int j = 0; j < n; j++) {
            float e = expf(row[j] - maxv);
            probs[i * n + j] = e;
            sum += e;
        }
        for (int j = 0; j < n; j++) probs[i * n + j] /= sum;
        int label = labels[i];
        float p = probs[i * n + label];
        /* guard against log(0) from float underflow */
        if (p < 1e-12f) p = 1e-12f;
        loss_per_row[i] = -logf(p);
    }
}

void softmax_cross_entropy_backward(const float* probs, const int* labels,
                                     float* dLogits, int m, int n) {
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            float target = (j == labels[i]) ? 1.0f : 0.0f;
            dLogits[i * n + j] = (probs[i * n + j] - target) / (float)m;
        }
    }
}

void embedding_forward(const float* table, const int* idx, float* out,
                        int batch, int vocab, int dim) {
    (void)vocab; /* not needed for the lookup itself, kept for API symmetry */
    for (int i = 0; i < batch; i++) {
        const float* row = table + idx[i] * dim;
        memcpy(out + i * dim, row, sizeof(float) * (size_t)dim);
    }
}

void embedding_backward(float* dTable, const int* idx, const float* dOut,
                         int batch, int dim) {
    for (int i = 0; i < batch; i++) {
        float* row = dTable + idx[i] * dim;
        const float* g = dOut + i * dim;
        for (int j = 0; j < dim; j++) row[j] += g[j];
    }
}

void sgd_step(float* param, const float* grad, float lr, int n) {
    for (int i = 0; i < n; i++) {
        param[i] -= lr * grad[i];
    }
}
