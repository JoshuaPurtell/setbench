#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json

from setbench_family import load_family, run_suite


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--variant", required=True, choices=["0pct", "30pct", "80pct"])
    parser.add_argument("--subject", required=True, choices=["gold", "variant"])
    parser.add_argument("--suite", required=True, choices=["train", "hidden"])
    args = parser.parse_args()

    result = run_suite(
        load_family("crystal_guardians"),
        variant=args.variant,
        subject=args.subject,
        suite=args.suite,
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
