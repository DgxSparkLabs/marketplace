---
date: 2026-05-24
purpose: per-platform reference (install, discovery, support, CI assertions, gaps)
status: live
---

# Platforms

This marketplace targets six AI coding platforms — Claude Code, Codex, Gemini, Cursor, Windsurf, and Devin. Three of them (Claude, Codex, Gemini) support a one-command GitHub install; the other three install via IDE import or `git clone`. A shared `.agents/skills/` directory is read natively by Windsurf, Cursor, and Devin — the only true cross-platform convergence point. For end-user install commands, start with `README.md`. This document is the canonical reference for how each platform installs, how it discovers content, what the CI workflows assert about it, and where the gaps are.

## How to read these docs

This file is one of three hub docs in the pyramid:

- `README.md` — user-facing entry point (install + Quick Start)
- `[[PLATFORMS]]` (this file) — per-platform reference
- `[[ARCHITECTURE]]` — how the generator produces these per-platform outputs
- `[[CONTRIBUTING]]` — how to add things and test

The four detail-reference docs ([[ADDING_A_CONSTRUCT]], [[CONSTRUCT_TYPES]], [[RULE_FORMAT]], [[SKILL_FORMAT]]) sit one level down. Master docs link to them rather than duplicating their content.

## At a glance

| Platform | Install command (one-liner) | Native CLI? | Plugin install via CLI? | Skills auto-discovery? | Status |
|---|---|:--:|:--:|:--:|---|
| Claude Code | `/plugin marketplace add DgxSparkLabs/marketplace` | yes | yes (9 of 10 constructs — rules via filesystem) | via plugin install | fully working |
| Codex | `codex plugin marketplace add DgxSparkLabs/marketplace` | yes | yes | via plugin install | fully working |
| Gemini | `gemini extensions install https://github.com/DgxSparkLabs/marketplace --consent` | yes | extensions, not plugins | `.gemini/skills/` (via extension) | fully working |
| Cursor | Dashboard → Settings → Plugins → Import → paste GitHub URL | yes (`agent`) | no — IDE-only install | `.agents/skills/` | IDE install only |
| Windsurf | `git clone` + open in IDE | no | n/a | `.agents/skills/` | clone-only |
| Devin | `git clone` + `devin skills list` | yes | n/a (no marketplace) | `.agents/skills/` | clone-only |

Sources: [[archive/phase-5-cross-platform-install/VERIFICATION_2026-05/SUMMARY#Per-platform install story (what's true today)]] (Claude/Codex/Gemini), [[archive/phase-5-cross-platform-install/VERIFICATION_2026-05/cursor#Executive summary]] (Cursor), [[archive/empirical-cli-findings/windsurf]] (Windsurf), [[archive/empirical-cli-findings/devin]] (Devin).

---

## Claude Code

### What it is

Anthropic's official CLI agent. The marketplace's canonical platform — every other platform's emission is derived from the Claude-shaped per-plugin manifest.

### Install path

#### From GitHub (default branch)

```bash
# Register the marketplace
claude plugin marketplace add DgxSparkLabs/marketplace

# Install a plugin
claude plugin install skill-telegram-notify@dgxsparklabs-marketplace --scope project

# Verify
claude plugin list
```

The shortform `owner/repo` form, an explicit `https://github.com/...` URL, and a local path all work. Verified PASS for the local-path variant in [[archive/phase-5-cross-platform-install/VERIFICATION_2026-05/empirical_act_verification#Claude Code]] (CL1 — `Successfully added marketplace: dgxsparklabs-marketplace`).

#### From GitHub (specific branch)

Claude's `claude plugin marketplace add` does not document a `--ref` flag in any captured CLI output. Branch-specific install for Claude Code is **not verified** in this repo's evidence; use the default-branch form or a local clone of the target branch.

#### From local clone

```bash
git clone https://github.com/DgxSparkLabs/marketplace
cd marketplace
claude plugin marketplace add ./
claude plugin install skill-telegram-notify@dgxsparklabs-marketplace --scope project
```

Verified PASS in [[archive/phase-5-cross-platform-install/VERIFICATION_2026-05/empirical_act_verification#Claude Code]] (CL1, CL2, CL3). The cache lands at `~/.claude/plugins/cache/dgxsparklabs-marketplace/<plugin>/<version>/`.

### Discovery commands

| Command | What it lists | Example output |
|---|---|---|
| `claude plugin marketplace list` | All registered marketplaces | After registration: `❯ dgxsparklabs-marketplace / Source: Directory (/mnt/c/Users/devic/source/marketplace)` (from `logs/CL1.txt`) |
| `claude plugin list` | Installed plugins, with version + scope + enable state | `❯ skill-example@dgxsparklabs-marketplace / Version: 1.0.0 / Scope: project / Status: ✔ enabled` (from `logs/CL3.txt`) |
| `claude plugin list --json` | Same, machine-readable | JSON: `{"installed": [...], "available": [...]}` — exit 0 even with no installs |
| `claude plugin list --json --available` | Installed + every available plugin across registered marketplaces | All entries from this marketplace appear (19 as of 2026-05-26 minimal-stable-state; was 81 before the archive) |
| `claude plugin details <name>` | Component inventory + projected token cost for one plugin | Text table; missing-plugin response: `Plugin "..." not found.` |
| `claude plugin validate <path>` | Plugin manifest correctness | `✔ Validation passed` (or `with warnings`); enforces kebab-case names for Claude.ai sync |

### Per-plugin install

```bash
claude plugin install bundle-skill-all@dgxsparklabs-marketplace --scope project
```

Bundles auto-install their dependencies. The install output reports `(+ N dependencies: ...)`. Uninstalling a bundle does NOT auto-remove its deps — they orphan and persist until `claude plugin prune --scope <scope> -y`.

### What constructs it supports

| Construct | Supported | Notes |
|---|:--:|---|
| skill | yes | installed via `/plugin install`; activates immediately |
| rule | **NO (filesystem-only)** | Rules are not a Claude plugin component per `code.claude.com/docs/en/plugins-reference#plugin-components-reference` (fetched 2026-05-26). Claude consumes rules via its memory subsystem at `.claude/rules/*.md` (project) and `~/.claude/rules/*.md` (user) per `code.claude.com/docs/en/memory#organize-rules-with-claude-rules`. `RuleConstruct` was removed from `ClaudeCodePlatform.supports` on 2026-05-26 — see "Claude rule discovery" below for the install path. |
| command, agent, hook, mcp, lsp, monitor, output-style, theme | yes | native plugin install |

Nine construct types declared in `ClaudeCodePlatform.supports` at `scripts/platforms.py:128-132` (RuleConstruct intentionally absent — see the inline comment at `scripts/platforms.py:112-123`).

### Claude rule discovery

After the 2026-05-26 deprecation, no `rule-<name>` plugins surface in Claude's marketplace listing. Operators install rules from this marketplace into Claude's memory subsystem directly:

```bash
# Project scope — symlink (live updates as the rule file changes upstream)
mkdir -p .claude/rules
ln -s "$(pwd)/rules/blast-radius/rule.md" .claude/rules/blast-radius.md

# Or copy for portability
cp rules/blast-radius/rule.md .claude/rules/blast-radius.md

# User scope (apply to every project on this machine)
mkdir -p ~/.claude/rules
cp rules/blast-radius/rule.md ~/.claude/rules/blast-radius.md
```

The `agents` CLI shim automates the per-marketplace install when targeted at `.agents/rules/` (`agents install rule-blast-radius --scope project --agents-only`), but Claude does not currently auto-discover from `.agents/rules/` — for Claude specifically the symlink-or-copy approach above is canonical. See `docs/USER_GUIDE.md` Claude section for the full operator walkthrough.

**Claude-side bundle cascade**: bundles whose members are exclusively `rule:` references (`bundle-quality-rules`, `bundle-workflow-rules`, `bundle-documentation-rules`, `bundle-environment-rules`, `bundle-notifications-rules`) and the catch-all `bundle-rule-all` are no longer surfaced in Claude's marketplace listing because their dependencies are no longer valid Claude plugins. They remain available to Cursor / Codex / Gemini / Windsurf where rule plugins are still valid.

Source `rules/<name>/` directories remain — they still feed Cursor / Windsurf / Codex / Gemini rule emission. Cursor and Codex per-plugin manifests still surface them. Only the Claude-plugin wrapping is gone.

### Discovery paths it reads

- `.claude-plugin/marketplace.json` at the repo root (marketplace manifest)
- `_generated/<plugin>/.claude-plugin/plugin.json` (per-plugin manifest, one per Claude-installable plugin)
- Cache: `~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/` (versioned subdirs)

### CI assertions

| Workflow | What it asserts |
|---|---|
| `compat-marketplace-add.yml` (claude job) | `claude plugin marketplace add ./` exits 0; `claude plugin marketplace list \| grep -F dgxsparklabs-marketplace` matches; per-plugin `install skill-example` succeeds; `plugin list \| grep -F skill-example` matches |
| `compat-skill.yml` (claude job) | Installs `skill-telegram-notify`; `claude plugin list \| grep -F "skill-telegram-notify@dgxsparklabs-marketplace"` matches |
| `compat-agent.yml` (claude job) | Installs `agent-example`; `claude plugin details agent-example \| grep -F notebook-reviewer` matches |
| `compat-command.yml` (claude job) | Installs `command-example`; both `plugin list` and `plugin details` grep-match the name |
| `compat-hook.yml` (claude job) | Installs `hook-example`; `claude plugin details hook-example \| grep -F UserPromptSubmit` matches |
| `compat-mcp.yml` (claude job) | Installs `mcp-example`; `claude plugin details mcp-example \| grep -iF mcp` matches (case-insensitive; output is human-readable text, not JSON) |
| `compat-monitor.yml`, `compat-output-style.yml`, `compat-theme.yml` (claude jobs) | Each installs the corresponding `*-example` plugin and asserts it appears in both `plugin list` and `plugin details` |

All cleanup steps run `claude plugin uninstall <name> --scope project || true` then `claude plugin prune --scope project -y || true`.

### Known gaps

- **Branch-specific install not documented.** The `claude plugin marketplace add` CLI surface as captured in our act logs has no `--ref` equivalent. If you need a specific branch, clone first and add `./`.

### Out-of-scope or non-applicable

- Skill auto-discovery from `.agents/skills/` — Claude Code installs explicitly via `/plugin install` rather than auto-loading from filesystem paths.

### References

- [[archive/phase-5-cross-platform-install/VERIFICATION_2026-05/SUMMARY#Per-platform install story (what's true today)]] — install status table
- [[archive/phase-5-cross-platform-install/VERIFICATION_2026-05/empirical_act_verification#Claude Code]] — per-claim CL1/CL2/CL3 evidence
- [[INVESTIGATION_PLUGIN_DEPENDENCIES#Result]] — proof that bundle dependencies auto-install
- [[RULE_FORMAT]] — rule install workaround details

---

## Codex

### What it is

OpenAI's terminal coding agent. Installs via `npm install -g @openai/codex`. Reuses Claude's `.claude-plugin/marketplace.json` for marketplace registration (legacy-compatible) and reads its own `.codex-plugin/plugin.json` per plugin.

### Install path

#### From GitHub (default branch)

```bash
npm install -g @openai/codex
codex plugin marketplace add DgxSparkLabs/marketplace
codex plugin list
codex plugin add skill-telegram-notify@dgxsparklabs-marketplace
```

Works post-merge on `main` (the merged branch contains `.claude-plugin/marketplace.json` and the per-plugin `.codex-plugin/plugin.json` manifests Codex requires). The post-merge verification log captures `Added marketplace 'dgxsparklabs-marketplace' from https://github.com/DgxSparkLabs/marketplace.git. C2_EXIT=0` (from `logs/post-merge-c2-verification.log`). Pre-merge against `main` the no-ref form failed with `marketplace root does not contain a supported manifest` — see C2 in [[archive/phase-5-cross-platform-install/VERIFICATION_2026-05/empirical_act_verification#Codex]].

#### From GitHub (specific branch)

```bash
codex plugin marketplace add DgxSparkLabs/marketplace --ref feat/some-branch
```

The `--ref <branch>` flag is verified working. From `logs/C3.txt`: `Added marketplace 'dgxsparklabs-marketplace' from https://github.com/DgxSparkLabs/marketplace.git#feat/claude-plugin-compliance. Installed marketplace root: /root/.codex/.tmp/marketplaces/dgxsparklabs-marketplace. C3_EXIT=0`.

#### From local clone

```bash
git clone https://github.com/DgxSparkLabs/marketplace
cd marketplace
codex plugin marketplace add ./
codex plugin list
codex plugin add skill-example@dgxsparklabs-marketplace
```

Verified PASS in [[archive/phase-5-cross-platform-install/VERIFICATION_2026-05/empirical_act_verification#Codex]] (C1 for marketplace add; C4 for enumeration; C5 for per-plugin install after the Phase 1.5 manifest fix landed — see `logs/C5-post.txt`). After registration, `~/.codex/config.toml` contains a `[marketplaces.dgxsparklabs-marketplace]` block with `source_type = "local"` and the local path.

### Discovery commands

| Command | What it lists | Example output |
|---|---|---|
| `codex plugin list` | Every plugin in every registered marketplace, with install status | `PLUGIN ... STATUS ... VERSION ... PATH` table; e.g. `skill-example@dgxsparklabs-marketplace ... not installed` (from `logs/C4.txt`; full 81-row enumeration in `logs/post-implementation-codex.log`) |
| `cat ~/.codex/config.toml` | Registered marketplaces (no dedicated `marketplace list` subcommand) | `[marketplaces.dgxsparklabs-marketplace] / last_updated = "..." / source_type = "local" / source = "..."` (from `logs/C1.txt`) |
| `codex mcp list` | Configured MCP servers from `~/.codex/config.toml` | Empty-state: `No MCP servers configured yet. Try \`codex mcp add my-tool -- my-command\`.` |
| `codex mcp get <name>` | One MCP server detail; supports `--json` | Text or JSON; missing: `error: MCP server '<name>' not found` |
| `codex --help` | Full subcommand surface | 21 commands listed (output format: text) |
| `codex features list` | Feature flag table | 80+ rows of `feature_name  stage  bool` (catalog is binary-bundled) |
| `codex login status` | Auth state | `Not logged in.` or `Logged in as <user>` — auth-free even when unauthenticated |

### Per-plugin install

```bash
codex plugin add skill-telegram-notify@dgxsparklabs-marketplace
```

Reads `_generated/<plugin>/.codex-plugin/plugin.json` (emitted by generator Phase 1.5; gated on `CodexPlatform.supports = {SkillConstruct, MCPConstruct, HookConstruct}`). Plugins of unsupported construct types (themes, agents, output styles) appear in `codex plugin list` but install would fail — they're not in Codex's `supports` set so no `.codex-plugin/plugin.json` is emitted.

### What constructs it supports

| Construct | Supported | Notes |
|---|:--:|---|
| skill | yes (manifest-only) | `_generated/skill-*/.codex-plugin/plugin.json` emits `"skills": "./skills/"` pointer. Skill mirror retired 2026-05-25 (D-1) — Codex reads skills via the per-plugin manifest, not a repo-root `.codex/skills/` tree. |
| mcp | yes | manifest emits `"mcpServers": "./mcp.json"` |
| hook | yes | manifest emits `"hooks": "./hooks/hooks.json"` |
| agent | yes | `.codex/agents/<name>.toml` per `developers.openai.com/codex/subagents/` (2026-05-25). Source is Claude-style markdown (D-16); converted at emit time by `scripts/converters/md_to_toml.py`. |
| rule, command, lsp, monitor, output-style, theme | no | Codex reads rules from `AGENTS.md`, `.cursor/rules/*.md`, `.windsurf/rules/*.md` directly; other constructs are Claude-specific |

`CodexPlatform.supports = {SkillConstruct, MCPConstruct, HookConstruct, AgentConstruct}` at `scripts/platforms.py:150`.

### Discovery paths it reads

- `.claude-plugin/marketplace.json` (legacy-compatible marketplace manifest)
- `.agents/plugins/marketplace.json` (Codex canonical path per `developers.openai.com/codex/plugins/build`, 2026-05-25 — emitted by Phase 5.5, byte-identical to the legacy path)
- `_generated/<plugin>/.codex-plugin/plugin.json` (per-plugin manifest)
- `.codex/agents/<name>.toml` (sub-agent definitions, Unit 4)
- `AGENTS.md`, `.cursor/rules/*.md`, `.windsurf/rules/*.md` for rule context
- Config: `~/.codex/config.toml`

### CI assertions

| Workflow | What it asserts |
|---|---|
| `compat-marketplace-add.yml` (codex job) | `codex plugin marketplace add ./` exits 0; `cat ~/.codex/config.toml \| grep -F dgxsparklabs-marketplace` matches; `codex plugin list \| grep -F "skill-example@dgxsparklabs-marketplace"` matches; `codex plugin add skill-example@dgxsparklabs-marketplace` exits 0 |
| `compat-skill.yml` (codex job) | Registers marketplace from local path; asserts entry appears in `~/.codex/config.toml` |
| `compat-mcp.yml` (codex job) | `codex mcp list` baseline exits 0; `codex mcp add example -- uvx mcp-server-fetch` succeeds; `codex mcp list \| grep -F example` matches; `codex mcp get example --json` exits 0 |

All Codex jobs run with `continue-on-error: false` (promoted from advisory to required after Wave 4 verification that the GitHub Actions org-level block on `@openai/codex` was lifted).

### Known gaps

- **Pre-merge branch state required `--ref`.** Pre-merge, `codex plugin marketplace add DgxSparkLabs/marketplace` failed (C2) and required `--ref feat/claude-plugin-compliance` (C3). Post-merge on `main` the no-ref form works. See [[archive/phase-5-cross-platform-install/VERIFICATION_2026-05/SUMMARY#Finding 1: The `.agents/` directory is a real convergence — but only for content, not for marketplaces]].
- **`codex plugin marketplace list` doesn't exist.** Codex has `add`, `upgrade`, `remove` but no list subcommand. Inspect `~/.codex/config.toml` directly to see registered marketplaces.

### Out-of-scope or non-applicable

- The canonical `.agents/plugins/marketplace.json` path is supported by Codex but not adopted here — `.claude-plugin/marketplace.json` is accepted legacy-compatibly. See [[archive/phase-5-cross-platform-install/VERIFICATION_2026-05/SUMMARY#Finding 1: The `.agents/` directory is a real convergence — but only for content, not for marketplaces]].

### References

- [[archive/phase-5-cross-platform-install/VERIFICATION_2026-05/empirical_act_verification#Codex]] — C1-C7 per-claim table
- [[archive/empirical-cli-findings/codex]] — npm package metadata, config locations
- [[ARCHITECTURE#The `supports` gate]] — how per-platform manifest emission is gated

---

## Gemini

### What it is

Google's CLI agent (`npm install -g @google/gemini-cli`). Uses "extensions" (not "plugins") as its installation unit. The whole marketplace installs as one extension via the GitHub URL.

### Install path

#### From GitHub (default branch)

```bash
npm install -g @google/gemini-cli
gemini extensions install https://github.com/DgxSparkLabs/marketplace --consent
gemini extensions list 2>&1
gemini skills list --all 2>&1
```

Works because the generator emits `gemini-extension.json` at the repo root (Phase 4.5, `scripts/generate_manifest.py:202-209`). Pre-Phase-4.5 the install failed with `Configuration file not found at /tmp/gemini-extension*/gemini-extension.json` (G2 in [[archive/phase-5-cross-platform-install/VERIFICATION_2026-05/empirical_act_verification#Gemini]]).

#### From GitHub (specific branch)

```bash
echo "y" | gemini extensions install https://github.com/DgxSparkLabs/marketplace --ref feat/some-branch --consent
```

The `--ref <branch>` flag is real and Gemini clones the requested branch. CI uses this pattern: `compat-extension.yml` calls it with `--ref ${{ github.head_ref || github.ref_name }}`. The G3 attempt was VERIFIED-FAIL pre-Phase-4.5 because the root-level manifest didn't yet exist; post-Phase-4.5 the install succeeds. The flag itself is verified; the post-merge install path is exercised by every PR via `compat-extension.yml`'s `gemini-github-url-install` job.

#### From local clone

```bash
git clone https://github.com/DgxSparkLabs/marketplace
cd marketplace
echo "y" | gemini extensions install ./.gemini/ --consent
```

Verified PASS in [[archive/phase-5-cross-platform-install/VERIFICATION_2026-05/empirical_act_verification#Gemini]] (G1 — `Extension "dgxsparklabs-marketplace" installed successfully and enabled`, from `logs/G1.txt`). Local install reads `.gemini/gemini-extension.json` (byte-identical to the root copy).

### Discovery commands

| Command | What it lists | Example output |
|---|---|---|
| `gemini extensions list 2>&1` | Installed extensions | `G5_FOUND=YES` after grep for `dgxsparklabs` (from `logs/G5.txt`). Output goes to stderr on Linux — `2>&1` is required for piped grep |
| `gemini skills list --all 2>&1` | Discovered skills (project + user + built-in + extension-bundled) | `G6_FOUND=YES` after grep for `telegram-notify` (from `logs/G6.txt`); the `--all` flag includes built-ins |
| `gemini mcp list 2>&1` | Configured MCP servers | Empty-state: `No MCP servers configured.` — also written to stderr |
| `gemini extensions validate <path>` | Validate extension manifest | Exit 0 if valid; `Configuration file not found at <path>/gemini-extension.json` if missing |
| `gemini --version` | Binary version | Single string, e.g. `0.42.0` |
| `gemini --help` | Subcommand surface | 5 main subcommands + many flags |

### Per-plugin install

Not applicable — Gemini installs the whole marketplace as a single extension. Once the extension is installed, all skills inside it auto-discover. `gemini skills install <local-skill-dir>` does exist for installing a single skill outside the extension flow, but our CI installs the whole extension instead.

### What constructs it supports

| Construct | Supported | Notes |
|---|:--:|---|
| skill | yes | mirrored to `.gemini/skills/<name>/`; auto-discovered by `gemini skills list` |
| rule | no | Gemini reads rule context from `GEMINI.md` and `AGENTS.md` |
| command, agent, hook, mcp, lsp, monitor, output-style, theme | no | not part of Gemini's extension/skill model |

`GeminiPlatform.supports = {SkillConstruct}` at `scripts/platforms.py:189`.

### Discovery paths it reads

- `gemini-extension.json` at repo root (GitHub URL install) or `.gemini/gemini-extension.json` (local install)
- `.gemini/skills/<name>/SKILL.md` (auto-discovered skills)
- `GEMINI.md` and `AGENTS.md` (rule context)
- Config: `~/.gemini/config.json`, `~/.gemini/settings.json`

### CI assertions

| Workflow | What it asserts |
|---|---|
| `compat-extension.yml` (gemini job) | `gemini extensions list` baseline exits 0; `gemini extensions validate ./.gemini/` exits 0; local install via `echo "y" \| gemini extensions install ./.gemini/ --consent` succeeds; `gemini extensions list 2>&1 \| grep -F dgxsparklabs` matches |
| `compat-extension.yml` (gemini-github-url-install job) | Installs from `https://github.com/DgxSparkLabs/marketplace --ref <current-branch> --consent`; asserts the extension appears in `extensions list` |
| `compat-skill.yml` (gemini job) | `echo "y" \| gemini skills install ./_generated/skill-telegram-notify`; `gemini skills list --all \| grep -F telegram-notify` matches |
| `compat-mcp.yml` (gemini job) | `gemini mcp list` baseline exits 0; `gemini mcp add example uvx mcp-server-fetch` succeeds; `gemini mcp list 2>&1 \| grep -F example` matches |

### Known gaps

- **`gemini extensions list` and `gemini mcp list` write to stderr, not stdout.** Pipes must include `2>&1`. Verified across both commands.
- **`gemini --list-extensions` (top-level flag) requires auth.** Use the subcommand form `gemini extensions list` — that's auth-free.
- **Workspace trust required for project-scoped skill discovery.** Without it, Gemini reports `Skipping project agents due to untrusted folder`. Use `--skip-trust` for one-shot bypass.
- **Remote skill install via `--path` (G4) fails** with `No valid skills found` for unclear reasons; the extension-install path works. Open question, low priority.
- **`gemini hooks migrate --from-claude` is destructive and has no `--dry-run`.** Excluded from CI; reads `.claude/settings.json` and writes to `.gemini/settings.json` without confirmation.

### Out-of-scope or non-applicable

- Rules — Gemini does not have a rules concept; behavioral context comes from `GEMINI.md` / `AGENTS.md`.

### References

- [[archive/phase-5-cross-platform-install/VERIFICATION_2026-05/empirical_act_verification#Gemini]] — G1-G6 per-claim table
- [[archive/empirical-cli-findings/gemini]] — npm package metadata

---

## Cursor

### What it is

The Anysphere IDE (VS Code fork). The Cursor IDE Marketplace launched 2026-02-17 with Cursor 2.5; team marketplaces launched 2026-03-03 with Cursor 2.6. A Cursor CLI named `agent` exists (NOT `cursor`) — but it has no plugin install commands.

### Install path

#### From GitHub (default branch)

Plugin install for Cursor is IDE-only or admin-Dashboard-only. There is no `cursor plugin install <github-url>` equivalent.

**Path 1 — Cursor team marketplace (Cursor 2.6+, admin):**

> Dashboard → Settings → Plugins → Import → paste `https://github.com/DgxSparkLabs/marketplace` → save

Requires `.cursor-plugin/marketplace.json` at the repo root (emitted by generator Phase 6 at `scripts/generate_manifest.py:214-236`). As of 2026-05-01, team marketplace setup no longer requires a repository, but importing this marketplace specifically does require the GitHub URL or the manifest.

**Path 2 — In-editor:**

```text
/add-plugin
```

Slash command available in the agent chat panel since Cursor 2.5. The full argument syntax (including whether it accepts a raw GitHub URL) is not documented in Cursor's public docs.

#### From GitHub (specific branch)

Cursor team marketplace import is a Dashboard UI flow. Branch selection happens in the dashboard (not via CLI flag). No `--ref` equivalent exists for the `/add-plugin` slash command in published docs.

#### From local clone

```bash
git clone https://github.com/DgxSparkLabs/marketplace
# Open in Cursor IDE — rules and skills auto-load
```

Rules in `.cursor/rules/`, skills in `.agents/skills/`, `.cursor/skills/`, `.claude/skills/`, `.codex/skills/` all load automatically when the workspace opens.

#### Cursor CLI install (does not install plugins)

```bash
# macOS/Linux/WSL
curl https://cursor.com/install -fsS | bash

# Windows PowerShell
irm 'https://cursor.com/install?win32=true' | iex

# Verify
agent --version
```

CLI binary verified at `~/.local/bin/agent` (symlink) and `~/.local/share/cursor-agent/versions/<v>/cursor-agent` (real) in [[archive/phase-5-cross-platform-install/VERIFICATION_2026-05/empirical_act_verification#Cursor CLI]] (CU1, CU2, CU3). From `logs/CU1.txt`: `2026.05.20-2b5dd59. CU1_EXIT=0. CU1=PASS`.

### Discovery commands

The `agent` CLI has no plugin enumeration commands. Discovery is implicit — open the workspace in the IDE and Cursor scans the discovery paths below.

| Command | What it lists | Example output |
|---|---|---|
| `agent --version` | CLI binary version | `2026.05.20-2b5dd59` (from `logs/CU1.txt`) |
| `agent --help` | Full subcommand list | Commands: `install-shell-integration`, `uninstall-shell-integration`, `login`, `logout`, `mcp`, `worker`, `status\|whoami`, `models`, `about`, `update`, `create-chat`, `generate-rule\|rule`, `agent`, `ls`, `resume`, `help` (from `logs/CU3.txt`) |
| `agent --plugin-dir <path>` | Loads a local plugin directory for the session (no persistent install) | Runtime injection only |
| `agent mcp <subcommand>` | MCP server management | Documented but not captured in our logs |
| (In-IDE) `/rules`, `/commands` | List rules/commands in interactive session | Slash commands inside the editor agent chat |

### Per-plugin install

Not applicable for the CLI. In the IDE, `/add-plugin` is the per-plugin install gesture; the team marketplace Dashboard import is the multi-plugin gesture.

### What constructs it supports

| Construct | Supported | Notes |
|---|:--:|---|
| skill | yes | read from `.agents/skills/<name>/SKILL.md` (single canonical path) |
| rule | yes | read from `.cursor/rules/<name>.md`; per-plugin `.cursor-plugin/plugin.json` emitted for inclusion in team marketplace |
| agent | yes | read from `.cursor/agents/<name>.md` (workspace-level sub-agents, per `cursor.com/docs/agent/subagents`, 2026-05-25) |
| command | yes (manifest-only) | per-plugin `.cursor-plugin/plugin.json` includes `"commands": "./commands/"` pointer; Cursor auto-discovers `commands/` inside the installed plugin |
| hook | yes (manifest-only) | per-plugin `.cursor-plugin/plugin.json` includes `"hooks": "./hooks/hooks.json"` pointer |
| mcp | yes (manifest-only) | per-plugin `.cursor-plugin/plugin.json` includes `"mcpServers"` field |
| lsp, monitor, output-style, theme | no | Claude-specific construct types |

`CursorPlatform.supports = {RuleConstruct, SkillConstruct, AgentConstruct, CommandConstruct, HookConstruct, MCPConstruct}` at `scripts/platforms.py:280`.

### Discovery paths it reads

- `.cursor/rules/*.md` (with optional `.mdc` extension for richer frontmatter)
- `.cursor/agents/<name>.md` (workspace-level sub-agents per `cursor.com/docs/agent/subagents`, 2026-05-25)
- `.agents/skills/<name>/SKILL.md` (primary skill path per [cursor.com/docs/context/skills, 2026-05-24](https://cursor.com/docs/context/skills))
- `.cursor-plugin/marketplace.json` at repo root (team marketplace import)
- `_generated/<plugin>/.cursor-plugin/plugin.json` (per-plugin manifest with `agents` / `commands` / `hooks` / `mcpServers` pointer fields as applicable per `cursor.com/docs/reference/plugins`, 2026-05-25)
- `.cursorrules` (legacy single-file rule format; still valid as of May 2026)

### CI assertions

No CI workflow asserts Cursor-specific install behavior. Cursor's CI surface is format-only:

| Validation | What it covers |
|---|---|
| Generator drift check (CI baseline) | `.cursor/rules/*.md` and `.cursor-plugin/marketplace.json` regenerate byte-identical |
| `npx --yes cursor-doctor@1.11.0 scan .cursor/rules/` | Third-party format validator (free for `scan`; pay tier for `fix`); not currently wired into a workflow but available as an opt-in step |

There is no `compat-cursor.yml` workflow because no auth-free CLI command introspects installed plugins.

### Known gaps

- **No CLI plugin install.** The `agent` CLI has `mcp`, `models`, `generate-rule`, `install-shell-integration`, and others — but no `plugin install`, `plugin list`, `marketplace add`, or `add-plugin`. Plugin install is editor-only (`/add-plugin`) or admin-Dashboard-only. The `--plugin-dir <path>` flag exists for runtime injection of a local plugin dir — useful for testing, not for installation.
- **Prior empirical doc was wrong about CLI existence.** Before 2026-05-24, the project assumed Cursor had no CLI. The actual binary is `agent` (with `cursor-agent` as alias); the prior CI test probed for `cursor --version`. Now resolved — see [[archive/phase-5-cross-platform-install/VERIFICATION_2026-05/cursor#Section 2: Cursor CLI (with evidence)]].
- **Team marketplace branch selection happens in the Dashboard UI**, not via flag. No verified CLI/URL pattern for choosing a non-default branch.

### Out-of-scope or non-applicable

- MCP, hooks, commands, agents, output styles, themes — Cursor's plugin manifest supports many of these fields, but we don't currently emit them to Cursor. Future scope.

### References

- [[archive/phase-5-cross-platform-install/VERIFICATION_2026-05/cursor]] — full WebFetch research with URL + fetch date per claim
- [[archive/phase-5-cross-platform-install/VERIFICATION_2026-05/empirical_act_verification#Cursor CLI]] — CU1-CU3 act evidence
- [[archive/phase-5-cross-platform-install/VERIFICATION_2026-05/SUMMARY#Finding 5: Cursor CLI binary IS `agent` — prior empirical doc was wrong]]

---

## Windsurf

### What it is

The Codeium IDE (VS Code fork; acquired by Cognition in July 2025). No CLI exists; install is clone-and-open only. Windsurf Cascade (the agent panel) auto-discovers content at IDE open.

### Install path

#### From GitHub (default branch)

```bash
git clone https://github.com/DgxSparkLabs/marketplace
# Open the cloned directory in Windsurf IDE
# Rules auto-load from .windsurf/rules/
# Skills auto-load from .windsurf/skills/ and .agents/skills/
# Invoke any skill via @skill-name in Cascade chat
```

#### From GitHub (specific branch)

```bash
git clone -b feat/some-branch https://github.com/DgxSparkLabs/marketplace
```

Plain git pattern — Windsurf has no install command, so branch selection happens at clone time.

#### From local clone

Same as default-branch install. The IDE reads from the workspace's filesystem.

### Discovery commands

Windsurf has no CLI, so there are no introspection commands. Discovery is implicit — Cascade scans the discovery paths below on IDE open. Confirmed empirically across npm, pip, snap, apt, and GitHub releases: no Windsurf CLI binary exists. See [[archive/empirical-cli-findings/windsurf#Evidence from CI]].

| Indirect verification | How |
|---|---|
| Skill discovery | Open `.windsurf/skills/<name>/SKILL.md` or `.agents/skills/<name>/SKILL.md` in the IDE; Cascade reports it on first chat turn |
| Rule discovery | Cascade applies `.windsurf/rules/*.md` rules silently per their `trigger:` frontmatter (`always_on`, `model_decision`, `glob`, `manual`) |

### Per-plugin install

Not applicable — Windsurf has no plugin marketplace concept. Rules and skills are loaded from filesystem only.

### What constructs it supports

| Construct | Supported | Notes |
|---|:--:|---|
| rule | yes | mirrored to `.windsurf/rules/<name>.md` with `trigger: always_on` frontmatter |
| skill | yes (via `.agents/`) | Windsurf Cascade auto-discovers `.agents/skills/<name>/SKILL.md` per [docs.windsurf.com/windsurf/cascade/skills, 2026-05-25] |
| hook | yes | `.windsurf/hooks.json` (single hooks file at the `.windsurf/` root) per [docs.windsurf.com/windsurf/cascade/hooks, 2026-05-25] |
| everything else | no | Windsurf has no concepts beyond rules + skills + hooks |

`WindsurfPlatform.supports = {RuleConstruct, HookConstruct}` at `scripts/platforms.py:344`. Skills reach Windsurf via the shared `.agents/skills/` mirror emitted by `AgentsPlatform` (see [[ARCHITECTURE#The seven platform classes]]).

### Discovery paths it reads

- `.windsurf/rules/<name>.md` (with required `trigger:` frontmatter field — `always_on`, `model_decision`, `glob`, or `manual`; 12,000 char body limit per file)
- `.windsurf/hooks.json` (Cascade-triggered hooks per docs.windsurf.com/windsurf/cascade/hooks, 2026-05-25)
- `.agents/skills/<name>/SKILL.md` (auto-discovered by Cascade)
- User-scope equivalents: `~/.codeium/windsurf/...`, `~/.agents/skills/`

### CI assertions

No live-CLI assertion is possible. The CI surface is format-only:

| Validation | What it covers |
|---|---|
| Generator drift check (CI baseline) | `.windsurf/rules/*.md` regenerate byte-identical, frontmatter parses |
| `tests/test_marketplace.py` | YAML frontmatter parse + 12,000-char body length check via stdlib (no third-party validator available) |

There is no `compat-windsurf.yml` workflow because no CLI exists to invoke.

### Known gaps

- **No CLI exists, anywhere.** Verified across npm (`windsurf@0.0.1` is an unrelated terminal-cursor utility by an unaffiliated author), pip, snap, apt, and GitHub releases. See [[archive/empirical-cli-findings/windsurf#Evidence from CI]].
- **No plugin marketplace concept.** Rules and skills are loaded from filesystem only.

### Out-of-scope or non-applicable

- Headless validation. Best available is file-existence + frontmatter-parse checks via stdlib YAML.

### References

- [[archive/empirical-cli-findings/windsurf]] — CLI verification evidence
- [[archive/phase-5-cross-platform-install/VERIFICATION_2026-05/SUMMARY#Per-platform install story (what's true today)]] — Windsurf install row
- [[RULE_FORMAT#Windsurf (`formats/windsurf.md`)]] — Windsurf rule format spec

---

## Devin

### What it is

Cognition's terminal agent (`curl -fsSL https://cli.devin.ai/install.sh | bash`). Built on Windsurf/Codeium infrastructure (`devin auth login` reads "Log in to Windsurf"). No marketplace concept; reads content from the filesystem at session start.

### Install path

#### From GitHub (default branch)

```bash
# Install the binary (installer exits 1 in non-TTY environments; wrap with || true)
curl -fsSL https://cli.devin.ai/install.sh | bash || true

git clone https://github.com/DgxSparkLabs/marketplace
cd marketplace

# Auth-free discovery commands
devin skills list
devin rules list
devin mcp list
```

The Devin binary lands at `~/.local/bin/devin`. Auth-free verification commands work without `devin auth login`.

#### From GitHub (specific branch)

```bash
git clone -b feat/some-branch https://github.com/DgxSparkLabs/marketplace
```

Plain git pattern. Devin reads the cloned workspace on session start.

#### From local clone

Same as default-branch. Verified PASS in [[archive/empirical-cli-findings/devin#Auth-free commands verified (exit 0, useful output)]].

### Discovery commands

| Command | What it lists | Example output |
|---|---|---|
| `devin skills list` | All discovered skills (project + user dirs) | `/github-search [user,model] (./.devin/skills/github-search)` — format: `/<slash-command> [triggers] (path) - description` (per [[archive/empirical-cli-findings/devin#Skills output sample (from project context)]]) |
| `devin skills paths` | Where skills are loaded from | Lists `~/.config/devin/skills/`, `~/.agents/skills/`, `.devin/skills/`, `.agents/skills/` |
| `devin skills show <name>` | One skill's content | Formatted SKILL.md content |
| `devin rules list` | All discovered rules with provider tags | Rules tagged `Cursor`, `Windsurf`, `Standard` |
| `devin rules paths` | Where rules are loaded from | `Windsurf rules: .windsurf/rules/*.md` / `Cursor rules: .cursorrules, .cursor/rules/*.md` |
| `devin rules show <name>` | One rule's content | Formatted rule content |
| `devin mcp list` | Configured MCP servers | Empty-state: `No MCP servers configured` |
| `devin mcp get <name>` | One MCP server detail | Full config |
| `devin auth status` | Auth state (auth-free) | `Not logged in. / Credentials path: <path>` |
| `devin --version` | Binary version | `devin 2026.5.6-10 (87ae95e)` |

### Per-plugin install

Not applicable — Devin has no marketplace. Content is discovered live from the filesystem. The clone IS the install.

### What constructs it supports

| Construct | Supported | Notes |
|---|:--:|---|
| skill | yes (via `.agents/`) | reads `.agents/skills/<name>/SKILL.md` natively (per `devin skills paths` output). Legacy `.devin/skills/` mirror retired 2026-05-25 (D-1) — Devin's own enumeration confirms `.agents/skills/` is sufficient (Q-B1 PASS). |
| rule | yes (via Cursor/Windsurf mirrors) | reads `.windsurf/rules/*.md`, `.cursor/rules/*.md`, `.cursorrules`, `AGENTS.md` natively — no separate `.devin/rules/` emission needed |
| mcp | yes | `devin mcp list` / `devin mcp add` manage MCP server configs |
| everything else | no | Devin has no concepts beyond skills, rules, and MCP |

`DevinPlatform.supports = {SkillConstruct}` at `scripts/platforms.py:386` (kept so a future per-plugin Devin manifest schema can plug in via Phase 1.5 without code changes). `DevinPlatform.mirror_directory = None` — no Phase 3 mirror is emitted; skills reach Devin via the `.agents/skills/` shared mirror.

### Discovery paths it reads

Per `devin skills paths` (verified 2026-05-22, post-retirement re-verified 2026-05-25):

```
User skills (global):
  ~/.config/devin/skills/<skill-name>/SKILL.md
  ~/.agents/skills/<skill-name>/SKILL.md

Project skills:
  .agents/skills/<skill-name>/SKILL.md
```

Per `devin rules paths`:

```
Windsurf rules:  .windsurf/rules/*.md
Cursor rules:    .cursorrules, .cursor/rules/*.md
```

### CI assertions

| Workflow | What it asserts |
|---|---|
| `compat-skill.yml` (devin job) | `devin skills list \| grep -i telegram` matches (case-insensitive; Devin reads `.devin/skills/` mirror present after generator runs) |
| `compat-mcp.yml` (devin job) | `devin mcp list` baseline exits 0; `devin mcp add example -- uvx mcp-server-fetch` succeeds; `devin mcp list \| grep -i example` matches |

Devin jobs install the CLI via the composite action `./.github/actions/setup-devin` (which wraps the installer with `|| true` to tolerate the non-TTY exit code).

### Known gaps

- **Installer exits 1 in non-TTY environments.** The binary still installs; CI must wrap with `|| true`. See [[archive/empirical-cli-findings/devin#Install note]].
- **No plugin marketplace concept.** Content is discovered live from the filesystem.
- **`devin rules list` has no JSON flag.** Output is human-readable text only.

### Out-of-scope or non-applicable

- A `.devin/skills/` mirror is currently emitted alongside `.agents/skills/`, but Devin reads both — retiring the `.devin/skills/` mirror is on the future-cleanup list per `HANDOFF.md`. Not load-bearing.

### References

- [[archive/empirical-cli-findings/devin]] — full subcommand tree + auth-free command list
- [[archive/phase-5-cross-platform-install/VERIFICATION_2026-05/SUMMARY#Per-platform install story (what's true today)]] — Devin install row

---

## Cross-platform conventions

### The `.agents/` convergence (content only, not plugins)

Windsurf, Cursor, and Devin all auto-discover skills from `.agents/skills/<name>/SKILL.md` natively, per each platform's official docs (all fetched 2026-05-24):

- Cursor: `cursor.com/docs/context/skills` lists `.agents/skills/` as a project-level skill path
- Windsurf: `docs.windsurf.com/windsurf/cascade/skills` lists `.agents/skills/<name>/SKILL.md`
- Devin: `devin skills paths` empirical output lists `.agents/skills/<skill-name>/SKILL.md` as a project skill path

This is the **only** true cross-platform convergence. The generator emits the shared content via `AgentsPlatform` (see [[ARCHITECTURE#The seven platform classes]]).

For **plugin marketplaces**, there is no `.agents/` convergence. Each platform uses its own path:

- Claude → `.claude-plugin/marketplace.json` + `.claude-plugin/plugin.json`
- Codex → `.claude-plugin/marketplace.json` (legacy-compatible) or `.agents/plugins/marketplace.json` (canonical, not adopted here)
- Cursor → `.cursor-plugin/marketplace.json` at repo root + per-plugin `.cursor-plugin/plugin.json`

See [[archive/phase-5-cross-platform-install/VERIFICATION_2026-05/SUMMARY#Finding 1: The `.agents/` directory is a real convergence — but only for content, not for marketplaces]].

### Mirror hygiene rules (what NOT to copy across)

When `Platform.emit` copies source content into a per-platform mirror directory, it must exclude per-platform manifest directories so they don't bleed across mirrors. The generator uses a shared `shutil.ignore_patterns` constant:

```python
# scripts/platforms.py:58-61
_COPY_IGNORE = shutil.ignore_patterns(
    "__pycache__", "*.pyc",
    ".claude-plugin", ".codex-plugin", ".cursor-plugin",
)
```

Every Platform's `emit` method passes `ignore=_COPY_IGNORE` to `shutil.copytree`. Result: mirrored skill content (e.g. `.gemini/skills/<name>/`) will never contain a stray `.claude-plugin/` directory from the source tree.

### Per-platform manifest paths (one-line each)

| Platform | Marketplace manifest | Per-plugin manifest | Skill content mirror | Rule / agent / hook mirror |
|---|---|---|---|---|
| Claude Code | `.claude-plugin/marketplace.json` | `_generated/<plugin>/.claude-plugin/plugin.json` | (via plugin install) | rules consumed via filesystem (`.claude/rules/*.md`) — not a plugin component as of 2026-05-26 |
| Codex | `.claude-plugin/marketplace.json` (legacy) + `.agents/plugins/marketplace.json` (canonical, Phase 5.5) | `_generated/<plugin>/.codex-plugin/plugin.json` | (via per-plugin manifest only — `.codex/skills/` retired 2026-05-25) | `.codex/agents/<name>.toml` (sub-agents); reads rules from `AGENTS.md`, `.cursor/`, `.windsurf/` |
| Gemini | `gemini-extension.json` (root, for GitHub URL) or `.gemini/gemini-extension.json` (local) | n/a (extensions, not plugins) | `.gemini/skills/` | `.gemini/agents/<name>.md`, `.gemini/hooks/hooks.json`; reads rules from `GEMINI.md`, `AGENTS.md` |
| Cursor | `.cursor-plugin/marketplace.json` (root, team-import) | `_generated/<plugin>/.cursor-plugin/plugin.json` (with `agents`/`commands`/`hooks`/`mcpServers` pointer fields) | `.agents/skills/` (primary) | `.cursor/rules/`, `.cursor/agents/<name>.md` |
| Windsurf | n/a | n/a | `.agents/skills/` | `.windsurf/rules/`, `.windsurf/hooks.json` |
| Devin | n/a | n/a | `.agents/skills/` (legacy `.devin/skills/` retired 2026-05-25) | reads from `.cursor/`, `.windsurf/`, `AGENTS.md` |
| Agents (convergence) | `.agents/plugins/marketplace.json` (Phase 5.5; byte-identical to `.claude-plugin/marketplace.json`) | n/a | `.agents/skills/<name>/SKILL.md` | `.agents/rules/<name>.md` (forward-looking) |

For the architecture behind why Cursor is IDE-only and how `AgentsPlatform` exists, see [[ARCHITECTURE#The seven platform classes]].

---

## Discovery cheatsheet

One table cross-referencing every platform's discovery commands. Use this when you're trying to verify "did my install actually land?".

| Platform | List installed | List available | Show one item | Where things are loaded from |
|---|---|---|---|---|
| Claude Code | `claude plugin list` | `claude plugin list --json --available` | `claude plugin details <name>` | `~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/` |
| Codex | `codex plugin list` (lists installed and available together) | same | `codex mcp get <name>` (for MCP only) | `~/.codex/config.toml` + `~/.codex/.tmp/marketplaces/` |
| Gemini | `gemini extensions list 2>&1`, `gemini skills list --all 2>&1` | `gemini skills list --all 2>&1` | `gemini extensions validate <path>` | `~/.gemini/extensions/`, `.gemini/skills/` |
| Cursor | (no CLI introspection) | (Dashboard UI) | (none headless) | `.cursor/rules/`, `.agents/skills/`, `.cursor-plugin/marketplace.json` |
| Windsurf | (no CLI) | (no CLI) | (none) | `.windsurf/rules/`, `.windsurf/hooks.json`, `.agents/skills/` |
| Devin | `devin skills list`, `devin rules list`, `devin mcp list` | same (filesystem-discovered) | `devin skills show <name>`, `devin rules show <name>`, `devin mcp get <name>` | `devin skills paths` + `devin rules paths` print them |

Note all `gemini` list commands need `2>&1` because Gemini writes list output to stderr on Linux.

---

## Glossary

| Term | Meaning here |
|---|---|
| **construct** | One of 10 plugin construct types: skill, rule, command, agent, hook, mcp, lsp, monitor, output-style, theme. Each is a class in `scripts/constructs.py`. See [[CONSTRUCT_TYPES]]. |
| **platform** | One of 7 emission targets: Claude Code, Codex, Gemini, Cursor, Windsurf, Devin, plus `AgentsPlatform`. Each is a class in `scripts/platforms.py`. |
| **`supports`** | Per-platform set of construct CLASSES that platform can host. Gates per-plugin manifest emission and mirror generation. See [[ARCHITECTURE#The `supports` gate]]. |
| **mirror hygiene** | Excluding per-platform manifest dirs (`.claude-plugin`, `.codex-plugin`, `.cursor-plugin`) from `shutil.copytree` so they don't bleed across mirrors. |
| **bundle** | A dep-only plugin grouping other plugins. Two kinds: catalog bundles (declared in `catalog.toml`) and code-generated catch-alls (`bundle-<prefix>-all`). |
| **catch-all** | A code-generated bundle named `bundle-<prefix>-all` (e.g., `bundle-skill-all`) installing every plugin of one construct type. NOT declared in `catalog.toml`. |
| **`.agents/`** | Cross-platform skill convergence directory at `.agents/skills/<name>/SKILL.md`. Read natively by Windsurf, Cursor, and Devin. |
| **GitHub-direct install** | A one-command install from a GitHub URL or shortform, without `git clone`. Supported natively by Claude, Codex, and Gemini. |

---

## References

- [[archive/phase-5-cross-platform-install/VERIFICATION_2026-05/SUMMARY]] — ground-truth synthesis (most current single doc)
- [[archive/phase-5-cross-platform-install/VERIFICATION_2026-05/empirical_act_verification]] — per-claim act-based evidence (18 claims)
- [[archive/phase-5-cross-platform-install/VERIFICATION_2026-05/cursor]] — Cursor IDE + CLI May 2026 WebFetch research
- [[archive/empirical-cli-findings/devin]] — Devin CLI subcommand tree
- [[archive/empirical-cli-findings/windsurf]] — Windsurf CLI verification (no CLI exists)
- [[archive/empirical-cli-findings/codex]] — Codex npm metadata
- [[archive/empirical-cli-findings/gemini]] — Gemini npm metadata
- [[ARCHITECTURE]] — generator architecture (Construct + Platform protocols, six phases)
- [[CONTRIBUTING]] — how to add things and test
- [[CONSTRUCT_TYPES]] — 10-construct reference table
- [[RULE_FORMAT]] — rule format spec
- [[SKILL_FORMAT]] — SKILL.md format spec
- [[ADDING_A_CONSTRUCT]] — primary contributor walkthrough

---

*Last updated: 2026-05-24.*
