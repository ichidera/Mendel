# architecture/moe/

Implements Mixture-of-Experts: a way to store far more specialized capability than we can afford to run per token, by routing each token to only a small subset of "expert" sub-networks.

## Responsible for
- The router: the small network that decides which expert(s) handle a given token
- Expert modules themselves (the sub-networks the router picks between)
- Load-balancing logic so experts get used roughly evenly during training, rather than the router collapsing onto a handful of favorites
- Sparse activation bookkeeping — making sure only the selected experts actually run, so the compute savings are real, not just nominal

## Not responsible for
- Attention — that's `attention/`, even though both live inside a transformer block
- Deciding *how many* experts to have or how large each one is — that's an architecture-level config decision made in `architecture/README.md`'s config schema, this directory implements whatever the config specifies

## Why this is a core lever for Mendel
MoE is one of the more direct answers to "light as Gemma, capable as a much bigger model": total stored parameters can be large (lots of specialized knowledge), while active parameters per token stay small (low compute/memory cost per inference step). The whole value of this directory is keeping "total capacity" and "per-token cost" as separate, independently tunable numbers.

## Correctness matters more than cleverness here
A router bug that silently sends every token to the same expert quietly turns Mendel back into a much smaller dense model, without any obvious error. Any change to routing logic should ship with a load-balance check in `eval/` — expert utilization should be visible and monitored, not assumed.
