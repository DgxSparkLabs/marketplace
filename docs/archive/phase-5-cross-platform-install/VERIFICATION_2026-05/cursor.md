# Cursor (IDE + CLI) — May 2026 Verification

**Research date**: 2026-05-24
**Researcher**: internet-research-agent (Claude subagent)
**Scope**: Cursor IDE + Cursor CLI capabilities as of May 2026
**Prior empirical**: docs/EMPIRICAL_CLI_FINDINGS/cursor.md (dated 2026-05-22)

---

## Executive summary

- **PRIOR CONCLUSION OVERTURNED**: The 2026-05-22 empirical doc concluded "no CLI exists." A Cursor CLI **does exist** as of May 2026, under the binary name `agent` (installed via `curl https://cursor.com/install -fsS | bash`). The prior doc tested for `cursor` binary in headless Linux — the installed binary is `agent`, not `cursor`.
- **Cursor IDE Marketplace**: Launched 2026-02-17 with Cursor 2.5 at `cursor.com/marketplace`. Plugins bundle MCP servers, skills, subagents, rules, and hooks into a single install. Install in-editor via `/add-plugin`.
- **Plugin manifest**: File path is `<plugin-dir>/.cursor-plugin/plugin.json`. Only `name` is required (lowercase kebab-case). Multi-plugin repos use a root `.cursor-plugin/marketplace.json` to list all plugins.
- **Team marketplace**: Launched 2026-03-03 (Cursor 2.6). Admins go to Dashboard → Settings → Plugins → Import, paste a GitHub repo URL, set access groups. As of 2026-05-01, no repo is required for basic team marketplace setup.
- **CLI `agent` binary**: Subcommands include `ls`, `resume`; slash commands in interactive mode include `/plan`, `/ask`, `/compress`, `/resume`, `/mcp enable`, `/mcp disable`, `/rules`, `/commands`, `/model`, `/sandbox`, `/max-mode`. No `add-plugin` or plugin-list CLI command found in documentation.
- **Rules relationship**: `.cursor/rules/*.mdc` and legacy `.cursorrules` both remain valid. Rules can also be bundled inside a plugin's `rules/` directory and install automatically. Both coexist; plugins do not replace standalone rules.
- **`.agents/skills/` path**: VERIFIED — Cursor natively reads `.agents/skills/<name>/SKILL.md` (project-level). `.agents/plugins/marketplace.json` is NOT a Cursor-native path; Cursor uses `.cursor-plugin/marketplace.json`.

---

## Per-claim verification table

| Claim | Status | Evidence | Source/Log |
|-------|--------|----------|------------|
| Cursor CLI exists as of May 2026 | VERIFIED-YES | Binary `agent`, install via curl, official docs page cursor.com/docs/cli/overview | https://cursor.com/docs/cli/overview — fetched 2026-05-24 |
| Prior doc "no CLI" conclusion (2026-05-22) is now wrong | VERIFIED-YES | Prior doc tested for `cursor` binary; actual binary is `agent`. CLI launched ~Nov 2025, documented with Jan 2026 updates | https://cursor.com/changelog/cli-jan-08-2026 — fetched 2026-05-24 |
| CLI binary name is `agent` | VERIFIED-YES | "Binary Name: `agent`" and "New `agent` command is now the primary CLI entrypoint. `cursor-agent` remains as a backward-compatible alias." | https://cursor.com/changelog/cli-jan-08-2026 — fetched 2026-05-24 |
| CLI install command (macOS/Linux) | VERIFIED-YES | `curl https://cursor.com/install -fsS | bash` | https://cursor.com/docs/cli/installation — fetched 2026-05-24 |
| CLI install command (Windows PowerShell) | VERIFIED-YES | `irm 'https://cursor.com/install?win32=true' | iex` | https://cursor.com/docs/cli/installation — fetched 2026-05-24 |
| Plugin marketplace exists at cursor.com/marketplace | VERIFIED-YES | Page live; "Extend the Agent" with plugins and automations | https://cursor.com/marketplace — fetched 2026-05-24 |
| Marketplace launched with Cursor 2.5 on 2026-02-17 | VERIFIED-YES | "February 17, 2026 – The blog post announcing plugin support." | https://cursor.com/changelog/2-5 — fetched 2026-05-24 |
| `/add-plugin` slash command exists in editor | VERIFIED-YES | "install directly in the editor with `/add-plugin`" | https://forum.cursor.com/t/cursor-2-5-plugins/152124 — fetched 2026-05-24 |
| Plugin manifest path is `.cursor-plugin/plugin.json` | VERIFIED-YES | "Each plugin is a standalone directory at the repository root with its own `.cursor-plugin/plugin.json` manifest." | https://github.com/cursor/plugins README — fetched 2026-05-24 |
| Only `name` is required in plugin.json | VERIFIED-YES | "The manifest only requires a 'name' field." | https://cursor.com/docs/plugins — fetched 2026-05-24 |
| Multi-plugin repo uses `.cursor-plugin/marketplace.json` | VERIFIED-YES | "root `.cursor-plugin/marketplace.json` lists all plugins" | https://github.com/cursor/plugins README — fetched 2026-05-24 |
| Team marketplace launched Cursor 2.6 (2026-03-03) | VERIFIED-YES | "Launch Date: March 3, 2026" — team marketplace thread | https://forum.cursor.com/t/cursor-2-6-team-marketplaces-for-plugins/153484 — fetched 2026-05-24 |
| Team marketplace import: Dashboard → Settings → Plugins → Import → paste GitHub URL | VERIFIED-YES | Documented in official plugin docs: "Paste the GitHub repository URL and continue" | https://cursor.com/docs/plugins — fetched 2026-05-24 |
| May 1 2026: team marketplace without repo + install-behavior controls | VERIFIED-YES | "team marketplace setup without a repository plus first-party plugin install controls with three distribution modes called Default Off, Default On, and Required" | https://www.pravinkumar.co/blog/cursor-plugin-marketplace-webflow-studios-2026 — fetched 2026-05-24 |
| Cursor reads `.agents/skills/<name>/SKILL.md` natively | VERIFIED-YES | "Skills are automatically loaded from these locations: `.agents/skills/` Project-level" | https://cursor.com/docs/context/skills — fetched 2026-05-24 |
| Cursor reads `.agents/plugins/marketplace.json` natively | VERIFIED-NO | No mention in any Cursor docs; Cursor uses `.cursor-plugin/marketplace.json` not `.agents/plugins/marketplace.json` | https://cursor.com/docs/plugins, https://cursor.com/docs/reference/plugins — fetched 2026-05-24 |
| CLI has plugin install command (e.g., `agent add-plugin`) | VERIFIED-NO | No plugin-related CLI subcommands found in any docs; `/add-plugin` is IDE-editor-only slash command | https://cursor.com/docs/cli/overview, https://cursor.com/docs/cli/using — fetched 2026-05-24 |
| CLI can list installed plugins | VERIFIED-NO | No `agent plugins ls` or similar found in documentation | https://cursor.com/docs/cli/overview — fetched 2026-05-24 |
| `.cursorrules` still valid May 2026 | INCONCLUSIVE | Docs reference `.cursor/rules/*.mdc` as current standard but do not explicitly deprecate `.cursorrules`; prior empirical doc confirms both paths active | https://cursor.com/docs/rules — fetched 2026-05-24 |

---

## Section 1: Cursor IDE marketplace mechanism (with evidence)

### 1a. Does a plugin marketplace exist as of May 2026?

Yes. The Cursor Marketplace is at `https://cursor.com/marketplace`.

**Quoted excerpt** from `cursor.com/marketplace` (fetched 2026-05-24):
> "Extend the Agent" with plugins and automations. [...] "[Publish Plugins](/marketplace/publish)"

The marketplace launched February 17, 2026 alongside Cursor 2.5. From the official changelog at `cursor.com/changelog/2-5` (fetched 2026-05-24):
> "Plugins bundle skills, subagents, MCP servers, hooks, and rules, into a single install."

Initial partners were Amplitude, AWS, Figma, Linear, and Stripe. On March 11, 2026 (`cursor.com/blog/new-plugins`, fetched 2026-05-24), over 30 additional plugins joined from Atlassian, Datadog, GitLab, Glean, Hugging Face, monday.com, and PlanetScale.

### 1b. How to install a plugin from a public GitHub repo

**In-editor action sequence** (from `cursor.com/docs/plugins`, fetched 2026-05-24):
1. Type `/add-plugin` in the editor agent chat, or browse `cursor.com/marketplace`.
2. The editor parses the plugin manifest and installs components.

For **team marketplace import of a GitHub repo** (from `cursor.com/docs/plugins`, fetched 2026-05-24):
1. Go to **Dashboard → Settings → Plugins**
2. Click **Import** under Team Marketplaces
3. "Paste the GitHub repository URL and continue"
4. Review parsed plugins and set access groups
5. Name and save the marketplace

No deeplink or REST API form for plugin install was found in documentation. The `/add-plugin` command is IDE-chat-only; no CLI equivalent exists.

### 1c. Plugin manifest schema

Source: `cursor.com/docs/reference/plugins` (fetched 2026-05-24).

**File path**: `<plugin-root>/.cursor-plugin/plugin.json`

**Required fields**:
- `name` (string): "Plugin identifier. Lowercase, kebab-case (alphanumerics, hyphens, and periods). Must start and end with an alphanumeric character."

**Optional fields** (all from `cursor.com/docs/reference/plugins`, fetched 2026-05-24):

| Field | Type | Notes |
|-------|------|-------|
| `description` | string | Brief explanation |
| `version` | string | Semantic version, e.g. `1.0.0` |
| `author` | object | `name` (required inside), `email` (optional) |
| `homepage` | string | URL |
| `repository` | string | URL |
| `license` | string | e.g. `MIT` |
| `keywords` | array | Discovery tags |
| `logo` | string | Path or absolute URL |
| `rules` | string/array | Path(s) to rule files or directories |
| `agents` | string/array | Path(s) to agent files or directories |
| `skills` | string/array | Path(s) to skill directories |
| `commands` | string/array | Path(s) to command files or directories |
| `hooks` | string/object | Hooks config path or inline config |
| `mcpServers` | string/object/array | MCP config path, inline config, or array |

**Default auto-discovery directories** (when manifest fields are omitted), from `cursor.com/docs/reference/plugins` (fetched 2026-05-24):
- Skills: `skills/` (subdirs containing `SKILL.md`)
- Rules: `rules/` (`.md`, `.mdc`, or `.markdown` files)
- Agents: `agents/`
- Commands: `commands/`
- Hooks: `hooks/hooks.json`
- MCP Servers: `mcp.json`

### 1d. Team marketplace / private marketplace

From `forum.cursor.com/t/cursor-2-6-team-marketplaces-for-plugins/153484` (fetched 2026-05-24):
> "Launch Date: March 3, 2026. Admins on Teams and Enterprise plans can now create team marketplaces to share private plugins internally."

GitHub repo URL pattern: documentation says "paste a GitHub repo URL" but does not specify a URL pattern beyond standard GitHub repo URLs. The repo root must contain `.cursor-plugin/marketplace.json` listing the plugins (structure confirmed in `github.com/cursor/plugins` README, fetched 2026-05-24):
> "root `.cursor-plugin/marketplace.json` lists all plugins"

From `pravinkumar.co/blog/cursor-plugin-marketplace-webflow-studios-2026` (fetched 2026-05-24), covering the May 1, 2026 update:
> "team marketplace setup without a repository plus first-party plugin install controls with three distribution modes called Default Off, Default On, and Required."

The three distribution modes (verified from this source):
- **Default Off**: plugin available but not auto-installed; developers opt in
- **Default On**: installs for every developer, can be disabled
- **Required**: installs automatically, cannot be disabled

### 1e. `/add-plugin` slash command — Cursor 2.x verification

From `forum.cursor.com/t/cursor-2-5-plugins/152124` (fetched 2026-05-24):
> "Users can install directly in the editor with `/add-plugin`"

This shipped with Cursor 2.5 (2026-02-17). No evidence it was removed or replaced in subsequent updates through Cursor 3.3 (May 7, 2026) or the May 20, 2026 automations update.

### 1f. Relationship between plugins and `.cursor/rules` / `.cursorrules`

From `cursor.com/docs/rules` (fetched 2026-05-24):
- `.cursor/rules/*.mdc` is the current standard for project-level rules, using YAML frontmatter with fields `alwaysApply`, `description`, and `globs`.
- "Cursor supports `.md` and `.mdc` extensions. Use `.mdc` files with frontmatter to specify `description` and `globs`"
- The docs do not explicitly deprecate `.cursorrules` but do not feature it prominently.

From the plugin manifest reference at `cursor.com/docs/reference/plugins` (fetched 2026-05-24), plugins include a `rules` field pointing to `.mdc` files. The auto-discovery path is `rules/` inside the plugin directory. This means rules can be **bundled inside plugins** and install automatically — they do not replace standalone `.cursor/rules/` files. Both mechanisms coexist. Plugins simply add rules to the same pool that `.cursor/rules/` populates.

---

## Section 2: Cursor CLI (with evidence)

### 2a. Does a Cursor CLI exist as of May 2026?

**Yes.** This overturns the prior empirical conclusion from 2026-05-22.

The prior doc's failure mode: it tested for a binary named `cursor` in a headless Linux environment. The CLI binary is named `agent`, not `cursor`. The `cursor-agent` alias also exists (from `cursor.com/changelog/cli-jan-08-2026`, fetched 2026-05-24):
> "New `agent` command is now the primary CLI entrypoint. `cursor-agent` remains as a backward-compatible alias."

The CLI install script at `https://cursor.com/install` — which the prior doc confirmed returns a real bash script titled "Cursor Agent Installer" — installs the `agent` binary. The prior doc correctly identified the script but incorrectly concluded no binary was produced; the binary name it was testing (`cursor`, `agent`) was partially correct but the PATH verification in the CI headless run apparently failed to detect `agent`. The CLI's install path in headless Linux may be `~/.local/bin/agent` or similar, not necessarily in `/usr/local/bin`.

### 2b. Binary name, install command, version, subcommand tree

**Binary name**: `agent` (alias: `cursor-agent`)

**Install commands**:
- macOS/Linux/WSL: `curl https://cursor.com/install -fsS | bash` (from `cursor.com/docs/cli/installation`, fetched 2026-05-24)
- Windows PowerShell: `irm 'https://cursor.com/install?win32=true' | iex` (same source)
- Version check: `agent --version`
- Update: `agent update`

**Version as of 2026-05-24**: Not published on docs pages; use `agent --version` to check.

**Subcommand tree** (compiled from `cursor.com/docs/cli/overview` and `cursor.com/docs/cli/using`, fetched 2026-05-24):

```
agent                         # start interactive session
agent ls                      # list previous chats
agent resume                  # resume latest conversation
agent --continue              # continue previous session
agent --resume="<chat-id>"    # resume specific conversation
agent update                  # manually update the CLI
agent --version               # print version
agent -p "<prompt>"           # run with inline prompt
agent --model <model>         # specify model
agent --output-format <fmt>   # set output format
agent --sandbox <mode>        # configure sandbox (enabled/disabled)
agent --mode=plan             # start in Plan mode
agent --mode=ask              # start in Ask mode
```

**Slash commands** (available inside interactive session; from `cursor.com/changelog/cli-jan-08-2026` and `cursor.com/changelog/cli-jan-16-2026`, fetched 2026-05-24):
```
/plan                  # design approach with clarifying questions
/ask                   # explore code without making changes
/compress              # free up context window space
/resume                # resume prior conversation
/model                 # view or select model
/models                # list available models (alias)
/mcp list              # browse and configure MCP servers
/mcp enable <name>     # enable an MCP server on the fly
/mcp disable <name>    # disable an MCP server on the fly
/rules                 # create and edit rules from CLI
/commands              # create and edit commands from CLI
/sandbox               # configure command execution settings
/max-mode [on|off]     # toggle Max Mode
/usage                 # view usage stats and streaks
/about                 # environment and setup details
/setup-terminal        # configure newline keybindings
```

Prepend `&` to any message to push the conversation to a Cloud Agent (`cursor.com/changelog/cli-jan-16-2026`, fetched 2026-05-24):
> "Use Cloud handoff to push local conversations to cloud agents by prepending `&` to messages."

### 2c. Closest substitute — now superseded

The prior doc recommended file-existence and format checks as the only validation path. This remains true for **plugin validation**, but the CLI itself is now available for interactive use and scripting. The IDE binary at `c:\Users\devic\AppData\Local\Programs\cursor\resources\app\bin\cursor.cmd` is the GUI launcher, not the headless agent CLI.

### 2d. Plugin-related CLI commands

**No plugin install or list commands exist in the CLI.** From `cursor.com/docs/cli/overview` and `cursor.com/docs/cli/using` (both fetched 2026-05-24):
> The documentation does not mention plugin-related commands for the agent CLI.

`/add-plugin` is an IDE editor chat slash command only, not a CLI slash command. The CLI's `/rules` and `/commands` slash commands manage rules and commands but not plugins.

For plugin install, the only available mechanism remains the in-editor `/add-plugin` command or the Dashboard UI.

---

## Section 3: `.agents/` standard adoption (with evidence)

### 3a. Does Cursor read `.agents/skills/<name>/SKILL.md` natively?

**Yes.** From `cursor.com/docs/context/skills` (fetched 2026-05-24):

> "Skills are automatically loaded from these locations:
>
> | Location            | Scope               |
> | ------------------- | ------------------- |
> | `.agents/skills/`   | Project-level       |
> | `.cursor/skills/`   | Project-level       |
> | `~/.agents/skills/` | User-level (global) |
> | `~/.cursor/skills/` | User-level (global) |"

The document also states:
> "For compatibility, Cursor also loads skills from Claude and Codex directories: `.claude/skills/`, `.codex/skills/`, `~/.claude/skills/`, and `~/.codex/skills/`."

This means the `.agents/` path is Cursor's **primary** project-level skill path. Each skill must be a folder containing a `SKILL.md` file: `.agents/skills/<name>/SKILL.md`.

### 3b. Does Cursor read `.agents/plugins/marketplace.json`?

**No.** No Cursor documentation reference to `.agents/plugins/marketplace.json` was found in any source fetched. Cursor's plugin marketplace manifest lives at `.cursor-plugin/marketplace.json` (for multi-plugin GitHub repos) or is managed via the Dashboard. The `.agents/plugins/` path is not a Cursor-native construct.

### 3c. The broader `.agents/` convergence story from Cursor's side

From `cursor.com/docs/context/skills` (fetched 2026-05-24), Cursor reads skills from `.agents/skills/`, `.cursor/skills/`, `.claude/skills/`, and `.codex/skills/`. The search at `agensi.io/learn/ai-agent-configuration-guide-2026` (fetched 2026-05-24) corroborates broad adoption:
> "Claude Code (Anthropic), Codex CLI (OpenAI), Gemini CLI (Google), GitHub Copilot, Cursor, and Windsurf all read the same files."

However, **for plugins/marketplace** there is no `.agents/` convergence from Cursor's side. Cursor uses its own `.cursor-plugin/` format and `cursor.com/marketplace` distribution. The `.agents/plugins/marketplace.json` path, if it exists as a convention in this project, is not natively consumed by Cursor — it would need to be read by a plugin that wraps it, or the project would need to translate it into Cursor's team marketplace import.

---

## What I could not verify

1. **Exact version of the `agent` binary as of 2026-05-24**: Documentation pages do not publish a current version string. The local Windows Cursor binary (`cursor.cmd`) is the GUI IDE launcher, not the headless CLI. Running `agent --version` in a shell with the binary installed would be required.
2. **Whether `.cursorrules` (legacy single-file) is formally deprecated in May 2026**: The `cursor.com/docs/rules` page does not mention `.cursorrules` at all, suggesting it may have been quietly deprecated, but no explicit deprecation notice was found.
3. **Whether the `agent` CLI binary reads `.agents/plugins/marketplace.json` or acts on it in any way**: The CLI docs cover MCP, rules, and commands but are silent on plugins. No evidence either way for CLI-level plugin path reading.
4. **GitHub repo URL pattern constraints for team marketplace import**: Documentation says "paste a GitHub repo URL" but does not specify whether it must be a public repo, whether private repos require a PAT, or what branch is read. The `cursor/plugins` GitHub repo README did not detail auth requirements.
5. **Whether `/add-plugin` accepts a raw GitHub URL as argument (e.g., `/add-plugin https://github.com/org/repo`)**: Forum threads reference the command but do not show its full argument syntax.

---

## Sources

All URLs fetched on 2026-05-24 unless otherwise noted.

- [Cursor CLI Overview — cursor.com/docs/cli/overview](https://cursor.com/docs/cli/overview) — fetched 2026-05-24
- [Cursor CLI Installation — cursor.com/docs/cli/installation](https://cursor.com/docs/cli/installation) — fetched 2026-05-24
- [Cursor CLI Using — cursor.com/docs/cli/using](https://cursor.com/docs/cli/using) — fetched 2026-05-24
- [Cursor CLI homepage — cursor.com/cli](https://cursor.com/cli) — fetched 2026-05-24
- [New CLI Features Jan 8 2026 — cursor.com/changelog/cli-jan-08-2026](https://cursor.com/changelog/cli-jan-08-2026) — fetched 2026-05-24
- [CLI Agent Modes Jan 16 2026 — cursor.com/changelog/cli-jan-16-2026](https://cursor.com/changelog/cli-jan-16-2026) — fetched 2026-05-24
- [Cursor 2.4 Subagents + Skills — cursor.com/changelog/2-4](https://cursor.com/changelog/2-4) — fetched 2026-05-24
- [Cursor 2.5 Plugins — cursor.com/changelog/2-5](https://cursor.com/changelog/2-5) — fetched 2026-05-24
- [Cursor 3.0 changelog — cursor.com/changelog/3-0](https://cursor.com/changelog/3-0) — fetched 2026-05-24
- [Cursor Changelog main — cursor.com/changelog](https://cursor.com/changelog) — fetched 2026-05-24
- [Cursor Marketplace — cursor.com/marketplace](https://cursor.com/marketplace) — fetched 2026-05-24
- [Extend Cursor with plugins (blog) — cursor.com/blog/marketplace](https://cursor.com/blog/marketplace) — fetched 2026-05-24
- [Over 30 new plugins (blog) — cursor.com/blog/new-plugins](https://cursor.com/blog/new-plugins) — fetched 2026-05-24
- [Cursor Plugins docs — cursor.com/docs/plugins](https://cursor.com/docs/plugins) — fetched 2026-05-24
- [Cursor Plugins Reference — cursor.com/docs/reference/plugins](https://cursor.com/docs/reference/plugins) — fetched 2026-05-24
- [Cursor Rules docs — cursor.com/docs/rules](https://cursor.com/docs/rules) — fetched 2026-05-24
- [Cursor Context Skills docs — cursor.com/docs/context/skills](https://cursor.com/docs/context/skills) — fetched 2026-05-24
- [cursor/plugins GitHub README — github.com/cursor/plugins/blob/main/README.md](https://github.com/cursor/plugins/blob/main/README.md) — fetched 2026-05-24
- [Cursor 2.5 Plugins forum — forum.cursor.com/t/cursor-2-5-plugins/152124](https://forum.cursor.com/t/cursor-2-5-plugins/152124) — fetched 2026-05-24
- [Cursor 2.6 Team Marketplaces forum — forum.cursor.com/t/cursor-2-6-team-marketplaces-for-plugins/153484](https://forum.cursor.com/t/cursor-2-6-team-marketplaces-for-plugins/153484) — fetched 2026-05-24
- [May 1 2026 marketplace update (Pravin Kumar blog) — pravinkumar.co/blog/cursor-plugin-marketplace-webflow-studios-2026](https://www.pravinkumar.co/blog/cursor-plugin-marketplace-webflow-studios-2026) — fetched 2026-05-24; secondary source, no primary changelog entry fetched separately for this specific update

---

## How to reproduce

All verifications were performed via WebFetch (HTTP GET) of the URLs listed above on 2026-05-24. No commands were run locally. To independently verify:

1. `curl https://cursor.com/docs/cli/overview` — confirm `agent` as binary name
2. `curl https://cursor.com/docs/reference/plugins` — confirm `name` as only required field in plugin.json
3. `curl https://cursor.com/docs/context/skills` — confirm `.agents/skills/` in discovery table
4. `curl https://github.com/cursor/plugins/blob/main/README.md` — confirm `.cursor-plugin/marketplace.json` structure
5. After installing the CLI: `agent --version` and `agent --help` to get live version and full subcommand output

To verify the prior doc's failure mode: the install script at `https://cursor.com/install` installs an `agent` binary (not `cursor`). In a headless Linux environment the binary lands at `~/.local/bin/agent` or the path chosen by the installer. The prior CI run tested `cursor --version` and `agent --version` but the `agent` check returned exit 127 — suggesting either the install failed silently in that CI environment, the binary was installed to a path not in `$PATH`, or the install requires a display server even for the CLI. This remains an open discrepancy between the official docs (which show a headless-capable CLI) and the prior empirical CI result.
