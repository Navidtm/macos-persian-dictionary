# English → Persian Dictionary for macOS

An open-source English-to-Persian dictionary that installs natively into
**Dictionary.app** on macOS. Entries are written as full learner's-dictionary
articles — definitions, pronunciation, example sentences, synonyms, antonyms,
related words, and idioms — not bare word-for-word translations.

This first release ships with **20 fully-completed entries**. The project is
built so it can grow to thousands of entries without ever needing a
redesign — see [Roadmap](#roadmap).

> **Status:** early foundation release (v0.1.0). Structure, tooling, and
> content quality bar are the focus right now, not word count.

This README has two audiences:

- **[For Users](#for-users)** — just want the dictionary installed. No
  Python, Xcode, or command line required.
- **[For Contributors / Developers](#for-contributors--developers)** — want
  to add words, fix translations, or work on the build tooling.

---

## Table of contents

- [Features](#features)
- [Screenshots](#screenshots)
- [For Users](#for-users)
- [For Contributors / Developers](#for-contributors--developers)
  - [Development setup](#development-setup)
  - [Build commands](#build-commands)
  - [How to add a new word](#how-to-add-a-new-word)
  - [Release process](#release-process)
- [Project structure](#project-structure)
- [How it works](#how-it-works)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Native integration** — installs as a real Dictionary.app source, usable
  system-wide (right-click "Look Up", the Dictionary panel, `dict://` links,
  the Dictionary sidebar, etc.), no separate app required.
- **Real dictionary entries, not flashcards.** Every word includes, wherever
  applicable:
  - Part of speech, with separate entries for a word's different roles
    (e.g. *benefit* as both noun and verb)
  - IPA pronunciation **and** a plain-English pronunciation guide
  - Multiple senses, each with its own translation(s) and definition
  - English example sentences with Persian translations
  - Synonyms and antonyms
  - Related/derived words (e.g. *ability → able, enable, disability*)
  - Common idioms and expressions
  - Usage notes (grammar patterns, common confusions, register)
- **Clean, readable design** — proper typography for both English and
  Persian (correct right-to-left rendering), clear section headers, no
  visual clutter, and automatic Dark Mode support.
- **One word, one file.** Every entry is a small, self-contained JSON file,
  so the dataset stays easy to review, diff, and scale.
- **Zero-dependency tooling.** The build and validation scripts use only the
  Python standard library — no `pip install` required to contribute.
- **No build tools needed to install it.** End users download a ready-made
  ZIP from GitHub Releases and double-click an installer script. Python,
  Make, Xcode, and the Dictionary Development Kit are developer-only
  dependencies.

## Screenshots

<!--
  TODO: add real screenshots once the first build is captured, e.g.:

  ![Dictionary.app search result for "patience"](docs/screenshots/patience-entry.png)
  ![Dictionary.app sidebar with English-Persian selected](docs/screenshots/sidebar.png)
-->

_Screenshots will be added here once the dictionary has been built and
installed on macOS — see [`docs/screenshots/`](docs/screenshots)._

---

## For Users

You don't need Python, Xcode, Make, or the Dictionary Development Kit —
those are only for people building the dictionary from source (see
[For Contributors / Developers](#for-contributors--developers)).

1. Go to the [Releases page](../../releases) and download the latest
   `EnglishPersianDictionary-vX.Y.Z.zip`.
2. Unzip it. You'll get three items:
   - `EnglishPersianDictionary.dictionary` — the dictionary itself
   - `Install.command` — installs it
   - `Uninstall.command` — removes it
3. Double-click **`Install.command`**.
   - The first time, macOS will likely warn that it's from an
     "unidentified developer," since it isn't signed. Right-click
     (Control-click) the file instead, choose **Open**, then confirm
     **Open** in the dialog that appears. You only need to do this once.
   - A Terminal window will briefly appear and run the install steps, then
     close automatically once you press a key.
4. Open **Dictionary.app**, go to **Dictionary → Settings** (or
   **Preferences**), and enable **English-Persian** in the list.
5. Look up any of the 20 seed words (e.g. "patience") to confirm it worked.

To remove it later, double-click **`Uninstall.command`** the same way.

---

## For Contributors / Developers

Everything below assumes you're working from a clone of this repository,
not the release ZIP.

### Development setup

Most of this project only needs Python 3 (standard library only — nothing
to `pip install`). Compiling an actual `.dictionary` bundle additionally
needs macOS and Apple's **Dictionary Development Kit**, which Apple stopped
distributing through Xcode after Xcode 9 (2017) — it won't be in Xcode →
Settings → Components on any current Xcode install. Get a preserved copy
from a community mirror instead:

```bash
git clone https://github.com/yourname/english-persian-dictionary.git
cd english-persian-dictionary

# Only needed for `make package` / `make install` / `make release`:
git clone https://github.com/nanoskript/dictionary-development-kit.git kit
```

Cloning the kit into `./kit` (as above) is the convention this project's
Makefile looks for automatically — no configuration needed. If you keep it
somewhere else, pass `DDK_ROOT` explicitly to any command below, e.g.
`make package DDK_ROOT="/path/to/dictionary-development-kit"`.

Two things that can trip you up with the kit itself:
- **Apple Silicon:** if you see "bad CPU type in executable", install
  Rosetta once: `softwareupdate --install-rosetta --agree-to-license`.
- **Missing Perl:** macOS still ships `/usr/bin/perl` (used by a couple of
  the kit's build steps) but it's deprecated and may disappear in a future
  macOS release. If it's missing: `brew install perl`.

### Build commands

| Command | What it does | Requires |
|---|---|---|
| `make build` | Generate `build/EnglishPersianDictionary.xml` (+ `.css`, `+.plist`) from `data/words/*.json` | Python 3 only |
| `make validate` | Validate all entries without building | Python 3 only |
| `make test` | Run the automated test suite | Python 3 only |
| `make preview` | Render entries to `build/preview.html` for design review in any browser | Python 3 only |
| `make package` | Compile `build/` into a `.dictionary` bundle | macOS + Dictionary Development Kit |
| `make install` | `package` + copy the bundle into `~/Library/Dictionaries` | macOS + Dictionary Development Kit |
| `make uninstall` | Remove the bundle from `~/Library/Dictionaries` | macOS |
| `make release` | Build a versioned, end-user-ready ZIP (what `Install.command` ships in) | macOS + Dictionary Development Kit |
| `make clean` | Remove all generated files (`build/`, `objects/`, `release/`) | — |

Day-to-day content work is usually just:

```bash
python3 scripts/validate.py   # check your JSON
make build                    # confirm it compiles to XML
make test                     # run the test suite
make preview WORDS="patience" # eyeball the rendered entry in a browser
```

`make package` / `make install` are for actually seeing the entry inside
Dictionary.app, and need a Mac with the kit installed as described above.

### How to add a new word

1. Scaffold a new entry:

   ```bash
   python3 scripts/new_word.py perseverance
   ```

   This creates `data/words/p/perseverance.json` pre-filled with the
   expected structure.

2. Fill in the fields — translations, definitions, example sentences,
   synonyms, antonyms, related words, idioms, and notes, as applicable. The
   full field reference lives in
   [`data/schema/word.schema.json`](data/schema/word.schema.json).

3. Validate, build, and preview:

   ```bash
   python3 scripts/validate.py
   make build
   make preview WORDS="perseverance"
   ```

4. Open a pull request. See [CONTRIBUTING.md](CONTRIBUTING.md) for the full
   style guide and review process.

### Release process

Releases are cut by pushing a version tag; a GitHub Actions workflow
(`.github/workflows/release.yml`) does the rest — building the dictionary,
compiling it with the Dictionary Development Kit, zipping it with the
installer scripts, and publishing it as a GitHub Release.

A maintainer only needs to run:

```bash
git tag v0.2.0
git push origin v0.2.0
```

That triggers CI to:

1. Check out the repo on a macOS runner.
2. Fetch the Dictionary Development Kit.
3. Derive the version from the tag (`v0.2.0` → `0.2.0`).
4. Run `make release VERSION=0.2.0`, which validates the data, builds the
   XML, compiles the `.dictionary` bundle, stamps that version into its
   `Info.plist`, and zips it with `Install.command` / `Uninstall.command` /
   `README.txt`.
5. Publish `EnglishPersianDictionary-v0.2.0.zip` as a GitHub Release asset.

To do the same thing locally (e.g. to sanity-check a release before
tagging), run `make release VERSION=0.2.0` yourself — it produces
`release/EnglishPersianDictionary-v0.2.0.zip` locally, identically to CI.

Remember to add a section to [CHANGELOG.md](CHANGELOG.md) for every release.

---

## Project structure

```
english-persian-dictionary/
├── data/
│   ├── schema/
│   │   └── word.schema.json        # Canonical field reference for word entries
│   └── words/                      # One JSON file per headword, sharded by first letter
│       ├── a/
│       │   ├── abandon.json
│       │   ├── ability.json
│       │   └── achieve.json
│       ├── b/
│       │   ├── beautiful.json
│       │   └── benefit.json
│       └── ...
├── resources/
│   ├── style/
│   │   └── EnglishPersianDictionary.css   # All entry styling (RTL-aware, Dark Mode)
│   ├── plist/
│   │   └── EnglishPersianDictionaryInfo.plist  # Dictionary bundle descriptor
│   ├── matter/
│   │   └── front_matter.html       # "About this dictionary" page
│   └── release/                    # End-user assets bundled into release ZIPs
│       ├── Install.command
│       ├── Uninstall.command
│       └── README.txt
├── scripts/
│   ├── build.py                    # data/words/*.json -> build/*.xml (+ css, + plist)
│   ├── validate.py                 # Validate data/words/*.json without building
│   ├── new_word.py                 # Scaffold a new word entry file
│   ├── preview.py                  # Render entries to plain HTML for design review
│   ├── check_ddk.sh                 # Shared "is the DDK installed?" check
│   ├── make_release_zip.sh         # Assemble the end-user release ZIP
│   ├── install_dictionary.sh       # Copy a built bundle into ~/Library/Dictionaries (dev use)
│   ├── uninstall_dictionary.sh     # Remove an installed bundle (dev use)
│   └── lib/
│       ├── dataset.py              # Locate/load word JSON files
│       ├── validate.py             # Schema validation rules (stdlib only)
│       └── xml_render.py           # Word entry dict -> Apple Dictionary XML
├── tests/
│   ├── test_data.py                # Every entry is valid, no duplicates, etc.
│   └── test_build.py               # Build output is well-formed and complete
├── .github/workflows/
│   ├── ci.yml                      # Validate + test on every push/PR
│   └── release.yml                 # Build + publish a GitHub Release on version tags
├── build/                          # Generated: dictionary XML/CSS/plist (git-ignored)
├── objects/                        # Generated: compiled .dictionary bundle (git-ignored)
├── release/                        # Generated: end-user release ZIP (git-ignored)
├── kit/                            # Local Dictionary Development Kit checkout (git-ignored)
├── Makefile
├── CONTRIBUTING.md
├── CHANGELOG.md
├── LICENSE
└── README.md
```

## How it works

Apple's Dictionary Services format expects three inputs: an XML file
containing `<d:entry>` elements (one per headword, each with one or more
`<d:index>` entries so lookups and inflections resolve to it), a CSS
stylesheet, and an `Info.plist` describing the bundle. Apple's
`build_dict.sh` (part of the Dictionary Development Kit) compiles those
three into a `.dictionary` bundle that Dictionary.app can load.

This project keeps the **content** (`data/words/*.json`) completely
separate from that **output format**. `scripts/build.py` is the only place
that knows how to turn one into the other:

```
data/words/*.json  →  scripts/build.py  →  build/EnglishPersianDictionary.xml
                                            build/EnglishPersianDictionary.css
                                            build/EnglishPersianDictionaryInfo.plist
                                                        │
                                                        ▼ (make package / make release, macOS only)
                                     objects/EnglishPersianDictionary.dictionary
                                                        │
                                                        ▼ (make release only)
                          release/EnglishPersianDictionary-vX.Y.Z.zip
                          (+ Install.command, Uninstall.command, README.txt)
```

This separation is what makes future growth safe: adding word #21 or word
#20,000 never touches the XML format, the CSS, or the build tooling — only
`data/words/`. It's also what makes end-user installs simple: users only
ever touch the last artifact in that chain, never the pipeline that
produced it.

## Roadmap

- [x] Project foundation: schema, build pipeline, validation, tests
- [x] 20 fully-completed entries covering common core vocabulary
- [x] Automated CI (GitHub Actions) running validation + the test suite on
      every push and pull request
- [x] Tag-triggered GitHub Releases with a ready-to-install ZIP (no Python,
      Make, or Xcode required for end users)
- [ ] Grow to ~1,000 entries covering the most frequent English words
- [ ] Add inflection indexing (plurals, verb tenses) so more surface forms
      resolve to the right entry
- [ ] Add a Persian → English direction as a separate dictionary target
- [ ] Add audio pronunciation support, if/when Dictionary Services allows it
- [ ] Explore automated import tooling for bulk-adding vetted entries at
      10,000+ / 100,000+ word scale, with a review queue for quality control
- [ ] Code-sign the release ZIP's installer scripts, if that turns out to
      meaningfully reduce the "unidentified developer" warning for end users

## Contributing

Contributions of new words, corrected translations, and tooling
improvements are very welcome. Please read
[CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request — it
covers the entry style guide, the data format, and the review process.

## License

Released under the [MIT License](LICENSE). See the license file for the
note on how dictionary content itself is licensed.
