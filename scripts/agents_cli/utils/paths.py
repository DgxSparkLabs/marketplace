"""Scope + construct → install target path resolution.

Two scopes (D-6):
  - ``project`` writes under the current working directory (``./.agents/``,
    ``./.cursor/``, ``./.windsurf/``, ``./.gemini/``, ``./.codex/``,
    ``./.claude/``).
  - ``user`` writes ONLY under ``~/.agents/`` (per D-6 user scope is .agents-only).

With ``--agents-only`` set, both scopes collapse to the ``.agents/`` paths only.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class InstallTargets:
    """Filesystem destinations for a single (construct, scope, agents_only) tuple.

    ``agents_path`` is always present (the .agents/ canonical destination).
    ``platform_paths`` is a list of additional per-platform destinations under
    project scope when ``agents_only`` is False; empty otherwise.
    """

    agents_path: Path
    platform_paths: list[Path]


def project_root() -> Path:
    """Project scope base = current working directory."""
    return Path.cwd()


def user_home() -> Path:
    """User scope base = $HOME (or HOMEDRIVE/HOMEPATH on Windows)."""
    return Path.home()


def resolve_skill(name: str, scope: str, agents_only: bool) -> InstallTargets:
    """Skills always live in <base>/.agents/skills/<name>/ (D-2 canonical)."""
    if scope == "user":
        return InstallTargets(user_home() / ".agents" / "skills" / name, [])
    base = project_root()
    return InstallTargets(base / ".agents" / "skills" / name, [])


def resolve_rule(name: str, scope: str, agents_only: bool) -> InstallTargets:
    if scope == "user":
        return InstallTargets(user_home() / ".agents" / "rules" / f"{name}.md", [])
    base = project_root()
    agents = base / ".agents" / "rules" / f"{name}.md"
    if agents_only:
        return InstallTargets(agents, [])
    return InstallTargets(
        agents,
        [
            base / ".cursor" / "rules" / f"{name}.md",
            base / ".windsurf" / "rules" / f"{name}.md",
        ],
    )


def resolve_agent(name: str, scope: str, agents_only: bool) -> InstallTargets:
    if scope == "user":
        return InstallTargets(user_home() / ".agents" / "agents" / f"{name}.md", [])
    base = project_root()
    agents = base / ".agents" / "agents" / f"{name}.md"
    if agents_only:
        return InstallTargets(agents, [])
    return InstallTargets(
        agents,
        [
            base / ".cursor" / "agents" / f"{name}.md",
            base / ".gemini" / "agents" / f"{name}.md",
            base / ".claude" / "agents" / f"{name}.md",
            # Codex .toml destination is computed inside the agent handler
            # because the filename + format conversion live there.
            base / ".codex" / "agents" / f"{name}.toml",
        ],
    )


def resolve_hook(name: str, scope: str, agents_only: bool) -> InstallTargets:
    if scope == "user":
        return InstallTargets(user_home() / ".agents" / "hooks" / f"{name}.json", [])
    base = project_root()
    agents = base / ".agents" / "hooks" / f"{name}.json"
    if agents_only:
        return InstallTargets(agents, [])
    return InstallTargets(
        agents,
        [
            base / ".cursor" / "hooks.json",
            base / ".windsurf" / "hooks.json",
            base / ".gemini" / "hooks" / "hooks.json",
        ],
    )


def resolve_mcp(name: str, scope: str, agents_only: bool) -> InstallTargets:
    if scope == "user":
        return InstallTargets(user_home() / ".agents" / "mcp-servers" / f"{name}.json", [])
    base = project_root()
    agents = base / ".agents" / "mcp-servers" / f"{name}.json"
    if agents_only:
        return InstallTargets(agents, [])
    return InstallTargets(agents, [])  # MCP per-platform merge is platform-specific; v1 = .agents/ only


def resolve_command(name: str, scope: str, agents_only: bool) -> InstallTargets:
    if scope == "user":
        return InstallTargets(user_home() / ".agents" / "commands" / f"{name}.md", [])
    base = project_root()
    agents = base / ".agents" / "commands" / f"{name}.md"
    if agents_only:
        return InstallTargets(agents, [])
    return InstallTargets(
        agents,
        [base / ".cursor" / "commands" / f"{name}.md"],
    )


def cache_dir() -> Path:
    """~/.cache/agents/ — where the CLI clones the marketplace."""
    xdg = os.environ.get("XDG_CACHE_HOME")
    if xdg:
        return Path(xdg) / "agents"
    return user_home() / ".cache" / "agents"
