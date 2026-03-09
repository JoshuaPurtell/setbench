# Holon Phantoms Scope

Holon Phantoms is structurally scaffoldable, but it is not yet an eval-ready candidate.

## Code currently present in setbench-engine-core

- `scaffold/src/hp/import_specs.rs`
- `scaffold/src/hp/runtime.rs`
- `scaffold/src/hp/mod.rs`
- `scaffold/src/hp/cards/mod.rs`

Those files are placeholders today, not a mature reference implementation.

Concrete gap versus an eval-ready family such as Dragon Frontiers:

- Holon Phantoms has `1` file under `scaffold/src/hp/cards/` and that file is only a placeholder module comment.
- Dragon Frontiers has `84` card implementation files under `scaffold/src/df/cards/`.
- `hp/import_specs.rs` exports empty `HP_POWERS` and `HP_TRAINERS` tables and returns `None` for every AST lookup.
- `hp/runtime.rs` returns defaults or no-ops for every runtime hook.

## Current status in setbench

- the family skeleton exists at `holon_phantoms`
- placeholder gold and stub files are copied from the current engine-core tip
- the family is blocked on a real reference implementation, train fixtures, held-out fixtures, and eval runners

## Practical implication

Holon Phantoms should not be treated as eval-ready until there is a real reference implementation to benchmark against. Right now it is a structural placeholder, not a finished third benchmark.

## Minimum engine-core work before setbench can continue

- implement a non-placeholder `scaffold/src/hp/cards/` surface
- populate `hp/import_specs.rs` with real power, trainer, and attack spec tables
- implement non-trivial behavior in `hp/runtime.rs` for attacks, powers, prompts, and triggers
- only after that should `setbench` add train scenarios, hidden held-out scenarios, and local runners for HP
