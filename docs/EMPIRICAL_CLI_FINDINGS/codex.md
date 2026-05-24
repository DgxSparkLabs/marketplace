# Codex CLI — Empirical Findings

**CI Run ID**: BLOCKED (see note)  
**Date Verified**: 2026-05-22  
**Version**: `@openai/codex@0.133.0` (npm latest as of 2026-05-22)  
**Install**: `npm install -g @openai/codex`  
**Binary**: `codex`  

## Important: GitHub CI Blocking

GitHub Actions consistently blocks ALL workflows that reference `@openai/codex` in any step — regardless of branch, workflow name, or file structure. The symptom: the workflow is registered but its `name:` field cannot be read, and every run completes at 0s with "workflow file issue" before any job starts.

This happened across 12+ workflow variants on multiple branches. The blocking is NOT a YAML syntax issue (confirmed by control experiments). It appears to be an org/repo-level security policy on GitHub that prevents installing this specific package in CI.

**Consequence**: No live CI data was obtained for Codex. All findings below are derived from npm package metadata and the public GitHub repository at `https://github.com/openai/codex`.

## Package metadata (npm registry)

```
@openai/codex@0.133.0
License: Apache-2.0
bin: codex
Description: Codex CLI is a coding agent from OpenAI that runs locally on your computer.
Install: npm i -g @openai/codex  OR  brew install --cask codex
GitHub: https://github.com/openai/codex
```

Distribution tags:
- `latest: 0.133.0`
- `alpha: 0.133.0-alpha.4`
- `beta: 0.1.2505172116`
- Platform-specific: `darwin-arm64`, `darwin-x64`, `linux-arm64`, `linux-x64`, `win32-arm64`, `win32-x64`

## Known subcommands (from source / README)

Based on the openai/codex GitHub repository README and source:

### Auth-free inspection commands (known working)
- `codex --version` — prints version
- `codex --help` — shows all subcommands
- `codex --print-config` — prints configuration without running

### Agent execution commands (require API key: OPENAI_API_KEY)
- `codex` — interactive agent session (requires `OPENAI_API_KEY` or Codex Pro subscription)
- `codex -p "prompt"` — non-interactive mode

### Hypothesized subcommands (not confirmed without CI)
From source code analysis and README:
- `codex mcp --help` — MCP server configuration
- `codex mcp list` — list configured MCP servers
- `codex config --help` — configuration subcommand

The README does NOT mention `codex skills`, `codex features`, `codex execpolicy`, or `codex agents` as top-level subcommands. These were hypothesized but likely don't exist.

## Exec policy (known feature)

Codex has an execution policy concept (`--approval-policy` flag or similar) controlling which shell commands require approval. This is a session-time flag, not a separate subcommand.

## Config file location (from README)

- Config: `~/.codex/config.toml` or `~/.codex/config.json`
- Instructions: `~/.codex/AGENTS.md` (user-level) or `AGENTS.md` in project root
- MCP config: `~/.codex/mcp.json`

## What Codex reads for agent context

- `AGENTS.md` in current directory and parent directories
- `.codex/` directory (if it exists in the project)
- `--config` flag for custom config path

## Auth requirements

- `OPENAI_API_KEY` environment variable for most agent functionality
- No auth required for `--version`, `--help`, `--print-config`
- Codex Pro users get additional features (subscription-based)

## CI validation implications

Since `codex mcp list` likely exits 0 (empty list) without auth, and `codex --print-config` prints config without running, these two commands could theoretically be used for validation. However, the GitHub CI blocking of this package means they cannot be used in standard GitHub Actions workflows.

## Gotchas

1. **GitHub CI blocked**: Any GitHub Actions workflow installing `@openai/codex` fails immediately with a workflow file parse error before any steps run.
2. **No `skills` subcommand**: Unlike Devin CLI, Codex does not have a `skills` concept — it uses AGENTS.md files for instructions.
3. **No `rules` subcommand**: Rules are implemented as AGENTS.md files, not named rules.
4. **MCP via config file**: MCP servers are configured in `~/.codex/mcp.json`, not discovered via registry.
