# Dragon Frontiers Scope

Dragon Frontiers is the next clean candidate for a SetBench family because the reference implementation already exists in `setbench-engine-core`.

## Code already present in setbench-engine-core

- `scaffold/src/df/import_specs.rs`
- `scaffold/src/df/runtime.rs`
- `scaffold/src/df/helpers.rs`
- `scaffold/src/df/mod.rs`

## Current status in setbench

- gold files are copied into `dragon_frontiers/source/gold`
- a matching stub surface and curriculum manifest exist in `dragon_frontiers`
- the family is still blocked on public train fixtures, hidden held-out fixtures, and eval runners

## Practical implication

Dragon Frontiers should be materially easier to stand up than a brand new set because the shared engine repo already has a mature reference implementation. The remaining work is benchmark extraction, scenario design, and curriculum slicing, not engine invention.
