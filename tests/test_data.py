"""Tests that every word entry under data/words/ is well-formed.

Run with:
    python3 -m unittest discover -s tests -v
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from scripts.lib.dataset import load_all_words  # noqa: E402
from scripts.lib.validate import validate_entry  # noqa: E402


class TestWordData(unittest.TestCase):
    def setUp(self):
        self.entries = load_all_words()

    def test_at_least_one_word_exists(self):
        self.assertGreater(len(self.entries), 0, "data/words/ should contain at least one entry")

    def test_every_entry_is_valid(self):
        for entry in self.entries:
            errors = validate_entry(entry.data, where=entry.path)
            self.assertEqual(errors, [], f"Validation errors in {entry.path}: {errors}")

    def test_no_duplicate_headwords(self):
        seen = {}
        for entry in self.entries:
            word = entry.data.get("word", "").strip().lower()
            self.assertNotIn(
                word,
                seen,
                f"Duplicate headword '{word}' in {entry.path} and {seen.get(word)}",
            )
            seen[word] = entry.path

    def test_file_matches_headword_slug(self):
        """The JSON filename should match slugify(word), so contributors can
        find an entry by its headword alone."""
        from scripts.lib.dataset import slugify

        for entry in self.entries:
            expected = f"{slugify(entry.data['word'])}.json"
            actual = os.path.basename(entry.path)
            self.assertEqual(
                actual, expected, f"{entry.path} should be named {expected}"
            )

    def test_every_example_has_english_and_persian(self):
        for entry in self.entries:
            for pos in entry.data.get("parts_of_speech", []):
                for sense in pos.get("senses", []):
                    for example in sense.get("examples", []):
                        self.assertTrue(example.get("en", "").strip())
                        self.assertTrue(example.get("fa", "").strip())


if __name__ == "__main__":
    unittest.main()
