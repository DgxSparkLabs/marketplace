# Research Methodology

> **Purpose:** How the research was done. What tools and strategies worked, what was noise, how to extend. A rookie agent can use this to do more research without reinventing the approach.

---

## Overview

12 research rounds were conducted between March 2026, covering 6 platforms:

| Platform | Tool Used | What We Searched | Yield |
|----------|-----------|-----------------|-------|
| GitHub | `github-search` skill + `gh` CLI | Repos, code, README patterns | 72+ repos in canonical, 182+ across all rounds |
| arXiv | `duckduckgo-search` skill + `web-scraper` | Site-restricted searches (`site:arxiv.org`) | 38+ papers in canonical, 90+ across all rounds |
| Reddit | `duckduckgo-search` + `web-scraper` (old.reddit.com) | Thread discovery, then full thread scraping | 14+ threads in canonical, 53+ across all rounds |
| Twitter/X | `duckduckgo-search` + `web-scraper` | Site-restricted searches | 14+ threads in canonical, 130+ signals across all rounds |
| Kaggle | `duckduckgo-search` + Kaggle API (via `uv run`) | Datasets, competitions, notebooks | 20+ datasets, 1 competition |
| Web (DuckDuckGo) | `duckduckgo-search` skill | Industry articles, reports, company pages | 85+ results, 10 deep-scraped articles |

---

## What Worked

### 1. Site-restricted DuckDuckGo searches

The most productive strategy. Restrict searches to a specific platform and use domain-specific query terms.

**arXiv example queries (high yield):**
```
site:arxiv.org "skill marketplace" AI agent 2025
site:arxiv.org agent skill security vulnerability 2025
site:arxiv.org "agent exchange" OR "skill exchange" market
site:arxiv.org talent marketplace matching algorithm
site:arxiv.org multi-agent skill sharing composition
```

**GitHub example queries (high yield):**
```
skill marketplace language:python stars:>10
agent skills SKILL.md
MCP marketplace registry
claude code skills marketplace
```

**Reddit example queries (high yield):**
```
site:reddit.com "skill marketplace" AI agent
site:reddit.com claude code skills marketplace
site:reddit.com "agent skills" marketplace trust security
```

### 2. Scraping with `web-scraper` skill

The `web-scraper` skill (trafilatura-based) works well for:
- arXiv abstract pages (clean extraction)
- Reddit threads via `old.reddit.com` (bypasses SPA issues)
- Blog posts and articles (trafilatura handles boilerplate removal)

It does NOT work well for:
- Kaggle pages (SPA, requires API instead)
- Twitter/X pages (rate limited, often blocked)
- GitHub repo pages (use `gh` CLI instead)

### 3. The `github-search` skill for deep repo exploration

For GitHub, the `github-search` skill is far more effective than web scraping. It:
- Searches via GitHub API (structured results)
- Reads README, file trees, source code, issues
- Provides synthesis of patterns and gotchas

For maximum yield, follow up with `gh repo view <owner/repo>` and `gh api repos/<owner/repo>/contents` to explore file structure.

### 4. Iterative round-based research

Each round (`skill-marketplaces-N/`) built on the previous. This worked because:
- Earlier rounds established baseline knowledge
- Later rounds focused on gaps identified in earlier rounds
- Each round's `SUMMARY.md` noted what was new vs. confirmed

**Round progression:**
- R1-R2: Discovery and mapping (what exists?)
- R3-R4: Depth on security, governance, enterprise (what's important?)
- R5-R7: Industry analysis, business models, economics (what works commercially?)
- R8-R9: Protocol adoption, crisis events, standards (what's happening now?)
- R10-R12: Targeted deep dives and verification

### 5. Cross-platform triangulation

The strongest findings are ones confirmed across multiple platforms:
- "Trust is the product" — confirmed by Reddit (user demand), arXiv (academic analysis), Twitter (security incidents), GitHub (project architectures)
- "26.1% vulnerability rate" — confirmed by arXiv (Agent Skills survey) AND independently by Snyk (36.82%) AND by ClawHavoc (1,200 malicious skills)

**Rule:** Single-source findings are hypotheses. Multi-source findings are insights. Always cross-reference.

---

## What Was Noise

### Low-yield search strategies

1. **Generic "skill marketplace" searches** — dominated by human talent/freelance marketplaces (Upwork, Fiverr), not AI agent skills. Add "AI agent" or "SKILL.md" to disambiguate.

2. **Kaggle web scraping** — Kaggle is an SPA. The `web-scraper` skill returns minimal content. Use the Kaggle API directly:
   ```bash
   kaggle datasets list -s "skill marketplace" --sort-by hottest
   kaggle competitions list -s "freelance"
   ```

3. **Twitter/X direct scraping** — rate limited and often returns login walls. DuckDuckGo `site:twitter.com` or `site:x.com` works better than direct scraping.

4. **arXiv broad queries** — "marketplace" alone returns economics papers. Always include "AI agent" or "skill" or "LLM" in arXiv queries.

### Low-value content patterns

1. **"Awesome list" repos** — curated lists of links. Useful as research seeds but not as implementation references.
2. **Hackathon/student projects** — high volume, low quality. Most freelance marketplace repos are weekend projects. Filter by stars > 10 to skip.
3. **Self-promotional Twitter threads** — founders hyping their own products. Cross-reference with GitHub activity (are people actually using it?).
4. **AI-generated research summaries** — some arXiv papers and blog posts are themselves AI-generated with questionable data. Look for specific metrics, datasets, and reproducible methodology.

---

## How to Extend This Research

### Adding a new research round

1. Create `research/skill-marketplaces-13/` (increment from the latest round)
2. For each platform, create a findings file (`github.md`, `arxiv.md`, etc.)
3. Focus on what's NEW since R12 — don't re-research what's already covered
4. Create a `SUMMARY.md` noting key additions
5. Merge the most important findings into the canonical top-level files incrementally
6. Update `research/README.md` to include the new round

### Recommended search queries for future rounds

**GitHub (check monthly):**
```
skill marketplace created:>2026-03-01 stars:>5
SKILL.md marketplace pushed:>2026-03-01
MCP registry security pushed:>2026-03-01
```

**arXiv (check weekly):**
```
site:arxiv.org "agent skill" OR "skill marketplace" 2026
site:arxiv.org "MCP" "security" agent 2026
site:arxiv.org "tool use" marketplace verification 2026
```

**Reddit (check weekly):**
```
site:reddit.com "skill marketplace" OR "agent skills" after:2026-03-01
site:reddit.com "claude code" marketplace skills
```

### Tools available in this repo

| Task | Tool | Example |
|------|------|---------|
| Web search | `duckduckgo-search` skill | `/duckduckgo-search site:arxiv.org agent skill security 2026` |
| Web scraping | `web-scraper` skill | `/web-scraper https://arxiv.org/abs/2603.04448` |
| GitHub search | `github-search` skill | `/github-search skill marketplace SKILL.md stars:>10` |
| YouTube research | `youtube-search` + `youtube-wisdom` | `/youtube-search AI agent skill marketplace` |
| Session recall | `session-history` skill | `/session-history search "marketplace"` |
| Prior art check | `prior-art` rule (always active) | Automatically triggers before building anything non-trivial |

### Verification protocol

Before adding any finding to a canonical file:

1. **Verify the source exists.** If it's a GitHub repo, check it on live GitHub. If it's an arXiv paper, check the arXiv page.
2. **Note provenance.** "Found in R13 via DuckDuckGo search for X" or "Verified on GitHub 2026-04-01."
3. **Cross-reference.** Is this confirmed by another source? Multi-source findings go in the main body. Single-source findings go in notes.
4. **Check for contradictions.** Does this contradict something in the existing canonical file? If so, note both positions.

---

## Research Infrastructure

### File organization

```
research/
├── README.md                    ← Navigation index (read first)
├── KNOWLEDGE_BASE.md            ← Distilled insights (read second)
├── ANTI_PATTERNS.md             ← Dead ends and traps (read third)
├── METHODOLOGY.md               ← This file (how to do more research)
├── TASKS.md                     ← Maintenance backlog
├── SUMMARY_AND_CONCLUSIONS.md   ← Master synthesis
├── {platform}_findings.md       ← Per-platform canonical files
├── competitive_landscape.md     ← Market sizing and competitive analysis
├── industry_overview.md         ← Industry publications analysis
├── skill-marketplace-landscape.md ← Platform mapping
├── deep-research/               ← Single-round deep synthesis
└── skill-marketplaces-{1-12}/   ← Archival research rounds
```

### Data quality tiers

| Tier | Definition | Example |
|------|-----------|---------|
| **Verified** | Checked against live source, cross-referenced | phuryn/pm-skills: 7,382 stars (verified March 2026), anthropics/skills: 94,879 stars (verified March 2026) |
| **Corroborated** | Appears in 2+ research rounds with consistent data | 26.1% vulnerability rate (arXiv + Snyk audit) |
| **Reported** | Appears in one research round, not independently verified | Single-round data without live verification |
| **Suspect** | Inconsistent across rounds or no provenance trail | xpack-ai/XPack (confirmed nonexistent March 2026) |

**Verified repos (March 2026 GitHub API check):** phuryn/pm-skills (7,382), anthropics/skills (94,879), obra/superpowers (87,967), VoltAgent/awesome-openclaw-skills (38,269), VoltAgent/awesome-agent-skills (11,458), numman-ali/openskills (9,035), daymade/claude-code-skills (656), binance/binance-skills-hub (465), sickn33/antigravity-awesome-skills (24,861), vercel-labs/agent-skills (23,107), kepano/obsidian-skills (14,303), agentskills/agentskills (13,261), WordPress/agent-skills (905), docker/mcp-registry (453), archestra-ai/archestra (3,547), iflytek/skillhub (225).

When extending research, aim for Verified or Corroborated tier. Note the tier when adding to canonical files.
