"""install / uninstall / upgrade orchestration.

Each public function takes already-validated argparse output (Namespace-style)
plus an optional ``marketplace_root`` for tests that want to bypass the clone.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

from .constructs import PREFIX_TO_HANDLER, split_plugin_name
from .utils import git_ops


CLAUDE_ONLY_PREFIXES = {"lsp", "monitor", "output-style", "theme"}


def _resolve_marketplace_root(marketplace_root: Path | None, ref: str) -> Path:
    if marketplace_root is not None:
        return git_ops.use_local_checkout(marketplace_root)
    return git_ops.ensure_clone(ref=ref)


def install(
    plugin: str,
    *,
    scope: str = "project",
    agents_only: bool = False,
    ref: str = "main",
    marketplace_root: Path | None = None,
) -> int:
    """Install one plugin. Returns process exit code."""
    try:
        prefix, name = split_plugin_name(plugin)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    handler = PREFIX_TO_HANDLER.get(prefix)
    if handler is None:
        if prefix in CLAUDE_ONLY_PREFIXES or prefix == "bundle":
            print(
                f"error: '{prefix}' plugins are Claude-only or bundles; "
                f"install via `claude plugin install {plugin}` or the platform's native CLI.",
                file=sys.stderr,
            )
            return 1
        print(f"error: no handler for prefix '{prefix}'", file=sys.stderr)
        return 1

    try:
        root = _resolve_marketplace_root(marketplace_root, ref)
    except Exception as exc:
        print(f"error: marketplace clone failed: {exc}", file=sys.stderr)
        return 1

    try:
        written = handler.install(root, name, scope=scope, agents_only=agents_only)
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        print("hint: try `agents list --available` to see installable plugins.", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"error: write failed ({exc}); try --scope user.", file=sys.stderr)
        return 1

    print(f"Installed {plugin} ({scope} scope, {len(written)} path(s)):")
    for p in written:
        print(f"  {p}")
    return 0


def uninstall(
    plugin: str,
    *,
    scope: str = "project",
    agents_only: bool = False,
) -> int:
    try:
        prefix, name = split_plugin_name(plugin)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    handler = PREFIX_TO_HANDLER.get(prefix)
    if handler is None:
        print(f"error: cannot uninstall '{plugin}' (Claude-only or bundle).", file=sys.stderr)
        return 1

    removed = handler.uninstall(name, scope=scope, agents_only=agents_only)
    if not removed:
        print(f"{plugin} not installed at {scope} scope.")
        return 0
    print(f"Removed {plugin} ({len(removed)} path(s)):")
    for p in removed:
        print(f"  {p}")
    return 0


def upgrade(
    plugin: str | None,
    *,
    all_plugins: bool = False,
    scope: str = "project",
    agents_only: bool = False,
    ref: str = "main",
    marketplace_root: Path | None = None,
) -> int:
    """Upgrade — reinstall on top of existing content. Simplification of D-13."""
    if all_plugins:
        # Scan project / user scope for currently installed plugins and reinstall each.
        from .list import installed_plugins  # local import to avoid cycle
        names = installed_plugins(scope=scope)
        if not names:
            print("nothing to upgrade.")
            return 0
        rc = 0
        for n in names:
            rc |= install(
                n, scope=scope, agents_only=agents_only,
                ref=ref, marketplace_root=marketplace_root,
            )
        return rc
    if not plugin:
        print("error: provide a plugin name or --all.", file=sys.stderr)
        return 2
    return install(
        plugin, scope=scope, agents_only=agents_only,
        ref=ref, marketplace_root=marketplace_root,
    )
