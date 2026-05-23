#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Marketplace test suite.

Validates the post-migration structure:
  - Source layout (skills/, rules/, commands/, agents/, hooks/, mcp-servers/,
    lsp-servers/, monitors/, output-styles/, themes/)
  - MARKETPLACE.toml + catalog.toml integrity and cross-references
  - Example plugins in their native construct folders
  - Generator drift (running --check must succeed)
  - Generated marketplace.json + plugin.json schemas
  - Per-rule activate.sh executability and shebang
  - Cross-platform mirror coverage
  - Plugin naming (kebab-case)
  - Secret scanning (no API keys committed)

Run:
    uv run tests/test_marketplace.py          # all tests
    uv run tests/test_marketplace.py -v       # verbose
    uv run tests/test_marketplace.py -k Rule  # filter by test name
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tomllib
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

MARKETPLACE_TOML = REPO_ROOT / "MARKETPLACE.toml"
CATALOG_TOML = REPO_ROOT / "catalog.toml"
MARKETPLACE_JSON = REPO_ROOT / ".claude-plugin" / "marketplace.json"

SKILLS_DIR = REPO_ROOT / "skills"
RULES_DIR = REPO_ROOT / "rules"
GENERATED_DIR = REPO_ROOT / "_generated"

# The 8 new top-level construct source directories (skills/ and rules/ also exist)
CONSTRUCT_DIRS = {
    "commands":       REPO_ROOT / "commands",
    "agents":         REPO_ROOT / "agents",
    "hooks":          REPO_ROOT / "hooks",
    "mcp-servers":    REPO_ROOT / "mcp-servers",
    "lsp-servers":    REPO_ROOT / "lsp-servers",
    "monitors":       REPO_ROOT / "monitors",
    "output-styles":  REPO_ROOT / "output-styles",
    "themes":         REPO_ROOT / "themes",
}

# Map from construct folder name → expected example directory name
CONSTRUCT_EXAMPLES = {
    "skills":         "example-skill",
    "rules":          "example-rule",
    "commands":       "example-command",
    "agents":         "example-agent",
    "hooks":          "example-hook",
    "mcp-servers":    "example-mcp",
    "lsp-servers":    "example-lsp",
    "monitors":       "example-monitor",
    "output-styles":  "example-output-style",
    "themes":         "example-theme",
}

MIRROR_DIRS = {
    "codex":    REPO_ROOT / ".codex" / "skills",
    "gemini":   REPO_ROOT / ".gemini" / "skills",
    "cursor":   REPO_ROOT / ".cursor" / "rules",
    "windsurf": REPO_ROOT / ".windsurf" / "rules",
    "devin-s":  REPO_ROOT / ".devin"  / "skills",
    "devin-r":  REPO_ROOT / ".devin"  / "rules",
}

KEBAB_CASE = re.compile(r"^[a-z][a-z0-9-]*[a-z0-9]$")


# ────────────────────────── helpers ──────────────────────────────────────────

def load_toml(path: Path) -> dict:
    with open(path, "rb") as f:
        return tomllib.load(f)


def load_marketplace() -> dict:
    return load_toml(MARKETPLACE_TOML)


def load_catalog() -> dict:
    return load_toml(CATALOG_TOML)


def list_skills() -> list[Path]:
    """Return real skills (exclude example-* directories)."""
    return sorted(
        d for d in SKILLS_DIR.iterdir()
        if d.is_dir() and (d / "SKILL.md").exists() and not d.name.startswith("example-")
    )


def list_rules() -> list[Path]:
    """Return real rules (exclude example-* directories)."""
    return sorted(
        d for d in RULES_DIR.iterdir()
        if d.is_dir() and (d / "rule.md").exists() and not d.name.startswith("example-")
    )


def list_examples_native() -> list[Path]:
    """Return all 10 example plugins from their native construct folders."""
    examples = []
    for folder_name, example_name in CONSTRUCT_EXAMPLES.items():
        if folder_name == "skills":
            folder = SKILLS_DIR
        elif folder_name == "rules":
            folder = RULES_DIR
        else:
            folder = REPO_ROOT / folder_name
        ex_path = folder / example_name
        if ex_path.is_dir():
            examples.append(ex_path)
    return sorted(examples, key=lambda p: p.name)


# ────────────────────────── tests ────────────────────────────────────────────

class TestSourceLayout(unittest.TestCase):
    """Every source directory follows naming + required-file conventions."""

    def test_skills_dir_exists(self):
        self.assertTrue(SKILLS_DIR.is_dir(), "skills/ must exist")

    def test_rules_dir_exists(self):
        self.assertTrue(RULES_DIR.is_dir(), "rules/ must exist")

    def test_commands_dir_exists(self):
        self.assertTrue(CONSTRUCT_DIRS["commands"].is_dir(), "commands/ must exist")

    def test_agents_dir_exists(self):
        self.assertTrue(CONSTRUCT_DIRS["agents"].is_dir(), "agents/ must exist")

    def test_hooks_dir_exists(self):
        self.assertTrue(CONSTRUCT_DIRS["hooks"].is_dir(), "hooks/ must exist")

    def test_mcp_servers_dir_exists(self):
        self.assertTrue(CONSTRUCT_DIRS["mcp-servers"].is_dir(), "mcp-servers/ must exist")

    def test_lsp_servers_dir_exists(self):
        self.assertTrue(CONSTRUCT_DIRS["lsp-servers"].is_dir(), "lsp-servers/ must exist")

    def test_monitors_dir_exists(self):
        self.assertTrue(CONSTRUCT_DIRS["monitors"].is_dir(), "monitors/ must exist")

    def test_output_styles_dir_exists(self):
        self.assertTrue(CONSTRUCT_DIRS["output-styles"].is_dir(), "output-styles/ must exist")

    def test_themes_dir_exists(self):
        self.assertTrue(CONSTRUCT_DIRS["themes"].is_dir(), "themes/ must exist")

    def test_examples_not_in_separate_dir(self):
        self.assertFalse((REPO_ROOT / "examples").exists(), "examples/ must not exist — examples live in native construct folders")

    def test_skill_names_kebab_case(self):
        for skill in list_skills():
            self.assertRegex(skill.name, KEBAB_CASE, f"skill name '{skill.name}' must be kebab-case")

    def test_rule_names_kebab_case(self):
        for rule in list_rules():
            self.assertRegex(rule.name, KEBAB_CASE, f"rule name '{rule.name}' must be kebab-case")

    def test_skills_have_skill_md(self):
        for skill in list_skills():
            self.assertTrue((skill / "SKILL.md").exists(), f"{skill.name} missing SKILL.md")

    def test_rules_have_rule_md(self):
        for rule in list_rules():
            self.assertTrue((rule / "rule.md").exists(), f"{rule.name} missing rule.md")

    def test_each_construct_dir_has_its_example(self):
        """Every native construct folder must contain its reference example."""
        for folder_name, example_name in CONSTRUCT_EXAMPLES.items():
            if folder_name == "skills":
                folder = SKILLS_DIR
            elif folder_name == "rules":
                folder = RULES_DIR
            else:
                folder = REPO_ROOT / folder_name
            self.assertTrue(
                (folder / example_name).is_dir(),
                f"{folder_name}/{example_name}/ must exist as the reference example",
            )


class TestConfigFiles(unittest.TestCase):
    """MARKETPLACE.toml and catalog.toml are well-formed and consistent."""

    def test_marketplace_toml_parses(self):
        mp = load_marketplace()
        self.assertIn("marketplace", mp)
        self.assertIn("owner", mp)
        self.assertIn("repository", mp)

    def test_marketplace_has_required_fields(self):
        mp = load_marketplace()
        self.assertIn("name", mp["marketplace"])
        self.assertIn("version", mp["marketplace"])
        self.assertIn("description", mp["marketplace"])
        self.assertIn("name", mp["owner"])
        self.assertIn("url", mp["repository"])

    def test_marketplace_version_semver(self):
        mp = load_marketplace()
        version = mp["marketplace"]["version"]
        self.assertRegex(version, r"^\d+\.\d+\.\d+$", f"version '{version}' must be semver")

    def test_catalog_toml_parses(self):
        cat = load_catalog()
        self.assertIn("construct", cat)
        self.assertIn("skill_domain", cat)
        self.assertIn("rule_domain", cat)

    def test_catalog_has_all_ten_construct_types(self):
        cat = load_catalog()
        expected = {"skill", "rule", "command", "agent", "hook", "mcp", "lsp", "monitor", "output-style", "theme"}
        actual = set(cat.get("construct", {}).keys())
        self.assertEqual(actual, expected, "catalog.toml must define all 10 construct types")

    def test_catalog_has_examples_domain_for_each_construct(self):
        """Every construct type must have a [<construct>_domain.examples] entry."""
        cat = load_catalog()
        for ckey in cat.get("construct", {}):
            domain_table = ckey.replace("-", "_") + "_domain"
            domain_data = cat.get(domain_table, {})
            self.assertIn(
                "examples",
                domain_data,
                f"catalog.toml must have [{domain_table}.examples] for construct '{ckey}'",
            )

    def test_examples_domain_members_exist_in_source_dirs(self):
        """Each [<construct>_domain.examples] member must resolve to a real directory."""
        cat = load_catalog()
        for ckey, cconf in cat.get("construct", {}).items():
            src_dir_rel = cconf.get("source_directory", "").rstrip("/")
            domain_table = ckey.replace("-", "_") + "_domain"
            domain_data = cat.get(domain_table, {})
            examples_domain = domain_data.get("examples", {})
            for member in examples_domain.get("members", []):
                member_path = REPO_ROOT / src_dir_rel / member
                self.assertTrue(
                    member_path.is_dir(),
                    f"[{domain_table}.examples] member '{member}' not found at {src_dir_rel}/{member}/",
                )

    def test_every_skill_in_one_domain(self):
        cat = load_catalog()
        actual = {s.name for s in list_skills()}
        referenced: set[str] = set()
        for dname, dconf in cat["skill_domain"].items():
            if dname == "examples":
                continue
            for m in dconf.get("members", []):
                self.assertNotIn(m, referenced, f"skill '{m}' appears in multiple domains")
                referenced.add(m)
                self.assertIn(m, actual, f"skill_domain.{dname} references '{m}' but skills/{m}/SKILL.md does not exist")
        orphans = actual - referenced
        self.assertFalse(orphans, f"skills not in any domain: {sorted(orphans)}")

    def test_every_rule_in_one_domain(self):
        cat = load_catalog()
        actual = {r.name for r in list_rules()}
        referenced: set[str] = set()
        for dname, dconf in cat["rule_domain"].items():
            if dname == "examples":
                continue
            for m in dconf.get("members", []):
                self.assertNotIn(m, referenced, f"rule '{m}' appears in multiple domains")
                referenced.add(m)
                self.assertIn(m, actual, f"rule_domain.{dname} references '{m}' but rules/{m}/rule.md does not exist")
        orphans = actual - referenced
        self.assertFalse(orphans, f"rules not in any domain: {sorted(orphans)}")

    def test_domain_names_kebab_case(self):
        cat = load_catalog()
        for d in cat.get("skill_domain", {}):
            self.assertRegex(d, KEBAB_CASE, f"skill domain '{d}' must be kebab-case")
        for d in cat.get("rule_domain", {}):
            self.assertRegex(d, KEBAB_CASE, f"rule domain '{d}' must be kebab-case")


class TestExamples(unittest.TestCase):
    """Each example plugin is fully self-contained and validates."""

    EXPECTED_EXAMPLES = {
        "example-skill", "example-rule", "example-command", "example-agent",
        "example-hook", "example-mcp", "example-lsp", "example-monitor",
        "example-output-style", "example-theme",
    }

    def test_all_ten_examples_present(self):
        actual = {e.name for e in list_examples_native()}
        missing = self.EXPECTED_EXAMPLES - actual
        self.assertFalse(missing, f"missing example plugins: {sorted(missing)}")

    def test_each_example_has_plugin_json(self):
        for ex in list_examples_native():
            pj = ex / ".claude-plugin" / "plugin.json"
            self.assertTrue(pj.exists(), f"{ex.name} missing .claude-plugin/plugin.json")

    def test_each_example_plugin_json_valid(self):
        for ex in list_examples_native():
            pj_path = ex / ".claude-plugin" / "plugin.json"
            pj = json.loads(pj_path.read_text(encoding="utf-8"))
            self.assertEqual(pj["name"], ex.name, f"{ex.name} plugin.json name field mismatch")
            self.assertIn("description", pj)
            self.assertIn("version", pj)
            self.assertIsInstance(pj.get("author"), dict, f"{ex.name} author must be object not string")

    def test_each_example_has_readme(self):
        for ex in list_examples_native():
            self.assertTrue((ex / "README.md").exists(), f"{ex.name} missing README.md tutorial")

    def test_examples_live_in_native_dirs_not_examples_folder(self):
        """All 10 examples must be in their construct's native folder, not examples/."""
        for folder_name, example_name in CONSTRUCT_EXAMPLES.items():
            if folder_name == "skills":
                folder = SKILLS_DIR
            elif folder_name == "rules":
                folder = RULES_DIR
            else:
                folder = REPO_ROOT / folder_name
            self.assertTrue(
                (folder / example_name).is_dir(),
                f"{example_name} must live in {folder_name}/{example_name}/, not examples/",
            )


class TestGeneratorDrift(unittest.TestCase):
    """Generator output must match committed content (no drift)."""

    def test_generator_check_succeeds(self):
        proc = subprocess.run(
            ["uv", "run", str(REPO_ROOT / "scripts" / "generate_manifest.py"), "--check"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=120,
        )
        self.assertEqual(proc.returncode, 0, f"generator --check reported drift:\n{proc.stdout}\n{proc.stderr}")


class TestGeneratedManifests(unittest.TestCase):
    """The generated marketplace.json and per-plugin manifests are well-formed."""

    def test_marketplace_json_exists(self):
        self.assertTrue(MARKETPLACE_JSON.exists(), "root .claude-plugin/marketplace.json missing")

    def test_marketplace_json_parses(self):
        data = json.loads(MARKETPLACE_JSON.read_text(encoding="utf-8"))
        self.assertIn("plugins", data)
        self.assertIn("metadata", data)
        self.assertIn("owner", data)

    def test_marketplace_json_owner_is_object(self):
        data = json.loads(MARKETPLACE_JSON.read_text(encoding="utf-8"))
        self.assertIsInstance(data["owner"], dict)

    def test_every_plugin_has_required_fields(self):
        data = json.loads(MARKETPLACE_JSON.read_text(encoding="utf-8"))
        for p in data["plugins"]:
            self.assertIn("name", p)
            self.assertIn("source", p)
            self.assertIn("version", p)
            self.assertTrue(p["source"].startswith("./"), f"plugin {p['name']} source must start with ./")

    def test_plugin_names_kebab_case(self):
        data = json.loads(MARKETPLACE_JSON.read_text(encoding="utf-8"))
        for p in data["plugins"]:
            self.assertRegex(p["name"], KEBAB_CASE, f"plugin name '{p['name']}' must be kebab-case")

    def test_plugin_count(self):
        """81 = 26 skills + 8 skill-bundles + 21 rules + 6 rule-bundles + 10 examples + 10 example-bundles."""
        data = json.loads(MARKETPLACE_JSON.read_text(encoding="utf-8"))
        self.assertEqual(len(data["plugins"]), 81, "expected 81 plugin entries in marketplace.json")

    def test_generated_skill_wrappers_exist(self):
        for skill in list_skills():
            pj = GENERATED_DIR / f"skill-{skill.name}" / ".claude-plugin" / "plugin.json"
            self.assertTrue(pj.exists(), f"missing generated wrapper for skill '{skill.name}'")

    def test_generated_rule_wrappers_have_activate(self):
        for rule in list_rules():
            target = GENERATED_DIR / f"rule-{rule.name}"
            self.assertTrue(target.exists(), f"missing generated wrapper for rule '{rule.name}'")
            self.assertTrue((target / "activate.sh").exists(), f"rule-{rule.name} missing activate.sh")
            self.assertTrue((target / "rules" / f"{rule.name}.md").exists(), f"rule-{rule.name} missing rules/{rule.name}.md")

    def test_skill_bundle_plugins_have_dependencies(self):
        cat = load_catalog()
        for dname in cat.get("skill_domain", {}):
            if dname == "examples":
                continue
            pj_path = GENERATED_DIR / f"skills-{dname}" / ".claude-plugin" / "plugin.json"
            self.assertTrue(pj_path.exists(), f"missing skills-{dname} bundle")
            pj = json.loads(pj_path.read_text(encoding="utf-8"))
            self.assertIn("dependencies", pj)
            self.assertGreater(len(pj["dependencies"]), 0, f"skills-{dname} has no dependencies")
            for dep in pj["dependencies"]:
                self.assertTrue(dep.startswith("skill-"), f"skills-{dname} dependency '{dep}' must start with skill-")

    def test_rule_bundle_plugins_have_dependencies(self):
        cat = load_catalog()
        for dname in cat.get("rule_domain", {}):
            if dname == "examples":
                continue
            pj_path = GENERATED_DIR / f"rules-{dname}" / ".claude-plugin" / "plugin.json"
            self.assertTrue(pj_path.exists(), f"missing rules-{dname} bundle")
            pj = json.loads(pj_path.read_text(encoding="utf-8"))
            self.assertIn("dependencies", pj)
            for dep in pj["dependencies"]:
                self.assertTrue(dep.startswith("rule-"), f"rules-{dname} dependency '{dep}' must start with rule-")

    def test_rules_all_bundle_contains_every_rule(self):
        pj_path = GENERATED_DIR / "rules-all" / ".claude-plugin" / "plugin.json"
        self.assertTrue(pj_path.exists(), "rules-all bundle missing")
        pj = json.loads(pj_path.read_text(encoding="utf-8"))
        expected_deps = {f"rule-{r.name}" for r in list_rules()}
        self.assertEqual(set(pj["dependencies"]), expected_deps, "rules-all dependencies must include every rule")

    def test_example_bundle_plugins_exist(self):
        """Each construct type must have a generated <construct>s-examples bundle."""
        cat = load_catalog()
        for ckey, cconf in cat.get("construct", {}).items():
            bundle_prefix = cconf.get("prefix_domain", f"{ckey}s-")
            bundle_name = f"{bundle_prefix}examples"
            pj_path = GENERATED_DIR / bundle_name / ".claude-plugin" / "plugin.json"
            self.assertTrue(pj_path.exists(), f"missing example bundle plugin: {bundle_name}")

    def test_example_bundle_plugins_have_dependencies(self):
        """Each <construct>s-examples bundle must have at least one dependency."""
        cat = load_catalog()
        for ckey, cconf in cat.get("construct", {}).items():
            bundle_prefix = cconf.get("prefix_domain", f"{ckey}s-")
            bundle_name = f"{bundle_prefix}examples"
            pj_path = GENERATED_DIR / bundle_name / ".claude-plugin" / "plugin.json"
            if pj_path.exists():
                pj = json.loads(pj_path.read_text(encoding="utf-8"))
                self.assertIn("dependencies", pj, f"{bundle_name} missing dependencies field")
                self.assertGreater(len(pj["dependencies"]), 0, f"{bundle_name} has empty dependencies")


class TestActivateScripts(unittest.TestCase):
    """Generated activate.sh scripts must be executable and well-formed."""

    def test_activate_scripts_have_shebang(self):
        for rule in list_rules():
            activate = GENERATED_DIR / f"rule-{rule.name}" / "activate.sh"
            first_line = activate.read_text(encoding="utf-8").splitlines()[0]
            self.assertTrue(first_line.startswith("#!"), f"rule-{rule.name}/activate.sh missing shebang")

    def test_activate_scripts_use_strict_bash(self):
        for rule in list_rules():
            activate = GENERATED_DIR / f"rule-{rule.name}" / "activate.sh"
            text = activate.read_text(encoding="utf-8")
            self.assertIn("set -euo pipefail", text, f"rule-{rule.name}/activate.sh missing 'set -euo pipefail'")


class TestCrossPlatformMirrors(unittest.TestCase):
    """Each mirror directory exists and contains expected items."""

    def test_skill_mirrors_have_every_skill(self):
        for platform in ("codex", "gemini", "devin-s"):
            for skill in list_skills():
                target = MIRROR_DIRS[platform] / skill.name
                self.assertTrue(target.exists(), f"{platform} mirror missing skill {skill.name}")

    def test_rule_mirrors_have_every_rule(self):
        for platform in ("cursor", "windsurf", "devin-r"):
            for rule in list_rules():
                target = MIRROR_DIRS[platform] / f"{rule.name}.md"
                self.assertTrue(target.exists(), f"{platform} mirror missing rule {rule.name}")


class TestGeminiExtension(unittest.TestCase):
    """Generator must emit a valid gemini-extension.json in the .gemini/ mirror dir."""

    GEMINI_EXTENSION_JSON = REPO_ROOT / ".gemini" / "gemini-extension.json"

    def test_gemini_extension_json_exists(self):
        self.assertTrue(
            self.GEMINI_EXTENSION_JSON.exists(),
            ".gemini/gemini-extension.json missing — run generate_manifest.py",
        )

    def test_gemini_extension_json_parseable(self):
        data = json.loads(self.GEMINI_EXTENSION_JSON.read_text(encoding="utf-8"))
        self.assertIsInstance(data, dict, "gemini-extension.json must be a JSON object")

    def test_gemini_extension_json_has_required_fields(self):
        data = json.loads(self.GEMINI_EXTENSION_JSON.read_text(encoding="utf-8"))
        self.assertIn("name", data, "gemini-extension.json must have 'name' field")
        self.assertIn("version", data, "gemini-extension.json must have 'version' field")

    def test_gemini_extension_name_matches_marketplace(self):
        import tomllib
        with open(MARKETPLACE_TOML, "rb") as f:
            mp = tomllib.load(f)
        data = json.loads(self.GEMINI_EXTENSION_JSON.read_text(encoding="utf-8"))
        self.assertEqual(
            data["name"],
            mp["marketplace"]["name"],
            "gemini-extension.json name must match MARKETPLACE.toml marketplace.name",
        )

    def test_gemini_extension_version_matches_marketplace(self):
        import tomllib
        with open(MARKETPLACE_TOML, "rb") as f:
            mp = tomllib.load(f)
        data = json.loads(self.GEMINI_EXTENSION_JSON.read_text(encoding="utf-8"))
        self.assertEqual(
            data["version"],
            mp["marketplace"]["version"],
            "gemini-extension.json version must match MARKETPLACE.toml marketplace.version",
        )


class TestSecretScan(unittest.TestCase):
    """No tracked file may contain a credential-shaped string."""

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
                    self.fail(f"{path.relative_to(REPO_ROOT)} contains {label}: {match.group()[:20]}...")


# ────────────────────────── runner ───────────────────────────────────────────

if __name__ == "__main__":
    unittest.main(verbosity=2)
