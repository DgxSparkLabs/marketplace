"""command install — copy commands/<name>/commands/*.md to .agents/commands/ + .cursor/commands/."""

from __future__ import annotations

import shutil
from pathlib import Path

from ..utils.paths import resolve_command


def install(marketplace_root: Path, name: str, *, scope: str, agents_only: bool) -> list[Path]:
    src_dir = marketplace_root / "src" / "commands" / name / "commands"
    if not src_dir.exists():
        raise FileNotFoundError(f"command-{name} not found at {src_dir}")
    src_files = sorted(src_dir.glob("*.md"))
    if not src_files:
        raise FileNotFoundError(f"No command .md files in {src_dir}")

    targets = resolve_command(name, scope, agents_only)
    written: list[Path] = []
    for dest_template in [targets.agents_path, *targets.platform_paths]:
        for src in src_files:
            dest = dest_template.with_name(f"{src.stem}.md")
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(src, dest)
            written.append(dest)
    return written


def uninstall(name: str, *, scope: str, agents_only: bool) -> list[Path]:
    targets = resolve_command(name, scope, agents_only)
    removed: list[Path] = []
    for dest in [targets.agents_path, *targets.platform_paths]:
        if dest.exists():
            dest.unlink()
            removed.append(dest)
    return removed
