# Vision

MISSION.md says what we're building. This says why it matters if we succeed.

## The world we're aiming at

Right now, real capability — genuine reasoning, planning, tool use, autonomous action — lives behind an API call to a data center. The models small enough to run on your own device are capable of conversation, not of *work*. That gap is not a law of nature. It's the current state of an unsolved research problem, and it's closing slower than it should because most of the effort chasing it happens behind closed doors, optimizing for what a company can charge for rather than what a person can own.

We want a future where the most capable agent you can run is one you actually possess — on your laptop, on your phone, under your control, with nobody else's server in the loop and nobody else's usage policy standing between you and your own hardware. Not because closed, hosted models are illegitimate — they solve real problems for real people — but because *this specific* capability, running fully under your own control, shouldn't be something only well-funded labs can offer.

## What success looks like

- A single developer can fine-tune Mendel on a task that matters to them, on hardware they already own, without needing lab-scale compute.
- Mendel can be handed a genuinely multi-step goal — not just a question — and carry it through: plan it, use the tools it needs, recover when a step fails, and finish.
- The gap between "runs on a phone" and "capable enough to actually help" keeps shrinking, and this project is part of why it shrinks.
- Every architectural and training decision that got us there is documented and reproducible, so the next project doesn't have to rediscover it.

## What we're not trying to be

Not a benchmark-chasing leaderboard entry. Not a repackaging of someone else's weights with a new name. Not a project that claims capabilities it hasn't measured in `eval/`. If a claim in this document or in MISSION.md ever stops being backed by something real in the repo, that's a bug in our honesty, and it should be treated as one.

## Time horizon

This is a multi-year bet on a problem that hasn't been solved yet, by anyone, at the size we're aiming for. Progress will be uneven — some levers (quantization, retrieval) will show results quickly; others (matching frontier-level reasoning at this size) may take much longer, or may require ideas nobody working on this project has had yet. VISION.md describes the destination. ROADMAP.md describes what we currently believe the path looks like, and that path will be revised often as we learn.
