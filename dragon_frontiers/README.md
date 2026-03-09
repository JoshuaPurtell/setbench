# Dragon Frontiers

This directory is the source-of-truth Dragon Frontiers family in SetBench.

## Status

Dragon Frontiers now has:

- gold files copied from `setbench-engine-core`
- a matching stub surface
- a curriculum manifest for `0pct`, `30pct`, and `80pct`
- an attack-focused public train slice
- broad hidden import-spec and runtime-hook coverage on top of the hidden event-log eval

The public train surface is still intentionally narrower than the hidden suite. It focuses
on deterministic attack/event-log behavior for a small set of DF attacks whose semantics
live in `import_specs.rs` and `runtime.rs`.

The hidden suite now also checks:

- full attack import-spec coverage
- full power/body import-spec coverage
- trainer effect coverage
- runtime hook coverage for attack modifiers, Shining Horn gating, energy overrides,
  energy-attachment hooks, between-turn effects, power locks, and trigger registration

Remaining expansion work is:

- broaden the visible train scenarios beyond the current attack-focused slice
- add more dynamic power/trainer event-log scenarios, not just hook/unit coverage
- tighten eventual export packaging for Terminal Bench
