"""
Baseline model definition: N previous characters -> embeddings -> concat ->
hidden layer (ReLU) -> output logits over the vocabulary. Bengio-style char
MLP, deliberately no attention yet -- see architecture/attention/README.md
for that follow-up. This file owns exactly what architecture/README.md
promises: model shape and the forward pass, wired from engine/ primitives.
Nothing here trains, evaluates, or loads data -- see eval/baseline/ for that.
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "engine", "python"))
import core  # noqa: E402


class CharMLPConfig:
    def __init__(self, vocab_size, context_size=3, embed_dim=8, hidden=32):
        self.vocab_size = vocab_size
        self.context_size = context_size
        self.embed_dim = embed_dim
        self.hidden = hidden


class CharMLP:
    """Holds parameters and exposes a forward pass. No training logic here."""

    def __init__(self, config: CharMLPConfig):
        self.config = config
        c = config
        self.table = core.param((c.vocab_size, c.embed_dim), fan_in=c.embed_dim)
        self.W1 = core.param((c.context_size * c.embed_dim, c.hidden),
                              fan_in=c.context_size * c.embed_dim)
        self.b1 = core.zeros((c.hidden,))
        self.W2 = core.param((c.hidden, c.vocab_size), fan_in=c.hidden)
        self.b2 = core.zeros((c.vocab_size,))

    def parameters(self):
        return [self.table, self.W1, self.b1, self.W2, self.b2]

    def forward(self, context_batch):
        """context_batch: list of [c1, c2, ..., c_context_size] index lists.
        Returns a logits Tensor of shape (batch, vocab_size)."""
        c = self.config
        embs = []
        for pos in range(c.context_size):
            idx_list = [row[pos] for row in context_batch]
            embs.append(core.embedding(self.table, idx_list, c.embed_dim))
        concat_emb = core.concat_last_dim(embs)
        hidden = core.relu(core.add_bias(core.matmul(concat_emb, self.W1), self.b1))
        logits = core.add_bias(core.matmul(hidden, self.W2), self.b2)
        return logits
