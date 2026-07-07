# control/

Lets Mendel operate a real graphical interface directly — moving the mouse, clicking, typing — rather than only interacting through APIs or a shell.

## Responsible for
- Screen understanding: interpreting a screenshot or accessibility tree well enough to identify what's on screen and where
- Input execution: issuing mouse movement/clicks and keyboard input to the target OS/application
- Action verification: confirming an intended action actually happened (the right window was clicked, the right field was typed into) rather than assuming success
- Coordinate/element targeting: translating "click the submit button" into an actual screen position or accessibility-tree element reference

## Not responsible for
- Deciding *what* to click or type in service of a larger goal — that's `agent/`'s planning layer; this directory only executes a given low-level action against the screen
- Shell or tool-call actions — those go through `agent/cli/` and `agent/tools/` respectively; this directory is specifically for GUI-level control where no API or shell path exists

## Why this is its own top-level directory, not a subdirectory of agent/
GUI control is a genuinely distinct capability surface with its own perception problem (reading a screen) on top of its own action problem (issuing input) — it's closer in kind to a sensor/actuator interface than to planning logic. Keeping it as a peer to `agent/` rather than nested inside it reflects that: `agent/` decides to use it, the way it might decide to use `agent/tools/`, but it isn't part of the planning loop itself.

## The hardest part, honestly
Verifying an action *succeeded* is harder than performing it — a click can land on the wrong element, a typed field can silently fail to receive focus. Treat "did that actually work" as a first-class problem here, not an afterthought; failures in this layer are usually invisible until a much later step breaks for a reason that traces back here.
