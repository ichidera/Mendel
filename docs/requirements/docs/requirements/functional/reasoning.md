# Reasoning

**Status:** draft
**Owner module(s):** `architecture/`, `distillation/`
**Related eval:** _none yet — see eval/README.md_
**Last updated:** _initial draft_

## Requirement

Mendel must be able to work through a problem in explicit intermediate steps rather than jumping directly from prompt to answer — reasoning that visibly builds toward a conclusion, and that a reader (or the agent loop itself) can inspect and check partway through.

## Acceptance criteria

- Given a multi-step logic, math, or inference problem, Mendel produces intermediate reasoning steps before a final answer, not just the answer
- Reasoning steps are individually checkable — each step should follow from the previous one, such that an error can be localized to a specific step rather than only showing up in a wrong final answer
- Reasoning quality degrades gracefully under quantization and MoE routing changes — a regression here should be visible in `eval/` before it ships, per `non-functional/reliability.md`
- Reasoning performance is measured against problems the model wasn't directly trained on, not just training-distribution problems

## Out of scope

- Multi-step *task* execution across tools/environment (that's `functional/planning.md` and `functional/agentic-loop.md` — reasoning here means internal problem-solving, not acting in the world)
- Any claim about matching a specific frontier model's reasoning benchmark scores — the target is measured capability-per-parameter, not leaderboard parity (see `VISION.md`)

## Open questions

- What's the right benchmark suite — do we adopt existing public reasoning benchmarks, build Mendel-specific ones, or both?
- How much of "reasoning ability" should be distilled directly (teacher traces) vs. emerge from base training + RLHF-style refinement?
