"""Render a single word entry (already validated) into the XML markup
expected by Apple's Dictionary Development Kit.

Apple's dictionary format is XHTML-ish content wrapped in <d:entry> /
<d:index> elements (namespace ``http://www.apple.com/DTDs/DictionaryService-1.0.rng``).
See: Dictionary Development Kit -> Documentation -> Dictionary Format
for the authoritative reference.

Every visual choice here (div/span class names) is matched by a rule in
resources/style/EnglishPersianDictionary.css -- the two files should
always be edited together.
"""
from __future__ import annotations

from xml.sax.saxutils import escape, quoteattr

from .dataset import slugify


def _esc(text: str) -> str:
    """Escape text for use between XML tags."""
    return escape(text or "")


def _attr(text: str) -> str:
    """Escape text for use as a quoted XML attribute value (includes quotes)."""
    return quoteattr(text or "")


def _render_pronunciation(pos: dict) -> str:
    parts = []
    if pos.get("ipa"):
        parts.append(f'<span class="ipa">{_esc(pos["ipa"])}</span>')
    if pos.get("pronunciation_guide"):
        parts.append(f'<span class="pron-guide">({_esc(pos["pronunciation_guide"])})</span>')
    if not parts:
        return ""
    return f'<span class="pronunciation">{" ".join(parts)}</span>'


def _render_example(example: dict) -> str:
    en = _esc(example.get("en", ""))
    fa = _esc(example.get("fa", ""))
    return (
        '<div class="example">'
        f'<div class="example-en" xml:lang="en">{en}</div>'
        f'<div class="example-fa" xml:lang="fa" dir="rtl">{fa}</div>'
        "</div>"
    )


def _render_word_list(label: str, words: list, css_class: str) -> str:
    if not words:
        return ""
    joined = ", ".join(_esc(w) for w in words)
    return (
        f'<div class="{css_class}">'
        f'<span class="label">{_esc(label)}:</span> '
        f'<span class="values" xml:lang="en">{joined}</span>'
        "</div>"
    )


def _render_sense(sense: dict, sense_number: int, total_senses: int) -> str:
    translations = sense.get("translations", [])
    translations_html = "، ".join(_esc(t) for t in translations)

    html = ['<li class="sense">']

    if total_senses > 1:
        html.append(f'<span class="sense-number">{sense_number}</span>')

    html.append(
        f'<div class="translations" xml:lang="fa" dir="rtl">{translations_html}</div>'
    )

    if sense.get("definition_en"):
        html.append(
            f'<div class="definition-en" xml:lang="en">{_esc(sense["definition_en"])}</div>'
        )

    examples = sense.get("examples", [])
    if examples:
        html.append('<div class="examples">')
        html.extend(_render_example(ex) for ex in examples)
        html.append("</div>")

    html.append(_render_word_list("Synonyms", sense.get("synonyms", []), "synonyms"))
    html.append(_render_word_list("Antonyms", sense.get("antonyms", []), "antonyms"))

    html.append("</li>")
    return "".join(part for part in html if part)


def _render_pos_block(pos: dict) -> str:
    pos_type = _esc(pos.get("type", ""))
    pronunciation = _render_pronunciation(pos)
    senses = pos.get("senses", [])

    html = [
        '<div class="pos-block">',
        '<div class="pos-line">',
        f'<span class="pos-label" xml:lang="en">{pos_type}</span>',
        pronunciation,
        "</div>",
        '<ol class="senses">',
    ]
    html.extend(
        _render_sense(sense, i + 1, len(senses)) for i, sense in enumerate(senses)
    )
    html.append("</ol>")
    html.append("</div>")
    return "".join(html)


def _render_related_words(related_words: list) -> str:
    if not related_words:
        return ""
    items = []
    for rel in related_words:
        pos = f' <span class="related-pos" xml:lang="en">({_esc(rel["pos"])})</span>' if rel.get("pos") else ""
        items.append(
            '<li class="related-item">'
            f'<span class="related-word" xml:lang="en">{_esc(rel["word"])}</span>'
            f"{pos}"
            f' <span class="related-translation" xml:lang="fa" dir="rtl">{_esc(rel["translation"])}</span>'
            "</li>"
        )
    return (
        '<div class="related-words">'
        '<h3 class="section-title">Related Words</h3>'
        f'<ul class="related-list">{"".join(items)}</ul>'
        "</div>"
    )


def _render_idioms(idioms: list) -> str:
    if not idioms:
        return ""
    items = []
    for idiom in idioms:
        example = ""
        if idiom.get("example_en") or idiom.get("example_fa"):
            example = (
                '<div class="example">'
                f'<div class="example-en" xml:lang="en">{_esc(idiom.get("example_en", ""))}</div>'
                f'<div class="example-fa" xml:lang="fa" dir="rtl">{_esc(idiom.get("example_fa", ""))}</div>'
                "</div>"
            )
        items.append(
            '<li class="idiom-item">'
            f'<div class="idiom-phrase" xml:lang="en">{_esc(idiom["phrase"])}</div>'
            f'<div class="idiom-translation" xml:lang="fa" dir="rtl">{_esc(idiom["translation"])}</div>'
            f"{example}"
            "</li>"
        )
    return (
        '<div class="idioms">'
        '<h3 class="section-title">Idioms &amp; Expressions</h3>'
        f'<ul class="idiom-list">{"".join(items)}</ul>'
        "</div>"
    )


def _render_notes(notes: str) -> str:
    if not notes or notes.strip() == "—":
        return ""
    return (
        '<div class="notes">'
        '<h3 class="section-title">Usage Note</h3>'
        f'<p class="notes-text">{_esc(notes)}</p>'
        "</div>"
    )


def render_entry(entry: dict) -> str:
    """Render one word entry dict into a full <d:entry>...</d:entry> string."""
    word = entry["word"]
    slug = slugify(word)

    index_values = {word, word.capitalize()}
    index_values.update(entry.get("inflections", []) or [])
    index_elements = "".join(
        f'<d:index d:value={_attr(v)} d:title={_attr(word)}/>' for v in sorted(index_values)
    )

    pos_blocks = "".join(_render_pos_block(pos) for pos in entry.get("parts_of_speech", []))
    related_html = _render_related_words(entry.get("related_words", []))
    idioms_html = _render_idioms(entry.get("idioms", []))
    notes_html = _render_notes(entry.get("notes", ""))

    body = (
        '<div class="entry">'
        '<div class="head-block">'
        f'<span class="headword" xml:lang="en">{_esc(word)}</span>'
        "</div>"
        f"{pos_blocks}"
        f"{related_html}"
        f"{idioms_html}"
        f"{notes_html}"
        "</div>"
    )

    return (
        f'<d:entry id="entry_{slug}" d:title={_attr(word)}>'
        f"{index_elements}"
        f"{body}"
        "</d:entry>"
    )
