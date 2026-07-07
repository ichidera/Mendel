# quantization/

Shrinks a trained Mendel checkpoint by reducing how many bits represent each weight — the most direct, most "free lunch" lever available, up to a point.

## Responsible for
- Post-training quantization methods (reducing precision after training completes)
- Quantization-aware training hooks, if training-time simulation of low precision improves final results
- Calibration: choosing scale/zero-point parameters per layer (or per group) so reduced-bit weights still represent the trained values as faithfully as possible
- Precision-vs-capability tradeoff reporting: for every supported bit-width, a clear record of what capability was measured before and after

## Not responsible for
- Deciding the *architecture* being quantized — that's `architecture/`'s job, this directory takes a finished checkpoint as input
- Deciding whether a given quantization level is "good enough" to ship — that's a call made against `eval/` results, this directory just makes each precision level available and measured

## The honest failure mode to watch for
Quantization degrades gracefully for a while, then falls off a cliff at some bit-width — small capability loss until a threshold, then a sharp collapse. Every quantization level added here needs an eval run attached to it in `eval/`, not just a "runs without crashing" check. "It loads and generates text" is not the same as "it still plans and uses tools correctly" — the latter is usually what breaks first.

## Interacts with
- `inference/` — the runtime needs to know which bit-width a given checkpoint uses and support execution at that precision
- `moe/` — expert weights may tolerate different quantization levels than the router; don't assume one bit-width fits every component uniformly
