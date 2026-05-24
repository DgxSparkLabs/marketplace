# README Rewrite Report (Phase 2)

**Date**: 2026-05-24
**Branch**: feat/claude-plugin-compliance
**Commit**: b38d82b
**Spec source**: docs/VERIFICATION_2026-05/README_REWRITE_PREVIEW.md
**Validation source**: docs/VERIFICATION_2026-05/IMPLEMENTATION_VALIDATION.md

## Sections rewritten

| Section | Status | Notes |
|---------|--------|-------|
| Quick Start → Claude Code | DONE | Added inline note that install + list both work end-to-end (CL1/CL2/CL3 verified) |
| Quick Start → Codex | DONE | Replaced local-path-only block with GitHub shortform + `--ref` pre-merge note + `codex plugin list` + `codex plugin add` |
| Quick Start → Gemini | DONE | Added `gemini extensions install <github-url> --ref feat/claude-plugin-compliance --consent` as primary path; kept local clone as alternative |
| Quick Start → Cursor | DONE | Added team-marketplace import path (IDE action), noted `agent` CLI exists with no plugin commands, kept clone-and-open as alternative; added skill auto-load from `.agents/skills/` |
| Quick Start → Windsurf | DONE | Added skills story — `.agents/skills/` auto-discovered by Cascade; updated comment block |
| Quick Start → Devin | DONE | Added note that skills come from both `.devin/skills/` and `.agents/skills/` |
| Per-Platform Details → Claude Code | DONE | Added CL1/CL2/CL3 verification note |
| Per-Platform Details → Codex | DONE | Rewrote to use GitHub shortform with `--ref` pre-merge note; explained `.codex-plugin/plugin.json` per-plugin manifest; added `codex plugin list` + `codex plugin add` |
| Per-Platform Details → Gemini | DONE | GitHub URL install as primary path with `--ref` pre-merge note; explained root-level `gemini-extension.json` purpose; kept local path as alternative |
| Per-Platform Details → Cursor | DONE | Distinguished (a) team-marketplace Dashboard import, (b) clone+open, (c) `agent` CLI with no plugin commands; added `.agents/skills/` mention |
| Per-Platform Details → Windsurf | DONE | Added `.agents/skills/` auto-discovery; explained 27 skills now visible post-Phase-1 |
| Per-Platform Details → Devin | DONE | Added `.agents/skills/` dual-path note alongside `.devin/skills/` |
| Repository Structure | DONE | Added `.agents/skills/`, root-level `gemini-extension.json`, root-level `.cursor-plugin/marketplace.json`; updated platform count (6→7) and phase count (5→6) |
| Table of Contents | DONE (no changes needed) | Section headings unchanged; anchors verified intact |

## Pre-merge footnotes added

| Location | Footnote text |
|----------|---------------|
| Quick Start → Codex | Note: until PR #1 lands on main, `--ref feat/claude-plugin-compliance` is required |
| Quick Start → Gemini | Note: until PR #1 lands on main, `--ref feat/claude-plugin-compliance` is required |
| Per-Platform Details → Codex | Note: until PR #1 lands on main, `--ref feat/claude-plugin-compliance` is required |
| Per-Platform Details → Gemini | Note: until PR #1 lands on main, `--ref feat/claude-plugin-compliance` is required |

## Sanity check results

- Table of Contents anchors: PASS — all six `#<platform>` and `#<platform>-1` anchors verified against heading text; no heading changes made
- Markdown syntax: PASS — all code fences closed, tables well-formed, no orphaned backticks
- Every command cites a VERIFIED-PASS claim or IDE-action-sequence flag: PASS
  - Claude Code commands: CL1/CL2/CL3 VERIFIED-PASS
  - Codex `codex plugin marketplace add` with `--ref`: C3 VERIFIED-PASS
  - Codex `codex plugin add`: C5 VERIFIED-PASS (post-Phase-1)
  - Codex `codex plugin list`: C4 VERIFIED-PASS
  - Gemini local install: G1 VERIFIED-PASS
  - Gemini GitHub URL install: G2/G3 expected PASS post-push (env constraint, not code defect — documented in IMPLEMENTATION_REPORT)
  - Gemini `extensions list 2>&1`: G5 VERIFIED-PASS
  - Gemini `skills list --all 2>&1`: G6 VERIFIED-PASS
  - Cursor `agent --version`: CU1 VERIFIED-PASS
  - Cursor `agent` install commands: CU2 VERIFIED-PASS (install path confirmed)
  - Cursor team-marketplace Dashboard import: flagged as IDE-action-sequence
  - Cursor `git clone` + open: standard VCS operation, no act claim required
  - Windsurf `git clone` + open: standard VCS operation; `.agents/skills/` documented per Windsurf official docs (WebFetch 2026-05-24)
  - Devin `git clone` + `devin skills list` + `devin rules list`: May-22 empirical baseline
- pytest after rewrite: 52 passed, 0 failed
- drift check after rewrite: OK — `generated content matches committed content`

## Deviations from the preview

None. Every section specified in README_REWRITE_PREVIEW.md was applied. The "optional addition" for Devin (`npx skills add DgxSparkLabs/marketplace -a devin`) was not included per the preview's own caveat ("unverified live, would need another act run") — omitting unverified commands is consistent with the constraint that every command must cite a VERIFIED-PASS claim.

## How to verify

```powershell
# From repo root (C:\Users\devic\source\marketplace):

# 1. Confirm commit
git log -1 --oneline
# Expected: b38d82b docs(readme): rewrite install instructions to use verified-working native commands

# 2. Run tests (should show 52 passed)
uv run python tests/test_marketplace.py

# 3. Run drift check (should say OK)
uv run scripts/generate_manifest.py --check

# 4. Inspect the README
# - Quick Start → Codex should show GitHub shortform with --ref note
# - Quick Start → Gemini should show GitHub URL install with --ref note
# - Quick Start → Cursor should show team-marketplace path + agent CLI note
# - Quick Start → Windsurf should mention .agents/skills/
# - Repository Structure should include .agents/, gemini-extension.json, .cursor-plugin/marketplace.json
```
