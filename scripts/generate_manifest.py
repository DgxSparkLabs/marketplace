#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
generate_manifest.py — thin orchestrator for the marketplace generator.

Phases:
  1. Individual construct plugins: emit one _generated/<prefix>-<name>/ per source
  2a. Catalog bundles: emit one _generated/bundle-<name>/ per [bundle.*] in catalog.toml
  2b. Code-generated catch-alls: emit bundle-<prefix>-all per construct with sources
  3. Cross-platform mirrors: call Platform.emit for each construct instance
  4. Gemini extension manifest: write .gemini/gemini-extension.json
  5. Top-level marketplace.json: write from in-memory entries (decision #17)

Usage:
  uv run scripts/generate_manifest.py          # write everything
  uv run scripts/generate_manifest.py --check  # exit non-zero if output differs
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

# Add scripts/ to sys.path so sibling modules resolve correctly
sys.path.insert(0, str(Path(__file__).resolve().parent))

from bundles import _auto_description, load_bundles
from constructs import CONSTRUCTS
from platforms import GeminiPlatform, PLATFORMS
from utils import (
    CATALOG,
    GENERATED,
    MARKETPLACE_JSON,
    REPO_ROOT,
    _marketplace_author,
    _marketplace_description,
    _marketplace_name,
    _marketplace_version,
    _to_json,
    scan_source_dir,
    write_plugin_json,
)


def _make_marketplace_entry(
    plugin_json: dict, plugin_dir: Path, category: str
) -> dict:
    """Build a marketplace.json plugin entry from an in-memory plugin.json dict."""
    return {
        "name": plugin_json["name"],
        "source": f"./{plugin_dir.relative_to(REPO_ROOT).as_posix()}",
        "description": plugin_json["description"],
        "version": plugin_json["version"],
        "author": plugin_json["author"],
        "category": category,
    }


def _write_marketplace_json(entries: list[dict]) -> None:
    """Write the top-level marketplace.json from in-memory entries.

    Sorted by category then name for deterministic diffs.
    """
    entries.sort(key=lambda e: (e["category"], e["name"]))
    manifest = {
        "name": _marketplace_name(),
        "owner": _marketplace_author(),
        "plugins": entries,
    }
    MARKETPLACE_JSON.parent.mkdir(parents=True, exist_ok=True)
    MARKETPLACE_JSON.write_text(_to_json(manifest), encoding="utf-8")


def _emit_bundle_plugin(
    name: str,
    description: str,
    deps: list[str],
    category: str = "bundle",
) -> dict:
    """Write a single bundle plugin under _generated/bundle-<name>/.

    Returns the marketplace.json entry for in-memory aggregation.

    Shared by Phase 2a (catalog bundles) and Phase 2b (code-generated
    catch-alls). Phase 2a callers resolve description fallback before calling.
    """
    plugin_name = f"bundle-{name}"
    plugin_json = {
        "name": plugin_name,
        "version": _marketplace_version(),
        "description": description,
        "author": _marketplace_author(),
        "dependencies": deps,
    }
    plugin_dir = GENERATED / plugin_name
    plugin_dir.mkdir(parents=True, exist_ok=True)
    write_plugin_json(plugin_dir, plugin_json)
    return _make_marketplace_entry(plugin_json, plugin_dir, category)


def main() -> None:
    marketplace_entries: list[dict] = []

    # Clear and recreate _generated/ (clean slate each run)
    if GENERATED.exists():
        shutil.rmtree(GENERATED)
    GENERATED.mkdir()

    # ── Phase 1: Individual construct plugins ──────────────────────────────────
    for construct in CONSTRUCTS.values():
        for name in scan_source_dir(construct.source_directory):
            plugin_json = construct.build_plugin_json(name)
            plugin_dir = GENERATED / f"{construct.prefix}-{name}"
            plugin_dir.mkdir(parents=True, exist_ok=True)
            construct.emit(name, plugin_dir)
            marketplace_entries.append(
                _make_marketplace_entry(plugin_json, plugin_dir, construct.category)
            )

    # ── Phase 2a: User-declared catalog bundles ────────────────────────────────
    bundles = load_bundles(CATALOG, CONSTRUCTS)
    for bundle in bundles:
        deps = bundle.resolve_dependencies(CONSTRUCTS)
        description = bundle.description or _auto_description(deps)
        marketplace_entries.append(
            _emit_bundle_plugin(bundle.name, description, deps)
        )

    # ── Phase 2b: Code-generated catch-all bundles (decision #23) ─────────────
    #    For each construct: emit bundle-<prefix>-all with deps = every instance.
    #    Skip constructs that have no source instances (no empty bundles).
    for construct in CONSTRUCTS.values():
        deps = [
            f"{construct.prefix}-{n}"
            for n in scan_source_dir(construct.source_directory)
        ]
        if not deps:
            continue
        marketplace_entries.append(
            _emit_bundle_plugin(
                name=f"{construct.prefix}-all",
                description=f"Every {construct.prefix} in the marketplace",
                deps=deps,
            )
        )

    # ── Phase 3: Cross-platform mirrors ───────────────────────────────────────
    # Wipe all mirror roots first for a clean slate
    for platform in PLATFORMS.values():
        if platform.mirror_directory is not None and platform.mirror_directory.exists():
            shutil.rmtree(platform.mirror_directory)

    for platform in PLATFORMS.values():
        if platform.mirror_directory is None:
            continue
        for construct_cls in platform.supports:
            construct = next(
                c for c in CONSTRUCTS.values() if isinstance(c, construct_cls)
            )
            for name in scan_source_dir(construct.source_directory):
                platform.emit(construct, name)

    # ── Phase 4: Gemini extension manifest ────────────────────────────────────
    gemini = next(p for p in PLATFORMS.values() if isinstance(p, GeminiPlatform))
    gemini.emit_extension_manifest()

    # ── Phase 5: Top-level marketplace.json (from in-memory entries) ──────────
    _write_marketplace_json(marketplace_entries)

    # Summary
    from collections import Counter
    cats = Counter(e["category"] for e in marketplace_entries)
    print(f"Generated {len(marketplace_entries)} plugin entries in marketplace.json")
    for cat, count in sorted(cats.items()):
        print(f"  {cat}: {count}")


def _check_drift() -> int:
    """Snapshot current outputs, regenerate, diff. Return 0 if identical, 1 if drift."""

    def snapshot_tree(roots: list[Path]) -> dict[str, bytes]:
        out: dict[str, bytes] = {}
        for root in roots:
            if not root.exists():
                continue
            for p in sorted(root.rglob("*")):
                if p.is_file():
                    out[str(p.relative_to(REPO_ROOT))] = p.read_bytes()
        return out

    mirror_dirs = [
        p.mirror_directory
        for p in PLATFORMS.values()
        if p.mirror_directory is not None
    ]
    targets = [GENERATED, MARKETPLACE_JSON.parent] + mirror_dirs

    before = snapshot_tree(targets)
    main()
    after = snapshot_tree(targets)

    if before == after:
        print("OK: generated content matches committed content.")
        return 0

    missing = sorted(set(before) - set(after))
    added = sorted(set(after) - set(before))
    changed = sorted(p for p in (set(before) & set(after)) if before[p] != after[p])

    print("DRIFT detected. Run `uv run scripts/generate_manifest.py` and commit the result.")
    for p in missing:
        print(f"  removed:  {p}")
    for p in added:
        print(f"  added:    {p}")
    for p in changed:
        print(f"  changed:  {p}")
    return 1


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(_check_drift())
    main()
