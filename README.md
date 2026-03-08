# SetBench Full

Internal source-of-truth repo for full SetBench benchmark families and partial-gold curricula.

This repo exists to keep benchmark-generation assets separate from both the shared engine and the public packaged tasks.

## Boundary

- `setbench-engine-core` owns reusable engine/runtime/scaffold code.
- `setbench-full` owns benchmark families, gold/stub pairs, train/held-out fixtures, and partial-gold curricula such as `0pct`, `30pct`, and `80pct`.
- `terminal-bench-3` owns only exported packaged tasks.

`terminal-bench-3` must never import this repo directly.

If a TB3 task needs shared engine code, it must pin an exact `setbench-engine-core` commit. It must not pull `setbench-full`, and it must not transitively depend on any `setbench-full` layout.

## Split

There are two different splits that matter in this repo.

1. Repo split

- `setbench-engine-core`: shared engine and scaffold only
- `setbench-full`: benchmark family source material and curriculum variants
- `terminal-bench-3`: exported benchmark task packages only

2. Within each benchmark family

- `source/`: canonical source-of-truth assets
- `variants/`: derived disclosure tiers such as `0pct`, `30pct`, and `80pct`

The intended workflow is:

1. maintain canonical family assets in `source/`
2. derive curriculum tiers into `variants/`
3. export exactly one packaged task variant into `terminal-bench-3`

## Current contents

- `crystal_guardians/`: benchmark family source and curriculum variants.
- `roadmap/`: scoping notes for future benchmark families.
- `scripts/`: local materializers for deriving task variants from the benchmark source.

## Local execution

The repo includes a local Crystal Guardians runner:

```bash
cd /Users/joshpurtell/Documents/GitHub/setbench-full
./scripts/run_crystal_guardians.py --variant 0pct --subject gold --suite hidden
```

That runner:

1. archives the pinned `setbench-engine-core` commit into a temporary workspace
2. overlays the chosen Crystal Guardians variant
3. generates event-log gold from the two gold files at runtime
4. runs the requested suite against the staged workspace

## Export intent

The long-term flow is:

1. Author and maintain benchmark families here.
2. Pin `setbench-engine-core` explicitly.
3. Materialize one packaged task variant for Terminal Bench.
4. Copy only the packaged artifact into `terminal-bench-3`.

The packaged TB3 task should stay narrowly scoped, cleanly additive, and benchmark-only.
