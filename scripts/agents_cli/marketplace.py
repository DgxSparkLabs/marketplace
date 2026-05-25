"""marketplace add / list / remove — manage registered marketplace URLs.

Lightweight per-user registry persisted at ``~/.agents/marketplaces.json``.
Each entry stores ``name`` + ``url``; the active marketplace defaults to the
first entry. This mirrors the per-platform marketplace registries (claude /
codex) but at the .agents/ layer.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from .utils.paths import user_home


def _registry_path() -> Path:
    return user_home() / ".agents" / "marketplaces.json"


def _load() -> list[dict]:
    p = _registry_path()
    if not p.exists():
        return []
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []


def _save(entries: list[dict]) -> None:
    p = _registry_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(entries, indent=2) + "\n", encoding="utf-8")


def cmd_add(url: str, name: str | None = None) -> int:
    entries = _load()
    # Default name = repo basename, stripped of .git
    if not name:
        name = url.rstrip("/").rsplit("/", 1)[-1].removesuffix(".git")
    for e in entries:
        if e["name"] == name:
            print(f"marketplace '{name}' already registered ({e['url']}).", file=sys.stderr)
            return 1
    entries.append({"name": name, "url": url})
    _save(entries)
    print(f"Registered marketplace '{name}' → {url}")
    return 0


def cmd_list() -> int:
    entries = _load()
    if not entries:
        print("No marketplaces registered. Use `agents marketplace add <url>`.")
        return 0
    print(f"Registered marketplaces ({len(entries)}):")
    for e in entries:
        print(f"  {e['name']:<32s} {e['url']}")
    return 0


def cmd_remove(name: str) -> int:
    entries = _load()
    kept = [e for e in entries if e["name"] != name]
    if len(kept) == len(entries):
        print(f"error: no marketplace named '{name}'.", file=sys.stderr)
        return 1
    _save(kept)
    print(f"Removed marketplace '{name}'.")
    return 0
