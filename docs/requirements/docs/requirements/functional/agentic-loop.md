# Agentic loop

**Status:** draft
**Owner module(s):** `agent/`
**Related eval:** _none yet — see eval/README.md_
**Last updated:** _initial draft_

## Requirement

Mendel must be able to operate autonomously across many steps toward a goal: acting, observing the result, and correcting course when a step doesn't go as expected, without a human re-prompting it after every action.

## Acceptance criteria

- Given a goal requiring multiple sequential actions, Mendel completes the full sequence without requiring a human to manually chain each step
- Mendel notices when a step failed or produced an unexpected result, distinct from assuming success (see `agent/README.md`'s stated failure mode: "agent loops fail quietly by continuing past a bad step")
- On noticing a failed step, Mendel takes a corrective action rather than repeating the same failed approach or continuing on an invalidated plan
- The loop terminates appropriately — recognizing goal completion, not running indefinitely or stopping prematurely
- Behavior remains stable across long agentic runs (many steps), not just short 2-3 step demonstrations

## Out of scope

- The specific mechanics of *how* a plan gets revised — that's `functional/planning.md`
- Tool-call formatting and MCP mechanics — that's `functional/tool-use.md`
- Shell-specific and GUI-specific execution — those are `functional/cli.md` and `functional/computer-control.md`; this file is about the surrounding loop, not any one action surface

## Open questions

- What's the right way to measure "self-correction" as a distinct capability from raw task success, so a fix here can be evaluated in isolation (per `eval/README.md`'s isolated-vs-end-to-end principle)?
- How long an agentic run should Mendel be expected to sustain reliably at initial target sizes, and how does that scale with model size — is there a clear relationship we should be tracking?
