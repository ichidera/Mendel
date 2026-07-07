# Contributing to Mendel

Thanks for considering it. This project is attacking a genuinely unsolved problem — capability density at small scale — and it needs contributors thinking carefully across research, engineering, and evaluation. Here's how to get involved effectively.

## Before you write any code

1. **Read the module's README first.** Every directory in this repo has one, and it states what that module is responsible for and, just as importantly, what it isn't. If your change doesn't fit cleanly into one module's stated responsibility, that's a signal to either pick the right module or propose a new one — not to bolt it onto the nearest existing file.
2. **Check `ROADMAP.md`.** If your idea belongs to a phase we haven't started yet, it's still welcome, but flag that context in your issue/PR so it doesn't get evaluated as if it's the current priority.
3. **For anything nontrivial, open an issue before a PR.** Especially for architecture, distillation, or agent-loop changes — these are exactly the areas where two people can build conflicting things in parallel without knowing it. A quick issue avoids wasted work.

## The core rule: a file is what it does

If your PR adds a file that does two unrelated things, split it before submitting. If you're not sure where something belongs, ask in the issue rather than guessing — a misplaced file is more expensive to fix later than a five-minute question now.

## What a good PR looks like here

- **Lives in the right module**, per that module's own README
- **Includes or updates an eval** in `eval/` if it touches a capability claim — "it runs" is not the same as "it works," and this repo treats those as different bars
- **Updates the module README** if it changes what that module is responsible for, or adds a meaningful new component to it
- **Explains the *why*** in the PR description, not just the what — if it's a nontrivial decision, consider whether it deserves an entry in `docs/` too
- **Passes CI** (`.github/workflows/`) — lint, tests, and security checks are non-negotiable gates, not suggestions

## Code review and ownership

Review requests route through `.github/CODEOWNERS`, matching the maintainers listed in `MAINTAINERS.md`. Module maintainers own approval for changes in their area; cross-module changes may need review from more than one maintainer. See `GOVERNANCE.md` for how disagreements get resolved if they don't settle through normal review.

## Reporting bugs / requesting features

Use the issue templates in `.github/ISSUE_TEMPLATE/` — they exist to make sure the information a maintainer actually needs shows up on the first message, not after three rounds of "can you clarify."

## Questions, not bugs

Use GitHub Discussions rather than an issue — see `.github/SUPPORT.md` for where different kinds of questions belong.

## Code of conduct

All contribution happens under `.github/CODE_OF_CONDUCT.md`. Read it; it's short and it's enforced.

## License

By contributing, you agree your contribution is licensed under the project's license (see `LICENSE`). If that's not something you can agree to, please don't open the PR — reach out first and we'll figure out what's possible.
