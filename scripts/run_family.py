#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json

from setbench_family import load_family, run_suite


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--family", required=True)
    parser.add_argument("--variant", required=True)
    parser.add_argument("--subject", required=True, choices=["gold", "variant"])
    parser.add_argument("--suite", required=True, choices=["train", "hidden"])
    args = parser.parse_args()

    family = load_family(args.family)
    result = run_suite(
        family,
        variant=args.variant,
        subject=args.subject,
        suite=args.suite,
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
