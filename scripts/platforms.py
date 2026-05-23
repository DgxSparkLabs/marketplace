#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
platforms.py — 6 Platform classes implementing the Platform protocol.

Each class encapsulates:
  - name             : platform identifier
  - mirror_directory : where to write mirrored content (None for ClaudeCode)
  - supports         : set of Construct CLASSES this platform handles
  - emit(construct, name) : write mirrored content for one construct instance
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
    _marketplace_description,
    _marketplace_name,
    _marketplace_version,
    _to_json,
)


class Platform(Protocol):
    """An AI coding platform we generate config/mirror outputs for."""

    name: str                         # e.g., "codex"
    mirror_directory: Path | None     # None for ClaudeCode (no separate mirror)
    supports: set[type[Construct]]    # CLASSES of supported constructs

    def emit(self, construct: Construct, name: str) -> None:
        """Emit the mirror for this construct instance under mirror_directory."""
        ...


# ─── Platform implementations ─────────────────────────────────────────────────

class ClaudeCodePlatform:
    """Canonical platform — no separate mirror.

    Claude Code reads .claude-plugin/marketplace.json (top-level manifest)
    and per-plugin .claude-plugin/plugin.json files directly. The generator
    writes these in its main phases; no separate mirror is needed.
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


class CodexPlatform:
    """Codex CLI platform.

    Codex reuses our .claude-plugin/marketplace.json directly and also
    supports skill mirrors at .codex/skills/<name>/.
    """

    name = "codex"
    mirror_directory: Path = REPO_ROOT / ".codex"
    supports: set[type[Construct]] = {SkillConstruct}

    def emit(self, construct: Construct, name: str) -> None:
        dst = self.mirror_directory / "skills" / name
        shutil.copytree(
            construct.source_directory / name,
            dst,
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )


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
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )

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

    Cursor detects .cursor/rules/<name>.md files on workspace open.
    No headless install command — file detection only.
    """

    name = "cursor"
    mirror_directory: Path = REPO_ROOT / ".cursor"
    supports: set[type[Construct]] = {RuleConstruct}

    def emit(self, construct: Construct, name: str) -> None:
        rules_dir = self.mirror_directory / "rules"
        rules_dir.mkdir(parents=True, exist_ok=True)
        src_rule = construct.source_directory / name
        # Prefer platform-specific format file if present; fall back to rule.md
        fmt_file = src_rule / "formats" / "cursor.md"
        if fmt_file.exists():
            shutil.copy(fmt_file, rules_dir / f"{name}.md")
        else:
            shutil.copy(src_rule / "rule.md", rules_dir / f"{name}.md")


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
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )


# ─── Registry ────────────────────────────────────────────────────────────────

PLATFORMS: dict[str, Platform] = {
    "claude-code": ClaudeCodePlatform(),
    "codex":       CodexPlatform(),
    "gemini":      GeminiPlatform(),
    "cursor":      CursorPlatform(),
    "windsurf":    WindsurfPlatform(),
    "devin":       DevinPlatform(),
}
