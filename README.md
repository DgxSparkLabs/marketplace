# DgxSparkLabs Marketplace

A multi-platform marketplace of agent skills, rules, and other constructs for Claude Code, with auto-generated mirrors for Codex, Gemini, Cursor, Windsurf, and Devin. Install a single plugin and get a curated tool; install a bundle and get a whole domain. Every construct lives in one source directory and the generator propagates it to all six platforms automatically.

## Quick Start

Pick your platform, copy the block, and you're running.

### Claude Code

```bash
# In a Claude Code session — register the marketplace, then install what you want
/plugin marketplace add DgxSparkLabs/marketplace
/plugin install bundle-skill-all@dgxsparklabs-marketplace
# Or a single skill:
/plugin install skill-telegram-notify@dgxsparklabs-marketplace
# Or a rule bundle:
/plugin install bundle-quality-rules@dgxsparklabs-marketplace
```

### Codex

```bash
# Register the marketplace (reads from local clone or GitHub shortform)
codex plugin marketplace add ./
# Codex registers it as dgxsparklabs-marketplace in ~/.codex/config.toml
# Individual plugin install follows the same pattern as Claude Code
```

### Gemini

```bash
# Install an individual skill from the generated plugin directory
echo "y" | gemini skills install ./_generated/skill-telegram-notify
# Validate the extension manifest
gemini extensions validate ./.gemini/
# Install as a Gemini extension (answers the workspace-trust prompt)
echo "y" | gemini extensions install ./.gemini/ --consent
```

### Cursor

Clone the repo and open it in the Cursor IDE. Cursor auto-detects `.cursor/rules/*.md` at project open — no install command exists or is needed.

```bash
git clone https://github.com/DgxSparkLabs/marketplace
# Open the cloned directory in Cursor IDE
```

### Windsurf

Same clone-and-open pattern. Windsurf reads `.windsurf/rules/*.md` automatically.

```bash
git clone https://github.com/DgxSparkLabs/marketplace
# Open the cloned directory in Windsurf IDE
```

### Devin

Clone the repo; Devin auto-discovers skills and rules from the filesystem at session start.

```bash
git clone https://github.com/DgxSparkLabs/marketplace
# Verify what Devin sees (auth-free):
devin skills list
devin rules list
```

---

## Construct Types Available

| Type | Prefix | Description | Count |
|------|--------|-------------|-------|
| skill | `skill-` | Slash-command invoked on demand | 27 |
| rule | `rule-` | Always-on context loaded every session | 21 |
| command | `command-` | Structured agent command definitions | 1 (example) |
| agent | `agent-` | Autonomous agent configuration | 1 (example) |
| hook | `hook-` | Event-triggered automation | 1 (example) |
| mcp | `mcp-` | Model Context Protocol server config | 1 (example) |
| lsp | `lsp-` | Language Server Protocol integration | 1 (example) |
| monitor | `monitor-` | Continuous monitoring setup | 1 (example) |
| output-style | `output-style-` | Output formatting rules | 1 (example) |
| theme | `theme-` | Visual theme configuration | 1 (example) |

To add a new construct of any type, see [`docs/ADDING_A_CONSTRUCT.md`](docs/ADDING_A_CONSTRUCT.md).

---

## Installation Patterns

### Individual plugins

```bash
# Claude Code — install by prefixed name
/plugin install skill-telegram-notify@dgxsparklabs-marketplace
/plugin install skill-duckduckgo-search@dgxsparklabs-marketplace
/plugin install rule-blast-radius@dgxsparklabs-marketplace
/plugin install rule-no-ai-credit@dgxsparklabs-marketplace
/plugin install mcp-example@dgxsparklabs-marketplace
```

### Domain bundles — related items grouped

```bash
# Skill domain bundles
/plugin install bundle-communication-skills@dgxsparklabs-marketplace
/plugin install bundle-search-research-skills@dgxsparklabs-marketplace
/plugin install bundle-devops-skills@dgxsparklabs-marketplace
/plugin install bundle-session-management-skills@dgxsparklabs-marketplace
/plugin install bundle-project-scaffolding-skills@dgxsparklabs-marketplace
/plugin install bundle-code-analysis-skills@dgxsparklabs-marketplace
/plugin install bundle-meta-tooling-skills@dgxsparklabs-marketplace
/plugin install bundle-ai-services-skills@dgxsparklabs-marketplace

# Rule domain bundles
/plugin install bundle-quality-rules@dgxsparklabs-marketplace
/plugin install bundle-workflow-rules@dgxsparklabs-marketplace
/plugin install bundle-documentation-rules@dgxsparklabs-marketplace
/plugin install bundle-environment-rules@dgxsparklabs-marketplace
/plugin install bundle-notifications-rules@dgxsparklabs-marketplace
```

### Catch-all bundles — everything of one type

```bash
# Install every skill, or every rule, in a single command
/plugin install bundle-skill-all@dgxsparklabs-marketplace
/plugin install bundle-rule-all@dgxsparklabs-marketplace
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

**Notable behavior:** Installing a bundle automatically installs its member plugins as dependencies. The install output reports `(+ N dependencies: ...)`. Marketplace is registered as `dgxsparklabs-marketplace`.

**Cleanup:**

```bash
claude plugin uninstall skill-telegram-notify --scope project
claude plugin prune --scope project -y
claude plugin marketplace remove dgxsparklabs-marketplace
```

---

### Codex

**What it reads:** Reads `.claude-plugin/marketplace.json` when registered. Rules are read from `AGENTS.md`, `.cursor/rules/*.md`, and `.windsurf/rules/*.md` via filesystem — no `codex rules` subcommand exists.

**Install + use:**

```bash
# 1. Register from local clone
codex plugin marketplace add ./

# 2. Verify registration
cat ~/.codex/config.toml | grep dgxsparklabs-marketplace

# 3. List configured MCP servers
codex mcp list

# 4. Add an MCP server manually (Codex has no skills concept)
codex mcp add my-tool -- uvx mcp-server-fetch
```

**Limitations:** Codex has no `skills` subcommand. Skills are conveyed via `AGENTS.md` instructions, not named slash-commands. Plugin install uses the same `/plugin install` convention as Claude Code, but Codex plugin manifests use a different format internally.

**Cleanup:**

```bash
codex plugin marketplace remove dgxsparklabs-marketplace
```

---

### Gemini

**What it reads:** Skills from `.gemini/skills/<name>/SKILL.md` or individual install paths. Extension manifest at `.gemini/gemini-extension.json`. MCP servers from `~/.gemini/settings.json`. Rules via `GEMINI.md` and `AGENTS.md` — no `gemini rules` subcommand exists.

**Install + use:**

```bash
# Install an individual skill (our SKILL.md format is directly detected)
echo "y" | gemini skills install ./_generated/skill-telegram-notify

# List discovered skills (project + user + built-in)
gemini skills list --all

# Validate our extension manifest
gemini extensions validate ./.gemini/

# Install as a Gemini extension
echo "y" | gemini extensions install ./.gemini/ --consent

# List installed extensions (NOTE: output goes to stderr — pipe with 2>&1)
gemini extensions list 2>&1

# List configured MCP servers (NOTE: output goes to stderr — pipe with 2>&1)
gemini mcp list 2>&1
```

**Quirks:**
- `gemini extensions list` and `gemini mcp list` write all output to **stderr**, not stdout. Always pipe with `2>&1` when grepping.
- `gemini --list-extensions` (top-level flag) requires auth and exits 41. Use the `gemini extensions list` subcommand form instead — it is auth-free.
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

**What it reads:** `.cursor/rules/*.md` files with YAML frontmatter (`description`, `globs`, `alwaysApply`). Auto-detected when the directory is opened in the IDE.

**Install:** No CLI exists for Cursor. Clone the repo and open the directory in the IDE.

```bash
git clone https://github.com/DgxSparkLabs/marketplace
# Open in Cursor IDE — rules appear automatically in the rules panel
```

**Validate format (third-party, auth-free):**

```bash
npx --yes cursor-doctor@1.11.0 scan .cursor/rules/
```

**Limitations:** No headless CLI. No install command. The IDE does all the detection.

---

### Windsurf

**What it reads:** `.windsurf/rules/*.md` files with a required `trigger:` frontmatter field (`always_on`, `model_decision`, `glob`, or `manual`). Body limit: 12,000 characters per file.

**Install:** Clone and open in the Windsurf IDE. No CLI exists.

```bash
git clone https://github.com/DgxSparkLabs/marketplace
# Open in Windsurf IDE — rules auto-load from .windsurf/rules/
```

**Limitations:** No headless CLI. No install command.

---

### Devin

**What it reads:**
- Skills: `.devin/skills/<name>/SKILL.md` (project) or `~/.config/devin/skills/<name>/SKILL.md` (user)
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

**Notable behavior:** Devin reads `.cursor/rules/` and `.windsurf/rules/` natively — it sees all 21 of our rules automatically from those mirror directories. No configuration required. This is the broadest cross-platform coverage: one clone and all skills plus rules are immediately visible. `devin auth login` says "Log in to Windsurf" — Devin is built on Windsurf/Codeium infrastructure.

---

## Repository Structure

```
marketplace/
├── MARKETPLACE.toml              # Marketplace identity (owner, version, license)
├── catalog.toml                  # Bundle definitions only
├── .claude-plugin/
│   └── marketplace.json          # Generated root manifest
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
├── .codex/   .gemini/            # Cross-platform mirrors (Codex, Gemini)
├── .cursor/  .windsurf/  .devin/ # Cross-platform mirrors (Cursor, Windsurf, Devin)
├── scripts/
│   ├── generate_manifest.py      # Generator entry point (5-phase orchestrator)
│   ├── constructs.py             # 10 Construct classes
│   ├── platforms.py              # 6 Platform classes
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
| [`docs/PLATFORM_INSPECTION_CATALOG.md`](docs/PLATFORM_INSPECTION_CATALOG.md) | Empirically verified CLI commands per platform, with match-mode annotations for CI |
| [`docs/EMPIRICAL_CLI_FINDINGS/`](docs/EMPIRICAL_CLI_FINDINGS/) | Raw research notes — Devin, Gemini, Codex, Cursor, Windsurf findings |
| [`docs/PLAN_DI_REFACTOR.md`](docs/PLAN_DI_REFACTOR.md) | Generator architecture — the DI strategy-pattern design |
| [`docs/DI_REFACTOR_REPORT.md`](docs/DI_REFACTOR_REPORT.md) | What the refactor changed and why |
| [`docs/RESUME_HERE.md`](docs/RESUME_HERE.md) | Project orientation for new agents and contributors |

---

## License

MIT
