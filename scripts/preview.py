#!/usr/bin/env python3
"""Generate a plain-HTML preview of dictionary entries.

Dictionary.app itself is only available on macOS, and compiling a real
`.dictionary` bundle needs Apple's Dictionary Development Kit. To make
design review possible for everyone (any OS, any browser, no extra
tooling), this script renders the same entry markup used in the real
build into a standalone HTML file that links the real project CSS.

Usage:
    python3 scripts/preview.py                  # preview every word
    python3 scripts/preview.py patience journey  # preview only these words

Output:
    build/preview.html
"""
from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))

from lib.dataset import REPO_ROOT, load_all_words  # noqa: E402
from lib.xml_render import render_entry  # noqa: E402

BUILD_DIR = os.path.join(REPO_ROOT, "build")
CSS_PATH = os.path.join(REPO_ROOT, "resources", "style", "EnglishPersianDictionary.css")

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>English -&gt; Persian Dictionary — Preview</title>
<style>
  body {{
    margin: 0;
    padding: 32px;
    background: #f5f5f7;
  }}
  .preview-card {{
    max-width: 640px;
    margin: 0 auto 24px auto;
    background: #ffffff;
    border-radius: 12px;
    padding: 24px 28px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
  }}
  .preview-heading {{
    max-width: 640px;
    margin: 0 auto 16px auto;
    font-family: -apple-system, Helvetica, Arial, sans-serif;
    color: #6e6e73;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
  }}
{css}
</style>
</head>
<body>
{cards}
</body>
</html>
"""

# The renderer wraps <d:entry> around the content and adds <d:index>
# elements, which are meaningless in plain HTML. Strip those wrapper tags
# and keep only the inner <div class="entry">...</div> markup.
ENTRY_INNER_RE = re.compile(r"<d:entry[^>]*>(?:<d:index[^/]*/>)*(.*)</d:entry>", re.DOTALL)


def extract_inner_html(entry_xml: str) -> str:
    match = ENTRY_INNER_RE.search(entry_xml)
    return match.group(1) if match else entry_xml


def main() -> int:
    requested = {w.lower() for w in sys.argv[1:]}
    entries = load_all_words()

    if requested:
        entries = [e for e in entries if e.data.get("word", "").lower() in requested]
        if not entries:
            print(f"No matching words found for: {', '.join(sorted(requested))}", file=sys.stderr)
            return 1

    with open(CSS_PATH, "r", encoding="utf-8") as f:
        css = f.read()

    cards = []
    for word_entry in entries:
        inner_html = extract_inner_html(render_entry(word_entry.data))
        cards.append(f'<div class="preview-card">{inner_html}</div>')

    heading = f'<div class="preview-heading">Preview &middot; {len(entries)} entries</div>'
    html = HTML_TEMPLATE.format(css=css, cards=heading + "\n" + "\n".join(cards))

    os.makedirs(BUILD_DIR, exist_ok=True)
    out_path = os.path.join(BUILD_DIR, "preview.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Wrote {out_path} ({len(entries)} entries) -- open it in any browser.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
