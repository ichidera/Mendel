# distillation/

Trains Mendel by learning from the behavior of larger, more capable models — not just from raw text. This is the single highest-leverage lever in the project: it's how a small model inherits judgment instead of rediscovering it from scratch.

## Responsible for
- Teacher-student training pipelines: generating or collecting teacher outputs, and training Mendel to match them
- Loss functions specific to distillation (e.g. matching output distributions, not just final answers — soft-label / logit-matching approaches where available)
- Data pipeline for whatever the teacher signal is: full reasoning traces, tool-use trajectories, planning decompositions — not just final text completions
- Curriculum decisions: what capability gets distilled in what order (e.g. basic reasoning before agentic tool-use)

## Not responsible for
- Defining the student model's architecture — that's `architecture/`, this directory trains whatever architecture it's given
- Shrinking weights after training via reduced precision — that's `quantization/`
- Evaluating whether distillation actually worked — that's `eval/`, though this directory should make it easy to plug a checkpoint into eval

## Why behavior, not just text
Standard pretraining learns statistical patterns in text. Distillation here specifically means training Mendel against a stronger model's *outputs on the actual target capabilities* — reasoning chains, plans, tool calls, corrections after failed tool calls. The goal is to inherit the *process* a capable model uses, not just facts it knows. If a training run only distills final answers with no visibility into intermediate reasoning, it's not using this lever fully — flag that in the run's documentation.

## A note on provenance
Whatever teacher model or models are used as a training signal, document that clearly and check licensing before use — this repo intends to be genuinely open-source and redistributable, and that's only true if every dependency in the pipeline is too.
