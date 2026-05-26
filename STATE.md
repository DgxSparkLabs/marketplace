# STATE

> Live within-session truth. Pair with `HANDOFF.md` (between-sessions) and `PITFALLS.md` (cross-session lessons).

## Right now

- **Branch:** `chore/housekeeping-and-roadmap` (PR #10 open, CI pending)
- **Main tip:** `4b00faa` — PR #9 squash-merged
- **Working tree:** clean (this STATE.md update is uncommitted on purpose — live file)
- **Active arc:** **awaiting PR #10 CI** before starting Cursor IDE QA cycle (roadmap item #9)

## Last action taken

Built `.devcontainer/` for operator QA + marketplace dev: Claude CLI (official Anthropic feature), Node 20, Python 3.12, uv (via curl), Flask, git, gh. Forwards ports 8088/8089 for the hermetic stub. Persists Claude auth across rebuilds via named docker volume scoped to `${devcontainerId}`. Added Setup Option A: Dev Container at the top of `docs/TEST_YOURSELF.md` Claude section.

PR #10: https://github.com/DgxSparkLabs/marketplace/pull/10 — now six-commit bundle:
- `3717127` housekeeping + roadmap + STATE.md + research dir archive moves + .gitignore
- `4d4818b` mcp-example name alignment
- `767b37b` Claude construct reference card (initial — empirically corrected later)
- `a8c74af` Scheme B+ naming alignment across 10 example plugins + reference card empirical corrections
- `dbdac07` 11-issue Claude section audit fix
- (pending commit) dev container

Tests passing locally: 78 marketplace + 21 schema-fitness = 99 green. Drift clean.

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
