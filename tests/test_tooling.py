#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Tests for the contributor tooling scripts (scripts/new_construct.py,
scripts/validate_source.py).

Validates:
  - validate_source flags missing description, invalid JSON, a missing
    ${CLAUDE_PLUGIN_ROOT} reference, and a non-kebab instance dir; passes on
    well-formed sources AND on the real src/ tree.
  - new_construct's kebab guard and example-template selection.
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import new_construct  # noqa: E402
import validate_source  # noqa: E402
from constructs import CONSTRUCTS  # noqa: E402
from utils import SRC  # noqa: E402


class TestValidateSource(unittest.TestCase):
    def test_good_skill_passes(self):
        with tempfile.TemporaryDirectory() as t:
            d = Path(t) / "skills" / "good"
            d.mkdir(parents=True)
            (d / "SKILL.md").write_text(
                "---\nname: good\ndescription: A good skill.\n---\nbody\n", encoding="utf-8"
            )
            self.assertEqual(validate_source.validate([d]), [])

    def test_missing_description_flagged(self):
        with tempfile.TemporaryDirectory() as t:
            d = Path(t) / "skills" / "bad"
            d.mkdir(parents=True)
            (d / "SKILL.md").write_text("---\nname: bad\n---\nbody\n", encoding="utf-8")
            self.assertTrue(any("description" in p for p in validate_source.validate([d])))

    def test_missing_plugin_root_ref_flagged(self):
        with tempfile.TemporaryDirectory() as t:
            d = Path(t) / "lsp-servers" / "x"
            d.mkdir(parents=True)
            (d / "lsp-config.json").write_text(
                '{"args": ["${CLAUDE_PLUGIN_ROOT}/nope.py"]}', encoding="utf-8"
            )
            self.assertTrue(any("nope.py" in p for p in validate_source.validate([d])))

    def test_present_plugin_root_ref_ok(self):
        with tempfile.TemporaryDirectory() as t:
            d = Path(t) / "lsp-servers" / "x"
            d.mkdir(parents=True)
            (d / "server.py").write_text("# server\n", encoding="utf-8")
            (d / "lsp-config.json").write_text(
                '{"args": ["${CLAUDE_PLUGIN_ROOT}/server.py"]}', encoding="utf-8"
            )
            self.assertEqual(validate_source.validate([d]), [])

    def test_invalid_json_flagged(self):
        with tempfile.TemporaryDirectory() as t:
            d = Path(t) / "mcp-servers" / "x"
            d.mkdir(parents=True)
            (d / "mcp-config.json").write_text("{not json", encoding="utf-8")
            self.assertTrue(any("invalid JSON" in p for p in validate_source.validate([d])))

    def test_non_kebab_instance_dir_flagged(self):
        with tempfile.TemporaryDirectory() as t:
            d = Path(t) / "skills" / "Bad_Name"
            d.mkdir(parents=True)
            (d / "SKILL.md").write_text("---\ndescription: x\n---\n", encoding="utf-8")
            self.assertTrue(any("kebab-case" in p for p in validate_source.validate([d])))

    def test_real_src_is_clean(self):
        # The shipped sources must pass their own validator.
        self.assertEqual(validate_source.validate([SRC]), [])


class TestNewConstruct(unittest.TestCase):
    def test_kebab_regex(self):
        self.assertTrue(new_construct.KEBAB.match("telegram-notify"))
        self.assertFalse(new_construct.KEBAB.match("Bad_Name"))
        self.assertFalse(new_construct.KEBAB.match("UPPER"))

    def test_pick_example_prefers_single_or_multi(self):
        src = CONSTRUCTS["skill"].source_directory
        self.assertEqual(new_construct._pick_example(src, multi=False), "example-single")
        self.assertEqual(new_construct._pick_example(src, multi=True), "example-multi")

    def test_pick_example_rule_single_dir(self):
        # rule ships a single 'example' dir (not example-single/-multi)
        src = CONSTRUCTS["rule"].source_directory
        self.assertEqual(new_construct._pick_example(src, multi=False), "example")


if __name__ == "__main__":
    unittest.main(verbosity=2)
