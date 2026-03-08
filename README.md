# SetBench Full

Internal source-of-truth repo for full SetBench benchmark families and partial-gold curricula.

This repo exists to keep benchmark-generation assets separate from both the shared engine and the public packaged tasks.

## Boundary

- `setbench-engine-core` owns reusable engine/runtime/scaffold code.
- `setbench-full` owns benchmark families, gold/stub pairs, train/held-out fixtures, and partial-gold curricula such as `0pct`, `30pct`, and `80pct`.
- `terminal-bench-3` owns only exported packaged tasks.

`terminal-bench-3` must never import this repo directly.

If a TB3 task needs shared engine code, it must pin an exact `setbench-engine-core` commit. It must not pull `setbench-full`, and it must not transitively depend on any `setbench-full` layout.

## Current contents

- `crystal_guardians/`: benchmark family source and curriculum variants.
- `roadmap/`: scoping notes for future benchmark families.
- `scripts/`: local materializers for deriving task variants from the benchmark source.

## Export intent

The long-term flow is:

1. Author and maintain benchmark families here.
2. Pin `setbench-engine-core` explicitly.
3. Materialize one packaged task variant for Terminal Bench.
4. Copy only the packaged artifact into `terminal-bench-3`.

The packaged TB3 task should stay narrowly scoped, cleanly additive, and benchmark-only.
