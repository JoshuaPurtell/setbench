# Dragon Frontiers

This directory is the source-of-truth Dragon Frontiers family in SetBench.

## Status

Dragon Frontiers now has:

- gold files copied from `setbench-engine-core`
- a matching stub surface
- a curriculum manifest for `0pct`, `30pct`, and `80pct`
- a public train replay slice aligned with the hidden event-log scenarios
- broad hidden import-spec and runtime-hook coverage on top of the hidden event-log eval

The public train surface now matches the hidden dynamic replay scenarios. Hidden eval
still goes further by checking import-spec completeness and direct runtime-hook behavior
that does not need to be agent-visible.

The hidden suite now also checks:

- full attack import-spec coverage
- full power/body import-spec coverage
- trainer effect coverage
- runtime hook coverage for attack modifiers, Shining Horn gating, energy overrides,
  energy-attachment hooks, between-turn effects, power locks, and trigger registration

Remaining expansion work is:

- add more dynamic power/trainer event-log scenarios, not just hook/unit coverage
- tighten eventual export packaging for Terminal Bench
