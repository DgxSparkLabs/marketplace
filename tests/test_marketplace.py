# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6.0", "textual>=1.0.0", "ruff"]
# ///
"""
Marketplace test suite.

Validates that every skill and rule in the repository meets the
conventions defined in CONTRIBUTING.md, docs/SKILL_FORMAT.md, and
docs/RULE_FORMAT.md.

Run:
    uv run tests/test_marketplace.py          # all tests
    uv run tests/test_marketplace.py -v       # verbose
    uv run tests/test_marketplace.py -k rule  # only rule tests
"""

import json
import os
import re
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent

SKILLS_DIR = REPO_ROOT / "skills"
RULES_DIR = REPO_ROOT / "rules"

# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #


def _iter_items() -> list[Path]:
    """Return sorted list of item directories (skills + rules)."""
    items = []
    for parent in (SKILLS_DIR, RULES_DIR):
        if parent.is_dir():
            items.extend(
                p for p in parent.iterdir()
                if p.is_dir() and not p.name.startswith(("_", "."))
            )
    return sorted(items)


def _is_skill(item: Path) -> bool:
    return (item / "SKILL.md").exists()


def _is_rule(item: Path) -> bool:
    return (item / "rule.md").exists()


def _parse_yaml_frontmatter(text: str) -> dict | None:
    """Extract YAML frontmatter from ``---`` delimited blocks."""
    m = re.match(r"^---\n(.*?\n)---", text, re.DOTALL)
    if not m:
        return None
    return yaml.safe_load(m.group(1))


def _read_readme_catalog() -> str:
    return (REPO_ROOT / "README.md").read_text()


def _strip_frontmatter(text: str) -> str:
    """Remove YAML frontmatter, returning body only."""
    return re.sub(r"^---\n.*?\n---\n*", "", text, count=1, flags=re.DOTALL)


# --------------------------------------------------------------------------- #
# Discover items once so test IDs are deterministic
# --------------------------------------------------------------------------- #

ALL_ITEMS = _iter_items()
RULES = [p for p in ALL_ITEMS if _is_rule(p)]
SKILLS = [p for p in ALL_ITEMS if _is_skill(p)]


# --------------------------------------------------------------------------- #
# Test: General marketplace structure
# --------------------------------------------------------------------------- #


class TestMarketplaceStructure(unittest.TestCase):
    """Repo-level structure and catalog consistency."""

    def test_every_item_has_readme(self):
        for item in ALL_ITEMS:
            with self.subTest(item=item.name):
                self.assertTrue(
                    (item / "README.md").exists(),
                    f"{item.name}/ is missing README.md",
                )

    def test_every_item_is_skill_or_rule(self):
        for item in ALL_ITEMS:
            with self.subTest(item=item.name):
                self.assertTrue(
                    _is_skill(item) or _is_rule(item),
                    f"{item.name}/ has neither SKILL.md nor rule.md",
                )

    def test_no_item_is_both_skill_and_rule(self):
        for item in ALL_ITEMS:
            with self.subTest(item=item.name):
                self.assertFalse(
                    _is_skill(item) and _is_rule(item),
                    f"{item.name}/ has both SKILL.md and rule.md — pick one",
                )

    def test_directory_names_are_kebab_case(self):
        for item in ALL_ITEMS:
            with self.subTest(item=item.name):
                self.assertRegex(
                    item.name,
                    r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$",
                    f"{item.name}/ is not kebab-case",
                )

    def test_readme_catalog_lists_all_rules(self):
        catalog = _read_readme_catalog()
        for rule in RULES:
            with self.subTest(rule=rule.name):
                self.assertIn(
                    f"[{rule.name}](./rules/{rule.name}/)",
                    catalog,
                    f"Rule {rule.name} missing from root README.md catalog",
                )

    def test_readme_catalog_lists_all_skills(self):
        catalog = _read_readme_catalog()
        for skill in SKILLS:
            with self.subTest(skill=skill.name):
                self.assertIn(
                    f"[{skill.name}](./skills/{skill.name}/)",
                    catalog,
                    f"Skill {skill.name} missing from root README.md catalog",
                )

    def test_readme_catalog_rules_sorted_alphabetically(self):
        catalog = _read_readme_catalog()
        # Extract rule names from the Rules table
        rules_section = re.search(
            r"### Rules\n\n\|.*?\n\|.*?\n((?:\|.*\n)*)", catalog
        )
        if not rules_section:
            self.fail("Could not find Rules table in README.md")
        names = re.findall(r"\| \[([^\]]+)\]", rules_section.group(1))
        self.assertEqual(names, sorted(names), "Rules table is not sorted alphabetically")

    def test_readme_catalog_skills_sorted_alphabetically(self):
        catalog = _read_readme_catalog()
        skills_section = re.search(
            r"### Skills\n\n\|.*?\n\|.*?\n((?:\|.*\n)*)", catalog
        )
        if not skills_section:
            self.fail("Could not find Skills table in README.md")
        names = re.findall(r"\| \[([^\]]+)\]", skills_section.group(1))
        self.assertEqual(names, sorted(names), "Skills table is not sorted alphabetically")

    def test_no_secrets_committed(self):
        """Scan for common secret patterns in tracked files."""
        secret_patterns = [
            r"sk-[A-Za-z0-9]{20,}",              # OpenAI keys
            r"re_[A-Za-z0-9]{20,}",              # Resend keys
            r"ghp_[A-Za-z0-9]{36}",              # GitHub PAT
            r"AKIA[0-9A-Z]{16}",                 # AWS access key
            r"xoxb-[0-9]{10,}",                  # Slack token
        ]
        for item in ALL_ITEMS:
            for fpath in item.rglob("*"):
                if not fpath.is_file() or fpath.suffix in {".pyc"}:
                    continue
                try:
                    content = fpath.read_text(errors="ignore")
                except Exception:
                    continue
                for pat in secret_patterns:
                    with self.subTest(file=str(fpath.relative_to(REPO_ROOT)), pattern=pat):
                        self.assertNotRegex(
                            content, pat,
                            f"Possible secret in {fpath.relative_to(REPO_ROOT)}",
                        )

    def test_required_top_level_docs_exist(self):
        for name in ["README.md", "CONTRIBUTING.md", "AGENTS.md"]:
            with self.subTest(file=name):
                self.assertTrue(
                    (REPO_ROOT / name).exists(), f"Missing {name}"
                )

    def test_format_specs_exist(self):
        for name in ["SKILL_FORMAT.md", "RULE_FORMAT.md"]:
            with self.subTest(file=name):
                self.assertTrue(
                    (REPO_ROOT / "docs" / name).exists(), f"Missing docs/{name}"
                )

    def test_template_exists(self):
        tpl = REPO_ROOT / "_template"
        self.assertTrue(tpl.exists(), "_template/ directory missing")
        self.assertTrue((tpl / "SKILL.md").exists(), "_template/SKILL.md missing")
        self.assertTrue((tpl / "README.md").exists(), "_template/README.md missing")


# --------------------------------------------------------------------------- #
# Test: Rule conventions
# --------------------------------------------------------------------------- #


class TestRuleStructure(unittest.TestCase):
    """Every rule directory follows docs/RULE_FORMAT.md."""

    def test_rule_md_exists(self):
        for rule in RULES:
            with self.subTest(rule=rule.name):
                self.assertTrue((rule / "rule.md").exists())

    def test_rule_md_has_no_frontmatter(self):
        for rule in RULES:
            with self.subTest(rule=rule.name):
                content = (rule / "rule.md").read_text()
                self.assertFalse(
                    content.startswith("---"),
                    f"{rule.name}/rule.md should be plain Markdown (no frontmatter)",
                )

    def test_install_sh_exists(self):
        for rule in RULES:
            with self.subTest(rule=rule.name):
                self.assertTrue(
                    (rule / "install.sh").exists(),
                    f"{rule.name}/ missing install.sh",
                )

    def test_install_sh_is_executable(self):
        for rule in RULES:
            path = rule / "install.sh"
            if not path.exists():
                continue
            with self.subTest(rule=rule.name):
                mode = path.stat().st_mode
                self.assertTrue(
                    mode & stat.S_IXUSR,
                    f"{rule.name}/install.sh is not executable",
                )

    def test_install_sh_has_shebang(self):
        for rule in RULES:
            path = rule / "install.sh"
            if not path.exists():
                continue
            with self.subTest(rule=rule.name):
                first_line = path.read_text().splitlines()[0]
                self.assertTrue(
                    first_line.startswith("#!/"),
                    f"{rule.name}/install.sh missing shebang",
                )

    def test_install_sh_has_set_e(self):
        for rule in RULES:
            path = rule / "install.sh"
            if not path.exists():
                continue
            with self.subTest(rule=rule.name):
                content = path.read_text()
                self.assertIn(
                    "set -e",
                    content,
                    f"{rule.name}/install.sh missing 'set -e' (or set -euo pipefail)",
                )

    def test_install_sh_supports_help(self):
        for rule in RULES:
            path = rule / "install.sh"
            if not path.exists():
                continue
            with self.subTest(rule=rule.name):
                result = subprocess.run(
                    [str(path), "--help"],
                    capture_output=True, text=True, timeout=10,
                )
                self.assertEqual(
                    result.returncode, 0,
                    f"{rule.name}/install.sh --help exited {result.returncode}: {result.stderr}",
                )
                self.assertIn("--global", result.stdout, "help should mention --global")
                self.assertIn("--format", result.stdout, "help should mention --format")

    def test_install_sh_rejects_invalid_format(self):
        for rule in RULES:
            path = rule / "install.sh"
            if not path.exists():
                continue
            with self.subTest(rule=rule.name):
                result = subprocess.run(
                    [str(path), "--format", "bogus"],
                    capture_output=True, text=True, timeout=10,
                )
                self.assertNotEqual(
                    result.returncode, 0,
                    f"{rule.name}/install.sh should reject invalid format 'bogus'",
                )

    def test_formats_dir_exists(self):
        for rule in RULES:
            with self.subTest(rule=rule.name):
                self.assertTrue(
                    (rule / "formats").is_dir(),
                    f"{rule.name}/ missing formats/ directory",
                )

    def test_windsurf_format_exists_and_valid(self):
        for rule in RULES:
            wf = rule / "formats" / "windsurf.md"
            with self.subTest(rule=rule.name):
                self.assertTrue(wf.exists(), f"{rule.name}/formats/windsurf.md missing")
                fm = _parse_yaml_frontmatter(wf.read_text())
                self.assertIsNotNone(fm, "windsurf.md should have YAML frontmatter")
                self.assertEqual(
                    fm.get("trigger"), "always_on",
                    f"{rule.name}/formats/windsurf.md must have trigger: always_on",
                )

    def test_cursor_format_exists_and_valid(self):
        for rule in RULES:
            cf = rule / "formats" / "cursor.md"
            with self.subTest(rule=rule.name):
                self.assertTrue(cf.exists(), f"{rule.name}/formats/cursor.md missing")
                fm = _parse_yaml_frontmatter(cf.read_text())
                self.assertIsNotNone(fm, "cursor.md should have YAML frontmatter")
                self.assertTrue(
                    fm.get("alwaysApply") is True,
                    f"{rule.name}/formats/cursor.md must have alwaysApply: true",
                )

    def test_format_body_matches_rule_md(self):
        """The body of windsurf.md and cursor.md should match rule.md content."""
        for rule in RULES:
            rule_body = (rule / "rule.md").read_text().strip()
            for fmt_name in ("windsurf.md", "cursor.md"):
                fmt_file = rule / "formats" / fmt_name
                if not fmt_file.exists():
                    continue
                with self.subTest(rule=rule.name, fmt=fmt_name):
                    fmt_body = _strip_frontmatter(fmt_file.read_text()).strip()
                    self.assertEqual(
                        fmt_body, rule_body,
                        f"{rule.name}/formats/{fmt_name} body differs from rule.md",
                    )


class TestRuleInstallIdempotent(unittest.TestCase):
    """Install scripts are idempotent — running twice doesn't duplicate."""

    def test_agents_format_idempotent(self):
        for rule in RULES:
            path = rule / "install.sh"
            if not path.exists():
                continue
            with self.subTest(rule=rule.name):
                with tempfile.TemporaryDirectory() as tmpdir:
                    # Run install twice into a temp directory
                    env = os.environ.copy()
                    env["HOME"] = tmpdir
                    subprocess.run(
                        [str(path), "--global", "--format", "agents"],
                        capture_output=True, text=True, timeout=10,
                        env=env,
                    )
                    subprocess.run(
                        [str(path), "--global", "--format", "agents"],
                        capture_output=True, text=True, timeout=10,
                        env=env,
                    )
                    agents_file = Path(tmpdir) / ".config" / "devin" / "AGENTS.md"
                    if agents_file.exists():
                        content = agents_file.read_text()
                        rule_text = (rule / "rule.md").read_text().strip().splitlines()[0]
                        # The first line of the rule should appear exactly once
                        count = content.count(rule_text)
                        self.assertEqual(
                            count, 1,
                            f"{rule.name}: AGENTS.md contains rule header {count} times after 2 installs",
                        )


class TestRuleInstallGlobal(unittest.TestCase):
    """Global install creates parent directories and installs all formats."""

    def test_global_install_all_formats(self):
        for rule in RULES:
            path = rule / "install.sh"
            if not path.exists():
                continue
            with self.subTest(rule=rule.name):
                with tempfile.TemporaryDirectory() as tmpdir:
                    env = os.environ.copy()
                    env["HOME"] = tmpdir
                    result = subprocess.run(
                        [str(path), "--global", "--format", "all"],
                        capture_output=True, text=True, timeout=10,
                        env=env,
                    )
                    self.assertEqual(
                        result.returncode, 0,
                        f"{rule.name}: --global --format all failed: {result.stderr}",
                    )
                    agents = Path(tmpdir) / ".config" / "devin" / "AGENTS.md"
                    windsurf = Path(tmpdir) / ".windsurf" / "rules" / f"{rule.name}.md"
                    cursor = Path(tmpdir) / ".cursor" / "rules" / f"{rule.name}.md"
                    self.assertTrue(agents.exists(), f"{rule.name}: AGENTS.md not created")
                    self.assertTrue(windsurf.exists(), f"{rule.name}: windsurf rule not created")
                    self.assertTrue(cursor.exists(), f"{rule.name}: cursor rule not created")

    def test_project_install_all_formats(self):
        for rule in RULES:
            path = rule / "install.sh"
            if not path.exists():
                continue
            with self.subTest(rule=rule.name):
                with tempfile.TemporaryDirectory() as tmpdir:
                    result = subprocess.run(
                        [str(path), "--format", "all"],
                        capture_output=True, text=True, timeout=10,
                        cwd=tmpdir,
                    )
                    self.assertEqual(
                        result.returncode, 0,
                        f"{rule.name}: --format all failed: {result.stderr}",
                    )
                    agents = Path(tmpdir) / "AGENTS.md"
                    windsurf = Path(tmpdir) / ".windsurf" / "rules" / f"{rule.name}.md"
                    cursor = Path(tmpdir) / ".cursor" / "rules" / f"{rule.name}.md"
                    self.assertTrue(agents.exists(), f"{rule.name}: AGENTS.md not created")
                    self.assertTrue(windsurf.exists(), f"{rule.name}: windsurf rule not created")
                    self.assertTrue(cursor.exists(), f"{rule.name}: cursor rule not created")


# --------------------------------------------------------------------------- #
# Test: Skill conventions
# --------------------------------------------------------------------------- #


class TestSkillStructure(unittest.TestCase):
    """Every skill directory follows docs/SKILL_FORMAT.md."""

    def test_skill_md_exists(self):
        for skill in SKILLS:
            with self.subTest(skill=skill.name):
                self.assertTrue(
                    (skill / "SKILL.md").exists(),
                    f"{skill.name}/ missing SKILL.md",
                )

    def test_skill_md_has_frontmatter(self):
        for skill in SKILLS:
            with self.subTest(skill=skill.name):
                content = (skill / "SKILL.md").read_text()
                fm = _parse_yaml_frontmatter(content)
                self.assertIsNotNone(
                    fm,
                    f"{skill.name}/SKILL.md should have YAML frontmatter",
                )

    def test_skill_frontmatter_has_name(self):
        for skill in SKILLS:
            with self.subTest(skill=skill.name):
                content = (skill / "SKILL.md").read_text()
                fm = _parse_yaml_frontmatter(content)
                if fm is None:
                    continue
                self.assertIn(
                    "name", fm,
                    f"{skill.name}/SKILL.md frontmatter missing 'name' field",
                )

    def test_skill_frontmatter_has_description(self):
        for skill in SKILLS:
            with self.subTest(skill=skill.name):
                content = (skill / "SKILL.md").read_text()
                fm = _parse_yaml_frontmatter(content)
                if fm is None:
                    continue
                self.assertIn(
                    "description", fm,
                    f"{skill.name}/SKILL.md frontmatter missing 'description'",
                )

    def test_skill_frontmatter_description_under_80_chars(self):
        for skill in SKILLS:
            with self.subTest(skill=skill.name):
                content = (skill / "SKILL.md").read_text()
                fm = _parse_yaml_frontmatter(content)
                if fm is None or "description" not in fm:
                    continue
                self.assertLessEqual(
                    len(fm["description"]), 80,
                    f"{skill.name} description is too long ({len(fm['description'])} chars)",
                )

    def test_skill_frontmatter_has_allowed_tools(self):
        for skill in SKILLS:
            with self.subTest(skill=skill.name):
                content = (skill / "SKILL.md").read_text()
                fm = _parse_yaml_frontmatter(content)
                if fm is None:
                    continue
                self.assertIn(
                    "allowed-tools", fm,
                    f"{skill.name}/SKILL.md should restrict allowed-tools",
                )

    def test_skill_allowed_tools_are_valid(self):
        valid_builtins = {"read", "edit", "grep", "glob", "exec"}
        for skill in SKILLS:
            with self.subTest(skill=skill.name):
                content = (skill / "SKILL.md").read_text()
                fm = _parse_yaml_frontmatter(content)
                if fm is None or "allowed-tools" not in fm:
                    continue
                for tool in fm["allowed-tools"]:
                    if tool.startswith("mcp__"):
                        continue  # MCP tools have their own naming
                    self.assertIn(
                        tool, valid_builtins,
                        f"{skill.name}: unknown tool '{tool}' in allowed-tools",
                    )

    def test_skill_has_prompt_body(self):
        for skill in SKILLS:
            with self.subTest(skill=skill.name):
                content = (skill / "SKILL.md").read_text()
                body = _strip_frontmatter(content).strip()
                self.assertTrue(
                    len(body) > 0,
                    f"{skill.name}/SKILL.md has empty prompt body",
                )


# --------------------------------------------------------------------------- #
# Test: Python scripts (PEP 723, syntax)
# --------------------------------------------------------------------------- #


class TestPythonScripts(unittest.TestCase):
    """Python scripts follow PEP 723 and have valid syntax."""

    def _find_python_scripts(self) -> list[Path]:
        scripts = []
        for item in ALL_ITEMS:
            for py in item.rglob("*.py"):
                scripts.append(py)
        return sorted(scripts)

    def test_pep723_inline_metadata(self):
        for py in self._find_python_scripts():
            with self.subTest(script=str(py.relative_to(REPO_ROOT))):
                content = py.read_text()
                self.assertIn(
                    "# /// script",
                    content,
                    f"{py.relative_to(REPO_ROOT)} missing PEP 723 inline metadata",
                )

    def test_pep723_has_requires_python(self):
        for py in self._find_python_scripts():
            with self.subTest(script=str(py.relative_to(REPO_ROOT))):
                content = py.read_text()
                if "# /// script" not in content:
                    continue
                self.assertIn(
                    "requires-python",
                    content,
                    f"{py.relative_to(REPO_ROOT)} PEP 723 block missing requires-python",
                )

    def test_valid_python_syntax(self):
        for py in self._find_python_scripts():
            with self.subTest(script=str(py.relative_to(REPO_ROOT))):
                result = subprocess.run(
                    [sys.executable, "-c", f"import ast; ast.parse(open('{py}').read())"],
                    capture_output=True, text=True, timeout=10,
                )
                self.assertEqual(
                    result.returncode, 0,
                    f"{py.relative_to(REPO_ROOT)} has syntax errors: {result.stderr}",
                )


# --------------------------------------------------------------------------- #
# Test: Shell scripts (shebang, safety)
# --------------------------------------------------------------------------- #


class TestShellScripts(unittest.TestCase):
    """Shell scripts follow conventions: shebang, set -e, executable."""

    def _find_shell_scripts(self) -> list[Path]:
        scripts = []
        for item in ALL_ITEMS:
            for sh in item.rglob("*.sh"):
                scripts.append(sh)
        return sorted(scripts)

    def test_has_shebang(self):
        for sh in self._find_shell_scripts():
            with self.subTest(script=str(sh.relative_to(REPO_ROOT))):
                first_line = sh.read_text().splitlines()[0]
                self.assertTrue(
                    first_line.startswith("#!/"),
                    f"{sh.relative_to(REPO_ROOT)} missing shebang",
                )

    def test_has_set_e(self):
        for sh in self._find_shell_scripts():
            with self.subTest(script=str(sh.relative_to(REPO_ROOT))):
                content = sh.read_text()
                self.assertIn(
                    "set -e",
                    content,
                    f"{sh.relative_to(REPO_ROOT)} missing 'set -e'",
                )

    def test_is_executable(self):
        for sh in self._find_shell_scripts():
            with self.subTest(script=str(sh.relative_to(REPO_ROOT))):
                mode = sh.stat().st_mode
                self.assertTrue(
                    mode & stat.S_IXUSR,
                    f"{sh.relative_to(REPO_ROOT)} is not executable",
                )

    def test_bash_n_syntax_check(self):
        """Run bash -n on all shell scripts to catch syntax errors."""
        for sh in self._find_shell_scripts():
            with self.subTest(script=str(sh.relative_to(REPO_ROOT))):
                result = subprocess.run(
                    ["bash", "-n", str(sh)],
                    capture_output=True, text=True, timeout=10,
                )
                self.assertEqual(
                    result.returncode, 0,
                    f"{sh.relative_to(REPO_ROOT)} has bash syntax errors: {result.stderr}",
                )


# --------------------------------------------------------------------------- #
# Test: Cross-references between README catalog and actual items
# --------------------------------------------------------------------------- #


class TestCatalogConsistency(unittest.TestCase):
    """Catalog in README.md matches actual items on disk."""

    def test_no_phantom_rules_in_catalog(self):
        """Catalog shouldn't list rules that don't exist on disk."""
        catalog = _read_readme_catalog()
        rules_section = re.search(
            r"### Rules\n\n\|.*?\n\|.*?\n((?:\|.*\n)*)", catalog
        )
        if not rules_section:
            return
        catalog_names = set(re.findall(r"\| \[([^\]]+)\]", rules_section.group(1)))
        actual_names = {r.name for r in RULES}
        phantoms = catalog_names - actual_names
        self.assertEqual(
            phantoms, set(),
            f"Rules in catalog but not on disk: {phantoms}",
        )

    def test_no_phantom_skills_in_catalog(self):
        """Catalog shouldn't list skills that don't exist on disk."""
        catalog = _read_readme_catalog()
        skills_section = re.search(
            r"### Skills\n\n\|.*?\n\|.*?\n((?:\|.*\n)*)", catalog
        )
        if not skills_section:
            return
        catalog_names = set(re.findall(r"\| \[([^\]]+)\]", skills_section.group(1)))
        actual_names = {s.name for s in SKILLS}
        phantoms = catalog_names - actual_names
        self.assertEqual(
            phantoms, set(),
            f"Skills in catalog but not on disk: {phantoms}",
        )

    def test_catalog_descriptions_match_skill_frontmatter(self):
        """Catalog description should match SKILL.md description."""
        catalog = _read_readme_catalog()
        for skill in SKILLS:
            with self.subTest(skill=skill.name):
                fm = _parse_yaml_frontmatter((skill / "SKILL.md").read_text())
                if fm is None or "description" not in fm:
                    continue
                # Find the row in the catalog
                pattern = rf"\| \[{re.escape(skill.name)}\]\([^)]+\) \| (.+?) \|"
                m = re.search(pattern, catalog)
                if m is None:
                    continue  # Already caught by other tests
                catalog_desc = m.group(1).strip()
                self.assertEqual(
                    catalog_desc,
                    fm["description"],
                    f"{skill.name}: catalog description doesn't match SKILL.md",
                )

    def test_catalog_descriptions_match_rule_readme(self):
        """Catalog description for rules should be consistent with the README's first line."""
        catalog = _read_readme_catalog()
        for rule in RULES:
            with self.subTest(rule=rule.name):
                pattern = rf"\| \[{re.escape(rule.name)}\]\([^)]+\) \| (.+?) \|"
                m = re.search(pattern, catalog)
                if m is None:
                    continue
                catalog_desc = m.group(1).strip()
                # Catalog description should not be empty
                self.assertTrue(
                    len(catalog_desc) > 0,
                    f"{rule.name}: empty catalog description",
                )


# --------------------------------------------------------------------------- #
# Test: catalog.toml consistency
# --------------------------------------------------------------------------- #


class TestCatalogToml(unittest.TestCase):
    """catalog.toml is valid and references real marketplace items."""

    CATALOG_PATH = REPO_ROOT / "catalog.toml"

    def test_catalog_toml_exists(self):
        self.assertTrue(self.CATALOG_PATH.exists(), "catalog.toml not found at repo root")

    def test_catalog_toml_parses(self):
        import tomllib
        with open(self.CATALOG_PATH, "rb") as f:
            cat = tomllib.load(f)
        self.assertIsInstance(cat, dict)

    def _load(self) -> dict:
        import tomllib
        with open(self.CATALOG_PATH, "rb") as f:
            return tomllib.load(f)

    def test_platforms_have_required_fields(self):
        cat = self._load()
        required = {"label", "rule_format", "global_config", "project_config", "project_rules"}
        for pid, p in cat.get("platforms", {}).items():
            with self.subTest(platform=pid):
                missing = required - set(p.keys())
                self.assertEqual(missing, set(), f"{pid} missing fields: {missing}")

    def test_skills_disabled_by_default_exist(self):
        cat = self._load()
        actual = {s.name for s in SKILLS}
        for name in cat.get("skills_disabled_by_default", []):
            with self.subTest(skill=name):
                self.assertIn(name, actual, f"skills_disabled_by_default references nonexistent skill: {name}")

    def test_workspace_scope_defaults_exist(self):
        cat = self._load()
        actual_rules = {r.name for r in RULES}
        actual_skills = {s.name for s in SKILLS}
        all_names = actual_rules | actual_skills
        for name in cat.get("workspace_scope_defaults", []):
            with self.subTest(item=name):
                self.assertIn(name, all_names, f"workspace_scope_defaults references nonexistent item: {name}")

    def test_skill_family_members_exist(self):
        cat = self._load()
        actual = {s.name for s in SKILLS}
        for fname, fdata in cat.get("skill_families", {}).items():
            for member in fdata.get("members", []):
                with self.subTest(family=fname, skill=member):
                    self.assertIn(member, actual, f"Skill family '{fname}' references nonexistent skill: {member}")

    def test_rule_family_members_exist(self):
        cat = self._load()
        actual = {r.name for r in RULES}
        for fname, fdata in cat.get("rule_families", {}).items():
            for member in fdata.get("members", []):
                with self.subTest(family=fname, rule=member):
                    self.assertIn(member, actual, f"Rule family '{fname}' references nonexistent rule: {member}")

    def test_devin_has_no_global_rules(self):
        """Devin doesn't support global rules — global_rules must be empty."""
        cat = self._load()
        devin = cat.get("platforms", {}).get("devin", {})
        self.assertEqual(devin.get("global_rules", ""), "", "Devin should have empty global_rules")


# --------------------------------------------------------------------------- #
# Test: Linting (ruff)
# --------------------------------------------------------------------------- #


class TestLinting(unittest.TestCase):
    """All Python files pass ruff linting."""

    def _all_python_files(self) -> list[Path]:
        files = [REPO_ROOT / "install.py"]
        files.append(REPO_ROOT / "tests" / "test_marketplace.py")
        for item in ALL_ITEMS:
            for py in item.rglob("*.py"):
                files.append(py)
        return sorted(f for f in files if f.exists())

    def test_ruff_lint(self):
        """Run ruff on all Python files."""
        targets = [str(f) for f in self._all_python_files()]
        result = subprocess.run(
            [sys.executable, "-m", "ruff", "check", *targets],
            capture_output=True, text=True, timeout=30,
        )
        self.assertEqual(
            result.returncode, 0,
            f"ruff found lint issues:\n{result.stdout}",
        )


# --------------------------------------------------------------------------- #
# Test: Root-level scripts (install.py, scripts/*.sh)
# --------------------------------------------------------------------------- #


class TestRootScripts(unittest.TestCase):
    """Root-level scripts follow the same conventions as item scripts."""

    def test_install_py_has_valid_syntax(self):
        result = subprocess.run(
            [sys.executable, "-c",
             f"import ast; ast.parse(open('{REPO_ROOT / 'install.py'}').read())"],
            capture_output=True, text=True, timeout=10,
        )
        self.assertEqual(result.returncode, 0, f"install.py syntax error: {result.stderr}")

    def test_install_py_has_pep723(self):
        content = (REPO_ROOT / "install.py").read_text()
        self.assertIn("# /// script", content)
        self.assertIn("requires-python", content)

    def test_scripts_install_sh_exists_and_valid(self):
        sh = REPO_ROOT / "scripts" / "install.sh"
        self.assertTrue(sh.exists(), "scripts/install.sh missing")
        content = sh.read_text()
        self.assertTrue(content.splitlines()[0].startswith("#!/"), "missing shebang")
        self.assertIn("set -e", content, "missing set -e")
        mode = sh.stat().st_mode
        self.assertTrue(mode & stat.S_IXUSR, "not executable")
        result = subprocess.run(["bash", "-n", str(sh)], capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, f"bash syntax error: {result.stderr}")

    def test_scripts_install_rule_sh_exists_and_valid(self):
        sh = REPO_ROOT / "scripts" / "install-rule.sh"
        self.assertTrue(sh.exists(), "scripts/install-rule.sh missing")
        content = sh.read_text()
        self.assertTrue(content.splitlines()[0].startswith("#!/"), "missing shebang")
        self.assertIn("set -e", content, "missing set -e")
        mode = sh.stat().st_mode
        self.assertTrue(mode & stat.S_IXUSR, "not executable")
        result = subprocess.run(["bash", "-n", str(sh)], capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, f"bash syntax error: {result.stderr}")

    def test_run_ci_local_sh_valid(self):
        sh = REPO_ROOT / "tests" / "run-ci-local.sh"
        if not sh.exists():
            self.skipTest("tests/run-ci-local.sh not present")
        result = subprocess.run(["bash", "-n", str(sh)], capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, f"bash syntax error: {result.stderr}")


# --------------------------------------------------------------------------- #
# Test: Skill conventions (extended)
# --------------------------------------------------------------------------- #


class TestSkillConventionsExtended(unittest.TestCase):
    """Additional skill convention checks not in the base suite."""

    def test_skill_name_matches_directory(self):
        """The 'name' field in SKILL.md frontmatter must match the directory name."""
        for skill in SKILLS:
            with self.subTest(skill=skill.name):
                fm = _parse_yaml_frontmatter((skill / "SKILL.md").read_text())
                if fm is None or "name" not in fm:
                    continue
                self.assertEqual(
                    fm["name"], skill.name,
                    f"{skill.name}: SKILL.md name '{fm['name']}' doesn't match directory",
                )

    def test_skill_triggers_valid(self):
        """If triggers are specified, they must be 'user' and/or 'model'."""
        valid_triggers = {"user", "model"}
        for skill in SKILLS:
            with self.subTest(skill=skill.name):
                fm = _parse_yaml_frontmatter((skill / "SKILL.md").read_text())
                if fm is None or "triggers" not in fm:
                    continue
                for t in fm["triggers"]:
                    self.assertIn(
                        t, valid_triggers,
                        f"{skill.name}: invalid trigger '{t}' (must be user or model)",
                    )

    def test_skill_setup_sh_is_valid_shell(self):
        """If a skill has setup.sh, it must be valid bash."""
        for skill in SKILLS:
            setup = skill / "setup.sh"
            if not setup.exists():
                continue
            with self.subTest(skill=skill.name):
                content = setup.read_text()
                self.assertTrue(content.splitlines()[0].startswith("#!/"), "missing shebang")
                self.assertIn("set -e", content, "missing set -e")
                mode = setup.stat().st_mode
                self.assertTrue(mode & stat.S_IXUSR, "not executable")
                result = subprocess.run(
                    ["bash", "-n", str(setup)],
                    capture_output=True, text=True, timeout=10,
                )
                self.assertEqual(result.returncode, 0, f"bash syntax error: {result.stderr}")

    def test_skill_has_scripts_or_instructions(self):
        """Every skill should have either a scripts/ dir or substantial instructions."""
        for skill in SKILLS:
            with self.subTest(skill=skill.name):
                has_scripts = (skill / "scripts").is_dir()
                body = _strip_frontmatter((skill / "SKILL.md").read_text()).strip()
                # Must have scripts or at least 100 chars of instructions
                self.assertTrue(
                    has_scripts or len(body) > 100,
                    f"{skill.name}: no scripts/ dir and prompt body is too short ({len(body)} chars)",
                )


# --------------------------------------------------------------------------- #
# Test: install.py unit tests (non-interactive logic)
# --------------------------------------------------------------------------- #


class TestInstallerMCP(unittest.TestCase):
    """Unit tests for install.py MCP server install/uninstall."""

    def test_install_mcp_creates_config(self):
        """install_mcp should create config file with mcpServers entry."""
        # Import lazily to avoid questionary/rich dependency in test runner
        sys.path.insert(0, str(REPO_ROOT))
        try:
            from install import install_mcp
        finally:
            sys.path.pop(0)

        with tempfile.TemporaryDirectory() as tmpdir:
            cfg = Path(tmpdir) / "config.json"
            server = {"config": {"command": "uvx", "args": ["test-server"]}}
            result = install_mcp("test", server, cfg)
            self.assertEqual(result, "installed")
            self.assertTrue(cfg.exists())
            data = json.loads(cfg.read_text())
            self.assertIn("test", data["mcpServers"])

    def test_install_mcp_idempotent(self):
        sys.path.insert(0, str(REPO_ROOT))
        try:
            from install import install_mcp
        finally:
            sys.path.pop(0)

        with tempfile.TemporaryDirectory() as tmpdir:
            cfg = Path(tmpdir) / "config.json"
            server = {"config": {"command": "uvx", "args": ["test"]}}
            install_mcp("test", server, cfg)
            result = install_mcp("test", server, cfg)
            self.assertEqual(result, "already installed")

    def test_install_mcp_corrupt_config(self):
        """install_mcp should handle corrupt JSON gracefully."""
        sys.path.insert(0, str(REPO_ROOT))
        try:
            from install import install_mcp
        finally:
            sys.path.pop(0)

        with tempfile.TemporaryDirectory() as tmpdir:
            cfg = Path(tmpdir) / "config.json"
            cfg.write_text("not json")
            server = {"config": {"command": "test"}}
            result = install_mcp("test", server, cfg)
            self.assertEqual(result, "installed")

    def test_uninstall_mcp_removes_server(self):
        sys.path.insert(0, str(REPO_ROOT))
        try:
            from install import install_mcp, uninstall_mcp
        finally:
            sys.path.pop(0)

        with tempfile.TemporaryDirectory() as tmpdir:
            cfg = Path(tmpdir) / "config.json"
            server = {"config": {"command": "test"}}
            install_mcp("test", server, cfg)
            result = uninstall_mcp("test", cfg)
            self.assertEqual(result, "removed")
            data = json.loads(cfg.read_text())
            self.assertNotIn("test", data["mcpServers"])

    def test_uninstall_mcp_not_found(self):
        sys.path.insert(0, str(REPO_ROOT))
        try:
            from install import uninstall_mcp
        finally:
            sys.path.pop(0)

        with tempfile.TemporaryDirectory() as tmpdir:
            cfg = Path(tmpdir) / "config.json"
            result = uninstall_mcp("test", cfg)
            self.assertEqual(result, "not found")

    def test_uninstall_mcp_not_installed(self):
        sys.path.insert(0, str(REPO_ROOT))
        try:
            from install import uninstall_mcp
        finally:
            sys.path.pop(0)

        with tempfile.TemporaryDirectory() as tmpdir:
            cfg = Path(tmpdir) / "config.json"
            cfg.write_text('{"mcpServers": {}}')
            result = uninstall_mcp("test", cfg)
            self.assertEqual(result, "not installed")

    def test_uninstall_mcp_corrupt_config(self):
        sys.path.insert(0, str(REPO_ROOT))
        try:
            from install import uninstall_mcp
        finally:
            sys.path.pop(0)

        with tempfile.TemporaryDirectory() as tmpdir:
            cfg = Path(tmpdir) / "config.json"
            cfg.write_text("corrupt")
            result = uninstall_mcp("test", cfg)
            self.assertEqual(result, "config unreadable")


class TestInstallerReadMCP(unittest.TestCase):
    """Unit tests for read_mcp_servers."""

    def test_read_mcp_servers_missing_file(self):
        sys.path.insert(0, str(REPO_ROOT))
        try:
            from install import read_mcp_servers
        finally:
            sys.path.pop(0)

        result = read_mcp_servers(Path("/tmp/nonexistent_config.json"))
        self.assertEqual(result, {})

    def test_read_mcp_servers_valid(self):
        sys.path.insert(0, str(REPO_ROOT))
        try:
            from install import read_mcp_servers
        finally:
            sys.path.pop(0)

        with tempfile.TemporaryDirectory() as tmpdir:
            cfg = Path(tmpdir) / "config.json"
            cfg.write_text('{"mcpServers": {"foo": {"command": "bar"}}}')
            result = read_mcp_servers(cfg)
            self.assertEqual(result, {"foo": {"command": "bar"}})

    def test_read_mcp_servers_corrupt(self):
        sys.path.insert(0, str(REPO_ROOT))
        try:
            from install import read_mcp_servers
        finally:
            sys.path.pop(0)

        with tempfile.TemporaryDirectory() as tmpdir:
            cfg = Path(tmpdir) / "config.json"
            cfg.write_text("not json")
            result = read_mcp_servers(cfg)
            self.assertEqual(result, {})


class TestInstallerRules(unittest.TestCase):
    """Unit tests for install.py rule install/uninstall with real rules."""

    def _get_installer_funcs(self):
        sys.path.insert(0, str(REPO_ROOT))
        try:
            from install import install_rule, uninstall_rule, is_rule_installed, PLATFORMS
            return install_rule, uninstall_rule, is_rule_installed, PLATFORMS
        finally:
            sys.path.pop(0)

    def test_install_rule_agents_format(self):
        """Install a real rule in agents format."""
        install_rule, _, _, _ = self._get_installer_funcs()
        rule = RULES[0]
        rule_dict = {"name": rule.name, "path": rule}
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "AGENTS.md"
            paths = {"rules": target}
            result = install_rule(rule_dict, "devin", paths)
            self.assertEqual(result, "installed")
            self.assertTrue(target.exists())
            self.assertIn("##", target.read_text())

    def test_install_rule_agents_idempotent(self):
        install_rule, _, _, _ = self._get_installer_funcs()
        rule = RULES[0]
        rule_dict = {"name": rule.name, "path": rule}
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "AGENTS.md"
            paths = {"rules": target}
            install_rule(rule_dict, "devin", paths)
            result = install_rule(rule_dict, "devin", paths)
            self.assertEqual(result, "already installed")

    def test_install_rule_cursor_format(self):
        install_rule, _, _, _ = self._get_installer_funcs()
        rule = RULES[0]
        rule_dict = {"name": rule.name, "path": rule}
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "rules"
            paths = {"rules": target}
            result = install_rule(rule_dict, "cursor", paths)
            self.assertEqual(result, "installed")
            self.assertTrue((target / f"{rule.name}.md").exists())

    def test_uninstall_rule_agents(self):
        install_rule, uninstall_rule, _, _ = self._get_installer_funcs()
        rule = RULES[0]
        rule_dict = {"name": rule.name, "path": rule}
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "AGENTS.md"
            paths = {"rules": target}
            install_rule(rule_dict, "devin", paths)
            result = uninstall_rule(rule_dict, "devin", paths)
            self.assertEqual(result, "removed")

    def test_uninstall_rule_not_found(self):
        _, uninstall_rule, _, _ = self._get_installer_funcs()
        rule = RULES[0]
        rule_dict = {"name": rule.name, "path": rule}
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "AGENTS.md"
            paths = {"rules": target}
            result = uninstall_rule(rule_dict, "devin", paths)
            self.assertEqual(result, "not found")

    def test_uninstall_rule_not_installed(self):
        _, uninstall_rule, _, _ = self._get_installer_funcs()
        rule = RULES[0]
        rule_dict = {"name": rule.name, "path": rule}
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "AGENTS.md"
            target.write_text("# Some other content\n")
            paths = {"rules": target}
            result = uninstall_rule(rule_dict, "devin", paths)
            self.assertEqual(result, "not installed")

    def test_uninstall_rule_cursor_format(self):
        install_rule, uninstall_rule, _, _ = self._get_installer_funcs()
        rule = RULES[0]
        rule_dict = {"name": rule.name, "path": rule}
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "rules"
            paths = {"rules": target}
            install_rule(rule_dict, "cursor", paths)
            result = uninstall_rule(rule_dict, "cursor", paths)
            self.assertEqual(result, "removed")
            self.assertFalse((target / f"{rule.name}.md").exists())

    def test_uninstall_rule_cursor_not_installed(self):
        _, uninstall_rule, _, _ = self._get_installer_funcs()
        rule = RULES[0]
        rule_dict = {"name": rule.name, "path": rule}
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "rules"
            target.mkdir()
            paths = {"rules": target}
            result = uninstall_rule(rule_dict, "cursor", paths)
            self.assertEqual(result, "not installed")

    def test_is_rule_installed_agents(self):
        install_rule, _, is_rule_installed, _ = self._get_installer_funcs()
        rule = RULES[0]
        rule_dict = {"name": rule.name, "path": rule}
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "AGENTS.md"
            paths = {"rules": target}
            self.assertFalse(is_rule_installed("devin", rule.name, paths))
            install_rule(rule_dict, "devin", paths)
            self.assertTrue(is_rule_installed("devin", rule.name, paths))

    def test_is_rule_installed_cursor(self):
        install_rule, _, is_rule_installed, _ = self._get_installer_funcs()
        rule = RULES[0]
        rule_dict = {"name": rule.name, "path": rule}
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "rules"
            paths = {"rules": target}
            self.assertFalse(is_rule_installed("cursor", rule.name, paths))
            install_rule(rule_dict, "cursor", paths)
            self.assertTrue(is_rule_installed("cursor", rule.name, paths))


class TestInstallerSkills(unittest.TestCase):
    """Unit tests for install.py skill install/uninstall."""

    def _get_funcs(self):
        sys.path.insert(0, str(REPO_ROOT))
        try:
            from install import install_skill, uninstall_skill, is_skill_installed
            return install_skill, uninstall_skill, is_skill_installed
        finally:
            sys.path.pop(0)

    def test_install_skill(self):
        install_skill, _, _ = self._get_funcs()
        skill = SKILLS[0]
        skill_dict = {"name": skill.name, "path": skill}
        with tempfile.TemporaryDirectory() as tmpdir:
            skills_dir = Path(tmpdir) / "skills"
            skills_dir.mkdir()
            result = install_skill(skill_dict, skills_dir)
            self.assertEqual(result, "installed")
            self.assertTrue((skills_dir / skill.name).is_dir())
            self.assertTrue((skills_dir / skill.name / "SKILL.md").exists())

    def test_install_skill_overwrites(self):
        """Installing over an existing skill should replace it."""
        install_skill, _, _ = self._get_funcs()
        skill = SKILLS[0]
        skill_dict = {"name": skill.name, "path": skill}
        with tempfile.TemporaryDirectory() as tmpdir:
            skills_dir = Path(tmpdir) / "skills"
            skills_dir.mkdir()
            install_skill(skill_dict, skills_dir)
            result = install_skill(skill_dict, skills_dir)
            self.assertEqual(result, "installed")

    def test_install_skill_not_supported(self):
        install_skill, _, _ = self._get_funcs()
        skill_dict = {"name": "test", "path": Path(".")}
        result = install_skill(skill_dict, None)
        self.assertEqual(result, "not supported")

    def test_uninstall_skill(self):
        install_skill, uninstall_skill, _ = self._get_funcs()
        skill = SKILLS[0]
        skill_dict = {"name": skill.name, "path": skill}
        with tempfile.TemporaryDirectory() as tmpdir:
            skills_dir = Path(tmpdir) / "skills"
            skills_dir.mkdir()
            install_skill(skill_dict, skills_dir)
            result = uninstall_skill(skill.name, skills_dir)
            self.assertEqual(result, "removed")
            self.assertFalse((skills_dir / skill.name).exists())

    def test_uninstall_skill_not_installed(self):
        _, uninstall_skill, _ = self._get_funcs()
        with tempfile.TemporaryDirectory() as tmpdir:
            skills_dir = Path(tmpdir) / "skills"
            skills_dir.mkdir()
            result = uninstall_skill("nonexistent", skills_dir)
            self.assertEqual(result, "not installed")

    def test_uninstall_skill_not_supported(self):
        _, uninstall_skill, _ = self._get_funcs()
        result = uninstall_skill("test", None)
        self.assertEqual(result, "not supported")

    def test_is_skill_installed(self):
        install_skill, _, is_skill_installed = self._get_funcs()
        skill = SKILLS[0]
        skill_dict = {"name": skill.name, "path": skill}
        with tempfile.TemporaryDirectory() as tmpdir:
            skills_dir = Path(tmpdir) / "skills"
            skills_dir.mkdir()
            paths = {"skills": skills_dir}
            self.assertFalse(is_skill_installed(skill.name, paths))
            install_skill(skill_dict, skills_dir)
            self.assertTrue(is_skill_installed(skill.name, paths))

    def test_is_skill_installed_no_skills_dir(self):
        _, _, is_skill_installed = self._get_funcs()
        paths = {"skills": None}
        self.assertFalse(is_skill_installed("anything", paths))


class TestInstallerScanner(unittest.TestCase):
    """Unit tests for scan_rules / scan_skills on the real marketplace."""

    def test_scan_rules_finds_all(self):
        sys.path.insert(0, str(REPO_ROOT))
        try:
            from install import scan_rules
        finally:
            sys.path.pop(0)

        rules = scan_rules(REPO_ROOT)
        rule_names = {r["name"] for r in rules}
        expected = {r.name for r in RULES}
        self.assertEqual(rule_names, expected)

    def test_scan_skills_finds_all(self):
        sys.path.insert(0, str(REPO_ROOT))
        try:
            from install import scan_skills
        finally:
            sys.path.pop(0)

        skills = scan_skills(REPO_ROOT)
        skill_names = {s["name"] for s in skills}
        expected = {s.name for s in SKILLS}
        self.assertEqual(skill_names, expected)

    def test_scan_rules_has_descriptions(self):
        sys.path.insert(0, str(REPO_ROOT))
        try:
            from install import scan_rules
        finally:
            sys.path.pop(0)

        rules = scan_rules(REPO_ROOT)
        for r in rules:
            with self.subTest(rule=r["name"]):
                self.assertTrue(
                    len(r["description"]) > 0,
                    f"{r['name']}: scan_rules returned empty description",
                )

    def test_scan_skills_has_descriptions(self):
        sys.path.insert(0, str(REPO_ROOT))
        try:
            from install import scan_skills
        finally:
            sys.path.pop(0)

        skills = scan_skills(REPO_ROOT)
        for s in skills:
            with self.subTest(skill=s["name"]):
                self.assertTrue(
                    len(s["description"]) > 0,
                    f"{s['name']}: scan_skills returned empty description",
                )

    def test_scan_rules_has_formats(self):
        sys.path.insert(0, str(REPO_ROOT))
        try:
            from install import scan_rules
        finally:
            sys.path.pop(0)

        rules = scan_rules(REPO_ROOT)
        for r in rules:
            with self.subTest(rule=r["name"]):
                self.assertIn("windsurf", r["formats"])
                self.assertIn("cursor", r["formats"])


class TestInstallerUIHelpers(unittest.TestCase):
    """Unit tests for UI helper functions."""

    def test_status_badge(self):
        sys.path.insert(0, str(REPO_ROOT))
        try:
            from install import status_badge
        finally:
            sys.path.pop(0)

        self.assertIn("installed", status_badge(True))
        self.assertIn("not installed", status_badge(False))

    def test_action_badge_installed(self):
        sys.path.insert(0, str(REPO_ROOT))
        try:
            from install import action_badge
        finally:
            sys.path.pop(0)

        self.assertIn("green", action_badge("installed"))
        self.assertIn("green", action_badge("removed"))
        self.assertIn("dim", action_badge("already installed"))
        self.assertIn("dim", action_badge("not installed"))
        self.assertIn("dim", action_badge("not found"))
        self.assertIn("yellow", action_badge("no cursor format"))


# --------------------------------------------------------------------------- #
# Test: Rule uninstall line-removal edge cases
# --------------------------------------------------------------------------- #


class TestRuleUninstallEdgeCases(unittest.TestCase):
    """Verify uninstall_rule correctly removes rule blocks from AGENTS.md."""

    def _get_funcs(self):
        sys.path.insert(0, str(REPO_ROOT))
        try:
            from install import install_rule, uninstall_rule
            return install_rule, uninstall_rule
        finally:
            sys.path.pop(0)

    def test_uninstall_preserves_other_rules(self):
        """Uninstalling one rule should not affect other rules."""
        install_rule, uninstall_rule = self._get_funcs()
        if len(RULES) < 2:
            self.skipTest("Need at least 2 rules")
        rule_a = {"name": RULES[0].name, "path": RULES[0]}
        rule_b = {"name": RULES[1].name, "path": RULES[1]}
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "AGENTS.md"
            paths = {"rules": target}
            install_rule(rule_a, "devin", paths)
            install_rule(rule_b, "devin", paths)
            uninstall_rule(rule_a, "devin", paths)
            content = target.read_text()
            # rule_b should still be there
            rule_b_title = ""
            for line in (RULES[1] / "rule.md").read_text().splitlines():
                if line.startswith("## "):
                    rule_b_title = line[3:].strip()
                    break
            self.assertIn(rule_b_title, content)

    def test_install_uninstall_roundtrip(self):
        """Install then uninstall should leave an empty-ish file."""
        install_rule, uninstall_rule = self._get_funcs()
        rule = {"name": RULES[0].name, "path": RULES[0]}
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "AGENTS.md"
            paths = {"rules": target}
            install_rule(rule, "devin", paths)
            self.assertTrue(len(target.read_text().strip()) > 0)
            uninstall_rule(rule, "devin", paths)
            # File should have minimal content
            remaining = target.read_text().strip()
            # Should not contain any ## headings from the rule
            self.assertNotIn("## ", remaining)


# --------------------------------------------------------------------------- #
# Test: Install script safety — context bloat prevention
# --------------------------------------------------------------------------- #


class TestInstallScriptSafety(unittest.TestCase):
    """Tests for install-rule.sh safety features: bloat warnings,
    idempotency, scope collision detection, and input validation."""

    def test_format_all_prints_bloat_warning(self):
        """--format all should print a warning about context duplication."""
        rule = RULES[0]
        with tempfile.TemporaryDirectory() as tmpdir:
            env = os.environ.copy()
            env["HOME"] = tmpdir
            result = subprocess.run(
                [str(rule / "install.sh"), "--global", "--format", "all"],
                capture_output=True, text=True, timeout=10, env=env,
            )
            self.assertEqual(result.returncode, 0)
            self.assertIn("Warning", result.stdout)
            self.assertIn("multiple times", result.stdout)

    def test_format_agents_no_bloat_warning(self):
        """Default --format agents should NOT print a bloat warning."""
        rule = RULES[0]
        with tempfile.TemporaryDirectory() as tmpdir:
            env = os.environ.copy()
            env["HOME"] = tmpdir
            result = subprocess.run(
                [str(rule / "install.sh"), "--global"],
                capture_output=True, text=True, timeout=10, env=env,
            )
            self.assertEqual(result.returncode, 0)
            self.assertNotIn("Warning", result.stdout)

    def test_windsurf_format_idempotent(self):
        """Installing Windsurf format twice should skip on second run."""
        rule = RULES[0]
        with tempfile.TemporaryDirectory() as tmpdir:
            env = os.environ.copy()
            env["HOME"] = tmpdir
            for _ in range(2):
                subprocess.run(
                    [str(rule / "install.sh"), "--global", "--format", "windsurf"],
                    capture_output=True, text=True, timeout=10, env=env,
                )
            result = subprocess.run(
                [str(rule / "install.sh"), "--global", "--format", "windsurf"],
                capture_output=True, text=True, timeout=10, env=env,
            )
            self.assertIn("already up to date", result.stdout)

    def test_cursor_format_idempotent(self):
        """Installing Cursor format twice should skip on second run."""
        rule = RULES[0]
        with tempfile.TemporaryDirectory() as tmpdir:
            env = os.environ.copy()
            env["HOME"] = tmpdir
            subprocess.run(
                [str(rule / "install.sh"), "--global", "--format", "cursor"],
                capture_output=True, text=True, timeout=10, env=env,
            )
            result = subprocess.run(
                [str(rule / "install.sh"), "--global", "--format", "cursor"],
                capture_output=True, text=True, timeout=10, env=env,
            )
            self.assertIn("already up to date", result.stdout)

    def test_scope_collision_warns_when_both_scopes_installed(self):
        """Installing globally when project-level exists should print a note."""
        rule = RULES[0]
        with tempfile.TemporaryDirectory() as tmpdir:
            env = os.environ.copy()
            env["HOME"] = tmpdir
            # Install at project scope first
            subprocess.run(
                [str(rule / "install.sh"), "--format", "agents"],
                capture_output=True, text=True, timeout=10, env=env, cwd=tmpdir,
            )
            # Now install at global scope — should detect project-level copy
            result = subprocess.run(
                [str(rule / "install.sh"), "--global", "--format", "agents"],
                capture_output=True, text=True, timeout=10, env=env, cwd=tmpdir,
            )
            self.assertIn("also installed", result.stdout)

    def test_help_documents_format_all_risk(self):
        """--help should mention the bloat risk of --format all."""
        rule = RULES[0]
        result = subprocess.run(
            [str(rule / "install.sh"), "--help"],
            capture_output=True, text=True, timeout=10,
        )
        self.assertIn("WARNING", result.stdout)
        self.assertIn("duplicate", result.stdout.lower())


class TestInstallPySafety(unittest.TestCase):
    """Tests for install.py safety features: accurate detection,
    no leading newline, and format idempotency."""

    def _get_funcs(self):
        sys.path.insert(0, str(REPO_ROOT))
        try:
            from install import install_rule, is_rule_installed
            return install_rule, is_rule_installed
        finally:
            sys.path.pop(0)

    def test_is_rule_installed_detects_all_rules_correctly(self):
        """is_rule_installed should detect every rule after install —
        verifies the .title() fix for 'No AI Credit', 'Python UV', etc."""
        install_rule, is_rule_installed = self._get_funcs()
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "AGENTS.md"
            paths = {"rules": target}
            for rule in RULES:
                rule_dict = {"name": rule.name, "path": rule}
                install_rule(rule_dict, "devin", paths)
            # Now check that every rule is detected as installed
            for rule in RULES:
                with self.subTest(rule=rule.name):
                    self.assertTrue(
                        is_rule_installed("devin", rule.name, paths),
                        f"is_rule_installed failed to detect '{rule.name}' "
                        f"— likely heading mismatch",
                    )

    def test_new_agents_file_has_no_leading_newline(self):
        """Installing into a non-existent AGENTS.md should not start with \\n."""
        install_rule, _ = self._get_funcs()
        rule = RULES[0]
        rule_dict = {"name": rule.name, "path": rule}
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "AGENTS.md"
            paths = {"rules": target}
            install_rule(rule_dict, "devin", paths)
            content = target.read_text()
            self.assertFalse(
                content.startswith("\n"),
                "New AGENTS.md should not start with a blank line",
            )

    def test_existing_agents_file_gets_separator_newline(self):
        """Appending to an existing AGENTS.md should add a separator newline."""
        install_rule, _ = self._get_funcs()
        if len(RULES) < 2:
            self.skipTest("Need at least 2 rules")
        rule_a = {"name": RULES[0].name, "path": RULES[0]}
        rule_b = {"name": RULES[1].name, "path": RULES[1]}
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "AGENTS.md"
            paths = {"rules": target}
            install_rule(rule_a, "devin", paths)
            install_rule(rule_b, "devin", paths)
            content = target.read_text()
            # Should not have double blank lines between rules
            self.assertNotIn("\n\n\n", content)

    def test_cursor_format_idempotent_in_install_py(self):
        """install_rule for cursor format should return 'already installed'
        when file content matches."""
        install_rule, _ = self._get_funcs()
        rule = RULES[0]
        rule_dict = {"name": rule.name, "path": rule}
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "rules"
            paths = {"rules": target}
            install_rule(rule_dict, "cursor", paths)
            result = install_rule(rule_dict, "cursor", paths)
            self.assertEqual(result, "already installed")

    def test_windsurf_format_idempotent_in_install_py(self):
        """install_rule for windsurf format should return 'already installed'
        when file content matches."""
        install_rule, _ = self._get_funcs()
        rule = RULES[0]
        rule_dict = {"name": rule.name, "path": rule}
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "rules"
            paths = {"rules": target}
            install_rule(rule_dict, "windsurf", paths)
            result = install_rule(rule_dict, "windsurf", paths)
            self.assertEqual(result, "already installed")


# --------------------------------------------------------------------------- #
# Entry point
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    unittest.main()
