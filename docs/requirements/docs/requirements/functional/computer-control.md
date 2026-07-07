# Computer control

**Status:** draft
**Owner module(s):** `control/`
**Related eval:** _none yet — see eval/README.md_
**Last updated:** _initial draft_

## Requirement

Mendel must be able to operate a real graphical interface directly — interpreting what's on screen and issuing mouse and keyboard input — for tasks with no API or shell path available.

## Acceptance criteria

- Given a screenshot or accessibility-tree representation of a screen, Mendel correctly identifies relevant on-screen elements (buttons, fields, menus) well enough to act on them
- Mendel issues mouse/keyboard actions that correctly target the intended element, not an adjacent or similar-looking one
- Mendel verifies that an intended action actually took effect (per `control/README.md`'s note that verification is harder than execution) rather than assuming success and continuing
- Mendel recovers sensibly when an action fails to land as intended — recognizing the mismatch and adjusting, rather than compounding the error with further blind actions

## Out of scope

- Deciding *what* to click/type in service of a larger goal — that's `functional/planning.md` and `functional/agentic-loop.md`; this file is about correct low-level execution and verification only
- Shell/CLI actions — those are `functional/cli.md`, used instead of this capability whenever an API or shell path exists

## Open questions

- What's the right perception input — raw screenshots, an accessibility tree, or both — and how does that choice interact with the footprint budget in `non-functional/footprint.md`?
- How do we build a safe, repeatable eval harness for GUI control that doesn't risk unintended side effects on a real system during testing?
