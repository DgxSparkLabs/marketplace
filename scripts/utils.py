#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
utils.py — shared helpers for the marketplace generator.

Provides:
  - GENERATED, MARKETPLACE_JSON, CATALOG constants
  - scan_source_dir   — list instance names under a source directory
  - _load_plugin_json — cached JSON read of a source plugin.json
  - _frontmatter      — YAML frontmatter parser for markdown files
  - _to_json          — deterministic JSON pretty-print
  - _marketplace_*    — MARKETPLACE.toml field accessors
  - write_plugin_json — write .claude-plugin/plugin.json under a target dir
"""

from __future__ import annotations

import json
import tomllib
from functools import cache
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GENERATED = REPO_ROOT / "_generated"
MARKETPLACE_JSON = REPO_ROOT / ".claude-plugin" / "marketplace.json"
CATALOG = REPO_ROOT / "catalog.toml"
MARKETPLACE_TOML = REPO_ROOT / "MARKETPLACE.toml"


def scan_source_dir(source_dir: Path) -> list[str]:
    """List instance names (subdirectory names) under a source directory.

    Returns an empty list if the directory doesn't exist.
    Results are sorted for deterministic output.
    """
    if not source_dir.exists():
        return []
    return sorted(d.name for d in source_dir.iterdir() if d.is_dir())


@cache
def _load_plugin_json(path: Path) -> dict:
    """Cached read of a plugin.json file. Path must be absolute."""
    return json.loads(path.read_text(encoding="utf-8"))


def _frontmatter(path: Path) -> dict:
    """Parse YAML frontmatter (key: value lines) from a markdown file.

    Handles simple scalar values only — lists and nested objects are not
    parsed. Returns an empty dict if no frontmatter block is found.
    """
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    fm_text = text[4:end]
    result: dict[str, str] = {}
    for raw in fm_text.splitlines():
        raw = raw.strip()
        if not raw or raw.startswith("#"):
            continue
        if ":" not in raw:
            continue
        key, _, val = raw.partition(":")
        result[key.strip()] = val.strip().strip('"').strip("'")
    return result


def _to_json(obj: dict) -> str:
    """Pretty-print a dict as JSON with 2-space indent and trailing newline."""
    return json.dumps(obj, indent=2) + "\n"


@cache
def _load_marketplace_toml() -> dict:
    """Load and cache MARKETPLACE.toml."""
    with open(MARKETPLACE_TOML, "rb") as f:
        return tomllib.load(f)


def _marketplace_version() -> str:
    """Read the marketplace version from MARKETPLACE.toml."""
    return _load_marketplace_toml()["marketplace"]["version"]


def _marketplace_author() -> dict:
    """Build author dict (name + url) from MARKETPLACE.toml."""
    mp = _load_marketplace_toml()
    return {"name": mp["owner"]["name"], "url": mp["owner"]["url"]}


def _marketplace_name() -> str:
    """Read the marketplace name from MARKETPLACE.toml.

    This is the string after the ``@`` in
    ``claude plugin install <plugin>@<marketplace>``. Single source of
    truth at MARKETPLACE.toml line 12. Written into the top-level
    ``.claude-plugin/marketplace.json`` ``name`` field by
    ``_write_marketplace_json`` in ``scripts/generate_manifest.py``.
    See docs/ADDING_A_CONSTRUCT.md § "Trace each fragment to its source".
    """
    return _load_marketplace_toml()["marketplace"]["name"]


def _marketplace_description() -> str:
    """Read the marketplace description from MARKETPLACE.toml.

    Used by GeminiPlatform.emit_extension_manifest() for the
    .gemini/gemini-extension.json file.
    """
    return _load_marketplace_toml()["marketplace"]["description"]


def write_plugin_json(target_dir: Path, plugin_json: dict) -> None:
    """Write plugin.json under target_dir/.claude-plugin/plugin.json.

    Creates the .claude-plugin/ subdirectory if it doesn't exist.

    Uses ``newline=""`` so the embedded ``\\n`` line endings produced by
    ``_to_json`` are written verbatim on every platform (without this,
    Python on Windows translates ``\\n`` to ``\\r\\n`` and breaks our
    byte-identity drift check against LF-committed files).
    """
    plugin_subdir = target_dir / ".claude-plugin"
    plugin_subdir.mkdir(parents=True, exist_ok=True)
    (plugin_subdir / "plugin.json").write_text(
        _to_json(plugin_json), encoding="utf-8", newline=""
    )
