---
date: 2026-05-24
scope: project-level-docs-only
purpose: inventory-for-consolidation
---

# Documentation Inventory — DgxSparkLabs/marketplace

> Built by a subagent on 2026-05-24 as input to the next consolidation pass. The deliverable is the table below. Decisions about archive/delete/merge/keep should be made from this file alone — no need to re-open the source files.

## Summary

- **Total files inventoried**: 45
- **Total bytes**: 634,536 (~620 KB)
- **Scope**: `*.md` files under `docs/**`, repo root, and `.github/**` (none exist in `.github/`). Per-skill/per-plugin/per-rule README and SKILL.md files are out of scope; `research/`, `skill-templates/`, examples-folder READMEs all out of scope.
- **Snapshot**: main at `92d1aa7` (PR #1 + PR #2 both merged). Phase 5 (cross-platform install fix) and post-merge cleanup are complete. Next planned arc: adjust support for Cursor/Windsurf/Devin (the three platforms without native CLI plugin install).

### Breakdown by `status` value

| Status | Count |
|---|---|
| `live-accurate` | 11 |
| `live-stale` | 3 |
| `partially-stale` | 7 |
| `pure-history` | 24 |
| `orphaned` | 0 |
| `redundant-with-...` | 0 |
| `unclear` | 0 |

### Breakdown by `proposed_action` value

| Proposed action | Count |
|---|---|
| `stays-at-top-level` | 11 |
| `archive-to-docs/archive/<bucket>` (di-refactor=4, phase-1-compliance=3, phase-2-validation=6, phase-5-cross-platform-install=6, restructure=1) | 20 |
| `merge-into-master-doc` | 11 |
| `delete-as-redundant` | 3 |
| `delete-as-empty` | 0 |
| `decide-with-user` | 0 |

### Major duplication clusters (call these out to the consolidator)

1. **Plan dossier x3 for the SAME DI refactor**: `docs/PLAN_DI_REFACTOR.md` (v3, 90 KB), `docs/PLAN_DI_REFACTOR_CRITIQUE.md` (v1 critique, 38 KB), `docs/PLAN_DI_REFACTOR_CRITIQUE_V2.md` (v2 critique, 23 KB), plus `docs/DI_REFACTOR_REPORT.md` (implementation report) and `docs/DI_REFACTOR_VALIDATION_REPORT.md` (validation). 5 files, ~178 KB total, covering one feature arc that's been DONE since 79caefb. All 25 locked decisions from the plan are also restated in `HANDOFF.md` and `docs/RESUME_HERE.md`. Heavy archive candidate.

2. **Phase 5 cross-platform install fix arc**: `docs/PLAN_CROSS_PLATFORM_INSTALL_FIX.md` + the entire `docs/VERIFICATION_2026-05/` directory (7 .md files: SUMMARY, empirical_act_verification, cursor, IMPLEMENTATION_REPORT, IMPLEMENTATION_VALIDATION, README_REWRITE_PREVIEW, README_REWRITE_REPORT) — 8 files, ~125 KB. All represent one completed arc with VERIFICATION_2026-05/SUMMARY.md as the synthesis and the other six as audit trail.

3. **Multi-platform CI/CD design + reports**: `docs/PLATFORM_VALIDATION_CICD_PLAN.md` (design, 25 KB), `docs/VALIDATION_IMPLEMENTATION_BRIEF.md` (implementer prompt, 10 KB), `docs/VERIFICATION_REPORT.md` (first CI cycle), `docs/FIX_REPORT.md` (second), `docs/FINALIZATION_REPORT.md` (Wave 4) — 5 files, ~73 KB. Same Phase 2 arc; the three -REPORTs are sequential audit trail of a feature now fully landed and superseded by Phase 5 work.

4. **Empirical CLI exploration: old vs new**: `docs/EMPIRICAL_CLI_FINDINGS/` (6 files, 26 KB, dated 2026-05-22) vs `docs/VERIFICATION_2026-05/cursor.md` (which explicitly *overturns* the older `docs/EMPIRICAL_CLI_FINDINGS/cursor.md`). The newer set is partially superseding the older but doesn't replace it (different platforms, different scope). May need merging into one canonical "what each platform's CLI does" reference.

5. **Plugin compliance migration dossier**: `docs/GOAL_PLUGIN_COMPLIANCE.md`, `docs/PLAN_PLUGIN_COMPLIANCE.md`, `docs/IMPLEMENTING_AGENT_PROMPT.md`, `docs/INVESTIGATION_PLUGIN_DEPENDENCIES.md`, `docs/RESTRUCTURE_REPORT.md`, `docs/pr1-body.md`, `docs/ORG_POLICY_INVESTIGATION.md`, `CHANGELOG.md` entry for v1.0.0. The whole "Phase 1: migrate from TUI installer to native /plugin marketplace add" arc, fully landed.

6. **Orientation files with overlap**: `HANDOFF.md` + `docs/RESUME_HERE.md` + `docs/ONBOARDING.md` + `AGENTS.md`. Four onboarding/handoff docs with different intended audiences but overlapping content. AGENTS.md and ONBOARDING.md both pre-date the DI refactor and contain stale claims.

## File-by-file inventory

| path | bytes | purpose | audience | status | topics | keep_for_master_doc | proposed_action | notes |
|---|---|---|---|---|---|---|---|---|
| `README.md` | 19,430 | User-facing installation and overview document covering per-platform install + GitHub-direct-install support matrix + repo structure. | end-user | live-accurate | platforms, cross-platform-install, contributing | yes | stays-at-top-level | Recently rewritten via `docs/VERIFICATION_2026-05/README_REWRITE_REPORT.md`. Every command appears as VERIFIED-PASS in `docs/VERIFICATION_2026-05/empirical_act_verification.md`. Drift assessment in its own section below. |
| `HANDOFF.md` | 16,586 | Long-form project state tracker — current branch, 5 completed phases, what's next, project layout, architecture summary, known limitations. | future-claude | live-accurate | handoff, architecture, di-refactor, cross-platform-install | yes | stays-at-top-level | Says "Last updated: 2026-05-24, after PR #1 merged" — accurate. Cross-references `docs/RESUME_HERE.md` as the short companion. Some overlap with RESUME_HERE.md (architecture, glossary) and with `AGENTS.md` (conventions). |
| `AGENTS.md` | 25,031 | Per-project AI agent instructions: conventions, no-AI-credit, testing, Python uv discipline, plus ~10 KB of generic project-discipline rules (verify-your-work, blast-radius, document-lifecycle, autonomous-persistence, revert-on-failure, output-discipline, etc.). | future-claude | live-stale | contributing, handoff | partial | stays-at-top-level | "Layout" section says `examples/` exists and references `_template/` and per-construct ADDING_* docs — all wrong post-DI-refactor. "Testing" section references `tests/run-ci-local.sh` which may not exist. The generic discipline-rule sections (~200 lines from "Document Lifecycle" through "Output Discipline") are user-global content imported here; not project-specific. Recommend trimming the stale layout section, keeping the discipline content. |
| `CHANGELOG.md` | 5,453 | Append-only history of behavior-changing milestones. Most recent entry: 2026-05-22 v1.0.0 plugin compliance migration. | end-user | partially-stale | pr-history, contributing | yes | stays-at-top-level | Missing entries for the DI refactor (Phase 4) and Phase 5 cross-platform install fix; both are documented elsewhere but not in CHANGELOG. Earlier entries describe the deleted Textual TUI installer in past tense — those are correct. |
| `CONTRIBUTING.md` | 4,436 | Contributor workflow: how to add a plugin, what conventions to follow, where to find tutorials. | contributor | partially-stale | contributing | partial | stays-at-top-level | References 12 separate `docs/ADDING_*.md` tutorials in the contributor table — all 11 of those were deleted and merged into `docs/ADDING_A_CONSTRUCT.md` per DI refactor decision #10. Also says "edit `examples/`" which is the old layout. Needs a rewrite to point at `docs/ADDING_A_CONSTRUCT.md` and at the post-restructure `<construct>/example/` paths. |
| `PITFALLS.md` | 3,495 | Knowledge base of bugs that occurred and how they were fixed, scoped to "things that went wrong." | future-claude | pure-history | pr-history | partial | stays-at-top-level | Every entry references commits from the pre-DI-refactor era (installer.py-era bugs like Banner K glyph, install_rule exists check, telegram-notify secret leak). All commits referenced are obsolete since `install.py` was deleted. Content has historical value but the issues themselves are no longer reachable. Could be archived but `AGENTS.md` mandates a top-level PITFALLS.md — keep at top level even if all current entries become historical. |
| `docs/ADDING_A_CONSTRUCT.md` | 4,780 | Single-source contributor walkthrough for adding any of 10 construct types, replacing the 11 old per-construct ADDING_* docs (DI refactor decision #10). | contributor | live-accurate | contributing | yes | stays-at-top-level | Accurate; references the post-DI-refactor architecture (constructs.py, platforms.py, etc.). Could move under a future `docs/reference/` if structure is reorganized. |
| `docs/CONSTRUCT_TYPES.md` | 4,387 | Reference table of the 10 construct types with prefixes, source dirs, install command examples; cross-references `ADDING_A_CONSTRUCT.md`. | contributor | live-accurate | contributing, architecture | yes | stays-at-top-level | Bidirectional cross-reference with `docs/ADDING_A_CONSTRUCT.md`. Architecture section mentions "6 Platform classes" but post-Phase 5 there are 7 — minor staleness, easy fix. |
| `docs/DI_REFACTOR_REPORT.md` | 9,113 | Implementation report for the DI refactor (Phase 4): commit list, what changed, plugin name snapshot diff, test results. | audit-trail | pure-history | di-refactor, architecture | partial | archive-to-docs/archive/di-refactor | Tightly coupled to `docs/PLAN_DI_REFACTOR.md` (the plan) and `docs/DI_REFACTOR_VALIDATION_REPORT.md` (the validation). The "Asymmetries Dissolved" and "Surprises / Notes" sections have permanent reference value worth merging into a master architecture doc. |
| `docs/DI_REFACTOR_VALIDATION_REPORT.md` | 17,071 | Post-implementation validator's report confirming all 25 locked decisions were honored, with per-row evidence. | audit-trail | pure-history | di-refactor | no | archive-to-docs/archive/di-refactor | Audit-trail proof that Phase 4 was implemented correctly; no ongoing reference value beyond audit. Bidirectional cross-references with `docs/PLAN_DI_REFACTOR.md` and `docs/DI_REFACTOR_REPORT.md`. |
| `docs/FINALIZATION_REPORT.md` | 10,493 | Final report on the Phase 2 multi-platform validation CI work: Wave 4 promotion (codex/gemini from advisory to required), generator extension to emit gemini-extension.json, all 11 workflows green. Dated 2026-05-22. | audit-trail | pure-history | verification, pr-history, platforms | no | archive-to-docs/archive/phase-2-validation | Sequential audit trail with `docs/VERIFICATION_REPORT.md` (cycle 1) and `docs/FIX_REPORT.md` (cycle 2). Superseded by Phase 5 work that extended these same workflows. Contains GHA run URLs that document the exact commits and timing — useful only for audit. |
| `docs/FIX_REPORT.md` | 10,692 | Fix-cycle report for Phase 2 CI work: 3 fixes (compat-mcp grep target, gemini mcp list stderr, removal of gemini hooks migrate job). Dated 2026-05-22. | audit-trail | pure-history | verification, pr-history, platforms | no | archive-to-docs/archive/phase-2-validation | Cross-references `docs/VERIFICATION_REPORT.md` (its predecessor) and `docs/FINALIZATION_REPORT.md` (its successor). The empirical CLI findings (gemini mcp list writes to stderr, hooks migrate has no --dry-run) were promoted into `docs/PLATFORM_INSPECTION_CATALOG.md` already. |
| `docs/GOAL_PLUGIN_COMPLIANCE.md` | 3,491 | The 12 binary success criteria for the Phase 1 migration from the Textual TUI installer to native /plugin marketplace add. | audit-trail | pure-history | planning, di-refactor | no | archive-to-docs/archive/phase-1-compliance | Status line says "Planning complete. Execution not yet started." but execution has been fully done for months. The 12 criteria are all met. Cross-referenced from `docs/IMPLEMENTING_AGENT_PROMPT.md` and `docs/PLAN_PLUGIN_COMPLIANCE.md`. |
| `docs/IMPLEMENTING_AGENT_PROMPT.md` | 6,424 | Prompt template for spawning a subagent to execute the Phase 1 plugin compliance migration. | audit-trail | pure-history | planning, handoff | no | archive-to-docs/archive/phase-1-compliance | One-shot artifact from Phase 1 spawn. References `docs/GOAL_PLUGIN_COMPLIANCE.md` and `docs/PLAN_PLUGIN_COMPLIANCE.md`. Cross-referenced from `docs/VALIDATION_IMPLEMENTATION_BRIEF.md` as a precedent template. |
| `docs/INVESTIGATION_PLUGIN_DEPENDENCIES.md` | 11,421 | Empirical investigation proving Claude Code plugin dependencies auto-install (resolved 2026-05-22 — Outcome A). Includes Option 1/2/3 fallback design preserved as reference. | audit-trail | pure-history | di-refactor, verification, cli-empirical | partial | merge-into-master-doc | The "Result" section + "Bonus findings" table is reusable architecture knowledge. The fallback design section (Option 2) is no longer relevant. Cited from `HANDOFF.md`, `docs/PLAN_PLUGIN_COMPLIANCE.md`, `CHANGELOG.md`, `CONTRIBUTING.md`. |
| `docs/ONBOARDING.md` | 6,815 | 3-minute orientation for new agents/contributors, dated pre-DI-refactor. | future-claude | live-stale | handoff, contributing | partial | delete-as-redundant | Layout section shows `examples/` directory (deleted), references 71-plugin count (now 81), references 11 separate ADDING_* docs (consolidated to one), says skill count is 26 (now 27), says PR has not yet merged. Largely superseded by `docs/RESUME_HERE.md` + `HANDOFF.md` + `CONTRIBUTING.md`. |
| `docs/ORG_POLICY_INVESTIGATION.md` | 16,662 | Forensic investigation into why GitHub Actions transiently blocked @openai/codex and @google/gemini-cli on 2026-05-22, with hypothesis that it was a content-scanner queue-level rejection rather than an org policy. | audit-trail | pure-history | verification, cli-empirical, platforms | partial | archive-to-docs/archive/phase-2-validation | One-off forensic artifact. Useful as a canary: if the same "0s workflow file issue" pattern recurs, this doc is the diagnostic baseline. Referenced from `docs/PLAN_DI_REFACTOR.md` background section. |
| `docs/PLAN_CROSS_PLATFORM_INSTALL_FIX.md` | 34,985 | The Phase 5 plan: 8 issues identified by verification, 4 locked decisions (A1/B2/C1/Q2), 3 phases. v2 status; fully implemented and merged. | audit-trail | pure-history | planning, cross-platform-install, platforms, architecture | partial | archive-to-docs/archive/phase-5-cross-platform-install | The "Architectural Decisions To Lock" section (A1/B2/C1) is reusable knowledge. Cross-references the entire `docs/VERIFICATION_2026-05/` directory. The Risk Register has reusable patterns for any future cross-platform extension. |
| `docs/PLAN_DI_REFACTOR.md` | 90,518 | The Phase 4 DI refactor plan (v3): 25 locked decisions, full code sketches, test redesign, migration path. The largest single doc in the inventory. | audit-trail | pure-history | planning, di-refactor, architecture | partial | merge-into-master-doc | Contains permanent architectural reference (Construct/Platform/Bundle protocol design, asymmetry table, generator phases). Bidirectional cross-references with `docs/PLAN_DI_REFACTOR_CRITIQUE.md` and `docs/PLAN_DI_REFACTOR_CRITIQUE_V2.md`. The "Asymmetries this refactor dissolves" table and "Locked Decisions" table are worth lifting verbatim into a master architecture doc; the rest (code sketches, migration steps) is one-shot. |
| `docs/PLAN_DI_REFACTOR_CRITIQUE.md` | 38,488 | v1 reviewer critique that fed the v3 plan: 3 BLOCKERs, 6 IMPORTANTs, 5 NICEs, section-by-section notes, empirical verifications. | audit-trail | pure-history | planning, di-refactor | no | archive-to-docs/archive/di-refactor | Pure design-process artifact. All findings were rolled into v3 of the plan and the v2 critique confirmed resolution. No ongoing reference value. |
| `docs/PLAN_DI_REFACTOR_CRITIQUE_V2.md` | 23,178 | v2 reviewer critique confirming v1 BLOCKERs resolved + finding 5 new IMPORTANTs + 3 NICEs + 5 coverage gaps. | audit-trail | pure-history | planning, di-refactor | no | archive-to-docs/archive/di-refactor | Same audit-trail bucket as the v1 critique. All findings rolled into the final implementation per `docs/DI_REFACTOR_VALIDATION_REPORT.md`. |
| `docs/PLAN_PLUGIN_COMPLIANCE.md` | 13,446 | The Phase 1 plan for migrating from Textual TUI installer to native /plugin marketplace add — architecture, naming convention, repository layout, task order. | audit-trail | pure-history | planning, di-refactor | partial | archive-to-docs/archive/phase-1-compliance | The "Plugin naming convention" table and "Repository Layout" section have lasting reference value but are duplicated in `HANDOFF.md` and `docs/RESUME_HERE.md`. References sibling docs `docs/GOAL_PLUGIN_COMPLIANCE.md` and `docs/INVESTIGATION_PLUGIN_DEPENDENCIES.md`. |
| `docs/PLATFORM_INSPECTION_CATALOG.md` | 28,126 | Executable spec for multi-platform CI: every auth-free CLI command per platform with expected exit codes, output formats, match modes. Verification date 2026-05-22. | future-claude | partially-stale | platforms, cli-empirical, verification | yes | merge-into-master-doc | Primary reference for "what does platform X's CLI do." Cited from `docs/PLATFORM_VALIDATION_CICD_PLAN.md`, `README.md` Deep Dives, `HANDOFF.md`. Partially superseded by `docs/VERIFICATION_2026-05/cursor.md` which overturns the "no Cursor CLI" claim. The Cursor and Windsurf sections need updates per the May 2026 verification round. |
| `docs/PLATFORM_VALIDATION_CICD_PLAN.md` | 25,171 | Phase 2 CI/CD design: 10 compat-*.yml workflows, 5 composite actions, 20 locked decisions, Wave 1-4 phasing (all DONE 2026-05-22). | audit-trail | pure-history | planning, verification, platforms | partial | archive-to-docs/archive/phase-2-validation | Lasting reference: the 20 locked decisions and the per-workflow spec table. Cross-references `docs/PLATFORM_INSPECTION_CATALOG.md` (its executable spec), `docs/VALIDATION_IMPLEMENTATION_BRIEF.md` (implementer prompt), and the three Phase 2 reports (VERIFICATION/FIX/FINALIZATION). |
| `docs/pr1-body.md` | 6,965 | The body of PR #1 (cross-platform install + validation). One-off artifact. | audit-trail | pure-history | pr-history | no | delete-as-redundant | PR #1 is already merged; the PR body is on GitHub. Local copy has no ongoing reference value. Mentions 81 plugin count, 55 tests (now 52 per current state) — already out of date. |
| `docs/REENTRY_TEST_PROTOCOL.md` | 16,340 | Reusable test protocol for stress-testing whether cold subagents can re-orient using the orientation kit (`docs/RESUME_HERE.md` + `HANDOFF.md` + planning dossier). Includes a 4-round prompt template + grading rubric. | future-claude | partially-stale | handoff, planning | partial | merge-into-master-doc | A meta-process artifact. Round 2 questions reference Phase 2/3 work that's now done; the protocol itself is reusable but the specific probe questions are stale. Could move to a `docs/processes/` subdirectory or be merged into a future "orientation maintenance" master doc. |
| `docs/RESTRUCTURE_REPORT.md` | 9,248 | Report on the "Option D" restructure: examples moved from `examples/example-<type>/` into `<construct>/example-<type>/`. Dated 2026-05-23, commit d7a046d. | audit-trail | pure-history | pr-history, architecture | no | archive-to-docs/archive/restructure | Pre-DI-refactor checkpoint. Subsequently superseded by DI refactor decision #18 which renamed `example-<type>` → `example`. Audit-trail only. Cross-referenced from `docs/PLAN_DI_REFACTOR.md` background. |
| `docs/RESUME_HERE.md` | 12,797 | The "first file to read on re-entry" — 30-second TLDR, you-are-here, architecture, dead-ends list. Last updated 2026-05-24 post-Phase-5. | future-claude | live-accurate | handoff, architecture, cross-platform-install | yes | stays-at-top-level | Highest-quality orientation doc in the repo. Cross-references `HANDOFF.md` and the entire `VERIFICATION_2026-05/` arc + both PLAN docs. Some overlap with `HANDOFF.md` (architecture table, glossary) — that's intentional per the doc's stated design (RESUME = 30s, HANDOFF = longer). |
| `docs/RULE_FORMAT.md` | 4,599 | Rule directory structure, frontmatter spec for Windsurf/Cursor formats, installation mechanism explanation. | contributor | live-accurate | architecture, contributing | yes | stays-at-top-level | Reference doc for the "rules ship as plugins + activate.sh" architecture. Stable. Cross-references `docs/ADDING_A_RULE.md` which no longer exists (consolidated into ADDING_A_CONSTRUCT.md) — small link rot. |
| `docs/SKILL_FORMAT.md` | 7,910 | Full SKILL.md format spec: frontmatter fields, prompt body substitutions ($1, $SKILL_DIR, @file, !command). | contributor | live-accurate | architecture, contributing | yes | stays-at-top-level | Reference doc; stable. Cross-references `docs/ADDING_A_SKILL.md` which no longer exists — small link rot. |
| `docs/VALIDATION_IMPLEMENTATION_BRIEF.md` | 9,624 | Prompt template for spawning the subagent that implemented Phase 2 multi-platform validation CI. | audit-trail | pure-history | planning, handoff, verification | no | archive-to-docs/archive/phase-2-validation | One-shot artifact. References `docs/PLATFORM_VALIDATION_CICD_PLAN.md` (its spec), `docs/PLATFORM_INSPECTION_CATALOG.md` (its catalog source), `docs/IMPLEMENTING_AGENT_PROMPT.md` (its template precedent). |
| `docs/VERIFICATION_REPORT.md` | 17,887 | First CI verification cycle for Phase 2 validation, dated 2026-05-22. 1 required failure (compat-mcp claude grep) + 3 advisory failures. | audit-trail | pure-history | verification, pr-history, platforms | no | archive-to-docs/archive/phase-2-validation | Cycle 1 of Phase 2; superseded by `docs/FIX_REPORT.md` (cycle 2) and `docs/FINALIZATION_REPORT.md` (cycle 3). All assertions catalogued in the catalog. Contains GHA run URLs and timestamps from May 22 — diagnostic only. |
| `docs/EMPIRICAL_CLI_FINDINGS/README.md` | 6,314 | Master index of the May 22 empirical CLI findings: methodology, master findings table, per-platform auth-free commands, surprises list. | future-claude | partially-stale | cli-empirical, platforms | partial | merge-into-master-doc | Several claims now wrong per Phase 5 verification: "Codex BLOCKED by GitHub" (block lifted), "Cursor: confirmed no CLI" (overturned by VERIFICATION_2026-05/cursor.md), "Devin install path includes .agents/skills" needs reconciling with current generator state. The factual content is partially correct and partially superseded. |
| `docs/EMPIRICAL_CLI_FINDINGS/codex.md` | 4,121 | Codex CLI findings: package metadata, known subcommands, config file locations, gotchas. Dated 2026-05-22. | future-claude | partially-stale | cli-empirical, platforms | partial | merge-into-master-doc | "GitHub CI Blocked" section is now historical (block lifted 2026-05-22 per `docs/ORG_POLICY_INVESTIGATION.md` and `docs/VERIFICATION_2026-05/empirical_act_verification.md`). The non-blocking content (package metadata, subcommand list) is still accurate but partially restated in `docs/PLATFORM_INSPECTION_CATALOG.md`. |
| `docs/EMPIRICAL_CLI_FINDINGS/cursor.md` | 2,791 | Cursor CLI findings: "no headless CLI exists." Dated 2026-05-22. | future-claude | live-stale | cli-empirical, platforms | no | delete-as-redundant | Wholly overturned by `docs/VERIFICATION_2026-05/cursor.md` which proves the `agent` CLI exists. The misdiagnosed binary name (`cursor` vs `agent`) is the bug; that's a useful note for the master doc but the file as a whole is superseded. |
| `docs/EMPIRICAL_CLI_FINDINGS/devin.md` | 7,022 | Devin CLI findings: install path, full subcommand tree, auth-free commands, file paths. Dated 2026-05-22. | future-claude | live-accurate | cli-empirical, platforms | yes | merge-into-master-doc | Most detailed Devin CLI doc in the repo. The `devin skills paths` output (`.devin/skills/`, `.agents/skills/`, etc.) is load-bearing evidence for the AgentsPlatform decision. Worth lifting verbatim into a master "Devin platform" reference. |
| `docs/EMPIRICAL_CLI_FINDINGS/gemini.md` | 3,655 | Gemini CLI findings: package metadata, known subcommands. Dated 2026-05-22. | future-claude | partially-stale | cli-empirical, platforms | partial | merge-into-master-doc | "GitHub CI Blocking" section is historical. The subcommand list and config locations are accurate but subsumed by `docs/PLATFORM_INSPECTION_CATALOG.md` Platform 3 section. |
| `docs/EMPIRICAL_CLI_FINDINGS/windsurf.md` | 2,072 | Windsurf CLI findings: "NO CLI EXISTS for headless/terminal use." Dated 2026-05-22. | future-claude | live-accurate | cli-empirical, platforms | yes | merge-into-master-doc | Short, accurate, still relevant. The `.windsurf/rules/` discovery + npm namespace-squatter note are reusable knowledge. Worth lifting into a master "Windsurf platform" reference. |
| `docs/VERIFICATION_2026-05/SUMMARY.md` | 10,495 | Ground-truth synthesis of the May 2026 verification round: per-platform install status, 5 cross-cutting findings, what changed vs prior research. | future-claude | live-accurate | verification, cross-platform-install, platforms, cli-empirical | yes | merge-into-master-doc | The most useful single document in this directory. Cross-references `docs/VERIFICATION_2026-05/empirical_act_verification.md`, `docs/VERIFICATION_2026-05/cursor.md`. Status table is current truth as of 2026-05-24. Several lessons (per-plugin manifest is what Codex needs, `.agents/` is content not marketplace) are reusable architecture knowledge. |
| `docs/VERIFICATION_2026-05/empirical_act_verification.md` | 18,176 | Per-claim verification table (18 claims: C1-C7 Codex, G1-G6 Gemini, CU1-CU3 Cursor, CL1-CL3 Claude) with status, log file, evidence, reproducible command. | audit-trail | pure-history | verification, cli-empirical, platforms, cross-platform-install | partial | archive-to-docs/archive/phase-5-cross-platform-install | Primary evidence base for Phase 5 decisions. The corrections-to-prior-research table is worth lifting into a "lessons learned" section. The detailed per-platform deep-dives are tightly coupled to specific commits and act runs from 2026-05-24. |
| `docs/VERIFICATION_2026-05/cursor.md` | 24,792 | Cursor (IDE + CLI) WebFetch research dated 2026-05-24: overturns prior "no CLI" finding, documents the plugin marketplace launch (2026-02-17), team marketplace (2026-03-03), `agent` binary subcommands, manifest schema. | future-claude | live-accurate | cli-empirical, platforms, cross-platform-install | yes | merge-into-master-doc | Most current Cursor reference in the repo. Bidirectional cross-reference with `docs/EMPIRICAL_CLI_FINDINGS/cursor.md` (which it supersedes). Every claim is WebFetch-cited with URL + fetch date. Worth promoting wholesale into a master "Cursor platform" reference. |
| `docs/VERIFICATION_2026-05/IMPLEMENTATION_REPORT.md` | 9,715 | Implementer's commit-by-commit report on Phase 5 cross-platform install fix: 12 steps, all DONE, test results 52 passing. | audit-trail | pure-history | verification, di-refactor, cross-platform-install, architecture | no | archive-to-docs/archive/phase-5-cross-platform-install | Audit trail. Cross-references `docs/PLAN_CROSS_PLATFORM_INSTALL_FIX.md` and `docs/VERIFICATION_2026-05/IMPLEMENTATION_VALIDATION.md`. |
| `docs/VERIFICATION_2026-05/IMPLEMENTATION_VALIDATION.md` | 13,717 | Validator's APPROVED verdict on Phase 5 implementation: per-step and per-decision verification, independent runs (pytest 52 passing, drift OK, act codex re-run). | audit-trail | pure-history | verification, di-refactor, cross-platform-install | no | archive-to-docs/archive/phase-5-cross-platform-install | Audit trail. Cross-references the implementation report and the plan. |
| `docs/VERIFICATION_2026-05/README_REWRITE_PREVIEW.md` | 10,861 | Spec/plan for the Phase 2 README rewrite: every existing install instruction mapped to its verified-working replacement. | audit-trail | pure-history | planning, cross-platform-install | no | archive-to-docs/archive/phase-5-cross-platform-install | One-shot artifact. Cross-references `docs/VERIFICATION_2026-05/empirical_act_verification.md` for citations. Now superseded by the actual README rewrite (committed as b38d82b) and its companion report. |
| `docs/VERIFICATION_2026-05/README_REWRITE_REPORT.md` | 5,743 | Phase 2 report confirming every section was rewritten per the preview spec, with sanity check results. | audit-trail | pure-history | pr-history, cross-platform-install | no | archive-to-docs/archive/phase-5-cross-platform-install | Audit trail. Implicit cross-reference to the preview spec and to the post-rewrite README. |

## Cluster map (visual)

Five natural clusters emerge:

```
CLUSTER 1: Plugin compliance migration (Phase 1, 2026-05 v1.0.0)
  docs/GOAL_PLUGIN_COMPLIANCE.md
  docs/PLAN_PLUGIN_COMPLIANCE.md
  docs/IMPLEMENTING_AGENT_PROMPT.md
  docs/INVESTIGATION_PLUGIN_DEPENDENCIES.md
  docs/RESTRUCTURE_REPORT.md
  docs/pr1-body.md
  docs/ONBOARDING.md (incidentally captured pre-refactor state)
  → Status: arc complete, all docs are audit-trail. Archive bucket: phase-1-compliance.

CLUSTER 2: Multi-platform validation CI (Phase 2, 2026-05-22)
  docs/PLATFORM_VALIDATION_CICD_PLAN.md
  docs/VALIDATION_IMPLEMENTATION_BRIEF.md
  docs/VERIFICATION_REPORT.md     (cycle 1)
  docs/FIX_REPORT.md              (cycle 2)
  docs/FINALIZATION_REPORT.md     (cycle 3)
  docs/ORG_POLICY_INVESTIGATION.md (forensic, transient block)
  → Status: arc complete. Catalog (PLATFORM_INSPECTION_CATALOG) is the only enduring artifact.

CLUSTER 3: DI refactor (Phase 4, 2026-05-24)
  docs/PLAN_DI_REFACTOR.md           (90 KB, v3 plan)
  docs/PLAN_DI_REFACTOR_CRITIQUE.md  (v1 critique)
  docs/PLAN_DI_REFACTOR_CRITIQUE_V2.md (v2 critique)
  docs/DI_REFACTOR_REPORT.md
  docs/DI_REFACTOR_VALIDATION_REPORT.md
  → Status: arc complete. The 25 locked decisions + architecture overview are reusable.
    Everything else is process audit-trail. Archive bucket: di-refactor.

CLUSTER 4: Cross-platform install fix (Phase 5, 2026-05-24)
  docs/PLAN_CROSS_PLATFORM_INSTALL_FIX.md
  docs/VERIFICATION_2026-05/SUMMARY.md
  docs/VERIFICATION_2026-05/empirical_act_verification.md
  docs/VERIFICATION_2026-05/cursor.md (also part of cluster 5)
  docs/VERIFICATION_2026-05/IMPLEMENTATION_REPORT.md
  docs/VERIFICATION_2026-05/IMPLEMENTATION_VALIDATION.md
  docs/VERIFICATION_2026-05/README_REWRITE_PREVIEW.md
  docs/VERIFICATION_2026-05/README_REWRITE_REPORT.md
  → Status: arc complete. SUMMARY.md and cursor.md have reusable content;
    the rest is audit trail. Archive bucket: phase-5-cross-platform-install.

CLUSTER 5: Empirical CLI baseline
  docs/EMPIRICAL_CLI_FINDINGS/README.md
  docs/EMPIRICAL_CLI_FINDINGS/codex.md     (partially superseded)
  docs/EMPIRICAL_CLI_FINDINGS/cursor.md    (FULLY superseded by VERIFICATION_2026-05/cursor.md)
  docs/EMPIRICAL_CLI_FINDINGS/devin.md     (still current)
  docs/EMPIRICAL_CLI_FINDINGS/gemini.md    (partially superseded)
  docs/EMPIRICAL_CLI_FINDINGS/windsurf.md  (still current)
  → Status: split. Two files (devin, windsurf) are current. Cursor is replaced.
    The rest is partially overlapping with docs/PLATFORM_INSPECTION_CATALOG.md
    and with VERIFICATION_2026-05/. Worth merging all live CLI knowledge into
    one canonical per-platform reference.

CLUSTER 6: Cross-cutting reference (always-live)
  README.md                           (user-facing)
  HANDOFF.md                          (project state)
  AGENTS.md                           (AI agent rules; some staleness)
  CHANGELOG.md                        (history)
  CONTRIBUTING.md                     (entry point for contributors; some staleness)
  PITFALLS.md                         (bug knowledge base; all historical)
  docs/RESUME_HERE.md                 (orientation; current)
  docs/ADDING_A_CONSTRUCT.md          (consolidated contributor walkthrough)
  docs/CONSTRUCT_TYPES.md             (reference table)
  docs/RULE_FORMAT.md                 (rule spec; live)
  docs/SKILL_FORMAT.md                (skill spec; live)
  docs/PLATFORM_INSPECTION_CATALOG.md (CI executable spec; partially stale)
  docs/REENTRY_TEST_PROTOCOL.md       (orientation-kit test process; partially stale)
  → Status: stays at top level (mostly). These are the "live" docs that survive
    the consolidation. Some need rewriting (AGENTS.md, ONBOARDING.md,
    CONTRIBUTING.md, PLATFORM_INSPECTION_CATALOG.md) to reflect the
    post-Phase-5 architecture.
```

## README drift assessment

Reading the current `README.md` against the other docs as of 2026-05-24:

**Things README claims that match reality:**
- "Multi-platform marketplace" with 6 platforms — matches `HANDOFF.md`, generator code, and test count.
- Install paths per platform (Claude `/plugin marketplace add ...`, Codex `codex plugin marketplace add ...`, Gemini `gemini extensions install <github-url> --consent`, Cursor team-marketplace import, Windsurf clone+open, Devin clone+`devin skills list`) — all match `docs/VERIFICATION_2026-05/SUMMARY.md` and `empirical_act_verification.md`. Every command in README appears as VERIFIED-PASS or as an IDE-action-sequence.
- Construct counts (27 skills, 21 rules) — match the source tree (verified by `git ls-files`).
- 81-plugin marketplace entry count — matches `HANDOFF.md`.
- Repository Structure section (post-Phase-5 layout including `.agents/skills/`, root-level `gemini-extension.json`, `.cursor-plugin/marketplace.json`) — accurate.
- Notes about Codex enumeration + install both working — match `docs/VERIFICATION_2026-05/SUMMARY.md` Finding 2/3.
- Gemini stderr quirk for `extensions list` / `mcp list` — documented in catalog.

**Things README claims that need verification or are slightly drifted:**
- "All 27 skills are visible where previously they were not" (Windsurf section) — true per design but not externally verified end-to-end; documentation correctly says "per Windsurf Cascade docs" rather than claiming live empirical proof.
- "Gemini reports 'Skipping project agents due to untrusted folder' until the workspace is trusted" — true but only relevant to Gemini IDE/auth setup, not install. Slightly misleading placement.
- Cursor team marketplace import section says "Cursor 2.6+ teams" — `docs/VERIFICATION_2026-05/cursor.md` clarifies that as of 2026-05-01 the team marketplace can be set up "without a repository" too. Worth a footnote.

**Things that have NO drift (no contradiction between README and other docs):**
- Per-platform read paths (`.claude-plugin/`, `.codex-plugin/`, etc.) — match generator code and `docs/RESUME_HERE.md` table.
- Bundle install commands (`bundle-skill-all`, `bundle-quality-rules`, etc.) — match `catalog.toml` definitions.

**Verdict on README drift**: minor. The README is in good shape after the recent rewrite (b38d82b). It does NOT need urgent updating. The only nitpicks are (a) a footnote on Cursor 2026-05-01 update about no-repo team marketplaces, (b) clarification that Windsurf "27 visible" is design-level, not end-to-end-tested. Both are nice-to-have, not required.

## Open questions for human

These files have purposes I can characterize but where a consolidation decision really should be made with the user's input:

1. **`PITFALLS.md`** — All current entries reference commits and code paths from the pre-DI-refactor era (Textual TUI installer). `AGENTS.md` mandates a top-level PITFALLS.md per the user's global rules, so I cannot recommend deletion. But should the historical entries be cleared (since the code they reference is gone) or preserved as "pre-1.0 archive"? Either is defensible.

2. **`docs/REENTRY_TEST_PROTOCOL.md`** — This is a meta-process artifact (how to test that orientation docs work). Is the protocol still being used, or is this an aspiration that never had an active maintainer? If the latter, it should be archived. If active, it should be modernized for the post-Phase-5 state.

3. **`docs/EMPIRICAL_CLI_FINDINGS/README.md`** — Half-superseded by `docs/PLATFORM_INSPECTION_CATALOG.md` and half by `docs/VERIFICATION_2026-05/SUMMARY.md`. Should this become a stub pointing at the canonical reference, or should it be deleted entirely after the live content is merged?

4. **`docs/PLAN_DI_REFACTOR_CRITIQUE.md` and `_V2.md`** — These reviewer critiques are 100% process artifacts. The findings have been resolved per `docs/DI_REFACTOR_VALIDATION_REPORT.md`. Is there value in keeping the critique history as evidence of the design rigor, or is it pure noise once the validation report exists?

5. **The `pr1-body.md` file** — PR bodies on GitHub are durable; local copies usually aren't kept. Was this saved deliberately for offline reference, or is it a leftover from the PR creation process?
