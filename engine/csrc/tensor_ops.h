#ifndef MENDEL_TENSOR_OPS_H
#define MENDEL_TENSOR_OPS_H

/* All buffers are raw row-major float arrays. Shape bookkeeping lives on the
 * Python side — this layer is pure math, nothing else. No tensor "object"
 * exists in C on purpose: it's the muscle, not the director. */

float* mendel_alloc(int n);              /* zero-initialized malloc of n floats */
void   mendel_free(float* p);

/* out(m,n) = A(m,k) @ B(k,n) */
void matmul_forward(const float* A, const float* B, float* out, int m, int k, int n);

/* dA(m,k) = dOut(m,n) @ B^T ; dB(k,n) = A^T @ dOut(m,n) — both accumulate (+=) */
void matmul_backward(const float* A, const float* B, const float* dOut,
                      float* dA, float* dB, int m, int k, int n);

/* out(m,n) = X(m,n) + b(n), b broadcast across rows */
void add_bias_forward(const float* X, const float* b, float* out, int m, int n);

/* dX = dOut (identity) ; db(n) = column-sum of dOut — db accumulates (+=) */
void add_bias_backward(const float* dOut, float* dX, float* db, int m, int n);

void relu_forward(const float* X, float* out, int n);
/* dX accumulates (+=) */
void relu_backward(const float* X, const float* dOut, float* dX, int n);

/* probs(m,n) = softmax(logits) row-wise ; loss_per_row(m) = -log(probs[i][labels[i]]) */
void softmax_cross_entropy_forward(const float* logits, const int* labels,
                                    float* loss_per_row, float* probs, int m, int n);

/* dLogits(m,n) = (probs - one_hot(labels)) / m  — mean-reduced gradient */
void softmax_cross_entropy_backward(const float* probs, const int* labels,
                                     float* dLogits, int m, int n);

/* out(batch,dim) = table[idx[i]] for i in 0..batch */
void embedding_forward(const float* table, const int* idx, float* out,
                        int batch, int vocab, int dim);
/* dTable accumulates (+=) at rows given by idx */
void embedding_backward(float* dTable, const int* idx, const float* dOut,
                         int batch, int dim);

/* param(n) -= lr * grad(n), in place */
void sgd_step(float* param, const float* grad, float lr, int n);

#endif
