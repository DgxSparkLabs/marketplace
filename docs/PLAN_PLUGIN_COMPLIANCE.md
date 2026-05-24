# Plan — Claude Code Plugin Compliance

**Branch:** `feat/claude-plugin-compliance`
**Goal:** see `docs/GOAL_PLUGIN_COMPLIANCE.md`
**Companion:** see `docs/INVESTIGATION_PLUGIN_DEPENDENCIES.md` for the bundle-architecture uncertainty

This is the working plan. Update it as the work progresses and design decisions firm up.

---

## Why This Exists

The current marketplace ships via a curl-bootstrapped Textual TUI installer (`install.py` + `scripts/install.sh`). This works but is non-standard. Claude Code natively supports `/plugin marketplace add <user>/<repo>` to discover and install plugins from a GitHub repo containing a `.claude-plugin/marketplace.json` manifest. Adopting this format makes the marketplace installable through Claude Code's native CLI surface with no bootstrap, no Python TUI, no curl-bash.

Reference repo we are modeling after: [`alirezarezvani/claude-skills`](https://github.com/alirezarezvani/claude-skills).

---

## Architecture (the design we're building)

### 1. Repository identity

- GitHub repo: `https://github.com/DgxSparkLabs/marketplace`
- Single source for repo metadata: a new `MARKETPLACE.toml` at the repo root containing name, owner, repository URL, homepage, license, version. All generated plugin manifests inherit from this. Renaming the org or bumping the version becomes a one-line edit.

### 2. Two source-of-truth layers

| Layer | Location | Owned by | Purpose |
|-------|----------|----------|---------|
| Content | `skills/<name>/SKILL.md`, `rules/<name>/rule.md`, `examples/example-<type>/...` | Humans | The actual plugin content — what gets installed |
| Tagging | `catalog.toml` | Humans | Which construct type each item is, which domain bundle it belongs to |
| Generated | `_generated/<plugin-name>/...`, `.codex/`, `.gemini/`, `.cursor/`, `.windsurf/`, `.claude-plugin/marketplace.json` | `generate_manifest.py` | Plugin wrappers, bundle plugins, cross-platform mirrors, root manifest |

Humans edit content + tagging. The generator produces everything else. Generated content is committed to git so the repo is self-contained and `/plugin marketplace add` works against a fresh clone with no setup.

### 3. Plugin naming convention

| Construct type | Individual prefix | Domain prefix | Example individual | Example domain |
|----------------|-------------------|---------------|--------------------|----------------|
| skill | `skill-` | `skills-` | `skill-telegram-notify` | `skills-communication` |
| rule | `rule-` | `rules-` | `rule-blast-radius` | `rules-quality` |
| command | `command-` | `commands-` | `command-review` | `commands-git` |
| agent | `agent-` | `agents-` | `agent-security-reviewer` | `agents-engineering` |
| hook | `hook-` | `hooks-` | `hook-pre-commit-lint` | `hooks-quality-gates` |
| mcp | `mcp-` | `mcps-` | `mcp-fetch` | `mcps-research` |
| lsp | `lsp-` | `lsps-` | `lsp-typescript` | `lsps-web-stack` |
| monitor | `monitor-` | `monitors-` | `monitor-disk-usage` | `monitors-system-health` |
| output style | `output-style-` | `output-styles-` | `output-style-explanatory` | `output-styles-formal-suite` |
| theme | `theme-` | `themes-` | `theme-solarized` | `themes-classic-pack` |

Predictable, machine-parseable, identifies construct type from plugin name alone.

### 4. Domain-bundle architecture (dependency-only, with fallback)

**Preferred design** — bundles are content-free plugin.json files declaring dependencies:

```json
{
  "name": "skills-communication",
  "version": "1.0.0",
  "description": "Communication skills: send-email, telegram-notify",
  "dependencies": ["skill-send-email", "skill-telegram-notify"]
}
```

**Hard dependency:** this design requires Claude Code to auto-install plugin dependencies. **This is the open question tracked in `INVESTIGATION_PLUGIN_DEPENDENCIES.md` and task #13.** Verify before building bundles.

**Fallback if deps don't auto-install** (selected by us as Option 2 in that file): each bundle ships an `install-deps.sh` that calls `claude plugin install <each>`. User runs the script after the bundle install.

### 5. Rules architecture (Path 2 — explicit, manual activation)

Claude Code's plugin system does not natively support installing rules (confirmed via documentation review; feature request open at anthropics/claude-code#21163). The workaround:

- Each rule is shipped as a real plugin: `rule-<name>/.claude-plugin/plugin.json` + `rules/<name>.md` + `activate.sh`
- `/plugin install rule-<name>@dgxsparklabs-marketplace` extracts the plugin to `~/.claude/plugins/cache/...`
- User then runs `bash <cache>/rule-<name>/activate.sh`, which symlinks the rule file into `.claude/rules/`
- Claude Code loads `.claude/rules/*.md` automatically at session start

A repo-root `activate-installed-rules.sh` provides a one-shot helper that scans all installed rule plugins and symlinks them in bulk.

This is an asymmetry with skills (which auto-activate). The asymmetry is real and documented; we do not hide it.

### 6. Cross-platform mirrors

Auto-generated and committed:

| Mirror | Source | Format |
|--------|--------|--------|
| `.codex/skills/` | `skills/*/SKILL.md` | Codex CLI skill format |
| `.gemini/skills/` | `skills/*/SKILL.md` | Gemini CLI skill format |
| `.cursor/rules/` | `rules/*/formats/cursor.md` | Cursor rule format with frontmatter |
| `.windsurf/rules/` | `rules/*/formats/windsurf.md` | Windsurf rule format with `trigger: always_on` |

Users of non-Claude-Code platforms `git clone` and point their tool at the right subdirectory. No npm install, no Python.

### 7. Example plugins (10 total, one per construct type)

`examples/` directory ships a working reference plugin for every construct type. Each is both functional (installable, runnable) and pedagogical (README explains every part, contributors copy-and-adapt). All examples share a coherent fictional context — proposed: **"DgxSpark Lab Notebook"** — so examples feel like a mini-application demonstrating how constructs compose.

| Example | Demonstrates |
|---------|-------------|
| `example-skill` | SKILL.md format, $SKILL_DIR usage, allowed-tools, triggers |
| `example-rule` | rule plugin + activate.sh symlink mechanism |
| `example-command` | slash command markdown |
| `example-agent` | sub-agent with own system prompt |
| `example-hook` | UserPromptSubmit + PreToolUse hooks |
| `example-mcp` | MCP server registration |
| `example-lsp` | LSP server registration |
| `example-monitor` | background monitor |
| `example-output-style` | output style with frontmatter |
| `example-theme` | theme file |

---

## Generator Script (`scripts/generate_manifest.py`)

PEP 723 inline-deps script, runnable via `uv run`.

**Inputs:** `MARKETPLACE.toml`, `catalog.toml`, `skills/`, `rules/`, `examples/`

**Outputs:** `.claude-plugin/marketplace.json`, `_generated/**`, `.codex/`, `.gemini/`, `.cursor/`, `.windsurf/`

**Modes:**
- `--write` (default) — generate and write all output files
- `--check` — exit non-zero if generated content differs from committed content (CI gate)

---

## Repository Layout (target)

```
marketplace/
├── MARKETPLACE.toml                         single source of repo identity
├── .claude-plugin/marketplace.json          generated root manifest (~71 plugin entries)
│
├── skills/                                  REAL CONTENT — 26 skills, flat
├── rules/                                   REAL CONTENT — 21 rules, flat
├── examples/                                REAL CONTENT — 10 example-* reference plugins
│
├── _generated/                              GENERATED — committed
│   ├── skill-*/                             individual skill wrappers
│   ├── rule-*/                              individual rule wrappers (+ activate.sh)
│   ├── skills-*/                            dep-only skill domain bundles
│   ├── rules-*/                             dep-only rule domain bundles (+ install-deps.sh fallback)
│   └── rules-all/                           catch-all rule bundle
│
├── .codex/skills/                           GENERATED — committed mirrors
├── .gemini/skills/
├── .cursor/rules/
├── .windsurf/rules/
│
├── activate-installed-rules.sh              repo-root helper for bulk rule activation
├── catalog.toml                             construct types + domain tagging
├── scripts/
│   └── generate_manifest.py                 NEW (PEP 723 + uv)
├── tests/test_marketplace.py                updated for new structure
│                                            (install.py, scripts/install.sh, scripts/install-rule.sh,
│                                             rules/*/install.sh are DELETED — no longer exist)
└── docs/
    ├── GOAL_PLUGIN_COMPLIANCE.md            this branch's goal + success criteria
    ├── PLAN_PLUGIN_COMPLIANCE.md            this file
    ├── INVESTIGATION_PLUGIN_DEPENDENCIES.md task #13 verification plan + fallbacks
    ├── CONSTRUCT_TYPES.md                   index of construct types + Claude Code mapping
    ├── ADDING_A_SKILL.md                    contributor tutorials (one per construct type)
    ├── ADDING_A_RULE.md
    ├── ADDING_A_COMMAND.md
    ├── ADDING_AN_AGENT.md
    ├── ADDING_A_HOOK.md
    ├── ADDING_AN_MCP_SERVER.md
    ├── ADDING_AN_LSP_SERVER.md
    ├── ADDING_A_MONITOR.md
    ├── ADDING_AN_OUTPUT_STYLE.md
    ├── ADDING_A_THEME.md
    └── ADDING_A_DOMAIN_BUNDLE.md            how catalog.toml tagging produces bundles
```

---

## Install UX (after migration)

```bash
# Add the marketplace once
/plugin marketplace add DgxSparkLabs/marketplace

# Skills — auto-activate after install
/plugin install skill-telegram-notify@dgxsparklabs-marketplace            # individual
/plugin install skills-communication@dgxsparklabs-marketplace             # bundle (deps install per task #13 outcome)

# Rules — require activate step after install
/plugin install rule-blast-radius@dgxsparklabs-marketplace
bash ~/.claude/plugins/cache/dgxsparklabs-marketplace/rule-blast-radius/activate.sh

# Or all rules at once
/plugin install rules-all@dgxsparklabs-marketplace
bash ~/.claude/plugins/cache/dgxsparklabs-marketplace/rules-all/activate.sh

# Or activate everything currently installed in one shot
bash ~/.local/share/marketplace/activate-installed-rules.sh

# Other construct types follow the skill pattern (auto-activate)
/plugin install example-command@dgxsparklabs-marketplace
/plugin install example-agent@dgxsparklabs-marketplace
/plugin install example-hook@dgxsparklabs-marketplace
```

---

## Task Execution Order

| # | Task | Why this position |
|---|------|-------------------|
| 12 | Rename `ForkYoraiLevi` → `DgxSparkLabs` everywhere | Cleanup first so subsequent generation inherits correct URLs |
| 13 | Verify plugin dep auto-install (build 2 test plugins, push throwaway marketplace) | Blocking research — bundle architecture depends on outcome |
| 2 | Set up source layout + `MARKETPLACE.toml` + extend `catalog.toml` tagging | Foundation for the generator |
| 3 | Build 10 `example-*` plugins | Reference templates the generator and docs depend on |
| 4 | Write `generate_manifest.py` | The engine |
| 5 | Run generator → `_generated/` + mirrors | Materialize the marketplace |
| 9 | Update `tests/test_marketplace.py` for new structure | Validate the materialization passes |
| 6 | Add CI manifest validation step (`--check`) | Prevent drift in PRs |
| 7 | Delete TUI installer + all legacy install scripts; clean up references | Full removal in this branch — no soft-deprecation |
| 8 | Write `CONSTRUCT_TYPES.md` + 11 `ADDING_*.md` tutorials + README rewrite | Documentation pass with full structure known |
| 10 | End-to-end verification + open PR to main | Ship |

Task #1 (design phase) closes when execution begins.

---

## Known Risks and Decisions Made

| Risk | Decision | Trigger to revisit |
|------|----------|---------------------|
| Plugin dependencies may not auto-install | Verify in task #13 before building bundles. Fallback is Option 2 (bundle ships `install-deps.sh`). | Empirical test outcome |
| Rules need manual activation step — confusing UX | Accept. Document prominently. Mitigate with `activate-installed-rules.sh`. | Anthropic adds native rules field to plugin.json |
| 71+ plugin entries may clutter `/plugin install` picker | Use consistent prefixes (`skill-`, `skills-`, `rule-`, `rules-`, etc.) and `displayName` field per entry | If user feedback indicates discovery friction |
| Cross-platform mirrors duplicate content on disk | Auto-generated and validated by CI. Repo size cost accepted for offline-clone usability. | If repo size becomes problematic |
| Deleting TUI breaks users on the `curl ... \| bash` path | Document the migration prominently in CHANGELOG.md and the PR description. New install path: `/plugin marketplace add DgxSparkLabs/marketplace`. Non-Claude-Code platform users use the auto-generated mirrors (`.codex/`, `.gemini/`, `.cursor/`, `.windsurf/`). No backwards-compat shim is shipped. | User reports of broken installs after merge |

---

## What Done Looks Like

When all 12 criteria in `GOAL_PLUGIN_COMPLIANCE.md` pass, this branch is mergeable to main. The PR description should reference both planning documents and the task list.
