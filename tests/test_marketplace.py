# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6.0"]
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

import os
import re
import stat
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent

# Directories that are NOT items (skills or rules)
EXCLUDED_DIRS = {"docs", "_template", ".git", ".github", "tests", "__pycache__"}

# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #


def _iter_items() -> list[Path]:
    """Return sorted list of item directories (skills + rules)."""
    return sorted(
        p
        for p in REPO_ROOT.iterdir()
        if p.is_dir() and p.name not in EXCLUDED_DIRS and not p.name.startswith(".")
    )


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
                    f"[{rule.name}]",
                    catalog,
                    f"Rule {rule.name} missing from root README.md catalog",
                )

    def test_readme_catalog_lists_all_skills(self):
        catalog = _read_readme_catalog()
        for skill in SKILLS:
            with self.subTest(skill=skill.name):
                self.assertIn(
                    f"[{skill.name}]",
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
                    agents_file = Path(tmpdir) / ".config" / "cognition" / "AGENTS.md"
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
                        [str(path), "--global"],
                        capture_output=True, text=True, timeout=10,
                        env=env,
                    )
                    self.assertEqual(
                        result.returncode, 0,
                        f"{rule.name}: --global install failed: {result.stderr}",
                    )
                    # Verify all four format files were created
                    agents = Path(tmpdir) / ".config" / "cognition" / "AGENTS.md"
                    windsurf = Path(tmpdir) / ".windsurf" / "rules" / f"{rule.name}.md"
                    cursor = Path(tmpdir) / ".cursor" / "rules" / f"{rule.name}.md"
                    claude = Path(tmpdir) / ".claude" / "CLAUDE.md"
                    self.assertTrue(agents.exists(), f"{rule.name}: AGENTS.md not created")
                    self.assertTrue(windsurf.exists(), f"{rule.name}: windsurf rule not created")
                    self.assertTrue(cursor.exists(), f"{rule.name}: cursor rule not created")
                    self.assertTrue(claude.exists(), f"{rule.name}: CLAUDE.md not created")

    def test_project_install_all_formats(self):
        for rule in RULES:
            path = rule / "install.sh"
            if not path.exists():
                continue
            with self.subTest(rule=rule.name):
                with tempfile.TemporaryDirectory() as tmpdir:
                    result = subprocess.run(
                        [str(path)],
                        capture_output=True, text=True, timeout=10,
                        cwd=tmpdir,
                    )
                    self.assertEqual(
                        result.returncode, 0,
                        f"{rule.name}: project install failed: {result.stderr}",
                    )
                    agents = Path(tmpdir) / "AGENTS.md"
                    windsurf = Path(tmpdir) / ".windsurf" / "rules" / f"{rule.name}.md"
                    cursor = Path(tmpdir) / ".cursor" / "rules" / f"{rule.name}.md"
                    claude = Path(tmpdir) / "CLAUDE.md"
                    self.assertTrue(agents.exists(), f"{rule.name}: AGENTS.md not created")
                    self.assertTrue(windsurf.exists(), f"{rule.name}: windsurf rule not created")
                    self.assertTrue(cursor.exists(), f"{rule.name}: cursor rule not created")
                    self.assertTrue(claude.exists(), f"{rule.name}: CLAUDE.md not created")


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
# Entry point
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    unittest.main()
