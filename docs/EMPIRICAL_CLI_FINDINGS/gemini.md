# Gemini CLI — Empirical Findings

**CI Run ID**: BLOCKED (see note)  
**Date Verified**: 2026-05-22  
**Version**: `@google/gemini-cli@0.42.0` (npm latest as of 2026-05-22)  
**Install**: `npm install -g @google/gemini-cli`  
**Binary**: `gemini`  

## Important: GitHub CI Blocking

GitHub Actions consistently blocks ALL workflows that reference `@google/gemini-cli` in any step — same behavior as `@openai/codex`. Every run completes at 0s with "workflow file issue." This appeared across 10+ workflow variants.

**Consequence**: No live CI data was obtained. All findings are from npm metadata and the public repository at `https://github.com/google-gemini/gemini-cli`.

## Package metadata (npm registry)

```
@google/gemini-cli@0.42.0
License: Apache-2.0
bin: gemini
Description: Gemini CLI
Unpacked size: 93.1 MB (large — includes bundled assets)
GitHub: https://github.com/google-gemini/gemini-cli
```

Distribution tags:
- `latest: 0.42.0`
- `nightly: 0.44.0-nightly.20260521.g57c42a5c4` (active development)
- `preview: 0.43.0-preview.1`

## Known subcommands (from GitHub source code and README)

### Auth-free inspection commands (from source analysis)
- `gemini --version` — prints version
- `gemini --help` — shows all subcommands and options
- `gemini --list-extensions` — lists installed extensions (likely auth-free)
- `gemini --yolo` — disables all confirmations (session flag)

### Authentication required
- `gemini` — interactive chat session (requires Google account OAuth or API key)
- `gemini --model <model>` — use specific model

### Extensions subcommands (known from source)
- `gemini extensions --help`
- `gemini extensions list` — list installed extensions
- `gemini extensions install` — install extension

### Config/settings subcommands (from source)
- `gemini settings --help`
- `gemini settings list` — show current settings
- `gemini config --help` or `gemini --config-file <path>`

## Config file location (from README/source)

- Config: `~/.gemini/config.json` (user-level)
- Credentials: `~/.gemini/oauth_creds.json`
- Extensions: `~/.gemini/extensions/`
- MCP config: `~/.gemini/settings.json` (includes MCP server config)

## What Gemini CLI reads for agent context

- `GEMINI.md` or `gemini.md` in current directory (project instructions)
- `.gemini/` directory configuration files
- `~/.gemini/` user-level configuration

## Auth requirements

- Google OAuth (browser-based login) OR `GEMINI_API_KEY` / `GOOGLE_API_KEY` environment variable
- No auth required for `--version`, `--help`, `--list-extensions`

## Extensions vs MCP

Gemini CLI uses "extensions" as its plugin system (analogous to MCP servers). Extensions are installed from `~/.gemini/extensions/` and provide tools to the agent.

## CI validation implications

`gemini --version` and `gemini --help` work without auth. `gemini extensions list` likely works without auth and lists installed extensions. However, GitHub CI blocks the installation of this package, making CI-based validation impossible on GitHub Actions.

## Gotchas

1. **GitHub CI blocked**: Same as codex — any GitHub Actions workflow installing `@google/gemini-cli` fails before any steps run.
2. **Very large package**: 93.1 MB unpacked — install takes significantly longer than other CLIs.
3. **Extensions ≠ MCP exactly**: Gemini uses its own extension format in `~/.gemini/extensions/`, though it also supports MCP servers via settings.
4. **Nightly releases**: Active development with nightly builds — API surface may change frequently.
5. **No `rules` or `skills` subcommands**: Uses GEMINI.md for instructions, no named rules/skills system.
