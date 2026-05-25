"""skill install — copy ``skills/<name>/`` to ``.agents/skills/<name>/``."""

from __future__ import annotations

import shutil
from pathlib import Path

from ..utils.paths import resolve_skill


def install(marketplace_root: Path, name: str, *, scope: str, agents_only: bool) -> list[Path]:
    """Install ``skill-<name>`` from the cloned marketplace at ``marketplace_root``.

    Returns the list of paths written.
    """
    src = marketplace_root / "skills" / name
    if not src.exists():
        raise FileNotFoundError(f"skill-{name} not found at {src}")

    targets = resolve_skill(name, scope, agents_only)
    written: list[Path] = []
    for dest in [targets.agents_path, *targets.platform_paths]:
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists():
            shutil.rmtree(dest, ignore_errors=True)
        shutil.copytree(src, dest, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        written.append(dest)
    return written


def uninstall(name: str, *, scope: str, agents_only: bool) -> list[Path]:
    targets = resolve_skill(name, scope, agents_only)
    removed: list[Path] = []
    for dest in [targets.agents_path, *targets.platform_paths]:
        if dest.exists():
            shutil.rmtree(dest, ignore_errors=True)
            removed.append(dest)
    return removed
