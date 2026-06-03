# Skill Marketplaces: Deep Research Summary — Round 5

> **Date:** March 16, 2026
> **Scope:** GitHub, Twitter/X, Reddit, arXiv, Kaggle, Broad Web
> **Method:** 6 parallel research agents, 25+ searches, 40+ pages scraped, 2,100+ lines of raw findings
> **Building on:** 4 prior research rounds (70+ GitHub repos, 21 arXiv papers, 26+ Twitter signals, 21 Reddit threads, 8 Kaggle datasets)

---

## Executive Summary

The skill marketplace ecosystem is at an **inflection point**. In ~2 months (Jan-Mar 2026), over **350,000 AI agent skills** have been published across three competing marketplaces — a growth rate that took npm a decade. But this explosive growth has exposed deep structural tensions:

1. **The Security Crisis is Real and Urgent.** 26.1% of marketplace skills contain vulnerabilities. The ClawHavoc supply chain attack infiltrated 1,184 malicious skills. The #1 most-downloaded skill on ClawHub was malicious. "Skills are the new code — they just don't look like it."

2. **Curation Beats Volume, Definitively.** Academic research proves curated skills improve agent performance by +16.2pp on average. Domain-specific collections (7,311 stars for PM skills) massively outperform general marketplaces (34 stars for SkillX). Microsoft explicitly warns that loading all skills causes "context rot."

3. **The Monetization Problem Remains Unsolved.** Skills are markdown files — freely copyable. The most viable model according to community consensus is Skill-as-a-Service (hosted execution). Enterprise DevTool companies treat skills as free marketing channels instead.

4. **Two Distinct Markets Have Emerged.** Enterprise (curated catalog → admin approval → RBAC → audit trail) vs. Consumer/Developer (open marketplace → community ratings → self-service). These require fundamentally different architectures.

5. **The Real Target Market is Non-Technical Users.** Technical developers will DIY. "Vibe coders" — the growing population of non-technical builders using AI — are the actual paying customers.

---

## Platform-by-Platform Findings

### GitHub (72+ repos analyzed across 5 rounds)

**The Landscape:**
- **Dominant category:** Claude Code / OpenClaw skill collections (SKILL.md format is de-facto standard)
- **Top repo:** phuryn/pm-skills (7,311 stars, 706 forks) — domain-specific PM skills
- **Enterprise players:** Microsoft (132 skills + governance toolkit with 6,100+ tests), Binance (cross-framework crypto skills), Gate (crypto ecosystem skills)
- **Only 2 of 72+ repos have real marketplace infrastructure** (SkillX and SquidBay). Everything else is a curated Git repository.

**Key Technical Innovations Found:**
| Innovation | Repo | Significance |
|------------|------|-------------|
| Meta-skill (skill that creates skills) | daymade/claude-code-skills | Self-reinforcing marketplace growth |
| Execution runtime (90-99% token savings) | mhattingpete/claude-skills-marketplace | Cost reduction via local execution |
| Skill + Agent composable hierarchy | mhattingpete/claude-skills-marketplace | Two-level composition > flat collections |
| Agent reflection loop (0.0-1.0 scoring) | tiger_cowork | Built-in quality assurance |
| Three-tier pricing (Rent/Learn/Own) | squidbay | IP protection at different levels |
| Agent identity with locked names | squidbay | First reputation system for AI agents |
| DAG-based orchestration | AgentSkillOS | Outperforms flat invocation at 200K scale |
| 611+ cybersecurity skills (MITRE mapped) | mukul975/Anthropic-Cybersecurity-Skills | Vertical specialization proof point |

### Twitter/X (25+ relevant discussions)

**Key Signals:**
- **350K skills in ~2 months** — unprecedented ecosystem growth
- **Security crisis fully visible:** ClawHavoc (1,184 malicious skills), #1 skill was malicious, 12% of audited ClawHub skills malicious
- **Enterprise validation:** Vercel, Supabase, Stripe, Remotion, Microsoft, Coinbase all publishing free official skills
- **Adoption S-curve:** 3% (early 2025) → 12% (March 2026) → projected 30-40% (2027)
- **Crypto/Web3 pushing micropayments:** x402 protocol, Binance/KuCoin/Heurist skill marketplaces

**Sentiment:** ~55% bullish, ~30% cautious/analytical, ~15% skeptical

### Reddit (15+ threads, 100+ comments scraped)

**Key Community Insights:**
- **"Just Ask Claude" is the #1 objection** — countered by: edge case handling requires real-world iteration
- **Context window paradox:** Valuable skills may be too large to fit in context
- **Security scanning is the most praised feature** (Agensi's 8-regex layer)
- **Distribution > Quality Gatekeeping** as the primary marketplace value
- **Preview paradox for paid skills:** Show content = give away the product
- **Skill-as-a-Service is the most viable paid model** (never expose source)
- **Scam/spam flooding is an existential risk** (AI can generate low-quality skills at scale)
- **Enterprise pattern crystallized:** Admin-curated catalog → engineer approval → permission-based sharing → auditable execution

### arXiv (21+ papers across 5 rounds)

**Landmark Findings:**

| Finding | Paper | Impact |
|---------|-------|--------|
| Curated skills improve performance +16.2pp avg | SkillsBench | Validates quality over quantity |
| Self-generated skills provide zero benefit | SkillsBench | Agents can't replace human curation |
| EvoSkill: iterative failure analysis works (+7.3-12.1%) | EvoSkill | Structured self-evolution is the only validated path |
| DAG orchestration >> flat invocation | AgentSkillOS | Composition architecture matters |
| 26.1% vulnerability rate in marketplace skills | Security analysis | Supply chain attacks are systemic |
| 12B-30B model sweet spot for skills | SLM Framework | Skills aren't just for frontier models |
| 7B judge polices 72B agent at 90%+ accuracy | FormalJudge | Formal verification enables weak-to-strong safety |
| Skill transfer = lateral gene transfer | SkillFlow | Skills as "genetic material" across agents |
| Agent labor markets reproduce human macro phenomena | Competitive Games | Economic theory transfers directly |
| SCEMA: 5-dimensional skill evaluation | SkillNet | Safety, Completeness, Executability, Maintainability, cost-Awareness |

**The Curation Paradox:** Curated skills dramatically improve agent performance, yet agents cannot reliably generate high-quality skills themselves. Human expertise remains essential — this is the fundamental value proposition of skill marketplaces.

### Kaggle (30+ datasets, 13+ notebooks)

**Available Data for Building a Skill Marketplace:**
- **LinkedIn Jobs+Skills (1.3M)** — gold standard for skill-job relationships
- **Upwork 60K** — real marketplace pricing and rating data
- **Skills Taxonomy (3,291)** — baseline skill categorization
- **Job-Skill-Set** — purpose-built for ML matching
- **First "agentic" Kaggle competition** — legal information retrieval

**Key Gap:** No datasets exist for AI agent skill quality assessment. This is an untapped research opportunity.

---

## The Five Unsolved Problems

### 1. Security at Scale
- 26.1% vulnerability rate, 5.2% intentionally malicious
- Markdown files aren't treated with code-level suspicion but have equivalent power
- ClawHavoc proved supply chain attacks are practical and profitable
- **Best current approach:** SkillFortify (96.95% F1 with formal verification)

### 2. Monetization
- Skills are text files — freely copyable
- Enterprise DevTool companies give skills away as marketing
- Pay-per-use requires execution control
- **Most viable model:** Skill-as-a-Service (hosted execution, never expose source)
- **Alternative:** Three-tier pricing (Rent/Learn/Own via SquidBay)

### 3. Discovery & Curation
- 350K+ skills but no reliable quality signals
- AI-generated spam flooding is trivially easy
- The "Just Ask Claude" problem undermines perceived value
- **Best current approach:** Hybrid semantic search + human curation + security scanning

### 4. Governance & Trust
- Enterprise requires execution-layer controls (not application-level suggestions)
- No standard credential/identity system for agents
- Audit trails and RBAC are mandatory for regulated industries
- **Best current approach:** Microsoft agent-governance-toolkit (OWASP 10/10)

### 5. Skill Composition & Orchestration
- Flat skill loading is provably suboptimal (AgentSkillOS)
- DAG-based orchestration needs `depends-on:` / `composes-with:` metadata
- Skill Graphs > SKILL.md for expressing relationships
- **Research frontier:** Recursive and conditional composition patterns

---

## Market Map (March 2026)

### AI Agent Skill Marketplaces

| Platform | Skills | Model | Differentiator |
|----------|--------|-------|---------------|
| **SkillsMP** | 351K+ | Open registry | Volume play, largest catalog |
| **Skills.sh** | 84K+ | Open + Snyk scanning | Security scanning, 18 agent compatibility |
| **ClawHub** | 5.7K | Curated | VirusTotal integration, quality focus |
| **SkillShop** | Agent-curated | AI-first discovery | "Tell it what you're building" |
| **Agensi** | Marketplace | 8-layer security | Strongest security scanning |
| **SkillX** | Hybrid search | Platform features | Ratings, leaderboard, CLI |
| **SquidBay** | Bitcoin Lightning | Agent commerce | Rent/Learn/Own pricing, agent identity |
| **Binance Skills Hub** | Crypto-focused | Enterprise | Cross-framework, crypto native |

### Traditional Talent Marketplaces (for context)

| Platform | Model | Scale |
|----------|-------|-------|
| **Upwork** | Commission (20-5%) | $3.8B+ GMV |
| **Fiverr** | Freemium + commission | $1.1B+ revenue |
| **Toptal** | Curated subscription | Enterprise-focused |
| **Gloat** | Internal talent marketplace | AI-powered matching |

---

## The Enterprise Deployment Model (Converged from 4 Sources)

```
1. AUTHOR   → Business expert + engineer co-create skill
2. REVIEW   → Admin/engineer approves (security audit + quality check)
3. PUBLISH  → Skill enters curated company catalog (skill store)
4. DISCOVER → Business users browse approved skills per project
5. EXECUTE  → Agent runs skill in isolated runtime with permission-based access
6. AUDIT    → All actions logged to immutable, non-deletable audit trail
7. PROMOTE  → Successful project skills promoted to org-wide catalog
```

**Critical principle:** "Controls must be underneath, not at application level." — Agent cannot override policy. Isolated runtime where network/filesystem/API access explicitly granted per agent.

---

## Cumulative Research Coverage (All 5 Rounds)

| Platform | R1 | R2 | R3 | R4 | R5 | Total |
|----------|----|----|----|----|-----|-------|
| GitHub repos | 8 | 40+ | 12 | 10+ | 72+ | **80+** |
| ArXiv papers | 5 | 4 | 6 | 6 | 20+ | **21+** |
| Twitter/X signals | 5 | 7 | 8 | 6 | 25+ | **30+** |
| Reddit threads | 5 | 5 | 6 | 5 | 15+ | **25+** |
| Kaggle datasets | 2 | 3 | 5 | 5 | 30+ | **30+** |
| Industry sources | — | 1 | 1 | — | 15+ | **15+** |
| Web scrapes | — | — | — | — | 40+ | **40+** |

### Key Metrics

| Metric | Value | Source |
|--------|-------|--------|
| Total skills published | 400K+ | SkillsMP + Skills.sh + ClawHub |
| Growth rate | 350K in ~2 months | Twitter/BuildMVPFast |
| Vulnerability rate | 26.1% | arXiv security analysis |
| Malicious skill rate | 5.2% | arXiv/ClawHavoc |
| Curated skill performance gain | +16.2pp average | SkillsBench |
| MCP attack success rate | 52.8% | arXiv 2601.17549 |
| DAG vs flat invocation | Substantial improvement | AgentSkillOS (200-200K skills) |
| Self-evolved skill gain | +7.3% to +12.1% | EvoSkill |
| SLM sweet spot | 12B-30B parameters | arXiv 2602.16653 |
| Adoption rate | ~12% of developers | Twitter estimates (March 2026) |
| Agents supporting SKILL.md | 20+ | agentskills.io |
| Microsoft governance tests | 6,100+ | agent-governance-toolkit |
| Cybersecurity skills | 611+ | MITRE ATT&CK mapped |
| Microsoft enterprise skills | 132 | 6 languages |

---

## Strategic Conclusions

### What's Working
1. **SKILL.md as open standard** — adopted by 20+ agents, cross-framework portability is real
2. **Domain specialization** — PM skills (7K+ stars), cybersecurity (611+ skills), protein design, DevOps all proving vertical focus wins
3. **Git-as-distribution** — simple, proven, works. No platform lock-in
4. **Security scanning integration** — VirusTotal, Snyk, formal verification all improving
5. **Enterprise governance tooling** — Microsoft's 6,100+ test governance toolkit sets the bar

### What's Not Working
1. **Volume-first marketplaces** — 350K skills mostly noise, quality signals weak
2. **Monetization** — skills-as-markdown is non-defensible IP
3. **Self-generated skills** — naive approaches provide zero benefit (SkillsBench)
4. **Application-level governance** — agents can override config-based controls
5. **Flat skill invocation** — provably suboptimal vs DAG orchestration

### What's Next
1. **Security will be table stakes** — mandatory scanning, formal verification emerging
2. **Curation layers** will be the real business, not the skills themselves
3. **Skill-as-a-Service** (hosted execution) is the path to sustainable monetization
4. **Enterprise adoption** requires governance-first, not marketplace-first
5. **DAG-based composition** will replace flat skill loading
6. **Vertical specialization** will outperform horizontal platforms
7. **Non-technical users** are the addressable market for paid skills
8. **Agent-to-agent skill commerce** (SquidBay, x402) is the long-term future but early

### What We Should Do (Recommendations from 5 Rounds)

**Immediate:**
1. Map our skills to OWASP Agentic Top 10
2. Add `version:` field to SKILL.md frontmatter (ecosystem converging on semver)
3. Pick a vertical domain and go deep (DevSecOps, observability, or infrastructure)
4. Publish to skills.sh (highest-leverage distribution action, free Snyk scanning)

**Short-term:**
5. Build security scanning into skill validation
6. Document how our skills fit the enterprise deployment model
7. Add `depends-on:` / `composes-with:` metadata for skill composition
8. Build an observability skill (OpenTelemetry — commercial demand proven)

**Medium-term:**
9. Explore Skill-as-a-Service model for premium skills
10. Implement DAG-based skill orchestration (AgentSkillOS approach)
11. Evaluate EvoSkill methodology for automated skill improvement
12. Consider governance-as-a-skill (community demand proven via anthropics/skills#412)

**Do NOT:**
- Don't auto-generate skills naively (zero benefit proven)
- Don't chase volume (context rot, spam flooding)
- Don't ignore MCP security (52.8% attack success rate)
- Don't build application-level governance (execution-layer is the only approach that works)
- Don't build a general-purpose marketplace (domain-specific wins every time)

---

## Files in This Directory

| File | Lines | Content |
|------|-------|---------|
| github.md | ~130 | 72+ repos: Claude Code skills, talent marketplaces, enterprise governance, key patterns |
| twitter.md | ~100 | 25+ discussions: ecosystem growth, security crisis, business models, sentiment analysis |
| reddit.md | ~100 | 15+ threads: community pain points, enterprise deployment, monetization debates |
| arxiv.md | ~160 | 20+ papers: security analysis, skill orchestration, matching algorithms, economic frameworks |
| kaggle.md | ~130 | 30+ datasets: freelance data, job-skill matching, taxonomies, ML approaches |
| industry_overview.md | ~140 | Market overview: traditional vs AI marketplaces, business models, convergence |
| SUMMARY.md | this file | Comprehensive synthesis, conclusions, recommendations |

## Also Available (Agent-Written Detailed Reports)

| File | Lines | Content |
|------|-------|---------|
| ../github_findings.md | 589 | Detailed analysis of 8 repos with architecture deep-dives |
| ../twitter_findings.md | 443 | Full scraped articles, security crisis timeline, market map |
| ../reddit_findings.md | 419 | 7 scraped threads with 100+ comments, pain point analysis |
| ../arxiv_findings.md | 445 | 38 papers catalogued, 14 deeply analyzed, novel algorithms |
| ../kaggle_findings.md | 277 | 30+ datasets, 13 notebooks, ML approach taxonomy |

---

*Generated March 16, 2026 — Round 5 of ongoing skill marketplace research*
