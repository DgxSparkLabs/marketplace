# DgxSparkLabs Marketplace

A multi-platform marketplace of agent skills, rules, and other constructs. Install natively on Claude Code, Codex, and Gemini with one-command GitHub fetches; import directly from GitHub into Cursor's team marketplace (IDE); or clone-and-open on Windsurf and Devin. Every construct lives in one source directory and the generator emits platform-native manifests (`.claude-plugin/`, `.codex-plugin/`, `.cursor-plugin/`) plus a shared `.agents/skills/` mirror that Windsurf, Cursor, and Devin all read natively.

> **2026-05-26 minimal-stable-state.** The marketplace currently ships **10 reference plugins (one per construct type) + 1 cross-construct examples bundle + 8 catch-all bundles = 19 plugin entries**. The 26 production skills and 21 production rules that previously shipped have been archived under `docs/archive/skills-pre-stable-2026-05-26/` and `docs/archive/rules-pre-stable-2026-05-26/`. Real content is re-added one plugin at a time after each is verified across every platform. See `CHANGELOG.md` for the full transition note.

## Table of Contents

- [GitHub-Direct Install Support](#github-direct-install-support)
- [Quick Start](#quick-start)
  - [Claude Code](#claude-code) · [Codex](#codex) · [Gemini](#gemini) · [Cursor](#cursor) · [Windsurf](#windsurf) · [Devin](#devin)
- [Construct Types Available](#construct-types-available)
- [Installation Patterns](#installation-patterns)
  - Individual plugins · Domain bundles · Catch-all bundles · Cross-construct examples bundle
- [Per-Platform Details](#per-platform-details)
  - [Claude Code](#claude-code-1) · [Codex](#codex-1) · [Gemini](#gemini-1) · [Cursor](#cursor-1) · [Windsurf](#windsurf-1) · [Devin](#devin-1)
- [Repository Structure](#repository-structure)
- [Contributing](#contributing)
- [Deep Dives](#deep-dives)
- [License](#license)

## GitHub-Direct Install Support

At-a-glance: which platforms install this marketplace directly from a GitHub URL or shortform, and which require cloning first.

| Platform | One-command GitHub install | Command / action |
|----------|---------------------------|------------------|
| Claude Code | ✅ Yes (CLI shortform) | `/plugin marketplace add DgxSparkLabs/marketplace` |
| Codex | ✅ Yes (CLI shortform) | `codex plugin marketplace add DgxSparkLabs/marketplace` |
| Gemini | ✅ Yes (CLI HTTPS URL) | `gemini extensions install https://github.com/DgxSparkLabs/marketplace --consent` |
| Cursor | ⚙️ IDE-only (paste GitHub URL) | Dashboard → Settings → Plugins → Import → paste repo URL (Cursor 2.6+) |
| Windsurf | ❌ Clone required (no CLI exists) | `git clone https://github.com/DgxSparkLabs/marketplace` then open in IDE |
| Devin | ❌ Clone required (no marketplace concept) | `git clone https://github.com/DgxSparkLabs/marketplace` then `devin skills list` |
| `agents` CLI (cross-platform) | ✅ Yes (one-line installer) | `curl -fsSL https://raw.githubusercontent.com/DgxSparkLabs/marketplace/main/install.sh \| bash` then `agents install <plugin> --scope project` |

## Quick Start

Pick your platform, copy the block, and you're running. For end-to-end management (install, list, enable/disable, uninstall, scope semantics) across all six platforms plus the `agents` CLI, see [`docs/USER_GUIDE.md`](docs/USER_GUIDE.md) — one document instead of chasing each vendor's docs separately.

### Claude Code

```bash
# In a Claude Code session — register the marketplace, then install what you want
# Install + list both work end-to-end (verified: CL1/CL2/CL3 PASS)
/plugin marketplace add DgxSparkLabs/marketplace
# One of every construct type — useful for studying every reference plugin
/plugin install bundle-examples@dgxsparklabs-marketplace
# Or a single example plugin:
/plugin install skill-example@dgxsparklabs-marketplace
# Or every plugin of one construct type (currently one each — see minimal-stable-state note above):
/plugin install bundle-skill-all@dgxsparklabs-marketplace
```

### Codex

```bash
# Register the marketplace via GitHub shortform
codex plugin marketplace add DgxSparkLabs/marketplace

# Browse what's available
codex plugin list

# Install a specific plugin
codex plugin add skill-example@dgxsparklabs-marketplace
```

### Gemini

```bash
# Install the whole marketplace as a Gemini extension directly from GitHub (no clone required)
gemini extensions install https://github.com/DgxSparkLabs/marketplace --consent

# Verify the extension is registered (note: list output goes to stderr — pipe with 2>&1)
gemini extensions list 2>&1

# List discovered skills (project + user + built-in)
gemini skills list --all 2>&1

# Or, from a local clone (still works):
echo "y" | gemini extensions install ./.gemini/ --consent
```

### Cursor

```bash
# Path 1: Cursor team marketplace (Cursor 2.6+, admin Dashboard import)
#   Dashboard → Settings → Plugins → Import → paste GitHub repo URL → save
#   Requires .cursor-plugin/marketplace.json at repo root (present in this repo)
#   See: https://cursor.com/docs/plugins

# Path 2: Clone + open (works for all Cursor versions)
git clone https://github.com/DgxSparkLabs/marketplace
# Open the cloned directory in Cursor IDE
# Rules auto-load from .cursor/rules/; skills auto-load from .agents/skills/

# Note: the Cursor CLI ('agent' binary) exists but has NO plugin install commands.
# Install Cursor CLI (macOS/Linux/WSL): curl https://cursor.com/install -fsS | bash
# Install Cursor CLI (Windows PowerShell): irm 'https://cursor.com/install?win32=true' | iex
```

### Windsurf

```bash
# Clone and open in Windsurf IDE
git clone https://github.com/DgxSparkLabs/marketplace
# Rules auto-load from .windsurf/rules/
# Skills auto-load from .agents/skills/ (per Windsurf Cascade docs)
# Invoke any skill via @skill-name in Cascade chat
```

### Devin

Clone the repo; Devin auto-discovers skills and rules from the filesystem at session start.

```bash
git clone https://github.com/DgxSparkLabs/marketplace
# Verify what Devin sees (auth-free):
devin skills list
devin rules list
```

Note: skills come from `.agents/skills/` — Devin reads it natively. The legacy `.devin/skills/` mirror was retired 2026-05-25 (verified empirically); no migration needed.

### Cross-platform: `agents` CLI

For any platform where you'd rather drive installs from a shell than rely on each tool's native installer, the `agents` CLI ships a small Python shim that installs a plugin into `.agents/<construct>/` (the shared convergence path) and, optionally, every per-platform path (`.cursor/`, `.windsurf/`, `.gemini/`, `.codex/`, `.claude/`) in one command.

```bash
# POSIX one-liner installer (drops `agents` into ~/.local/bin/)
curl -fsSL https://raw.githubusercontent.com/DgxSparkLabs/marketplace/main/install.sh | bash

# Windows PowerShell one-liner
irm https://raw.githubusercontent.com/DgxSparkLabs/marketplace/main/install.ps1 | iex

# Install a skill into the current project (.agents/ + per-platform paths)
agents install skill-telegram-notify --scope project

# Strict mode — write only to .agents/, skip per-platform spray
agents install rule-blast-radius --scope project --agents-only

# Install for the user (~/.agents/ only)
agents install agent-example --scope user

# Browse what's available
agents list --available

# Remove
agents uninstall skill-telegram-notify --scope project
```

The CLI supports all `.agents/` constructs (skill, rule, agent, hook, mcp, command). Claude-only constructs (lsp, monitor, output-style, theme) install via `claude plugin install` as before.

---

## Construct Types Available

Every construct type currently ships exactly one reference plugin (the `example/` source dir). Production skills and rules were archived 2026-05-26 — see the minimal-stable-state note above and `CHANGELOG.md`.

| Type | Prefix | Description | Count |
|------|--------|-------------|-------|
| [skill](skills/) | `skill-` | Slash-command invoked on demand | 1 (example) |
| [rule](rules/) | `rule-` | Always-on context loaded every session | 1 (example) |
| [command](commands/) | `command-` | Structured agent command definitions | 1 (example) |
| [agent](agents/) | `agent-` | Autonomous agent configuration | 1 (example) |
| [hook](hooks/) | `hook-` | Event-triggered automation | 1 (example) |
| [mcp](mcp-servers/) | `mcp-` | Model Context Protocol server config | 1 (example) |
| [lsp](lsp-servers/) | `lsp-` | Language Server Protocol integration | 1 (example) |
| [monitor](monitors/) | `monitor-` | Continuous monitoring setup | 1 (example) |
| [output-style](output-styles/) | `output-style-` | Output formatting rules | 1 (example) |
| [theme](themes/) | `theme-` | Visual theme configuration | 1 (example) |

To add a new construct of any type, see [`docs/ADDING_A_CONSTRUCT.md`](docs/ADDING_A_CONSTRUCT.md).

---

## Installation Patterns

These examples show Claude Code's `/plugin install` slash-command syntax (most expressive). Equivalent commands exist for Codex (`codex plugin add <name>@dgxsparklabs-marketplace`) and Gemini (`gemini extensions install` for the whole marketplace, or `gemini skills install` for individual skills). See [Per-Platform Details](#per-platform-details) for each platform's exact command form.

### Individual plugins

```bash
# Claude Code — install by prefixed name
/plugin install skill-example@dgxsparklabs-marketplace
/plugin install command-example@dgxsparklabs-marketplace
/plugin install hook-example@dgxsparklabs-marketplace
/plugin install mcp-example@dgxsparklabs-marketplace
```

### Domain bundles — related items grouped

> **2026-05-26 minimal-stable-state.** The 8 skill domain bundles and 5 rule domain bundles that previously lived here were removed alongside the source archive (see CHANGELOG). They will be re-introduced one at a time as production skills and rules return to the marketplace. The cross-construct `bundle-examples` is still available for studying every construct type from a single install.

### Catch-all bundles — everything of one type

```bash
# Each catch-all currently installs the one example for its construct type.
# As production plugins return, each catch-all grows to match.
/plugin install bundle-skill-all@dgxsparklabs-marketplace
/plugin install bundle-command-all@dgxsparklabs-marketplace
# (Catch-alls exist for every Claude-supported construct: skill, command,
# agent, hook, mcp, lsp, monitor, output-style, theme. There is no
# bundle-rule-all — rules are not a Claude plugin component per F8.)
```

### Cross-construct examples bundle — study all 10 construct types

```bash
# One of each construct type, useful for contributors and integrators
/plugin install bundle-examples@dgxsparklabs-marketplace
```

---

## Per-Platform Details

### Claude Code

**What it reads:** `.claude-plugin/marketplace.json` (root manifest) and `_generated/<plugin>/.claude-plugin/plugin.json` (per-plugin).

**Install + use:**

```bash
# 1. Register the marketplace (GitHub shortform or local path both work)
claude plugin marketplace add DgxSparkLabs/marketplace
# or from a local clone:
claude plugin marketplace add ./

# 2. Browse what's available
claude plugin list --json --available

# 3. Install a plugin
claude plugin install skill-telegram-notify@dgxsparklabs-marketplace --scope project

# 4. Verify it's installed
claude plugin list

# 5. Inspect plugin details
claude plugin details skill-telegram-notify
```

**Notable behavior:** Installing a bundle automatically installs its member plugins as dependencies. The install output reports `(+ N dependencies: ...)`. Marketplace is registered as `dgxsparklabs-marketplace`. Install + list both verified end-to-end (CL1/CL2/CL3 PASS).

**Cleanup:**

```bash
claude plugin uninstall skill-telegram-notify --scope project
claude plugin prune --scope project -y
claude plugin marketplace remove dgxsparklabs-marketplace
```

---

### Codex

**What it reads:** Reads `.claude-plugin/marketplace.json` for marketplace registration. Per-plugin install reads `_generated/<plugin>/.codex-plugin/plugin.json` (emitted by the generator for every construct type in `CodexPlatform.supports`). Rules are read from `AGENTS.md`, `.cursor/rules/*.md`, and `.windsurf/rules/*.md` via filesystem.

**Install + use:**

```bash
# 1. Register the marketplace via GitHub shortform
codex plugin marketplace add DgxSparkLabs/marketplace

# Or from a local clone:
codex plugin marketplace add ./

# 2. Browse what's available
codex plugin list

# 3. Install a specific plugin (requires .codex-plugin/plugin.json per plugin — present post-Phase-1)
codex plugin add skill-telegram-notify@dgxsparklabs-marketplace

# 4. List configured MCP servers
codex mcp list

# 5. Add an MCP server manually
codex mcp add my-tool -- uvx mcp-server-fetch
```

**How per-plugin install works:** Each `_generated/<plugin>/` directory now contains `.codex-plugin/plugin.json` alongside `.claude-plugin/plugin.json`. Codex reads its own manifest; Claude reads its own. The per-plugin Codex manifest includes a construct-type pointer (`skills: "./skills/"` for skills, `mcpServers: "./mcp.json"` for MCP, `hooks: "./hooks/hooks.json"` for hooks).

**Cleanup:**

```bash
codex plugin marketplace remove dgxsparklabs-marketplace
```

---

### Gemini

**What it reads:** Skills from `.gemini/skills/<name>/SKILL.md` or individual install paths. Extension manifest at `.gemini/gemini-extension.json` (for local installs) and `gemini-extension.json` at repo root (for GitHub URL installs — both files are byte-identical). MCP servers from `~/.gemini/settings.json`. Rules via `GEMINI.md` and `AGENTS.md`.

**Install + use:**

```bash
# Install directly from GitHub (no clone required)
gemini extensions install https://github.com/DgxSparkLabs/marketplace --consent

# Verify the extension is registered (NOTE: output goes to stderr — pipe with 2>&1)
gemini extensions list 2>&1

# List discovered skills (project + user + built-in)
gemini skills list --all 2>&1

# Or, from a local clone (still works):
echo "y" | gemini extensions install ./.gemini/ --consent

# List configured MCP servers (NOTE: output goes to stderr — pipe with 2>&1)
gemini mcp list 2>&1
```

**Quirks:**
- `gemini extensions list` and `gemini mcp list` write all output to **stderr**, not stdout. Always pipe with `2>&1` when grepping.
- `gemini --list-extensions` (top-level flag) requires auth and exits 41. Use the `gemini extensions list` subcommand form instead — it is auth-free.
- The `gemini-extension.json` at the repo root is byte-identical to `.gemini/gemini-extension.json`. The root copy exists solely to enable GitHub-URL install (`gemini extensions install <github-url>` expects the file at the cloned repo root).
- No marketplace concept: skills and extensions are installed individually.
- Gemini reports `Skipping project agents due to untrusted folder` until the workspace is trusted.

**Cleanup:**

```bash
gemini skills uninstall telegram-notify
gemini extensions uninstall dgxsparklabs-marketplace
gemini mcp remove <name>
```

---

### Cursor

**What it reads:** `.cursor/rules/*.md` files with YAML frontmatter (`description`, `globs`, `alwaysApply`). Skills from `.agents/skills/<name>/SKILL.md` (primary project-level skill path per Cursor docs). Auto-detected when the directory is opened in the IDE.

**Install paths:**

**Path 1 — Cursor team marketplace (Cursor 2.6+, admin only):**
Import via Dashboard: Settings → Plugins → Import → paste the GitHub repo URL → save. This uses `.cursor-plugin/marketplace.json` at the repo root (present post-Phase-1). See: https://cursor.com/docs/plugins

**Path 2 — Clone and open (all Cursor versions):**

```bash
git clone https://github.com/DgxSparkLabs/marketplace
# Open in Cursor IDE — rules appear automatically in the rules panel
# Skills are available from .agents/skills/ via @skill-name
```

**Cursor CLI (`agent` binary):**

The `agent` CLI exists but has no plugin install commands. It is useful for interactive sessions only.

```bash
# Install (macOS/Linux/WSL):
curl https://cursor.com/install -fsS | bash

# Install (Windows PowerShell):
irm 'https://cursor.com/install?win32=true' | iex

# Verify:
agent --version
```

Available commands: `install-shell-integration`, `login`, `logout`, `mcp`, `worker`, `models`, `create-chat`, `generate-rule`, `agent`, and others. No `plugin install`, `plugin list`, or `marketplace` subcommands exist. The `--plugin-dir <path>` flag loads a local plugin directory at runtime (not a persistent install).

**Validate rule format (third-party, auth-free):**

```bash
npx --yes cursor-doctor@1.11.0 scan .cursor/rules/
```

---

### Windsurf

**What it reads:** `.windsurf/rules/*.md` files with a required `trigger:` frontmatter field (`always_on`, `model_decision`, `glob`, or `manual`). Body limit: 12,000 characters per file. Skills from `.windsurf/skills/<name>/SKILL.md` AND `.agents/skills/<name>/SKILL.md` — both auto-discovered by Windsurf Cascade (per `docs.windsurf.com/windsurf/cascade/skills`).

**Install:** Clone and open in the Windsurf IDE. No CLI exists.

```bash
git clone https://github.com/DgxSparkLabs/marketplace
# Open in Windsurf IDE
# Rules auto-load from .windsurf/rules/
# Skills auto-load from .agents/skills/ (per Windsurf Cascade docs)
# Invoke any skill via @skill-name in Cascade chat
```

**Skills story:** The generator emits `.agents/skills/<name>/SKILL.md` for every skill via `AgentsPlatform`. Windsurf Cascade picks these up automatically. As of 2026-05-26 the marketplace ships one example skill; production skills return one at a time from `docs/archive/skills-pre-stable-2026-05-26/` as each is re-verified.

**Limitations:** No headless CLI. No install command.

---

### Devin

**What it reads:**
- Skills: `.devin/skills/<name>/SKILL.md` (project) AND `.agents/skills/<name>/SKILL.md` — Devin reads both paths natively
- Rules: `.windsurf/rules/*.md`, `.cursor/rules/*.md`, `.cursorrules`, `AGENTS.md` — all read natively

**Install + use:**

```bash
# Install the Devin CLI
curl -fsSL https://cli.devin.ai/install.sh | bash || true
# (the installer exits 1 in non-TTY but the binary lands at ~/.local/bin/devin)

# Clone the marketplace
git clone https://github.com/DgxSparkLabs/marketplace
cd marketplace

# Verify what Devin sees (all auth-free)
devin skills list
devin rules list
devin mcp list

# Check where Devin scans for skills and rules
devin skills paths
devin rules paths
```

**Notable behavior:** Devin reads `.cursor/rules/` and `.windsurf/rules/` natively — every rule emitted to those mirror directories is auto-discovered (the marketplace currently ships the one example rule). Skills come from both `.devin/skills/` and `.agents/skills/`; the `.agents/skills/` path is the cross-platform convergence point shared with Windsurf and Cursor. `devin auth login` says "Log in to Windsurf" — Devin is built on Windsurf/Codeium infrastructure.

---

## Repository Structure

```
marketplace/
├── MARKETPLACE.toml              # Marketplace identity (owner, version, license)
├── catalog.toml                  # Bundle definitions only
├── gemini-extension.json         # Root-level copy for gemini extensions install <github-url>
├── .claude-plugin/
│   └── marketplace.json          # Generated root manifest
├── .cursor-plugin/
│   └── marketplace.json          # Cursor team-marketplace manifest (Cursor 2.6+)
├── skills/                       # Source skill directories (one per skill)
├── rules/                        # Source rule directories (one per rule)
├── commands/                     # Command construct sources
├── agents/                       # Agent construct sources
├── hooks/                        # Hook construct sources
├── mcp-servers/                  # MCP server construct sources
├── lsp-servers/                  # LSP server construct sources
├── monitors/                     # Monitor construct sources
├── output-styles/                # Output style construct sources
├── themes/                       # Theme construct sources
├── _generated/                   # Generated plugin wrappers + bundles
├── .agents/
│   └── skills/                   # Cross-platform skills mirror (Windsurf, Cursor, Devin)
├── .codex/   .gemini/            # Cross-platform mirrors (Codex, Gemini)
├── .cursor/  .windsurf/  .devin/ # Cross-platform mirrors (Cursor, Windsurf, Devin)
├── scripts/
│   ├── generate_manifest.py      # Generator entry point (6-phase orchestrator)
│   ├── constructs.py             # 10 Construct classes
│   ├── platforms.py              # 7 Platform classes (incl. AgentsPlatform)
│   ├── bundles.py                # Bundle + BundleMember dataclasses
│   └── utils.py                  # Shared helpers
└── docs/                         # Architecture docs, platform findings, plans
```

Mirrors are regenerated by running:

```bash
uv run scripts/generate_manifest.py
```

---

## Contributing

To add a new construct, see [`docs/ADDING_A_CONSTRUCT.md`](docs/ADDING_A_CONSTRUCT.md). The guide covers all 10 construct types with a step-by-step checklist per type.

---

## Deep Dives

| Document | Purpose |
|----------|---------|
| [`docs/USER_GUIDE.md`](docs/USER_GUIDE.md) | End-user reference for managing plugins/extensions (install, list, enable/disable, uninstall, scope) across all 6 platforms + the `agents` CLI |
| [`docs/PLATFORMS.md`](docs/PLATFORMS.md) | Per-platform install, support, discovery, and CI reference (Claude/Codex/Gemini/Cursor/Windsurf/Devin/Agents) |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | Generator architecture — Construct/Platform/Bundle protocols, generation phases |
| [`docs/RESUME_HERE.md`](docs/RESUME_HERE.md) | Project orientation for new agents and contributors |
| [`docs/archive/phase-2-validation/PLATFORM_INSPECTION_CATALOG.md`](docs/archive/phase-2-validation/PLATFORM_INSPECTION_CATALOG.md) | Empirically verified CLI commands per platform, with match-mode annotations for CI (historical reference) |
| [`docs/archive/empirical-cli-findings/`](docs/archive/empirical-cli-findings/) | Raw research notes — Devin, Gemini, Codex, Cursor, Windsurf findings (historical) |
| [`docs/archive/di-refactor/PLAN_DI_REFACTOR.md`](docs/archive/di-refactor/PLAN_DI_REFACTOR.md) | DI strategy-pattern design — 25 locked decisions (Phase 4, historical) |
| [`docs/archive/di-refactor/DI_REFACTOR_REPORT.md`](docs/archive/di-refactor/DI_REFACTOR_REPORT.md) | What the refactor changed and why (Phase 4, historical) |

---

## License

MIT
