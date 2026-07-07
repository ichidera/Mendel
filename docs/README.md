# docs/

The project's memory of *why*, not just *what*. Design rationale, experiment logs, and decisions that were made — including the ones that were reversed.

## Responsible for
- Design decision records: why an architectural or engineering choice was made, what alternatives were considered, and why they were rejected
- Experiment logs: what was tried in `distillation/`, `quantization/`, `architecture/`, etc., what the result was, and whether it shipped
- Explanations that don't belong in a module README because they cut across multiple modules (e.g. "why we chose this MoE + quantization combination together")

## Not responsible for
- Module-specific responsibility statements — each module's own `README.md` owns "what this directory does," this directory owns "why we ended up doing it this way"
- User-facing instructions — setup/usage docs, if they grow large enough to need their own home, get their own top-level location rather than living here

## Why this directory exists at all
In a project moving fast on genuinely unsolved research problems, the reasoning behind a decision is at least as valuable as the decision itself — especially the failed experiments. A negative result in `distillation/` that isn't written down here will get quietly re-attempted by someone else in six months. Treat a well-documented failure as equally valuable to a shipped success.

## Format
Short, dated entries beat comprehensive rewrites. A decision record doesn't need to be polished — it needs to be honest and easy to find later. Link back to the relevant module and, where one exists, the `eval/` result that informed the decision.
