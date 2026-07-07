# ADR 0001: Template

**Status:** template — copy this file to a new number when recording a real decision (e.g. `0002-...md`)
**Date:** _fill in_
**Related requirement(s):** _which file(s) in `../requirements/` this decision affects, if any_

## Context

What situation forced this decision? What did we observe — an experiment result, a benchmark failure, a design conflict between two modules — that made the previous approach no longer sufficient?

## Decision

What did we actually decide to do? State it plainly, as something a future contributor could act on without needing to reconstruct the reasoning first.

## Alternatives considered

What else did we consider, and why was it rejected? Include the option that seemed obvious but didn't work — that's often the most valuable part of the record, since it stops someone from re-proposing it in six months without knowing it was already tried.

## Consequences

What does this decision change downstream? Note any requirement file in `../requirements/` that needs its status updated to `revised` as a result, and update it in the same PR as this ADR.

## Related eval

If this decision was driven by (or should be validated against) a specific `eval/` result, link it here.

---

## Naming and numbering convention

- File name: `NNNN-short-descriptive-title.md`, numbers zero-padded to four digits, sequential, never reused even if a decision is later reversed
- A reversed decision gets a *new* ADR explaining the reversal — don't edit or delete the original; the original recorded a real decision made with the information available at the time, and that's worth keeping
- Link related ADRs to each other directly (e.g. "supersedes ADR 0003") rather than relying on numbering alone to convey the relationship
