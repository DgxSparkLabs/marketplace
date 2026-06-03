#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
generate_manifest.py — thin orchestrator for the marketplace generator.

Phases:
  1.  Individual construct plugins: emit one _generated/<prefix>-<name>/ per source
  1.5 Per-platform per-plugin manifests: emit .<platform>-plugin/plugin.json
       inside each _generated/<plugin>/ dir, gated on platform.supports (Decision B2)
  2a. Catalog bundles: emit one _generated/bundle-<name>/ per [bundle.*] in catalog.toml
  2b. Code-generated catch-alls: emit bundle-<prefix>-all per construct with sources
  3.  Cross-platform mirrors: call Platform.emit for each construct instance
  4.  Gemini extension manifest: write .gemini/gemini-extension.json
  4.5 Root-level gemini-extension.json: copy .gemini/gemini-extension.json → repo root
  5.  Top-level marketplace.json: write from in-memory entries (decision #17)
  5.5 Codex canonical marketplace at .agents/plugins/marketplace.json (D-14)
  6.  Root-level .cursor-plugin/marketplace.json: write Cursor multi-plugin manifest

Usage:
  uv run scripts/generate_manifest.py          # write everything
  uv run scripts/generate_manifest.py --check  # exit non-zero if output differs
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

# Add scripts/ to sys.path so sibling modules resolve correctly
sys.path.insert(0, str(Path(__file__).resolve().parent))

from bundles import _auto_description, load_bundles
from constructs import CONSTRUCTS
from platforms import ClaudeCodePlatform, CursorPlatform, GeminiPlatform, PLATFORMS
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
    """Build a marketplace.json plugin entry from an in-memory plugin.json dict.

    The marketplace entry ``name`` is the install-time identifier (what the
    operator types after ``claude plugin install``). It is unique per plugin
    and is derived here from ``plugin_dir.name`` (set in Phase 1 as
    ``<construct.prefix>-<source-dir-name>``, e.g. ``skill-example``).

    Post-2026-05-28 (multi-instance-capable refactor): ``plugin_json["name"]``
    is the **plugin's slash namespace** (``<brand>-<construct.prefix>-<source-
    dir-name>``, e.g. ``dgxsparklabs-skill-example``). It is also unique per
    plugin, and the two fields differ only in the brand prefix.

    An earlier short-lived attempt (Path A, ``d641f92``, 2026-05-27) used a
    SHARED ``<brand>-<construct.category>`` name across all plugins of one
    construct type, with the intent of grouping multi-instance components
    under a single slash namespace. Path A was reverted on 2026-05-28 after
    ``claude plugin details <shared-namespace>`` collapsed to a single first-
    installed-wins view of components. See
    ``docs/research/multi-instance-claude-only-2026-05-27/PLAN.md`` for the
    revert rationale.
    """
    return {
        "name": plugin_dir.name,
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
        "description": _marketplace_description(),
        "plugins": entries,
    }
    MARKETPLACE_JSON.parent.mkdir(parents=True, exist_ok=True)
    MARKETPLACE_JSON.write_text(_to_json(manifest), encoding="utf-8", newline="")


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


def _write_inventory(entries: list[dict]) -> None:
    """Emit docs/INVENTORY.md — the authoritative, generated plugin list (FR-12).

    Added to the drift snapshot (see ``_check_drift``) so docs never hardcode
    counts: a stale count then fails ``--check`` exactly like a stale manifest.
    Reuses the in-memory marketplace entries; deterministic (sorted by category
    then name).
    """
    from collections import Counter

    cats = Counter(e["category"] for e in entries)
    lines = [
        "# Marketplace inventory",
        "",
        "_Generated by `scripts/generate_manifest.py` — do not edit by hand. This "
        "is the authoritative plugin list; reference it instead of hardcoding counts "
        "in prose (README, CONTRIBUTING, HANDOFF)._",
        "",
        f"**{len(entries)} plugin entries**: "
        + ", ".join(f"{count} {cat}" for cat, count in sorted(cats.items())),
        "",
    ]
    for cat in sorted(cats):
        lines.append(f"## {cat} ({cats[cat]})")
        for x in sorted(
            (x for x in entries if x["category"] == cat), key=lambda x: x["name"]
        ):
            lines.append(f"- `{x['name']}` — {x['description']}")
        lines.append("")
    (REPO_ROOT / "docs" / "INVENTORY.md").write_text(
        "\n".join(lines), encoding="utf-8", newline=""
    )


def main() -> None:
    marketplace_entries: list[dict] = []

    # Track (plugin_dir, construct, name) tuples for Phase 1.5
    individual_plugins: list[tuple[Path, object, str]] = []

    # Constructs that emit a Claude plugin (== entry in
    # ``.claude-plugin/marketplace.json``). RuleConstruct is intentionally
    # absent per F8: rules are a Claude memory feature, not a plugin
    # component. See ClaudeCodePlatform.supports docstring in platforms.py
    # and docs/research/claude-qa-2026-05-26/RESEARCH.md F8.
    claude_supports = ClaudeCodePlatform.supports

    # Clear and recreate _generated/ (clean slate each run)
    if GENERATED.exists():
        shutil.rmtree(GENERATED)
    GENERATED.mkdir()

    # ── Phase 1: Individual construct plugins ──────────────────────────────────
    # ``construct.emit`` always runs so per-platform manifests (Cursor /
    # Codex) emitted in Phase 1.5 still have a directory to populate. The
    # Claude marketplace entry is only added when the construct is in
    # ClaudeCodePlatform.supports.
    for construct in CONSTRUCTS.values():
        is_claude_plugin = type(construct) in claude_supports
        for name in scan_source_dir(construct.source_directory):
            plugin_dir = GENERATED / f"{construct.prefix}-{name}"
            plugin_dir.mkdir(parents=True, exist_ok=True)
            construct.emit(name, plugin_dir)
            if is_claude_plugin:
                plugin_json = construct.build_plugin_json(name)
                marketplace_entries.append(
                    _make_marketplace_entry(plugin_json, plugin_dir, construct.category)
                )
            individual_plugins.append((plugin_dir, construct, name))

    # ── Phase 1.5: Per-platform per-plugin manifests (Decision B2) ────────────
    # For each (plugin × platform) pair where type(construct) in platform.supports,
    # write _generated/<plugin>/.<platform>-plugin/plugin.json. Platforms that
    # return {} from build_plugin_json (e.g. AgentsPlatform, GeminiPlatform) are
    # skipped. ClaudeCodePlatform is also skipped here because the Claude manifest
    # is already written by Phase 1 (via construct.emit → write_plugin_json).
    for plugin_dir, construct, name in individual_plugins:
        construct_type = type(construct)
        for platform in PLATFORMS.values():
            if platform.name == "claude-code":
                # Already emitted by Phase 1; skip to avoid overwriting.
                continue
            if construct_type not in platform.supports:
                continue
            manifest = platform.build_plugin_json(construct, name)
            if not manifest:
                # Platforms that don't host plugin manifests return {}; skip.
                continue
            target = plugin_dir / f".{platform.name}-plugin" / "plugin.json"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(
                json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline=""
            )

    # ── Phase 2a: User-declared catalog bundles ────────────────────────────────
    # F8: filter rule-* out of every bundle's dependencies — those plugins
    # no longer exist in the Claude marketplace, so a bundle install would
    # fail at the dependency resolution step. Catalog bundles whose entire
    # membership was rule-* (bundle.quality-rules, bundle.workflow-rules,
    # bundle.documentation-rules, bundle.environment-rules,
    # bundle.notifications-rules) become empty post-filter and are dropped.
    # Mixed bundles (bundle.examples) shed only their rule member.
    # Cursor / Codex consumers still see the full rule set via the
    # _generated/rule-<name>/ dirs + per-platform manifests in Phase 1.5.
    bundles = load_bundles(CATALOG, CONSTRUCTS)
    for bundle in bundles:
        raw_deps = bundle.resolve_dependencies(CONSTRUCTS)
        deps = [d for d in raw_deps if not d.startswith("rule-")]
        if not deps:
            # Bundle was entirely rule-*; nothing left for Claude.
            continue
        description = bundle.description or _auto_description(deps)
        marketplace_entries.append(
            _emit_bundle_plugin(bundle.name, description, deps)
        )

    # ── Phase 2b: Code-generated catch-all bundles — RETIRED 2026-05-27 ────────
    # Previously emitted bundle-<prefix>-all per Claude-supported construct.
    # Removed because they cluttered the marketplace listing with one bundle per
    # construct that provided no curation value over the per-construct emission
    # already done in Phase 1. The cross-construct `bundle-examples` (from
    # catalog.toml) remains as the one curated multi-member bundle.

    # ── Phase 3: Cross-platform mirrors ───────────────────────────────────────
    # Wipe all mirror roots first for a clean slate. Platforms whose
    # ``mirror_directory`` is None (DevinPlatform after D-1; ClaudeCodePlatform)
    # are filtered both here and below. CodexPlatform still has a mirror_directory
    # because Unit 4 emits .codex/agents/<n>.toml; only its skill mirror was
    # retired (D-1) — the emit method short-circuits non-Agent construct types.
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

    # ── Phase 4.5: Root-level gemini-extension.json (Issue 3 fix) ─────────────
    # gemini extensions install <github-url> clones the repo and looks for
    # gemini-extension.json at the repo root (not in .gemini/). Copy the
    # already-generated manifest to root so both install paths work.
    shutil.copy2(
        REPO_ROOT / ".gemini" / "gemini-extension.json",
        REPO_ROOT / "gemini-extension.json",
    )

    # ── Phase 5: Top-level marketplace.json (from in-memory entries) ──────────
    _write_marketplace_json(marketplace_entries)

    # ── Phase 5.5: Codex canonical marketplace at .agents/plugins/ (D-14) ─────
    # developers.openai.com/codex/plugins/build (2026-05-25) documents this as
    # the canonical path. .claude-plugin/marketplace.json remains the legacy-
    # compat path (Codex still reads it as a fallback). Both files are
    # byte-identical; this is a copy, not a re-emit.
    agents_plugins_dir = REPO_ROOT / ".agents" / "plugins"
    agents_plugins_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(MARKETPLACE_JSON, agents_plugins_dir / "marketplace.json")

    # ── Phase 6: Root-level .cursor-plugin/marketplace.json (Issue 5 fix) ─────
    # Cursor team-marketplace import (Dashboard → Settings → Plugins → Import)
    # expects .cursor-plugin/marketplace.json at repo root listing all plugins.
    # Schema per cursor.com/docs/plugins: {name, plugins: [{name, source}]}.
    cursor_platform = next(p for p in PLATFORMS.values() if isinstance(p, CursorPlatform))
    cursor_plugin_entries = []
    for plugin_dir, construct, name in individual_plugins:
        if type(construct) in cursor_platform.supports:
            full_name = f"{construct.prefix}-{name}"
            cursor_plugin_entries.append({
                "name": full_name,
                "source": f"./{plugin_dir.relative_to(REPO_ROOT).as_posix()}",
            })
    cursor_plugin_entries.sort(key=lambda e: e["name"])
    cursor_marketplace = {
        "name": _marketplace_name(),
        "description": _marketplace_description(),
        "plugins": cursor_plugin_entries,
    }
    cursor_plugin_dir = REPO_ROOT / ".cursor-plugin"
    cursor_plugin_dir.mkdir(parents=True, exist_ok=True)
    (cursor_plugin_dir / "marketplace.json").write_text(
        _to_json(cursor_marketplace), encoding="utf-8", newline=""
    )

    # ── Phase 7: docs/INVENTORY.md (drift-checked single source of truth, FR-12) ─
    _write_inventory(marketplace_entries)

    # Summary
    from collections import Counter
    cats = Counter(e["category"] for e in marketplace_entries)
    print(f"Generated {len(marketplace_entries)} plugin entries in marketplace.json")
    for cat, count in sorted(cats.items()):
        print(f"  {cat}: {count}")
    print(f"  per-platform manifests emitted for {len(individual_plugins)} individual plugins")


def _check_drift() -> int:
    """Snapshot current outputs, regenerate, diff. Return 0 if identical, 1 if drift."""

    def snapshot_tree(roots: list[Path]) -> dict[str, bytes]:
        out: dict[str, bytes] = {}
        for root in roots:
            if not root.exists():
                continue
            if root.is_file():
                # Individual file targets (gemini-extension.json, docs/INVENTORY.md).
                # rglob("*") yields nothing for a file, so these must be read directly.
                out[str(root.relative_to(REPO_ROOT))] = root.read_bytes()
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
    # Also snapshot root-level generated files
    root_generated = [
        REPO_ROOT / "gemini-extension.json",
        REPO_ROOT / ".cursor-plugin",
        REPO_ROOT / ".agents" / "plugins",  # Phase 5.5 (D-14)
        REPO_ROOT / "docs" / "INVENTORY.md",  # Phase 7 (FR-12)
    ]
    targets = [GENERATED, MARKETPLACE_JSON.parent] + mirror_dirs + root_generated

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
