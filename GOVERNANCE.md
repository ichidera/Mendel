# Governance

Mendel is governed under a **Benevolent Dictator For Life (BDFL)** model.

## What that means in practice

- The BDFL has final say on technical direction, architectural decisions, and project scope when consensus doesn't emerge naturally.
- The BDFL's default mode of operating is *not* to overrule — most day-to-day decisions are made by whichever maintainer owns the relevant module (see `MAINTAINERS.md` and `.github/CODEOWNERS`). The BDFL steps in for cross-cutting decisions, disputes maintainers can't resolve between themselves, and anything that changes the project's mission or license.
- This model exists to keep decision-making fast and coherent while the project is small and moving on genuinely unsettled research questions — not to concentrate credit or exclude input. Disagreement, RFCs, and open debate on any decision are welcome and expected before a call gets made.

## Who holds the role

See `MAINTAINERS.md` for the current BDFL and module maintainers.

## How decisions actually get made

1. **Module-level decisions** (an implementation choice within `distillation/`, a new attention variant, etc.) are made by that module's maintainer(s), following the responsibilities laid out in the module's own `README.md`.
2. **Cross-module decisions** (a change that affects the architecture/quantization/inference boundary, for example) are discussed openly — an issue or discussion thread first, with the affected module maintainers weighing in — before being decided.
3. **Project-level decisions** (mission changes, license changes, governance changes, adding/removing a maintainer) rest with the BDFL, made in the open, with reasoning recorded in `docs/`.

## Escalation

If a disagreement between contributors or maintainers can't be resolved through discussion, either party can request a BDFL ruling by opening an issue tagged `governance`. The BDFL's decision in that case is final, but the reasoning behind it will always be written down — nothing gets decided silently.

## Evolving this model

BDFL works well for a small, fast-moving project; it may not be the right model forever. If Mendel grows a maintainer team substantial enough that this stops fitting, that's a project-level decision under the process above — this document isn't permanent by assumption, it's the right fit for where the project is right now.

## Code of conduct enforcement

Code of conduct violations are handled per `.github/CODE_OF_CONDUCT.md`, independently of technical governance — a code of conduct decision is not a BDFL technical call, and is handled through the reporting process described there.
