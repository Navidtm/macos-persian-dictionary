#!/usr/bin/env python3
"""Scaffold a new word entry file.

Usage:
    python3 scripts/new_word.py <english-word>

Creates data/words/<first-letter>/<word>.json pre-filled with the entry
skeleton described in data/schema/word.schema.json, so a contributor only
has to fill in the blanks instead of remembering the whole structure.
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from lib.dataset import WORDS_DIR, slugify  # noqa: E402

TEMPLATE = {
    "word": "",
    "level": "B1",
    "parts_of_speech": [
        {
            "type": "noun",
            "ipa": "",
            "pronunciation_guide": "",
            "senses": [
                {
                    "translations": [""],
                    "definition_en": "",
                    "examples": [{"en": "", "fa": ""}],
                    "synonyms": [],
                    "antonyms": [],
                }
            ],
        }
    ],
    "related_words": [],
    "idioms": [],
    "notes": "",
}


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python3 scripts/new_word.py <english-word>", file=sys.stderr)
        return 1

    word = sys.argv[1].strip().lower()
    if not word:
        print("ERROR: word must not be empty", file=sys.stderr)
        return 1

    slug = slugify(word)
    letter = slug[0]
    directory = os.path.join(WORDS_DIR, letter)
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, f"{slug}.json")

    if os.path.exists(path):
        print(f"ERROR: {path} already exists.", file=sys.stderr)
        return 1

    entry = dict(TEMPLATE)
    entry["word"] = word

    with open(path, "w", encoding="utf-8") as f:
        json.dump(entry, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"Created {path}")
    print("Next steps:")
    print("  1. Fill in IPA, pronunciation guide, translations, and definitions.")
    print("  2. Add at least one example sentence with its Persian translation.")
    print("  3. Add synonyms/antonyms/related words/idioms where relevant.")
    print("  4. Run `python3 scripts/validate.py` to check your entry.")
    print("  5. Run `make build` to make sure it compiles into the XML source.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
