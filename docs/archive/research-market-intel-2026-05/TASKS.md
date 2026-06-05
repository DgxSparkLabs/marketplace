# Research Maintenance Tasks

> **Context:** The `research/` directory contains 90+ files across 12 research rounds. Agents have repeatedly caused confusion by rewriting canonical files instead of making incremental updates. This task list prevents that from happening again.

---

## Problem Statement

Agents working in this directory face three recurring issues:

1. **No canonical file markers** — agents can't tell which files are authoritative vs. archival
2. **No merge protocol** — agents rewrite files from scratch instead of merging findings incrementally
3. **No navigation guide** — with 12 research round directories, agents pick arbitrary files to read/modify

## Completed Fixes

- [x] **T1: Create `research/README.md`** — navigation index marking canonical files, archival rounds, and reading order
- [x] **T2: Update `AGENTS.md`** — add research directory rules (never rewrite canonical files, merge incrementally, add new rounds as `skill-marketplaces-N+1/`)
- [x] **T3: Add `.gitignore` rules** — exclude raw scrape artifacts (`raw_scrape_*.txt`, `nb*_content.txt`, `batch*_results.md`, etc.)
- [x] **T4: Revert bad canonical file rewrites** — restored `arxiv_findings.md`, `github_findings.md`, `kaggle_findings.md`, `reddit_findings.md`, `twitter_findings.md` to their reviewed/committed versions
- [x] **T5: Commit untracked synthesis files** — `SUMMARY_AND_CONCLUSIONS.md`, `competitive_landscape.md`, `general_findings.md`, research rounds 10–12
- [x] **T8: Verify suspicious entries** — verified 16 repos against live GitHub API (March 2026). All R12 high-star repos confirmed real (anthropics/skills: 94,879, obra/superpowers: 87,967, VoltAgent: 38,269). Of 5 previously flagged "hallucinated" repos, 4 exist (only xpack-ai/XPack is truly nonexistent). Updated `ANTI_PATTERNS.md` and `METHODOLOGY.md` with verification results.
- [x] **T9: Deduplicate `FINAL_SUMMARY.md` vs `SUMMARY_AND_CONCLUSIONS.md`** — designated `SUMMARY_AND_CONCLUSIONS.md` as canonical master summary, marked both `FINAL_SUMMARY.md` files as archival with superseded notes, incrementally merged R7-R12 findings (security crisis, 5-layer architecture, regulatory landscape, blockchain, security solutions, market sizing) into the canonical file as an addendum.

## Future Tasks

- [ ] **T6: Synthesize R10–R12 into canonical files** — rounds 10, 11, and 12 have per-platform findings (`arxiv.md`, `github.md`, etc.) that haven't been merged into the top-level canonical files yet. Merge incrementally — do NOT rewrite.
- [ ] **T7: Reconcile star counts** — add "as of Round N" annotations to the canonical `github_findings.md`. Verified star counts (March 2026): phuryn/pm-skills: 7,382, daymade/claude-code-skills: 656, binance/binance-skills-hub: 465. See `METHODOLOGY.md` for full verified list.
- [ ] **T10: Archive raw search artifacts in R1** — `skill-marketplaces/search{1-10}_results.{txt,json}` are raw search dumps from R1. Consider gitignoring or moving to a `raw/` subdirectory.

## Rules for Future Research Updates

1. **Read `research/README.md` first** before touching any research file
2. **Never wholesale-rewrite a canonical file** — merge new findings into existing structure
3. **New research rounds go in `skill-marketplaces-N+1/`** — then selectively merge key findings upstream
4. **Verify before citing** — check star counts and repo existence against live sources before adding to canonical files
5. **Note provenance** — when adding a data point, note which research round it came from
