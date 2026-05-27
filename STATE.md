# STATE

> Live within-session truth. Pair with `HANDOFF.md` (between-sessions) and `PITFALLS.md` (cross-session lessons).

## Right now

- **Branch:** `chore/housekeeping-and-roadmap` (PR #10 open, CI pending)
- **Main tip:** `4b00faa` — PR #9 squash-merged
- **Working tree:** clean (this STATE.md update is uncommitted on purpose — live file)
- **Active arc:** **awaiting PR #10 CI** before starting Cursor IDE QA cycle (roadmap item #9)

## Last action taken

Added a standalone Docker image for the hermetic stub. New files: `tests/fixtures/claude-stub/Dockerfile` (uv + Flask via PEP 723, default CMD runs the body dumper on 8089). Updated `tests/fixtures/claude-stub/README.md` with a full Docker workflow section showing the two-container composition (stub + qa-claude sharing netns via `--network container:claude-stub`). Captured request bodies stream to `./.stub-logs/stub-bodies.log` on the host via bind mount. `.stub-logs/` added to `.gitignore`. PITFALLS entry added for the Cursor-IDE port-8089 conflict on Windows that breaks Docker Desktop host-side `-p` mapping (primary workflow doesn't need port mapping so unaffected). Empirically smoke-tested: build succeeds, stub serves correctly inside the container, sibling alpine container reaches the stub via shared netns and bodies appear on host log.

### Prior commit: Implemented Path A — brand-prefixed shared slash namespace, after two rounds of empirical Docker validation confirmed Claude accepts it. The change decouples install names (still unique per plugin) from slash namespace (now shared per construct):

- Install: `claude plugin install skill-example@dgxsparklabs-marketplace` (unchanged)
- Invoke: `/dgxsparklabs-skill:lab-notebook` (was `/skill-example:lab-notebook`)

Source changes: two-line edit to `_base_plugin_shape` in `scripts/constructs.py` + two-line edit to `_make_marketplace_entry` in `scripts/generate_manifest.py` + one test rename in `tests/test_marketplace.py`. Doc cascade across `docs/ADDING_A_CONSTRUCT.md`, `docs/TEST_YOURSELF.md`, `docs/USER_GUIDE.md`, `skills/example/SKILL.md` inline comments. CHANGELOG entry added.

**Pre-merge blocker**: operator runs the 6-step TUI tab-completion recipe at `docs/research/shared-namespace-2026-05-27/RESEARCH.md` § Probe C. Resolver-internals trace already shows the candidate set is well-formed; only the TUI render path remains unverified.

Tests: 77 marketplace + 21 schema-fitness = 98 green. Drift clean.

PR #10 will be at 11 commits after the next push.

### Five prior operator-feedback adoptions (still in this PR):

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
