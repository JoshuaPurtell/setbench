# Holon Phantoms Scope

Holon Phantoms is also a near-term candidate because the reference implementation already exists in `setbench-engine-core`.

## Code already present in setbench-engine-core

- `scaffold/src/hp/import_specs.rs`
- `scaffold/src/hp/runtime.rs`
- `scaffold/src/hp/mod.rs`

## What a HP benchmark family still needs

- a gold/stub split for the graded files
- public train and hidden held-out scenario suites
- visible and hidden deterministic runners
- partial-gold curriculum definitions
- export metadata for Terminal Bench packaging

## Practical implication

Like Dragon Frontiers, Holon Phantoms is already within the current engine scaffold boundary. That makes it a better next step than introducing a wholly new set family with no existing reference implementation.
