# Portability

**Status:** draft
**Owner module(s):** `inference/`
**Related eval:** _none yet — see eval/README.md_
**Last updated:** _initial draft_

## Requirement

Mendel must run correctly across the range of target hardware and platforms this project intends to support, with clearly separated execution paths per target rather than one path patched with conditionals for every device.

## Acceptance criteria

- Defined list of supported device classes (to be finalized: phone, laptop/edge, single-server-GPU at minimum) with a distinct, maintained execution path for each, per `inference/README.md`'s guidance against a single conditional-laden path
- Model checkpoints and quantization levels are portable across supported runtimes without requiring a full re-export per platform, where feasible
- Any platform-specific dependency (a particular OS, a particular accelerator API) is documented clearly enough that a contributor can tell immediately whether their target is supported
- Portability claims are tested, not assumed — a platform isn't "supported" until it has a passing entry in `eval/`

## Out of scope

- Absolute speed or memory use on a given platform — those are `non-functional/performance.md` and `non-functional/footprint.md` respectively; this file covers "does it run correctly here at all," not "how well"

## Open questions

- What's the actual minimum supported platform list at each project phase — do we commit to phone support early, or treat it as a later milestone once laptop/edge is solid?
- How much of `agent/cli/` and `control/`'s behavior is platform-dependent (different shells, different OS accessibility APIs) and how does that affect what "portable" even means for those capabilities specifically?
