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
    _load_plugin_json,
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

    Codex reuses our .claude-plugin/marketplace.json directly. Skills are
    served per-plugin via _generated/<plugin>/.codex-plugin/plugin.json
    (Phase 1.5) — the legacy repo-root .codex/skills/ mirror was retired
    (D-1, hermetic act run Q-A1 confirmed Codex never consumed it).

    ``supports`` controls both Phase 3 mirror emission AND Phase 1.5 plugin
    manifest emission. For SkillConstruct, MCPConstruct, and HookConstruct,
    only the ``build_plugin_json`` plugin manifest is emitted (Phase 1.5);
    no mirror directory content is written for these types.

    build_plugin_json produces a Codex-shaped manifest per
    developers.openai.com/codex/plugins/build (fetched 2026-05-24):
      Required: name, version, description
      Optional component pointers: skills, mcpServers, hooks
    """

    name = "codex"
    mirror_directory: Path = REPO_ROOT / ".codex"
    supports: set[type[Construct]] = {
        SkillConstruct, MCPConstruct, HookConstruct, AgentConstruct,
    }

    def emit(self, construct: Construct, name: str) -> None:
        # Skill mirror retired (D-1): skills are surfaced via Phase 1.5
        # _generated/<plugin>/.codex-plugin/plugin.json only.
        # MCP and hook manifests are also handled by build_plugin_json only.
        # Unit 4 adds AgentConstruct: .codex/agents/<n>.toml per
        # developers.openai.com/codex/subagents/ (2026-05-25). The source
        # is Claude-style markdown (D-16); convert at emit time.
        if isinstance(construct, AgentConstruct):
            # Lazy import — only Codex needs the converter, keeps the cycle small.
            from converters.md_to_toml import claude_agent_md_to_codex_toml

            agents_dir = self.mirror_directory / "agents"
            agents_dir.mkdir(parents=True, exist_ok=True)
            src_agents = construct.source_directory / name / "agents"
            if not src_agents.exists():
                return
            for agent_md in sorted(src_agents.glob("*.md")):
                toml_text = claude_agent_md_to_codex_toml(
                    agent_md.read_text(encoding="utf-8")
                )
                (agents_dir / f"{agent_md.stem}.toml").write_text(
                    toml_text, encoding="utf-8", newline=""
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

    The .gemini/ directory is the extension root per
    geminicli.com/docs/extensions/reference/ (2026-05-25). Skills, agents,
    and hooks subdirs are all auto-discovered relative to that root:
      - .gemini/gemini-extension.json (repo-level extension manifest)
      - .gemini/skills/<name>/   (per-skill mirror)
      - .gemini/agents/<n>.md    (sub-agent definitions, Unit 3 / A3)
      - .gemini/hooks/hooks.json (hooks file, Unit 3 / A9)
    """

    name = "gemini"
    mirror_directory: Path = REPO_ROOT / ".gemini"
    supports: set[type[Construct]] = {SkillConstruct, AgentConstruct, HookConstruct}

    def emit(self, construct: Construct, name: str) -> None:
        if isinstance(construct, SkillConstruct):
            dst = self.mirror_directory / "skills" / name
            shutil.copytree(
                construct.source_directory / name,
                dst,
                dirs_exist_ok=True,
                ignore=_COPY_IGNORE,
            )
        elif isinstance(construct, AgentConstruct):
            agents_dir = self.mirror_directory / "agents"
            agents_dir.mkdir(parents=True, exist_ok=True)
            src_agents = construct.source_directory / name / "agents"
            if src_agents.exists():
                for agent_md in sorted(src_agents.glob("*.md")):
                    shutil.copy(agent_md, agents_dir / agent_md.name)
        elif isinstance(construct, HookConstruct):
            # TODO: with multiple hook plugins, this last-writer-wins overwrite.
            # Add merge semantics (concatenate hooks arrays) when a second hook
            # plugin lands. Single plugin today, so direct copy is sufficient.
            hooks_dir = self.mirror_directory / "hooks"
            hooks_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy(
                construct.source_directory / name / "hooks" / "hooks.json",
                hooks_dir / "hooks.json",
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
            _to_json(manifest), encoding="utf-8", newline=""
        )


class CursorPlatform:
    """Cursor IDE platform.

    Cursor detects .cursor/rules/<name>.md files on workspace open, reads
    .agents/skills/ for skills, and (Unit 2) reads .cursor/agents/<n>.md
    for workspace-level sub-agents. Team-marketplace import requires a
    root-level .cursor-plugin/marketplace.json (emitted by generator Phase 6).

    Per Unit 2 (D-10/D-11), ``supports`` now covers six construct types:
    Rule, Skill, Agent, Command, Hook, MCP. Cursor's plugin manifest schema
    (cursor.com/docs/reference/plugins, 2026-05-25) supports the pointer
    fields ``agents``, ``commands``, ``hooks``, ``mcpServers`` and auto-
    discovers from the matching subdirs inside an installed plugin. So
    Command/Hook/MCP need no Phase 3 mirror branch — they are surfaced
    purely through the per-plugin .cursor-plugin/plugin.json (Phase 1.5).
    AgentConstruct is the exception: .cursor/agents/<n>.md is a workspace-
    level file (read before any plugin install) so emit copies it directly.
    """

    name = "cursor"
    mirror_directory: Path = REPO_ROOT / ".cursor"
    supports: set[type[Construct]] = {
        RuleConstruct, SkillConstruct, AgentConstruct,
        CommandConstruct, HookConstruct, MCPConstruct,
    }

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
        elif isinstance(construct, AgentConstruct):
            # Workspace-level sub-agents at .cursor/agents/<n>.md per
            # cursor.com/docs/agent/subagents (2026-05-25). One plugin can
            # contain multiple sub-agent .md files — copy them all.
            agents_dir = self.mirror_directory / "agents"
            agents_dir.mkdir(parents=True, exist_ok=True)
            src_agents = construct.source_directory / name / "agents"
            if src_agents.exists():
                for agent_md in sorted(src_agents.glob("*.md")):
                    shutil.copy(agent_md, agents_dir / agent_md.name)
        # Command/Hook/MCP: no mirror branch — surfaced through Phase 1.5
        # .cursor-plugin/plugin.json auto-discovery only.
        # Skills are served from .agents/ (AgentsPlatform); no .cursor/skills/ needed.

    def build_plugin_json(self, construct: Construct, name: str) -> dict:
        # Per cursor.com/docs/reference/plugins (2026-05-25): name is required;
        # description + version + pointer fields (``agents``, ``commands``,
        # ``hooks``, ``mcpServers``, ``skills``) make installer intent explicit.
        # Without ``description`` and ``version``, Cursor's slash-popup renderer
        # falls back to install metadata (commit SHA, etc.) and produces a
        # mangled display — see docs/research/qa-bug-fixes-2026-05/RESEARCH.md
        # Bug 3 (2026-05-25 QA).
        full_name = f"{construct.prefix}-{name}"
        manifest: dict = {
            "name": full_name,
            "version": _marketplace_version(),
            "description": _description_from_construct(construct, name),
        }
        if isinstance(construct, SkillConstruct):
            manifest["skills"] = "./"  # SKILL.md is at plugin root
        elif isinstance(construct, AgentConstruct):
            manifest["agents"] = "./agents/"
        elif isinstance(construct, CommandConstruct):
            manifest["commands"] = "./commands/"
        elif isinstance(construct, HookConstruct):
            manifest["hooks"] = "./hooks/hooks.json"
        elif isinstance(construct, MCPConstruct):
            # Reuse the source plugin.json's mcpServers value (path or inline dict),
            # mirroring the Codex pattern above.
            source_pj = _load_plugin_json(
                construct.source_directory / name / ".claude-plugin" / "plugin.json"
            )
            manifest["mcpServers"] = source_pj["mcpServers"]
        # RuleConstruct: name + version + description only (no pointer field needed).
        return manifest


class WindsurfPlatform:
    """Windsurf IDE platform.

    Windsurf detects .windsurf/rules/<name>.md files on workspace open and
    (Unit 5) reads .windsurf/hooks.json natively per
    docs.windsurf.com/windsurf/cascade/hooks (2026-05-25). No headless
    install command — file detection only.
    """

    name = "windsurf"
    mirror_directory: Path = REPO_ROOT / ".windsurf"
    supports: set[type[Construct]] = {RuleConstruct, HookConstruct}

    def emit(self, construct: Construct, name: str) -> None:
        if isinstance(construct, RuleConstruct):
            rules_dir = self.mirror_directory / "rules"
            rules_dir.mkdir(parents=True, exist_ok=True)
            src_rule = construct.source_directory / name
            # Prefer platform-specific format file if present; fall back to rule.md
            fmt_file = src_rule / "formats" / "windsurf.md"
            if fmt_file.exists():
                shutil.copy(fmt_file, rules_dir / f"{name}.md")
            else:
                shutil.copy(src_rule / "rule.md", rules_dir / f"{name}.md")
        elif isinstance(construct, HookConstruct):
            # TODO: with multiple hook plugins, this last-writer-wins overwrite.
            # Add merge semantics (concatenate hooks arrays) when a second hook
            # plugin lands. Windsurf reads hooks.json directly at .windsurf/
            # root (no hooks/ subdir, unlike Gemini).
            self.mirror_directory.mkdir(parents=True, exist_ok=True)
            shutil.copy(
                construct.source_directory / name / "hooks" / "hooks.json",
                self.mirror_directory / "hooks.json",
            )

    def build_plugin_json(self, construct: Construct, name: str) -> dict:
        # Windsurf has no plugin manifest format; return {} to skip emission.
        return {}


class DevinPlatform:
    """Devin CLI platform.

    Devin reads rules from .cursor/rules/ and .windsurf/rules/ natively
    (verified empirically — no separate .devin/rules/ emission needed).
    Skills are read from .agents/skills/ natively (verified hermetic act
    run Q-B1 2026-05-25); the legacy .devin/skills/ mirror was retired
    per D-1. SkillConstruct stays in ``supports`` so a future per-plugin
    Devin manifest schema can plug in via Phase 1.5 without code changes.
    """

    name = "devin"
    mirror_directory: Path | None = None
    supports: set[type[Construct]] = {SkillConstruct}

    def emit(self, construct: Construct, name: str) -> None:
        # No mirror directory (D-1): Devin reads .agents/skills/ natively.
        return

    def build_plugin_json(self, construct: Construct, name: str) -> dict:
        # Devin has no plugin manifest format; return {} to skip emission.
        return {}


class AgentsPlatform:
    """Cross-platform .agents/ convergence layer (Decisions A1 + D-12).

    Windsurf, Cursor, and Devin all read `.agents/skills/<name>/SKILL.md`
    natively (verified 2026-05-24 from official docs). This Platform emits
    to that shared path so a single copy serves all three.

    Per Decision A1: AgentsPlatform is a proper Platform class — same shape
    as the other six Platforms: name, mirror_directory, supports, emit.

    Per Decision D-12 (Unit 1): also emits .agents/rules/<name>.md as a
    forward-looking convergence layer. No platform reads this path today
    (verified Q-R1/Q-R2 2026-05-25), but Cursor 2.7+ and Windsurf 2.0 are
    credible adopters — emitting now means we are already in place when
    one of them flips. Raw rule.md is copied; no format conversion (each
    consumer can adopt its own frontmatter conventions later).

    build_plugin_json returns {} — AgentsPlatform hosts content only,
    not plugin manifests.
    """

    name = "agents"
    mirror_directory: Path = REPO_ROOT / ".agents"
    supports: set[type[Construct]] = {SkillConstruct, RuleConstruct}

    def emit(self, construct: Construct, name: str) -> None:
        if isinstance(construct, SkillConstruct):
            target = self.mirror_directory / "skills" / name
            shutil.copytree(
                construct.source_directory / name,
                target,
                dirs_exist_ok=True,
                ignore=_COPY_IGNORE,
            )
        elif isinstance(construct, RuleConstruct):
            rules_dir = self.mirror_directory / "rules"
            rules_dir.mkdir(parents=True, exist_ok=True)
            # Raw rule.md (no frontmatter conversion) per D-12.
            shutil.copy(
                construct.source_directory / name / "rule.md",
                rules_dir / f"{name}.md",
            )

    def build_plugin_json(self, construct: Construct, name: str) -> dict:
        # AgentsPlatform hosts content only, not plugin manifests.
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
