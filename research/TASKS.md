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

## Future Tasks (Not Yet Started)

- [ ] **T6: Synthesize R10–R12 into canonical files** — rounds 10, 11, and 12 have per-platform findings (`arxiv.md`, `github.md`, etc.) that haven't been merged into the top-level canonical files yet. Merge incrementally — do NOT rewrite.
- [ ] **T7: Reconcile star counts** — some GitHub repos show different star counts across rounds (e.g., `phuryn/pm-skills`: 7,312 → 7,317 → 7,322). Add "as of Round N" annotations to the canonical `github_findings.md`.
- [ ] **T8: Verify suspicious entries** — the R11/R12 data contains repos with very high star counts (`VoltAgent/awesome-openclaw-skills`: 38K, `numman-ali/openskills`: 9K) that should be verified against live GitHub before citing in canonical files.
- [ ] **T9: Deduplicate `FINAL_SUMMARY.md` vs `SUMMARY_AND_CONCLUSIONS.md`** — both `research/skill-marketplaces/FINAL_SUMMARY.md` (381 lines, covers R1–R9) and `research/SUMMARY_AND_CONCLUSIONS.md` (431 lines) serve similar roles. Decide which is canonical and note the other as superseded.
- [ ] **T10: Archive raw search artifacts in R1** — `skill-marketplaces/search{1-10}_results.{txt,json}` are raw search dumps from R1. Consider gitignoring or moving to a `raw/` subdirectory.

## Rules for Future Research Updates

1. **Read `research/README.md` first** before touching any research file
2. **Never wholesale-rewrite a canonical file** — merge new findings into existing structure
3. **New research rounds go in `skill-marketplaces-N+1/`** — then selectively merge key findings upstream
4. **Verify before citing** — check star counts and repo existence against live sources before adding to canonical files
5. **Note provenance** — when adding a data point, note which research round it came from
