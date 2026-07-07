# Reliability

**Status:** draft
**Owner module(s):** `eval/`, cross-cutting across all capability modules
**Related eval:** _none yet — see eval/README.md_
**Last updated:** _initial draft_

## Requirement

Mendel's capabilities must degrade predictably and visibly, never silently — a change anywhere in the stack (a new quantization level, a routing change, a new attention variant) that weakens a capability must be caught before it ships, not discovered later as an unexplained regression.

## Acceptance criteria

- Every capability in `functional/` has a corresponding regression-tracked eval, so a change elsewhere in the repo that degrades it is caught in CI, not in the field
- Failure modes are distinguishable from each other — a wrong final answer traces back to a specific cause (bad reasoning, bad tool call, bad retrieval, bad routing) rather than being an undifferentiated "it didn't work," per `eval/README.md`'s isolated-vs-end-to-end principle
- Known cliff-edge risks (quantization collapsing past a bit-width threshold, MoE routing collapsing onto a subset of experts) have explicit, monitored checks rather than being caught only by chance
- Agentic and CLI operations fail *safely* — a failed step should not compound into a worse state, per the failure-mode notes already stated in `agent/README.md` and `agent/cli/README.md`

## Out of scope

- Raw capability level itself — that's each individual `functional/` file; this file is about *predictability of behavior*, not the behavior's ceiling
- Security vulnerabilities in the traditional software sense — those're handled through the project's standard security process (`.github/security.yml`, `SUPPORT.md`), not this requirement

## Open questions

- What's the right regression-testing cadence — every PR, nightly, per release? This likely needs to differ by how expensive a given eval is to run.
- Should there be a formal "capability floor" below which a release is blocked, and if so, who sets it — ties into `GOVERNANCE.md`'s decision-making process for cross-cutting calls.
