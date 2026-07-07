# Roadmap

This is our current best guess at the path from here to VISION.md, broken into phases. It is not a promise with dates — it's a working plan that will be revised as levers succeed, fail, or turn out to matter less than expected. Each phase links to the modules doing the work; see each module's own README for what "done" means at a component level.

## Phase 0 — Scaffolding (current)
Repository structure, governance, CI/CD, contribution process, module ownership boundaries. No model code yet. The goal of this phase is that a new contributor can read the repo and know exactly where their idea belongs before writing a line of it.

**Owning modules:** `.github/`, root docs, `scripts/`

## Phase 1 — First trainable baseline
A working, small, dense model architecture that trains and runs end to end — deliberately unambitious on capability, the point is a correct, reproducible pipeline from architecture definition through to a checkpoint that `inference/` can execute.

**Owning modules:** `architecture/`, `inference/`, `eval/` (baseline reasoning benchmarks)

## Phase 2 — Distillation pipeline
Stand up the teacher-student training pipeline: collecting or generating strong reasoning/planning traces from capable models, and training the Phase 1 baseline against them. First real test of whether "inherit judgment, not just facts" actually moves the needle at this scale.

**Owning modules:** `distillation/`, `eval/` (reasoning + planning benchmarks)

## Phase 3 — Efficiency levers
Introduce Mixture-of-Experts routing and quantization, measuring capability-per-parameter and capability-per-bit at each step. This phase is where "light as Gemma" starts becoming a real, measured claim rather than an aspiration.

**Owning modules:** `architecture/moe/`, `quantization/`, `eval/` (precision/capability tradeoff tracking)

## Phase 4 — Retrieval
Offload factual knowledge out of the weights and into an external index, freeing parameter budget for reasoning and procedure rather than memorization.

**Owning modules:** `retrieval/`, `eval/`

## Phase 5 — Agentic loop and tool use
Build the planning/acting/observing loop, MCP and general tool-calling support, and skill-loading — the point where Mendel stops being a model that answers and becomes one that acts.

**Owning modules:** `agent/`, `agent/tools/`, `agent/skills/`, `eval/` (agentic task benchmarks)

## Phase 6 — CLI and computer control
Shell operation and GUI control (mouse/keyboard) — the capabilities that let Mendel act on a real computer the way a person would, not just through clean APIs.

**Owning modules:** `agent/cli/`, `control/`, `eval/`

## Phase 7 — Integration and hardening
Everything working together: an agentic, tool-using, self-correcting model running at a genuinely lightweight footprint on real target hardware. This phase is mostly about finding where the pieces built in isolation break when combined, and fixing that.

**Owning modules:** all of the above, plus `docs/` capturing what broke and why

## How this roadmap changes
Phases are sequenced by dependency, not by fixed calendar time, and several can run in parallel once Phase 1 lands (e.g. Phase 3's quantization work doesn't strictly need Phase 2's distillation pipeline to be finished). If a phase's approach turns out to be wrong, that gets written up in `docs/` and this file gets updated — a roadmap that never changes isn't being tested against reality.
