"""
Phase 1 baseline, first real slice: a character-level MLP language model
(Bengio-style: N previous characters -> embeddings -> hidden layer -> next
character), trained with the hand-written C engine, no PyTorch/NumPy/JAX
anywhere in the loop. This is deliberately NOT a transformer yet -- attention
is a follow-up PR. The point of this script is proving the engine trains a
real model end to end, on real (if tiny) data.
"""
import sys
import os
import random

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "python"))
import core  # noqa: E402

CONTEXT_SIZE = 3
EMBED_DIM = 8
HIDDEN = 32
EPOCHS = 400
LR = 0.15
SEED = 0


def load_corpus():
    path = os.path.join(os.path.dirname(__file__), "tiny_corpus.txt")
    with open(path) as f:
        return f.read().strip().replace("\n", " ")


def build_dataset(corpus, stoi):
    pad = stoi["."]
    X, Y = [], []
    context = [pad] * CONTEXT_SIZE
    for ch in corpus:
        ix = stoi[ch]
        X.append(list(context))
        Y.append(ix)
        context = context[1:] + [ix]
    return X, Y


def forward_batch(table, W1, b1, W2, b2, X_idx, embed_dim, context_size):
    embs = []
    for pos in range(context_size):
        idx_list = [row[pos] for row in X_idx]
        embs.append(core.embedding(table, idx_list, embed_dim))
    concat_emb = core.concat_last_dim(embs)
    hidden = core.relu(core.add_bias(core.matmul(concat_emb, W1), b1))
    logits = core.add_bias(core.matmul(hidden, W2), b2)
    return logits


def generate(table, W1, b1, W2, b2, stoi, itos, vocab_size, length=60, seed=1):
    rng = random.Random(seed)
    pad = stoi["."]
    context = [pad] * CONTEXT_SIZE
    out_chars = []
    for _ in range(length):
        logits = forward_batch(table, W1, b1, W2, b2, [context], EMBED_DIM, CONTEXT_SIZE)
        probs = core.softmax_probs(logits)
        # weighted sample over the vocab-sized probability row
        r = rng.random()
        cum = 0.0
        pick = vocab_size - 1
        for i, p in enumerate(probs):
            cum += p
            if r <= cum:
                pick = i
                break
        out_chars.append(itos[pick])
        context = context[1:] + [pick]
    return "".join(out_chars)


def main():
    random.seed(SEED)
    corpus = load_corpus()
    chars = sorted(set(corpus))
    vocab = ["."] + chars  # "." is the start/pad token
    stoi = {ch: i for i, ch in enumerate(vocab)}
    itos = {i: ch for ch, i in stoi.items()}
    vocab_size = len(vocab)

    X_idx, Y_idx = build_dataset(corpus, stoi)
    print(f"corpus length: {len(corpus)} chars, vocab size: {vocab_size}, "
          f"training pairs: {len(X_idx)}")

    table = core.param((vocab_size, EMBED_DIM), fan_in=EMBED_DIM)
    W1 = core.param((CONTEXT_SIZE * EMBED_DIM, HIDDEN), fan_in=CONTEXT_SIZE * EMBED_DIM)
    b1 = core.zeros((HIDDEN,))
    W2 = core.param((HIDDEN, vocab_size), fan_in=HIDDEN)
    b2 = core.zeros((vocab_size,))
    params = [table, W1, b1, W2, b2]
    opt = core.SGD(params, lr=LR)

    print("\nbefore training, sampled generation (should look like noise):")
    print(" ", repr(generate(table, W1, b1, W2, b2, stoi, itos, vocab_size)))

    print("\ntraining:")
    for epoch in range(1, EPOCHS + 1):
        opt.zero_grad()
        logits = forward_batch(table, W1, b1, W2, b2, X_idx, EMBED_DIM, CONTEXT_SIZE)
        loss = core.softmax_cross_entropy(logits, Y_idx)
        loss.backward()
        opt.step()
        if epoch == 1 or epoch % 50 == 0:
            print(f"  epoch {epoch:4d}  loss {loss.ptr[0]:.4f}")

    print("\nafter training, sampled generation (should resemble the corpus):")
    print(" ", repr(generate(table, W1, b1, W2, b2, stoi, itos, vocab_size)))


if __name__ == "__main__":
    main()
