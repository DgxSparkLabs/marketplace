#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
constructs.py — 10 Construct classes implementing the Construct protocol.

Each class encapsulates:
  - prefix           : plugin name prefix (e.g., "skill")
  - source_directory : source tree root (e.g., Path("skills/"))
  - category         : marketplace.json category tag
  - build_plugin_json: produce plugin.json content dict (no I/O)
  - emit             : write the full plugin to target_dir (all I/O)

Registry:
  CONSTRUCTS: dict[str, Construct]  — single source of truth
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Protocol, runtime_checkable

from utils import (
    REPO_ROOT,
    _frontmatter,
    _load_plugin_json,
    _marketplace_author,
    _marketplace_version,
    write_plugin_json,
)


@runtime_checkable
class Construct(Protocol):
    """A Claude Code plugin construct type (skill, rule, command, ...)."""

    prefix: str           # e.g., "skill"
    source_directory: Path  # e.g., Path("skills/") — relative to repo root
    category: str         # marketplace.json category tag (often == prefix)

    def build_plugin_json(self, name: str) -> dict:
        """Build the plugin.json content dict. Pure — no I/O."""
        ...

    def emit(self, name: str, target_dir: Path) -> None:
        """Write the full plugin to target_dir.

        Includes: copy source content, generate construct-specific
        artifacts (e.g., activate.sh for rules), and write
        .claude-plugin/plugin.json. Does ALL I/O for this instance.
        """
        ...


# ─── shared base helper ──────────────────────────────────────────────────────

def _base_plugin_shape(construct: Construct, name: str) -> dict:
    """Common plugin.json fields shared by all construct types."""
    return {
        "name": f"{construct.prefix}-{name}",
        "version": _marketplace_version(),
        "author": _marketplace_author(),
    }


# ─── activate.sh template (rules) ────────────────────────────────────────────

ACTIVATE_SH_TEMPLATE = """\
#!/usr/bin/env bash
# activate.sh — symlink (or copy on platforms without symlink support)
# this plugin's rule file(s) into the project's .claude/rules/.
# Run once after installing this plugin.
#
# Usage:
#   bash <path>/activate.sh                   # default target: .claude/rules
#   bash <path>/activate.sh <rules-dir>       # custom target
#
# On Linux/macOS: creates symlinks so plugin updates auto-propagate.
# On Windows (Git Bash, MSYS) without symlink privileges: falls back
# to file copy. After a plugin update, re-run activate.sh to refresh.
set -euo pipefail

RULES_DIR="${{1:-.claude/rules}}"
PLUGIN_DIR="$(cd "$(dirname "$0")" && pwd)"

mkdir -p "$RULES_DIR"
mode="symlinked"
for rule in "$PLUGIN_DIR/rules"/*.md; do
  [ -e "$rule" ] || continue
  target="$RULES_DIR/$(basename "$rule")"
  rm -f "$target"
  if ln -s "$rule" "$target" 2>/dev/null && [ -L "$target" ]; then
    :  # real symlink created
  else
    # Symlink unsupported on this platform; fall back to copy.
    cp -f "$rule" "$target"
    mode="copied"
  fi
done
echo "$mode rule(s) into $RULES_DIR. Claude Code will load them at next session start."
if [ "$mode" = "copied" ]; then
  echo "Note: copies, not symlinks (your platform doesn't allow symlinks here)."
  echo "      Re-run activate.sh after a plugin update to refresh."
fi
"""


# ─── Construct implementations ────────────────────────────────────────────────

class SkillConstruct:
    prefix = "skill"
    source_directory = REPO_ROOT / "skills"
    category = "skill"

    def build_plugin_json(self, name: str) -> dict:
        base = _base_plugin_shape(self, name)
        fm = _frontmatter(self.source_directory / name / "SKILL.md")
        base["description"] = fm.get("description", name)
        base["skills"] = ["./"]
        base["keywords"] = ["skill", name]
        return base

    def emit(self, name: str, target_dir: Path) -> None:
        # Copy entire source tree (SKILL.md, scripts/, references/, etc.)
        shutil.copytree(
            self.source_directory / name,
            target_dir,
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )
        # Write plugin.json under .claude-plugin/ (overrides any source copy)
        write_plugin_json(target_dir, self.build_plugin_json(name))


class RuleConstruct:
    prefix = "rule"
    source_directory = REPO_ROOT / "rules"
    category = "rule"

    def build_plugin_json(self, name: str) -> dict:
        base = _base_plugin_shape(self, name)
        base["description"] = (
            f"Always-on rule: {name}. Install, then run activate.sh "
            f"to symlink the rule into ~/.claude/rules/."
        )
        base["keywords"] = ["rule", name]
        return base

    def emit(self, name: str, target_dir: Path) -> None:
        # Copy rule.md into rules/<name>.md subdir (activate.sh expects rules/*.md)
        rules_subdir = target_dir / "rules"
        rules_subdir.mkdir(parents=True, exist_ok=True)
        shutil.copy(
            self.source_directory / name / "rule.md",
            rules_subdir / f"{name}.md",
        )

        # Copy README.md if present
        readme = self.source_directory / name / "README.md"
        if readme.exists():
            shutil.copy(readme, target_dir / "README.md")

        # Generate activate.sh from template
        activate_path = target_dir / "activate.sh"
        activate_path.write_text(ACTIVATE_SH_TEMPLATE, encoding="utf-8")
        activate_path.chmod(0o755)

        # Write plugin.json under .claude-plugin/
        write_plugin_json(target_dir, self.build_plugin_json(name))


class CommandConstruct:
    prefix = "command"
    source_directory = REPO_ROOT / "commands"
    category = "command"

    def build_plugin_json(self, name: str) -> dict:
        base = _base_plugin_shape(self, name)
        # Description from the first command .md file's frontmatter
        commands_dir = self.source_directory / name / "commands"
        description = name
        if commands_dir.exists():
            for cmd_file in sorted(commands_dir.glob("*.md")):
                fm = _frontmatter(cmd_file)
                description = fm.get("description", name)
                break
        base["description"] = description
        base["commands"] = ["./commands"]
        return base

    def emit(self, name: str, target_dir: Path) -> None:
        shutil.copytree(
            self.source_directory / name,
            target_dir,
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )
        write_plugin_json(target_dir, self.build_plugin_json(name))


class AgentConstruct:
    prefix = "agent"
    source_directory = REPO_ROOT / "agents"
    category = "agent"

    def build_plugin_json(self, name: str) -> dict:
        base = _base_plugin_shape(self, name)
        # Description from the first agent .md file's frontmatter
        agents_dir = self.source_directory / name / "agents"
        description = name
        if agents_dir.exists():
            for agent_file in sorted(agents_dir.glob("*.md")):
                fm = _frontmatter(agent_file)
                description = fm.get("description", name)
                break
        base["description"] = description
        # Note: Claude Code reads agents from the plugin's agents/ subdir automatically.
        # No "agents" field is needed in plugin.json (the spec doesn't define one).
        return base

    def emit(self, name: str, target_dir: Path) -> None:
        shutil.copytree(
            self.source_directory / name,
            target_dir,
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )
        write_plugin_json(target_dir, self.build_plugin_json(name))


class HookConstruct:
    prefix = "hook"
    source_directory = REPO_ROOT / "hooks"
    category = "hook"

    def build_plugin_json(self, name: str) -> dict:
        base = _base_plugin_shape(self, name)
        # Description from hooks.json if present
        hooks_json_path = self.source_directory / name / "hooks" / "hooks.json"
        description = name
        if hooks_json_path.exists():
            hooks_data = json.loads(hooks_json_path.read_text(encoding="utf-8"))
            description = hooks_data.get("description", name)
        base["description"] = description
        # Note: Claude Code reads hooks from the plugin's hooks/hooks.json automatically.
        # No "hooks" field is needed in plugin.json (the spec doesn't define one).
        return base

    def emit(self, name: str, target_dir: Path) -> None:
        shutil.copytree(
            self.source_directory / name,
            target_dir,
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )
        write_plugin_json(target_dir, self.build_plugin_json(name))


class MCPConstruct:
    prefix = "mcp"
    source_directory = REPO_ROOT / "mcp-servers"
    category = "mcp"

    def build_plugin_json(self, name: str) -> dict:
        base = _base_plugin_shape(self, name)
        source_pj = _load_plugin_json(
            self.source_directory / name / ".claude-plugin" / "plugin.json"
        )
        base["description"] = source_pj["description"]
        # mcpServers may be a path string or inline dict; pass through as-is
        base["mcpServers"] = source_pj["mcpServers"]
        return base

    def emit(self, name: str, target_dir: Path) -> None:
        # Copy entire source tree (includes mcp-config.json, scripts, etc.)
        shutil.copytree(
            self.source_directory / name,
            target_dir,
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )
        # Overwrite .claude-plugin/plugin.json with our computed version
        write_plugin_json(target_dir, self.build_plugin_json(name))


class LSPConstruct:
    prefix = "lsp"
    source_directory = REPO_ROOT / "lsp-servers"
    category = "lsp"

    def build_plugin_json(self, name: str) -> dict:
        base = _base_plugin_shape(self, name)
        source_pj = _load_plugin_json(
            self.source_directory / name / ".claude-plugin" / "plugin.json"
        )
        base["description"] = source_pj["description"]
        base["lspServers"] = source_pj["lspServers"]
        return base

    def emit(self, name: str, target_dir: Path) -> None:
        shutil.copytree(
            self.source_directory / name,
            target_dir,
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )
        write_plugin_json(target_dir, self.build_plugin_json(name))


class MonitorConstruct:
    prefix = "monitor"
    source_directory = REPO_ROOT / "monitors"
    category = "monitor"

    def build_plugin_json(self, name: str) -> dict:
        base = _base_plugin_shape(self, name)
        source_pj = _load_plugin_json(
            self.source_directory / name / ".claude-plugin" / "plugin.json"
        )
        base["description"] = source_pj["description"]
        base.setdefault("experimental", {})["monitors"] = (
            source_pj.get("experimental", {}).get("monitors", "./monitors/monitors.json")
        )
        return base

    def emit(self, name: str, target_dir: Path) -> None:
        shutil.copytree(
            self.source_directory / name,
            target_dir,
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )
        write_plugin_json(target_dir, self.build_plugin_json(name))


class OutputStyleConstruct:
    prefix = "output-style"
    source_directory = REPO_ROOT / "output-styles"
    category = "output-style"

    def build_plugin_json(self, name: str) -> dict:
        base = _base_plugin_shape(self, name)
        source_pj = _load_plugin_json(
            self.source_directory / name / ".claude-plugin" / "plugin.json"
        )
        base["description"] = source_pj["description"]
        base["outputStyles"] = source_pj.get("outputStyles", "./output-styles")
        return base

    def emit(self, name: str, target_dir: Path) -> None:
        shutil.copytree(
            self.source_directory / name,
            target_dir,
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )
        write_plugin_json(target_dir, self.build_plugin_json(name))


class ThemeConstruct:
    prefix = "theme"
    source_directory = REPO_ROOT / "themes"
    category = "theme"

    def build_plugin_json(self, name: str) -> dict:
        base = _base_plugin_shape(self, name)
        source_pj = _load_plugin_json(
            self.source_directory / name / ".claude-plugin" / "plugin.json"
        )
        base["description"] = source_pj["description"]
        base.setdefault("experimental", {})["themes"] = (
            source_pj.get("experimental", {}).get("themes", "./themes")
        )
        return base

    def emit(self, name: str, target_dir: Path) -> None:
        shutil.copytree(
            self.source_directory / name,
            target_dir,
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )
        write_plugin_json(target_dir, self.build_plugin_json(name))


# ─── Registry ────────────────────────────────────────────────────────────────

CONSTRUCTS: dict[str, Construct] = {
    "skill":         SkillConstruct(),
    "rule":          RuleConstruct(),
    "command":       CommandConstruct(),
    "agent":         AgentConstruct(),
    "hook":          HookConstruct(),
    "mcp":           MCPConstruct(),
    "lsp":           LSPConstruct(),
    "monitor":       MonitorConstruct(),
    "output-style":  OutputStyleConstruct(),
    "theme":         ThemeConstruct(),
}
