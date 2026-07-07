# retrieval/

Lets Mendel look facts up at inference time instead of memorizing them in its weights. This is the lever that most directly separates "knowledge" from "parameter count" — a fact retrieved from an index costs no parameters at all.

## Responsible for
- The retrieval index itself: how documents/facts are stored and searched (embedding-based, keyword, hybrid — whatever's in use)
- The embedding model or method used to encode queries and documents for retrieval, if separate from Mendel itself
- The interface between "model decides it needs to look something up" and "retrieval system returns relevant content" — including how retrieved content gets formatted back into context
- Freshness/update logic: how the index gets new information without retraining the model

## Not responsible for
- Deciding *when* to retrieve vs. answer from parametric memory — that's a policy the model itself learns (via `distillation/`) or the `agent/` loop decides procedurally; this directory just serves requests when asked
- General tool-calling infrastructure — MCP and tool-use plumbing lives in `agent/tools/`, even though retrieval may be exposed as one such tool

## Why this matters for a lightweight model
Every fact Mendel doesn't have to store in its weights is capacity freed up for reasoning, planning, and tool-use ability instead. A small model that can reliably retrieve what it doesn't know is trading a weakness (limited parametric memory) for a strength (always-current, checkable information) — provided retrieval is fast and accurate enough not to become the bottleneck itself.

## What "working" looks like here
Retrieval quality should be evaluated on its own, separately from end-to-end task success in `eval/` — a bad retrieval result and a bad reasoning step look identical in a wrong final answer, and they need different fixes.
