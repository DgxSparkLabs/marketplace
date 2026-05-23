#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Marketplace test suite — post DI-refactor.

Validates:
  - Source layout (10 construct source dirs + examples)
  - Generated plugins at correct paths with correct schemas
  - Code-generated catch-all bundles (bundle-<prefix>-all)
  - Platform mirror coverage (Codex, Gemini, Cursor, Windsurf, Devin)
  - marketplace.json schema, sorting, and completeness
  - Bundle validation (reserved names, empty bundles, syntax)
  - CONSTRUCTS registry invariants
  - Plugin count formula
  - No secrets in tracked files
  - Generator drift check

Run:
    uv run tests/test_marketplace.py          # all tests
    uv run tests/test_marketplace.py -v       # verbose
    uv run tests/test_marketplace.py -k Name  # filter
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tomllib
import unittest
from pathlib import Path

# Add scripts/ to sys.path for imports
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from bundles import BundleMember, load_bundles
from constructs import (
    CONSTRUCTS,
    RuleConstruct,
    SkillConstruct,
)
from platforms import PLATFORMS
from utils import CATALOG, MARKETPLACE_JSON, scan_source_dir

MARKETPLACE_TOML = REPO_ROOT / "MARKETPLACE.toml"
GENERATED_DIR = REPO_ROOT / "_generated"


# ─── helpers ─────────────────────────────────────────────────────────────────

def load_toml(path: Path) -> dict:
    with open(path, "rb") as f:
        return tomllib.load(f)


def load_marketplace_json() -> dict:
    return json.loads(MARKETPLACE_JSON.read_text(encoding="utf-8"))


# ─── TestSourceLayout ─────────────────────────────────────────────────────────

class TestSourceLayout(unittest.TestCase):
    """Source directory conventions — contract tests."""

    def test_construct_source_dirs_exist(self):
        """Each of the 10 construct source directories must exist."""
        for construct_id, construct in CONSTRUCTS.items():
            with self.subTest(construct=construct_id):
                self.assertTrue(
                    construct.source_directory.exists(),
                    f"{construct_id}: source_directory {construct.source_directory} does not exist",
                )

    def test_examples_present_per_construct(self):
        """Each construct source dir must contain an 'example' subdir."""
        for construct_id, construct in CONSTRUCTS.items():
            with self.subTest(construct=construct_id):
                self.assertTrue(
                    (construct.source_directory / "example").is_dir(),
                    f"{construct_id}: missing {construct.source_directory}/example/",
                )

    def test_instance_names_kebab_case(self):
        """Every instance name across all constructs must be kebab-case."""
        kebab = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
        for construct_id, construct in CONSTRUCTS.items():
            for name in scan_source_dir(construct.source_directory):
                with self.subTest(construct=construct_id, name=name):
                    self.assertRegex(
                        name, kebab,
                        f"{construct_id}/{name}: not kebab-case; "
                        f"derived plugin name '{construct.prefix}-{name}' would be invalid",
                    )

    def test_examples_not_in_separate_dir(self):
        """A top-level examples/ folder must not exist — examples live in native construct dirs."""
        self.assertFalse(
            (REPO_ROOT / "examples").exists(),
            "examples/ must not exist — examples live in native construct folders",
        )


# ─── TestGeneratedPlugins ─────────────────────────────────────────────────────

class TestGeneratedPlugins(unittest.TestCase):
    """Generated plugin artifacts — integration + contract tests."""

    def test_all_plugins_at_correct_path(self):
        """Every plugin in marketplace.json must resolve to a real .claude-plugin/plugin.json."""
        manifest = load_marketplace_json()
        for entry in manifest["plugins"]:
            plugin_path = Path(entry["source"]) / ".claude-plugin" / "plugin.json"
            with self.subTest(plugin=entry["name"]):
                self.assertTrue(
                    plugin_path.exists(),
                    f"{entry['name']}: source {entry['source']} has no .claude-plugin/plugin.json",
                )

    def test_all_plugins_parse_and_have_required_fields(self):
        """Every plugin.json must parse and carry the required common fields."""
        manifest = load_marketplace_json()
        common_required = {"name", "description", "version", "author"}
        for entry in manifest["plugins"]:
            plugin_path = Path(entry["source"]) / ".claude-plugin" / "plugin.json"
            with self.subTest(plugin=entry["name"]):
                data = json.loads(plugin_path.read_text(encoding="utf-8"))
                missing = common_required - set(data.keys())
                self.assertFalse(
                    missing,
                    f"{entry['name']}: missing common fields {missing}",
                )
                if entry["category"] == "bundle":
                    self.assertIn(
                        "dependencies", data,
                        f"{entry['name']}: bundle missing 'dependencies' field",
                    )

    def test_bundle_dependencies_resolve_to_real_plugins(self):
        """Every catalog bundle's dependencies must resolve to real plugin files."""
        for bundle in load_bundles(CATALOG, CONSTRUCTS):
            deps = bundle.resolve_dependencies(CONSTRUCTS)
            for dep_name in deps:
                with self.subTest(bundle=bundle.name, dep=dep_name):
                    self.assertTrue(
                        Path(f"_generated/{dep_name}/.claude-plugin/plugin.json").exists(),
                        f"Bundle '{bundle.name}' dep '{dep_name}' has no generated plugin",
                    )

    def test_individual_plugin_name_matches_prefix_and_source(self):
        """Each individual plugin's name field must equal <prefix>-<source_name>."""
        for construct in CONSTRUCTS.values():
            for name in scan_source_dir(construct.source_directory):
                plugin_path = REPO_ROOT / "_generated" / f"{construct.prefix}-{name}" / ".claude-plugin" / "plugin.json"
                with self.subTest(construct=construct.prefix, name=name):
                    data = json.loads(plugin_path.read_text(encoding="utf-8"))
                    self.assertEqual(
                        data["name"], f"{construct.prefix}-{name}",
                        f"Plugin name mismatch for {construct.prefix}-{name}",
                    )


# ─── TestCatchAllBundles ──────────────────────────────────────────────────────

class TestCatchAllBundles(unittest.TestCase):
    """Code-generated bundle-<prefix>-all bundles — integration tests."""

    def test_catchall_present_for_each_construct_with_sources(self):
        """bundle-<prefix>-all must exist iff the construct has at least one source."""
        for construct in CONSTRUCTS.values():
            sources = scan_source_dir(construct.source_directory)
            catchall_path = REPO_ROOT / "_generated" / f"bundle-{construct.prefix}-all" / ".claude-plugin" / "plugin.json"
            with self.subTest(construct=construct.prefix):
                if sources:
                    self.assertTrue(
                        catchall_path.exists(),
                        f"Catch-all missing for {construct.prefix} (sources present: {sources})",
                    )
                else:
                    self.assertFalse(
                        catchall_path.exists(),
                        f"Catch-all should be absent for {construct.prefix} (no sources)",
                    )

    def test_catchall_deps_match_all_sources(self):
        """Each catch-all bundle's deps must equal exactly every instance of that construct."""
        for construct in CONSTRUCTS.values():
            sources = scan_source_dir(construct.source_directory)
            if not sources:
                continue
            catchall_path = REPO_ROOT / "_generated" / f"bundle-{construct.prefix}-all" / ".claude-plugin" / "plugin.json"
            with self.subTest(construct=construct.prefix):
                data = json.loads(catchall_path.read_text(encoding="utf-8"))
                expected = {f"{construct.prefix}-{n}" for n in sources}
                self.assertEqual(
                    set(data["dependencies"]), expected,
                    f"Catch-all for {construct.prefix} has wrong deps",
                )


# ─── TestPlatformMirrors ──────────────────────────────────────────────────────

class TestPlatformMirrors(unittest.TestCase):
    """Per-platform mirror contents — integration tests."""

    def test_codex_skills_mirror(self):
        """Codex mirror must contain a directory for every skill."""
        codex = PLATFORMS["codex"]
        if SkillConstruct not in codex.supports:
            self.skipTest("Codex does not declare skill support")
        skill = next(c for c in CONSTRUCTS.values() if isinstance(c, SkillConstruct))
        for name in scan_source_dir(skill.source_directory):
            with self.subTest(skill=name):
                mirror_dir = codex.mirror_directory / "skills" / name
                self.assertTrue(
                    mirror_dir.exists(),
                    f"Codex mirror missing skills/{name}/",
                )
                self.assertTrue(
                    (mirror_dir / "SKILL.md").exists(),
                    f"Codex mirror skills/{name}/ missing SKILL.md",
                )

    def test_gemini_skills_mirror_and_extension_manifest(self):
        """Gemini mirror must contain skills and a valid gemini-extension.json."""
        gemini = PLATFORMS["gemini"]
        skill = next(c for c in CONSTRUCTS.values() if isinstance(c, SkillConstruct))
        for name in scan_source_dir(skill.source_directory):
            with self.subTest(skill=name):
                self.assertTrue(
                    (gemini.mirror_directory / "skills" / name / "SKILL.md").exists(),
                    f"Gemini mirror missing skills/{name}/SKILL.md",
                )
        # Repo-level extension manifest (Phase 4 emission)
        manifest_path = gemini.mirror_directory / "gemini-extension.json"
        self.assertTrue(manifest_path.exists(), ".gemini/gemini-extension.json missing")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for required in ("name", "version", "description"):
            self.assertIn(required, manifest, f"gemini-extension.json missing '{required}' field")
        # Version must match MARKETPLACE.toml
        with open(MARKETPLACE_TOML, "rb") as f:
            mp = tomllib.load(f)
        self.assertEqual(manifest["name"], mp["marketplace"]["name"])
        self.assertEqual(manifest["version"], mp["marketplace"]["version"])

    def test_cursor_rules_mirror(self):
        """Cursor mirror must contain a .md file for every rule."""
        cursor = PLATFORMS["cursor"]
        rule = next(c for c in CONSTRUCTS.values() if isinstance(c, RuleConstruct))
        for name in scan_source_dir(rule.source_directory):
            with self.subTest(rule=name):
                self.assertTrue(
                    (cursor.mirror_directory / "rules" / f"{name}.md").exists(),
                    f"Cursor mirror missing rules/{name}.md",
                )

    def test_windsurf_rules_mirror(self):
        """Windsurf mirror must contain a .md file for every rule."""
        windsurf = PLATFORMS["windsurf"]
        rule = next(c for c in CONSTRUCTS.values() if isinstance(c, RuleConstruct))
        for name in scan_source_dir(rule.source_directory):
            with self.subTest(rule=name):
                self.assertTrue(
                    (windsurf.mirror_directory / "rules" / f"{name}.md").exists(),
                    f"Windsurf mirror missing rules/{name}.md",
                )

    def test_devin_skills_mirror(self):
        """Devin mirror must contain a directory for every skill.

        Devin reads rules from .cursor/ and .windsurf/ natively (empirically
        verified); we emit a Devin-native skills mirror only.
        """
        devin = PLATFORMS["devin"]
        skill = next(c for c in CONSTRUCTS.values() if isinstance(c, SkillConstruct))
        for name in scan_source_dir(skill.source_directory):
            with self.subTest(skill=name):
                self.assertTrue(
                    (devin.mirror_directory / "skills" / name / "SKILL.md").exists(),
                    f"Devin mirror missing skills/{name}/SKILL.md",
                )


# ─── TestMarketplaceJson ──────────────────────────────────────────────────────

class TestMarketplaceJson(unittest.TestCase):
    """marketplace.json schema and completeness — contract + integration tests."""

    def test_marketplace_json_exists_and_parses(self):
        """Top-level .claude-plugin/marketplace.json must exist and parse."""
        self.assertTrue(MARKETPLACE_JSON.exists(), ".claude-plugin/marketplace.json missing")
        data = load_marketplace_json()
        self.assertIsInstance(data, dict)
        self.assertIn("plugins", data)
        self.assertIn("owner", data)

    def test_marketplace_entries_have_required_fields(self):
        """Every marketplace.json entry must have all required fields."""
        required = {"name", "source", "description", "version", "author", "category"}
        manifest = load_marketplace_json()
        for entry in manifest["plugins"]:
            with self.subTest(plugin=entry["name"]):
                missing = required - set(entry.keys())
                self.assertFalse(missing, f"{entry['name']}: missing fields {missing}")
                self.assertTrue(
                    entry["source"].startswith("./"),
                    f"{entry['name']}: source must start with './'",
                )

    def test_marketplace_entries_sorted_by_category_then_name(self):
        """Entries must be sorted by (category, name) for deterministic diffs."""
        manifest = load_marketplace_json()
        entries = manifest["plugins"]
        sorted_entries = sorted(entries, key=lambda e: (e["category"], e["name"]))
        actual_order = [(e["category"], e["name"]) for e in entries]
        expected_order = [(e["category"], e["name"]) for e in sorted_entries]
        self.assertEqual(actual_order, expected_order, "marketplace.json entries are not sorted")

    def test_marketplace_lists_all_expected_plugins(self):
        """Marketplace must list exactly: all individuals + catalog bundles + catch-alls."""
        manifest = load_marketplace_json()
        actual_names = {e["name"] for e in manifest["plugins"]}

        # Individual construct plugins
        expected: set[str] = set()
        for construct in CONSTRUCTS.values():
            for name in scan_source_dir(construct.source_directory):
                expected.add(f"{construct.prefix}-{name}")

        # Catalog bundles
        for bundle in load_bundles(CATALOG, CONSTRUCTS):
            expected.add(f"bundle-{bundle.name}")

        # Code-generated catch-alls
        for construct in CONSTRUCTS.values():
            if scan_source_dir(construct.source_directory):
                expected.add(f"bundle-{construct.prefix}-all")

        self.assertEqual(actual_names, expected, "marketplace.json plugin set mismatch")


# ─── TestNoOrphanedConstructs ─────────────────────────────────────────────────

class TestNoOrphanedConstructs(unittest.TestCase):
    """Every construct instance appears in at least one bundle — integration."""

    def test_every_construct_in_at_least_one_bundle(self):
        """Every individual plugin must be reachable via some bundle."""
        all_bundle_deps: set[str] = set()
        # Catalog bundles
        for bundle in load_bundles(CATALOG, CONSTRUCTS):
            all_bundle_deps.update(bundle.resolve_dependencies(CONSTRUCTS))
        # Code-generated catch-alls (decision #23) — these include everything
        for construct in CONSTRUCTS.values():
            all_bundle_deps.update(
                f"{construct.prefix}-{n}"
                for n in scan_source_dir(construct.source_directory)
            )
        # Every instance must be in the union
        for construct in CONSTRUCTS.values():
            for name in scan_source_dir(construct.source_directory):
                plugin_name = f"{construct.prefix}-{name}"
                with self.subTest(plugin=plugin_name):
                    self.assertIn(
                        plugin_name, all_bundle_deps,
                        f"{plugin_name} is not in any bundle (catalog or catch-all)",
                    )


# ─── TestBundleValidation ─────────────────────────────────────────────────────

class TestBundleValidation(unittest.TestCase):
    """Bundle loader validation — unit tests."""

    def test_bundle_cannot_use_reserved_catchall_name(self):
        """load_bundles raises ValueError if catalog defines a reserved <prefix>-all name."""
        import tempfile
        bad_catalog = "[bundle.skill-all]\nmembers = [\"skill:foo\"]\n"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
            f.write(bad_catalog)
            f.flush()
            with self.assertRaises(ValueError, msg="Reserved catch-all name should raise ValueError"):
                load_bundles(Path(f.name), CONSTRUCTS)

    def test_bundle_requires_members(self):
        """load_bundles raises ValueError if a bundle has no 'members' field."""
        import tempfile
        bad_catalog = "[bundle.empty]\ndescription = \"no members\"\n"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
            f.write(bad_catalog)
            f.flush()
            with self.assertRaises(ValueError, msg="Bundle without members should raise ValueError"):
                load_bundles(Path(f.name), CONSTRUCTS)

    def test_bundle_member_syntax_validated(self):
        """BundleMember.from_str raises ValueError on malformed member strings."""
        with self.assertRaises(ValueError):
            BundleMember.from_str("no-colon-here")
        with self.assertRaises(ValueError):
            BundleMember.from_str(":empty-prefix")
        with self.assertRaises(ValueError):
            BundleMember.from_str("skill:")
        # Valid cases should not raise
        m = BundleMember.from_str("skill:telegram-notify")
        self.assertEqual(m.ref_type, "plugin")
        self.assertEqual(m.prefix, "skill")
        self.assertEqual(m.name, "telegram-notify")
        b = BundleMember.from_str("bundle:communication-skills")
        self.assertEqual(b.ref_type, "bundle")
        self.assertIsNone(b.prefix)


# ─── TestConstructRegistry ────────────────────────────────────────────────────

class TestConstructRegistry(unittest.TestCase):
    """CONSTRUCTS registry invariants — unit tests."""

    def test_all_prefixes_unique(self):
        """No two construct classes may share the same prefix."""
        prefixes = [c.prefix for c in CONSTRUCTS.values()]
        duplicates = [p for p in prefixes if prefixes.count(p) > 1]
        self.assertEqual(
            len(prefixes), len(set(prefixes)),
            f"Duplicate prefixes in CONSTRUCTS: {duplicates}",
        )

    def test_all_prefixes_kebab_case(self):
        """Every construct prefix must be kebab-case."""
        kebab = re.compile(r"^[a-z]+(-[a-z]+)*$")
        for construct_id, construct in CONSTRUCTS.items():
            with self.subTest(construct=construct_id):
                self.assertRegex(
                    construct.prefix, kebab,
                    f"{construct_id}: prefix '{construct.prefix}' is not kebab-case",
                )


# ─── TestPluginCount ──────────────────────────────────────────────────────────

class TestPluginCount(unittest.TestCase):
    """Plugin count formula — integration test (replaces hardcoded == 81)."""

    def test_marketplace_count_matches_expected_formula(self):
        """Count = individuals + catalog_bundles + catch-alls (one per construct with sources)."""
        manifest = load_marketplace_json()
        individuals = sum(
            len(scan_source_dir(c.source_directory)) for c in CONSTRUCTS.values()
        )
        catalog_bundles = len(load_bundles(CATALOG, CONSTRUCTS))
        catchalls = sum(
            1 for c in CONSTRUCTS.values()
            if scan_source_dir(c.source_directory)
        )
        expected = individuals + catalog_bundles + catchalls
        self.assertEqual(
            len(manifest["plugins"]), expected,
            f"Expected {expected} plugins "
            f"({individuals} individual + {catalog_bundles} catalog + {catchalls} catch-alls), "
            f"got {len(manifest['plugins'])}",
        )


# ─── TestNoSecrets ────────────────────────────────────────────────────────────

class TestNoSecrets(unittest.TestCase):
    """No tracked file may contain credential-shaped strings."""

    PATTERNS = [
        (re.compile(r"sk-[A-Za-z0-9]{32,}"), "OpenAI/Anthropic-style API key"),
        (re.compile(r"AIza[A-Za-z0-9_-]{30,}"), "Google API key"),
        (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS access key"),
        (re.compile(r"ghp_[A-Za-z0-9]{30,}"), "GitHub personal access token"),
        (re.compile(r"xox[bpars]-[A-Za-z0-9-]{10,}"), "Slack token"),
    ]

    SKIP_DIRS = {".git", "node_modules", "_dep-test", "user_resource_dump", "research"}

    def test_no_secrets_in_tracked_files(self):
        for path in REPO_ROOT.rglob("*"):
            if not path.is_file():
                continue
            if any(part in self.SKIP_DIRS for part in path.parts):
                continue
            if path.suffix in {".png", ".jpg", ".jpeg", ".svg", ".lock"}:
                continue
            try:
                content = path.read_text(encoding="utf-8", errors="ignore")
            except (OSError, UnicodeDecodeError):
                continue
            for pattern, label in self.PATTERNS:
                match = pattern.search(content)
                if match:
                    self.fail(
                        f"{path.relative_to(REPO_ROOT)} contains {label}: "
                        f"{match.group()[:20]}..."
                    )


# ─── TestGeneratorDrift ───────────────────────────────────────────────────────

class TestGeneratorDrift(unittest.TestCase):
    """Generator output must match committed content — E2E test."""

    def test_check_succeeds(self):
        result = subprocess.run(
            [sys.executable, "-m", "uv", "run",
             str(REPO_ROOT / "scripts" / "generate_manifest.py"), "--check"],
            capture_output=True,
            cwd=REPO_ROOT,
        )
        # Try direct uv invocation
        result = subprocess.run(
            ["uv", "run", str(REPO_ROOT / "scripts" / "generate_manifest.py"), "--check"],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
            timeout=120,
        )
        self.assertEqual(
            result.returncode, 0,
            f"generator --check reported drift:\n{result.stdout}\n{result.stderr}",
        )


# ─── TestMarketplaceToml ──────────────────────────────────────────────────────

class TestMarketplaceToml(unittest.TestCase):
    """MARKETPLACE.toml integrity — contract tests."""

    def test_marketplace_toml_parses(self):
        mp = load_toml(MARKETPLACE_TOML)
        self.assertIn("marketplace", mp)
        self.assertIn("owner", mp)
        self.assertIn("repository", mp)

    def test_marketplace_has_required_fields(self):
        mp = load_toml(MARKETPLACE_TOML)
        self.assertIn("name", mp["marketplace"])
        self.assertIn("version", mp["marketplace"])
        self.assertIn("description", mp["marketplace"])
        self.assertIn("name", mp["owner"])
        self.assertIn("url", mp["repository"])

    def test_marketplace_version_semver(self):
        mp = load_toml(MARKETPLACE_TOML)
        version = mp["marketplace"]["version"]
        self.assertRegex(version, r"^\d+\.\d+\.\d+$", f"version '{version}' must be semver")

    def test_catalog_toml_contains_only_bundles(self):
        """After the DI refactor, catalog.toml must contain only [bundle.*] blocks."""
        cat = load_toml(CATALOG)
        # Old schema keys must not be present
        for old_key in ("construct", "skill_domain", "rule_domain", "platform"):
            self.assertNotIn(
                old_key, cat,
                f"catalog.toml still contains old schema key '{old_key}' — "
                "DI refactor requires bundles-only catalog",
            )
        # Must have bundle entries
        self.assertIn("bundle", cat, "catalog.toml must have [bundle.*] entries")


# ─── TestActivateScripts ──────────────────────────────────────────────────────

class TestActivateScripts(unittest.TestCase):
    """Generated activate.sh scripts are well-formed — contract tests."""

    def test_activate_scripts_have_shebang(self):
        rule = next(c for c in CONSTRUCTS.values() if isinstance(c, RuleConstruct))
        for name in scan_source_dir(rule.source_directory):
            activate = REPO_ROOT / "_generated" / f"rule-{name}" / "activate.sh"
            with self.subTest(rule=name):
                first_line = activate.read_text(encoding="utf-8").splitlines()[0]
                self.assertTrue(
                    first_line.startswith("#!"),
                    f"rule-{name}/activate.sh missing shebang",
                )

    def test_activate_scripts_use_strict_bash(self):
        rule = next(c for c in CONSTRUCTS.values() if isinstance(c, RuleConstruct))
        for name in scan_source_dir(rule.source_directory):
            activate = REPO_ROOT / "_generated" / f"rule-{name}" / "activate.sh"
            with self.subTest(rule=name):
                text = activate.read_text(encoding="utf-8")
                self.assertIn(
                    "set -euo pipefail", text,
                    f"rule-{name}/activate.sh missing 'set -euo pipefail'",
                )


# ─── runner ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    unittest.main(verbosity=2)
