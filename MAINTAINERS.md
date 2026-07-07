# Maintainers

Mendel is governed as a BDFL project — see `GOVERNANCE.md` for how decisions get made. This file lists who currently holds that role and who maintains which parts of the codebase day to day.

## BDFL

| Name | GitHub | Scope |
|---|---|---|
| ichidera | @ichidera | Final say project-wide; see GOVERNANCE.md |

## Module maintainers

Day-to-day technical decisions within a module rest with that module's maintainer(s). This table should stay in sync with `.github/CODEOWNERS` — if they disagree, `CODEOWNERS` is what GitHub actually enforces for review requests, so treat a mismatch as a bug and fix it promptly.

| Module | Maintainer(s) |
|---|---|
| `architecture/` | _unassigned_ |
| `architecture/attention/` | _unassigned_ |
| `architecture/moe/` | _unassigned_ |
| `distillation/` | _unassigned_ |
| `quantization/` | _unassigned_ |
| `retrieval/` | _unassigned_ |
| `agent/` | _unassigned_ |
| `agent/tools/` | _unassigned_ |
| `agent/skills/` | _unassigned_ |
| `agent/cli/` | _unassigned_ |
| `control/` | _unassigned_ |
| `eval/` | _unassigned_ |
| `inference/` | _unassigned_ |
| `docs/` | _unassigned_ |

Until a module has a dedicated maintainer, the BDFL holds that responsibility by default.

## Becoming a maintainer

Sustained, quality contribution to a specific module is the path — there's no formal application. If you've been consistently active in a module's issues and PRs, open an issue tagged `governance` proposing yourself (or nominating someone else), and the BDFL will make the call, per `GOVERNANCE.md`.

## Stepping down

Maintainers can step back from a module at any time — open an issue tagged `governance` to hand it off. No justification required; life happens.
