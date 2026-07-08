"""Single source of truth for the baseline eval's hyperparameters. Kept as
its own file so a future attention-based model can have its own config
without touching this one, and so a diff in this file is immediately visible
as "the eval conditions changed" rather than buried inside run.py."""


class BaselineConfig:
    def __init__(self):
        self.context_size = 3
        self.embed_dim = 16
        self.hidden = 64
        self.epochs = 600
        self.lr = 0.1
        self.seed = 0
        self.val_fraction = 0.2
        self.eval_every = 50  # epochs between validation loss checks

    def as_dict(self):
        return dict(self.__dict__)
