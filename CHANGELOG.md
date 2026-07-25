# Changelog

## 2026-07-25 — Template cleanup: project memory off main, docs made exact

Executed after the scope-down, from a three-lane evidence pass (full-file inventory, code-grounded doc audit, three independent newcomer walkthroughs):

- Project/session memory moved off `main` to the `project-memory` branch: STATE, HANDOFF, PITFALLS, LESSONS, RESUME_HERE, ROADMAP (inlined into referrers), `docs/archive/` (490 files), `docs/.discussion/`, VAULT-RULES, `.devcontainer/`.
- `generate_manifest.py --check` is now read-only: it restores the pre-check tree on drift instead of silently regenerating in place (the fail-once-then-pass trap all three walkthroughs hit); regression-tested.
- Fork-rename CI trap fixed: compat workflows derive the marketplace identity from `src/MARKETPLACE.toml` instead of hardcoding it.
- Docs corrected against code with file:line evidence: README (browse command needs `--json`; stale install+enable two-step dropped; prerequisites + scope warnings added), SKILL_FORMAT (rewritten — removed a fictional `$SKILL_DIR` install-time substitution and all multi-platform content; the real mechanism is `${CLAUDE_PLUGIN_ROOT}`), AGENTS/SECURITY/RELEASING rewritten, example plugin READMEs corrected, published marketplace description no longer advertises six platforms.

## 2026-07-25 — Skills-only, Claude-only template scope-down (#18)

The marketplace was reduced from ten construct types x six platforms to **one construct (skills) on one platform (Claude Code)** and rebuilt as a **fork-ready template**: contributors touch `src/skills/` only; `regen-bot` CI validates (naming standard #19), regenerates, and commits all install artifacts on push to main. Executed as PR #37 (platform shrink), PR #38 (construct shrink), PR #39 (CI inversion + naming enforcement), and the template-polish PR (docs). The fork->commit->CI->install contract was proven end-to-end on a real fork (evidence on #18). Every removed capability has a `status:someday` re-expansion issue (#20-#36); no removed code is archived in-tree — recover concepts from git history or the `project-memory` branch.

Incident recorded: PR #38 silently dropped both test suites' `unittest.main` blocks, making the suite gate vacuously green until caught and fixed (`32fedd5`, hardened in `8b19b12` — suites now run via `-m unittest` with a nonzero-test-count assertion). see the `project-memory` branch (PITFALLS entry).

---

Older entries (multi-platform era, construct QA arcs, v1.0.0) are preserved on the [`project-memory` branch](https://github.com/DgxSparkLabs/marketplace/tree/project-memory) and in git history.
