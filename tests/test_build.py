"""Tests that scripts/build.py produces well-formed, complete XML output.

Run with:
    python3 -m unittest discover -s tests -v
"""
import os
import subprocess
import sys
import unittest
import xml.etree.ElementTree as ET

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..")
BUILD_XML = os.path.join(REPO_ROOT, "build", "EnglishPersianDictionary.xml")

NAMESPACES = {
    "d": "http://www.apple.com/DTDs/DictionaryService-1.0.rng",
    "xhtml": "http://www.w3.org/1999/xhtml",
}


class TestBuildOutput(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        result = subprocess.run(
            [sys.executable, os.path.join(REPO_ROOT, "scripts", "build.py")],
            capture_output=True,
            text=True,
        )
        cls.build_result = result
        if os.path.exists(BUILD_XML):
            cls.tree = ET.parse(BUILD_XML)
        else:
            cls.tree = None

    def test_build_succeeds(self):
        self.assertEqual(
            self.build_result.returncode,
            0,
            f"build.py failed:\nstdout:\n{self.build_result.stdout}\nstderr:\n{self.build_result.stderr}",
        )

    def test_xml_is_well_formed(self):
        self.assertIsNotNone(self.tree, "build/EnglishPersianDictionary.xml was not produced")

    def test_contains_front_matter_entry(self):
        root = self.tree.getroot()
        entries = root.findall("d:entry", NAMESPACES)
        ids = {entry.get("id") for entry in entries}
        self.assertIn("front_back_matter", ids)

    def test_entry_count_matches_word_count(self):
        sys.path.insert(0, os.path.join(REPO_ROOT, "scripts"))
        from lib.dataset import load_all_words  # noqa: E402

        word_count = len(load_all_words())
        root = self.tree.getroot()
        entries = root.findall("d:entry", NAMESPACES)
        # +1 for the front matter entry.
        self.assertEqual(len(entries), word_count + 1)


if __name__ == "__main__":
    unittest.main()
