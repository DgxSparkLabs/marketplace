#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""tasks.py — one-verb task runner for the common workflows (NFR-8).

Usage:
    uv run scripts/tasks.py <task>

Tasks:
    regen    regenerate manifests / mirrors / docs/INVENTORY.md from src/
    check    drift-check only (no writes; exit 1 on drift)
    test     run all three test suites
    verify   check + test + `claude plugin validate ./`
             (the validate step is skipped with a warning if the `claude`
             CLI is not on PATH, so `verify` is usable on any dev box)
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # repo root (this file lives in scripts/)

SUITES = ("test_marketplace", "test_schema_fitness", "test_agents_cli", "test_tooling")


def run(cmd: list[str]) -> int:
    print(f"\n$ {' '.join(cmd)}", flush=True)
    return subprocess.call(cmd, cwd=ROOT)


def regen() -> int:
    return run(["uv", "run", "scripts/generate_manifest.py"])


def check() -> int:
    return run(["uv", "run", "scripts/generate_manifest.py", "--check"])


def test() -> int:
    rc = 0
    for suite in SUITES:
        rc |= run(["uv", "run", f"tests/{suite}.py"])
    return rc


def verify() -> int:
    rc = check()
    rc |= test()
    if shutil.which("claude"):
        rc |= run(["claude", "plugin", "validate", "./"])
    else:
        print(
            "\n[verify] WARNING: 'claude' CLI not on PATH — "
            "skipping `claude plugin validate ./` (run it in CI / a Claude env)."
        )
    print("\n" + ("VERIFY OK" if rc == 0 else "VERIFY FAILED"))
    return rc


TASKS = {"regen": regen, "check": check, "test": test, "verify": verify}


def main(argv: list[str]) -> int:
    if len(argv) != 1 or argv[0] not in TASKS:
        print(f"usage: uv run scripts/tasks.py <{'|'.join(TASKS)}>", file=sys.stderr)
        return 2
    return TASKS[argv[0]]()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
