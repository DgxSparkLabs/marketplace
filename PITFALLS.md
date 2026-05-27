---
status: live
purpose: knowledge-base-of-bugs-and-fixes
---

# Pitfalls

Knowledge base of bugs that occurred in this project and how they were fixed. Per `AGENTS.md`, after fixing any bug worth remembering, add an entry here so the next agent can avoid the same trap.

Pre-1.0 entries (Textual TUI installer era — installer crashes, banner glyphs, secret-leak skill setup, dangling-symlink bootstrap) are preserved at [`docs/archive/pre-1.0-pitfalls.md`](docs/archive/pre-1.0-pitfalls.md). They reference code paths that no longer exist after the v1.0.0 plugin-compliance migration and Phase 4 DI refactor.

## Format

Each entry uses this template:

```markdown
## <Short symptom title>

- **Symptom:** What you observed (the visible failure mode).
- **Cause:** Root cause — the actual reason it broke.
- **Fix:** What resolved it.
- **Commit:** `<short-sha>` (optional but preferred).
```

Keep entries 2-4 lines per field. Link to the commit so the next agent can read the diff. If a pitfall is structural (would have been caught by a test or hook), add the guardrail too and note it in the entry.

## Entries

## Dev container: Flask missing for hermetic stub

- **Symptom:** `python3 tests/fixtures/claude-stub/stub.py` errors `ModuleNotFoundError: No module named 'flask'` even after `apt-get install python3-flask` ran in `post-create.sh`.
- **Cause:** The python feature provides its own Python interpreter at `/usr/local/bin/python3` (Python 3.12). `apt-get install python3-flask` installs Flask for the system Python in `/usr/bin/python3`, not the feature's Python. They're different interpreters with separate site-packages.
- **Fix:** Stub files now carry PEP 723 inline metadata declaring `dependencies = ["flask>=3.0"]`. Invoke with `uv run tests/fixtures/claude-stub/stub.py` — uv creates an ephemeral env with Flask pinned to the script's requirement. Matches AGENTS.md "always use uv" rule and eliminates the apt-vs-feature interpreter mismatch class entirely.
- **Detect:** If a Python script bombs on `ModuleNotFoundError` after an apt install "succeeded", the apt package is for a different interpreter. Run `which python3` and `python3 -c 'import sys; print(sys.path)'` to confirm. Better: add PEP 723 to any script with non-stdlib deps and use `uv run`.

## Dev container: EACCES on /home/vscode/.claude/plugins

- **Symptom:** `claude plugin marketplace add /workspaces/marketplace/` fails with `EACCES: permission denied, mkdir '/home/vscode/.claude/plugins'`.
- **Cause:** The named docker volume `claude-code-config-${devcontainerId}` is mounted root-owned by default. The `remoteUser: vscode` can't mkdir inside the mount because the mount happens BEFORE the user-level setup runs. The Anthropic feature installs `claude` correctly but doesn't chown the mount.
- **Fix:** `post-create.sh` now runs `sudo chown -R $(id -u):$(id -g) "$HOME/.claude"` before anything else, and pre-creates `$HOME/.claude/plugins`. Same pattern as the Anthropic reference container.
- **Detect:** Any "EACCES mkdir" inside a path that maps to a named volume mount → the volume is root-owned. Either chown in `postCreateCommand` (runs as remoteUser with sudo) or `onCreateCommand` (runs as root by default).
