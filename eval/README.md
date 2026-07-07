# eval/

Measures whether Mendel actually has the capabilities this project claims — reasoning, planning, tool-use, agentic operation, CLI competence, GUI control. A capability claim without a benchmark here doesn't count.

## Responsible for
- Benchmark suites for each target capability listed in the top-level README/MISSION: thinking, planning, tool-use/MCP, skills, agentic multi-step tasks, CLI operation, mouse/keyboard control
- Regression tracking: catching when a change elsewhere in the repo (a new quantization level, a routing change, a new attention variant) *quietly* degrades a capability
- Precision/capability tradeoff reports referenced by `quantization/` and `architecture/moe/`
- Isolated component evals (e.g. tool-call formatting correctness, retrieval accuracy) as well as end-to-end task evals

## Not responsible for
- Fixing whatever a failing eval reveals — that's the relevant lever's directory (a bad reasoning eval points back to `distillation/`, a bad tool-use eval points back to `agent/tools/`)
- Model architecture or training — this directory only measures, it doesn't build

## Why isolated and end-to-end evals both matter
An end-to-end task failure could stem from a bad plan, a bad tool call, a bad shell command interpretation, or a bad final answer — and it looks the same from outside. Every capability area should have both: a component-level eval that isolates *that* piece specifically, and an end-to-end eval that tests it in context. Without the isolated version, every failure gets misattributed to "the model isn't smart enough" when the actual bug might be one directory over.

## A living contract
If a new capability is claimed anywhere in this repo's docs, an eval for it belongs here before that claim ships. This directory is what keeps MISSION.md honest.
