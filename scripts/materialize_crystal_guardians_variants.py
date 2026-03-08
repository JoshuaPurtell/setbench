#!/usr/bin/env python3

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FAMILY = ROOT / "crystal_guardians"
SOURCE = FAMILY / "source"
VARIANTS = FAMILY / "variants"


def extract_pub_blocks(text: str) -> dict[str, str]:
    lines = text.splitlines(keepends=True)
    blocks: dict[str, str] = {}
    i = 0
    while i < len(lines):
        line = lines[i]
        match = re.match(r"pub fn ([A-Za-z0-9_]+)\s*\(", line)
        if not match:
            i += 1
            continue

        name = match.group(1)
        start = i
        brace_depth = line.count("{") - line.count("}")
        i += 1
        while i < len(lines):
            brace_depth += lines[i].count("{") - lines[i].count("}")
            i += 1
            if brace_depth <= 0:
                break
        blocks[name] = "".join(lines[start:i])
    return blocks


def replace_blocks(base_text: str, replacements: dict[str, str]) -> str:
    result = base_text
    for name, replacement in replacements.items():
        pattern = re.compile(
            rf"^pub fn {re.escape(name)}\s*\(.*?^\}}$\n?",
            re.MULTILINE | re.DOTALL,
        )
        result, count = pattern.subn(replacement.rstrip("\n") + "\n", result, count=1)
        if count != 1:
            raise RuntimeError(f"expected to replace exactly one block for {name}")
    return result


def write_variant(variant: str, all_cards_text: str, cg_engine_text: str) -> None:
    out_dir = VARIANTS / variant
    (out_dir / "all_cards.rs").write_text(all_cards_text)
    (out_dir / "cg_engine.rs").write_text(cg_engine_text)


def main() -> None:
    gold_all_cards = (SOURCE / "gold" / "all_cards.rs").read_text()
    gold_cg_engine = (SOURCE / "gold" / "cg_engine.rs").read_text()
    stub_all_cards = (SOURCE / "stubs" / "all_cards.rs").read_text()
    stub_cg_engine = (SOURCE / "stubs" / "cg_engine.rs").read_text()

    gold_all_blocks = extract_pub_blocks(gold_all_cards)
    gold_cg_blocks = extract_pub_blocks(gold_cg_engine)
    stub_all_blocks = extract_pub_blocks(stub_all_cards)
    stub_cg_blocks = extract_pub_blocks(stub_cg_engine)

    write_variant("0pct", stub_all_cards, stub_cg_engine)

    reveal_30_all = {
        "power_effect_ast",
        "trainer_effect_ast",
        "attack_effect_ast",
        "power_effect_id",
        "power_is_once_per_turn",
        "attack_cost_modifier",
    }
    reveal_30_cg = {"is_double_rainbow"}
    repl_30_all = {name: stub_all_blocks[name] for name in gold_all_blocks if name not in reveal_30_all}
    repl_30_cg = {name: stub_cg_blocks[name] for name in gold_cg_blocks if name not in reveal_30_cg}
    write_variant(
        "30pct",
        replace_blocks(gold_all_cards, repl_30_all),
        replace_blocks(gold_cg_engine, repl_30_cg),
    )

    hidden_80_all = {"attack_overrides", "post_attack", "execute_power", "resolve_custom_prompt"}
    hidden_80_cg = {"prevents_attack_effects"}
    repl_80_all = {name: stub_all_blocks[name] for name in hidden_80_all}
    repl_80_cg = {name: stub_cg_blocks[name] for name in hidden_80_cg}
    write_variant(
        "80pct",
        replace_blocks(gold_all_cards, repl_80_all),
        replace_blocks(gold_cg_engine, repl_80_cg),
    )


if __name__ == "__main__":
    main()
