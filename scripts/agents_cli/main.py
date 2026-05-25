#!/usr/bin/env python3
"""agents — cross-platform marketplace CLI shim.

Subcommands (D-3):
  install    Install a plugin to project or user scope.
  uninstall  Remove a plugin.
  upgrade    Reinstall a plugin (or --all) to pull latest.
  list       List installed plugins; --available lists everything in the marketplace.
  info       Show metadata for one plugin.
  marketplace add|list|remove   Manage registered marketplaces.

Global flags:
  --scope project|user   Install scope (default: project) (D-6).
  --agents-only          Strict mode: write only to .agents/ paths (D-13 Option C).
  --ref <branch>         Marketplace branch to clone (default: main) (D-4).
  --version              Print the CLI version.
  --help                 Show help.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Make sibling 'converters' / 'agents_cli' importable when run via `uv run` or
# `python -m agents_cli.main` from a different cwd.
_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from agents_cli import __version__, install as install_mod, list as list_mod, marketplace as marketplace_mod


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="agents",
        description="Cross-platform marketplace CLI for .agents/ + per-platform install.",
    )
    p.add_argument("--version", action="version", version=f"agents {__version__}")
    sub = p.add_subparsers(dest="command", required=False)

    # install
    p_install = sub.add_parser("install", help="Install a plugin.")
    p_install.add_argument("plugin", help="Plugin name (e.g. skill-example).")
    p_install.add_argument("--scope", choices=["project", "user"], default="project")
    p_install.add_argument("--agents-only", action="store_true",
                           help="Write only to .agents/ paths (skip per-platform spray).")
    p_install.add_argument("--ref", default="main", help="Marketplace branch (default: main).")
    p_install.add_argument("--marketplace-root", default=None,
                           help="Use a local marketplace checkout instead of cloning (testing).")

    # uninstall
    p_uninstall = sub.add_parser("uninstall", help="Uninstall a plugin.")
    p_uninstall.add_argument("plugin")
    p_uninstall.add_argument("--scope", choices=["project", "user"], default="project")
    p_uninstall.add_argument("--agents-only", action="store_true")

    # upgrade
    p_upgrade = sub.add_parser("upgrade", help="Reinstall a plugin (or --all) to pull latest.")
    p_upgrade.add_argument("plugin", nargs="?", default=None)
    p_upgrade.add_argument("--all", dest="all_plugins", action="store_true")
    p_upgrade.add_argument("--scope", choices=["project", "user"], default="project")
    p_upgrade.add_argument("--agents-only", action="store_true")
    p_upgrade.add_argument("--ref", default="main")
    p_upgrade.add_argument("--marketplace-root", default=None)

    # list
    p_list = sub.add_parser("list", help="List installed plugins.")
    p_list.add_argument("--available", action="store_true",
                        help="List every plugin in the marketplace (not just installed).")
    p_list.add_argument("--scope", choices=["project", "user"], default="project")
    p_list.add_argument("--type", dest="type_filter", default=None,
                        help="Filter --available by construct type.")

    # info
    p_info = sub.add_parser("info", help="Show metadata for a plugin.")
    p_info.add_argument("plugin")

    # marketplace (with nested sub)
    p_market = sub.add_parser("marketplace", help="Manage marketplace registrations.")
    market_sub = p_market.add_subparsers(dest="marketplace_command", required=True)
    m_add = market_sub.add_parser("add", help="Register a marketplace URL.")
    m_add.add_argument("url")
    m_add.add_argument("--name", default=None)
    market_sub.add_parser("list", help="List registered marketplaces.")
    m_remove = market_sub.add_parser("remove", help="Unregister a marketplace.")
    m_remove.add_argument("name")

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 0

    if args.command == "install":
        root = Path(args.marketplace_root).resolve() if args.marketplace_root else None
        return install_mod.install(
            args.plugin, scope=args.scope, agents_only=args.agents_only,
            ref=args.ref, marketplace_root=root,
        )
    if args.command == "uninstall":
        return install_mod.uninstall(
            args.plugin, scope=args.scope, agents_only=args.agents_only,
        )
    if args.command == "upgrade":
        root = Path(args.marketplace_root).resolve() if args.marketplace_root else None
        return install_mod.upgrade(
            args.plugin, all_plugins=args.all_plugins,
            scope=args.scope, agents_only=args.agents_only,
            ref=args.ref, marketplace_root=root,
        )
    if args.command == "list":
        return list_mod.cmd_list(
            scope=args.scope, available=args.available, type_filter=args.type_filter,
        )
    if args.command == "info":
        return list_mod.cmd_info(args.plugin)
    if args.command == "marketplace":
        if args.marketplace_command == "add":
            return marketplace_mod.cmd_add(args.url, name=args.name)
        if args.marketplace_command == "list":
            return marketplace_mod.cmd_list()
        if args.marketplace_command == "remove":
            return marketplace_mod.cmd_remove(args.name)

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
