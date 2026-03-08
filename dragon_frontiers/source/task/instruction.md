# SetBench V1: Dragon Frontiers Attack Slice

Implement the Dragon Frontiers attack slice for the provided Rust Pokemon TCG engine.

Edit exactly these files:
- `/app/scaffold/src/df/import_specs.rs`
- `/app/scaffold/src/df/runtime.rs`

Use these references while you work:
- `/tests/train/train_scenarios.json`
- `/tests/train/train.sh`

The current benchmark slice is intentionally narrow. It focuses on deterministic
event-log reproduction for these Dragon Frontiers attacks:
- `DF-3` Heracross δ: `Extra Claws`
- `DF-7` Nidoqueen δ: `Vengeance`
- `DF-15` Dewgong δ: `Surge`
- `DF-32` Kirlia: `Link Blast`
- `DF-35` Nidorino δ: `Rage`
- `DF-49` Feebas δ: `Flail`
- `DF-60` Ralts: `Psychic Boom`
- `DF-65` Swablu δ: `Splash About`

The visible train loop should generate gold from the family gold files at runtime and
then compare the candidate output against that gold on the published train scenarios.
