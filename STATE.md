# STATE

> Live within-session truth. Pair with `HANDOFF.md` (between-sessions) and `PITFALLS.md` (cross-session lessons).

## Right now

- **Branch:** `chore/housekeeping-and-roadmap` (PR #10 open, CI pending)
- **Main tip:** `4b00faa` — PR #9 squash-merged
- **Working tree:** clean (this STATE.md update is uncommitted on purpose — live file)
- **Active arc:** **awaiting PR #10 CI** before starting Cursor IDE QA cycle (roadmap item #9)

## Last action taken

Fixed two real bugs from operator's first dev container run:
1. **Flask missing** — `apt-get install python3-flask` in post-create.sh either failed or installed somewhere Python3 didn't find. Replaced with PEP 723 inline metadata in both stub files (`stub.py`, `stub_body_dumper.py`); `uv run` now fetches Flask into an ephemeral env on first invocation. No apt, no pip install, no virtualenv to activate. Matches AGENTS.md "always use uv" rule.
2. **EACCES on /home/vscode/.claude/plugins** — the named docker volume was mounted root-owned, so `claude plugin marketplace add` couldn't mkdir. Added `sudo chown` in post-create.sh to fix it. Canonical pattern from Anthropic reference container.

Smoke-tested locally: `uv run tests/fixtures/claude-stub/stub.py` resolves Flask (8 packages, 528ms) and starts the server. Tests still pass.

Touched files:
- `tests/fixtures/claude-stub/stub.py` + `stub_body_dumper.py` — added PEP 723 + uv-run shebang
- `tests/fixtures/claude-stub/README.md` — quick-start now uses `uv run`
- `.devcontainer/post-create.sh` — chown for the volume; dropped apt flask
- `.devcontainer/README.md` — tool table updated
- `docs/TEST_YOURSELF.md` — hermetic session setup uses `uv run`
- `.github/workflows/compat-headless-claude.yml` — CI also switched to `uv run`

PR #10: https://github.com/DgxSparkLabs/marketplace/pull/10 — now 7-commit bundle. Tests passing locally: 78 marketplace + 21 schema-fitness = 99 green. Drift clean.

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
