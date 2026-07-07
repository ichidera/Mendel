# FAQ

## What is Mendel, in one sentence?
An open-source effort to build the most capable *lightweight* model we can — one that can think, plan, use tools and MCP, follow skills, act agentically, operate a CLI, and control a mouse/keyboard — without requiring data-center-scale hardware to run.

## Why not just use an existing small open model?
Existing lightweight open models (the current generation of small on-device models from various labs) are optimized primarily for efficient conversation and basic tasks, not for the specific combination of capabilities this project targets: multi-step planning, tool/MCP use, agentic self-correction, and computer control, all at a small footprint. Where good ideas already exist in that space — quantization tricks, per-layer embeddings, mixture-of-experts routing — we intend to learn from and build on them, not reinvent them out of pride. See `ROADMAP.md` for how those ideas map onto our own levers.

## Is this trying to beat the biggest proprietary models?
No — that's not the comparison that matters here. The goal is closing the gap between "runs on your own hardware" and "capable enough to actually do agentic work," not chasing leaderboard parity with models that assume a data center. See `VISION.md` for the actual target.

## What makes a model "lightweight" here, concretely?
Low enough parameter/memory footprint and low enough active compute per token to run on consumer hardware — a laptop, and eventually a phone — rather than requiring server-grade GPUs. Specific target numbers will be defined and tracked in `eval/` as the project matures rather than fixed prematurely here.

## What's the actual technical approach?
Five main levers, combined rather than used in isolation: distillation from stronger models' behavior, mixture-of-experts routing, quantization, retrieval-augmentation to offload factual memorization, and careful agentic scaffolding to compensate for raw scale with better loop structure. See each lever's directory README for specifics, and `ROADMAP.md` for sequencing.

## Is Mendel affiliated with any AI lab?
No. This is an independent open-source project.

## What license is this under?
See `LICENSE`. Intent is a permissive license so the model can genuinely be run, modified, fine-tuned, and redistributed by anyone — check `LICENSE` for the current, authoritative terms.

## How is the project governed?
BDFL model — see `GOVERNANCE.md` for exactly how decisions are made and `MAINTAINERS.md` for who currently holds which role.

## How can I help?
See `CONTRIBUTING.md`. Contributions to any lever, to `eval/`, or to documentation are all genuinely valuable — this isn't a project where only model-training work counts.

## Where do I ask a question that isn't a bug report?
GitHub Discussions — see `.github/SUPPORT.md`.

## Why the name "Mendel"?
Explained in `README.md` — short version: Mendel figured out what could be inherited and how, using careful small experiments rather than brute force. That's the spirit of this project's approach to capability.
