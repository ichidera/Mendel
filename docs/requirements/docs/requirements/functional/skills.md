# Skills

**Status:** draft
**Owner module(s):** `agent/skills/`
**Related eval:** _none yet — see eval/README.md_
**Last updated:** _initial draft_

## Requirement

Mendel must be able to discover, load, and correctly follow modular skill definitions that guide it through specific task types, without that procedural knowledge needing to be permanently encoded in its weights.

## Acceptance criteria

- Given a task that matches an available skill, Mendel selects and loads the relevant skill rather than improvising from general knowledge alone
- Following a loaded skill measurably improves task performance compared to attempting the same task without it (per `agent/skills/README.md`'s "with and without" evaluation approach)
- Mendel correctly handles multiple candidate skills for an ambiguous task — either by picking the best fit or by using general reasoning to disambiguate first
- Skill-following degrades gracefully, not catastrophically, when a skill's instructions don't perfectly match the task at hand

## Out of scope

- Authoring new skill files — that's a contribution/content question, not a model capability requirement
- General tool mechanics referenced *within* a skill — that's `functional/tool-use.md`, this file covers the loading/selection/following behavior itself

## Open questions

- What's the right skill discovery mechanism at inference time — keyword matching, embedding similarity, or something the model itself decides via reasoning?
- How many skills can be loaded/considered simultaneously before context becomes the bottleneck, especially at Mendel's target footprint?
