# Contributing

Thank you for wanting to help grow this dictionary. This project only works
long-term if entries stay consistent and high quality, so please read this
short guide before opening a pull request.

## Ground rules

- **One word per file.** Each headword lives in its own JSON file under
  `data/words/<first-letter>/<word>.json`. Never add words by editing a big
  shared file — there isn't one, by design (see [`README.md`](README.md#project-structure)).
- **Every entry should teach, not just translate.** A bare translation
  (`"cat" -> "گربه"`) is not enough. Include a definition, at least one
  example sentence with its Persian translation, and synonyms/antonyms/related
  words wherever they genuinely apply. Look at existing entries in
  `data/words/` for the expected depth and tone.
- **Persian text quality matters as much as English.** Use correct Persian
  orthography (proper ZWNJ / نیم‌فاصله where conventional, correct
  punctuation), and prefer natural, commonly used translations over overly
  literal ones.
- **Cite your source if you didn't write it yourself.** If a definition or
  example is adapted from another dictionary, say so in your pull request
  description so we can check licensing compatibility.

## Adding a new word

1. Generate a starter file:

   ```bash
   python3 scripts/new_word.py <word>
   ```

   This creates `data/words/<letter>/<word>.json` pre-filled with the
   expected structure (see `data/schema/word.schema.json` for the full
   field reference).

2. Fill in every field that applies:
   - `parts_of_speech[].type`, `.ipa`, `.pronunciation_guide`
   - `senses[].translations`, `.definition_en`, `.examples`
   - `synonyms`, `antonyms` where they exist
   - `related_words`, `idioms`, and a free-text `notes` field for anything
     a learner would find useful (register, common mistakes, grammar
     patterns, etc.)

   Omit fields that genuinely don't apply (not every word has antonyms or
   idioms) rather than leaving them as empty placeholders.

3. Validate your entry:

   ```bash
   python3 scripts/validate.py
   ```

4. Make sure the full dictionary still builds:

   ```bash
   make build
   ```

5. Run the test suite:

   ```bash
   make test
   ```

6. Open a pull request. Please keep one logical change per PR (e.g. "Add
   entry: perseverance" or "Fix Persian translation for 'ability'") so
   reviews stay quick.

## Editing an existing entry

Just edit the JSON file directly, then repeat steps 3-5 above. Please explain
*why* a change is being made in the PR description, especially for
translation corrections — native-speaker context is very helpful for
reviewers.

## Style guide (quick reference)

| Field | Convention |
|---|---|
| `word` | lower-case, exactly as it should appear as the headword |
| `ipa` | full IPA, wrapped in `/slashes/` |
| `pronunciation_guide` | plain-English respelling, e.g. `"uh-BAN-dun"` |
| `translations` | most common Persian equivalent(s) first |
| `definition_en` | one clear sentence, learner-friendly, not circular |
| `examples[].en` / `.fa` | natural sentences, not written for the dictionary's own definition |
| `notes` | anything a learner would want to know that doesn't fit elsewhere |

## Code changes

Changes to `scripts/`, `resources/`, or `Makefile` are welcome too —
performance improvements, better validation, nicer CSS, additional build
targets, etc. Please keep the project dependency-free (standard library
Python only) unless there's a strong reason not to, since that's what keeps
`make build` and `make test` usable with nothing but a stock Python 3
install.

## Code of conduct

Be respectful and constructive. This is a small project aiming to be useful
to a lot of language learners — assume good faith, and keep disagreements
about translations focused on the language, not the person.
