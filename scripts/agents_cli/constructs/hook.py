"""hook install — copy hooks.json to .agents/hooks/<name>.json + per-platform paths.

Hook merge semantics are deferred (risk register #4): with a single hook
plugin today, a straight copy / last-writer-wins is acceptable. When a
second hook plugin lands, replace these straight copies with a merge that
concatenates the platform's existing ``hooks`` arrays.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from ..utils.paths import resolve_hook


def install(marketplace_root: Path, name: str, *, scope: str, agents_only: bool) -> list[Path]:
    src = marketplace_root / "hooks" / name / "hooks" / "hooks.json"
    if not src.exists():
        raise FileNotFoundError(f"hook-{name} not found at {src}")

    targets = resolve_hook(name, scope, agents_only)
    written: list[Path] = []
    for dest in [targets.agents_path, *targets.platform_paths]:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(src, dest)
        written.append(dest)
    return written


def uninstall(name: str, *, scope: str, agents_only: bool) -> list[Path]:
    targets = resolve_hook(name, scope, agents_only)
    removed: list[Path] = []
    # Only remove the .agents/ canonical artifact; per-platform hook files may
    # be shared with other plugins, so removing them on uninstall would break
    # other installs. Conservative default for v1.
    if targets.agents_path.exists():
        targets.agents_path.unlink()
        removed.append(targets.agents_path)
    return removed
