# SetBench

Internal source-of-truth repo for full SetBench benchmark families and partial-gold curricula.

This repo exists to keep benchmark-generation assets separate from both the shared engine and the public packaged tasks.

## Boundary

- `setbench-engine-core` owns reusable engine/runtime/scaffold code.
- `setbench` owns benchmark families, gold/stub pairs, train/held-out fixtures, and partial-gold curricula such as `0pct`, `30pct`, and `80pct`.
- `terminal-bench-3` owns only exported packaged tasks.

`terminal-bench-3` must never import this repo directly.

If a TB3 task needs shared engine code, it must pin an exact `setbench-engine-core` commit. It must not pull `setbench`, and it must not transitively depend on any `setbench` layout.

## Split

There are two different splits that matter in this repo.

1. Repo split

- `setbench-engine-core`: shared engine and scaffold only
- `setbench`: benchmark family source material and curriculum variants
- `terminal-bench-3`: exported benchmark task packages only

2. Within each benchmark family

- `source/`: canonical source-of-truth assets
- `variants/`: derived disclosure tiers such as `0pct`, `30pct`, and `80pct`

The intended workflow is:

1. maintain canonical family assets in `source/`
2. derive curriculum tiers into `variants/`
3. export exactly one packaged task variant into `terminal-bench-3`

## Current contents

- `crystal_guardians/`: validated benchmark family source and curriculum variants.
- `dragon_frontiers/`: validated benchmark family source and curriculum variants.
- `holon_phantoms/`: blocked family scaffold that mirrors the current engine-core placeholder.
- `roadmap/`: scoping notes for future benchmark families.
- `scripts/`: manifest-driven local materializers and runners.

## Local execution

The repo includes manifest-driven local runners:

```bash
cd /Users/joshpurtell/Documents/GitHub/setbench-full
./scripts/run_family.py --family crystal_guardians --variant 0pct --subject gold --suite hidden
```

That runner:

1. archives the pinned `setbench-engine-core` commit into a temporary workspace
2. overlays the chosen family variant
3. generates event-log gold from the two gold files at runtime
4. runs the requested suite against the staged workspace

## Export intent

The long-term flow is:

1. Author and maintain benchmark families here.
2. Pin `setbench-engine-core` explicitly.
3. Materialize one packaged task variant for Terminal Bench.
4. Copy only the packaged artifact into `terminal-bench-3`.

The packaged TB3 task should stay narrowly scoped, cleanly additive, and benchmark-only.

## Family status

- `crystal_guardians`: ready and validated through the local runner.
- `dragon_frontiers`: ready and validated through the local runner, with aligned public and hidden replay surfaces plus hidden import/runtime coverage.
- `holon_phantoms`: scaffolded structurally, but blocked on a real reference implementation in `setbench-engine-core`.
