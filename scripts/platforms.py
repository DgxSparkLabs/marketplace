#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
platforms.py — 7 Platform classes implementing the Platform protocol.

Each class encapsulates:
  - name             : platform identifier
  - mirror_directory : where to write mirrored content (None for ClaudeCode)
  - supports         : set of Construct CLASSES this platform handles
  - emit(construct, name) : write mirrored content for one construct instance
  - build_plugin_json(construct, name) -> dict : produce a per-platform per-plugin
      manifest dict. Called by generator Phase 1.5, gated on
      ``type(construct) in self.supports``. Platforms that do not host plugin
      manifests (e.g. AgentsPlatform) return ``{}``; the generator skips empty
      returns. ClaudeCodePlatform delegates to the construct's own
      ``build_plugin_json`` so the per-plugin Claude schema stays a single source
      of truth.
  - emit_extension_manifest() : (GeminiPlatform only) write repo-level manifest

Registry:
  PLATFORMS: dict[str, Platform]  — single source of truth
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Protocol

from constructs import (
    CONSTRUCTS,
    AgentConstruct,
    CommandConstruct,
    Construct,
    HookConstruct,
    LSPConstruct,
    MCPConstruct,
    MonitorConstruct,
    OutputStyleConstruct,
    RuleConstruct,
    SkillConstruct,
    ThemeConstruct,
)
from utils import (
    REPO_ROOT,
    _frontmatter,
    _marketplace_description,
    _marketplace_name,
    _marketplace_version,
    _to_json,
)

# Standard ignore pattern used in every copytree call.
# Excludes per-platform manifest directories so they don't bleed across mirrors.
_COPY_IGNORE = shutil.ignore_patterns(
    "__pycache__", "*.pyc",
    ".claude-plugin", ".codex-plugin", ".cursor-plugin",
)


class Platform(Protocol):
    """An AI coding platform we generate config/mirror outputs for."""

    name: str                         # e.g., "codex"
    mirror_directory: Path | None     # None for ClaudeCode (no separate mirror)
    supports: set[type[Construct]]    # CLASSES of supported constructs

    def emit(self, construct: Construct, name: str) -> None:
        """Emit the mirror for this construct instance under mirror_directory."""
        ...

    def build_plugin_json(self, construct: Construct, name: str) -> dict:
        """Produce the per-platform per-plugin manifest dict (no I/O).

        Called by generator Phase 1.5 for each (plugin, platform) pair where
        ``type(construct) in self.supports``. Return ``{}`` to skip emission
        (e.g. AgentsPlatform hosts skill content, not plugin manifests).
        """
        ...


# ─── helpers ──────────────────────────────────────────────────────────────────

def _description_from_construct(construct: Construct, name: str) -> str:
    """Extract a human-readable description from a construct instance.

    Tries the construct's own build_plugin_json (which already does this
    logic per-type) and falls back to the bare name.
    """
    try:
        return construct.build_plugin_json(name).get("description", name)
    except Exception:
        return name


# ─── Platform implementations ─────────────────────────────────────────────────

class ClaudeCodePlatform:
    """Canonical platform — no separate mirror.

    Claude Code reads .claude-plugin/marketplace.json (top-level manifest)
    and per-plugin .claude-plugin/plugin.json files directly. The generator
    writes these in its main phases; no separate mirror is needed.

    build_plugin_json delegates to the construct's own build_plugin_json so
    the per-plugin Claude schema stays a single source of truth.
    """

    name = "claude-code"
    mirror_directory = None
    supports: set[type[Construct]] = {
        SkillConstruct, RuleConstruct, CommandConstruct, AgentConstruct,
        HookConstruct, MCPConstruct, LSPConstruct, MonitorConstruct,
        OutputStyleConstruct, ThemeConstruct,
    }

    def emit(self, construct: Construct, name: str) -> None:
        pass  # no-op; marketplace.json is written by main flow

    def build_plugin_json(self, construct: Construct, name: str) -> dict:
        # Delegate to the construct — single source of truth for Claude schema.
        return construct.build_plugin_json(name)


class CodexPlatform:
    """Codex CLI platform.

    Codex reuses our .claude-plugin/marketplace.json directly and also
    supports skill mirrors at .codex/skills/<name>/.

    build_plugin_json produces a Codex-shaped manifest per
    developers.openai.com/codex/plugins/build (fetched 2026-05-24):
      Required: name, version, description
      Optional component pointers: skills, mcpServers, hooks
    """

    name = "codex"
    mirror_directory: Path = REPO_ROOT / ".codex"
    supports: set[type[Construct]] = {SkillConstruct, MCPConstruct, HookConstruct}

    def emit(self, construct: Construct, name: str) -> None:
        dst = self.mirror_directory / "skills" / name
        shutil.copytree(
            construct.source_directory / name,
            dst,
            dirs_exist_ok=True,
            ignore=_COPY_IGNORE,
        )

    def build_plugin_json(self, construct: Construct, name: str) -> dict:
        full_name = f"{construct.prefix}-{name}"
        manifest: dict = {
            "name": full_name,
            "version": "1.0.0",
            "description": _description_from_construct(construct, name),
        }
        if isinstance(construct, SkillConstruct):
            manifest["skills"] = "./skills/"
        elif isinstance(construct, MCPConstruct):
            manifest["mcpServers"] = "./mcp.json"
        elif isinstance(construct, HookConstruct):
            manifest["hooks"] = "./hooks/hooks.json"
        return manifest


class GeminiPlatform:
    """Gemini CLI platform.

    Gemini expects:
      - .gemini/gemini-extension.json (repo-level extension manifest)
      - .gemini/skills/<name>/ (per-skill mirror)
    """

    name = "gemini"
    mirror_directory: Path = REPO_ROOT / ".gemini"
    supports: set[type[Construct]] = {SkillConstruct}

    def emit(self, construct: Construct, name: str) -> None:
        dst = self.mirror_directory / "skills" / name
        shutil.copytree(
            construct.source_directory / name,
            dst,
            dirs_exist_ok=True,
            ignore=_COPY_IGNORE,
        )

    def build_plugin_json(self, construct: Construct, name: str) -> dict:
        # Gemini doesn't use a per-plugin manifest format; extension install
        # is registry-level via gemini-extension.json. Return {} to skip.
        return {}

    def emit_extension_manifest(self) -> None:
        """Write the repo-level .gemini/gemini-extension.json.

        Called once by the generator main flow (Phase 4). The file requires
        name + version; description is optional but recommended.
        """
        manifest = {
            "name": _marketplace_name(),
            "version": _marketplace_version(),
            "description": _marketplace_description(),
        }
        self.mirror_directory.mkdir(parents=True, exist_ok=True)
        (self.mirror_directory / "gemini-extension.json").write_text(
            _to_json(manifest), encoding="utf-8"
        )


class CursorPlatform:
    """Cursor IDE platform.

    Cursor detects .cursor/rules/<name>.md files on workspace open and reads
    .agents/skills/ for skills. Team-marketplace import requires a root-level
    .cursor-plugin/marketplace.json (emitted by generator Phase 6).

    build_plugin_json returns a minimal manifest — Cursor's plugin.json schema
    only requires ``name``; everything else is auto-discovered from default
    subdirs (skills/, rules/, agents/, ...).
    """

    name = "cursor"
    mirror_directory: Path = REPO_ROOT / ".cursor"
    supports: set[type[Construct]] = {RuleConstruct, SkillConstruct}

    def emit(self, construct: Construct, name: str) -> None:
        if isinstance(construct, RuleConstruct):
            rules_dir = self.mirror_directory / "rules"
            rules_dir.mkdir(parents=True, exist_ok=True)
            src_rule = construct.source_directory / name
            # Prefer platform-specific format file if present; fall back to rule.md
            fmt_file = src_rule / "formats" / "cursor.md"
            if fmt_file.exists():
                shutil.copy(fmt_file, rules_dir / f"{name}.md")
            else:
                shutil.copy(src_rule / "rule.md", rules_dir / f"{name}.md")
        # Skills are served from .agents/ (AgentsPlatform); no .cursor/skills/ needed.

    def build_plugin_json(self, construct: Construct, name: str) -> dict:
        # Cursor only requires `name`; everything else auto-discovers from subdirs.
        return {"name": f"{construct.prefix}-{name}"}


class WindsurfPlatform:
    """Windsurf IDE platform.

    Windsurf detects .windsurf/rules/<name>.md files on workspace open.
    No headless install command — file detection only.
    """

    name = "windsurf"
    mirror_directory: Path = REPO_ROOT / ".windsurf"
    supports: set[type[Construct]] = {RuleConstruct}

    def emit(self, construct: Construct, name: str) -> None:
        rules_dir = self.mirror_directory / "rules"
        rules_dir.mkdir(parents=True, exist_ok=True)
        src_rule = construct.source_directory / name
        # Prefer platform-specific format file if present; fall back to rule.md
        fmt_file = src_rule / "formats" / "windsurf.md"
        if fmt_file.exists():
            shutil.copy(fmt_file, rules_dir / f"{name}.md")
        else:
            shutil.copy(src_rule / "rule.md", rules_dir / f"{name}.md")

    def build_plugin_json(self, construct: Construct, name: str) -> dict:
        # Windsurf has no plugin manifest format; return {} to skip emission.
        return {}


class DevinPlatform:
    """Devin CLI platform.

    Devin reads rules from .cursor/rules/ and .windsurf/rules/ natively
    (verified empirically — no separate .devin/rules/ emission needed).
    Skills are mirrored at .devin/skills/<name>/.
    """

    name = "devin"
    mirror_directory: Path = REPO_ROOT / ".devin"
    supports: set[type[Construct]] = {SkillConstruct}

    def emit(self, construct: Construct, name: str) -> None:
        dst = self.mirror_directory / "skills" / name
        shutil.copytree(
            construct.source_directory / name,
            dst,
            dirs_exist_ok=True,
            ignore=_COPY_IGNORE,
        )

    def build_plugin_json(self, construct: Construct, name: str) -> dict:
        # Devin has no plugin manifest format; return {} to skip emission.
        return {}


class AgentsPlatform:
    """Cross-platform .agents/ skill convergence layer (Decision A1).

    Windsurf, Cursor, and Devin all read `.agents/skills/<name>/SKILL.md`
    natively (verified 2026-05-24 from official docs). This Platform emits
    to that shared path so a single copy serves all three.

    Per Decision A1: AgentsPlatform is a proper Platform class — same shape
    as the other six Platforms: name, mirror_directory, supports, emit.

    build_plugin_json returns {} — AgentsPlatform hosts skill content only,
    not plugin manifests.
    """

    name = "agents"
    mirror_directory: Path = REPO_ROOT / ".agents"
    supports: set[type[Construct]] = {SkillConstruct}

    def emit(self, construct: Construct, name: str) -> None:
        if isinstance(construct, SkillConstruct):
            target = self.mirror_directory / "skills" / name
            shutil.copytree(
                construct.source_directory / name,
                target,
                dirs_exist_ok=True,
                ignore=_COPY_IGNORE,
            )

    def build_plugin_json(self, construct: Construct, name: str) -> dict:
        # AgentsPlatform hosts skill content only, not plugin manifests.
        return {}


# ─── Registry ────────────────────────────────────────────────────────────────

PLATFORMS: dict[str, Platform] = {
    "claude-code": ClaudeCodePlatform(),
    "codex":       CodexPlatform(),
    "gemini":      GeminiPlatform(),
    "cursor":      CursorPlatform(),
    "windsurf":    WindsurfPlatform(),
    "devin":       DevinPlatform(),
    "agents":      AgentsPlatform(),
}
