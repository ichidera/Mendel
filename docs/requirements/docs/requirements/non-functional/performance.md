# Performance

**Status:** draft
**Owner module(s):** `inference/`
**Related eval:** _none yet — see eval/README.md_
**Last updated:** _initial draft_

## Requirement

Mendel must generate output, and complete agentic action sequences, at a speed usable for real interactive and autonomous work on its target hardware — not just technically capable of running, but fast enough to be genuinely useful.

## Acceptance criteria

- Tokens-per-second targets are defined per device class, distinct from the memory targets in `non-functional/footprint.md`
- Time-to-first-token is tracked separately from steady-state throughput, since agentic loops issuing many short exchanges are sensitive to the former
- Multi-step agentic runs (tool calls, CLI commands, GUI actions) complete in a time budget appropriate to the task — a technically-correct agentic sequence that takes an impractically long time doesn't meet this requirement
- Performance figures are always reported alongside the quantization level and MoE configuration they were measured with, since both directly affect speed

## Out of scope

- Static memory/storage footprint — that's `non-functional/footprint.md`
- Correctness of the output itself — that's the relevant `functional/` file; this file is purely about speed given correct behavior

## Open questions

- What's an acceptable latency budget for a single agentic step (plan → act → observe) before it materially hurts usability, and does that budget differ meaningfully across device classes?
- How much of the low-level optimization work described in `inference/README.md` (hand-tuned kernels, hardware-specific paths) is needed to hit initial targets versus being a later-stage refinement?
