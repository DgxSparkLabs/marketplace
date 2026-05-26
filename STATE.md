# STATE

> Live within-session truth. Pair with `HANDOFF.md` (between-sessions) and `PITFALLS.md` (cross-session lessons).

## Right now

- **Branch:** `chore/housekeeping-and-roadmap`
- **Main tip:** `4b00faa` — PR #9 squash-merged
- **Working tree:** roadmap + state init + archive moves staged, ready to commit
- **Active arc:** **roadmap-and-housekeeping** — clearing pre-existing untracked state and sequencing next 5 platform QA cycles

## Last action taken

Resolved all five pre-existing untracked items per operator direction:
- `Untitled.md` — already gone from disk
- `docs/PLAN_DI_REFACTOR.md` — deleted empty stub (canonical at `docs/archive/di-refactor/`)
- `docs/research/claude-headless-qa/` — moved to `docs/archive/claude-headless-qa-2026-05-26/`
- `docs/research/claude-qa-2026-05-26/` — moved to `docs/archive/claude-qa-2026-05-26/`
- `docs/research/research/` — added to `.gitignore` (canonical research stash, preserved on disk, not version-controlled)

## What's next

Per the roadmap (see `docs/ROADMAP.md`):

1. Decide disposition for the three untracked research dirs (`docs/research/research/`, `docs/research/claude-headless-qa/`, `docs/research/claude-qa-2026-05-26/`)
2. Begin **Cursor IDE QA cycle** on the minimal example set — first platform after Claude in the locked sequencing
3. Defer `mcp-example` / `skill-example` naming until QA cycles stabilize

## Open decision points (operator-driven)

- F4 visual theme — interactive verification (requires IDE access)
- `compat-headless-claude` CI advisory → required (needs first green run on main)
- `mcp-example` plugin rename → `mcp-fetch` (cosmetic)
- `skill-example` SKILL.md `name:` field — keep `/example-skill` or shorten to `/example`?

## Status

- Tests: 78 marketplace + 21 schema-fitness, last known green on PR #9
- Drift check: clean
- Hermetic Claude CI: advisory (PASS on PR #8 + #9 — promotion candidate)
