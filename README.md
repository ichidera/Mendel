<div align="center">

# Mendel

**The most capable lightweight model we can build.**

Thinking. Planning. Tool use and MCP. Skills. Agentic action. CLI. Computer control.
All small enough to run on hardware you actually own.

[Mission](MISSION.md) · [Vision](VISION.md) · [Roadmap](ROADMAP.md) · [Contributing](CONTRIBUTING.md) · [FAQ](FAQ.md) · [Governance](GOVERNANCE.md)

</div>

---

## What Mendel is

Model capability and model size are usually treated as the same axis. They aren't. Mendel exists in the gap between them — pulling every lever that trades raw scale for capability density, so that "runs on your laptop or phone" and "capable enough to actually get work done" stop being mutually exclusive.

This isn't a chatbot project. The target is an agent: something that can reason through a problem, break a goal into steps, call tools and MCP servers correctly, follow modular skills, operate a shell, and control a mouse and keyboard — all at a footprint nowhere near what that capability set usually costs.

Read [`MISSION.md`](MISSION.md) for the concrete objective and [`VISION.md`](VISION.md) for why it matters if we get there.

## The levers

No single trick closes the gap between small and capable. Mendel combines several:

| Lever | What it does |
|---|---|
| **Distillation** | Train on a stronger model's behavior — reasoning, plans, tool use — not just raw text |
| **Mixture-of-Experts** | Store more specialized capability than we run per token |
| **Quantization** | Represent weights in as few bits as the task tolerates |
| **Retrieval** | Keep facts out of the weights; look them up instead |
| **Agentic scaffolding** | Compensate for scale with better planning and self-correction structure |

Each lever has its own directory and its own README with specifics — see the repo layout below.

## Repository layout

```
mendel/
├── architecture/    # model definition — layers, attention, MoE routing
├── distillation/    # teacher-student training pipelines
├── quantization/    # bit-width reduction and precision tradeoffs
├── retrieval/       # external memory / lookup at inference time
├── agent/           # planning loop, tool use, MCP, skills, CLI operation
├── control/         # mouse/keyboard/GUI control
├── eval/            # capability benchmarks — the thing every claim here is measured against
├── inference/       # runtime — how a trained model executes on real hardware
└── docs/            # design rationale and experiment logs
```

**The rule this repo follows strictly:** a file's location and name tell you what it does — no digging required. Every directory above has its own `README.md` stating exactly what it's responsible for, and just as importantly, what it isn't. Read the module README before touching a module.

## Status

Early — see [`ROADMAP.md`](ROADMAP.md) for the current phase and what's next. Nothing here is a finished system yet; treat the docs as a map, not a receipt.

## Getting involved

- **Contribute code, evals, or docs:** [`CONTRIBUTING.md`](CONTRIBUTING.md)
- **Ask a question or float an idea:** GitHub Discussions (see [`.github/SUPPORT.md`](.github/SUPPORT.md))
- **Report a bug:** open an issue using the templates in `.github/ISSUE_TEMPLATE/`
- **Understand how decisions get made:** [`GOVERNANCE.md`](GOVERNANCE.md) — Mendel is run under a BDFL model

## License

See [`LICENSE`](LICENSE). Intent is a permissive license so Mendel can genuinely be run, modified, fine-tuned, and redistributed by anyone.

## Why "Mendel"

Gregor Mendel worked out what could be inherited, and how, using small controlled experiments rather than brute force. That's the bet this project is making on model capability: figure out exactly what a small model needs to inherit from a capable one, and build the pipeline that passes down exactly that — nothing more.