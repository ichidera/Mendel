# Tool use & MCP

**Status:** draft
**Owner module(s):** `agent/tools/`
**Related eval:** _none yet — see eval/README.md_
**Last updated:** _initial draft_

## Requirement

Mendel must be able to correctly decide when a tool or MCP server call is needed, format that call correctly, interpret the result, and recover sensibly when a call fails or returns something unexpected.

## Acceptance criteria

- Given a task solvable only with an external tool (current information, an action in the world, structured data access), Mendel calls the appropriate tool rather than guessing or hallucinating a result
- Tool calls are correctly formatted against the tool's actual schema/interface — malformed calls should be rare enough to be an eval-tracked regression, not an expected failure mode
- Mendel correctly parses structured tool results (JSON, MCP tool_result blocks, etc.) and incorporates them into its next step
- On a failed or malformed tool response, Mendel recognizes the failure and takes a sensible next step (retry, alternate tool, ask for clarification) rather than proceeding as if the call succeeded
- MCP server discovery and invocation work correctly against real MCP servers, not just mocked test harnesses

## Out of scope

- Shell command execution specifically — that's `functional/cli.md`, even though it's mechanically similar
- Deciding *whether* a tool-using approach is the right plan for a goal — that's `functional/planning.md`; this file covers correctness once the decision to use a tool has been made

## Open questions

- What's the right training signal for "when not to use a tool" — false-positive tool calls (using a tool when parametric knowledge would suffice) may be as important to avoid as false negatives
- How much tool-use competence should be distilled from a teacher's tool-call traces vs. learned through the agent loop's own scaffolding (`agent/README.md`'s "scaffolding compensates for scale" principle)?
