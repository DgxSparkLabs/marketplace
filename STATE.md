# STATE

> Live within-session truth. Pair with `HANDOFF.md` (between-sessions) and `PITFALLS.md` (cross-session lessons).

## Right now

- **Branch:** `chore/housekeeping-and-roadmap` (PR #10 open, CI pending)
- **Main tip:** `4b00faa` — PR #9 squash-merged
- **Working tree:** clean (this STATE.md update is uncommitted on purpose — live file)
- **Active arc:** **awaiting PR #10 CI** before starting Cursor IDE QA cycle (roadmap item #9)

## Last action taken

Five operator-feedback adoptions in one batch:

1. **Retired per-construct catch-all bundles** (`bundle-skill-all` etc.). Phase 2b loop deleted from `scripts/generate_manifest.py`; reserved-name check in `scripts/bundles.py` removed; tests, catalog, README, HANDOFF, USER_GUIDE, PLATFORMS, ARCHITECTURE, CONSTRUCT_TYPES, ADDING_A_CONSTRUCT, RESUME_HERE all updated. Plugin entry count 19 → **10** (9 individuals + 1 catalog bundle `bundle-examples`).

2. **`docs/TEST_YOURSELF.md` Step 3 jq filter.** Operator's `jq --arg mp ... '[.. | objects | select(.marketplaceName? == $mp)]'` pattern replaces the arbitrary `head -50` truncation — filters by marketplace name properly.

3. **Setup option B Docker now includes Flask + uv install steps.** `curl -LsSf https://astral.sh/uv/install.sh | sh` step added; Flask still self-bootstraps via PEP 723 in the stubs.

4. **New `docs/ADDING_A_CONSTRUCT.md` "Where do the names come from?" section.** Walks through the three name layers (marketplace / plugin / component) with `skill-example`/`lab-notebook` as the worked example. Answers the operator's "what command do I need to run when I add a new skill?" — `uv run scripts/generate_manifest.py`. `docs/TEST_YOURSELF.md` links to this near the reference card.

5. **Updated CHANGELOG with full retirement note + counts table.**

Tests: 77 marketplace + 21 schema-fitness = **98 green** (was 99; the dropped catch-all-reserved-name test is gone). Drift clean.

PR #10: https://github.com/DgxSparkLabs/marketplace/pull/10 — soon 9-commit bundle.

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
