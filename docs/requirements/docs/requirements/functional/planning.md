# Planning

**Status:** draft
**Owner module(s):** `agent/`, `distillation/`
**Related eval:** _none yet — see eval/README.md_
**Last updated:** _initial draft_

## Requirement

Given a high-level goal, Mendel must be able to decompose it into an ordered sequence of concrete sub-tasks, track progress across them, and adjust the plan when a sub-task doesn't go as expected.

## Acceptance criteria

- Given a multi-step goal, Mendel produces a plan with identifiable, ordered sub-tasks before acting, not just a first action
- Mendel can report (internally or on request) what sub-task it's currently on and what remains
- When a sub-task fails or produces an unexpected result, the plan is revised rather than the agent continuing on a stale plan (this overlaps with `functional/agentic-loop.md`'s self-correction requirement, but planning specifically covers *re-planning*, not just noticing failure)
- Plans hold up across a range of goal complexities — from a 3-step task to something requiring a dozen or more coordinated steps

## Out of scope

- The mechanics of noticing a step failed — that's `functional/agentic-loop.md`
- The specific tools used to execute a plan's steps — that's `functional/tool-use.md`

## Open questions

- Should plans be represented as structured data the agent loop consumes programmatically, or as natural-language reasoning the model re-derives each step? Tradeoff between reliability and flexibility.
- How do we evaluate "planning quality" separately from "execution quality" so a bad outcome can be attributed to the right failure point?
