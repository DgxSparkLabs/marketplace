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
    _is_candidate_subdir,
    _load_plugin_json,
    _marketplace_author,
    _marketplace_name,
    _marketplace_version,
    _read_source_plugin_description,
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
    """Common plugin.json fields shared by all construct types.

    The ``name`` field is the **Claude plugin identifier** — unique per
    plugin, composed as ``<brand>-<construct.prefix>-<source-dir-name>``
    (e.g. ``dgxsparklabs-skill-example``). ``<brand>`` is derived from
    ``MARKETPLACE.toml`` ``name`` by stripping the trailing ``-marketplace``
    suffix. Slash invocations follow the same pattern
    ``/<brand>-<construct.prefix>-<plugin>:<component>`` —
    e.g. ``/dgxsparklabs-skill-example:notebook``.

    The marketplace-entry name (what the operator types at install:
    ``claude plugin install skill-example@dgxsparklabs-marketplace``) is
    a separate, unprefixed identifier composed by ``_make_marketplace_entry``
    in ``scripts/generate_manifest.py`` from ``plugin_dir.name``
    (``<construct.prefix>-<source-dir-name>``).

    History: an earlier attempt (Path A, ``d641f92``, 2026-05-27) used a
    shared ``<brand>-<construct.category>`` here so multiple plugins of one
    construct shared a slash namespace; ``claude plugin details`` then
    collapsed to a single first-installed-wins view of the components.
    Path A was reverted on 2026-05-28 per
    ``docs/research/multi-instance-claude-only-2026-05-27/PLAN.md``.
    """
    mp_name = _marketplace_name()
    brand = mp_name.removesuffix("-marketplace") if mp_name.endswith("-marketplace") else mp_name
    return {
        "name": f"{brand}-{construct.prefix}-{name}",
        "version": _marketplace_version(),
        "author": _marketplace_author(),
    }


# ─── Construct implementations ────────────────────────────────────────────────

class SkillConstruct:
    # `prefix` controls both the INSTALL-time marketplace name
    # (e.g. `skill-example` in `claude plugin install skill-example@...`)
    # and the plugin.json `name` (composed in `_base_plugin_shape` as
    # `<brand>-<prefix>-<source-dir>`, e.g. `dgxsparklabs-skill-example`).
    # The slash form is `/dgxsparklabs-skill-example:<frontmatter-name>`.
    #
    # Two source layouts are supported per plugin (build_plugin_json picks):
    #   1. Solo:  skills/<plugin>/SKILL.md                       → skills: ["./"]
    #   2. Multi: skills/<plugin>/skills/<a>/SKILL.md
    #             skills/<plugin>/skills/<b>/SKILL.md  ...        → skills: ["./skills/"]
    # The plugin-level description for the multi layout is operator-authored
    # at skills/<plugin>/.claude-plugin/plugin.json (read by
    # _read_source_plugin_description), since there's no single SKILL.md to
    # pull it from.
    prefix = "skill"
    source_directory = REPO_ROOT / "src" / "skills"
    category = "skill"

    def build_plugin_json(self, name: str) -> dict:
        base = _base_plugin_shape(self, name)
        src = self.source_directory / name
        root_skill = src / "SKILL.md"
        skills_subdir = src / "skills"

        has_root = root_skill.exists()
        # ``_is_candidate_subdir`` filters out junk dirs (``__pycache__``,
        # hidden dirs) so a stray ``skills/__pycache__/SKILL.md`` doesn't
        # falsely flip ``has_subdir=True`` and route a solo plugin into
        # multi-layout emission.
        has_subdir = skills_subdir.is_dir() and any(
            (d / "SKILL.md").exists()
            for d in skills_subdir.iterdir()
            if _is_candidate_subdir(d)
        )

        if has_root and has_subdir:
            raise ValueError(
                f"Source plugin {src} contains BOTH a root SKILL.md AND a "
                f"skills/ subdir with skill children. Pick one layout: either "
                f"move the root SKILL.md into skills/<name>/ or remove the "
                f"skills/ subdir."
            )
        if not has_root and not has_subdir:
            raise ValueError(
                f"Source plugin {src} contains neither a root SKILL.md "
                f"(single-skill layout) nor a skills/<name>/SKILL.md subdir "
                f"(multi-skill layout). Create one or the other."
            )

        # Solo-layout description fallback chain (most specific first):
        #   1. SKILL.md frontmatter ``description:`` — the per-skill tooltip
        #      doubles as a sensible plugin description when there's only one
        #      skill in the plugin.
        #   2. ``<src>/.claude-plugin/plugin.json`` ``description`` — operator-
        #      authored plugin-level one-liner (separate concern but the right
        #      backstop when frontmatter is absent).
        #   3. Dir name — last resort, handled inside the helper.
        # Multi-layout has no single SKILL.md, so it goes straight to the
        # plugin-level description (which is the right shape for marketplace
        # listing when the plugin ships multiple skills).
        if has_root:
            fm = _frontmatter(root_skill)
            base["description"] = (
                fm.get("description") or _read_source_plugin_description(src, name)
            )
        else:
            base["description"] = _read_source_plugin_description(src, name)
        base["skills"] = ["./"] if has_root else ["./skills/"]
        base["keywords"] = ["skill", name]
        return base

    def emit(self, name: str, target_dir: Path) -> None:
        # Copy entire source tree (SKILL.md or skills/<n>/SKILL.md, plus
        # any scripts/ references/ etc.)
        shutil.copytree(
            self.source_directory / name,
            target_dir,
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )
        # Write plugin.json under .claude-plugin/ (overrides any source copy)
        write_plugin_json(target_dir, self.build_plugin_json(name))


class RuleConstruct:
    """Rule construct — not a Claude plugin component (F8, 2026-05-26).

    Per code.claude.com/docs/en/plugins-reference#plugin-components-reference
    (fetched 2026-05-26), Claude's plugin component list does not include
    rules. Claude reads rules from ``.claude/rules/*.md`` via the memory
    subsystem (code.claude.com/docs/en/memory#organize-rules-with-claude-rules,
    fetched 2026-05-26), so we no longer emit a ``.claude-plugin/plugin.json``
    or an ``activate.sh`` wrapper into ``_generated/rule-<name>/``.

    The dir is still created (with rule.md inside) so per-platform
    manifests for Cursor / Codex can land their own
    ``.cursor-plugin/plugin.json`` and ``.codex-plugin/plugin.json``
    files via Phase 1.5 — those platforms still surface our rules.
    """

    prefix = "rule"
    source_directory = REPO_ROOT / "src" / "rules"
    category = "rule"

    def build_plugin_json(self, name: str) -> dict:
        # No Claude plugin.json is written for rules, but the description
        # is still consumed by per-platform manifest builders (Cursor /
        # Codex) via _description_from_construct in platforms.py.
        base = _base_plugin_shape(self, name)
        base["description"] = (
            f"Rule: {name}. On Cursor/Windsurf this surfaces as a workspace "
            f"rule; on Claude Code, copy rules/{name}/rule.md into "
            f"~/.claude/rules/ (or .claude/rules/ for project scope) per "
            f"code.claude.com/docs/en/memory#organize-rules-with-claude-rules."
        )
        base["keywords"] = ["rule", name]
        return base

    def emit(self, name: str, target_dir: Path) -> None:
        # Copy rule.md into rules/<name>.md subdir so per-platform
        # manifests (Cursor / Codex) can point at it. No activate.sh
        # and no .claude-plugin/plugin.json: F8 retired the
        # rule-as-Claude-plugin emission.
        rules_subdir = target_dir / "rules"
        rules_subdir.mkdir(parents=True, exist_ok=True)
        shutil.copy(
            self.source_directory / name / "rule.md",
            rules_subdir / f"{name}.md",
        )

        # Copy README.md if present (Cursor/Codex consumers may surface it)
        readme = self.source_directory / name / "README.md"
        if readme.exists():
            shutil.copy(readme, target_dir / "README.md")


class CommandConstruct:
    prefix = "command"
    source_directory = REPO_ROOT / "src" / "commands"
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
    source_directory = REPO_ROOT / "src" / "agents"
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
    source_directory = REPO_ROOT / "src" / "hooks"
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
    source_directory = REPO_ROOT / "src" / "mcp-servers"
    category = "mcp"

    def build_plugin_json(self, name: str) -> dict:
        base = _base_plugin_shape(self, name)
        source_pj = _load_plugin_json(
            self.source_directory / name / ".claude-plugin" / "plugin.json"
        )
        base["description"] = _read_source_plugin_description(
            self.source_directory / name, name
        )
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
    source_directory = REPO_ROOT / "src" / "lsp-servers"
    category = "lsp"

    def build_plugin_json(self, name: str) -> dict:
        base = _base_plugin_shape(self, name)
        source_pj = _load_plugin_json(
            self.source_directory / name / ".claude-plugin" / "plugin.json"
        )
        base["description"] = _read_source_plugin_description(
            self.source_directory / name, name
        )
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
    source_directory = REPO_ROOT / "src" / "monitors"
    category = "monitor"

    def build_plugin_json(self, name: str) -> dict:
        base = _base_plugin_shape(self, name)
        source_pj = _load_plugin_json(
            self.source_directory / name / ".claude-plugin" / "plugin.json"
        )
        base["description"] = _read_source_plugin_description(
            self.source_directory / name, name
        )
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
    source_directory = REPO_ROOT / "src" / "output-styles"
    category = "output-style"

    def build_plugin_json(self, name: str) -> dict:
        base = _base_plugin_shape(self, name)
        source_pj = _load_plugin_json(
            self.source_directory / name / ".claude-plugin" / "plugin.json"
        )
        base["description"] = _read_source_plugin_description(
            self.source_directory / name, name
        )
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
    source_directory = REPO_ROOT / "src" / "themes"
    category = "theme"

    def build_plugin_json(self, name: str) -> dict:
        base = _base_plugin_shape(self, name)
        source_pj = _load_plugin_json(
            self.source_directory / name / ".claude-plugin" / "plugin.json"
        )
        base["description"] = _read_source_plugin_description(
            self.source_directory / name, name
        )
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
