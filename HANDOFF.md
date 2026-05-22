# Handoff

> **Start here if you've never seen this project before:** `docs/RESUME_HERE.md`. That file is the 3-minute orientation. This document (`HANDOFF.md`) is for ongoing-state tracking; it complements `RESUME_HERE.md` rather than duplicating it.

**Branch state:** `feat/claude-plugin-compliance` — migration complete, multi-platform validation design complete, validation implementation not yet started. PR #1 open: https://github.com/DgxSparkLabs/marketplace/pull/1

---

## What This Is

A **Claude Code plugin marketplace** for AI coding agents. Natively installable via `/plugin marketplace add DgxSparkLabs/marketplace`, with auto-generated mirrors for Devin CLI, Cursor, Windsurf, Codex CLI, and Gemini CLI.

- 26 skills (`skills/<name>/`)
- 21 rules (`rules/<name>/`)
- 10 example reference plugins (`examples/example-<type>/`)
- 71 plugin entries in `.claude-plugin/marketplace.json` (26 individual skills + 8 skill-domain bundles + 21 individual rules + 5 rule-domain bundles + 1 rules-all + 10 examples)
- 250+ research sources across 12 rounds in `research/`

---

## Two Completed Work Phases

### Phase 1 — Plugin Compliance Migration (DONE)

Moved the marketplace from a custom Textual TUI installer + curl-bash bootstrap to native Claude Code `/plugin marketplace add`.

- Deleted `install.py`, `scripts/install.sh`, `scripts/install-rule.sh`, all per-rule `install.sh` files, `pyproject.toml`, `uv.lock`, `_template/`
- Added `MARKETPLACE.toml` (single source for identity: owner, version, license, repo URL)
- Restructured `catalog.toml` around `[construct.*]` definitions + `[skill_domain.*]` / `[rule_domain.*]` tagging
- Wrote `scripts/generate_manifest.py` (PEP 723) — produces `_generated/skill-*/`, `_generated/rule-*/`, dependency-only bundle plugins, cross-platform mirrors (`.codex/`, `.gemini/`, `.cursor/`, `.windsurf/`, `.devin/`)
- Built 10 example reference plugins (`examples/example-<construct>/`) — one per Claude Code construct type
- Wrote 12 contributor tutorials (`docs/CONSTRUCT_TYPES.md` + 11 `docs/ADDING_*.md`)
- Verified end-to-end install of skills + bundles + rules against the local marketplace
- Renamed marketplace from `marketplace` → `dgxsparklabs-marketplace` for disambiguation
- Empirically verified that Claude Code auto-installs plugin dependencies (documented in `docs/INVESTIGATION_PLUGIN_DEPENDENCIES.md`)

### Phase 2 — Multi-Platform Validation Design (DONE)

Designed (but did not implement) the CI/CD layer that will verify our marketplace works on every platform we ship a mirror for.

Three sub-phases:

**Phase 2a — Empirical CLI Discovery:**
- Sub-agent on `exp/cli-empirical-discovery` branch built five `explore-<platform>.yml` workflows; ran CI; captured logs; documented findings in `docs/EMPIRICAL_CLI_FINDINGS/<platform>.md` per platform
- Local CLI exploration filled gaps for Codex + Gemini (blocked from GitHub Actions at org policy level)
- Key discoveries: Codex has `plugin marketplace add` accepting our format; Gemini has `skills install <local-path>` that detects our SKILL.md directly; Devin reads `.cursor/rules/` + `.windsurf/rules/` natively; Cursor + Windsurf have no headless CLI

**Phase 2b — Design Documents:**
- `docs/PLATFORM_INSPECTION_CATALOG.md` — executable spec, six platform sections, every claim cites verified CLI output from 2026-05-22
- `docs/PLATFORM_VALIDATION_CICD_PLAN.md` — CI/CD design, 10 compat workflows + 5 composite actions + 20 locked decisions across Section 4
- `docs/CI_WHITELIST_REQUEST.md` — copy-pasteable GitHub support ticket for the Codex/Gemini block

**Phase 2c — Critique-Driven Refinement:**
- Two reviewer passes flagged 14 items (4 blockers + 6 important + 4 nice)
- Three rounds of user-decision iteration via `AskUserQuestion`
- 12 items resolved by explicit decision, 1 by npm research (cursor-doctor), 1 by clarification (rules aren't plugin-installable, so `compat-rule.yml` excluded)
- Final reviewer pass: APPROVED FOR IMPLEMENTATION after one minor fix

---

## One Pending Work Phase

### Phase 3 — Multi-Platform Validation Implementation (NOT STARTED)

The design is locked. The implementing agent needs to:

1. Create branch `feat/multi-platform-validation` off `main` (after Phase 1+2 PR #1 merges)
2. Read `docs/PLATFORM_VALIDATION_CICD_PLAN.md` (the spec) and `docs/PLATFORM_INSPECTION_CATALOG.md` (the assertion source)
3. Implement 10 compat workflow files + 5 composite actions per Wave 1–4 phasing in `PLATFORM_VALIDATION_CICD_PLAN.md` Section 8
4. Write 2 local-dev fallback scripts (`scripts/validate-codex-local.sh`, `scripts/validate-gemini-local.sh`) for the platforms blocked from GitHub Actions
5. Estimated effort: ~15–20 hours

The brief to hand to the implementing agent is in `docs/IMPLEMENTING_AGENT_PROMPT.md` (which was written for the migration; the validation implementation will need a similar but new brief — that's the implementer's first task, or can be drafted as a one-paragraph extension of the existing prompt).

---

## How to Build / Test

```bash
uv run scripts/generate_manifest.py           # regenerate _generated/ + cross-platform mirrors
uv run scripts/generate_manifest.py --check   # CI gate: drift-detection mode
uv run tests/test_marketplace.py              # 35+ tests, must all pass
uv run tests/test_marketplace.py -v           # verbose
claude plugin validate _generated/skill-<name> # validate a single plugin manifest
```

Always regenerate and re-run tests before committing. CI does both as separate steps so failures are clearly distinguishable.

---

## Project Layout

```
marketplace/
├── MARKETPLACE.toml                    Single source for identity (owner, version, license)
├── catalog.toml                        Construct-type definitions + skill/rule domain tagging
├── .claude-plugin/marketplace.json     Generated root manifest (71 entries)
├── skills/                             Source content (26 skills)
├── rules/                              Source content (21 rules)
├── examples/                           10 reference plugins (one per construct type)
├── _generated/                         Per-plugin wrappers + bundles
├── .codex/ .gemini/ .cursor/ .windsurf/ .devin/   Cross-platform mirrors
├── activate-installed-rules.sh         Bulk helper for rule activation
├── scripts/generate_manifest.py        The engine
├── tests/test_marketplace.py           Test suite
├── docs/
│   ├── RESUME_HERE.md                  ★ Start here on re-entry
│   ├── GOAL_PLUGIN_COMPLIANCE.md       Migration success criteria
│   ├── PLAN_PLUGIN_COMPLIANCE.md       Migration architecture
│   ├── INVESTIGATION_PLUGIN_DEPENDENCIES.md  Empirical dep-resolution outcome
│   ├── IMPLEMENTING_AGENT_PROMPT.md    Migration implementer brief
│   ├── PLATFORM_INSPECTION_CATALOG.md  Empirical CLI commands per platform (the spec)
│   ├── PLATFORM_VALIDATION_CICD_PLAN.md  CI/CD design + 20 locked decisions
│   ├── CI_WHITELIST_REQUEST.md         Copy-pasteable GitHub support ticket
│   ├── CONSTRUCT_TYPES.md              Index of construct types
│   ├── ADDING_*.md (11 files)          Contributor tutorials
│   ├── SKILL_FORMAT.md  RULE_FORMAT.md  ONBOARDING.md
└── research/                           Market intelligence (read research/README.md first)
```

---

## Architecture Summary

- **Sources of truth**: `MARKETPLACE.toml`, `catalog.toml`, source content under `skills/`, `rules/`, `examples/`. Humans edit these.
- **Generated**: everything in `_generated/`, `.codex/`, `.gemini/`, `.cursor/`, `.windsurf/`, `.devin/`, and `.claude-plugin/marketplace.json`. The generator produces these from sources.
- **Skill or rule bundles** (`skills-<domain>`, `rules-<domain>`, `rules-all`) are content-free plugins whose `plugin.json` declares only `dependencies`. Claude Code auto-installs the dependencies — verified empirically.
- **Rules** install via `/plugin install` then activate via `activate.sh` symlink into `.claude/rules/`. Workaround for the lack of a `rules` field in Claude Code's plugin spec.
- **Multi-platform validation (planned)**: 10 compat workflows organized per-construct (skill, command, agent, hook, mcp, extension, monitor, output-style, theme, marketplace-add) with platform matrix per workflow.

---

## Conventions

- Names: kebab-case for everything (skills, rules, domains, plugin names).
- Python scripts: PEP 723 inline metadata, `uv run`.
- Shell scripts: shebang + `set -euo pipefail`.
- No project-level Python deps (no `pyproject.toml` at root).
- `author` in plugin.json is always an object `{ "name": "...", "url": "..." }`, never a string.
- `source` paths in marketplace.json start with `./`.
- Commit messages have no AI co-author attribution (see `rules/no-ai-credit/`).

---

## Adding Skills / Rules / Anything

Copy `examples/example-<type>/` and adapt. Each construct type has a tutorial in `docs/ADDING_*.md`; for the index, see `docs/CONSTRUCT_TYPES.md`.

General workflow:

1. Edit source content.
2. If skill or rule: add to a domain in `catalog.toml`.
3. `uv run scripts/generate_manifest.py`.
4. `uv run tests/test_marketplace.py`.
5. Commit.

---

## What's Next

In priority order, three independent paths forward:

- **File the GitHub Support whitelist request** — drafted at `docs/CI_WHITELIST_REQUEST.md`. Independent of all engineering work; can happen any time.
- **Merge PR #1** — the migration + design docs land on `main`. After merge, `main` has the full planning dossier.
- **Start multi-platform validation implementation** — create `feat/multi-platform-validation` off `main`; transcribe catalog rows into CI assertions per the locked design. Wave 1 → 4 per `PLATFORM_VALIDATION_CICD_PLAN.md` Section 8.

---

## Known Limitations

- Rule activation is a manual step (`activate.sh`). No native plugin-installable rules in Claude Code yet (feature request open at `anthropics/claude-code#21163`).
- Generator regenerates `_generated/` and mirrors from scratch each run — fast (~1s) but means hand-edits there are always lost.
- Cross-platform mirrors are best-effort. Platform-specific tooling may evolve faster than this repo tracks.
- `@openai/codex` and `@google/gemini-cli` blocked from GitHub Actions at org policy level. CI for those two platforms relies on local-dev fallback scripts (Phase 3 scope) until the whitelist request is granted.

---

## If You're Forgetting Everything

Read `docs/RESUME_HERE.md` first. It has the 30-second tldr, the bookmark of "you are here," the next concrete actions in priority order, the project glossary, the top 10 decisions with rationale, and the dead-ends list. This `HANDOFF.md` is for ongoing tracking; `RESUME_HERE.md` is for re-entry.
