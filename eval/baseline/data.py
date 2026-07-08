"""
Loads corpus.txt, builds a character vocabulary, and splits by *line* rather
than by individual character position. Splitting by line means a val line
is a genuinely unseen sequence during training, not just a few characters
sliced out of the middle of a training sequence the model already saw most
of. That's a meaningfully more honest generalization check than a naive
random split over (context, target) pairs would give.
"""
import os
import random


def load_lines():
    path = os.path.join(os.path.dirname(__file__), "corpus.txt")
    with open(path, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def build_vocab(lines):
    chars = sorted(set("".join(lines)))
    vocab = ["."] + chars  # "." is start/pad AND end-of-line target
    stoi = {c: i for i, c in enumerate(vocab)}
    itos = {i: c for c, i in stoi.items()}
    return vocab, stoi, itos


def split_lines(lines, val_fraction, seed):
    rng = random.Random(seed)
    shuffled = list(lines)
    rng.shuffle(shuffled)
    n_val = max(1, int(len(shuffled) * val_fraction))
    return shuffled[n_val:], shuffled[:n_val]  # train, val


def build_pairs(lines, stoi, context_size):
    """Also teaches an explicit end-of-line signal: after the last real
    character, the next 'target' is the pad token, so the model learns
    where sequences end, not just what comes next mid-sequence."""
    pad = stoi["."]
    X, Y = [], []
    for line in lines:
        context = [pad] * context_size
        for ch in line:
            ix = stoi[ch]
            X.append(list(context))
            Y.append(ix)
            context = context[1:] + [ix]
        X.append(list(context))
        Y.append(pad)
    return X, Y
