---
date: 2026-05-26
purpose: end-user guide for managing plugins and extensions
audience: end-user
status: live
---

# User Guide — Managing Plugins, Extensions, and Capabilities

## What this is

The DgxSparkLabs marketplace ships 27 skills, 22 rules, and 8 other-construct example plugins (agent, command, hook, mcp, lsp, monitor, output-style, theme) across six AI coding platforms — Claude Code, Codex, Gemini, Cursor, Windsurf, and Devin — plus a cross-platform `agents` CLI shim. Each platform exposes its own install / list / enable / disable / uninstall surface. This document covers every one of them so you do not have to chase per-vendor docs to learn how to manage what you installed. For the per-platform technical reference (paths each platform reads, CI assertions, known gaps), see `docs/PLATFORMS.md`. For hands-on QA verification with explicit expected behaviour, see `docs/TEST_YOURSELF.md`.

## Table of contents

- [At a glance](#at-a-glance)
- [Per-platform management](#per-platform-management)
  - [Claude Code](#claude-code)
  - [Codex](#codex)
  - [Gemini](#gemini)
  - [Cursor IDE](#cursor-ide)
  - [Cursor CLI (`agent`)](#cursor-cli-agent)
  - [Windsurf](#windsurf)
  - [Devin](#devin)
  - [`agents` CLI (cross-platform shim)](#agents-cli-cross-platform-shim)
- [Cross-platform conventions](#cross-platform-conventions)
- [Troubleshooting](#troubleshooting)
- [See also](#see-also)

## At a glance

One row per surface; each cell points at the canonical command (or "n/a" with explanation). Click a platform name to jump to its section.

| Surface | Install | List | Enable / Disable | Uninstall | Scope semantics |
|---|---|---|---|---|---|
| [Claude Code](#claude-code) | `claude plugin install <name>@<mp>` | `claude plugin list` / `claude plugin list --available` | `claude plugin enable <name>` / `claude plugin disable <name>` | `claude plugin uninstall <name>` | `--scope project` (writes project) or `--scope user` (writes user dir) |
| [Codex](#codex) | `codex plugin add <name>@<mp>` | `codex plugin list` | toggled by add/remove | `codex plugin remove <name>@<mp>` | per-marketplace install; no scope flag |
| [Gemini](#gemini) | `gemini extensions install <url-or-path> --consent` | `gemini extensions list 2>&1` | `gemini extensions disable <name>` / `enable <name>` | `gemini extensions uninstall <name>` | install is user-scope; auto-enable on install |
| [Cursor IDE](#cursor-ide) | `/add-plugin <name>@<github-url>` (chat) or Dashboard import | Settings → Plugins panel | per-plugin toggle in UI | Settings → Plugins → Remove | per-workspace; admin marketplace = team-wide |
| [Cursor CLI](#cursor-cli-agent) | no install surface — populate workspace files | n/a (filesystem only) | n/a | delete the workspace files | workspace-scoped only |
| [Windsurf](#windsurf) | no install surface — clone + open in IDE | n/a (filesystem only) | n/a | close project / remove files | workspace-scoped |
| [Devin](#devin) | no marketplace — clone the repo | `devin skills list` / `devin rules list` / `devin mcp list` | n/a (always-on if discovered) | delete the files | filesystem (per-project) |
| [`agents` CLI](#agents-cli-cross-platform-shim) | `agents install <name> --scope <s>` | `agents list` / `agents list --available` | n/a (install / uninstall) | `agents uninstall <name> --scope <s>` | `--scope project` (default; `.agents/` + per-platform spray) or `--scope user` (`~/.agents/` only) |

> Throughout this guide `<mp>` is shorthand for the marketplace identifier `dgxsparklabs-marketplace` (the name Claude / Codex register when you add this marketplace).

## Per-platform management

### Claude Code

Claude Code is the canonical surface — every other platform's emission is derived from the Claude-shaped per-plugin manifest. Install Claude Code: `npm install -g @anthropic-ai/claude-code`.

Reference: [code.claude.com/docs/en/plugins](https://code.claude.com/docs/en/plugins), [code.claude.com/docs/en/plugins-reference](https://code.claude.com/docs/en/plugins-reference), [code.claude.com/docs/en/plugin-marketplaces](https://code.claude.com/docs/en/plugin-marketplaces).

#### Install / uninstall

```bash
# Register the marketplace once (use any of these forms)
claude plugin marketplace add DgxSparkLabs/marketplace                 # GitHub shortform
claude plugin marketplace add https://github.com/DgxSparkLabs/marketplace
claude plugin marketplace add ./                                       # local clone
```

```bash
# Install / uninstall an individual plugin
claude plugin install skill-telegram-notify@dgxsparklabs-marketplace --scope project
claude plugin uninstall skill-telegram-notify --scope project
claude plugin prune --scope project -y                                 # drop orphaned deps
```

```bash
# Remove the marketplace itself
claude plugin marketplace remove dgxsparklabs-marketplace
```

#### Enable / disable

```bash
claude plugin enable  skill-telegram-notify --scope project
claude plugin disable skill-telegram-notify --scope project
```

Disable keeps the plugin installed (no re-download on re-enable); uninstall removes it from disk.

#### List installed / available

```bash
claude plugin list                                # installed plugins (project + user)
claude plugin list --json                         # same, machine-readable
claude plugin list --json --available             # installed + every available plugin in registered marketplaces
claude plugin marketplace list                    # registered marketplaces
claude plugin details <name>                      # one plugin's components + projected token cost
```

#### Scope semantics

Two scopes: `--scope project` writes to `./.claude/plugins/...` (lives with the project); `--scope user` writes to `~/.claude/plugins/...` (every project sees it). Bundles installed in one scope can include dependencies that also resolve into that scope.

#### What Claude does NOT install via the plugin marketplace

**Rules.** Per [code.claude.com/docs/en/plugins-reference#plugin-components-reference](https://code.claude.com/docs/en/plugins-reference#plugin-components-reference) (fetched 2026-05-26), Claude's plugin components are: Skills, Agents, Commands, Hooks, MCP servers, LSP servers, Monitors, Output Styles, Themes. **Rules are not listed** — they are part of Claude's *memory* subsystem, discovered from `.claude/rules/*.md` (project) and `~/.claude/rules/*.md` (user). See [code.claude.com/docs/en/memory#organize-rules-with-claude-rules](https://code.claude.com/docs/en/memory#organize-rules-with-claude-rules).

To use this marketplace's rules with Claude:

```bash
# Project scope — symlink (live updates) or copy (portable)
mkdir -p .claude/rules
ln -s "$(pwd)/rules/blast-radius/rule.md" .claude/rules/blast-radius.md
# or:
cp rules/blast-radius/rule.md .claude/rules/blast-radius.md

# User scope (apply across every project on this machine)
mkdir -p ~/.claude/rules
cp rules/blast-radius/rule.md ~/.claude/rules/blast-radius.md
```

The cross-platform `agents` CLI (below) automates this: `agents install rule-blast-radius --scope project --agents-only` writes to `.agents/rules/` and skips per-platform spray. Claude does not currently auto-discover from `.agents/rules/`, so for Claude specifically use the symlink-or-copy form above.

#### Validate a plugin (for contributors and curious users)

```bash
claude plugin validate ./           # validates the marketplace + all plugins
claude plugin validate _generated/skill-example
```

This marketplace gates CI on `claude plugin validate ./` producing zero warnings (see `.github/workflows/compat-validate.yml`).

### Codex

OpenAI's terminal coding agent. Install: `npm install -g @openai/codex`.

Reference: [developers.openai.com/codex/plugins/](https://developers.openai.com/codex/plugins/), [developers.openai.com/codex/plugins/build](https://developers.openai.com/codex/plugins/build).

#### Install / uninstall

```bash
codex plugin marketplace add DgxSparkLabs/marketplace                      # default branch
codex plugin marketplace add DgxSparkLabs/marketplace --ref some-branch    # specific branch
codex plugin marketplace add ./                                            # local clone

codex plugin add    skill-telegram-notify@dgxsparklabs-marketplace
codex plugin remove skill-telegram-notify@dgxsparklabs-marketplace

codex plugin marketplace remove dgxsparklabs-marketplace
```

#### Enable / disable

Codex has no explicit enable/disable subcommands. Plugins are toggled by add/remove. To temporarily disable a plugin without re-downloading, edit `~/.codex/config.toml` and comment out the `[plugins.<name>]` block.

#### List installed / available

```bash
codex plugin list                       # installed and available together (one table)
cat ~/.codex/config.toml                # registered marketplaces (no `marketplace list` subcommand)
codex mcp list                          # MCP-server-specific listing
```

#### Scope semantics

No project/user scope flag. Installs are per-marketplace into `~/.codex/`. The `.agents/plugins/marketplace.json` path (emitted by this marketplace's generator Phase 5.5) is Codex's canonical marketplace location going forward.

Reference: see `docs/PLATFORMS.md` Codex section for the marketplace ROOT path that `codex plugin marketplace list` reports.

### Gemini

Google's CLI agent. Install: `npm install -g @google/gemini-cli`. Gemini uses **extensions** (not plugins) as its install unit; the whole marketplace installs as one extension.

Reference: [geminicli.com/docs/extensions/](https://geminicli.com/docs/extensions/), [geminicli.com/docs/extensions/reference/](https://geminicli.com/docs/extensions/reference/).

#### Install / uninstall

```bash
# From GitHub (no clone required)
echo "y" | gemini extensions install https://github.com/DgxSparkLabs/marketplace --consent

# From GitHub at a specific branch
echo "y" | gemini extensions install https://github.com/DgxSparkLabs/marketplace --ref some-branch --consent

# From a local clone
echo "y" | gemini extensions install ./.gemini/ --consent

# Uninstall (name shown by `gemini extensions list 2>&1`)
gemini extensions uninstall dgxsparklabs-marketplace
```

The `--consent` flag is required: extensions can ship hooks and MCP servers, so Gemini asks for explicit consent before enabling them. The piped `echo "y"` answers the prompt for non-interactive scripts.

#### Enable / disable

```bash
gemini extensions disable dgxsparklabs-marketplace
gemini extensions enable  dgxsparklabs-marketplace
```

#### List installed / available

```bash
gemini extensions list 2>&1                # installed extensions (output goes to stderr; the 2>&1 is required)
gemini skills list --all 2>&1              # discovered skills (project + user + built-in + extension)
gemini mcp list 2>&1                       # configured MCP servers
gemini extensions validate <path>          # validate an extension manifest
```

The `2>&1` is required on Linux — Gemini writes list output to stderr by quirk. Verified empirically (see `docs/PLATFORMS.md` Gemini "Known gaps").

#### Scope semantics

Extensions install user-scope by default at `~/.gemini/extensions/<name>/`. Auto-enable on install. There is no project-scope-only install for a marketplace extension; for project-only skills, use `gemini skills install <local-skill-dir>`.

#### Gemini auth note

`gemini auth login` is required only if you actually run Gemini for chat — the extension install/list/validate commands are auth-free. The top-level `gemini --list-extensions` flag does require auth (and exits 41 when missing); always prefer the subcommand form `gemini extensions list`.

### Cursor IDE

Anysphere's IDE (VS Code fork). Plugin install is **IDE-only or admin-Dashboard-only** — there is no `cursor` CLI with plugin commands.

Reference: [cursor.com/docs/plugins](https://cursor.com/docs/plugins), [cursor.com/docs/reference/plugins](https://cursor.com/docs/reference/plugins).

#### Install / uninstall

Two install paths:

**Path 1 — In-editor `/add-plugin` (per-plugin):**

Open any workspace in Cursor, open the agent chat panel, and run:

```text
/add-plugin <plugin-name>@https://github.com/DgxSparkLabs/marketplace
```

The `<plugin-name>@<url>` form is important. The naked-URL form (`/add-plugin https://github.com/DgxSparkLabs/marketplace`) puts Cursor's chat agent into research-spiral mode (it investigates the repo instead of installing). The named form goes straight to the install UI.

**Path 2 — Dashboard team marketplace (admin, marketplace-wide):**

> Dashboard → Settings → Plugins → Import → paste `https://github.com/DgxSparkLabs/marketplace` → save

A branch selector appears in the Dashboard UI for non-default-branch import. Team marketplaces propagate to every member of the team.

Uninstall is the same UI: Settings → Plugins → click the plugin → Remove.

#### Enable / disable

Per-plugin toggles live in Settings → Plugins. Disabled plugins remain installed but inactive.

#### List installed / available

Settings → Plugins panel. There is no headless CLI introspection.

#### Scope semantics

In-editor install lands per-workspace under `.cursor/`. Dashboard team-marketplace import is team-wide (every member sees the marketplace once enabled).

#### settings.json shape

After install, the plugin's per-plugin manifest at `_generated/<plugin>/.cursor-plugin/plugin.json` is read by Cursor; its pointer fields (`skills`, `commands`, `agents`, `hooks`, `mcpServers`) tell Cursor where to find each construct inside the plugin. Workspace state lives in `.cursor/settings.json`.

### Cursor CLI (`agent`)

Cursor ships a CLI named `agent` (NOT `cursor`). It has **no plugin install commands** — `agent --help` lists `mcp`, `models`, `generate-rule`, etc., but no `plugin install`, `plugin list`, `marketplace add`, or `add-plugin`. The CLI reads from the workspace filesystem only.

Install:

```bash
curl https://cursor.com/install -fsS | bash                   # macOS / Linux / WSL
irm 'https://cursor.com/install?win32=true' | iex             # Windows PowerShell

agent --version
```

#### Install / uninstall (workspace-mirror only)

The CLI consumes whatever is on disk in `.cursor/`, `.cursor-plugin/`, and `.agents/`. To "install" a plugin for the CLI:

```bash
# 1. Populate the workspace from this marketplace via the cross-platform `agents` CLI
agents install skill-example --scope project
```

```bash
# 2. (Alternative) Inject a local plugin dir at runtime for one session
agent --plugin-dir ./path/to/plugin
```

To "uninstall", remove the workspace files (`agents uninstall <name> --scope project` cleans both `.agents/` and per-platform spray).

#### List installed / available

The CLI has no plugin enumeration command. Implicit discovery via opening the workspace in `agent`. For visibility, inspect the workspace files: `ls .cursor/rules/`, `ls .agents/skills/`, etc.

#### Scope semantics

Workspace only. `--plugin-dir` is a per-session runtime injection, not a persistent install.

### Windsurf

Codeium's IDE (VS Code fork; acquired by Cognition in July 2025). **No CLI exists** — confirmed empirically across npm / pip / snap / apt / GitHub releases.

Reference: [docs.windsurf.com/windsurf/cascade/skills](https://docs.windsurf.com/windsurf/cascade/skills), [docs.windsurf.com/windsurf/cascade/hooks](https://docs.windsurf.com/windsurf/cascade/hooks).

#### Install / uninstall (clone-and-open)

```bash
git clone https://github.com/DgxSparkLabs/marketplace
# Open the cloned directory in Windsurf IDE → File → Open Folder
```

That's it. Windsurf Cascade auto-discovers at IDE open:

- Rules: `.windsurf/rules/*.md` (with required `trigger:` frontmatter — `always_on`, `model_decision`, `glob`, or `manual`; 12,000-char body limit)
- Skills: `.agents/skills/<name>/SKILL.md` (the cross-platform path) AND `.windsurf/skills/<name>/SKILL.md`
- Hooks: `.windsurf/hooks.json`

Uninstall = close the project or delete the files.

#### Enable / disable / list

Implicit. There is no surface to enumerate what's loaded — verify by interacting with Cascade (`@skill-name` for skills; ask "what rules are in effect?" for rules).

#### Scope semantics

Workspace-scoped via the cloned directory. User-scope skills available via `~/.codeium/windsurf/...` / `~/.agents/skills/`.

### Devin

Cognition's terminal agent. Install: `curl -fsSL https://cli.devin.ai/install.sh | bash` (the installer exits 1 in non-TTY environments but the binary still lands at `~/.local/bin/devin`; CI workarounds wrap with `|| true`).

Reference: per-platform `docs/PLATFORMS.md` Devin section + `docs/archive/empirical-cli-findings/devin.md` (the empirical CLI tree).

#### Install / uninstall (no marketplace)

Devin has no plugin marketplace concept. Content is discovered live from the filesystem at session start. Clone the repo into your project and you are done:

```bash
git clone https://github.com/DgxSparkLabs/marketplace
cd marketplace
```

Devin reads:

- `.agents/skills/<name>/SKILL.md` (skills — both project and `~/.agents/skills/` for user-scope)
- `.windsurf/rules/*.md`, `.cursor/rules/*.md`, `.cursorrules`, `AGENTS.md` (rules — provider-tagged)
- MCP servers configured via `devin mcp add` (separate from our marketplace)

#### List installed / available

```bash
devin skills list                       # discovered skills (auth-free)
devin rules list                        # discovered rules with provider tags
devin mcp list                          # configured MCP servers
devin skills paths                      # where Devin scans for skills
devin rules paths                       # where Devin scans for rules
devin skills show <name>                # one skill's content
devin rules show <name>                 # one rule's content
```

These are all auth-free. `devin auth login` ("Log in to Windsurf" — Devin is built on Codeium infrastructure) is only required to run Devin agent sessions.

#### Enable / disable

Always-on if discovered. To disable a rule or skill, remove it from the discovered paths.

#### Scope semantics

Project-scope via the cloned repo. User-scope via `~/.config/devin/skills/` and `~/.agents/skills/`.

### `agents` CLI (cross-platform shim)

A Python shim shipped with this marketplace that gives every platform a uniform install experience driven from a shell. Install:

```bash
# POSIX (drops `agents` into ~/.local/bin/)
curl -fsSL https://raw.githubusercontent.com/DgxSparkLabs/marketplace/main/install.sh | bash

# Windows PowerShell
irm https://raw.githubusercontent.com/DgxSparkLabs/marketplace/main/install.ps1 | iex

# Pin to a specific marketplace branch
AGENTS_REF=some-branch curl -fsSL https://raw.githubusercontent.com/DgxSparkLabs/marketplace/main/install.sh | bash
```

Env-var surface (from `install.sh`): `AGENTS_REF` (marketplace branch, default `main`), `AGENTS_MARKETPLACE_URL` (repo URL override), `AGENTS_DEST` (wrapper install path), `AGENTS_LIB` (library install path), `AGENTS_PYTHON` (Python interpreter). Same env vars on `install.ps1` (`$env:AGENTS_REF`, etc.).

#### Install / uninstall

```bash
agents install   skill-telegram-notify --scope project
agents install   rule-blast-radius     --scope project --agents-only
agents install   agent-example         --scope user
agents uninstall skill-telegram-notify --scope project
```

#### Enable / disable

The CLI exposes install/uninstall only. To toggle without re-downloading, use the platform-native enable/disable surface where it exists (Claude, Gemini); on filesystem-only platforms (Windsurf, Devin), remove the file.

#### List installed / available

```bash
agents list                             # installed plugins (project + user)
agents list --available                 # all available plugins from the marketplace
agents info <plugin-name>               # metadata for one plugin
```

#### Scope semantics

- `--scope project` (default): writes to `.agents/<construct>/<name>/` AND sprays to per-platform paths (`.cursor/`, `.windsurf/`, `.gemini/`, `.codex/`, `.claude/`) so every consuming tool sees the content.
- `--scope user`: writes to `~/.agents/<construct>/<name>/` only (no project spray, no per-platform spray).
- `--agents-only`: strict mode — writes ONLY to `.agents/<construct>/` (or `~/.agents/<construct>/` if combined with `--scope user`); skips per-platform spray entirely.

#### Marketplace subcommands

```bash
agents marketplace add    <url-or-path>
agents marketplace list
agents marketplace remove <name>
```

## Cross-platform conventions

### The `.agents/` directory

Cross-platform skill convergence: Windsurf, Cursor, and Devin all natively discover skills at `.agents/skills/<name>/SKILL.md`. This is the only true convergence point. For rules, the forward-looking `.agents/rules/<name>.md` path is emitted by this marketplace's `AgentsPlatform` but is not yet read by any platform natively (Cursor 2.7+ and Windsurf 2.0 are credible future adopters).

Per-platform rule discovery today:

| Platform | Rule discovery path |
|---|---|
| Claude Code | `.claude/rules/*.md` (project) and `~/.claude/rules/*.md` (user) — memory subsystem, not plugins |
| Codex | `AGENTS.md`, `.cursor/rules/*.md`, `.windsurf/rules/*.md` (filesystem) |
| Gemini | `GEMINI.md`, `AGENTS.md` |
| Cursor | `.cursor/rules/*.md` (`.mdc` accepted) and `.cursorrules` (legacy single-file) |
| Windsurf | `.windsurf/rules/*.md` with `trigger:` frontmatter |
| Devin | `.windsurf/rules/`, `.cursor/rules/`, `.cursorrules`, `AGENTS.md` |

### Plugin name conventions

Every plugin in this marketplace is named `<prefix>-<instance-name>`:

| Construct | Prefix | Example |
|---|---|---|
| Skill | `skill-` | `skill-telegram-notify` |
| Rule | `rule-` | `rule-blast-radius` (Cursor/Codex/Gemini/Windsurf — Claude reads via filesystem) |
| Agent (sub-agent) | `agent-` | `agent-example` |
| Command | `command-` | `command-example` |
| Hook | `hook-` | `hook-example` |
| MCP server | `mcp-` | `mcp-example` |
| LSP server | `lsp-` | `lsp-example` (Claude-only consumer) |
| Monitor | `monitor-` | `monitor-example` (Claude-only consumer) |
| Output style | `output-style-` | `output-style-example` (Claude-only consumer) |
| Theme | `theme-` | `theme-example` (Claude-only consumer) |
| Bundle (dep-only) | `bundle-` | `bundle-skill-all`, `bundle-communication-skills` |

### Slash command namespacing (Claude-specific)

Per [code.claude.com/docs/en/plugins](https://code.claude.com/docs/en/plugins) (2026-05-26): *"Plugin skills are always namespaced (like `/my-first-plugin:hello`) to prevent conflicts when multiple plugins have skills with the same name. To change the namespace prefix, update the `name` field in `plugin.json`."* There is **no flatten mechanism** — the only lever is the plugin name.

| Construct | Invocation form | Source |
|---|---|---|
| Skill | `/<plugin-name>:<skill-name>` (e.g., `/skill-example:lab-notebook`) | plugins.md, skills.md |
| Command | `/<plugin-name>:<file-stem>` (e.g., `/command-example:hello`) | skills.md ("Custom commands have been merged into skills") |
| Agent (sub-agent) | `<plugin-name>:<agent-name>` (no `/` — appears in `/agents` UI; e.g., `agent-example:notebook-reviewer`) | plugins-reference.md |
| MCP tool | `mcp__<plugin-name>__<server-key>__<tool>` (hook-matcher form) OR `plugin:<plugin-name>:<server-key>` (CLI display form) | hooks.md, plugins-reference.md |

A common operator confusion: typing `/` in Claude shows skill entries that look "flat" (e.g., bare `/lab-notebook`) — the flat form also resolves per `code.claude.com/docs/en/skills`, but the **canonical** invocation is always the namespaced form `/skill-example:lab-notebook`.

For **bundles**, namespacing follows each contained plugin's own name. Installing `bundle-skill-all` does not introduce a `bundle-skill-all:*` namespace — the contained skills appear under their own plugin namespaces (e.g., `/skill-act-runner:act-runner`).

Reference: [code.claude.com/docs/en/plugins-reference#plugin-components-reference](https://code.claude.com/docs/en/plugins-reference#plugin-components-reference).

### Bundles vs individual plugins

A **bundle** is a dependency-only plugin that installs a curated group. An **individual plugin** is a single construct.

| Bundle kind | How named | Source |
|---|---|---|
| Domain bundle (curated) | `bundle-<domain>-<construct-plural>` (e.g., `bundle-communication-skills`) | declared in `catalog.toml` |
| Catch-all bundle (every plugin of one construct type) | `bundle-<prefix>-all` (e.g., `bundle-skill-all`) | code-generated; not declared in `catalog.toml` |
| Cross-construct examples bundle | `bundle-examples` | declared in `catalog.toml` — installs one of each construct type for tutorial purposes |

Installing a bundle in Claude auto-installs its dependencies (the install output reports `(+ N dependencies: ...)`). Uninstalling a bundle does NOT auto-remove its dependencies — they orphan until `claude plugin prune --scope <scope> -y`.

**Claude-side bundle cascade after the 2026-05-26 rule deprecation**: bundles whose members are exclusively `rule:` references (`bundle-quality-rules`, `bundle-workflow-rules`, `bundle-documentation-rules`, `bundle-environment-rules`, `bundle-notifications-rules`) and the catch-all `bundle-rule-all` are no longer surfaced in Claude's marketplace listing because their dependencies are no longer valid Claude plugins. They remain available to Cursor / Codex / Gemini / Windsurf where rule plugins are still valid. For Claude users who want the rule content, use the symlink-or-copy approach described in the Claude section above.

## Troubleshooting

### `claude plugin validate ./` warns about missing description

Fixed in this marketplace via `MARKETPLACE.toml`'s `description` field, which the generator propagates to the top-level `.claude-plugin/marketplace.json`. If you fork this marketplace, ensure your `MARKETPLACE.toml` keeps the `description` field set — CI gates on zero warnings via `.github/workflows/compat-validate.yml`. To check locally:

```bash
claude plugin validate ./        # expected: "Validation passed" with no warnings
```

### Cursor skill popup shows mangled metadata

Fixed in PR #5 — `CursorPlatform.build_plugin_json` for `SkillConstruct` now emits `description`, `version`, and a `skills` pointer per [cursor.com/docs/reference/plugins](https://cursor.com/docs/reference/plugins) (2026-05-25). Make sure you are on a recent release.

### Hook does not seem to do anything

Hooks fire silently by design — Claude does not print "hook fired" to the operator. Observe via per-event-type sentinel files. This marketplace's `hook-example` plugin writes to `/tmp/hook-fired-<event>.log` for every event variant (SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, Stop, SessionEnd). Verify with:

```bash
tail -f /tmp/hook-fired-*.log
```

See `hooks/example/hooks/hooks.json` for the per-event-type sentinel pattern you can replicate in your own hook plugins.

### MCP server fails to connect (`uv`-related)

The `mcp-example` plugin requires `uv` installed (it uses `uvx mcp-server-fetch`). Install once:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh                       # POSIX
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"            # Windows
```

After install, `uvx` becomes available on PATH and the MCP server connects on first invocation. See `mcp-servers/example/README.md` for details.

### Output style "applied" but I do not see a difference

Claude output styles change response framing without a separate confirmation. Verify via:

1. `cat .claude/settings.local.json` — expect `"outputStyle": "<Name>"`
2. `/clear` then ask Claude a small task that exercises the style markers (e.g., for `output-style-example`'s "Lab Notebook Voice", the response should end with a `Next:` line)
3. See `docs/TEST_YOURSELF.md` Claude section for the full validation method including a clean session A/B comparison

### Gemini `extensions list` prints nothing

Gemini writes list output to stderr — always pipe with `2>&1`:

```bash
gemini extensions list 2>&1
gemini skills list --all 2>&1
gemini mcp list 2>&1
```

### Cursor `/add-plugin <url>` triggers chat research instead of install

Use the named form `/add-plugin <plugin-name>@<url>`. The naked URL form sends the chat agent into a research spiral; the named form goes straight to the install UI.

## See also

- `README.md` — quick install + marketplace overview
- `docs/PLATFORMS.md` — per-platform technical reference (install, discovery, support, CI assertions, gaps)
- `docs/ARCHITECTURE.md` — generator and emission architecture
- `docs/ADDING_A_CONSTRUCT.md` — contributor walkthrough for adding a new plugin
- `docs/TEST_YOURSELF.md` — operator QA verification with explicit hands-on validations
- `CONTRIBUTING.md` — broader contributor workflow + the `claude plugin validate` CI gate
- `CHANGELOG.md` — release notes
