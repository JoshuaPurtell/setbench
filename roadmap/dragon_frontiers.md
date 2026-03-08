# Dragon Frontiers Scope

Dragon Frontiers is the next clean candidate for a SetBench family because the reference implementation already exists in `setbench-engine-core`.

## Code already present in setbench-engine-core

- `scaffold/src/df/import_specs.rs`
- `scaffold/src/df/runtime.rs`
- `scaffold/src/df/helpers.rs`
- `scaffold/src/df/mod.rs`

## What a DF benchmark family still needs

- a gold/stub split for the graded files
- public train scenarios and a visible runner
- hidden held-out scenarios and a hidden runner
- task-level instructions and export metadata
- a curriculum policy for `0pct`, `30pct`, and `80pct`

## Practical implication

Dragon Frontiers should be materially easier to stand up than a brand new set because the shared engine repo already has a mature reference implementation. The main work is benchmark extraction, scenario design, and curriculum slicing, not engine invention.
