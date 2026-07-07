# CLI operation

**Status:** draft
**Owner module(s):** `agent/cli/`
**Related eval:** _none yet — see eval/README.md_
**Last updated:** _initial draft_

## Requirement

Mendel must be able to operate a command-line shell competently: issuing commands, correctly interpreting their output (including errors and partial failures), chaining commands toward a goal, and debugging its own mistakes.

## Acceptance criteria

- Mendel issues syntactically correct commands appropriate to the task and shell environment
- Mendel correctly interprets command output, including distinguishing success from failure when the exit code alone doesn't make that obvious (e.g. a command that exits 0 but printed an error to stdout)
- On a failed command, Mendel identifies the likely cause from the output and issues a corrected next command, rather than repeating the same failed command or guessing blindly
- Mendel tracks shell session state correctly across multiple commands — working directory, environment variables, and effects of prior commands
- Destructive or irreversible commands are handled with appropriate caution, consistent with the safety note in `agent/cli/README.md`

## Out of scope

- Structured tool/MCP calls — those go through `functional/tool-use.md`; this file is specifically about unstructured shell text in, shell text out
- GUI-based control — that's `functional/computer-control.md`

## Open questions

- What sandboxing/dry-run guarantees should be a hard requirement here versus an implementation detail of `agent/cli/`?
- How do we build an eval set that captures messy, real-world CLI output (ambiguous warnings, multi-line stack traces) rather than only clean, well-behaved command output?
