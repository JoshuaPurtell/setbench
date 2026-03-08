# Dragon Frontiers

This directory is the source-of-truth Dragon Frontiers family in SetBench.

## Status

Dragon Frontiers now has:

- gold files copied from `setbench-engine-core`
- a matching stub surface
- a curriculum manifest for `0pct`, `30pct`, and `80pct`
- a first runnable attack-centric train and hidden eval slice

This first slice focuses on deterministic attack/event-log behavior for a small set of
DF attacks whose semantics live in `import_specs.rs` and `runtime.rs`.

It is not complete set coverage yet. The next expansion work is:

- broaden the visible and held-out scenario sets
- add power/body-heavy scenarios on top of the attack slice
- tighten eventual export packaging for Terminal Bench
