# agent/skills/

Loads and applies modular, task-specific instruction sets — "skills" — that guide Mendel through particular kinds of tasks without needing that knowledge baked permanently into the weights.

## Responsible for
- Skill definition format: how a skill is structured, discovered, and loaded
- Skill selection logic: given a task, deciding which skill(s), if any, apply
- Injecting a loaded skill's guidance into the agent loop's working context at the right point

## Not responsible for
- The general agent loop itself (planning, acting, observing) — that's `agent/`; skills modify *how* a task is approached, they don't replace the loop that executes it
- Tool mechanics — a skill might reference tools, but the actual calling logic is `agent/tools/`

## Why skills are a capability lever, not just documentation
The same argument as `retrieval/`, applied to *procedures* instead of *facts*: a skill that lives in a loadable file is procedural knowledge Mendel doesn't have to encode permanently in its weights. A small model with a well-designed skill library can match a much larger model's task-specific competence on exactly the tasks it has skills for, without paying the parameter cost of having memorized those procedures.

## What makes a good skill file here
A skill should be specific enough to change behavior meaningfully and general enough to apply across many instances of a task type — "how to fill out a PDF form" is a skill; "how to fill out *this specific* PDF form" is not. Each skill file should state plainly what triggers it and what it does, following the same file-transparency rule as the rest of this repo.

## Interacts with
- `eval/` — skill effectiveness should be measured with and without the skill loaded, to confirm it's actually improving task performance rather than just adding context noise
