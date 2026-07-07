# Extensibility

**Status:** draft
**Owner module(s):** cross-cutting — repo structure itself, all modules
**Related eval:** _none yet — see eval/README.md_
**Last updated:** _initial draft_

## Requirement

The repository's modular structure must actually deliver what it promises: a new contributor should be able to find where their idea belongs, implement it in isolation, and land it without needing to understand or touch unrelated parts of the system.

## Acceptance criteria

- Every module's `README.md` accurately states what it's responsible for and what it isn't — drift between stated and actual responsibility is treated as a bug, per each module README's own framing
- A new architectural idea (new attention variant, new MoE routing strategy) can be added as a self-contained addition to `architecture/attention/` or `architecture/moe/` without modifying unrelated files
- A new skill can be added to `agent/skills/` without any change to `agent/`'s core loop
- A new eval can be added to `eval/` for any capability without requiring changes to the capability's own implementation
- The `scripts/generate_repo_map.py` tool (or its successor) can verify the promised structure matches reality, catching drift automatically rather than relying on manual review

## Out of scope

- Whether a given architectural choice is *good* — that's judged by `eval/` results and each module's own design rationale in `docs/`; this file is about whether the codebase's structure supports adding and testing new ideas cleanly, not about the ideas themselves

## Open questions

- What interface/contract should each pluggable component type (attention variant, MoE router, skill file) be required to implement, and where should that contract be formally documented once the first few implementations exist?
- How do we measure "extensibility" concretely rather than just asserting it — is time-to-first-contribution for a new component type a reasonable proxy metric?
