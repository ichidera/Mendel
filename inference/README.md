# inference/

Runs a trained, quantized Mendel checkpoint on real target hardware — the layer where architecture and math finally become an actual running process.

## Responsible for
- The runtime/serving loop: loading a checkpoint and executing forward passes efficiently on target hardware (phone, laptop, edge device, server)
- Hardware-specific execution paths, including the lower-level optimized kernels (this is where hand-tuned C/CUDA/SIMD work belongs, once it's needed — see note below)
- Memory management at inference time: KV-cache handling, batching, streaming token generation
- Precision-aware execution: correctly running whichever bit-width `quantization/` has produced for a given deployment target

## Not responsible for
- Defining the model architecture — that's `architecture/`, this directory executes whatever architecture it's handed
- Deciding what precision to quantize to — that's `quantization/`'s call, this directory just needs to support execution at whatever precision is chosen
- Anything upstream of "a trained, ready-to-run checkpoint exists" — training and shrinking happen elsewhere; this is the last mile

## Where low-level optimization belongs
This is the one directory in the repo where writing tight, hardware-specific code (SIMD intrinsics, CUDA kernels, hand-tuned assembly-adjacent code for the hottest inner loops) is actually the right lever to pull — after the model's *capability* has been established elsewhere. Speed optimizations here make a given amount of computation cheaper; they don't change how much the model knows. Don't confuse the two when deciding where a change belongs.

## Target-specific execution paths
Expect genuinely different code paths for phone/edge deployment vs. server deployment — they have different memory budgets, different available instruction sets, and different acceptable latency profiles. Keep those paths clearly separated rather than one execution path with branching conditionals sprinkled through it.
