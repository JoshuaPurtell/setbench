#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ENGINE_CORE_REPO = ROOT.parent / "setbench-engine-core"
FAMILY = ROOT / "crystal_guardians"
SOURCE = FAMILY / "source"
VARIANTS = FAMILY / "variants"
TARGET_ROOT = ROOT / ".cache" / "cargo-target"


def run(cmd: list[str], *, cwd: Path | None = None, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def read_engine_pin() -> str:
    pin_path = ROOT / "engine_core_pin.toml"
    text = pin_path.read_text()
    match = re.search(r'^commit = "([0-9a-f]+)"$', text, re.MULTILINE)
    if not match:
        raise RuntimeError(f"could not parse engine core commit from {pin_path}")
    return match.group(1)


def archive_engine_core(commit: str, out_dir: Path) -> None:
    if not ENGINE_CORE_REPO.exists():
        raise RuntimeError(f"missing engine core repo at {ENGINE_CORE_REPO}")
    archive = subprocess.Popen(
        ["git", "-C", str(ENGINE_CORE_REPO), "archive", commit],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=False,
    )
    extract = subprocess.run(
        ["tar", "-xf", "-", "-C", str(out_dir)],
        stdin=archive.stdout,
        capture_output=True,
        text=False,
        check=False,
    )
    if archive.stdout:
        archive.stdout.close()
    stderr = archive.stderr.read().decode() if archive.stderr else ""
    archive_rc = archive.wait()
    if archive_rc != 0:
        raise RuntimeError(f"git archive failed for {commit}: {stderr.strip()}")
    if extract.returncode != 0:
        raise RuntimeError(f"tar extract failed: {extract.stderr.decode().strip()}")


def patch_runtime_paths(text: str, app_dir: Path, tests_dir: Path) -> str:
    return (
        text.replace('include_str!("/app/', f'include_str!("{app_dir}/')
        .replace('include_str!("/tests/', f'include_str!("{tests_dir}/')
        .replace('const GOLD_PATH: &str = "/app/', f'const GOLD_PATH: &str = "{app_dir}/')
    )


def install_eval_source(all_cards_path: Path, base_all_cards: Path, eval_runtime: Path, app_dir: Path, tests_dir: Path) -> None:
    patched_runtime = patch_runtime_paths(eval_runtime.read_text(), app_dir, tests_dir)
    all_cards_path.write_text(
        base_all_cards.read_text()
        + "\n\n// ============================================================================\n"
        + "// SETBENCH EVALUATION TESTS (injected at runtime)\n"
        + "// ============================================================================\n\n"
        + patched_runtime
    )


def static_todo_hits(*paths: Path) -> int:
    hits = 0
    for path in paths:
        hits += path.read_text().count("SETBENCH_TODO")
    return hits


def extract_summary(output: str) -> tuple[int, int]:
    match = re.search(r"SETBENCH_SUMMARY matched=(\d+) total=(\d+)", output)
    if not match:
        return 0, 0
    return int(match.group(1)), int(match.group(2))


def copy_tree(src: Path, dst: Path) -> None:
    if src.is_dir():
        shutil.copytree(src, dst, dirs_exist_ok=True)
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def build_workspace(temp_root: Path) -> tuple[Path, Path]:
    app_dir = temp_root / "app"
    tests_dir = temp_root / "tests"
    app_dir.mkdir(parents=True, exist_ok=True)
    tests_dir.mkdir(parents=True, exist_ok=True)
    archive_engine_core(read_engine_pin(), app_dir)

    copy_tree(SOURCE / "public" / "data", app_dir / "setbench_data")
    copy_tree(SOURCE / "public" / "train", tests_dir / "train")
    copy_tree(SOURCE / "hidden", tests_dir / ".hidden")
    copy_tree(SOURCE / "gold", tests_dir / ".hidden" / "gold")

    return app_dir, tests_dir


def select_subject_paths(subject: str, variant: str) -> tuple[Path, Path]:
    if subject == "gold":
        return SOURCE / "gold" / "all_cards.rs", SOURCE / "gold" / "cg_engine.rs"
    return VARIANTS / variant / "all_cards.rs", VARIANTS / variant / "cg_engine.rs"


def run_hidden_suite(app_dir: Path, tests_dir: Path, variant: str, subject: str) -> dict[str, object]:
    all_cards_path = app_dir / "scaffold" / "src" / "cg" / "all_cards.rs"
    cg_engine_path = app_dir / "tcg_core" / "src" / "cg_engine.rs"
    gold_all_cards = SOURCE / "gold" / "all_cards.rs"
    gold_cg_engine = SOURCE / "gold" / "cg_engine.rs"
    eval_runtime = SOURCE / "hidden" / "heldout_runtime_eval.rs"
    scenario_fixture = SOURCE / "hidden" / "heldout_scenarios.json"
    candidate_all_cards, candidate_cg_engine = select_subject_paths(subject, variant)
    gold_fixture = tests_dir / ".hidden" / "generated_gold.json"

    expected_games = scenario_fixture.read_text().count('"name"')
    todo_hits = static_todo_hits(candidate_all_cards, candidate_cg_engine)
    result: dict[str, object] = {
        "suite": "hidden",
        "variant": variant,
        "subject": subject,
        "static_ok": 1 if todo_hits == 0 else 0,
        "compile_ok": 0,
        "games_matched": 0,
        "games_total": expected_games,
        "score": 0.0,
    }
    if todo_hits:
        result["todo_hits"] = todo_hits
        return result

    install_eval_source(all_cards_path, gold_all_cards, eval_runtime, app_dir, tests_dir)
    shutil.copy2(gold_cg_engine, cg_engine_path)
    env = os.environ.copy()
    env["CARGO_TARGET_DIR"] = str(TARGET_ROOT / f"cg-hidden-{variant}-{subject}")
    env["SETBENCH_GOLD_OUTPUT"] = str(gold_fixture)
    gold = run(
        [
            "cargo",
            "test",
            "--package",
            "tcg_expansions",
            "setbench_eventlog_write_gold_fixture",
            "--",
            "--ignored",
            "--nocapture",
        ],
        cwd=app_dir,
        env=env,
    )
    result["gold_stdout"] = gold.stdout
    result["gold_stderr"] = gold.stderr
    if gold.returncode != 0 or not gold_fixture.exists():
        result["gold_ok"] = 0
        return result
    result["gold_ok"] = 1

    install_eval_source(all_cards_path, candidate_all_cards, eval_runtime, app_dir, tests_dir)
    shutil.copy2(candidate_cg_engine, cg_engine_path)

    compile_env = os.environ.copy()
    compile_env["CARGO_TARGET_DIR"] = env["CARGO_TARGET_DIR"]
    compile_proc = run(["cargo", "check", "--package", "tcg_expansions"], cwd=app_dir, env=compile_env)
    result["compile_stdout"] = compile_proc.stdout
    result["compile_stderr"] = compile_proc.stderr
    if compile_proc.returncode != 0:
        return result
    result["compile_ok"] = 1

    eval_env = os.environ.copy()
    eval_env["CARGO_TARGET_DIR"] = env["CARGO_TARGET_DIR"]
    eval_env["SETBENCH_GOLD_PATH"] = str(gold_fixture)
    suite_proc = run(
        [
            "cargo",
            "test",
            "--package",
            "tcg_expansions",
            "setbench_eval_suite",
            "--",
            "--test-threads=1",
            "--nocapture",
        ],
        cwd=app_dir,
        env=eval_env,
    )
    result["suite_stdout"] = suite_proc.stdout
    result["suite_stderr"] = suite_proc.stderr
    matched, total = extract_summary(suite_proc.stdout + "\n" + suite_proc.stderr)
    if total:
        result["games_total"] = total
    result["games_matched"] = matched
    if result["games_total"]:
        result["score"] = round(matched / int(result["games_total"]), 4)
    return result


def run_train_suite(app_dir: Path, tests_dir: Path, variant: str, subject: str) -> dict[str, object]:
    all_cards_path = app_dir / "scaffold" / "src" / "cg" / "all_cards.rs"
    cg_engine_path = app_dir / "tcg_core" / "src" / "cg_engine.rs"
    gold_all_cards = SOURCE / "gold" / "all_cards.rs"
    gold_cg_engine = SOURCE / "gold" / "cg_engine.rs"
    eval_runtime = SOURCE / "public" / "train" / "train_runtime_eval.rs"
    scenario_fixture = SOURCE / "public" / "train" / "train_scenarios.json"
    candidate_all_cards, candidate_cg_engine = select_subject_paths(subject, variant)
    gold_fixture = tests_dir / "train" / "generated_train_gold.json"

    expected_games = scenario_fixture.read_text().count('"name"')
    todo_hits = static_todo_hits(candidate_all_cards, candidate_cg_engine)
    result: dict[str, object] = {
        "suite": "train",
        "variant": variant,
        "subject": subject,
        "static_ok": 1 if todo_hits == 0 else 0,
        "compile_ok": 0,
        "games_matched": 0,
        "games_total": expected_games,
        "score": 0.0,
    }
    if todo_hits:
        result["todo_hits"] = todo_hits
        return result

    install_eval_source(all_cards_path, gold_all_cards, eval_runtime, app_dir, tests_dir)
    shutil.copy2(gold_cg_engine, cg_engine_path)
    env = os.environ.copy()
    env["CARGO_TARGET_DIR"] = str(TARGET_ROOT / f"cg-train-{variant}-{subject}")
    env["SETBENCH_GOLD_OUTPUT"] = str(gold_fixture)
    gold = run(
        [
            "cargo",
            "test",
            "--package",
            "tcg_expansions",
            "setbench_eventlog_write_gold_fixture",
            "--",
            "--ignored",
            "--nocapture",
        ],
        cwd=app_dir,
        env=env,
    )
    result["gold_stdout"] = gold.stdout
    result["gold_stderr"] = gold.stderr
    if gold.returncode != 0 or not gold_fixture.exists():
        result["gold_ok"] = 0
        return result
    result["gold_ok"] = 1

    install_eval_source(all_cards_path, candidate_all_cards, eval_runtime, app_dir, tests_dir)
    shutil.copy2(candidate_cg_engine, cg_engine_path)

    compile_env = os.environ.copy()
    compile_env["CARGO_TARGET_DIR"] = env["CARGO_TARGET_DIR"]
    compile_proc = run(["cargo", "check", "--package", "tcg_expansions"], cwd=app_dir, env=compile_env)
    result["compile_stdout"] = compile_proc.stdout
    result["compile_stderr"] = compile_proc.stderr
    if compile_proc.returncode != 0:
        return result
    result["compile_ok"] = 1

    eval_env = os.environ.copy()
    eval_env["CARGO_TARGET_DIR"] = env["CARGO_TARGET_DIR"]
    eval_env["SETBENCH_GOLD_PATH"] = str(gold_fixture)
    suite_proc = run(
        [
            "cargo",
            "test",
            "--package",
            "tcg_expansions",
            "setbench_train_suite",
            "--",
            "--test-threads=1",
            "--nocapture",
        ],
        cwd=app_dir,
        env=eval_env,
    )
    result["suite_stdout"] = suite_proc.stdout
    result["suite_stderr"] = suite_proc.stderr
    matched, total = extract_summary(suite_proc.stdout + "\n" + suite_proc.stderr)
    if total:
        result["games_total"] = total
    result["games_matched"] = matched
    if result["games_total"]:
        result["score"] = round(matched / int(result["games_total"]), 4)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--variant", choices=["0pct", "30pct", "80pct"], default="0pct")
    parser.add_argument("--subject", choices=["variant", "gold"], default="gold")
    parser.add_argument("--suite", choices=["train", "hidden"], default="hidden")
    parser.add_argument("--keep-workdir", action="store_true")
    args = parser.parse_args()

    temp_dir_obj = tempfile.TemporaryDirectory(prefix="setbench-full-cg-")
    temp_root = Path(temp_dir_obj.name)
    try:
        TARGET_ROOT.mkdir(parents=True, exist_ok=True)
        app_dir, tests_dir = build_workspace(temp_root)
        if args.suite == "hidden":
            result = run_hidden_suite(app_dir, tests_dir, args.variant, args.subject)
        else:
            result = run_train_suite(app_dir, tests_dir, args.variant, args.subject)
        result["workdir"] = str(temp_root)
        print(json.dumps(result, indent=2))
        return 0
    finally:
        if args.keep_workdir:
            temp_dir_obj.cleanup = lambda: None  # type: ignore[method-assign]
            print(f"kept workdir at {temp_root}", file=sys.stderr)
        else:
            temp_dir_obj.cleanup()


if __name__ == "__main__":
    raise SystemExit(main())
