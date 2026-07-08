#!/usr/bin/env python3
"""Build the Apple Dictionary Services XML source from data/words/*.json.

Usage:
    python3 scripts/build.py

Output:
    build/EnglishPersianDictionary.xml   - the compiled dictionary source
    build/EnglishPersianDictionary.css   - copied styling
    build/EnglishPersianDictionaryInfo.plist - copied bundle descriptor

This script does not invoke Apple's `build_dict.sh` (that step needs the
Dictionary Development Kit, which is only installable on macOS with Xcode's
optional components -- see README.md). It only prepares the inputs that
tool needs, so this step works on any platform with Python 3.
"""
from __future__ import annotations

import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(__file__))

from lib.dataset import REPO_ROOT, load_all_words  # noqa: E402
from lib.validate import validate_entry  # noqa: E402
from lib.xml_render import render_entry  # noqa: E402

BUILD_DIR = os.path.join(REPO_ROOT, "build")
RESOURCES_DIR = os.path.join(REPO_ROOT, "resources")
MATTER_DIR = os.path.join(RESOURCES_DIR, "matter")

DICTIONARY_NAME = "EnglishPersianDictionary"

XML_HEADER = """<?xml version="1.0" encoding="UTF-8"?>
<d:dictionary xmlns="http://www.w3.org/1999/xhtml" xmlns:d="http://www.apple.com/DTDs/DictionaryService-1.0.rng">
"""
XML_FOOTER = "</d:dictionary>\n"

CFBUNDLE_VERSION_RE = re.compile(
    r"(<key>CFBundleShortVersionString</key>\s*<string>)[^<]*(</string>)"
)


def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_plist(src: str, dst: str, version: str | None) -> None:
    """Copy the Info.plist template to the build directory.

    If DICT_VERSION is set in the environment (used by `make release`), the
    CFBundleShortVersionString value is replaced with it so a release ZIP's
    bundle version always matches its git tag. Everyday `make build` runs
    leave the plist untouched, so plain local builds are unaffected.
    """
    if not version:
        shutil.copyfile(src, dst)
        return

    contents = read_text(src)
    replaced, count = CFBUNDLE_VERSION_RE.subn(rf"\g<1>{version}\g<2>", contents)
    if count == 0:
        print(
            "WARNING: could not find CFBundleShortVersionString in the plist "
            "template; copying it unmodified.",
            file=sys.stderr,
        )
        replaced = contents
    with open(dst, "w", encoding="utf-8") as f:
        f.write(replaced)


def build_front_matter_entry() -> str:
    """The front matter entry is a normal <d:entry> that Dictionary.app can
    show as an introductory page. It is referenced by id from the Info.plist
    key `DCSDictionaryFrontMatterReferenceID`.
    """
    path = os.path.join(MATTER_DIR, "front_matter.html")
    body = read_text(path)
    return f'<d:entry id="front_back_matter" d:title="About This Dictionary">{body}</d:entry>'


def main() -> int:
    print(f"Loading word entries from data/words/ ...")
    entries = load_all_words()

    if not entries:
        print("ERROR: no word entries found in data/words/", file=sys.stderr)
        return 1

    # --- Validate --------------------------------------------------------
    all_errors = []
    seen_slugs = {}
    for word_entry in entries:
        errors = validate_entry(word_entry.data, where=word_entry.path)
        all_errors.extend(errors)

        word = word_entry.data.get("word")
        if word:
            slug = word.strip().lower()
            if slug in seen_slugs:
                all_errors.append(
                    f"{word_entry.path}: duplicate headword '{word}' "
                    f"(also defined in {seen_slugs[slug]})"
                )
            else:
                seen_slugs[slug] = word_entry.path

    if all_errors:
        print(f"\n{len(all_errors)} validation error(s) found:\n", file=sys.stderr)
        for error in all_errors:
            print(f"  - {error}", file=sys.stderr)
        print("\nBuild aborted. Fix the errors above and try again.", file=sys.stderr)
        return 1

    print(f"Validated {len(entries)} word entries. OK.")

    # --- Render ------------------------------------------------------------
    rendered_entries = [render_entry(we.data) for we in entries]
    rendered_entries.insert(0, build_front_matter_entry())

    xml_document = XML_HEADER + "\n".join(rendered_entries) + "\n" + XML_FOOTER

    os.makedirs(BUILD_DIR, exist_ok=True)
    xml_path = os.path.join(BUILD_DIR, f"{DICTIONARY_NAME}.xml")
    with open(xml_path, "w", encoding="utf-8") as f:
        f.write(xml_document)
    print(f"Wrote {xml_path}")

    # --- Copy static resources ---------------------------------------------
    css_src = os.path.join(RESOURCES_DIR, "style", f"{DICTIONARY_NAME}.css")
    css_dst = os.path.join(BUILD_DIR, f"{DICTIONARY_NAME}.css")
    shutil.copyfile(css_src, css_dst)
    print(f"Copied {css_dst}")

    plist_src = os.path.join(RESOURCES_DIR, "plist", f"{DICTIONARY_NAME}Info.plist")
    plist_dst = os.path.join(BUILD_DIR, f"{DICTIONARY_NAME}Info.plist")
    write_plist(plist_src, plist_dst, version=os.environ.get("DICT_VERSION"))
    print(f"Copied {plist_dst}")

    word_count = len(entries)
    sense_count = sum(
        len(pos.get("senses", []))
        for we in entries
        for pos in we.data.get("parts_of_speech", [])
    )
    print(f"\nDone: {word_count} words, {sense_count} senses, ready in build/.")
    print("Next: run `make package` on macOS (with the Dictionary Development")
    print("Kit installed) to compile build/ into a .dictionary bundle.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
