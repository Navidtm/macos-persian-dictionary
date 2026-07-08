"""Validation for word entry dictionaries.

This intentionally does NOT depend on the third-party `jsonschema` package
so that contributors can validate and build entries with nothing more than
a stock Python 3 install. The rules here mirror
``data/schema/word.schema.json`` -- if you change one, change the other.
"""
from __future__ import annotations

from typing import List

REQUIRED_ENTRY_FIELDS = ("word", "parts_of_speech")
REQUIRED_SENSE_FIELDS = ("translations", "definition_en")
REQUIRED_EXAMPLE_FIELDS = ("en", "fa")
REQUIRED_RELATED_FIELDS = ("word", "translation")
REQUIRED_IDIOM_FIELDS = ("phrase", "translation")

VALID_LEVELS = {"A1", "A2", "B1", "B2", "C1", "C2"}


def _err(errors: List[str], where: str, message: str) -> None:
    errors.append(f"{where}: {message}")


def validate_entry(entry: dict, where: str = "<entry>") -> List[str]:
    """Return a list of human-readable error strings. Empty list == valid."""
    errors: List[str] = []

    if not isinstance(entry, dict):
        return [f"{where}: top-level JSON must be an object"]

    for field in REQUIRED_ENTRY_FIELDS:
        if field not in entry:
            _err(errors, where, f"missing required field '{field}'")

    word = entry.get("word")
    if word is not None and (not isinstance(word, str) or not word.strip()):
        _err(errors, where, "'word' must be a non-empty string")

    level = entry.get("level")
    if level is not None and level not in VALID_LEVELS:
        _err(errors, where, f"'level' must be one of {sorted(VALID_LEVELS)}, got {level!r}")

    pos_list = entry.get("parts_of_speech")
    if pos_list is not None:
        if not isinstance(pos_list, list) or len(pos_list) == 0:
            _err(errors, where, "'parts_of_speech' must be a non-empty array")
        else:
            for i, pos in enumerate(pos_list):
                _validate_pos(pos, f"{where} > parts_of_speech[{i}]", errors)

    for i, related in enumerate(entry.get("related_words", []) or []):
        for field in REQUIRED_RELATED_FIELDS:
            if field not in related:
                _err(errors, f"{where} > related_words[{i}]", f"missing required field '{field}'")

    for i, idiom in enumerate(entry.get("idioms", []) or []):
        for field in REQUIRED_IDIOM_FIELDS:
            if field not in idiom:
                _err(errors, f"{where} > idioms[{i}]", f"missing required field '{field}'")

    return errors


def _validate_pos(pos: dict, where: str, errors: List[str]) -> None:
    if not isinstance(pos, dict):
        _err(errors, where, "must be an object")
        return

    if "type" not in pos or not str(pos.get("type", "")).strip():
        _err(errors, where, "missing required field 'type' (e.g. 'noun', 'verb')")

    senses = pos.get("senses")
    if not senses or not isinstance(senses, list):
        _err(errors, where, "must contain a non-empty 'senses' array")
        return

    for j, sense in enumerate(senses):
        sense_where = f"{where} > senses[{j}]"
        if not isinstance(sense, dict):
            _err(errors, sense_where, "must be an object")
            continue
        for field in REQUIRED_SENSE_FIELDS:
            if field not in sense:
                _err(errors, sense_where, f"missing required field '{field}'")

        translations = sense.get("translations")
        if translations is not None and (not isinstance(translations, list) or len(translations) == 0):
            _err(errors, sense_where, "'translations' must be a non-empty array of strings")

        for k, example in enumerate(sense.get("examples", []) or []):
            example_where = f"{sense_where} > examples[{k}]"
            if not isinstance(example, dict):
                _err(errors, example_where, "must be an object")
                continue
            for field in REQUIRED_EXAMPLE_FIELDS:
                if field not in example:
                    _err(errors, example_where, f"missing required field '{field}'")
