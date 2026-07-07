# Footprint

**Status:** draft
**Owner module(s):** `architecture/`, `architecture/moe/`, `quantization/`
**Related eval:** _none yet — see eval/README.md_
**Last updated:** _initial draft_

## Requirement

Mendel must run within memory and storage budgets appropriate to each target device class, without the capability requirements in `functional/` being treated as separate from this constraint — footprint and capability are traded off against each other deliberately, not achieved independently.

## Acceptance criteria

- A defined memory ceiling exists per target device class (phone, laptop/edge, single-server-GPU), tracked here once benchmarking work in Phase 1+ establishes realistic numbers
- Active parameters per token (as distinct from total stored parameters, per `architecture/moe/README.md`) are reported alongside total footprint for any MoE configuration
- Every quantization level shipped has a footprint figure attached, tied to the corresponding entry in `quantization/README.md`'s precision-vs-capability tracking
- Footprint claims are always paired with the capability level they were measured at — a footprint number without a corresponding `eval/` capability score is not a complete claim

## Out of scope

- Runtime speed/latency — that's `non-functional/performance.md`; footprint here means static memory/storage size, not execution time
- Which specific hardware platforms are supported — that's `non-functional/portability.md`

## Open questions

- What are the actual target numbers per device class? This needs real numbers, not placeholders — to be filled in once Phase 1's baseline gives us something to measure against.
- Should footprint targets be fixed up front, or set adaptively based on what capability levels prove achievable at each size during Phase 3?
