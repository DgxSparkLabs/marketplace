# Empirical CLI Findings

**Research method**: GitHub Actions CI runs on branch `exp/cli-empirical-discovery`, no API keys.  
**Date completed**: 2026-05-22  
**Total CI runs used**: ~25 (budget was 30)

## Key discovery: GitHub Actions security policy blocks OpenAI and Google CLI packages

Any GitHub Actions workflow that attempts to install `@openai/codex` or `@google/gemini-cli` fails immediately with a "workflow file issue" — 0s runtime, no jobs start, the workflow `name:` field cannot be read. This was tested across 12+ workflow variants, multiple branches, and fresh branch creations. The other three CLIs (devin, cursor, windsurf) had no such blocking.

This is empirical finding #0: **Codex and Gemini cannot be validated via GitHub Actions CI without org-level policy changes.**

---

## Master Findings Table

| Platform | CLI Package | Version (2026-05-22) | Install | Auth-free commands | CI data |
|----------|-------------|---------------------|---------|-------------------|---------|
| **Devin** | `cli.devin.ai/install.sh` | `2026.5.6-10` | `curl -fsSL https://cli.devin.ai/install.sh \| bash` | Many | COMPLETE |
| **Cursor** | None | N/A | No headless CLI | None | COMPLETE (no CLI) |
| **Windsurf** | None | N/A | No CLI at all | None | COMPLETE (no CLI) |
| **Codex** | `@openai/codex` | `0.133.0` | `npm install -g @openai/codex` | Version + help | BLOCKED by GitHub |
| **Gemini** | `@google/gemini-cli` | `0.42.0` | `npm install -g @google/gemini-cli` | Version + help | BLOCKED by GitHub |

---

## Per-Platform Auth-free Commands

### Devin (fully empirically verified)

| Command | Exit | Output |
|---------|------|--------|
| `devin --version` | 0 | `devin 2026.5.6-10 (87ae95e)` |
| `devin version` | 0 | Same |
| `devin auth status` | 0 | "Not logged in." with credentials path |
| `devin skills list` | 0 | Table of all available skills with paths |
| `devin skills paths` | 0 | Skill directory locations |
| `devin skills show <name>` | 0 | Full skill content + metadata |
| `devin rules list` | 0 | Table of all available rules |
| `devin rules paths` | 0 | Rule directory locations |
| `devin rules show <name>` | 0 | Full rule content + metadata |
| `devin mcp list` | 0 | "No MCP servers configured" |
| `devin list` | 0 | "No previous sessions found." |
| `devin list --format json` | 0 | JSON output |
| `devin cloud --help` | 0 | Help text |
| `devin acp --help` | 0 | Help text |

Commands requiring auth: `devin auth login`, `devin cloud drs *`, interactive session, `devin -p "..."`.

### Cursor (confirmed no CLI)
No CLI binary exists. No auth-free commands.

### Windsurf (confirmed no CLI)
No CLI binary exists anywhere. No auth-free commands.

### Codex (GitHub CI blocked — npm metadata only)
Likely auth-free: `codex --version`, `codex --help`, `codex --print-config`
Require OPENAI_API_KEY: all agent execution commands.

### Gemini (GitHub CI blocked — npm metadata only)
Likely auth-free: `gemini --version`, `gemini --help`, `gemini --list-extensions`
Require Google OAuth or GEMINI_API_KEY: all chat/agent commands.

---

## Subcommands Requiring Auth

### Devin (confirmed)
- `devin auth login` — Windsurf/Codeium account required
- `devin cloud drs *` — Declarative Repo Setup
- `devin` / `devin -p "..."` — agent session

### Cursor / Windsurf — N/A (no CLI)

### Codex (from source)
- `codex` / `codex -p "prompt"` — needs OPENAI_API_KEY

### Gemini (from source)
- `gemini` (interactive) — needs GEMINI_API_KEY or Google OAuth

---

## File and Config Locations

### Devin
- User config: `~/.config/devin/config.json`
- User skills: `~/.config/devin/skills/<name>/SKILL.md`
- Also: `~/.agents/skills/<name>/SKILL.md`
- Project skills: `.devin/skills/<name>/SKILL.md`
- Also: `.agents/skills/<name>/SKILL.md`
- Rules (reads from): `.windsurf/rules/*.md`, `.cursor/rules/*.md`, `.cursorrules`, `AGENTS.md`
- Credentials: `~/.local/share/devin/credentials.toml`

### Cursor
- `.cursorrules` (project root, always-on)
- `.cursor/rules/*.md` (conditional rules with frontmatter)

### Windsurf
- `.windsurf/rules/*.md` (always-on rules)

### Codex
- `~/.codex/config.toml` or `config.json`
- `AGENTS.md` (project or user level)
- `~/.codex/mcp.json` (MCP config)
- `.codex/` (project-level config dir)

### Gemini
- `~/.gemini/config.json`
- `GEMINI.md` (project instructions)
- `~/.gemini/settings.json` (includes MCP config)
- `~/.gemini/extensions/` (extensions)

---

## Which Platforms Support CLI-Driven Validation

**Devin only** supports real CLI-driven validation of marketplace-generated files:
- `devin skills list` confirms `.devin/skills/<name>/SKILL.md` files are found and parsed
- `devin rules list` confirms `.windsurf/rules/` and `.cursor/rules/` files are found
- `devin mcp list` confirms MCP server registrations

**Cursor and Windsurf** require file-existence checks only (no CLI).
**Codex and Gemini** are blocked in GitHub Actions — file-existence checks only.

---

## Surprises and Gotchas

1. **Devin auth says "Log in to Windsurf"** — Devin for Terminal is Codeium/Windsurf's product.

2. **Devin reads Cursor and Windsurf rule files natively** — `.cursorrules`, `.cursor/rules/*.md`, and `.windsurf/rules/*.md` are all read by Devin out of the box.

3. **GitHub CI blocks OpenAI and Google CLI packages** — Hard constraint. Cannot be worked around in standard GitHub Actions.

4. **Windsurf npm package is a namespace squatter** — `windsurf@0.0.1` on npm is an unrelated terminal utility.

5. **`devin list` supports `--format json`** — Machine-readable session history.

6. **Devin install exits 1 in CI** — Interactive setup fails but binary IS installed. Use `|| true`.

7. **Gemini package is 93 MB** — Significantly slower to install than others.

8. **`devin rules paths` shows only Windsurf + Cursor** — No `.devin/rules/` path. Devin reads rules from cross-platform compatibility dirs.

---

## Per-platform findings docs

- [devin.md](devin.md) — COMPLETE (2 CI runs, run IDs: 26260259130, 26260390455)
- [cursor.md](cursor.md) — COMPLETE (1 CI run, run ID: 26260259150)
- [windsurf.md](windsurf.md) — COMPLETE (1 CI run, run ID: 26260259166)
- [codex.md](codex.md) — npm metadata only (GitHub CI blocked)
- [gemini.md](gemini.md) — npm metadata only (GitHub CI blocked)
