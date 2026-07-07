# Mendel

**Mission:** build the most capable lightweight model — small enough to run on-device, capable enough to think, plan, use tools, and act.

Mendel is not trying to be the biggest model. It's trying to inherit the most from the biggest models while staying small enough to actually belong to the people running it. The name is deliberate: Mendel didn't grow the tallest pea plant — he figured out what could be *inherited*, and how. That's the whole bet this project is making.

## The bet

Capability and size are usually treated as the same axis. They aren't. A model's capability is bounded by how much of the world it needs to represent; its footprint is bounded by hardware. Mendel exists in the gap between those two constraints, and every design decision here is aimed at widening that gap rather than assuming it's fixed.

We're not chasing raw scale. We're chasing **capability density** — how much genuine reasoning, planning, and tool-use ability we can pack per parameter, per megabyte, per watt.

## What "capable" means for this project

Mendel isn't a chatbot. The target capability set is:

- **Thinking** — multi-step reasoning before answering, not just next-token pattern completion
- **Planning** — decomposing a goal into ordered sub-tasks and tracking progress across them
- **Tool use / MCP** — calling external tools and MCP servers correctly, handling structured results, recovering from failed calls
- **Skills** — loading and following modular instruction sets for specific task types rather than relying purely on parametric memory
- **Agentic operation** — running autonomously across many steps toward a goal, including self-correction
- **CLI fluency** — operating a shell competently: reading output, chaining commands, debugging its own mistakes
- **Computer control** — operating a mouse and keyboard against a real GUI, not just an API

Every one of these is a capability, not a parameter count. That distinction is the whole project.

## The levers we're pulling

No single trick closes the gap between "phone-sized" and "frontier-capable." We're combining several, in roughly this order of leverage:

| Lever | What it does | Where it lives in the repo |
|---|---|---|
| **Distillation** | Train Mendel on the *behavior* of larger, more capable models rather than raw text alone — inherit judgment, not just facts | `/distillation` |
| **Mixture-of-Experts (MoE)** | Store more specialized knowledge than we can afford to run at once; activate only the relevant slice per token | `/architecture/moe` |
| **Quantization** | Represent weights in as few bits as the task tolerates, without cliff-edge capability loss | `/quantization` |
| **Retrieval augmentation** | Keep facts out of the weights entirely — look them up at inference time instead of memorizing them | `/retrieval` |
| **Architecture efficiency** | Squeeze more effective capability per parameter through structural tricks (sparse attention, shared/per-layer embeddings, etc.) | `/architecture` |
| **Agentic scaffolding** | Compensate for raw capability gaps with better loop structure — planning, self-critique, tool feedback | `/agent` |

## Repo philosophy: the file *is* the function

Mendel's structure follows one rule strictly: **a file's location and name should tell you exactly what it does — no digging required.** If you can read the path, you should be able to guess the behavior. If you open the file, that guess should be confirmed on line one.

Practical consequences of this rule:

- No god-files. If a file starts doing two things, it becomes two files.
- No "utils.py" or "misc/" — every file's job is specific enough to name precisely.
- Config lives next to what it configures, not centralized in one sprawling settings file.
- Every module directory has its own short `README.md` explaining what that module is responsible for and, just as importantly, what it is *not* responsible for.

## Repository layout

```
mendel/
├── architecture/          # model definition — layers, attention, MoE routing
│   ├── moe/                 # expert routing and activation logic
│   └── attention/            # attention variants (sparse, local/global hybrid, etc.)
├── distillation/           # teacher-student training pipelines
├── quantization/           # bit-width reduction, calibration, eval-vs-precision tradeoffs
├── retrieval/              # external memory / lookup at inference time
├── agent/                  # planning loop, self-correction, task decomposition
│   ├── tools/                # tool-calling and MCP client logic
│   ├── skills/                # modular skill definitions the agent loads at runtime
│   └── cli/                   # shell-operating logic — command execution, output parsing
├── control/                # mouse/keyboard/GUI control interface
├── eval/                   # capability benchmarks — reasoning, planning, tool-use, agentic tasks
├── inference/              # runtime — how a trained model actually executes on target hardware
└── docs/                   # design rationale, experiment logs, decisions and why we made them
```

Each top-level directory owns exactly one lever from the table above, or one capability from the list above. If you're not sure where something belongs, that's a sign it needs to be split before it's merged.

## Status

Early. This README describes the target, not a finished system — treat it as a map, not a receipt. Expect the repo structure above to firm up as the first modules land; anything here is subject to revision as we learn what actually works.

## Contributing

Contributions are welcome, especially in the areas listed as levers above. Before opening a PR:

1. Know which lever or capability your change belongs to, and put it in that directory.
2. If your file does more than one job, split it before submitting.
3. Include or update the relevant eval in `/eval` — a capability claim without a benchmark doesn't count here.
4. Keep module-level `README.md`s honest and current; they're load-bearing documentation, not decoration.

## License

TBD — will be finalized before first public release. Intent is a permissive open-source license (Apache 2.0 or MIT) so the model can genuinely be run, modified, and redistributed by anyone.

## Why "Mendel"

Gregor Mendel worked out which traits get passed on and how, using nothing but careful observation and small, controlled experiments — not brute force. That's the spirit here: figure out what a small model actually needs to inherit from a capable one, and build the pipeline that passes exactly that down, nothing more.