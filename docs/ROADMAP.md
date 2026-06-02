---
title: Roadmap
last-updated: 2026-05-26
purpose: operator-syncable task list for sequenced platform QA + post-stable real-content re-add
status: live
---

# Roadmap

> The sequenced task list an operator can sync against. **Live document** — update as arcs land, decisions are made, or new tasks surface.

## TL;DR — where we are

- **Done:** PRs #3–#9 landed. Marketplace reduced to 10 example plugins (19 entries). Claude verified clean (9/9 hermetic findings PASS, F4 deferred). Hermetic Claude CI runs on every PR.
- **Now:** Next platform's QA cycle. Recommended start: **Cursor IDE** (biggest emission surface delta).
- **Sequencing constraint:** all 6 platforms must verify clean on the minimal example set before any real skill or rule returns from `docs/archive/`.
- **What the constraint gates:** this 6-platform-parity sequencing gates RE-ADDING the archived real skills/rules (#16–#18) — it does **not** gate accepting *new* construct PRs. New constructs are accepted now and validated Claude-first; the other 5 platforms still emit and their parity is tracked here.

## Status legend

- `[DONE]` — landed; artifact verifiable in git
- `[NEXT]` — ready to start; no upstream blocker
- `[BLOCKED]` — upstream task must complete first
- `[DECIDE]` — needs operator decision before work begins
- `[BACKLOG]` — known work, not yet sequenced
- `[ONGOING]` — durable maintenance thread

---

## Recently completed

| # | Task | Artifact |
|---|---|---|
| 1 | `[DONE]` Doc consolidation: 45 docs → hub-and-spoke masters | PR #3 |
| 2 | `[DONE]` Platform-feature-routing refactor + `agents` CLI shim | PR #4 |
| 3 | `[DONE]` Cross-platform emission bug fixes (6 example plugins) | PR #5 |
| 4 | `[DONE]` Claude QA + `docs/USER_GUIDE.md` | PR #6 |
| 5 | `[DONE]` `TEST_YOURSELF.md` branch-staleness fix | PR #7 |
| 6 | `[DONE]` Hermetic Claude stub + CI workflow (F5/F7/F9 auto-verify) | PR #8 |
| 7 | `[DONE]` Minimal-stable transition: archive 26 skills + 21 rules; entries 81 → 19 | PR #9 @ `1237ec4` |

## Active arc — per-platform QA cycles on minimal-stable set

Each platform must pass its `docs/TEST_YOURSELF.md` cells on the 10 example plugins. Same depth as the Claude QA arc: find bugs, fix via PR, document Known Issues, defer interactive-only cells.

| # | Task | Status | Blocker | Done when |
|---|---|---|---|---|
| 8 | Claude Code QA cycle | `[DONE]` | — | 9/9 hermetic PASS, F4 deferred |
| 9 | **Cursor IDE QA cycle** | `[NEXT]` | — | `compat-cursor-ide` cells pass; bugs landed |
| 10 | Cursor CLI QA cycle | `[BLOCKED]` | #9 | `.agents/` + cursor-agent skills work |
| 11 | Gemini CLI QA cycle | `[BLOCKED]` | #10 | Extensions install + hook conversion verified |
| 12 | Windsurf IDE QA cycle | `[BLOCKED]` | #11 | Cascade discovers `.windsurf/rules/` + `.agents/skills/` |
| 13 | Devin QA cycle | `[BLOCKED]` | #12 | `.devin/skills/` + `.agents/skills/` discovery |
| 14 | `agents` CLI shim QA cycle | `[BLOCKED]` | #13 | Install / uninstall / list / info / scope flags |

## Deferred Claude QA item

| # | Task | Status | Done when |
|---|---|---|---|
| 15 | F4 visual theme — interactive verification | `[DECIDE]` | Manual screenshot + Known Issues update |

## Post-platform-cycle — re-add real content one-by-one

| # | Task | Status | Blocker | Done when |
|---|---|---|---|---|
| 16 | Pick first real skill from `docs/archive/skills-pre-stable-*/`; re-add + cross-platform verify | `[BLOCKED]` | #9–14 green | Works on all 6 platforms, no regressions |
| 17 | Continue re-adding real skills | `[BLOCKED]` | #16 | All 26 either restored or explicitly retired |
| 18 | Re-add real rules (Claude-deprecated; verify on Cursor/Codex/Gemini/Windsurf/Devin) | `[BLOCKED]` | #17 (or parallel) | All 21 either restored or explicitly retired |

## Infrastructure follow-ups

| # | Task | Status | Done when |
|---|---|---|---|
| 19 | Promote `compat-headless-claude` from advisory → required CI gate | `[NEXT]` | `continue-on-error: false` in workflow file |
| 20 | Schema-fitness coverage for newly-emitted construct types | `[BACKLOG]` | Hooks/MCP/sub-agents covered on emitting platforms |
| 21 | Extend hermetic stub to Codex/Gemini/Cursor (if feasible) | `[BACKLOG]` | Each platform has unauth CI verification path |
| 35 | Dev container for operator QA + marketplace dev | `[DONE]` | `.devcontainer/` configured with Claude CLI, Node 20, uv, Python+Flask, gh; ports 8088/8089 forwarded; Claude config persisted via named volume |
| 36 | Sibling dev containers for Codex/Gemini/Cursor (as their QA arcs land) | `[BACKLOG]` | Each platform CLI in a feature-flagged or sibling `.devcontainer/<platform>/` config |
| 37 | **Cursor IDE — verify multi-instance source layouts** + fix `CursorPlatform.build_plugin_json` to read source `plugin.json` `skills` field instead of hardcoding `"./"` | `[BLOCKED]` | Blocker: #9 Cursor IDE QA cycle. See `docs/research/multi-instance-claude-only-2026-05-27/PLAN.md` |
| 38 | **Codex — verify multi-instance source layouts** | `[BLOCKED]` | Blocker: #10 Cursor CLI / Codex QA. May need no code change (manifest hardcodes `"./skills/"` already) but needs empirical verification |
| 39 | **Gemini — per-skill mirror flattening** in `GeminiPlatform.emit` for multi-instance skill plugins | `[BLOCKED]` | Blocker: #11 Gemini QA. The current `shutil.copytree` produces nested mirrors that Gemini discovery doesn't recurse into |
| 40 | **Windsurf — per-skill mirror flattening** (via the `.windsurf/skills/` mirror) | `[BLOCKED]` | Blocker: #12 Windsurf QA |
| 41 | **Devin — per-skill mirror flattening** (via the `.devin/skills/` mirror) | `[BLOCKED]` | Blocker: #13 Devin QA |
| 42 | **`.agents/` shim — per-skill mirror flattening** in `AgentsPlatform.emit` (consumed by Cursor CLI + Windsurf + Devin via convergence path) | `[BLOCKED]` | Blocker: any of #10/#12/#13/#14. Highest leverage fix because 3 platforms read from `.agents/`. |

## Housekeeping — pre-existing untracked state

| # | Task | Status | Disposition |
|---|---|---|---|
| 22 | `Untitled.md` at repo root | `[DONE]` | Resolved — file no longer on disk |
| 23 | `docs/PLAN_DI_REFACTOR.md` (empty stub) | `[DONE]` | Deleted 2026-05-26 — canonical at `docs/archive/di-refactor/` |
| 24 | `docs/research/claude-headless-qa/` | `[DONE]` | Moved to `docs/archive/claude-headless-qa-2026-05-26/` |
| 25 | `docs/research/claude-qa-2026-05-26/` | `[DONE]` | Moved to `docs/archive/claude-qa-2026-05-26/` |
| 26 | `docs/research/research/` (107 files, 2 MB canonical research stash) | `[DONE]` | Added to `.gitignore` — preserved on disk, not version-controlled |
| 27 | Create `STATE.md` | `[DONE]` | Created 2026-05-26 per CLAUDE.md bootstrap trigger |

## Naming / cosmetic decisions

| # | Task | Status | Notes |
|---|---|---|---|
| 28 | `mcp-example` plugin alignment (three-name mismatch) | `[DONE]` | PR #10 — marketplace + plugin.json + server key all align as `mcp-example`/`example` family |
| 29 | `skill-example` `name:` field — keep `/example-skill` or shorten to `/example`? | `[DONE]` | PR #10 — SKILL.md `name:` is now `lab-notebook`. Slash form `/skill-example:lab-notebook` (proven via Docker research). |
| 33 | **Systemic name-chain mismatch across 9 example plugins** (Scheme B+) | `[DONE]` | PR #10 — empirical Docker research (`docs/research/naming-conventions-2026-05-26/`) revealed the visible mismatch was narrower than feared (source-vs-marketplace; never reaches `/plugins`), and the real awkward slash form was just `/skill-example:example-skill` doubled. Applied Scheme B+: align 9 `plugin.json` names + rename SKILL.md `name:` to `lab-notebook` + rename monitor `example-disk` to `disk-usage`. |
| 34 | Extend per-construct reference cards to remaining 5 platforms in `docs/TEST_YOURSELF.md` | `[BACKLOG]` | Claude section now has exact-strings-to-type + expected-output card (PR #10). Cursor IDE / Cursor CLI / Gemini / Windsurf / Devin / agents CLI sections still terse — apply same depth as part of each platform's QA cycle (#9–#14). |

## Durable methodology threads

| # | Task | Status | Notes |
|---|---|---|---|
| 30 | Update compaction prompt to reflect PR #9 minimal-stable | `[BACKLOG]` | 2-line edit if saving the prompt durably |
| 31 | Obsidian vault conventions on new docs (wiki-links, frontmatter, kebab-case) | `[ONGOING]` | Per-doc when authored |
| 32 | Maintain `PITFALLS.md` on bug-fix arcs | `[ONGOING]` | Add entry after each non-obvious bug fix |

---

## Recommended next concrete action

After the housekeeping decisions in #24–#26 land, start **#9 — Cursor IDE QA cycle**. It has the biggest newly-emitted construct surface (sub-agents, commands, hooks, MCP) and is most likely to surface real bugs in the minimal example set.

If the operator wants the smallest possible next step instead: **#19 — promote hermetic-claude CI** (single line, single PR, locks in the safety net we now have).
