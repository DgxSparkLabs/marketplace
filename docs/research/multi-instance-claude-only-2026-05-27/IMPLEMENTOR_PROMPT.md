# Implementor brief — multi-instance-capable plugins (Claude-only)

You are picking up a session. The prior session produced a complete execution plan; your job is to execute it. This brief gives you all the context you need cold — you don't have to read the prior conversation.

## What this project is (1-minute orientation)

The **DgxSparkLabs marketplace** is a cross-platform AI agent plugin marketplace. It ships skills, rules, agents, commands, hooks, MCP servers, LSP servers, monitors, output styles, and themes (10 construct types) for six AI coding platforms (Claude Code, Codex, Gemini, Cursor IDE + CLI, Windsurf, Devin) plus a unified `.agents/` mirror convention. A Python generator (`scripts/generate_manifest.py`) reads source content from per-construct directories and emits per-platform native manifests + a top-level `.claude-plugin/marketplace.json`.

Read these files in this order if you need deeper context:

1. `HANDOFF.md` — project state tracker
2. `docs/RESUME_HERE.md` — 90-second orientation
3. `docs/ARCHITECTURE.md` — generator architecture, the 7 Platform classes and 10 Construct classes
4. `docs/PLATFORMS.md` — per-platform install reference
5. `docs/research/multi-instance-claude-only-2026-05-27/PLAN.md` — the plan you're executing
6. `docs/research/multi-instance-claude-only-2026-05-27/OBJECTIVE_CHECKLIST.md` — the verifiable checklist

## What you're implementing

The plan at `docs/research/multi-instance-claude-only-2026-05-27/PLAN.md` is comprehensive and implementation-ready. Read it once end-to-end before starting. The TL;DR:

- **Revert Path A**: change one f-string in `scripts/constructs.py` `_base_plugin_shape` so `plugin.json` `name` becomes `f"{brand}-{construct.prefix}-{name}"` (unique per plugin) instead of the shared `f"{brand}-{construct.category}"` (Path A).
- **Add multi-skill layout support**: `SkillConstruct.build_plugin_json` gains a layout-detection branch — single skill at plugin root OR multiple skills in a `skills/<skill>/` subdir. Both-layouts-present raises ValueError; neither raises ValueError.
- **Add a helper**: `_read_source_plugin_description` in `scripts/utils.py` reads the operator-authored plugin-level `description` from `<plugin>/.claude-plugin/plugin.json` (separate from per-component SKILL.md frontmatter).
- **Reorganize the example set**: `skills/example/` becomes a two-skill multi-instance plugin (`notebook` + `status`); a NEW `skills/example-single/` is a one-skill plugin (`hello`). The current single-skill `skills/example/SKILL.md` (with `name: lab-notebook`) is deleted; its content is split into the two new skills.
- **Add three tests**: rename + update `test_individual_plugin_name_is_unique_brand_namespace`; new `test_skill_plugin_layouts`; new `test_mcp_server_keys_unique_across_plugins`. Update the marketplace-count formula test.
- **PAUSE cross-platform**: the non-Claude platforms (Cursor, Codex, Gemini, Windsurf, Devin, `.agents/` shim) are explicitly NOT verified under multi-skill layouts. Their `emit()` and `build_plugin_json()` methods get NOTE comments tagging the unverified status; otherwise unchanged.
- **Cascade docs**: 10 files (README, ADDING_A_CONSTRUCT, TEST_YOURSELF, USER_GUIDE, PLATFORMS, CONSTRUCT_TYPES, RESUME_HERE, CHANGELOG, the two skill READMEs).
- **Update ROADMAP**: add follow-up tasks #37-#42 for per-platform multi-instance verification (one per non-Claude platform).
- **One commit on PR #10**: titled `refactor(skills): multi-instance-capable layout (Claude-only); revert Path A; pause non-Claude verification`.

## Starting state

- **Branch**: `chore/housekeeping-and-roadmap` — PR #10 open against `main`.
- **Last commit**: `3275049 feat(stub): standalone Dockerized hermetic stub + host bind-mounted logs`.
- **Path A is currently landed** at commit `d641f92` — your work reverts that aspect.
- **PR #10 commits so far**: 12. Your work is commit #13.

## How to execute

### Step 1 — read the plan

Read `docs/research/multi-instance-claude-only-2026-05-27/PLAN.md` end-to-end (~440 lines, ~10 min). Notice:

- The "Code changes" section has exact pseudo-code for each function.
- The "Test changes" section has exact pytest assertions.
- The "Source content changes" section enumerates every new and deleted file.
- The "What's deferred" section is the hard boundary — do NOT touch those items.

### Step 2 — execute in this order

1. **Source code changes** (`scripts/constructs.py`, `scripts/utils.py`, `scripts/platforms.py` NOTE comments only). Get the generator to emit correctly. Run `uv run scripts/generate_manifest.py` once to confirm it still works (output should still produce 10 plugin entries pre-source-content-change).
2. **Source content changes** — delete `skills/example/SKILL.md`, create the new `skills/example/skills/{notebook,status}/SKILL.md` files plus `skills/example/.claude-plugin/plugin.json` and update its `README.md`. Create the entire `skills/example-single/` directory with its three files (plugin.json, SKILL.md, README.md).
3. **Catalog update** — add `"skill:example-single"` to `bundle.examples` in `catalog.toml`.
4. **Regenerate** — `uv run scripts/generate_manifest.py`. Output should show 11 plugin entries (was 10). Inspect `_generated/skill-example/.claude-plugin/plugin.json` — `name` field should be `dgxsparklabs-skill-example`, `skills` field should be `["./skills/"]`. Inspect `_generated/skill-example-single/.claude-plugin/plugin.json` — `name` should be `dgxsparklabs-skill-example-single`, `skills` should be `["./"]`.
5. **Test updates** — modify `tests/test_marketplace.py` per the plan's test specs. Run `uv run tests/test_marketplace.py` and `uv run tests/test_schema_fitness.py`. Both must be green.
6. **ROADMAP update** — add items #37-#42 per the plan's ROADMAP section.
7. **Doc cascade** — update the 10 doc files per the plan's "Doc changes" table. Use the README and CONTRIBUTING quick-start drafts from the plan VERBATIM as the basis; adapt them to fit each file's existing structure.
8. **CHANGELOG entry** — add the entry per the plan's rollout section. Explicitly state what's verified (Claude) vs paused (non-Claude); cite the follow-up roadmap items.
9. **STATE.md update** — reflect end-of-implementation state.
10. **Commit** — single commit with the message from the plan's rollout section.
11. **Push** — `git push` to the existing `chore/housekeeping-and-roadmap` branch (PR #10 picks it up).

### Step 3 — verification

Run the verification recipe from the plan's "Verification recipe" section:

1. `uv run scripts/generate_manifest.py` (drift-clean)
2. `uv run tests/test_marketplace.py` + `uv run tests/test_schema_fitness.py` (both green)
3. (Optional but recommended) Empirical Docker test — install both example plugins into a hermetic Claude session, confirm `/dgxsparklabs-skill-example:notebook`, `/dgxsparklabs-skill-example:status`, `/dgxsparklabs-skill-example-single:hello` all resolve via the body-dumper stub. The `tests/fixtures/claude-stub/Dockerfile` exists (built in PR #10 commit `3275049`).
4. `claude plugin details dgxsparklabs-skill-example` must list BOTH `notebook` AND `status` as components (Path A's "first-installed-wins" collapse must be gone).

### Step 4 — when done

Run through `docs/research/multi-instance-claude-only-2026-05-27/OBJECTIVE_CHECKLIST.md` and mark each item complete. Every item must be verifiable — don't tick anything you can't show evidence for.

## Critical rules

- **NEVER include AI co-author attribution in commits** — per `rules/no-ai-credit/` and `AGENTS.md`. No `Co-Authored-By: Claude`, no "Generated with...", no AI tool names in commit messages or file headers.
- **Never push directly to main** — always go through PR #10.
- **No backwards-compatibility shims** for the Path A → Path D revert. Just change the f-string. Path A's shared-namespace pattern was unfortunate but short-lived; no need to support it.
- **Stay within Claude-only scope** — do NOT implement per-skill mirror flattening in `AgentsPlatform.emit` or `GeminiPlatform.emit`. Do NOT change `CursorPlatform.build_plugin_json` to read source plugin.json. These are deferred per the plan's "What's deferred" section. NOTE comments only.
- **Don't redesign anything** — the plan is the spec. Edge cases not covered by the plan should be flagged in chat, not silently designed around. If you find something genuinely ambiguous, ask the operator before guessing.

## What success looks like

The objective checklist file has all items checked. PR #10 has 13 commits, the last one being this implementation. CI is green (or at least no worse than before this commit). The implementor's commit message clearly states what was done + what was paused.

## What if something goes wrong

- If a test fails in a way the plan didn't anticipate, FIRST check the plan's "What's deferred" section to confirm you're not crossing the Claude-only scope boundary.
- If a test fails because a previous expectation no longer holds (e.g., the marketplace-count test), update the assertion to match the new reality per the plan's "Update marketplace-count test" section.
- If you find a contradiction in the plan, the IMPLEMENTOR_PROMPT and OBJECTIVE_CHECKLIST are the source of truth; the PLAN is the elaboration. If those three documents disagree, surface it to the operator before guessing.

## Time budget

The plan was designed for ~2 hours of focused implementation. If you're at 3 hours and not done, stop and surface what's blocking.
