# agent/

The loop that turns Mendel from "a model that answers" into "a model that acts": planning, tool use, self-correction, and multi-step execution toward a goal.

## Responsible for
- The core agent loop: given a goal, decide the next action, take it, observe the result, decide the next action again
- Task decomposition: breaking a high-level goal into an ordered sequence of sub-tasks
- Self-correction: noticing a step failed or produced an unexpected result, and adjusting rather than continuing blindly
- State/memory management *within a single agentic run* (what's been tried, what worked, what the current sub-goal is)

## Not responsible for
- The specific mechanics of calling a tool or MCP server — that's `agent/tools/`
- Loading and following a specific skill's instructions — that's `agent/skills/`
- Operating a shell specifically — that's `agent/cli/`
- Controlling a mouse/keyboard/GUI — that's `control/`, a peer to `agent/`, not a child of it, since GUI control is invoked *by* the agent loop but is its own capability surface

## Design principle: scaffolding compensates for scale
A smaller model can still be reliably agentic if the loop around it is well-designed — clear planning structure, explicit checkpoints, honest self-critique steps — rather than relying on the model to hold an entire plan perfectly in one forward pass. This directory is where "we can't out-scale the frontier, but we can out-structure it" actually gets implemented.

## Subdirectories
- `tools/` — tool-calling and MCP client logic
- `skills/` — modular, loadable skill definitions
- `cli/` — shell-operating logic specifically (command execution, output parsing, error recovery)

## Failure mode to design against
Agent loops fail quietly by continuing past a bad step instead of catching it. Any change here should make it easier for the loop to notice "that didn't work," not just easier for it to keep going.
