# STATE

> Live within-session truth. Pair with `HANDOFF.md` (between-sessions), `PITFALLS.md` (specific bug→fix entries), and `docs/LESSONS.md` (working-practice lessons — read before any generator/CI/layout change).

## Status — 2026-06-05

`v1.0.0` is published and `main` is green. The marketplace ships reference/example plugins across all ten construct types — see `docs/INVENTORY.md` for the authoritative entry count. `uv run scripts/tasks.py verify` (drift-check + the four test suites + `claude plugin validate ./`) is green.

### Post-release housekeeping — in flight on stacked branches off `main` (not yet merged)

- **Doc consolidation** (PR #15, branch `docs/consolidation`): archived the market-intel `research/` library and four settled research arcs under `docs/archive/` (history-preserving `git mv`); hard-deleted two stale orphans; de-drifted entry-doc links; added a canonical-docs index to `docs/RESUME_HERE.md`. Docs-only — `--check` clean.
- **Root reorg** (branch `chore/root-reorg`, off `docs/consolidation`): moved `install.sh` / `install.ps1` / `tasks.py` → `scripts/` and `CONTRIBUTING.md` / `CODE_OF_CONDUCT.md` → `docs/`; repointed every consumer (the `compat-agents-cli` workflow, the published `…/main/scripts/install.*` URLs, doc links). `scripts/tasks.py` `ROOT` was fixed for its new location.
- **Documentation sweep** (this session): cut/rewrote/consolidated every live `.md`. Generator-phase descriptions consolidated to `docs/ARCHITECTURE.md` (canonical; corrected against the code to phases 1–7); plugin counts to `docs/INVENTORY.md`; the four test suites to `docs/CONTRIBUTING.md`. Fixed stale `.devin/` mirror references and missing `src/` source-path prefixes, and rewrote the retired rule-install mechanism in `docs/RULE_FORMAT.md`.

### Marketplace shape

- Reference/example plugins for all 10 construct types. Exact counts are generated into `docs/INVENTORY.md` (the single source of truth — do not hardcode counts in prose).
- Rule is not a Claude plugin component (F8): Claude reads rules from `.claude/rules/` via its memory subsystem; rules still surface on Cursor / Codex / Windsurf via the generated mirrors.

### Paused (per `docs/ROADMAP.md`)

- 6-platform QA parity (#9–#14) and multi-instance follow-ups (#37–#42); re-adding the archived production skills/rules (#16–#18).

### Critical-rules adherence

- No AI co-author attribution (per `docs/archive/rules-pre-stable-2026-05-26/no-ai-credit/`). PR-only to `main`; feature branches push freely.
