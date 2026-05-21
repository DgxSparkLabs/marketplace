# Construct Types

A Claude Code plugin can ship ten distinct **construct types**. This marketplace ships individual plugins, domain bundles, and reference examples for every one. Pick the row that matches what you're building, then read the linked ADDING guide.

## The ten construct types

| Construct | What it is | Source dir | Example | Tutorial |
|-----------|-----------|------------|---------|----------|
| **Skill** | On-demand domain expertise. Invoked by user (`/skill-name`) or auto-invoked by Claude when the description matches. | `skills/<name>/` | `examples/example-skill/` | [ADDING_A_SKILL.md](./ADDING_A_SKILL.md) |
| **Rule** | Always-on behavioral guideline injected into every session via `.claude/rules/`. Requires a manual `activate.sh` symlink step after install. | `rules/<name>/` | `examples/example-rule/` | [ADDING_A_RULE.md](./ADDING_A_RULE.md) |
| **Command** | A custom slash command. Lighter-weight than a skill — single markdown file, user-invoked only. | `commands/<name>.md` (within a plugin) | `examples/example-command/` | [ADDING_A_COMMAND.md](./ADDING_A_COMMAND.md) |
| **Agent** | A sub-agent persona with its own system prompt and scoped tool access. | `agents/<name>.md` (within a plugin) | `examples/example-agent/` | [ADDING_AN_AGENT.md](./ADDING_AN_AGENT.md) |
| **Hook** | Event-triggered script (`UserPromptSubmit`, `PreToolUse`, `SessionStart`, `Stop`, etc.). | `hooks/hooks.json` (within a plugin) | `examples/example-hook/` | [ADDING_A_HOOK.md](./ADDING_A_HOOK.md) |
| **MCP server** | A Model Context Protocol server. Exposes tools, resources, and prompts to Claude. | `mcp-config.json` (within a plugin, `mcpServers` field) | `examples/example-mcp/` | [ADDING_AN_MCP_SERVER.md](./ADDING_AN_MCP_SERVER.md) |
| **LSP server** | A Language Server Protocol server. Gives Claude type info, definitions, and diagnostics for a language. | `lsp-config.json` (within a plugin, `lspServers` field) | `examples/example-lsp/` | [ADDING_AN_LSP_SERVER.md](./ADDING_AN_LSP_SERVER.md) |
| **Monitor** | Background process that runs on an interval and surfaces output to Claude on demand. | `monitors/monitors.json` (within a plugin, `experimental.monitors`) | `examples/example-monitor/` | [ADDING_A_MONITOR.md](./ADDING_A_MONITOR.md) |
| **Output style** | System-prompt modification — adjusts Claude's voice, format, or behavior. Can be user-selectable or auto-applied (`force-for-plugin: true`). | `output-styles/<name>.md` (within a plugin) | `examples/example-output-style/` | [ADDING_AN_OUTPUT_STYLE.md](./ADDING_AN_OUTPUT_STYLE.md) |
| **Theme** | UI color theme (experimental). | `themes/<name>.json` (within a plugin, `experimental.themes`) | `examples/example-theme/` | [ADDING_A_THEME.md](./ADDING_A_THEME.md) |

Plus a meta-construct:

| Construct | What it is | Defined in | Tutorial |
|-----------|-----------|------------|----------|
| **Domain bundle** | A plugin whose only job is to declare dependencies on other plugins, so users can install a logical group with one command. | `catalog.toml` `[skill_domain.*]` and `[rule_domain.*]` tagging | [ADDING_A_DOMAIN_BUNDLE.md](./ADDING_A_DOMAIN_BUNDLE.md) |

## Naming convention

Every plugin in this marketplace follows a strict prefix convention so the plugin name alone identifies what it is:

| Type | Individual | Domain bundle |
|------|-----------|---------------|
| skill | `skill-<name>` | `skills-<domain>` |
| rule | `rule-<name>` | `rules-<domain>` |
| command | `command-<name>` | `commands-<domain>` |
| agent | `agent-<name>` | `agents-<domain>` |
| hook | `hook-<name>` | `hooks-<domain>` |
| mcp server | `mcp-<name>` | `mcps-<domain>` |
| lsp server | `lsp-<name>` | `lsps-<domain>` |
| monitor | `monitor-<name>` | `monitors-<domain>` |
| output style | `output-style-<name>` | `output-styles-<domain>` |
| theme | `theme-<name>` | `themes-<domain>` |

Plus `example-<type>` for the reference templates in `examples/`.

## Install paths

Native `/plugin install` works for nine of the ten construct types. **Rules need a manual `activate.sh` step** because Claude Code's plugin system does not yet support installing rules natively (see [`INVESTIGATION_PLUGIN_DEPENDENCIES.md`](./INVESTIGATION_PLUGIN_DEPENDENCIES.md) for the full context).

```bash
# Pure plugin install (skill, command, agent, hook, mcp, lsp, monitor, output style, theme)
/plugin marketplace add DgxSparkLabs/marketplace
/plugin install skill-telegram-notify@dgxsparklabs-marketplace      # individual
/plugin install skills-communication@dgxsparklabs-marketplace       # bundle

# Rule install + activate (rules only)
/plugin install rule-blast-radius@dgxsparklabs-marketplace
bash ~/.claude/plugins/cache/dgxsparklabs-marketplace/rule-blast-radius/activate.sh

# Bulk rule activation (any number of rule plugins installed)
bash ~/.local/share/marketplace/activate-installed-rules.sh
```

## Architecture notes

- **Source of truth**: `skills/<name>/` and `rules/<name>/` are hand-edited content. `examples/<name>/` are hand-edited reference plugins.
- **Generated output**: `_generated/skill-<name>/`, `_generated/rule-<name>/`, `_generated/skills-<domain>/`, `_generated/rules-<domain>/` are produced by `uv run scripts/generate_manifest.py` from sources + `catalog.toml` tagging. Never edit `_generated/` files by hand.
- **Cross-platform mirrors**: `.codex/`, `.gemini/`, `.cursor/`, `.windsurf/`, `.devin/` are auto-generated for users on non-Claude-Code tools.
- **Single source for identity**: `MARKETPLACE.toml` declares owner, repo URL, version, license. All generated plugin.json files inherit from this.

## Adding new constructs

For each construct type, the workflow is:

1. Copy the matching `examples/example-<type>/` directory to a new location.
2. Edit the plugin manifest (`.claude-plugin/plugin.json`) and the construct content.
3. (Skills and rules only) Add the new entry to `catalog.toml` under the appropriate `[skill_domain.*]` or `[rule_domain.*]` so it lands in a bundle.
4. Run `uv run scripts/generate_manifest.py` to regenerate manifests and mirrors.
5. Run `uv run tests/test_marketplace.py` to validate.
6. Commit.

Each `ADDING_*.md` document walks through this for its specific construct type.
