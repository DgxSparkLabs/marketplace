# STATE

> Live within-session truth. Pair with `HANDOFF.md` (between-sessions) and `PITFALLS.md` (cross-session lessons).

## Session end — 2026-05-27

**Branch:** `chore/housekeeping-and-roadmap` (PR #10 open, 12 commits)
**Main tip:** `4b00faa` — PR #9 squash-merged
**Last commit on PR #10:** `3275049` — feat(stub): standalone Dockerized hermetic stub + host bind-mounted logs
**Working tree:** clean except `.claude/` untracked (operator's local Claude config); new research artifacts staged for commit (see below)

## What this session produced

Three artifacts in `docs/research/multi-instance-claude-only-2026-05-27/`:

1. **PLAN.md** — complete execution plan for the multi-instance-capable plugins refactor (Claude-only scope, ~440 lines)
2. **IMPLEMENTOR_PROMPT.md** — self-contained brief for the next session's implementor agent
3. **OBJECTIVE_CHECKLIST.md** — boolean verification checklist (~40 items, each independently testable)

Plus updates to `HANDOFF.md` (top-of-file banner pointing to the research artifacts).

## What the next session is set up to do

Execute the plan. Specifically: revert Path A (the shared-namespace pattern landed at commit `d641f92`), adopt multi-instance-capable plugins for Claude only, reorganize the example set to two plugins (`skill-example` with 2 skills, `skill-example-single` with 1 skill), add 3 tests, cascade docs across 10 files, add ROADMAP follow-ups #37-#42 for per-platform multi-instance verification. One commit on PR #10.

## Why this work didn't happen in THIS session

The user explicitly chose to end the session after the planning + review phase. Three rounds of subagent review caught real issues (cross-platform mirror discovery depth, MCP server-key cross-plugin collision, plan contradictions); the plan was rewritten to be implementation-ready. The user's instruction was to prepare everything for the next session and then end this one. Implementation happens fresh tomorrow.

## Outside the multi-instance refactor

PR #10 already contains 12 commits of substantial work: housekeeping + roadmap creation, mcp-example name alignment, Claude reference card, Scheme B+ naming, dev container, PEP 723 stubs + volume chown, bind-mount Docker setup, fenced code blocks for typed commands, catch-all bundle retirement, naming trace + code crosslinks, brand-namespace Path A (to be reverted next session), Dockerized hermetic stub. All of those stay regardless of the multi-instance refactor.

## Tests state

Last known green locally: 77 marketplace + 21 schema-fitness = 98 tests passing on commit `3275049`. The next session's implementation must maintain that.

## What's deferred (still on the roadmap, not blocking PR #10 merge)

- 6 platform QA cycles (Cursor IDE, Cursor CLI, Gemini, Windsurf, Devin, agents CLI shim) — roadmap items #9-#14
- 6 multi-instance verification follow-ups (one per non-Claude platform) — roadmap items #37-#42 (added by the next session per the plan)
- F4 visual theme — interactive verification, operator-only

## What the next session should NOT do

- Touch the non-Claude per-platform paths in `scripts/platforms.py` beyond adding NOTE comments
- Per-skill mirror flattening in `AgentsPlatform.emit` or `GeminiPlatform.emit`
- Reading source plugin.json in `CursorPlatform.build_plugin_json`
- Cross-platform empirical Docker verification (deferred to each platform's own QA cycle)

All four are explicitly out of scope per the PLAN.md "What's deferred" section.
