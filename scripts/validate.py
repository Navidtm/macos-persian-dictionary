#!/usr/bin/env python3
"""Validate every word entry in data/words/ without building the dictionary.

Usage:
    python3 scripts/validate.py

Exits with status 1 and prints a list of problems if any entry is invalid,
so this is safe to use as a pre-commit hook or CI step.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from lib.dataset import load_all_words  # noqa: E402
from lib.validate import validate_entry  # noqa: E402


def main() -> int:
    entries = load_all_words()
    if not entries:
        print("ERROR: no word entries found in data/words/", file=sys.stderr)
        return 1

    all_errors = []
    seen = {}
    for word_entry in entries:
        all_errors.extend(validate_entry(word_entry.data, where=word_entry.path))
        word = word_entry.data.get("word")
        if word:
            key = word.strip().lower()
            if key in seen:
                all_errors.append(
                    f"{word_entry.path}: duplicate headword '{word}' (also in {seen[key]})"
                )
            seen[key] = word_entry.path

    if all_errors:
        print(f"{len(all_errors)} problem(s) found:\n", file=sys.stderr)
        for error in all_errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    print(f"All {len(entries)} word entries are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
