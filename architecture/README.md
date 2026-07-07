# architecture/

Defines what Mendel *is* as a computational object — the layers, the forward pass, the shape of the network. Nothing in here trains a model or shrinks one. This is the blueprint, not the factory and not the compression plant.

## Responsible for
- Model definition: embedding layers, transformer blocks, output head
- Wiring together the pieces owned by `attention/` and `moe/` into a full forward pass
- Config schema for architectural hyperparameters (layer count, hidden size, expert count, etc.) — one config format, versioned, so a checkpoint always knows exactly what shape produced it

## Not responsible for
- **Training** the weights — that's `distillation/`
- **Shrinking** the weights after training — that's `quantization/`
- **Looking things up** at inference time instead of storing them — that's `retrieval/`
- **Running** the model on real hardware — that's `inference/`

If you're adding a new architectural idea (a new positional encoding, a new block type), it lives here as a self-contained module with its own file, and gets wired into the main forward pass — it does not get bolted onto an existing file that wasn't built for it.

## Subdirectories
- `attention/` — attention mechanism variants
- `moe/` — mixture-of-experts routing and expert modules

## Design constraint
Every architectural choice here should be justifiable on **capability-per-parameter** grounds, not just "this is what everyone else does." If a component doesn't earn its parameter budget, it doesn't belong in Mendel. Cite the tradeoff in the module's own README when you add something non-obvious.
