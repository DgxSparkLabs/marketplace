# Research Directory — Navigation Guide

> **Last updated:** March 2026
> **Total sources:** 200+ across 6 platforms (GitHub, arXiv, Reddit, Kaggle, Twitter/X, DuckDuckGo)
> **Research rounds:** 12 iterations (R1–R12) plus deep-research synthesis

---

## Canonical Files (Start Here)

These are the **authoritative, current** research documents. Read these first.

### Knowledge Guides (Distilled — Read These Before Raw Data)

| File | Purpose |
|------|---------|
| [KNOWLEDGE_BASE.md](KNOWLEDGE_BASE.md) | **Distilled insights** — what works, what matters, key patterns from all 200+ sources |
| [ANTI_PATTERNS.md](ANTI_PATTERNS.md) | **Noise catalog** — dead ends, traps, and things that look good but aren't |
| [METHODOLOGY.md](METHODOLOGY.md) | **How to do research** — tools, search strategies, what yields results |
| [TASKS.md](TASKS.md) | **Maintenance backlog** — open tasks and rules for future updates |

### Per-Platform Findings (Raw Data)

| File | Platform | Lines | Content |
|------|----------|-------|---------|
| [SUMMARY_AND_CONCLUSIONS.md](SUMMARY_AND_CONCLUSIONS.md) | All | 431 | **Master synthesis** — cross-platform analysis, key players, strategic conclusions |
| [arxiv_findings.md](arxiv_findings.md) | arXiv | 445 | 38 papers catalogued, 14 deep-dived — agent economics, security, skill lifecycle |
| [github_findings.md](github_findings.md) | GitHub | 589 | 72+ repos — marketplace platforms, skill registries, MCP ecosystem |
| [reddit_findings.md](reddit_findings.md) | Reddit | 419 | 14 threads — user sentiment, pain points, monetization skepticism |
| [twitter_findings.md](twitter_findings.md) | Twitter/X | 443 | 14 threads, 9 platforms — hype signals, security incidents, product launches |
| [kaggle_findings.md](kaggle_findings.md) | Kaggle | 277 | 20+ datasets, 1 competition — freelance data, skill demand, fraud detection |
| [general_findings.md](general_findings.md) | DuckDuckGo | 529 | 10 articles, 85+ results — market sizing, business models |
| [competitive_landscape.md](competitive_landscape.md) | Mixed | 507 | 20+ reports — market sizing, funding, enterprise adoption |
| [industry_overview.md](industry_overview.md) | Mixed | 569 | Industry publications — platform sites, analyst reports |
| [skill-marketplace-landscape.md](skill-marketplace-landscape.md) | Mixed | 457 | Landscape overview — all platforms mapped |

### Reading Order

1. `KNOWLEDGE_BASE.md` — distilled insights organized by topic (security, economics, architecture, users)
2. `ANTI_PATTERNS.md` — things to avoid and noise to recognize
3. `SUMMARY_AND_CONCLUSIONS.md` — full executive synthesis with data tables
4. Platform-specific files (arxiv, github, reddit, twitter, kaggle) — deep detail per source
5. `competitive_landscape.md` + `industry_overview.md` — market sizing and business context
6. `METHODOLOGY.md` — when you need to do more research

---

## Research Rounds (Archival)

Each `skill-marketplaces-N/` subdirectory contains one research iteration. These are **raw research data** from successive rounds — valuable for provenance and tracing how findings evolved, but **not canonical**. The top-level files above are the consolidated, authoritative versions.

| Directory | Round | Key Content |
|-----------|-------|-------------|
| `skill-marketplaces/` | R1 | Original round — 38 arXiv papers, 67 GitHub repos, FINAL_SUMMARY.md |
| `skill-marketplaces-2/` | R2 | Cross-platform expansion (arxiv, github, kaggle, reddit, twitter) |
| `skill-marketplaces-3/` | R3 | Package management, skill evaluation, MCP security |
| `skill-marketplaces-4/` | R4 | Governance, enterprise deployment, skill orchestration |
| `skill-marketplaces-5/` | R5 | + industry_overview.md |
| `skill-marketplaces-6/` | R6 | + emerging_trends.md |
| `skill-marketplaces-7/` | R7 | Governance reckoning, pricing models, agent market economics |
| `skill-marketplaces-8/` | R8 | + web_deep_dive.md |
| `skill-marketplaces-9/` | R9 | + industry.md, consolidated across 6 platforms |
| `skill-marketplaces-10/` | R10 | Search results, scraped tweets, GitHub/Kaggle deep dives |
| `skill-marketplaces-11/` | R11 | FINAL_SUMMARY.md, MOTIVATION_AND_NEXT_STEPS.md |
| `skill-marketplaces-12/` | R12 | Full round with all platforms + SUMMARY.md, MOTIVATION.md |
| `deep-research/` | Synthesis | Comprehensive cross-platform report |

### When to Use Archival Rounds

- **Tracing a claim**: If a canonical file references a specific stat or project, check the round where it was first found.
- **Checking data freshness**: Star counts and project status evolve across rounds. Earlier rounds have earlier snapshots.
- **Recovering dropped detail**: If a canonical file summarizes a topic, the corresponding round file often has more granular data.

---

## File Provenance Rules

1. **Canonical files are the source of truth.** If a fact appears in both a canonical file and an archival round, the canonical file takes precedence.
2. **Never overwrite canonical files with wholesale rewrites.** Merge new findings incrementally. The canonical files represent careful consolidation across 12 rounds.
3. **New research rounds** should be added as `skill-marketplaces-N+1/` directories, then key findings merged into canonical files.
4. **Star counts and metrics** should note their source round and date. Numbers evolve across rounds.
5. **Raw artifacts** (scrape dumps, notebook outputs, batch results) are gitignored. Only curated analysis files are committed.

---

## Key Statistics (Quick Reference)

| Metric | Value | Source |
|--------|-------|--------|
| AI agent skills indexed (SkillsGate) | 45,000+ | GitHub |
| AI agent skills claimed (SkillsMP) | 500,000+ | Twitter/X |
| SkillNet academic repository | 200,000+ | arXiv |
| Top GitHub repo stars (anthropics/skills) | 94,879 (verified March 2026) | GitHub |
| Top community repo stars (phuryn/pm-skills) | 7,382 (verified March 2026) | GitHub |
| Community skills with vulnerabilities | 26.1–36.82% | arXiv, Snyk ToxicSkills |
| Malicious skills in ClawHavoc attack | ~1,200 | arXiv (SoK) |
| Competing platforms identified | 15+ | All sources |
| AI agent market by 2030 | $47–53B (CAGR 41–46%) | Multi-source consensus |
| Academic papers (2024–2026) | 90+ | arXiv |
| Freelance contracts dataset | 1.3M entries | Kaggle |

---

## What's NOT Here

The following are gitignored (intermediate artifacts, not canonical research):
- `raw_scrape_*.txt` — raw web scrape dumps
- `nb*_content.txt` — notebook content extracts
- `batch*_results.md` — intermediate search batch results
- `scrape_*.md` / `scraped_*.md` — scrape processing notes
- `fetch_notebooks.py` — data collection script
