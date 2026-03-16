# Anti-Patterns & Noise Catalog

> **Purpose:** Things that look promising but aren't. Dead ends we've cataloged so you don't waste time on them. If you encounter any of these patterns in the wild, this document tells you what to think.
>
> **Sources:** 200+ sources across 12 research rounds. Each entry cites its origin.

---

## Table of Contents

1. [Project Anti-Patterns](#1-project-anti-patterns) — dead GitHub repos and failed approaches
2. [Strategy Anti-Patterns](#2-strategy-anti-patterns) — wrong ways to build a marketplace
3. [Data Anti-Patterns](#3-data-anti-patterns) — noise, fabrication, and misleading metrics
4. [Security Anti-Patterns](#4-security-anti-patterns) — false senses of security
5. [Economic Anti-Patterns](#5-economic-anti-patterns) — pricing and monetization traps
6. [Research Anti-Patterns](#6-research-anti-patterns) — how agents have previously gone wrong in this repo

---

## 1. Project Anti-Patterns

### Dead categories on GitHub

**Freelance marketplace clones.** All freelance marketplace repos in our GitHub research (Search 5) are hobby projects with 0-51 stars, mostly PHP, mostly dead. The traditional freelance marketplace is a mature, capital-intensive space dominated by Upwork/Fiverr. Building another one on GitHub is not where innovation happens.
- *If you find one:* Skip. Focus on AI-agent-native marketplaces instead.
- *Source:* `github_findings.md`, lines 409-425

**Web3/decentralized talent marketplaces.** Every "decentralized talent marketplace" repo has 0-2 stars: BlocklanceHQ, DigiFreelance-hub, Earnify, NeuroGuild-Network, Skill-Exchange-Platform. The blockchain adds complexity without solving the trust problem.
- *If you find one:* Interesting concept, zero traction. Note it and move on.
- *Source:* `github_findings.md`, `skill-marketplaces/github_findings.md` (category D)

**Peer-to-peer skill barter platforms.** All 11 barter/swap platforms in our research (SkillSwapAI, expair, Maven, etc.) have negligible adoption. The economics of barter don't work when one side has AI capabilities.
- *If you find one:* Conceptually novel, practically dead. The "Craigslist for skills" idea doesn't work.
- *Source:* `skill-marketplaces/github_findings.md` (category F)

### Low-value projects that look impressive

**Repos with high star counts but no substance.** "Awesome list" repos accumulate stars through aggregation, not innovation. VoltAgent/awesome-agent-skills (11K+ stars) is a curated list, not a marketplace. Don't confuse curation with product.
- *If you find one:* Useful as a research source, but not a competitor or implementation reference.

**Repos with suspiciously high star counts.** Our R11/R12 research rounds contain some entries with star counts that seem implausibly high for niche repos (e.g., 38K+ stars for `VoltAgent/awesome-openclaw-skills`). These have NOT been verified against live GitHub and may reflect data inflation or hallucination in the research process itself.
- *If you find one:* **Always verify star counts on live GitHub before citing.** Never trust research round data at face value.
- *Source:* Review finding from session 190375a7; `research/TASKS.md` (T8)

### Abandoned innovative projects

**SquidBay** (Bitcoin Lightning agent-to-agent marketplace, 2 stars). Has the most innovative concept we found — 3-tier pricing (Rent/Learn/Own), 98% to seller, agent identity, locked names. But 2 stars and minimal traction. The vision may be ahead of the market.
- *If you encounter it:* Study the architecture (it's excellent). Don't assume it's proven.
- *Source:* `github_findings.md`, `skill-marketplaces/github_findings.md` (#33)

**tiger_cowork** (self-hosted workspace with reflection loop, 0.0-1.0 scoring). Novel quality assurance mechanism but abandoned.
- *If you encounter it:* The reflection loop pattern (agent self-scores 0.0-1.0) is worth stealing. The project itself is dead.
- *Source:* `skill-marketplaces/github_findings.md` (#30)

---

## 2. Strategy Anti-Patterns

### Building for volume over trust

**The SkillsMP trap.** SkillsMP claims 500K+ skills. 351K skills with stars/date-only ranking. No curation, no verification, no quality signal. Result: more noise than value and an invitation for malicious content.
- *What to think:* Volume is a vanity metric. 51.4% of ClawHub skills were filtered as spam. Catalog size without trust is a liability, not an asset.
- *Source:* `twitter_findings.md`, `SUMMARY_AND_CONCLUSIONS.md` (lines 67-70)

### Commerce-first, community-last

Reddit is emphatic: build the community first, monetize second. Platforms that gate content behind payment before earning trust fail. Community solves supply, demand, AND retention simultaneously.
- *What to think:* If someone pitches "pay-to-list" or "pay-to-access" as the initial model, they haven't read the user research.
- *Source:* `reddit_findings.md`, `SUMMARY_AND_CONCLUSIONS.md` (lines 327-329)

### Standalone MCP hosting

Cloudflare, Vercel, and Docker all launched competing MCP hosting. Cloud giants bundle this for free. You cannot compete on hosting.
- *What to think:* Build the trust/discovery layer, not the hosting layer. Infrastructure is being commoditized by cloud giants.
- *Source:* `competitive_landscape.md` (lines 338, 447)

### General-purpose horizontal agents

Only Manus AI ($75M) got large funding for horizontal agents. The market rewards vertical, domain-specific approaches.
- *What to think:* "We do everything for everyone" is a losing position. "We do crypto skills better than anyone" is a winning one.
- *Source:* `competitive_landscape.md` (lines 332-343)

### Adapting incumbent labor marketplaces

Upwork and Fiverr are structurally conflicted — AI agents threaten to replace their supply side (human freelancers). Their incentive structure prevents them from embracing AI-native skills.
- *What to think:* Build around them, not through them. They will resist disruption.
- *Source:* `competitive_landscape.md` (lines 342, 449)

---

## 3. Data Anti-Patterns

### Star count inflation

Star counts evolve across research rounds and are not always reliable:
- `phuryn/pm-skills`: 7,312 (old) → 7,317 (R9) → 7,322 (R12) → 7,382 (verified March 2026) — normal growth
- `VoltAgent/awesome-openclaw-skills`: 38,090 → 38,102 (R12) → 38,269 (verified March 2026) — the apparent 12-star decrease between rounds was measurement timing, not real; repo is growing normally

**Rule:** When citing star counts, note the research round and date. Never present them as current without live verification.

### Previously flagged "hallucinated" repos — correction

A prior review flagged 5 repos as likely fabricated because they appeared in a rejected rewrite without provenance in any research round. **Live verification (March 2026) shows 4 of 5 exist:**

| Repo | Status | Actual Stars | Notes |
|------|--------|-------------|-------|
| `WordPress/agent-skills` | Exists | 905 | Real repo, no provenance in research rounds |
| `docker/mcp-registry` | Exists | 453 | Real repo, no provenance in research rounds |
| `archestra-ai/archestra` | Exists | 3,547 | Real repo, no provenance in research rounds |
| `iflytek/skillhub` | Exists | 225 | Real repo, no provenance in research rounds |
| `xpack-ai/XPack` | **Not Found** | — | Confirmed nonexistent |

The original issue was lack of provenance trail, not fabrication. However, the star counts in the rejected rewrite may still have been wrong (we don't have the original claimed values to compare). The rule stands: verify before citing.

**Rule:** If a repo has no provenance trail through the research rounds, treat it as unverified. Check it on live GitHub before including in any canonical file.

### Misleading platform metrics

- SkillsMP claims "500K+ skills" — unverified, likely includes duplicates and auto-generated content
- Skills.sh claims "80% AI slop" — their own community acknowledges quality problems
- "350K+ skills in ~2 months" — volume says nothing about quality

**Rule:** Platform-reported metrics are marketing. Cross-reference with independent sources (academic audits, community sentiment, actual GitHub activity).

### Research date confusion

Our research files have inconsistent dates:
- Headers say "July 2025" but content references events from March 2026
- arXiv IDs with `2603.xxxxx` prefix (March 2026) appear under "February 2026" dates
- The FINAL_SUMMARY correctly notes "March 16, 2026" but per-platform files still say "July 2025"

**Rule:** Treat research dates as approximate. The actual date of the research is when the git commit was made, not what the header says.

---

## 4. Security Anti-Patterns

### Trusting marketplace rankings

The #1 most downloaded skill on OpenClaw ("What Would Elon Do") had 9 security vulnerabilities (2 CRITICAL), silently exfiltrated data AND used prompt injection. It was downloaded THOUSANDS of times. Rankings are trivially gameable.
- *What to think:* Install counts and star ratings are NOT trust signals. Only verified security scans provide trust.
- *Source:* `twitter_findings.md` (lines 55, 175-176)

### Heuristic-only security scanning

SkillScan (static analysis + LLM) achieves only 86.7% precision, 82.5% recall. That means ~17% of malicious skills slip through AND ~13% of clean skills get false-flagged. Regex patterns are a start, not a solution.
- *What to think:* Our 104-test suite is better than most, but formal verification (SkillFortify: 96.95% F1) is the gold standard. Don't get complacent.
- *Source:* `arxiv_findings.md` (lines 194-196)

### Assuming uninstall removes the threat

Memory poisoning survives uninstallation. A malicious skill can write persistent data that affects future sessions even after removal.
- *What to think:* Sandboxing and `allowed-tools` restriction (which this marketplace already does) is essential. But detection post-install is not enough — prevention pre-install is necessary.
- *Source:* `arxiv_findings.md`, FINAL_SUMMARY security section

### "Skills don't look like code"

"Skills don't look like code — but they're executable." (Aikido.dev's Charlie Eriksen). Markdown and YAML instructions ARE code when an agent executes them. The security mental model must treat skills as untrusted executables, not documentation.
- *Source:* `twitter_findings.md` (lines 386-387)

---

## 5. Economic Anti-Patterns

### Commission-based pricing (the Upwork model)

Universally hated. "Competing on price is a loser for any supplier." "The lowest bidder usually gets the job" destroys quality. Upwork's 20%→5% sliding scale is the canonical example of what NOT to do.
- *What to think:* Low platform fees (SquidBay: 2%) or buy-once (Agensi) are better received. Revenue should come from premium features, not transaction tax.
- *Source:* `reddit_findings.md` (lines 218-225, 305-311)

### Competing on content alone

"The skills themselves trend toward free. Compete on trust, security, curation, and reliability." Skills are text files — the value isn't the content, it's the trust layer around it.
- *What to think:* If your business plan is "we have more skills," you've already lost to SkillsMP (500K+). Compete on quality, trust, and verification.
- *Source:* `reddit_findings.md` (lines 246-249, 272-278)

### Ignoring rapid obsolescence

"This shit changes rapidly so skills could be entirely different or meaningless in a month." Skills decay as models and APIs evolve.
- *What to think:* Version tracking, compatibility declarations, and decay signals are necessary infrastructure. A catalog that doesn't track freshness becomes stale in weeks.
- *Source:* `reddit_findings.md` (lines 110, 237-239)

### Free-without-monetization

Manufact has 5M+ SDK downloads and zero revenue. The open-source paradox: free adoption is easy, sustainable revenue is hard.
- *What to think:* "Free to use, paid to trust" is the emerging model. Free search/browse/install + paid verification/security/enterprise features.
- *Source:* `competitive_landscape.md` (lines 340, 403-409)

---

## 6. Research Anti-Patterns

These are mistakes that have actually happened in this repository. Learn from them.

### Wholesale rewriting canonical files

A previous agent rewrote all 5 canonical research files from scratch, dropping 21 arXiv papers, 38 GitHub repos, and entire analysis sections (fairness/bias, matching algorithms, decentralized architecture). The rewrite also introduced likely fabricated data (5 GitHub repos with specific star counts that don't exist in any research round).

**Rule:** NEVER wholesale-rewrite a canonical file. Merge new findings incrementally. See `research/README.md` for the protocol.

### Answering the wrong question

A previous agent was asked "how can this be resolved? break it down into tasks" (a meta/process question). Instead of creating a task breakdown, it rewrote 5 files totaling ~3,500 lines. Massive effort, wrong deliverable.

**Rule:** Read the prompt carefully. If asked for a plan, deliver a plan. If asked for a fix, deliver a fix. Don't conflate "I can do something impressive" with "I should do what was asked."

### Citing unverified research round data as fact

Research rounds 10-12 contain data that hasn't been cross-verified. Some entries have star counts that are inconsistent across rounds or implausibly high. Previous agents have cited this data without verification.

**Rule:** Verify before citing. Star counts and repo existence must be checked against live sources before adding to canonical files. Note provenance (which round, what date).

### Ignoring existing work

Multiple agents have started research from scratch rather than reading the existing 90+ files. This wastes time and creates contradictory or duplicate findings.

**Rule:** Read `research/README.md` first. Then `KNOWLEDGE_BASE.md`. Then `SUMMARY_AND_CONCLUSIONS.md`. Only THEN decide if new research is needed. The answer is usually "merge incrementally," not "start over."
