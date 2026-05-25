"""list / info — enumerate installed plugins, list available plugins, show info."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from .constructs import PREFIX_TO_HANDLER
from .utils import git_ops
from .utils.paths import project_root, user_home


_PROJECT_SCOPE_DIRS = {
    "skill":   (".agents", "skills"),
    "rule":    (".agents", "rules"),
    "agent":   (".agents", "agents"),
    "hook":    (".agents", "hooks"),
    "mcp":     (".agents", "mcp-servers"),
    "command": (".agents", "commands"),
}


def installed_plugins(*, scope: str = "project") -> list[str]:
    """Return installed plugin names (with prefix) at the given scope.

    Only inspects the ``.agents/`` canonical paths (the source of truth in our
    install model); per-platform paths are derivative.
    """
    base = project_root() if scope == "project" else user_home()
    out: list[str] = []
    for prefix, parts in _PROJECT_SCOPE_DIRS.items():
        directory = base.joinpath(*parts)
        if not directory.exists():
            continue
        for entry in sorted(directory.iterdir()):
            if entry.is_dir():
                out.append(f"{prefix}-{entry.name}")
            elif entry.is_file():
                out.append(f"{prefix}-{entry.stem}")
    return out


def cmd_list(*, scope: str = "project", available: bool = False, type_filter: str | None = None) -> int:
    if available:
        return _list_available(type_filter=type_filter)

    names = installed_plugins(scope=scope)
    if not names:
        print(f"No plugins installed at {scope} scope.")
        return 0
    print(f"Installed plugins ({scope} scope):")
    for n in names:
        print(f"  {n}")
    return 0


def _list_available(*, type_filter: str | None) -> int:
    """List every plugin shipped in the marketplace.

    Reads ``.claude-plugin/marketplace.json`` from the cached clone (or local
    checkout via AGENTS_MARKETPLACE_LOCAL=<path>).
    """
    import os
    local = os.environ.get("AGENTS_MARKETPLACE_LOCAL")
    try:
        if local:
            root = git_ops.use_local_checkout(Path(local))
        else:
            root = git_ops.ensure_clone()
    except Exception as exc:
        print(f"error: marketplace clone failed: {exc}", file=sys.stderr)
        return 1

    manifest_path = root / ".claude-plugin" / "marketplace.json"
    if not manifest_path.exists():
        print(f"error: marketplace manifest missing at {manifest_path}", file=sys.stderr)
        return 1
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    plugins = data.get("plugins", [])
    if type_filter:
        plugins = [p for p in plugins if p.get("category") == type_filter]
    if not plugins:
        print("(no matching plugins)")
        return 0
    print(f"Available plugins ({len(plugins)}):")
    for p in plugins:
        print(f"  {p['name']:<40s} {p.get('category', ''):<12s} {p.get('description', '')[:80]}")
    return 0


def cmd_info(plugin: str) -> int:
    """Show metadata for one plugin (from marketplace.json)."""
    import os
    local = os.environ.get("AGENTS_MARKETPLACE_LOCAL")
    try:
        if local:
            root = git_ops.use_local_checkout(Path(local))
        else:
            root = git_ops.ensure_clone()
    except Exception as exc:
        print(f"error: marketplace clone failed: {exc}", file=sys.stderr)
        return 1
    manifest = json.loads(
        (root / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8")
    )
    for entry in manifest.get("plugins", []):
        if entry.get("name") == plugin:
            for k, v in entry.items():
                print(f"{k}: {v}")
            return 0
    print(f"error: {plugin} not found.", file=sys.stderr)
    return 1
