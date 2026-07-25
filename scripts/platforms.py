#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
platforms.py — Platform classes implementing the Platform protocol.

Claude Code is the only supported platform after the skills-only, Claude-only
scope-down (issue #18). The Platform protocol is retained so a future platform
re-expansion (issues #28–#36) is a new class + registry entry, not a redesign.

Each class encapsulates:
  - name             : platform identifier
  - mirror_directory : where to write mirrored content (None for ClaudeCode)
  - supports         : set of Construct CLASSES this platform handles
  - emit(construct, name) : write mirrored content for one construct instance
  - build_plugin_json(construct, name) -> dict : produce a per-platform
      per-plugin manifest dict.

Registry:
  PLATFORMS: dict[str, Platform]  — single source of truth
"""

from __future__ import annotations

from pathlib import Path
from typing import Protocol

from constructs import (
    Construct,
    SkillConstruct,
)


class Platform(Protocol):
    """An AI coding platform we generate config/mirror outputs for."""

    name: str                         # e.g., "claude-code"
    mirror_directory: Path | None     # None for ClaudeCode (no separate mirror)
    supports: set[type[Construct]]    # CLASSES of supported constructs

    def emit(self, construct: Construct, name: str) -> None:
        """Emit the mirror for this construct instance under mirror_directory."""
        ...

    def build_plugin_json(self, construct: Construct, name: str) -> dict:
        """Produce the per-platform per-plugin manifest dict (no I/O)."""
        ...


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
        SkillConstruct,
    }

    def emit(self, construct: Construct, name: str) -> None:
        pass  # no-op; marketplace.json is written by main flow

    def build_plugin_json(self, construct: Construct, name: str) -> dict:
        # Delegate to the construct — single source of truth for Claude schema.
        return construct.build_plugin_json(name)


# ─── Registry ────────────────────────────────────────────────────────────────

PLATFORMS: dict[str, Platform] = {
    "claude-code": ClaudeCodePlatform(),
}
