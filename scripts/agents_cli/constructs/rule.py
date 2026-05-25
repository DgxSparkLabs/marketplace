"""rule install — copy ``rules/<name>/rule.md`` (or platform format file) to targets."""

from __future__ import annotations

import shutil
from pathlib import Path

from ..utils.paths import resolve_rule


def _source_for(marketplace_root: Path, name: str, dest: Path) -> Path:
    """Pick the source file for a given destination.

    Prefers ``rules/<name>/formats/<platform>.md`` when the destination
    sits under that platform's directory; falls back to the raw ``rule.md``.
    """
    src_root = marketplace_root / "rules" / name
    parts = dest.parts
    # Platform detection from destination path.
    if ".cursor" in parts:
        fmt = src_root / "formats" / "cursor.md"
        if fmt.exists():
            return fmt
    elif ".windsurf" in parts:
        fmt = src_root / "formats" / "windsurf.md"
        if fmt.exists():
            return fmt
    return src_root / "rule.md"


def install(marketplace_root: Path, name: str, *, scope: str, agents_only: bool) -> list[Path]:
    src_root = marketplace_root / "rules" / name
    if not (src_root / "rule.md").exists():
        raise FileNotFoundError(f"rule-{name} not found at {src_root}/rule.md")

    targets = resolve_rule(name, scope, agents_only)
    written: list[Path] = []
    for dest in [targets.agents_path, *targets.platform_paths]:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(_source_for(marketplace_root, name, dest), dest)
        written.append(dest)
    return written


def uninstall(name: str, *, scope: str, agents_only: bool) -> list[Path]:
    targets = resolve_rule(name, scope, agents_only)
    removed: list[Path] = []
    for dest in [targets.agents_path, *targets.platform_paths]:
        if dest.exists():
            dest.unlink()
            removed.append(dest)
    return removed
