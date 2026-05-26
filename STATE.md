# STATE

> Live within-session truth. Pair with `HANDOFF.md` (between-sessions) and `PITFALLS.md` (cross-session lessons).

## Right now

- **Branch:** `chore/housekeeping-and-roadmap` (PR #10 open, CI pending)
- **Main tip:** `4b00faa` — PR #9 squash-merged
- **Working tree:** clean (this STATE.md update is uncommitted on purpose — live file)
- **Active arc:** **awaiting PR #10 CI** before starting Cursor IDE QA cycle (roadmap item #9)

## Last action taken

Opened PR #10: https://github.com/DgxSparkLabs/marketplace/pull/10 — three-commit bundle:
- `3717127` housekeeping + roadmap + STATE.md + research dir archive moves + .gitignore
- `4d4818b` mcp-example name alignment (three-name mismatch → single `mcp-example`/`example` family)
- (pending commit) Claude construct reference card in `docs/TEST_YOURSELF.md` — exact strings to type per construct + expected output strings. Also discovered systemic name-chain mismatch across 9 example plugins (only mcp aligned, others still flipped); added as roadmap follow-up #33.

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
