# SKILL MARKETPLACE: DEEP RESEARCH FINAL REPORT (Round 11)

> **Date:** March 16, 2026
> **Research Scope:** GitHub, Twitter/X, Reddit, arXiv, Kaggle + 10 prior research rounds
> **Total Sources Analyzed:** 250+ across 11 research rounds, 6 platforms
> **Files Generated:** 80+ research documents across /research directory

---

## EXECUTIVE SUMMARY

The AI agent skill marketplace is **the defining infrastructure battle of 2026**. In under 18 months, the space has gone from zero to:

- **500,000+ skills** listed across major marketplaces
- **8+ academic papers** published in Q1 2026 alone
- **20+ competing platforms** with no clear winner
- **$52.62B projected AI agent market** by 2030 (46.3% CAGR)
- **Binance, Gate.io, Oracle, Salesforce, Google** all building agent skill marketplaces
- **1,200+ malicious skills** infiltrated OpenClaw (ClawHavoc campaign) — the first major supply chain attack

The space is pre-product-market-fit. **Nobody has won. The window is wide open.**

---

## CROSS-PLATFORM SYNTHESIS

### What Each Source Told Us

| Platform | # Sources | Primary Signal | Key Insight |
|----------|-----------|---------------|-------------|
| **GitHub** | 67+ repos | Code & architecture | SKILL.md is the de facto standard; 7,320-star pm-skills leads; crypto exchanges building their own |
| **Twitter/X** | 30+ voices, 22 product launches | Hype & real products | "App Store for agents" narrative dominant; LarryBrain proved $3K MRR; security panic after ClawHavoc |
| **Reddit** | 14+ threads | User pain points & skepticism | "Trust is the product"; monetization skepticism high; non-technical users are the real market |
| **arXiv** | 13+ papers | Formal research & frameworks | 26.1% skills have vulnerabilities; curated skills +16.2pp pass rate; DAG orchestration beats flat |
| **Kaggle** | 20+ datasets | Data & skill taxonomies | No dedicated agent skills dataset yet; 3,291+ skill taxonomy available; job market proxies exist |
| **Competitive** | 10+ articles | Market sizing & models | $7.84B (2025) -> $52.62B (2030); MCP 97M+ downloads; commerce layer doesn't exist yet |

### Five Truths Every Source Agrees On

1. **Trust is the product, not skills.** Creating skills is trivial (vibe-coding). Distributing them is solved (GitHub). The hard problem is verification, security, and reputation. The platform that solves trust wins.

2. **Composability is the moat.** Flat skill lists are commoditized. DAG-based orchestration, skill chaining, and structured composition are what differentiate. (arXiv: AgentSkillOS proves this empirically.)

3. **Security is critical and unsolved.** 26.1% of community skills have vulnerabilities. The ClawHavoc campaign (1,200 malicious skills) proved supply chain attacks are real. No current solution offers formal guarantees.

4. **Curated > self-generated.** SkillsBench proves curated skills raise pass rates by 16.2pp while self-generated skills provide zero benefit on average. Human curation still matters.

5. **Vertical beats horizontal.** Binance (crypto), PM Skills (product management), Animation Principles (creative) — vertical-first marketplaces outperform generic ones.

---

## KEY PLAYERS MAP (March 2026)

### Tier 1: Dominant Platforms (Ecosystem-level)
| Player | Type | Scale | Differentiation |
|--------|------|-------|-----------------|
| **SkillsMP** (skillsmp.com) | Aggregator | 500,000+ skills | Largest catalog; viral growth |
| **OpenClaw Skills Registry** | Official | 13,729+ skills | Official OpenClaw registry, VirusTotal scanning |
| **Anthropic Agent Skills** | Official | 75,600 GitHub stars | First-party Claude skills |
| **SkillNet** (academic) | Infrastructure | 200,000+ skills | Multi-dimensional evaluation framework |

### Tier 2: Emerging Challengers
| Player | Type | Differentiation |
|--------|------|-----------------|
| **SkillX.sh** | Open marketplace | Semantic search, leaderboard, ratings, CLI |
| **Agensi.io** | Curated commercial | 8-point security scan + manual review |
| **SkillsGate** | Open source CLI | 45,000+ indexed, semantic search |
| **SquidBay** | Bitcoin marketplace | Lightning micropayments, 3-tier pricing |
| **Agent 37** (agent37.com) | Web-first | Non-technical user accessible |
| **Shortcut** | Vertical (finance) | 89.1% analyst benchmark, community marketplace |

### Tier 3: Corporate/Vertical
| Player | Vertical | Backing |
|--------|----------|---------|
| **Binance Skills Hub** | Crypto | Binance (462 GitHub stars) |
| **Gate Skills** | Crypto | Gate.io |
| **Heurist** | Crypto/Web3 | Amber Group, ZK-secured |
| **Recall Network** | Decentralized | Multicoin, USV, Coinbase |

### Tier 4: Infrastructure/Tools
| Player | Function |
|--------|----------|
| **openskills** (9,030 stars) | Universal skills loader across all agents |
| **AgentSkillOS** | Skill selection/orchestration framework |
| **SkillFortify** | Formal security analysis (96.95% F1) |
| **SkillScan** | Multi-stage vulnerability detection |
| **Snyk agent-scan** (1,892 stars) | Enterprise security scanner |

---

## TECHNOLOGY LANDSCAPE

### The Emerging Standard Stack

```
+─────────────────────────────────────────────────────+
|  SKILL FORMAT: SKILL.md + YAML frontmatter          |
|  (Works: Claude, Gemini, Cursor, Codex, Kiro, etc.) |
+─────────────────────────────────────────────────────+
           |
+──────────┴──────────────────────────────────────────+
|  DISTRIBUTION: Git-based (npx skills add <url>)     |
|  PROTOCOLS: MCP (97M+ downloads) + A2A              |
+─────────────────────────────────────────────────────+
           |
+──────────┴──────────────────────────────────────────+
|  DISCOVERY: Semantic (embeddings) + FTS5 + RRF      |
|  ORGANIZATION: Capability trees (recursive)          |
|  ORCHESTRATION: DAG-based multi-skill pipelines      |
+─────────────────────────────────────────────────────+
           |
+──────────┴──────────────────────────────────────────+
|  SECURITY: 4-tier trust governance                   |
|  EVAL: Safety, Completeness, Executability,          |
|        Maintainability, Cost-awareness               |
+─────────────────────────────────────────────────────+
           |
+──────────┴──────────────────────────────────────────+
|  INFRA: Cloudflare Workers / Bun / SQLite (D1)      |
|  PAYMENTS: Stripe / Bitcoin Lightning / Crypto       |
+─────────────────────────────────────────────────────+
```

### Skill Lifecycle (from Academic Literature)

```
Discovery -> Practice -> Distillation -> Storage -> Composition -> Evaluation -> Update
    ^                                                                              |
    └──────────────────────────────────────────────────────────────────────────────┘
```

---

## SECURITY: THE DEFINING CHALLENGE

| Metric | Value | Source |
|--------|-------|--------|
| Skills with vulnerabilities | **26.1%** | arXiv: Skills in the Wild (42,447 skills) |
| Malicious skills (ClawHavoc) | **1,200+** | arXiv: SoK, SkillFortify |
| Malicious tools catalogued | **6,487** | arXiv: SkillFortify (MalTool) |
| High-severity (malicious intent) | **5.2%** | arXiv: Skills in the Wild |
| Scripts 2.12x more vulnerable | **OR=2.12, p<0.001** | arXiv: Skills in the Wild |
| Spam/malicious filtered (ClawHub) | **51.4%** | Twitter/X (VoltAgent analysis) |
| Skill duplicates across platforms | **46.3%** | HuggingFace audit |

### Security Solutions Landscape

| Solution | Approach | Results |
|----------|----------|---------|
| **SkillFortify** (formal) | Dolev-Yao model, SAT-based, abstract interpretation | 96.95% F1, 100% precision, 0% FPR |
| **SkillScan** (empirical) | Static analysis + LLM-based semantic classification | 86.7% precision, 82.5% recall |
| **Agensi.io** (commercial) | 8 regex-based checks + planned LLM layer | Score out of 100 |
| **Snyk agent-scan** (enterprise) | 15+ vulnerability classes, background scanning | Enterprise-grade |
| **VirusTotal** (ClawHub) | Malware binary scanning | Misses text-based attacks |

---

## ECONOMIC ANALYSIS

### Market Sizing

| Segment | 2025 | 2030 Projection | CAGR |
|---------|------|-----------------|------|
| AI Agent Market (overall) | ~$7.84B | $52.62B | 46.3% |
| AI Skills TAM | ~$10M | $500M-$1B | 80-100% YoY |
| A2A Protocol Market | Emerging | $2.3B (end 2026) | — |
| Freelance Platform Market | $12-15B | $20-25B (2028) | — |
| Internal Talent Marketplace | $0.95B | $1.5B (2033) | 10.5% |

### Pricing Models in Play

| Model | Example | Status |
|-------|---------|--------|
| **Free/Open Source** | pm-skills, SkillsGate | Dominant (80%+ of skills) |
| **One-time purchase** | Agensi.io | Emerging |
| **Three-tier (Rent/Learn/Own)** | SquidBay | Experimental |
| **Micropayments (per-use)** | Bitcoin Lightning | Novel but Bitcoin barrier |
| **Revenue share (50%)** | LarryBrain | Proven ($3K MRR) |
| **Platform fee (2%)** | SquidBay | Low friction |

### Key Economic Insight
> Commodity skills -> $0 (vibe-coding makes them free). Specialist skills -> 5x premium ($150/hr vs $30/hr). The monetizable zone is **complex, domain-specific, curated, maintained skills** that require real expertise to create and keep current.

---

## RESEARCH GAPS & WHITE SPACES

### Unsolved Problems (Opportunities)

| Gap | Description | Opportunity |
|-----|-------------|-------------|
| **Hybrid human+AI marketplace** | No platform where humans AND AI agents offer services | Convergence of $50B+ freelance + AI skills |
| **Commerce layer for MCP** | Protocol exists (97M+ downloads) but no payments/discovery | "The internet in 1995" |
| **Dynamic pricing engine** | No system prices skills based on quality + demand + reputation | Static pricing leaves money on table |
| **Cross-platform portability** | SKILL.md converging but no universal registry | Fragmentation is current reality |
| **Runtime sandboxing** | All security is pre-deployment; no runtime isolation | Critical for untrusted skills |
| **Skill composition economics** | How to price multi-skill DAG pipelines | Key for composability moat |
| **Enterprise private marketplace** | Almost no internal skill sharing solutions | Every enterprise needs this |
| **Federated trust** | No cross-marketplace reputation portability | Users locked to single platform |

---

## STRATEGIC CONCLUSIONS

### 1. The Market Is Real, Pre-PMF, and Massive
500K+ skills, $52B projected market, Binance/Oracle/Google building platforms. This is not hype — it's infrastructure-level demand. But no winner has emerged.

### 2. Win on Trust, Not Volume
Reddit is clear: users don't want more skills. They want trustworthy skills. Build the trust layer first. SkillFortify's formal approach (96.95% F1) shows what's possible.

### 3. Start Vertical, Expand Horizontal
Binance (crypto), pm-skills (product management), Animation Principles (creative), Shortcut (finance) — vertical-first wins. Own one domain before going broad.

### 4. Composability Is the Technical Moat
AgentSkillOS proves DAG orchestration substantially outperforms flat invocation even with identical skill sets. Build for composition from day one.

### 5. Curated Beats Generated
SkillsBench: curated skills +16.2pp, self-generated +0pp. The marketplace value is curation, not just hosting. Quality gates matter.

### 6. The Hybrid Human+AI Marketplace Doesn't Exist
The biggest white space: a marketplace where human experts and AI agents coexist as service providers. This is the convergence of a $50B+ freelance market and the emerging AI skills economy.

### 7. Security Is the Minimum Viable Trust
26.1% vulnerability rate means any serious marketplace MUST have security scanning. The bar is rising: regex-based (Agensi) -> ML-based (SkillScan) -> formal verification (SkillFortify).

### 8. Non-Technical Users Are the Real Paying Market
Reddit consensus: technical users build their own skills. The paying market is vibe coders, non-technical operators, and enterprise teams who want ready-made, trusted skills.

---

## ACTIONABLE RECOMMENDATIONS

### If Building a Skill Marketplace

1. **SKILL.md format** — Non-negotiable. Support Claude, Gemini, Cursor, Codex, Kiro.
2. **Trust layer first** — 4-tier governance, automated security scanning, locked identities, transaction-based reviews.
3. **Hybrid search** — Semantic embeddings + keyword FTS5 + reciprocal rank fusion.
4. **DAG orchestration** — Design for multi-skill composition, not flat catalogs.
5. **One vertical domain** — Pick PM, DevOps, crypto, data, security. Own it.
6. **Capability trees** — Recursive categorization at scale (AgentSkillOS pattern).
7. **Three-tier pricing** — Rent (per-use) / Learn (skill file) / Own (full package).
8. **Edge-first** — Cloudflare Workers / D1 / Vectorize for global low-latency.
9. **Both A2A and MCP** — Agent interoperability is table stakes.
10. **Target non-technical users** — They'll pay; technical users won't.

### If Investing/Evaluating

1. Trust > supply volume.
2. Vertical-first > horizontal platform.
3. Community engagement > skill count.
4. Security posture > feature list.
5. Watch for hybrid human+AI — largest TAM, doesn't exist yet.

---

## ALL RESEARCH FILES

| Round | Directory | Files | Key Additions |
|-------|-----------|-------|---------------|
| 1 | `/research/skill-marketplaces/` | 3 files | Initial GitHub, Kaggle, arXiv |
| 2 | `/research/skill-marketplaces-2/` | 6 files | All 5 platforms + summary |
| 3 | `/research/skill-marketplaces-3/` | 6 files | Deeper dives, more repos |
| 4 | `/research/skill-marketplaces-4/` | 6 files | Competitive analysis |
| 5 | `/research/skill-marketplaces-5/` | 7 files | Industry overview added |
| 6 | `/research/skill-marketplaces-6/` | 7 files | Emerging trends analysis |
| 7 | `/research/skill-marketplaces-7/` | 7 files | Business landscape |
| 8 | `/research/skill-marketplaces-8/` | 6 files | Web deep dive |
| 9 | `/research/skill-marketplaces-9/` | 7 files | Industry + summary |
| 10 | `/research/skill-marketplaces-10/` | 2 files | GitHub + Kaggle deep research |
| 11 | `/research/skill-marketplaces-11/` | 5 files | This round — fresh searches |
| — | `/research/` (root) | 15+ files | Summaries, competitive, general |

**Total: 80+ research documents, 250+ sources, 11 rounds of investigation.**

---

*The skill marketplace space is early, fragmented, and full of opportunity. The platform that solves trust + composability for a specific vertical will define the next era of AI agent infrastructure.*
