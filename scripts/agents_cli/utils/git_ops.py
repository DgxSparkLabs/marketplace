"""Git operations — shallow clone + ref resolution.

D-4: content source is ``git clone`` from the marketplace repo URL. Default
upstream is ``https://github.com/DgxSparkLabs/marketplace``; override via
``AGENTS_MARKETPLACE_URL`` env var. Cached at ``~/.cache/agents/marketplace/``.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

from .paths import cache_dir

DEFAULT_MARKETPLACE_URL = "https://github.com/DgxSparkLabs/marketplace"


def marketplace_url() -> str:
    """Public default; override via AGENTS_MARKETPLACE_URL."""
    return os.environ.get("AGENTS_MARKETPLACE_URL", DEFAULT_MARKETPLACE_URL)


def ensure_clone(ref: str = "main", *, force_refresh: bool = False) -> Path:
    """Ensure the marketplace is cloned locally; return the clone path.

    Uses a single cached clone at ``~/.cache/agents/marketplace/``. If the
    cache exists and force_refresh is False, fetches the latest for ``ref``.
    Otherwise re-clones.

    Raises ``subprocess.CalledProcessError`` if git fails.
    """
    target = cache_dir() / "marketplace"
    target.parent.mkdir(parents=True, exist_ok=True)

    if target.exists() and not force_refresh:
        # Fast path: update existing clone.
        try:
            subprocess.run(
                ["git", "-C", str(target), "fetch", "--depth", "1", "origin", ref],
                check=True, capture_output=True,
            )
            subprocess.run(
                ["git", "-C", str(target), "checkout", "FETCH_HEAD"],
                check=True, capture_output=True,
            )
            return target
        except subprocess.CalledProcessError:
            # Fall through to fresh clone if the cache is corrupted.
            shutil.rmtree(target, ignore_errors=True)

    if target.exists():
        shutil.rmtree(target, ignore_errors=True)

    subprocess.run(
        [
            "git", "clone", "--depth", "1", "--branch", ref,
            marketplace_url(), str(target),
        ],
        check=True, capture_output=True,
    )
    return target


def use_local_checkout(path: Path) -> Path:
    """Bypass clone — use a local marketplace checkout (tests + dev).

    The path is returned unmodified after a sanity check that it contains
    a ``_generated/`` directory or a recognisable construct source dir.
    """
    path = path.resolve()
    if not (path / "scripts" / "agents_cli").exists() and not (path / "_generated").exists():
        raise ValueError(
            f"{path} does not look like a marketplace checkout "
            "(no scripts/agents_cli/ and no _generated/)"
        )
    return path
