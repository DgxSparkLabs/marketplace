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
    AgentConstruct,
    HookConstruct,
    RuleConstruct,
    SkillConstruct,
    ThemeConstruct,
)
from platforms import PLATFORMS, AgentsPlatform, CodexPlatform, CursorPlatform, GeminiPlatform, WindsurfPlatform
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

    def test_codex_no_skills_mirror(self):
        """Codex skills mirror retired (D-1) — .codex/skills/ must not exist.

        SkillConstruct stays in CodexPlatform.supports so per-plugin
        .codex-plugin/plugin.json is still emitted (Phase 1.5); but the
        repo-root .codex/skills/ mirror tree is gone (Codex never read it —
        hermetic act run Q-A1 confirmation).
        """
        codex = PLATFORMS["codex"]
        # mirror_directory is intentionally kept (.codex/) so Unit 4 can write
        # .codex/agents/<n>.toml; only the skills/ subtree was retired.
        skills_dir = codex.mirror_directory / "skills"
        self.assertFalse(
            skills_dir.exists(),
            f"Codex skills mirror retired but {skills_dir} still exists",
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

    def test_devin_no_mirror_directory(self):
        """DevinPlatform.mirror_directory is None after D-1 retirement.

        Devin enumerates .agents/skills/ natively (verified hermetic act run
        Q-B1 2026-05-25); the .devin/skills/ mirror was a redundant copy.
        SkillConstruct stays in DevinPlatform.supports so a future per-plugin
        Devin manifest format can plug into Phase 1.5 without code changes.
        """
        devin = PLATFORMS["devin"]
        self.assertIsNone(
            devin.mirror_directory,
            "DevinPlatform.mirror_directory must be None after D-1 retirement",
        )
        self.assertFalse(
            (REPO_ROOT / ".devin").exists(),
            ".devin/ directory must not exist after D-1 retirement",
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


# ─── TestPerPlatformManifests ─────────────────────────────────────────────────

class TestPerPlatformManifests(unittest.TestCase):
    """Per-platform per-plugin manifests — contract + integration tests (Step 11).

    Verifies:
    - .codex-plugin/plugin.json exists for plugins whose construct is in CodexPlatform.supports
    - .codex-plugin/plugin.json does NOT exist for plugins NOT in CodexPlatform.supports
    - .cursor-plugin/plugin.json exists for plugins in CursorPlatform.supports
    - .cursor-plugin/plugin.json does NOT exist for constructs outside CursorPlatform.supports
    - All emitted per-platform manifests parse as valid JSON with required fields
    """

    def test_codex_plugin_json_emitted_for_supported_constructs(self):
        """_generated/<plugin>/.codex-plugin/plugin.json must exist iff CodexPlatform supports the construct."""
        codex = next(p for p in PLATFORMS.values() if isinstance(p, CodexPlatform))
        for construct in CONSTRUCTS.values():
            names = scan_source_dir(construct.source_directory)
            if not names:
                continue
            expected_present = type(construct) in codex.supports
            for name in names:
                plugin_name = f"{construct.prefix}-{name}"
                manifest_path = REPO_ROOT / "_generated" / plugin_name / ".codex-plugin" / "plugin.json"
                with self.subTest(plugin=plugin_name):
                    if expected_present:
                        self.assertTrue(
                            manifest_path.exists(),
                            f"{plugin_name}: .codex-plugin/plugin.json missing "
                            f"(construct {construct.prefix} is in CodexPlatform.supports)",
                        )
                    else:
                        self.assertFalse(
                            manifest_path.exists(),
                            f"{plugin_name}: .codex-plugin/plugin.json should NOT exist "
                            f"(construct {construct.prefix} is NOT in CodexPlatform.supports)",
                        )

    def test_codex_plugin_json_theme_not_emitted(self):
        """ThemeConstruct is not in CodexPlatform.supports; no .codex-plugin/ for themes."""
        codex = next(p for p in PLATFORMS.values() if isinstance(p, CodexPlatform))
        self.assertNotIn(
            ThemeConstruct, codex.supports,
            "ThemeConstruct should not be in CodexPlatform.supports",
        )
        theme = next(c for c in CONSTRUCTS.values() if isinstance(c, ThemeConstruct))
        for name in scan_source_dir(theme.source_directory):
            manifest_path = REPO_ROOT / "_generated" / f"theme-{name}" / ".codex-plugin" / "plugin.json"
            with self.subTest(theme=name):
                self.assertFalse(
                    manifest_path.exists(),
                    f"theme-{name}/.codex-plugin/plugin.json must not exist (Codex doesn't support themes)",
                )

    def test_cursor_plugin_json_emitted_for_supported_constructs(self):
        """_generated/<plugin>/.cursor-plugin/plugin.json must exist iff CursorPlatform supports the construct."""
        cursor = next(p for p in PLATFORMS.values() if isinstance(p, CursorPlatform))
        for construct in CONSTRUCTS.values():
            names = scan_source_dir(construct.source_directory)
            if not names:
                continue
            expected_present = type(construct) in cursor.supports
            for name in names:
                plugin_name = f"{construct.prefix}-{name}"
                manifest_path = REPO_ROOT / "_generated" / plugin_name / ".cursor-plugin" / "plugin.json"
                with self.subTest(plugin=plugin_name):
                    if expected_present:
                        self.assertTrue(
                            manifest_path.exists(),
                            f"{plugin_name}: .cursor-plugin/plugin.json missing "
                            f"(construct {construct.prefix} is in CursorPlatform.supports)",
                        )
                    else:
                        self.assertFalse(
                            manifest_path.exists(),
                            f"{plugin_name}: .cursor-plugin/plugin.json should NOT exist "
                            f"(construct {construct.prefix} is NOT in CursorPlatform.supports)",
                        )

    def test_codex_plugin_json_valid_schema(self):
        """Every emitted .codex-plugin/plugin.json must parse and have required Codex fields."""
        codex = next(p for p in PLATFORMS.values() if isinstance(p, CodexPlatform))
        for construct in CONSTRUCTS.values():
            if type(construct) not in codex.supports:
                continue
            for name in scan_source_dir(construct.source_directory):
                plugin_name = f"{construct.prefix}-{name}"
                manifest_path = REPO_ROOT / "_generated" / plugin_name / ".codex-plugin" / "plugin.json"
                with self.subTest(plugin=plugin_name):
                    data = json.loads(manifest_path.read_text(encoding="utf-8"))
                    for required in ("name", "version", "description"):
                        self.assertIn(
                            required, data,
                            f"{plugin_name}/.codex-plugin/plugin.json missing '{required}' field",
                        )
                    self.assertEqual(
                        data["name"], plugin_name,
                        f"{plugin_name}/.codex-plugin/plugin.json name mismatch",
                    )

    def test_cursor_plugin_json_valid_schema(self):
        """Every emitted .cursor-plugin/plugin.json must parse and have required Cursor fields."""
        cursor = next(p for p in PLATFORMS.values() if isinstance(p, CursorPlatform))
        for construct in CONSTRUCTS.values():
            if type(construct) not in cursor.supports:
                continue
            for name in scan_source_dir(construct.source_directory):
                plugin_name = f"{construct.prefix}-{name}"
                manifest_path = REPO_ROOT / "_generated" / plugin_name / ".cursor-plugin" / "plugin.json"
                with self.subTest(plugin=plugin_name):
                    data = json.loads(manifest_path.read_text(encoding="utf-8"))
                    self.assertIn(
                        "name", data,
                        f"{plugin_name}/.cursor-plugin/plugin.json missing 'name' field",
                    )
                    self.assertEqual(
                        data["name"], plugin_name,
                        f"{plugin_name}/.cursor-plugin/plugin.json name mismatch",
                    )

    def test_cursor_skill_plugin_json_has_display_fields(self):
        """Every Cursor SkillConstruct plugin.json must carry name+version+description+skills.

        Without all four fields, Cursor's slash-popup renderer falls back to
        install metadata (commit SHA) and produces a mangled display
        (docs/research/qa-bug-fixes-2026-05/RESEARCH.md Bug 3, 2026-05-25 QA).
        """
        cursor = next(p for p in PLATFORMS.values() if isinstance(p, CursorPlatform))
        skill = next(c for c in CONSTRUCTS.values() if isinstance(c, SkillConstruct))
        required = {"name", "version", "description", "skills"}
        for name in scan_source_dir(skill.source_directory):
            plugin_name = f"skill-{name}"
            manifest_path = REPO_ROOT / "_generated" / plugin_name / ".cursor-plugin" / "plugin.json"
            with self.subTest(plugin=plugin_name):
                data = json.loads(manifest_path.read_text(encoding="utf-8"))
                missing = required - set(data.keys())
                self.assertFalse(
                    missing,
                    f"{plugin_name}/.cursor-plugin/plugin.json missing required "
                    f"display fields {missing}; Cursor popup will mangle without these",
                )


# ─── TestRootLevelManifests ───────────────────────────────────────────────────

class TestRootLevelManifests(unittest.TestCase):
    """Root-level generated manifests — integration tests (Step 11).

    Verifies:
    - gemini-extension.json exists at repo root and has valid JSON with required fields
    - .cursor-plugin/marketplace.json exists at repo root and has valid JSON with plugins array
    """

    def test_root_gemini_extension_json_exists(self):
        """gemini-extension.json must exist at repo root (enables GitHub URL install)."""
        self.assertTrue(
            (REPO_ROOT / "gemini-extension.json").exists(),
            "gemini-extension.json missing at repo root — required for "
            "gemini extensions install https://github.com/... --consent",
        )

    def test_root_gemini_extension_json_valid(self):
        """Root gemini-extension.json must parse and carry required fields."""
        path = REPO_ROOT / "gemini-extension.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        for required in ("name", "version", "description"):
            with self.subTest(field=required):
                self.assertIn(
                    required, data,
                    f"gemini-extension.json missing '{required}' field",
                )

    def test_root_gemini_extension_json_matches_gemini_dir_copy(self):
        """Root gemini-extension.json must be byte-identical to .gemini/gemini-extension.json."""
        root_copy = (REPO_ROOT / "gemini-extension.json").read_bytes()
        mirror_copy = (REPO_ROOT / ".gemini" / "gemini-extension.json").read_bytes()
        self.assertEqual(
            root_copy, mirror_copy,
            "Root gemini-extension.json differs from .gemini/gemini-extension.json — "
            "they must be byte-identical (generator should shutil.copy2 the mirror)",
        )

    def test_cursor_marketplace_json_exists(self):
        """.cursor-plugin/marketplace.json must exist at repo root (enables Cursor team-import)."""
        self.assertTrue(
            (REPO_ROOT / ".cursor-plugin" / "marketplace.json").exists(),
            ".cursor-plugin/marketplace.json missing at repo root — required for "
            "Cursor team-marketplace import (Dashboard → Settings → Plugins → Import)",
        )

    def test_cursor_marketplace_json_valid(self):
        """.cursor-plugin/marketplace.json must parse and have name + plugins array."""
        path = REPO_ROOT / ".cursor-plugin" / "marketplace.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        self.assertIn("name", data, ".cursor-plugin/marketplace.json missing 'name' field")
        self.assertIn("plugins", data, ".cursor-plugin/marketplace.json missing 'plugins' array")
        self.assertIsInstance(data["plugins"], list)
        self.assertGreater(len(data["plugins"]), 0, ".cursor-plugin/marketplace.json has empty plugins list")

    def test_cursor_marketplace_json_entries_have_required_fields(self):
        """Every entry in .cursor-plugin/marketplace.json must have name and source."""
        path = REPO_ROOT / ".cursor-plugin" / "marketplace.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        for entry in data["plugins"]:
            with self.subTest(plugin=entry.get("name", "<missing>")):
                self.assertIn("name", entry)
                self.assertIn("source", entry)
                self.assertTrue(entry["source"].startswith("./"))

    def test_cursor_marketplace_lists_cursor_supported_plugins(self):
        """Every construct in CursorPlatform.supports must have entries in .cursor-plugin/marketplace.json."""
        cursor = next(p for p in PLATFORMS.values() if isinstance(p, CursorPlatform))
        path = REPO_ROOT / ".cursor-plugin" / "marketplace.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        listed_names = {e["name"] for e in data["plugins"]}
        for construct in CONSTRUCTS.values():
            if type(construct) not in cursor.supports:
                continue
            for name in scan_source_dir(construct.source_directory):
                plugin_name = f"{construct.prefix}-{name}"
                with self.subTest(plugin=plugin_name):
                    self.assertIn(
                        plugin_name, listed_names,
                        f"{plugin_name} missing from .cursor-plugin/marketplace.json "
                        f"(construct {construct.prefix} is in CursorPlatform.supports)",
                    )


# ─── TestAgentsMirror ─────────────────────────────────────────────────────────

class TestAgentsMirror(unittest.TestCase):
    """AgentsPlatform .agents/ mirror — integration tests (Step 11).

    Verifies:
    - .agents/skills/<name>/SKILL.md exists for every source skill
    - No .claude-plugin/ leaked into .agents/ mirror
    - No .codex-plugin/ leaked into .agents/ mirror
    """

    def test_agents_skills_mirror_exists(self):
        """.agents/skills/<name>/SKILL.md must exist for every source skill."""
        agents = next(p for p in PLATFORMS.values() if isinstance(p, AgentsPlatform))
        skill = next(c for c in CONSTRUCTS.values() if isinstance(c, SkillConstruct))
        for name in scan_source_dir(skill.source_directory):
            with self.subTest(skill=name):
                skill_md = agents.mirror_directory / "skills" / name / "SKILL.md"
                self.assertTrue(
                    skill_md.exists(),
                    f".agents/skills/{name}/SKILL.md missing — "
                    "Windsurf/Cursor/Devin can't discover this skill",
                )

    def test_agents_skills_no_claude_plugin_leak(self):
        """No .claude-plugin/ directory must appear under .agents/skills/."""
        agents = next(p for p in PLATFORMS.values() if isinstance(p, AgentsPlatform))
        skills_root = agents.mirror_directory / "skills"
        if not skills_root.exists():
            self.skipTest(".agents/skills/ does not exist")
        leaked = [
            str(p.relative_to(agents.mirror_directory))
            for p in skills_root.rglob(".claude-plugin")
            if p.is_dir()
        ]
        self.assertEqual(
            leaked, [],
            f".claude-plugin/ leaked into .agents/ mirror: {leaked}",
        )

    def test_agents_skills_no_codex_plugin_leak(self):
        """No .codex-plugin/ directory must appear under .agents/skills/."""
        agents = next(p for p in PLATFORMS.values() if isinstance(p, AgentsPlatform))
        skills_root = agents.mirror_directory / "skills"
        if not skills_root.exists():
            self.skipTest(".agents/skills/ does not exist")
        leaked = [
            str(p.relative_to(agents.mirror_directory))
            for p in skills_root.rglob(".codex-plugin")
            if p.is_dir()
        ]
        self.assertEqual(
            leaked, [],
            f".codex-plugin/ leaked into .agents/ mirror: {leaked}",
        )


# ─── TestAgentsPluginsMarketplace ─────────────────────────────────────────────

class TestAgentsPluginsMarketplace(unittest.TestCase):
    """Phase 5.5 .agents/plugins/marketplace.json (Unit 6 / D-14 / A5).

    Codex documents .agents/plugins/marketplace.json as the canonical
    marketplace path per developers.openai.com/codex/plugins/build
    (2026-05-25). We emit it as a byte-identical copy of
    .claude-plugin/marketplace.json (the legacy-compat path); both remain
    valid until Codex deprecates the legacy form.
    """

    def test_agents_plugins_marketplace_exists(self):
        self.assertTrue(
            (REPO_ROOT / ".agents" / "plugins" / "marketplace.json").exists(),
            ".agents/plugins/marketplace.json missing — Codex canonical path "
            "per developers.openai.com/codex/plugins/build (2026-05-25)",
        )

    def test_agents_plugins_marketplace_byte_identical(self):
        canonical = (REPO_ROOT / ".agents" / "plugins" / "marketplace.json").read_bytes()
        legacy = (REPO_ROOT / ".claude-plugin" / "marketplace.json").read_bytes()
        self.assertEqual(
            canonical, legacy,
            ".agents/plugins/marketplace.json must be byte-identical to "
            ".claude-plugin/marketplace.json (Phase 5.5 is a copy, not a re-emit)",
        )


# ─── TestWindsurfHooksMirror ──────────────────────────────────────────────────

class TestWindsurfHooksMirror(unittest.TestCase):
    """Windsurf hooks at .windsurf/hooks.json (Unit 5 / A10).

    Per docs.windsurf.com/windsurf/cascade/hooks (2026-05-25): Windsurf reads
    .windsurf/hooks.json at the workspace root (no hooks/ subdir, unlike
    Gemini). Single hook plugin today; multi-plugin merge deferred.
    """

    # Claude-style event names (PascalCase) that Windsurf does NOT understand.
    CLAUDE_EVENT_NAMES = frozenset({
        "UserPromptSubmit", "PreToolUse", "PostToolUse", "Notification",
        "Stop", "SubagentStop", "SessionStart", "SessionEnd", "PreCompact",
    })

    def test_windsurf_hooks_json_exists(self):
        windsurf = next(p for p in PLATFORMS.values() if isinstance(p, WindsurfPlatform))
        hooks_json = windsurf.mirror_directory / "hooks.json"
        self.assertTrue(hooks_json.exists(), ".windsurf/hooks.json missing")
        data = json.loads(hooks_json.read_text(encoding="utf-8"))
        self.assertIn(
            "hooks", data,
            ".windsurf/hooks.json must contain top-level 'hooks' key",
        )

    def test_windsurf_hooks_use_snake_case_event_names(self):
        """No Claude-style PascalCase event names may appear in .windsurf/hooks.json.

        Windsurf uses snake_case events (pre_user_prompt, pre_tool_use, etc.)
        per docs.windsurf.com/windsurf/cascade/hooks (2026-05-25). Claude
        event names load silently but never fire
        (docs/research/qa-bug-fixes-2026-05/RESEARCH.md sanity-check #5,
        QA 2026-05-25).
        """
        windsurf = next(p for p in PLATFORMS.values() if isinstance(p, WindsurfPlatform))
        hooks_json = windsurf.mirror_directory / "hooks.json"
        if not hooks_json.exists():
            self.skipTest(".windsurf/hooks.json does not exist")
        data = json.loads(hooks_json.read_text(encoding="utf-8"))
        event_keys = set((data.get("hooks") or {}).keys())
        leaked = event_keys & self.CLAUDE_EVENT_NAMES
        self.assertFalse(
            leaked,
            f".windsurf/hooks.json contains Claude-style event names {leaked}; "
            f"Windsurf requires snake_case events (pre_user_prompt, etc.) and "
            f"the file's hooks will never fire as-is",
        )
        # Conversely every event key must be lowercase snake_case
        # (Windsurf docs enumerate only snake_case events).
        for key in event_keys:
            with self.subTest(event=key):
                self.assertRegex(
                    key, r"^[a-z][a-z_]*$",
                    f"Windsurf event '{key}' is not snake_case",
                )

    def test_windsurf_hook_entries_are_flat(self):
        """Each Windsurf hook entry must be a flat dict, not Claude's nested ``{"hooks": [...]}``.

        Per docs.windsurf.com/windsurf/cascade/hooks (2026-05-25): the shape
        is ``{"hooks": {<event>: [{"command": "..."}]}}`` — no inner ``hooks``
        key. Claude's doubly-nested shape lands as opaque junk to Windsurf's
        parser.
        """
        windsurf = next(p for p in PLATFORMS.values() if isinstance(p, WindsurfPlatform))
        hooks_json = windsurf.mirror_directory / "hooks.json"
        if not hooks_json.exists():
            self.skipTest(".windsurf/hooks.json does not exist")
        data = json.loads(hooks_json.read_text(encoding="utf-8"))
        for event, entries in (data.get("hooks") or {}).items():
            for i, entry in enumerate(entries):
                with self.subTest(event=event, idx=i):
                    self.assertIsInstance(entry, dict, f"{event}[{i}] not a dict")
                    self.assertNotIn(
                        "hooks", entry,
                        f"{event}[{i}] has Claude-style nested 'hooks' key; "
                        f"Windsurf requires flat entries with command/powershell",
                    )
                    self.assertTrue(
                        "command" in entry or "powershell" in entry,
                        f"{event}[{i}] missing required command/powershell",
                    )


class TestHooksToWindsurfConverter(unittest.TestCase):
    """Unit tests for scripts/converters/hooks_to_windsurf.py."""

    SAMPLE = (
        '{"description": "x",'
        '"hooks": {"UserPromptSubmit": [{"hooks": ['
        '{"type": "command", "command": "echo hi"}'
        ']}]}}'
    )

    def setUp(self):
        from converters.hooks_to_windsurf import claude_hooks_to_windsurf_hooks  # noqa: E402
        self.convert = claude_hooks_to_windsurf_hooks

    def test_event_renamed_and_flattened(self):
        out = json.loads(self.convert(self.SAMPLE))
        self.assertEqual(
            out, {"hooks": {"pre_user_prompt": [{"command": "echo hi"}]}}
        )

    def test_unknown_event_dropped(self):
        src = '{"hooks": {"Stop": [{"hooks": [{"type": "command", "command": "x"}]}]}}'
        out = json.loads(self.convert(src))
        self.assertEqual(out, {"hooks": {}})

    def test_no_claude_keys_leak(self):
        out = self.convert(self.SAMPLE)
        for forbidden in ("UserPromptSubmit", '"type":', "description"):
            self.assertNotIn(
                forbidden, out,
                f"Windsurf output must not retain '{forbidden}'",
            )


# ─── TestCodexAgentsMirror / TestMdToTomlConverter ───────────────────────────

class TestCodexAgentsMirror(unittest.TestCase):
    """Codex sub-agents at .codex/agents/<n>.toml (Unit 4 / A4).

    Source is Claude-style markdown (D-16); .codex/agents/<n>.toml is the
    converted Codex shape per developers.openai.com/codex/subagents/
    (2026-05-25). Required Codex fields: name, description,
    developer_instructions.
    """

    def test_codex_agents_toml_exists(self):
        codex = next(p for p in PLATFORMS.values() if isinstance(p, CodexPlatform))
        agent = next(c for c in CONSTRUCTS.values() if isinstance(c, AgentConstruct))
        for name in scan_source_dir(agent.source_directory):
            src_agents = agent.source_directory / name / "agents"
            if not src_agents.exists():
                continue
            for agent_md in sorted(src_agents.glob("*.md")):
                with self.subTest(agent_plugin=name, agent_file=agent_md.name):
                    toml_path = codex.mirror_directory / "agents" / f"{agent_md.stem}.toml"
                    self.assertTrue(
                        toml_path.exists(),
                        f".codex/agents/{agent_md.stem}.toml missing for source "
                        f"agents/{name}/agents/{agent_md.name}",
                    )

    def test_codex_agents_toml_valid(self):
        """Every emitted .codex/agents/<n>.toml parses + has required Codex fields."""
        codex = next(p for p in PLATFORMS.values() if isinstance(p, CodexPlatform))
        agents_dir = codex.mirror_directory / "agents"
        if not agents_dir.exists():
            self.skipTest(".codex/agents/ does not exist (no agent sources)")
        toml_files = sorted(agents_dir.glob("*.toml"))
        self.assertGreater(len(toml_files), 0, ".codex/agents/ has no .toml files")
        for toml_path in toml_files:
            with self.subTest(toml=toml_path.name):
                data = tomllib.loads(toml_path.read_text(encoding="utf-8"))
                for required in ("name", "description", "developer_instructions"):
                    self.assertIn(
                        required, data,
                        f"{toml_path.name}: required Codex field '{required}' missing",
                    )

    def test_codex_agents_toml_roundtrip(self):
        """Known input (notebook-reviewer) round-trips through tomllib with expected fields."""
        codex = next(p for p in PLATFORMS.values() if isinstance(p, CodexPlatform))
        toml_path = codex.mirror_directory / "agents" / "notebook-reviewer.toml"
        if not toml_path.exists():
            self.skipTest("notebook-reviewer.toml not present")
        data = tomllib.loads(toml_path.read_text(encoding="utf-8"))
        self.assertEqual(data["name"], "notebook-reviewer")
        self.assertTrue(
            data["description"].startswith("Reviews"),
            f"description starts with: {data['description'][:40]!r}",
        )
        self.assertIn("peer reviewer", data["developer_instructions"])
        self.assertEqual(data.get("tools"), ["Read", "Grep", "Glob"])


class TestMdToTomlConverter(unittest.TestCase):
    """Unit tests for scripts/converters/md_to_toml.py (Unit 4)."""

    SAMPLE = (
        "---\n"
        "name: notebook-reviewer\n"
        "description: Reviews a lab notebook entry as a skeptical peer reviewer.\n"
        "tools: Read, Grep, Glob\n"
        "---\n"
        "\n"
        "You are a peer reviewer for laboratory notebook entries.\n"
        "\n"
        "Apply skeptical eye.\n"
    )

    def setUp(self):
        # Imported here so any import-time errors fail loudly in this class only.
        from converters.md_to_toml import claude_agent_md_to_codex_toml  # noqa: E402
        self.convert = claude_agent_md_to_codex_toml

    def test_required_fields_emitted(self):
        out = self.convert(self.SAMPLE)
        data = tomllib.loads(out)
        self.assertEqual(data["name"], "notebook-reviewer")
        self.assertTrue(data["description"].startswith("Reviews"))
        self.assertIn("peer reviewer", data["developer_instructions"])

    def test_tools_parsed_as_array(self):
        out = self.convert(self.SAMPLE)
        data = tomllib.loads(out)
        self.assertEqual(data["tools"], ["Read", "Grep", "Glob"])

    def test_missing_frontmatter_raises(self):
        with self.assertRaises(ValueError):
            self.convert("no frontmatter here")

    def test_missing_required_name_raises(self):
        bad = "---\ndescription: x\n---\nbody"
        with self.assertRaises(ValueError):
            self.convert(bad)

    def test_round_trip_on_real_example(self):
        """The committed agent source converts and re-parses cleanly."""
        src_path = REPO_ROOT / "agents" / "example" / "agents" / "notebook-reviewer.md"
        if not src_path.exists():
            self.skipTest(f"{src_path} not present")
        out = self.convert(src_path.read_text(encoding="utf-8"))
        data = tomllib.loads(out)  # round-trips through stdlib TOML reader
        self.assertEqual(data["name"], "notebook-reviewer")


# ─── TestGeminiAgentsMirror / TestGeminiHooksMirror ──────────────────────────

class TestGeminiAgentsMirror(unittest.TestCase):
    """Gemini sub-agents at .gemini/agents/<n>.md (Unit 3 / A3).

    Per geminicli.com/docs/extensions/reference/ (2026-05-25): sub-agents are
    .md files inside the agents/ directory of the extension root (.gemini/).
    """

    def test_gemini_agents_mirror_exists(self):
        gemini = next(p for p in PLATFORMS.values() if isinstance(p, GeminiPlatform))
        agent = next(c for c in CONSTRUCTS.values() if isinstance(c, AgentConstruct))
        for name in scan_source_dir(agent.source_directory):
            src_agents = agent.source_directory / name / "agents"
            if not src_agents.exists():
                continue
            for agent_md in sorted(src_agents.glob("*.md")):
                with self.subTest(agent_plugin=name, agent_file=agent_md.name):
                    mirrored = gemini.mirror_directory / "agents" / agent_md.name
                    self.assertTrue(
                        mirrored.exists(),
                        f".gemini/agents/{agent_md.name} missing for source "
                        f"agents/{name}/agents/{agent_md.name}",
                    )

    def test_gemini_agents_tools_is_yaml_array(self):
        """Emitted Gemini sub-agent frontmatter must have ``tools`` as a YAML array.

        Per geminicli.com/docs/core/subagents/ (2026-05-25), the Gemini
        sub-agent loader requires the ``tools`` field as an array. Our
        canonical Claude source uses a comma-separated string; without
        per-platform conversion the file is silently skipped by Gemini's
        /agents discovery (docs/research/qa-bug-fixes-2026-05/RESEARCH.md
        Bug 2, QA 2026-05-25).
        """
        gemini = next(p for p in PLATFORMS.values() if isinstance(p, GeminiPlatform))
        agents_dir = gemini.mirror_directory / "agents"
        if not agents_dir.exists():
            self.skipTest(".gemini/agents/ does not exist")
        files = sorted(agents_dir.glob("*.md"))
        self.assertGreater(len(files), 0, ".gemini/agents/ has no .md files")
        for md_path in files:
            with self.subTest(agent=md_path.name):
                text = md_path.read_text(encoding="utf-8")
                self.assertTrue(
                    text.startswith("---\n"),
                    f"{md_path.name}: missing YAML frontmatter opener",
                )
                end = text.find("\n---", 4)
                self.assertGreater(end, 0, f"{md_path.name}: frontmatter unterminated")
                fm = text[4:end]
                # If the source agent declared any tools, the emitted file
                # must render them as a YAML array (one ``  - <tool>`` line
                # per tool), never as the Claude-style scalar "tools: a, b, c".
                lines = fm.splitlines()
                tools_line_idx = next(
                    (i for i, ln in enumerate(lines) if ln.strip().startswith("tools:")),
                    None,
                )
                if tools_line_idx is None:
                    continue  # tools field absent: legal per Gemini docs
                tools_value = lines[tools_line_idx].split(":", 1)[1].strip()
                self.assertEqual(
                    tools_value, "",
                    f"{md_path.name}: 'tools:' must be followed by a YAML "
                    f"array on subsequent lines (got inline scalar "
                    f"{tools_value!r}); Gemini /agents will skip the file",
                )
                # At least one '  - <tool>' line should follow.
                array_items = [
                    ln for ln in lines[tools_line_idx + 1:]
                    if ln.startswith("  - ")
                ]
                self.assertGreater(
                    len(array_items), 0,
                    f"{md_path.name}: 'tools:' present but no '  - <tool>' "
                    f"array items follow",
                )


class TestMdToGeminiMdConverter(unittest.TestCase):
    """Unit tests for scripts/converters/md_to_gemini_md.py."""

    SAMPLE = (
        "---\n"
        "name: notebook-reviewer\n"
        "description: Reviews a lab notebook entry as a skeptical peer reviewer.\n"
        "tools: Read, Grep, Glob\n"
        "---\n"
        "\n"
        "You are a peer reviewer for laboratory notebook entries.\n"
    )

    def setUp(self):
        from converters.md_to_gemini_md import claude_agent_md_to_gemini_md  # noqa: E402
        self.convert = claude_agent_md_to_gemini_md

    def test_tools_emitted_as_yaml_array(self):
        out = self.convert(self.SAMPLE)
        self.assertIn("tools:\n  - Read\n  - Grep\n  - Glob\n", out)
        self.assertNotIn("tools: Read, Grep, Glob", out)

    def test_required_fields_preserved(self):
        out = self.convert(self.SAMPLE)
        self.assertIn("name: notebook-reviewer", out)
        self.assertIn(
            "description: Reviews a lab notebook entry as a skeptical peer reviewer.",
            out,
        )
        self.assertIn("You are a peer reviewer", out)

    def test_missing_frontmatter_raises(self):
        with self.assertRaises(ValueError):
            self.convert("no frontmatter here")

    def test_missing_required_name_raises(self):
        bad = "---\ndescription: x\n---\nbody"
        with self.assertRaises(ValueError):
            self.convert(bad)


class TestGeminiHooksMirror(unittest.TestCase):
    """Gemini hooks at .gemini/hooks/hooks.json (Unit 3 / A9).

    Per geminicli.com/docs/extensions/reference/ (2026-05-25): hooks live at
    hooks/hooks.json inside the extension root. Single hook plugin today —
    multi-plugin merge semantics deferred until a second hook plugin lands.
    """

    def test_gemini_hooks_json_exists(self):
        gemini = next(p for p in PLATFORMS.values() if isinstance(p, GeminiPlatform))
        hooks_json = gemini.mirror_directory / "hooks" / "hooks.json"
        self.assertTrue(hooks_json.exists(), ".gemini/hooks/hooks.json missing")
        # Must parse as valid JSON
        data = json.loads(hooks_json.read_text(encoding="utf-8"))
        self.assertIn(
            "hooks", data,
            ".gemini/hooks/hooks.json must contain top-level 'hooks' key",
        )


# ─── TestCursorAgentsMirror ──────────────────────────────────────────────────

class TestCursorAgentsMirror(unittest.TestCase):
    """Cursor workspace-level sub-agents at .cursor/agents/<n>.md (Unit 2 / A2).

    Cursor reads .cursor/agents/<n>.md natively per cursor.com/docs/agent/subagents
    (2026-05-25). One AgentConstruct plugin can contain multiple sub-agent .md
    files; each lands in .cursor/agents/.
    """

    def test_cursor_agents_mirror_exists(self):
        """.cursor/agents/<n>.md must exist for every source sub-agent .md."""
        cursor = next(p for p in PLATFORMS.values() if isinstance(p, CursorPlatform))
        agent = next(c for c in CONSTRUCTS.values() if isinstance(c, AgentConstruct))
        for name in scan_source_dir(agent.source_directory):
            src_agents = agent.source_directory / name / "agents"
            if not src_agents.exists():
                continue
            for agent_md in sorted(src_agents.glob("*.md")):
                with self.subTest(agent_plugin=name, agent_file=agent_md.name):
                    mirrored = cursor.mirror_directory / "agents" / agent_md.name
                    self.assertTrue(
                        mirrored.exists(),
                        f".cursor/agents/{agent_md.name} missing for source "
                        f"agents/{name}/agents/{agent_md.name}",
                    )


# ─── TestAgentsRulesMirror ────────────────────────────────────────────────────

class TestAgentsRulesMirror(unittest.TestCase):
    """AgentsPlatform .agents/rules/ mirror (Unit 1 / D-12).

    Forward-looking convergence: no platform reads .agents/rules/ today
    (verified Q-R1/Q-R2 2026-05-25), but Cursor 2.7+ / Windsurf 2.0 are
    credible adopters. Emit now so we are already in place when one of
    them flips. Raw rule.md is copied; no frontmatter conversion.
    """

    def test_rules_mirror_exists(self):
        """.agents/rules/<name>.md must exist for every source rule."""
        agents = next(p for p in PLATFORMS.values() if isinstance(p, AgentsPlatform))
        rule = next(c for c in CONSTRUCTS.values() if isinstance(c, RuleConstruct))
        for name in scan_source_dir(rule.source_directory):
            with self.subTest(rule=name):
                rule_md = agents.mirror_directory / "rules" / f"{name}.md"
                self.assertTrue(
                    rule_md.exists(),
                    f".agents/rules/{name}.md missing — forward-looking emission "
                    "must cover every source rule",
                )


# ─── TestMirrorHygiene ────────────────────────────────────────────────────────

class TestMirrorHygiene(unittest.TestCase):
    """Mirror directory hygiene — negative tests (Step 11, Issue 8).

    Verifies no cross-platform manifest directories leaked into mirror dirs.
    """

    # .devin removed post-D-1 (DevinPlatform.mirror_directory = None).
    # .codex retained — mirror_directory still set (.codex/agents/ in Unit 4).
    MIRROR_DIRS_TO_CHECK = [".codex", ".gemini", ".agents"]

    def _find_leaked_dirs(self, mirror_root: Path, leak_pattern: str) -> list[str]:
        """Walk mirror_root and return paths of any leak_pattern subdirs."""
        if not mirror_root.exists():
            return []
        return [
            str(p.relative_to(REPO_ROOT))
            for p in mirror_root.rglob(leak_pattern)
            if p.is_dir()
        ]

    def test_no_claude_plugin_in_mirror_dirs(self):
        """No .claude-plugin/ must appear inside .codex/, .gemini/, .devin/, .agents/ mirrors."""
        for mirror_name in self.MIRROR_DIRS_TO_CHECK:
            mirror_root = REPO_ROOT / mirror_name
            with self.subTest(mirror=mirror_name):
                leaked = self._find_leaked_dirs(mirror_root, ".claude-plugin")
                self.assertEqual(
                    leaked, [],
                    f".claude-plugin/ leaked into {mirror_name}/: {leaked}",
                )

    def test_no_codex_plugin_in_mirror_dirs(self):
        """No .codex-plugin/ must appear inside .gemini/, .agents/ mirrors."""
        for mirror_name in [".gemini", ".agents"]:
            mirror_root = REPO_ROOT / mirror_name
            with self.subTest(mirror=mirror_name):
                leaked = self._find_leaked_dirs(mirror_root, ".codex-plugin")
                self.assertEqual(
                    leaked, [],
                    f".codex-plugin/ leaked into {mirror_name}/: {leaked}",
                )

    def test_no_cursor_plugin_in_mirror_dirs(self):
        """No .cursor-plugin/ must appear inside .codex/, .gemini/, .devin/, .agents/ mirrors."""
        for mirror_name in self.MIRROR_DIRS_TO_CHECK:
            mirror_root = REPO_ROOT / mirror_name
            with self.subTest(mirror=mirror_name):
                leaked = self._find_leaked_dirs(mirror_root, ".cursor-plugin")
                self.assertEqual(
                    leaked, [],
                    f".cursor-plugin/ leaked into {mirror_name}/: {leaked}",
                )


# ─── runner ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    unittest.main(verbosity=2)
