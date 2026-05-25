#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Tests for the `agents` CLI shim (Unit 7).

Validates:
  - argparse surface: every documented subcommand parses; --scope rejects bad values
  - construct prefix dispatch + split_plugin_name
  - path resolution per scope + --agents-only
  - install / uninstall round-trip for skills (project scope, against the
    real marketplace at REPO_ROOT)
  - install for rules sprays to .cursor/ + .windsurf/ + .agents/ (project scope)
  - --agents-only collapses the spray to .agents/ only
  - list installed enumerates after install

Tests run against the in-tree marketplace via ``--marketplace-root``, so they
require no network. Project-scope writes are isolated by chdir into a tmpdir.
"""

from __future__ import annotations

import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from agents_cli import install as install_mod
from agents_cli import list as list_mod
from agents_cli.constructs import PREFIX_TO_HANDLER, split_plugin_name
from agents_cli.main import build_parser
from agents_cli.utils import paths as paths_mod


class _Chdir:
    """Tiny context manager for temporary cwd changes."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.prev: Path | None = None

    def __enter__(self) -> Path:
        self.prev = Path.cwd()
        os.chdir(self.path)
        return self.path

    def __exit__(self, *exc: object) -> None:
        if self.prev is not None:
            os.chdir(self.prev)


class TestArgParse(unittest.TestCase):
    def test_install_parses(self):
        p = build_parser()
        ns = p.parse_args(["install", "skill-example", "--scope", "user"])
        self.assertEqual(ns.command, "install")
        self.assertEqual(ns.plugin, "skill-example")
        self.assertEqual(ns.scope, "user")

    def test_install_default_scope_is_project(self):
        ns = build_parser().parse_args(["install", "skill-example"])
        self.assertEqual(ns.scope, "project")

    def test_install_agents_only_flag(self):
        ns = build_parser().parse_args(["install", "skill-example", "--agents-only"])
        self.assertTrue(ns.agents_only)

    def test_install_bad_scope_rejected(self):
        p = build_parser()
        with self.assertRaises(SystemExit):
            with redirect_stderr(io.StringIO()):
                p.parse_args(["install", "skill-example", "--scope", "global"])

    def test_uninstall_parses(self):
        ns = build_parser().parse_args(["uninstall", "skill-example"])
        self.assertEqual(ns.command, "uninstall")

    def test_list_parses_with_available(self):
        ns = build_parser().parse_args(["list", "--available"])
        self.assertTrue(ns.available)

    def test_upgrade_all_flag(self):
        ns = build_parser().parse_args(["upgrade", "--all"])
        self.assertTrue(ns.all_plugins)

    def test_info_parses(self):
        ns = build_parser().parse_args(["info", "skill-example"])
        self.assertEqual(ns.plugin, "skill-example")

    def test_marketplace_add_parses(self):
        ns = build_parser().parse_args(["marketplace", "add", "https://example.com/repo"])
        self.assertEqual(ns.marketplace_command, "add")
        self.assertEqual(ns.url, "https://example.com/repo")

    def test_marketplace_list_parses(self):
        ns = build_parser().parse_args(["marketplace", "list"])
        self.assertEqual(ns.marketplace_command, "list")

    def test_marketplace_remove_parses(self):
        ns = build_parser().parse_args(["marketplace", "remove", "foo"])
        self.assertEqual(ns.marketplace_command, "remove")
        self.assertEqual(ns.name, "foo")


class TestConstructDispatch(unittest.TestCase):
    def test_split_known_prefix(self):
        self.assertEqual(split_plugin_name("skill-example"), ("skill", "example"))
        self.assertEqual(split_plugin_name("rule-blast-radius"), ("rule", "blast-radius"))
        self.assertEqual(split_plugin_name("agent-example"), ("agent", "example"))

    def test_split_output_style_multiword_prefix(self):
        self.assertEqual(
            split_plugin_name("output-style-foo"), ("output-style", "foo")
        )

    def test_split_unknown_prefix_raises(self):
        with self.assertRaises(ValueError):
            split_plugin_name("unknown-thing")

    def test_handler_registered_for_each_supported_prefix(self):
        for prefix in ("skill", "rule", "agent", "hook", "mcp", "command"):
            self.assertIsNotNone(
                PREFIX_TO_HANDLER[prefix],
                f"handler missing for prefix '{prefix}'",
            )


class TestPaths(unittest.TestCase):
    def test_skill_project_scope_writes_to_agents(self):
        with tempfile.TemporaryDirectory() as tmp:
            with _Chdir(Path(tmp)) as cwd:
                t = paths_mod.resolve_skill("example", "project", False)
                self.assertEqual(t.agents_path, cwd / ".agents" / "skills" / "example")
                self.assertEqual(t.platform_paths, [])

    def test_rule_project_scope_sprays(self):
        with tempfile.TemporaryDirectory() as tmp:
            with _Chdir(Path(tmp)) as cwd:
                t = paths_mod.resolve_rule("example", "project", False)
                self.assertEqual(t.agents_path, cwd / ".agents" / "rules" / "example.md")
                self.assertIn(cwd / ".cursor" / "rules" / "example.md", t.platform_paths)
                self.assertIn(cwd / ".windsurf" / "rules" / "example.md", t.platform_paths)

    def test_rule_agents_only_collapses_spray(self):
        with tempfile.TemporaryDirectory() as tmp:
            with _Chdir(Path(tmp)) as cwd:
                t = paths_mod.resolve_rule("example", "project", True)
                self.assertEqual(t.platform_paths, [])

    def test_user_scope_is_agents_only(self):
        # User scope always writes only to ~/.agents/<construct>/ regardless of agents_only.
        t = paths_mod.resolve_agent("example", "user", False)
        self.assertEqual(t.platform_paths, [])
        self.assertTrue(str(t.agents_path).endswith(".agents/agents/example.md")
                        or str(t.agents_path).endswith(".agents\\agents\\example.md"))


class TestInstallSkillProjectScope(unittest.TestCase):
    def test_install_then_uninstall_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            with _Chdir(Path(tmp)) as cwd:
                buf = io.StringIO()
                with redirect_stdout(buf):
                    rc = install_mod.install(
                        "skill-example", scope="project",
                        marketplace_root=REPO_ROOT,
                    )
                self.assertEqual(rc, 0, msg=buf.getvalue())
                self.assertTrue((cwd / ".agents" / "skills" / "example" / "SKILL.md").exists())

                with redirect_stdout(io.StringIO()):
                    rc = install_mod.uninstall("skill-example", scope="project")
                self.assertEqual(rc, 0)
                self.assertFalse((cwd / ".agents" / "skills" / "example").exists())


class TestInstallRuleAllSpray(unittest.TestCase):
    def test_rule_writes_to_all_platforms_under_project(self):
        with tempfile.TemporaryDirectory() as tmp:
            with _Chdir(Path(tmp)) as cwd:
                with redirect_stdout(io.StringIO()):
                    rc = install_mod.install(
                        "rule-example", scope="project",
                        marketplace_root=REPO_ROOT,
                    )
                self.assertEqual(rc, 0)
                self.assertTrue((cwd / ".agents" / "rules" / "example.md").exists())
                self.assertTrue((cwd / ".cursor" / "rules" / "example.md").exists())
                self.assertTrue((cwd / ".windsurf" / "rules" / "example.md").exists())


class TestAgentsOnlyFlag(unittest.TestCase):
    def test_agents_only_skips_platform_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            with _Chdir(Path(tmp)) as cwd:
                with redirect_stdout(io.StringIO()):
                    rc = install_mod.install(
                        "rule-example", scope="project", agents_only=True,
                        marketplace_root=REPO_ROOT,
                    )
                self.assertEqual(rc, 0)
                self.assertTrue((cwd / ".agents" / "rules" / "example.md").exists())
                self.assertFalse((cwd / ".cursor" / "rules" / "example.md").exists())
                self.assertFalse((cwd / ".windsurf" / "rules" / "example.md").exists())


class TestList(unittest.TestCase):
    def test_list_installed_enumerates_after_install(self):
        with tempfile.TemporaryDirectory() as tmp:
            with _Chdir(Path(tmp)):
                with redirect_stdout(io.StringIO()):
                    install_mod.install(
                        "skill-example", scope="project",
                        marketplace_root=REPO_ROOT,
                    )
                names = list_mod.installed_plugins(scope="project")
                self.assertIn("skill-example", names)


class TestUnknownPluginErrors(unittest.TestCase):
    def test_unknown_prefix_returns_nonzero(self):
        buf = io.StringIO()
        with redirect_stderr(buf):
            rc = install_mod.install(
                "frobnicator-foo", scope="project",
                marketplace_root=REPO_ROOT,
            )
        self.assertNotEqual(rc, 0)

    def test_missing_plugin_returns_nonzero(self):
        with tempfile.TemporaryDirectory() as tmp:
            with _Chdir(Path(tmp)):
                buf = io.StringIO()
                with redirect_stderr(buf):
                    rc = install_mod.install(
                        "skill-doesnotexist", scope="project",
                        marketplace_root=REPO_ROOT,
                    )
                self.assertNotEqual(rc, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
