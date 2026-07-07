# requirements/

This is Mendel's scope, kept modular instead of living in one sprawling PRD. One file per capability (functional) or per quality attribute (non-functional), so a requirement stays a single source of truth no matter how many roadmap phases touch it.

## Why not a PRD

A single PRD covering thinking, planning, tool use, skills, agentic loops, CLI, computer control, footprint, performance, portability, reliability, openness, and extensibility would be enormous, and — worse — nobody would keep all of it in sync as any one piece evolved. Splitting by capability means a change to how we define "planning" touches exactly one file, reviewed by exactly the people who care about planning.

## Structure

- **`functional/`** — what Mendel must be able to *do*. One file per capability listed in `MISSION.md`.
- **`non-functional/`** — what must be true about *how* it does it: size, speed, portability, reliability, openness, extensibility.
- **`../decisions/`** — not requirements themselves; the record of *why* a requirement changed. If a target in `functional/planning.md` or `non-functional/footprint.md` shifts, the reasoning gets an entry there.

## Shared template

Every requirement file uses this shape:

```markdown
# <Capability or attribute name>

**Status:** draft | active | met | revised
**Owner module(s):** which module(s) in the repo implement this
**Related eval:** the eval/ benchmark that proves this requirement, once one exists
**Last updated:** date of last substantive change

## Requirement
Plain statement of what must be true.

## Acceptance criteria
Concrete, checkable conditions — the thing eval/ actually tests against.

## Out of scope
What this requirement deliberately does not cover, so it doesn't creep.

## Open questions
Anything unresolved that shouldn't block writing the requirement down.
```

## Status field meanings

- **draft** — written down, not yet agreed or measurable
- **active** — agreed, being worked toward, not yet met
- **met** — acceptance criteria satisfied and verified in `eval/`
- **revised** — changed from an earlier version; see `../decisions/` for why

## Keeping this honest

A requirement marked `met` without a corresponding `eval/` benchmark is a documentation bug, not a capability. Treat mismatches between this directory and `eval/`'s actual coverage as issues to fix, not details to let slide.
