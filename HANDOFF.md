# Handoff

> **First file to read on re-entry:** [`docs/RESUME_HERE.md`](./docs/RESUME_HERE.md) — 90-second orientation. This document is the longer state tracker; complements RESUME_HERE rather than duplicating it.

**Last updated:** 2026-05-24, end of DI-refactor session
**Branch state:** `feat/claude-plugin-compliance` at commit `a872e69` (TOC addition). PR #1 open: https://github.com/DgxSparkLabs/marketplace/pull/1 — **MERGEABLE, awaiting merge call**.
**Net status:** Every work phase complete. CI green. README rewritten with per-platform install + use examples. The only decision left is "merge or not."

---

## What This Is

A **Claude Code plugin marketplace** for AI coding agents. Natively installable via `/plugin marketplace add DgxSparkLabs/marketplace`, with auto-generated mirrors for Devin CLI, Cursor, Windsurf, Codex CLI, and Gemini CLI.

Current inventory (post-refactor):

- **26 skills** (`skills/<name>/`) + `skills/example/`
- **21 rules** (`rules/<name>/`) + `rules/example/`
- **`commands/`, `agents/`, `hooks/`, `mcp-servers/`, `lsp-servers/`, `monitors/`, `output-styles/`, `themes/`** — each has `example/` (real content TBD as Claude Code's plugin spec stabilizes)
- **81 plugin entries** in `.claude-plugin/marketplace.json`:
  - 26 individual skills (`skill-<name>`) + 1 `skill-example`
  - 21 individual rules (`rule-<name>`) + 1 `rule-example`
  - 8 individual examples for the other constructs (`command-example`, `agent-example`, `hook-example`, `mcp-example`, `lsp-example`, `monitor-example`, `output-style-example`, `theme-example`)
  - 8 skill domain bundles (`bundle-<domain>-skills`)
  - 5 rule domain bundles (`bundle-<domain>-rules`)
  - 10 catch-all bundles (`bundle-skill-all`, `bundle-rule-all`, ..., `bundle-theme-all`) — code-generated
  - 1 cross-construct `bundle-examples` (one of every construct's example)
- **250+ research sources** across 12 rounds in `research/`

---

## Completed Work Phases (4 total)

### Phase 1 — Plugin Compliance Migration (DONE, merged via Option D restructure)

Migrated from curl-bash + Textual TUI installer to native Claude Code `/plugin marketplace add`. Built the first version of `scripts/generate_manifest.py`. Wrote 12 contributor tutorials. Verified empirically that Claude Code auto-installs plugin dependencies (see [`docs/INVESTIGATION_PLUGIN_DEPENDENCIES.md`](./docs/INVESTIGATION_PLUGIN_DEPENDENCIES.md)).

### Phase 2 — Multi-Platform Validation Implementation (DONE)

Built 10 `compat-*.yml` workflows + 5 composite actions + 2 local-dev fallback scripts. All 10 compat workflows + the existing CI workflow run green on every push. Wave 4 promoted: Codex/Gemini matrix entries flipped from `continue-on-error: true` to `false` after the empirically-discovered transient install block lifted. Detailed reports: [`docs/VERIFICATION_REPORT.md`](./docs/VERIFICATION_REPORT.md), [`docs/FIX_REPORT.md`](./docs/FIX_REPORT.md), [`docs/FINALIZATION_REPORT.md`](./docs/FINALIZATION_REPORT.md).

### Phase 3 — Examples In Native Folders (DONE)

Restructured examples from a centralized `examples/example-<construct>/` layout to native `<construct>/example/` directories. Eliminated the catalog/code asymmetry where skills and rules were privileged. See [`docs/RESTRUCTURE_REPORT.md`](./docs/RESTRUCTURE_REPORT.md).

### Phase 4 — Dependency-Injection Refactor (DONE — most recent session)

Refactored the generator from per-construct procedural code (~600 lines of special cases) to a strategy-pattern architecture:

- `scripts/utils.py` — shared helpers
- `scripts/constructs.py` — 10 Construct classes + `CONSTRUCTS` registry (each with `build_plugin_json` + `emit`)
- `scripts/platforms.py` — 6 Platform classes + `PLATFORMS` registry
- `scripts/bundles.py` — `Bundle` dataclass + parser with reserved-name validation
- `scripts/generate_manifest.py` — thin orchestrator, 5 phases (~120 lines)
- `catalog.toml` reduced from 258 to 161 lines — bundle definitions only
- Examples renamed `example-<construct>` → `example` (so plugin names are `skill-example`, `mcp-example`, etc., not `example-skill`, `example-mcp`)
- 11 `ADDING_*.md` docs consolidated to 1 `ADDING_A_CONSTRUCT.md`
- README rewritten with per-platform install + use examples (verified empirically; no fabricated commands)
- README TOC added (`a872e69`)

Plan: [`docs/PLAN_DI_REFACTOR.md`](./docs/PLAN_DI_REFACTOR.md). Reviewer findings: [`docs/PLAN_DI_REFACTOR_CRITIQUE.md`](./docs/PLAN_DI_REFACTOR_CRITIQUE.md), [`docs/PLAN_DI_REFACTOR_CRITIQUE_V2.md`](./docs/PLAN_DI_REFACTOR_CRITIQUE_V2.md). Implementation report: [`docs/DI_REFACTOR_REPORT.md`](./docs/DI_REFACTOR_REPORT.md). Validation: [`docs/DI_REFACTOR_VALIDATION_REPORT.md`](./docs/DI_REFACTOR_VALIDATION_REPORT.md) — verdict: "validated, ready to merge."

---

## What's Next

In priority order:

1. **Review and merge PR #1** (`feat/claude-plugin-compliance` → `main`). Everything is on this branch; this is the single remaining decision. `gh pr merge 1 --merge` (or `--squash`, your call).
2. **(Optional) File the GitHub Support whitelist request** — [`docs/CI_WHITELIST_REQUEST.md`](./docs/CI_WHITELIST_REQUEST.md). Likely moot per [`docs/ORG_POLICY_INVESTIGATION.md`](./docs/ORG_POLICY_INVESTIGATION.md) (no policy was ever in effect; the original "block" was a transient infrastructure event). Submit only if a similar incident recurs.
3. **(Optional) Update validation CI for new construct contributions** as Claude Code's plugin spec evolves (e.g., when native rule install ships, retire the `activate.sh` workaround per `docs/RULE_FORMAT.md`).

---

## How to Build / Test

```bash
uv run scripts/generate_manifest.py           # regenerate _generated/ + cross-platform mirrors
uv run scripts/generate_manifest.py --check   # CI gate: drift-detection mode
uv run tests/test_marketplace.py              # 34 tests, must all pass
uv run tests/test_marketplace.py -v           # verbose
```

Always regenerate and re-run tests before committing. CI does both as separate steps so failures are clearly distinguishable.

---

## Project Layout

```
marketplace/
├── MARKETPLACE.toml                    Single source for identity (owner, version, license)
├── catalog.toml                        Bundles only (no [construct.*], no [<>_domain.*])
├── README.md                           Per-platform install + use examples (392 lines, TOC at top)
├── .claude-plugin/marketplace.json     Generated root manifest (81 entries)
├── skills/<name>/                      Real skills + skills/example/
├── rules/<name>/                       Real rules + rules/example/
├── commands/example/                   Example only (no real commands yet)
├── agents/example/, hooks/example/, mcp-servers/example/, lsp-servers/example/,
│   monitors/example/, output-styles/example/, themes/example/   Examples only
├── _generated/                         Per-plugin wrappers + bundles
├── .codex/, .gemini/, .cursor/, .windsurf/, .devin/   Cross-platform mirrors
├── activate-installed-rules.sh         Bulk helper for rule activation
├── .github/
│   ├── workflows/ci.yml                Manifest drift check + test suite
│   ├── workflows/compat-*.yml (10)     Per-construct multi-platform validation
│   └── actions/setup-<platform>/ (5)   Composite actions per platform
├── scripts/utils.py                    Shared helpers
├── scripts/constructs.py               10 Construct classes + CONSTRUCTS registry
├── scripts/platforms.py                6 Platform classes + PLATFORMS registry
├── scripts/bundles.py                  Bundle dataclass + load_bundles + BundleMember
├── scripts/generate_manifest.py        Thin orchestrator (5 phases)
├── scripts/validate-codex-local.sh     Local-dev Codex validation
├── scripts/validate-gemini-local.sh    Local-dev Gemini validation
├── tests/test_marketplace.py           34 tests
├── docs/
│   ├── RESUME_HERE.md                  ★ Start here on re-entry (90-second orientation)
│   ├── PLAN_DI_REFACTOR.md             DI refactor architecture + 25 locked decisions
│   ├── PLAN_DI_REFACTOR_CRITIQUE.md    v1 reviewer findings
│   ├── PLAN_DI_REFACTOR_CRITIQUE_V2.md v2 reviewer findings
│   ├── DI_REFACTOR_REPORT.md           Implementation report (snapshot diff + CI results)
│   ├── DI_REFACTOR_VALIDATION_REPORT.md Post-impl validator's verdict
│   ├── GOAL_PLUGIN_COMPLIANCE.md       Migration success criteria (original)
│   ├── PLAN_PLUGIN_COMPLIANCE.md       Migration architecture (original)
│   ├── INVESTIGATION_PLUGIN_DEPENDENCIES.md  Empirical dep auto-install proof
│   ├── PLATFORM_INSPECTION_CATALOG.md  Canonical CLI commands per platform
│   ├── PLATFORM_VALIDATION_CICD_PLAN.md  Validation CI design + 20 locked decisions
│   ├── EMPIRICAL_CLI_FINDINGS/         Raw research notes per platform
│   ├── ORG_POLICY_INVESTIGATION.md     Root-cause analysis (transient install block)
│   ├── RESTRUCTURE_REPORT.md           Phase 3 restructure outcome
│   ├── CONSTRUCT_TYPES.md              Concise reference table
│   ├── ADDING_A_CONSTRUCT.md           Single contributor tutorial (consolidates the old 11)
│   ├── SKILL_FORMAT.md, RULE_FORMAT.md, ONBOARDING.md  Format references
│   └── (earlier-cycle reports: VERIFICATION, FIX, FINALIZATION)
└── research/                           Market intelligence (research/README.md first)
```

---

## Architecture Summary

- **Sources of truth**: `MARKETPLACE.toml`, `catalog.toml`, source content under `<construct>/<name>/`. Humans edit these.
- **Generated**: `_generated/`, `.codex/`, `.gemini/`, `.cursor/`, `.windsurf/`, `.devin/`, `.claude-plugin/marketplace.json`. The generator produces these from sources.
- **Construct classes** (in `scripts/constructs.py`) encapsulate each of the 10 plugin types' build + emit logic. Adding a new construct = new class + entry in `CONSTRUCTS` registry.
- **Platform classes** (in `scripts/platforms.py`) encapsulate each of the 6 platforms' mirror logic and which constructs they `supports`. Adding a new platform = new class + entry in `PLATFORMS` registry.
- **Bundles** are dep-only plugins. Two kinds:
  - **Catalog bundles**: declared in `catalog.toml` `[bundle.*]` with explicit `members`. Generator's Phase 2a emits them.
  - **Catch-all bundles**: `bundle-<prefix>-all`, one per construct. Code-generated by Phase 2b. NOT in catalog.toml; catalog parsing rejects reserved names.
- **Rules** install via `/plugin install` then activate via `activate.sh` symlink into `.claude/rules/`. Workaround for the lack of a `rules` field in Claude Code's plugin spec. See `docs/RULE_FORMAT.md`.
- **Multi-platform validation**: 10 compat workflows in `.github/workflows/compat-*.yml` organized per-construct with platform matrix per workflow. Verified end-to-end empirically.

---

## Conventions

- Names: kebab-case for everything (skills, rules, domains, plugin names, bundle names).
- Python scripts: PEP 723 inline metadata, `uv run`. Python 3.11+ (uses `match` statement + `Protocol[runtime_checkable]`).
- Shell scripts: shebang + `set -euo pipefail`.
- No project-level Python deps (no `pyproject.toml` at root).
- `author` in plugin.json is always an object `{ "name": "...", "url": "..." }`, never a string.
- `source` paths in marketplace.json start with `./`.
- Commit messages have no AI co-author attribution (see `rules/no-ai-credit/`).

---

## Adding Skills / Rules / Anything

See [`docs/ADDING_A_CONSTRUCT.md`](./docs/ADDING_A_CONSTRUCT.md) — single tutorial covering all 10 construct types.

General workflow:

1. Copy `<construct>/example/` to `<construct>/<your-name>/`
2. Edit the copied content
3. If skill or rule: add to a bundle in `catalog.toml` (existing or new `[bundle.<your-domain>-<construct>]`)
4. `uv run scripts/generate_manifest.py`
5. `uv run tests/test_marketplace.py`
6. Commit (no AI co-author attribution)

---

## Known Limitations

- Rule activation is a manual step (`activate.sh`). No native plugin-installable rules in Claude Code yet (feature request open at `anthropics/claude-code#21163`).
- Generator regenerates `_generated/` and mirrors from scratch each run — fast (~1s) but means hand-edits there are always lost.
- Cross-platform mirrors are best-effort. Platform-specific tooling may evolve faster than this repo tracks.
- Cursor and Windsurf have no headless CLI. Clone-and-detect is the only install path.
- Devin's installer exits 1 in non-TTY environments (binary lands at `~/.local/bin/devin` regardless; CI works around this with `|| true`).
- Gemini's `extensions list` and `mcp list` write output to stderr — pipes must use `2>&1`.

---

## If You're Forgetting Everything

Read [`docs/RESUME_HERE.md`](./docs/RESUME_HERE.md) first. It has the 30-second tldr, the "you are here" bookmark, the next concrete actions in priority order, the project glossary, the top decisions with rationale, and the dead-ends list. This `HANDOFF.md` is for ongoing tracking; `RESUME_HERE.md` is for re-entry.
