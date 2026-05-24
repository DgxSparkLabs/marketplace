# Cursor Agent CLI — Empirical Findings

**CI Run ID**: 26260259150 (run 1)  
**Date Verified**: 2026-05-22  
**Result**: Install script exists but produces NO headless binary

## Summary

`https://cursor.com/install` returns a real Bash script titled "Cursor Agent Installer" but it installs the Cursor desktop application (GUI), not a headless CLI. No `cursor` or `agent` binary is available in PATH after install in a headless Linux environment.

## Evidence from CI

| Check | Result |
|-------|--------|
| `curl -fsSL https://cursor.com/install \| head -40` | Returns a real bash script: `#!/usr/bin/env bash` with title `"Cursor Agent Installer"` |
| `curl -fsSL https://cursor.com/install-agent` | 404 |
| `npm show cursor` | Found — unrelated terminal cursor package (MIT, deprecated) |
| `npm show @cursor-ai/cli` | 404 |
| `npm show @cursor/cli` | 404 |
| `npm show cursor-cli` | Found — unrelated terminal cursor utility (MIT, deprecated) |
| `cursor --version` after install | Exit 127 — command not found |
| `cursor --help` after install | Exit 127 — command not found |
| `agent --version` | Exit 127 — command not found |
| `agent --help` | Exit 127 — command not found |
| `agent mcp list` | Exit 127 — command not found |
| `agent status` | Exit 127 — command not found |
| `ls /opt/cursor` | No such file |
| `ls /usr/local/bin/cursor` | No such file |
| npm global packages | No cursor packages installed |

## The install script

`https://cursor.com/install` returns `#!/usr/bin/env bash` with:
- Title: "Cursor Agent Installer"
- Color support detection for non-TTY
- Fancy colored terminal output
- Does NOT produce a usable binary in headless CI environments

The script likely installs the Cursor GUI application (AppImage or Electron wrapper) which cannot run without a display server.

## Cursor AppImage availability

`curl -sI "https://downloader.cursor.sh/linux/appImage/x64"` — the CI run showed no output (likely a redirect or unavailable URL). Even if downloadable, the AppImage is the full GUI IDE.

## What IS available for Cursor (config, not CLI)

Cursor reads agent rules from:
- `.cursorrules` — project root, plain text (always-on rules)
- `.cursor/rules/*.md` — directory of conditional rules with YAML frontmatter
- (Confirmed by `devin rules paths` which documents Cursor rule paths)

There is NO programmatic Cursor CLI for listing or verifying rules.

## Auth-free commands: NONE (no CLI exists)

## Conclusion for marketplace validation

Cursor cannot be validated via CLI. Validation must be **file-existence and format checks**:
- Check `.cursorrules` or `.cursor/rules/<name>.mdc` exists
- Validate frontmatter `description`, `globs`, `alwaysApply` fields
- No CLI binary available to confirm which rules are "loaded"
