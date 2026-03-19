# Handoff

## What This Is

A **skills and rules marketplace** for AI coding agents. Not a software project — the "product" is the skills, rules, and research themselves. Cross-platform: Devin CLI, Claude Code, Cursor, Windsurf.

- **Skills** = on-demand capabilities invoked with `/skill-name` (24 skills)
- **Rules** = always-on behavioral guidelines loaded every session (15 rules)
- **Research** = 250+ sources across 12 rounds of market intelligence
- **TUI installer** = interactive terminal UI for installing everything (`install.py`)

## How to Build/Test

```bash
uv run install.py                    # run the TUI installer
uv run install.py --uninstall        # uninstall mode
uv run tests/test_marketplace.py     # 112 tests (must all pass)
uv run tests/test_marketplace.py -v  # verbose
uvx ruff check install.py            # lint
./tests/run-ci-local.sh              # run GitHub Actions locally with act+podman
```

**Always run `uv run tests/test_marketplace.py` before committing.** This is the quality gate.

## Project Layout

```
marketplace/
├── AGENTS.md                ← Project conventions (read this)
├── README.md                ← Catalog of all skills and rules
├── catalog.toml             ← TUI config: platforms, MCP servers, families
├── install.py               ← Single-file Textual TUI (1,991 lines, PEP 723)
├── scripts/install.sh       ← One-command bootstrap (curl | bash)
├── _template/               ← Starter for new skills
├── docs/
│   ├── ONBOARDING.md        ← 3-minute orientation for new agents
│   ├── SKILL_FORMAT.md      ← Full SKILL.md spec
│   └── RULE_FORMAT.md       ← Full rule spec
├── skills/                  ← 24 skill directories
├── rules/                   ← 15 rule directories
├── research/                ← 90+ files, 12 research rounds
└── tests/
    ├── test_marketplace.py  ← 112 tests (structure, conventions, installer)
    └── run-ci-local.sh      ← Local CI with act+podman
```

## Inventory

### Skills (24)

| Skill | What it does | Key deps |
|-------|-------------|----------|
| act-runner | Run GitHub Actions locally with act+podman | podman, act |
| check | Mid-session course correction — stop, review rules, realign | none |
| duckduckgo-search | Search DuckDuckGo, triage, scrape results | web-scraper skill |
| expose-port | Expose local port via HTTPS or TCP | ssh, bore (optional) |
| gemini-chat | Multi-turn chat with Google Gemini | GEMINI_API_KEY |
| github-search | Search GitHub repos for prior art | gh CLI |
| google-drive-reader | Read Google Docs from Drive | Google OAuth creds |
| motivation | Completeness checker before stopping | none |
| pitfall-check | Search PITFALLS.md and git log for known issues | none |
| project-bootstrap | Init AGENTS.md, HANDOFF.md, CHANGELOG.md, PITFALLS.md | none |
| recall-rules | Re-read global rules and thinking framework mid-session | none |
| send-email | Send email via Resend API | RESEND_API_KEY |
| session-history | Query past Devin CLI conversations | Devin sessions.db |
| session-wrapup | End-of-session audit for handoff readiness | none |
| skill-creator | Full skill authoring lifecycle with evals | claude CLI |
| ssh-tunnel | SSH port forwarding (local, remote, SOCKS) | OpenSSH |
| structured-handoff | Generate .tasks/ directory for autonomous sessions | none |
| sync-rules | Sync global agent rules into workspace | none |
| telegram-notify | Send Telegram notifications + wait for input | TELEGRAM_BOT_TOKEN |
| textual-tui-guide | Reference for building Textual TUIs | none |
| web-scraper | Fetch web page, extract clean text | none |
| youtube-search | Search YouTube for technical videos | none |
| youtube-wisdom | Extract knowledge from YouTube transcripts | none |
| devin-for-terminal | Look up Devin CLI documentation | none |

### Rules (15)

| Rule | What it enforces |
|------|-----------------|
| blast-radius | Scope changes, prefer small atomic edits |
| continuous-improvement | Seven-phase workflow for codebase hardening |
| document-lifecycle | Three-tier docs: rules, reference, history |
| document-progress | Plan tasks upfront, write progress to disk |
| improve-the-process | Every session improves the workflow |
| no-ai-credit | Never attribute work to AI agents |
| pitfalls-discipline | Maintain PITFALLS.md read/write loop |
| prior-art | Search before building |
| python-uv | Always use uv, never pip |
| session-resilience | Write state continuously to survive context loss |
| stay-motivated | Check todo list before stopping |
| task-formation | Decompose requests into goals, then tasks |
| telegram-on-complete | Notify via Telegram after completing work |
| verification-ladder | Five-layer automated testing |
| verify-your-work | Prove correctness, don't assume it |

## TUI Installer Architecture

`install.py` is a single-file Textual app with PEP 723 inline deps.

**Key components:**
- `catalog.toml` drives all configuration (platforms, MCP servers, skill/rule families, defaults)
- `_build_platforms()` converts TOML to runtime `PLATFORMS` dict; empty string `""` becomes `None` (falsy)
- `_execute_install()` handles per-platform scope forcing: if a platform has `global.rules = None`, rules redirect to workspace scope
- `MarketplaceList` — click-to-focus selection list
- `PathInput` — input with dropdown autocomplete for filesystem paths
- `AnimatedBanner` — spinning 3D wireframe cube with HSV color cycling
- Modal screens: PathPicker, Preview, Confirm (with scope breakdown), Results

**Platform support:**
- Devin CLI: skills to `~/.config/devin/skills/`, rules to AGENTS.md (global rules = None, forced workspace)
- Claude Code: skills to `~/.claude/skills/`, rules to CLAUDE.md
- Cursor: skills to `.cursor/skills/`, rules to `.cursor/rules/` (YAML frontmatter)
- Windsurf: skills to `.windsurf/skills/`, rules to `.windsurf/rules/` (YAML frontmatter)

**Install operations are idempotent.** Running twice produces the same result.

## Research Library

90+ files across 12 rounds. 250+ sources from GitHub, arXiv, Reddit, Twitter/X, Kaggle, web.

**Reading order:**
1. `research/KNOWLEDGE_BASE.md` — distilled insights (307 lines)
2. `research/ANTI_PATTERNS.md` — dead ends and traps (217 lines)
3. `research/SUMMARY_AND_CONCLUSIONS.md` — master synthesis (526 lines)
4. Platform-specific findings (arxiv, github, reddit, kaggle, etc.)
5. `research/METHODOLOGY.md` — how the research was done

**Key findings from 200+ sources:**
- $7.5-8.3B market in 2025, projected $47-53B by 2030 (41-46% CAGR)
- Trust is the product, not skills (26.1% of community skills have vulnerabilities)
- SKILL.md is the de facto standard (Anthropic, OpenAI, Microsoft, Cursor, Windsurf, 38+ agents)
- Nobody has won yet — 15+ competing platforms, all pre-PMF
- Narrow verticals beat general catalogs
- Composability (DAG orchestration) is the moat

**Critical research rules:**
- Never wholesale-rewrite canonical files — merge incrementally
- New research rounds go in `skill-marketplaces-N+1/`
- Verify star counts against live sources before citing
- Note provenance (which research round)
- See `research/TASKS.md` for maintenance backlog (T6, T7, T10 pending)

## Adding Skills/Rules

### New skill
1. Copy `_template/` to `skills/your-skill-name/`
2. Write `SKILL.md` (YAML frontmatter + prompt) — see `docs/SKILL_FORMAT.md`
3. Scripts in `scripts/` use PEP 723 inline deps
4. Set `allowed-tools` to minimum needed
5. Add README.md, update root README.md catalog (alphabetical)
6. Run tests

### New rule
1. Reference: `rules/no-ai-credit/`
2. Write `rule.md` (plain Markdown, no frontmatter)
3. Create `formats/windsurf.md` and `formats/cursor.md`
4. Adapt `install.sh` (delegates to `scripts/install-rule.sh`)
5. Add README.md, update root README.md catalog (alphabetical)
6. Run tests

## Conventions

- Directory names: **kebab-case**
- Python scripts: **snake_case**, PEP 723 inline deps, `uv run`
- Shell scripts: shebang + `set -euo pipefail`
- No project-level config at root (no pyproject.toml, package.json)
- No secrets committed
- Don't mix skill and rule formats in one directory
- Rules should be concise checklists, not essays

## Recent Changes

- **sync-rules skill** (`d1db0ca`→`0958aa3`): Import global agent rules into workspace. Fixed YAML escaping, slug collisions, empty slugs, avoids overwriting existing files.
- **catalog.toml + installer upgrade** (`9edc9de`): Per-item scope toggle, workspace paths with autocomplete, catalog externalization, platform-aware scope forcing.
- **Installer bug fixes** (`d6f254a`, `404b181`, `b2adcb6`): Crash on empty catalog, duplicate summary, race condition, banner K glyph, dropdown cap, installed marker across platforms, confirm summary scope breakdown.
- **Session resilience** (`2e5dccf`): Added HANDOFF.md, PITFALLS.md, CHANGELOG.md.

## Known Limitations

- Installed marker only checks global scope per platform. Workspace-installed items aren't reflected.
- Path autocomplete dropdown shows all results — very large directories may produce long lists.
- The `devin-for-terminal` skill is referenced in README but ships with Devin CLI itself, not in the repo.

## What's Next

- Research backlog: T6 (synthesize R10-R12 into canonical files), T7 (reconcile star counts), T10 (archive raw search artifacts in R1)
- Consider lazy loading for path autocomplete on large directories
- Consider workspace-scope detection for installed markers
