"""mcp install — copy MCP server config into .agents/mcp-servers/<name>.json.

v1 emits to the .agents/ canonical path only. Per-platform MCP merge (into
Cursor/Codex/Gemini configs) is intentionally deferred — each platform has
its own MCP config file with subtle merge rules that warrant a dedicated
implementer pass.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from ..utils.paths import resolve_mcp


def install(marketplace_root: Path, name: str, *, scope: str, agents_only: bool) -> list[Path]:
    src_plugin_json = (
        marketplace_root / "mcp-servers" / name / ".claude-plugin" / "plugin.json"
    )
    if not src_plugin_json.exists():
        raise FileNotFoundError(f"mcp-{name} not found at {src_plugin_json}")

    # Extract mcpServers payload from the source plugin.json.
    data = json.loads(src_plugin_json.read_text(encoding="utf-8"))
    payload = {"mcpServers": data.get("mcpServers", {})}

    targets = resolve_mcp(name, scope, agents_only)
    written: list[Path] = []
    for dest in [targets.agents_path, *targets.platform_paths]:
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        written.append(dest)
    return written


def uninstall(name: str, *, scope: str, agents_only: bool) -> list[Path]:
    targets = resolve_mcp(name, scope, agents_only)
    removed: list[Path] = []
    for dest in [targets.agents_path, *targets.platform_paths]:
        if dest.exists():
            dest.unlink()
            removed.append(dest)
    return removed
