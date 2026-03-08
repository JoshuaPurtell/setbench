#!/usr/bin/env python3

from __future__ import annotations

from setbench_family import load_family, materialize_all_variants


def main() -> None:
    materialize_all_variants(load_family("crystal_guardians"))


if __name__ == "__main__":
    main()
