# Handoff

> **2026-06-01 SESSION END — NEXT: live-tmux verification of the remaining constructs.** The LSP construct
> was fully built, fixed (incremental-`didChange` bug), made observable (`--always-error` marker + input
> log), and proven LIVE in the container tmux; it's documented in `docs/TEST_YOURSELF.md` cell 4.8.7 (human
> walkthrough + agent tmux operator guide). **Continuation prompt:** [`docs/.research/CONTINUATION-construct-tmux-verification.md`](./docs/.research/CONTINUATION-construct-tmux-verification.md)
> — read it cold to do the same live-tmux proof for command/skill/agent/hook/mcp/monitor/output-style/theme.
> NOTE: this LSP work + several STRAY non-LSP modified files (`CHANGELOG.md`, `scripts/utils.py`,
> `src/MARKETPLACE.toml`, two research docs) are **uncommitted** — do not commit blindly; the stray files are
> not from this work.

> **2026-05-27 SESSION END — NEXT SESSION HAS EXECUTION READY.** Three artifacts at [`docs/research/multi-instance-claude-only-2026-05-27/`](./docs/research/multi-instance-claude-only-2026-05-27/) prepare the next session for direct implementation:
> 1. [`IMPLEMENTOR_PROMPT.md`](./docs/research/multi-instance-claude-only-2026-05-27/IMPLEMENTOR_PROMPT.md) — self-contained brief for a fresh agent to execute cold.
> 2. [`PLAN.md`](./docs/research/multi-instance-claude-only-2026-05-27/PLAN.md) — full execution plan (~440 lines, ~2 hours of work).
> 3. [`OBJECTIVE_CHECKLIST.md`](./docs/research/multi-instance-claude-only-2026-05-27/OBJECTIVE_CHECKLIST.md) — boolean verification checklist for every change.
>
> **What the next session implements**: revert Path A (shared slash namespace) → adopt multi-instance-capable plugins for Claude only; the 5 non-Claude platforms continue emitting unchanged but their multi-instance correctness is acknowledged-unverified via NOTE comments + ROADMAP follow-ups #37-#42. One commit on the existing PR #10 (currently at 12 commits → 13).
>
> **First file to read on re-entry:** [`docs/research/multi-instance-claude-only-2026-05-27/IMPLEMENTOR_PROMPT.md`](./docs/research/multi-instance-claude-only-2026-05-27/IMPLEMENTOR_PROMPT.md). That brief contains everything else you need to read.

> **First file to read on re-entry (general project):** [`docs/RESUME_HERE.md`](./docs/RESUME_HERE.md) — 90-second orientation. This document is the longer state tracker; complements RESUME_HERE rather than duplicating it.

> **2026-05-26 minimal-stable-state transition.** The marketplace was reduced to 10 reference plugins (one per construct type) + 1 cross-construct examples bundle + 8 catch-all bundles = **19 plugin entries** (was 81). The 26 production skills and 21 production rules that previously shipped were **archived, not deleted**, into `docs/archive/skills-pre-stable-2026-05-26/` and `docs/archive/rules-pre-stable-2026-05-26/`. Source preserved via `git mv` so every commit history is intact. Real content returns one plugin at a time after each is verified across every platform. See `CHANGELOG.md` for the full transition rationale.

**Last updated:** 2026-05-24, after PR #1 merged to main (cross-platform native install compliance).
**Branch state:** `main` at `4b00faa`. All 11 CI workflows green on main. Feature branch `feat/claude-plugin-compliance` preserved per user direction.
**Active cleanup branch:** `chore/housekeeping-and-roadmap` (audit-trail commits + footnote drops + this HANDOFF refresh). PR follow-up pending.
**Net status:** Marketplace is genuinely installable on all 6 platforms via each platform's native mechanism. End-to-end CI assertions verify registration → enumeration → install → use for the CLI-native platforms (Claude/Codex/Gemini). Goal met.

---

## What This Is

A **genuinely multi-platform plugin marketplace** for AI coding agents. Installs natively on:

- **Claude Code** — `/plugin marketplace add DgxSparkLabs/marketplace` (CLI shortform)
- **Codex** — `codex plugin marketplace add DgxSparkLabs/marketplace` (CLI shortform)
- **Gemini CLI** — `gemini extensions install https://github.com/DgxSparkLabs/marketplace --consent` (GitHub URL)
- **Cursor IDE** — Dashboard team-marketplace import (paste GitHub URL; Cursor 2.6+)
- **Windsurf IDE** — `git clone` + open (Cascade auto-discovers `.windsurf/rules/` AND `.agents/skills/`)
- **Devin CLI** — `git clone` + `devin skills list` (auto-discovers `.devin/skills/` AND `.agents/skills/`)

Current inventory — see [`docs/INVENTORY.md`](./docs/INVENTORY.md) (generated, authoritative) for the exact per-platform plugin-entry counts. Do not hardcode counts here; that file is the source of truth.

- Example skills/rules ship under `src/<construct>/`; pre-stable production content is archived under `docs/archive/skills-pre-stable-2026-05-26/` and `docs/archive/rules-pre-stable-2026-05-26/`.
- `.claude-plugin/marketplace.json` lists Claude-supported individuals + catalog bundles. Per-construct catch-alls retired 2026-05-27.
- `.cursor-plugin/marketplace.json` lists Cursor's supported subset (rules + skills + agent + command + hook + mcp).
- Tests: run all three suites — `tests/test_marketplace.py` + `tests/test_schema_fitness.py` + `tests/test_agents_cli.py`.

---

## Completed Work Phases (5 total)

### Phase 1 — Plugin Compliance Migration (DONE)
Migrated from curl-bash + Textual TUI installer to native Claude Code `/plugin marketplace add`. Built v1 of `scripts/generate_manifest.py`. See [`docs/archive/phase-1-compliance/INVESTIGATION_PLUGIN_DEPENDENCIES.md`](./docs/archive/phase-1-compliance/INVESTIGATION_PLUGIN_DEPENDENCIES.md).

### Phase 2 — Multi-Platform Validation Implementation (DONE)
Built 10 `compat-*.yml` workflows + 5 composite actions. All green. Wave 4 promoted Codex/Gemini matrix entries from `continue-on-error: true` to `false`. See [`docs/archive/phase-2-validation/VERIFICATION_REPORT.md`](./docs/archive/phase-2-validation/VERIFICATION_REPORT.md), [`docs/archive/phase-2-validation/FIX_REPORT.md`](./docs/archive/phase-2-validation/FIX_REPORT.md), [`docs/archive/phase-2-validation/FINALIZATION_REPORT.md`](./docs/archive/phase-2-validation/FINALIZATION_REPORT.md).

### Phase 3 — Examples In Native Folders (DONE)
Restructured `examples/example-<construct>/` → `<construct>/example/`. Eliminated catalog/code asymmetry. See [`docs/archive/restructure/RESTRUCTURE_REPORT.md`](./docs/archive/restructure/RESTRUCTURE_REPORT.md).

### Phase 4 — Dependency-Injection Refactor (DONE)
Refactored generator from procedural per-construct code (~600 lines of special cases) to a strategy-pattern architecture: `scripts/utils.py`, `scripts/constructs.py` (10 Construct classes), `scripts/platforms.py` (initially 6 Platform classes), `scripts/bundles.py`, `scripts/generate_manifest.py` (thin orchestrator, 5 phases). 25 locked decisions in [`docs/archive/di-refactor/PLAN_DI_REFACTOR.md`](./docs/archive/di-refactor/PLAN_DI_REFACTOR.md). Implementation: [`docs/archive/di-refactor/DI_REFACTOR_REPORT.md`](./docs/archive/di-refactor/DI_REFACTOR_REPORT.md). Validation: [`docs/archive/di-refactor/DI_REFACTOR_VALIDATION_REPORT.md`](./docs/archive/di-refactor/DI_REFACTOR_VALIDATION_REPORT.md).

### Phase 5 — Cross-Platform Native Install Compliance (DONE — most recent session)

Verification round exposed that the README documented install commands that didn't fully work: Codex per-plugin install errored with `missing or invalid plugin.json`, Gemini GitHub URL install errored with `Configuration file not found`, Windsurf couldn't see skills, Cursor team-marketplace had no manifest to import. Compat CI only tested marketplace registration, missing enumeration + install.

**Plan**: [`docs/archive/phase-5-cross-platform-install/PLAN_CROSS_PLATFORM_INSTALL_FIX.md`](./docs/archive/phase-5-cross-platform-install/PLAN_CROSS_PLATFORM_INSTALL_FIX.md) (v2, 4 locked decisions A1/B2/C1/Q2).

**Verification artifacts** (`docs/archive/phase-5-cross-platform-install/VERIFICATION_2026-05/`):
- [`SUMMARY.md`](./docs/archive/phase-5-cross-platform-install/VERIFICATION_2026-05/SUMMARY.md) — ground-truth synthesis
- [`empirical_act_verification.md`](./docs/archive/phase-5-cross-platform-install/VERIFICATION_2026-05/empirical_act_verification.md) — per-claim table (C1-C7 Codex, G1-G6 Gemini, CU1-CU3 Cursor, CL1-CL3 Claude)
- [`cursor.md`](./docs/archive/phase-5-cross-platform-install/VERIFICATION_2026-05/cursor.md) — Cursor IDE + CLI WebFetch research (overturned prior "no CLI" conclusion)
- [`IMPLEMENTATION_REPORT.md`](./docs/archive/phase-5-cross-platform-install/VERIFICATION_2026-05/IMPLEMENTATION_REPORT.md) — implementer's commit-by-commit report
- [`IMPLEMENTATION_VALIDATION.md`](./docs/archive/phase-5-cross-platform-install/VERIFICATION_2026-05/IMPLEMENTATION_VALIDATION.md) — validator's APPROVED verdict
- [`README_REWRITE_PREVIEW.md`](./docs/archive/phase-5-cross-platform-install/VERIFICATION_2026-05/README_REWRITE_PREVIEW.md) + [`README_REWRITE_REPORT.md`](./docs/archive/phase-5-cross-platform-install/VERIFICATION_2026-05/README_REWRITE_REPORT.md) — Phase 2 README work
- [`workflows/`](./docs/archive/phase-5-cross-platform-install/VERIFICATION_2026-05/workflows/) — act verification scaffolds
- [`logs/`](./docs/archive/phase-5-cross-platform-install/VERIFICATION_2026-05/logs/) — full container logs + per-claim text snippets
- [`reproduce.ps1`](./docs/archive/phase-5-cross-platform-install/VERIFICATION_2026-05/reproduce.ps1) — full reproduction script

**Generator changes** (commits 534cfac through 654bfca on the feature branch, merged as `bfb476d`):
- Extended Platform protocol with `build_plugin_json(construct, name) -> dict`
- Added `AgentsPlatform` class (7th platform) emitting `.agents/skills/` (read by Windsurf, Cursor, Devin natively)
- Added per-plugin native manifest emission gated on `platform.supports`:
  - `_generated/<plugin>/.codex-plugin/plugin.json` per Codex-supported plugin
  - `_generated/<plugin>/.cursor-plugin/plugin.json` per Cursor-supported plugin
- New generator Phase 1.5 (per-plugin manifests), Phase 4.5 (root-level `gemini-extension.json`), Phase 6 (root-level `.cursor-plugin/marketplace.json`)
- Mirror dir hygiene: `shutil.copytree` ignore patterns exclude cross-platform manifest dirs
- CI extensions: `compat-marketplace-add.yml` Codex job now asserts enumeration + install; Claude job asserts install + list; `compat-extension.yml` has new `gemini-github-url-install` job
- 18 new tests in `tests/test_marketplace.py` (52 total now)

**End-to-end empirical proof** (real GHA on main, post-merge):
- Claude install chain (registration → install → list): PASS
- Codex marketplace add + plugin list + plugin add: PASS
- Codex GitHub shortform without `--ref` against main: PASS (post-merge; was the last gap)
- Gemini GitHub URL install + extension list: PASS
- All 11 CI workflows green on main at `bfb476d`

---

## What's Next

The goal is met. Remaining is polish / future-proofing:

1. **(In progress) Merge the post-merge cleanup PR** (`docs/post-merge-cleanup` branch) which commits the verification audit trail + drops `--ref` footnotes + refreshes this HANDOFF.md.

2. **(Optional) Retire `.devin/skills/` mirror** in favor of `.agents/skills/` alone — Devin reads both per `devin skills paths` empirical evidence; collapse is byte-saving cleanup.

3. **(Optional) Investigate G4 (Gemini remote skill install with `--path`)** — currently fails with "No valid skills found" but local install succeeds; understanding Gemini's remote validation requirements is a side concern.

4. **(Optional) Cursor `agent --plugin-dir` runtime injection** — the Cursor CLI exposes a `--plugin-dir <path>` flag for loading a local plugin dir at runtime. Worth exploring for testing scenarios; not for end-user install.

5. **(Long-term) Maintenance** — as platforms evolve (e.g., when native rule install ships in Claude Code, retire `activate.sh` workaround per `docs/RULE_FORMAT.md`).

---

## How to Build / Test

```bash
uv run scripts/generate_manifest.py           # regenerate everything from sources
uv run scripts/generate_manifest.py --check   # CI gate: drift-detection mode
uv run tests/test_marketplace.py              # must all pass
uv run tests/test_schema_fitness.py           # schema fitness suite
uv run tests/test_agents_cli.py               # agents-cli suite
```

For hermetic CI re-verification before pushing:

```powershell
# From repo root, runs all 4 verify workflows in Docker containers via act:
docs/archive/phase-5-cross-platform-install/VERIFICATION_2026-05/reproduce.ps1
```

---

## Project Layout (post-Phase-5)

```
marketplace/
├── MARKETPLACE.toml                    Identity (owner, version, license)
├── catalog.toml                        Bundles only
├── README.md                           Per-platform install + GitHub-Direct Install Support matrix
├── HANDOFF.md                          This file
├── gemini-extension.json               Root-level for `gemini extensions install <github-url>` (Phase 4.5)
├── .claude-plugin/marketplace.json     Claude marketplace manifest (entry count: docs/INVENTORY.md, authoritative)
├── .cursor-plugin/marketplace.json     Cursor team-marketplace manifest (entry count: docs/INVENTORY.md; Phase 6)
├── .agents/skills/<name>/              Cross-platform skill mirror (Windsurf+Cursor+Devin; Phase 1.5 of Phase 5)
├── src/<construct>/<name>/             Sources now live under src/ (cd7a7d8 reorg): src/skills/, src/rules/,
│   src/commands/, src/agents/, src/hooks/, src/mcp-servers/, src/lsp-servers/, src/monitors/,
│   src/output-styles/, src/themes/ — each with its example/ (e.g. src/skills/example-single/)
├── _generated/<plugin>/                Per-plugin wrappers; now contains:
│   ├── .claude-plugin/plugin.json     (always, written by Construct.emit in Phase 1)
│   ├── .codex-plugin/plugin.json      (where type(construct) ∈ CodexPlatform.supports; Phase 1.5)
│   └── .cursor-plugin/plugin.json     (where type(construct) ∈ CursorPlatform.supports; Phase 1.5)
├── .codex/, .gemini/, .cursor/, .windsurf/, .devin/   Cross-platform mirrors
├── activate-installed-rules.sh         Bulk rule activation helper
├── .github/
│   ├── workflows/ci.yml                Manifest drift check + test suite
│   ├── workflows/compat-*.yml (10)     Per-construct multi-platform validation
│   │   - compat-marketplace-add.yml: Claude+Codex registration+enum+install (Phase 5 extensions)
│   │   - compat-extension.yml: Gemini local install + GitHub URL install (Phase 5 extension)
│   └── actions/setup-<platform>/ (5)   Composite actions per platform
├── scripts/
│   ├── utils.py                        Shared helpers
│   ├── constructs.py                   10 Construct classes
│   ├── platforms.py                    7 Platform classes (Claude, Codex, Gemini, Cursor, Windsurf, Devin, AgentsPlatform)
│   ├── bundles.py                      Bundle dataclass + load_bundles
│   ├── generate_manifest.py            6-phase orchestrator (was 5; added 1.5/4.5/6 in Phase 5)
│   ├── validate-codex-local.sh         Local-dev Codex validation
│   └── validate-gemini-local.sh        Local-dev Gemini validation
├── tests/                              test_marketplace.py + test_schema_fitness.py + test_agents_cli.py
├── docs/
│   ├── RESUME_HERE.md                  ★ Start here on re-entry
│   ├── PLATFORMS.md                    Per-platform install/support/discovery/CI reference (master doc)
│   ├── ARCHITECTURE.md                 Generator architecture — Construct/Platform/Bundle protocols (master doc)
│   ├── CONSTRUCT_TYPES.md, ADDING_A_CONSTRUCT.md   Reference
│   ├── SKILL_FORMAT.md, RULE_FORMAT.md  Format references
│   └── archive/                        Historical arc material (audit trail; preserved via git mv)
│       ├── di-refactor/                Phase 4 plan + critiques + report + validation (5 files)
│       ├── phase-1-compliance/         Phase 1 plan + goal + implementer prompt + dependency investigation (4 files)
│       ├── phase-2-validation/         Phase 2 CI plan + 3 cycle reports + catalog + org-policy investigation (7 files)
│       ├── phase-5-cross-platform-install/  Phase 5 plan + VERIFICATION_2026-05/ tree (logs, workflows, reports, reproduce.ps1)
│       ├── empirical-cli-findings/     Phase 2 raw per-platform CLI research (6 files)
│       ├── restructure/                RESTRUCTURE_REPORT (Phase 3 outcome)
│       ├── processes/                  REENTRY_TEST_PROTOCOL (orientation-kit test process)
│       ├── consolidation-2026-05/      DOC_INVENTORY_2026-05-24.md (this consolidation arc)
│       ├── ONBOARDING.md, pr1-body.md  Orphans
│       ├── CONTRIBUTING_pre-consolidation.md  Pre-rewrite copy of CONTRIBUTING.md
│       └── pre-1.0-pitfalls.md         Pre-DI-refactor pitfalls knowledge base
└── research/                           Market intelligence
```

---

## Architecture Summary

- **Sources of truth**: `MARKETPLACE.toml`, `catalog.toml`, source content under `src/<construct>/<name>/` (cd7a7d8 reorg). Humans edit these.
- **Generated**: `_generated/`, `.codex/`, `.gemini/`, `.cursor/`, `.windsurf/`, `.devin/`, `.agents/`, `.claude-plugin/marketplace.json`, `.cursor-plugin/marketplace.json`, `gemini-extension.json` (root). Generator produces all from sources.
- **Construct classes** (10, in `scripts/constructs.py`) encapsulate per-construct build + emit. New construct = new class + registry entry.
- **Platform classes** (7, in `scripts/platforms.py`) encapsulate per-platform mirror + `build_plugin_json` + `supports`. New platform = new class + registry entry.
- **`supports`-gated emission** (Phase 5 / Decision B2): per-platform per-plugin manifests are written only where `type(construct) in platform.supports`. Adding a platform/construct automatically updates manifest emission via the protocol; no special cases.
- **Bundles**: catalog only (`catalog.toml [bundle.*]` → Phase 2a). Per-construct code-generated catch-alls (Phase 2b) retired 2026-05-27 — they cluttered the marketplace listing without curation value.
- **Rules**: install via `/plugin install` then activate via `activate.sh` symlink. Workaround for Claude Code's lack of native `rules` field. See `docs/RULE_FORMAT.md`.
- **Multi-platform validation**: 10 compat workflows on push/PR; Phase 5 added enumeration + install assertions for Claude/Codex/Gemini. Verified end-to-end on main at `4b00faa`.

---

## Conventions

- Names: kebab-case for everything.
- Python: PEP 723 inline metadata, `uv run`. Python 3.11+ (`match`, `Protocol[runtime_checkable]`).
- Shell: shebang + `set -euo pipefail`.
- No project-level Python deps.
- `author` in plugin.json is always `{ "name": "...", "url": "..." }`.
- `source` paths in marketplace.json start with `./`.
- Commit messages: no AI co-author attribution (see `rules/no-ai-credit/`).
- New verification rounds get their own `docs/VERIFICATION_<YYYY-MM>/` subdirectory.

---

## Adding Skills / Rules / Anything

See [`docs/ADDING_A_CONSTRUCT.md`](./docs/ADDING_A_CONSTRUCT.md). General workflow:

1. Copy `src/<construct>/example/` to `src/<construct>/<your-name>/`
2. Edit the copied content
3. (Optional) Add to a bundle in `catalog.toml` — bundles are optional curation; a construct is installable without bundle membership (the requirement was removed)
4. `uv run scripts/generate_manifest.py`
5. Run the three test suites (`tests/test_marketplace.py`, `tests/test_schema_fitness.py`, `tests/test_agents_cli.py`)
6. Commit (no AI co-author attribution)

The new per-platform per-plugin manifests (`.codex-plugin/`, `.cursor-plugin/`) are auto-generated; you don't write them by hand.

---

## Known Limitations

- Rule activation is a manual step (`activate.sh`). No native plugin-installable rules in Claude Code yet (feature request open at `anthropics/claude-code#21163`).
- Generator regenerates from scratch — hand-edits in `_generated/`, mirrors, or root manifest copies are lost.
- Cursor IDE plugin install is GUI-only (Dashboard or `/add-plugin` in editor chat) — no CLI install path. The `agent` CLI exists but has no plugin commands.
- Windsurf has no headless CLI at all.
- Devin's installer exits 1 in non-TTY (binary still lands; CI works around with `|| true`).
- Gemini's `extensions list` and `mcp list` write to stderr — pipes must use `2>&1`.
- G4 (Gemini remote skill install with `--path`) currently fails for unclear validation reasons; local install works fine. Side concern.

---

## If You're Forgetting Everything

Read [`docs/RESUME_HERE.md`](./docs/RESUME_HERE.md) first. It has the 30-second TLDR, "you are here," next concrete actions, project glossary, platform-by-platform install paths, and dead-ends list. This `HANDOFF.md` complements it with the longer history + full layout + architecture summary.
