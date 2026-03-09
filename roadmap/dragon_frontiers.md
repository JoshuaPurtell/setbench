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
- public train and hidden held-out replay runners are implemented
- public and hidden replay surfaces are aligned
- hidden eval additionally checks import-spec completeness and direct runtime hooks

## Practical implication

Dragon Frontiers is now a real benchmark family because the shared engine repo already has a mature reference implementation. Remaining work is depth and export polish, not basic family bring-up.
