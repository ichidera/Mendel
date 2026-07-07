# Openness

**Status:** draft
**Owner module(s):** cross-cutting — `distillation/`, `LICENSE`, project governance
**Related eval:** _none yet — see eval/README.md_
**Last updated:** _initial draft_

## Requirement

Mendel must remain genuinely open — runnable, modifiable, fine-tunable, and redistributable by anyone — which constrains not just the license on this repo, but every dependency and training input that goes into producing a checkpoint.

## Acceptance criteria

- The project license (see `LICENSE`) is permissive and applied consistently — no component silently depends on something more restrictive
- Any teacher model, dataset, or tool used as a training signal in `distillation/` has its licensing terms documented and checked for compatibility with open redistribution, per `distillation/README.md`'s provenance note
- Reproducibility: someone outside the project should be able to follow the documented pipeline (architecture → distillation → quantization) and arrive at a comparable result, not rely on undocumented internal steps
- No required dependency on a closed, paid, or access-restricted service for core training or inference — optional integrations are fine, hard requirements are not

## Out of scope

- Governance/decision-making openness — that's covered by `GOVERNANCE.md` directly, not this file
- Community process openness (how contributions are reviewed, etc.) — that's `CONTRIBUTING.md`

## Open questions

- Final license choice (Apache 2.0 vs. MIT) — flagged as open in `README.md`/`FAQ.md` already; needs to be resolved before a public release, since it affects what downstream openness guarantees this file can actually make.
- If distillation ends up depending on outputs from a model with usage restrictions, how does that get resolved without compromising this requirement?
