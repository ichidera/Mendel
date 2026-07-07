# agent/tools/

Handles calling external tools and MCP servers correctly — formatting calls, parsing results, and recovering when a call fails.

## Responsible for
- MCP client implementation: connecting to MCP servers, discovering available tools, invoking them
- Tool call formatting: turning the model's intent into a correctly structured tool call for whatever tool is being invoked
- Result parsing: turning a tool's raw response (JSON, text, structured data) into something the agent loop can reason over
- Failure handling for tool calls specifically: timeouts, malformed responses, auth errors, and how those get surfaced back to `agent/`

## Not responsible for
- Deciding *when* a tool should be used at all, or which tool fits a given sub-goal — that's the planning logic in `agent/`, this directory only handles the mechanics once a tool call has been decided on
- Shell-specific execution — running and parsing shell commands is close to tool-calling in spirit but has its own quirks (streaming output, exit codes, stdin/stdout/stderr) and lives in `agent/cli/` instead

## Why correctness here matters disproportionately
A capable model with a buggy tool-calling layer looks exactly like an incapable model from the outside — it fails the same way regardless of whether the reasoning was right. This directory should be over-tested relative to its apparent simplicity, because errors here are invisible until they cause a downstream task failure that gets misattributed to "the model isn't smart enough."

## Interacts with
- `eval/` — tool-use benchmarks should test this layer in isolation (does a call format correctly, does a malformed response get handled gracefully) as well as end-to-end through `agent/`
