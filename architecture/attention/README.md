# architecture/attention/

Implements the attention mechanism(s) Mendel uses to let tokens look at each other. This directory answers exactly one question: *for a given token, which other tokens does it attend to, and how expensively?*

## Responsible for
- Attention variant implementations (e.g. full global attention, sliding-window local attention, hybrid local/global schemes)
- KV-cache handling strategy for whichever variant is active
- Positional encoding schemes as they interact with attention (RoPE and variants)

## Not responsible for
- Expert routing — a mixture-of-experts decision about *which sub-network* processes a token is `moe/`'s job, not this directory's
- The overall block structure (attention + FFN + norm ordering) — that composition lives in `architecture/README.md`'s top-level model definition, this directory only supplies the attention piece

## Why this matters for a lightweight model
Attention is one of the most expensive parts of a transformer to run at long context, and one of the highest-leverage places to trade a small accuracy cost for a large efficiency win. This is exactly the kind of hybrid design other efficient model families use — interleaving cheap local (sliding-window) attention with occasional full global attention, so the model gets long-range awareness without paying full quadratic cost at every layer.

## Adding a new variant
Each attention variant gets its own file, implementing a shared interface (see the interface definition in this directory once the first variant lands). Include, in this README, a short note on the tradeoff: what compute/memory it saves, and what capability it costs, ideally with a pointer to the corresponding `eval/` benchmark once one exists.
