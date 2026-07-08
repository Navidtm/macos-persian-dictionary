"""Helpers for locating and loading word entry JSON files.

The dictionary's source of truth is a tree of small JSON files under
``data/words/<first-letter>/<word>.json``. This module is the single place
that knows how that tree is laid out, so build/validate/tooling scripts
never hard-code paths themselves.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Iterator

# Repository root = two levels up from this file (scripts/lib/dataset.py).
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
WORDS_DIR = os.path.join(REPO_ROOT, "data", "words")


def slugify(word: str) -> str:
    """Turn a headword into a safe file/id slug.

    Multi-word headwords (e.g. "give up") become hyphenated ("give-up"),
    which keeps this working cleanly as the dataset grows to phrasal verbs
    and multi-word expressions.
    """
    return word.strip().lower().replace(" ", "-")


@dataclass
class WordEntry:
    """A single loaded word entry plus the path it came from (for error
    messages)."""

    path: str
    data: dict


def iter_word_files(words_dir: str = WORDS_DIR) -> Iterator[str]:
    """Yield every *.json file under the words directory, sorted for
    deterministic build output."""
    if not os.path.isdir(words_dir):
        return
    for letter_dir in sorted(os.listdir(words_dir)):
        full_dir = os.path.join(words_dir, letter_dir)
        if not os.path.isdir(full_dir):
            continue
        for filename in sorted(os.listdir(full_dir)):
            if filename.endswith(".json"):
                yield os.path.join(full_dir, filename)


def load_word_file(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_all_words(words_dir: str = WORDS_DIR) -> list[WordEntry]:
    """Load every word entry, sorted alphabetically by headword."""
    entries = [
        WordEntry(path=path, data=load_word_file(path))
        for path in iter_word_files(words_dir)
    ]
    entries.sort(key=lambda e: e.data.get("word", ""))
    return entries
