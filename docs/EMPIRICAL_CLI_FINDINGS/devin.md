# Devin CLI — Empirical Findings

**CI Run IDs**: 26260259130 (run 1), 26260390455 (run 2)  
**Date Verified**: 2026-05-22  
**Version**: `devin 2026.5.6-10 (87ae95e)`  
**Install**: `curl -fsSL https://cli.devin.ai/install.sh | bash`  
**Binary location**: `~/.local/bin/devin` (symlink to `~/.local/share/devin/cli/_versions/current/bin/devin`)  
**Install note**: Installer exits with code 1 but binary IS installed. The installer tries to run interactive setup ("Login canceled") which fails in CI — this is expected.  

## Auth behavior

`devin auth status` (no auth required) → outputs:
```
Not logged in.
  Credentials path: /home/runner/.local/share/devin/credentials.toml
Run `devin auth login` to authenticate.
```
Exit code: 0. Auth-free.

## Full subcommand tree (all auth-free to enumerate)

```
Usage: devin [OPTIONS] [-- <PROMPT>...] [COMMAND]

Commands:
  auth       Authentication related commands
  mcp        Connect and log in to Model Context Protocol servers
  rules      Manage agent rules (always-on context blobs)
  skills     Manage agent skills (slash commands and agent-triggered context blobs)
  cloud      Manage Devin Cloud resources (environment setup, sandbox sessions, builds)
  list       List sessions in the current directory [aliases: ls]
  update     Check for updates and optionally install them
  version    Print the current version
  sandbox    [Research Preview] Process sandboxing for the exec tool
  setup      Interactive setup wizard
  uninstall  Uninstall and remove data
  acp        Run as an ACP (Agent Client Protocol) server over stdio
  shell      [Feature preview] Integrate with your shell to instantly launch devin with relevant context
  help       Print this message or the help of the given subcommand(s)
```

### `devin auth` subcommands
```
Commands:
  login   Log in to Windsurf   ← NOTE: says "Windsurf" (Devin is built on Windsurf/Codeium)
  logout  Log out and remove stored credentials
  status  Check authentication status
```

### `devin skills` subcommands
```
Commands:
  list   List all available skills
  show   Show details for a specific skill
  paths  Show skill directory locations
```

### `devin rules` subcommands
```
Commands:
  list   List all available rules
  show   Show details for a specific rule
  paths  Show rule directory locations
```

### `devin mcp` subcommands
```
Commands:
  add      Add a new MCP server
  list     List all configured MCP servers
  get      Get details for a specific MCP server
  remove   Remove an MCP server
  login    Authenticate with an MCP server via OAuth
  logout   Remove stored OAuth credentials for an MCP server
  enable   Enable a disabled MCP server
  disable  Disable an MCP server without removing it
```

### `devin cloud` subcommands
```
Commands:
  drs   Manage Declarative Repo Setup (environment blueprints, sandbox sessions, and builds)
```

### `devin list` (sessions) format options
```
Options:
  --format <FORMAT>
    - interactive: Interactive session picker (default)
    - json:        JSON output
    - csv:         CSV output
```
Exit code 0 when no sessions. Output: `No previous sessions found.`

## Auth-free commands verified (exit 0, useful output)

| Command | Exit | Auth Required | Output |
|---------|------|---------------|--------|
| `devin --version` | 0 | No | `devin 2026.5.6-10 (87ae95e)` |
| `devin --help` | 0 | No | Full help text |
| `devin version` | 0 | No | Same as --version |
| `devin auth status` | 0 | No | "Not logged in." with credentials path |
| `devin skills --help` | 0 | No | Subcommand list |
| `devin skills list` | 0 | No | Lists all skills from project + user dirs |
| `devin skills paths` | 0 | No | Shows skill directory locations |
| `devin rules --help` | 0 | No | Subcommand list |
| `devin rules list` | 0 | No | Lists all rules from project dirs |
| `devin rules paths` | 0 | No | Shows rule directory locations |
| `devin mcp --help` | 0 | No | Subcommand list |
| `devin mcp list` | 0 | No | "No MCP servers configured" |
| `devin list --help` | 0 | No | Help with --format JSON/CSV options |
| `devin list` | 0 | No | "No previous sessions found." |
| `devin cloud --help` | 0 | No | Help text |
| `devin acp --help` | 0 | No | Help text |
| `devin update --help` | 0 | No | Help text |

## Commands requiring auth (not tested without Windsurf account)

- `devin auth login` — requires Windsurf Enterprise account
- `devin cloud drs *` — likely requires auth
- `devin` (plain, interactive) — starts session, requires auth
- `devin -p "prompt"` — non-interactive mode, requires API key or auth

## Skill file paths (confirmed by `devin skills paths`)

```
User skills (global):
  ~/.config/devin/skills/<skill-name>/SKILL.md
  ~/.agents/skills/<skill-name>/SKILL.md

Project skills:
  .devin/skills/<skill-name>/SKILL.md
  .agents/skills/<skill-name>/SKILL.md
```

## Rule file paths (confirmed by `devin rules paths`)

```
Windsurf rules:
  .windsurf/rules/*.md   (always-on)

Cursor rules:
  .cursorrules           (always-on)
  .cursor/rules/*.md     (conditional)
```
Note: Devin reads from BOTH `.windsurf/rules/` and `.cursor/rules/` for compatibility with those platforms. Devin-specific project rules live in `.devin/` implicitly.

## Config locations

- User config: `~/.config/devin/config.json` (content: `{"version": 1}` after fresh install)
- Credentials: `~/.local/share/devin/credentials.toml`
- Sessions DB: `~/.local/share/devin/sessions.db`
- Binary: `~/.local/bin/devin` → `~/.local/share/devin/cli/_versions/<version>/bin/devin`

## Output formats

- `devin skills list` — human-readable table, no JSON flag
- `devin rules list` — human-readable table  
- `devin mcp list` — human-readable, no JSON flag
- `devin list --format json` — JSON output for session listing
- `devin --help` grep for 'json': matches `--agent-config` (JSON or YAML file), no general JSON output flag

## Skills output sample (from project context)

`devin skills list` enumerated 25+ skills from the `.devin/skills/` directory:
```
/github-search [user,model] (./.devin/skills/github-search)
/check [user,model] (./.devin/skills/check)
...
devin-for-terminal [model] (~/.local/share/devin/cli/_versions/2026.5.6-10/share/devin)
```
Format: `/<slash-command> [triggers] (path) - description`

## Noteworthy

1. **Devin IS built on Windsurf**: `devin auth login` says "Log in to Windsurf" — Devin for Terminal is Windsurf/Codeium's product.
2. **`devin rules paths` reveals cross-platform awareness**: Devin CLI reads Windsurf (`.windsurf/rules/*.md`) and Cursor (`.cursorrules`, `.cursor/rules/*.md`) rule files natively.
3. **Session listing supports JSON/CSV**: `devin list --format json` gives machine-readable session history.
4. **Declarative agent config**: `--agent-config <FILE>` accepts JSON or YAML for system instructions and tool visibility — useful for CI validation.
5. **ACP server mode**: `devin acp` runs as an Agent Client Protocol server over stdio — programmatic integration point.
