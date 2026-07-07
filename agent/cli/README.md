# agent/cli/

Lets Mendel operate a command-line shell competently: running commands, reading their output, chaining them together, and debugging its own mistakes.

## Responsible for
- Command execution: safely running shell commands and capturing stdout, stderr, and exit codes
- Output interpretation: parsing command results (including multi-line, streaming, or error output) into something the agent loop can act on
- Error recovery specific to shell work: recognizing a failed command, understanding *why* it failed from its output, and adjusting the next command accordingly
- Session/state handling: tracking working directory, environment variables, and command history across a multi-step shell session

## Not responsible for
- General tool-calling/MCP mechanics — those are structured, typed interactions handled by `agent/tools/`; shell commands are unstructured text in, unstructured text out, which is why this gets its own directory instead of being folded into tools
- Deciding *what* task the shell work is in service of — that's `agent/`'s planning layer

## Why shell competence is a distinct capability
Reading and correctly interpreting raw CLI output — stack traces, partial failures, ambiguous warnings — is a different skill from calling a well-typed tool with a clean JSON response. A model can be excellent at structured tool use and still fail badly at shell work if it can't parse messy real-world command output or recognize when a command silently did the wrong thing. This directory exists to make that failure mode a first-class target for both training data (`distillation/`) and evaluation (`eval/`).

## Safety note
Shell execution is one of the highest-stakes capabilities in this repo — a wrong command can do real, irreversible damage. Any change here should be reviewed with that in mind, and sandboxing/dry-run modes should be treated as core features, not optional extras.
