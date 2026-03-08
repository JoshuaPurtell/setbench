#!/usr/bin/env python3

from __future__ import annotations

import argparse

from setbench_family import load_family, materialize_all_variants, materialize_variant


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--family", required=True)
    parser.add_argument("--variant")
    args = parser.parse_args()

    family = load_family(args.family)
    if args.variant:
        print(materialize_variant(family, args.variant))
        return

    for out_dir in materialize_all_variants(family):
        print(out_dir)


if __name__ == "__main__":
    main()
