# Knowledge Base: What We've Learned

> **Purpose:** Distilled insights from 200+ sources across 12 research rounds. Read this before making strategic decisions about what to build, how to position, or what matters in the skill marketplace space.
>
> **Sources:** GitHub (72+ repos), arXiv (38+ papers), Reddit (14+ threads), Twitter/X (14+ threads, 9 platforms), Kaggle (20+ datasets), DuckDuckGo/web (85+ articles)
>
> **For raw data:** See per-platform files (`arxiv_findings.md`, `github_findings.md`, etc.) and `SUMMARY_AND_CONCLUSIONS.md`

---

## Table of Contents

1. [The Landscape in One Page](#1-the-landscape-in-one-page)
2. [What Users Actually Want](#2-what-users-actually-want)
3. [Security — The Defining Challenge](#3-security--the-defining-challenge)
4. [Architecture Patterns That Work](#4-architecture-patterns-that-work)
5. [Economics and Pricing](#5-economics-and-pricing)
6. [The Academic Foundations](#6-the-academic-foundations)
7. [Competitive Intelligence](#7-competitive-intelligence)
8. [What Makes This Marketplace Different](#8-what-makes-this-marketplace-different)
9. [Open Questions](#9-open-questions)

---

## 1. The Landscape in One Page

**What "skill marketplace" means in 2025-2026:**

| Domain | Examples | Maturity |
|--------|----------|----------|
| AI Agent Skills | SKILL.md files for Claude Code, Cursor, Gemini, Codex, Kiro | Early (< 1 year) |
| Human Talent/Freelance | Upwork, Fiverr, Freelancer.com, Mercor | Mature (15+ years) |
| Hybrid AI+Human | Does not exist yet | **White space** |

**Scale:**
- 500,000+ published skills across 12+ marketplaces (SkillsMP alone claims 500K+)
- 45,000+ indexed with semantic search (SkillsGate)
- 200,000+ in academic repositories (SkillNet, arXiv 2603.04448)
- 15+ competing platforms, none with dominant market share
- $7.5-8.3B market in 2025, projected $47-53B by 2030 (41-46% CAGR)
- 67% of Fortune 500 have production agentic AI deployments

**Three facts every agent should know:**
1. **Nobody has won yet.** 15+ platforms competing, all pre-product-market-fit. The window is open.
2. **Trust is the product, not skills.** Every source converges on this. The hard problem is verification, not creation.
3. **SKILL.md is the standard.** YAML frontmatter + Markdown prompt body. Adopted by Anthropic, OpenAI, Microsoft, Cursor, Windsurf, 38+ agents. Non-negotiable.

---

## 2. What Users Actually Want

Synthesized from Reddit (14 threads), Twitter/X (14 threads), and Kaggle user data.

### What they ask for

1. **Pre-approval vetting.** Not post-hoc moderation — vet before publishing. (Reddit consensus)
2. **Transparent trust metrics.** Success rate, total runs, last-updated date, security scan results. (Reddit, Twitter)
3. **Locked names.** Prevent reputation gaming through name squatting. (Reddit)
4. **Transaction-based reviews.** Only buyers/users can review. Eliminates fake reviews. (Reddit)
5. **Skill versioning and decay detection.** Skills rot as APIs and models change. Users want to know if a skill still works. (Reddit, arXiv: SkillNet)
6. **Narrow, domain-specific skills.** "Narrow workflows > general service" is the strongest Reddit signal. Binance (crypto), Shortcut (finance), Browser Use (web automation) prove this.
7. **Composability.** Users want to chain skills into workflows, not pick from flat catalogs. (arXiv, GitHub, Reddit)

### What they complain about

1. **"Too many options, no curation."** Discovery is the bottleneck. (Reddit)
2. **"Grifters will flood it."** Supply-chain attacks are expected. (Reddit, confirmed by arXiv)
3. **"Vibe-coding makes everything free."** Price pressure is relentless on commodity skills. (Reddit)
4. **High platform fees.** Upwork's 20%→5% sliding scale is universally hated. (Reddit, Kaggle)
5. **Broken discovery.** Browse/search dominates when instant matching would be better. (Reddit)

### The skeptic's argument (and why it's partially right)

Reddit skeptics say: "AIs already know everything — why would I pay for a skill file?"

**Where they're right:** Commodity skills (basic search, simple automation) will trend to $0. Vibe-coding competes with any skill at the commodity level.

**Where they're wrong:** Production reliability, maintenance, security vetting, and trust have real value. The SaaS analogy applies: "SaaS didn't succeed because software was impossible to write — it succeeded because using a maintained, reliable service was easier than owning the complexity." (Reddit user, top-voted)

---

## 3. Security — The Defining Challenge

This is the most researched topic across all sources. The numbers are alarming.

### The hard numbers

| Metric | Value | Source |
|--------|-------|--------|
| Community skills with vulnerabilities | 26.1% | arXiv: Agent Skills survey |
| Skills with flaws (Snyk audit of 3,984) | 36.82% | FINAL_SUMMARY |
| Malicious skills in ClawHavoc attack | ~1,200 | arXiv: SoK |
| Malicious tools detected (MalTool study) | 6,487 | arXiv |
| Attack success rate on frontier models | 80% | arXiv |
| Skills filtered as spam/malicious (ClawHub) | 51.4% | Twitter/X (VoltAgent) |
| Memory poisoning survives uninstallation | Yes | arXiv |
| Cost per missed bad actor (Mercor data) | $600 | Kaggle |

### What the attacks look like

1. **Supply-chain infiltration.** ClawHavoc: 1,200 malicious skills published to a major marketplace, exfiltrating API keys, crypto wallets, and browser credentials. (arXiv: SoK)
2. **Prompt injection via skills.** Malicious instructions embedded in skill files that hijack agent behavior. (arXiv: Prompt Injection via Agent Skills)
3. **Tool name manipulation.** ToolTweak: adversarial naming boosts selection rate from 20% to 81%. (arXiv: ToolTweak)
4. **Memory poisoning.** Malicious skills write persistent data that survives uninstallation and affects future sessions. (arXiv)

### The defense architecture (from literature)

**Four-Tier Governance Model** (arXiv: Agent Skills survey):

| Tier | Provenance | Permissions |
|------|-----------|------------|
| Tier 1 | Official/verified | Full access |
| Tier 2 | Community-reviewed | Standard access |
| Tier 3 | Community-contributed | Sandboxed |
| Tier 4 | Unverified | Read-only, no execution |

**What works in practice:**
- Static analysis (regex-based checks for dangerous commands, secret detection, env harvesting)
- VirusTotal integration (ClawHub)
- 8-point security scan + manual review (Agensi.io)
- Sandboxed execution for untrusted skills
- `allowed-tools` restriction to minimum needed (what this marketplace already does)

---

## 4. Architecture Patterns That Work

### The emerging technology stack

| Layer | Standard/Pattern | Adoption |
|-------|-----------------|----------|
| Skill Format | SKILL.md with YAML frontmatter | De facto standard |
| Registry | `marketplace.json` manifest | Common pattern |
| Distribution | Git-based (`npx skills add <repo>`) | Dominant |
| Discovery | Semantic search (embeddings) + FTS5 + RRF | Best practice (SkillX) |
| Organization | Capability trees (recursive categorization) | Academic best (AgentSkillOS) |
| Orchestration | DAG-based multi-skill pipelines | Outperforms flat invocation |
| Protocols | A2A (Agent-to-Agent) + MCP (Model Context Protocol) | Converging standards |
| Frontend | React + Tailwind, dark themes | Common |
| Backend | Cloudflare Workers / Node.js / Bun | Edge-first emerging |
| Database | SQLite (D1, sql.js) | Dominant for small-medium |

### The five architectural layers

From `FINAL_SUMMARY.md` — "No single project covers all 5. The first to integrate them wins."

```
1. Discovery    — How agents find skills (search, recommendation, capability trees)
2. Trust        — How skills are verified (scanning, tiers, reputation, attestation)
3. Payments     — How value flows (micropayments, subscriptions, open-source)
4. Orchestration — How skills compose (DAG pipelines, chaining, error recovery)
5. Governance   — How the ecosystem evolves (deprecation, disputes, standards)
```

### Reference architecture (from Agent Exchange paper)

```
User-Side Platform (USP)  ←→  Agent-Side Platform (ASP)
  Goal → Tasks                  Capabilities + Performance
        ↓                              ↓
  Agent Hubs                    Data Management Platform (DMP)
  Team coordination             Knowledge sharing
  Auction matching              Fair value attribution
```

Inspired by Real-Time Bidding (RTB) in advertising. Key insight: agents need structured auction mechanisms for efficient market matching, not just API calls.

### Skill lifecycle (from SoK paper)

```
Discovery → Practice → Distillation → Storage → Composition → Evaluation → Update
    ↑                                                                         |
    └─────────────────────────────────────────────────────────────────────────┘
```

Skills are not static artifacts. They have a lifecycle that requires active management. SkillNet's evaluation framework (SCEMC: Safety, Completeness, Executability, Maintainability, Cost) is the most rigorous published approach.

---

## 5. Economics and Pricing

### Pricing models observed in the wild

| Model | Example | Verdict |
|-------|---------|---------|
| Free/open-source | pm-skills, SkillsGate | Maximum adoption, no quality gate, no revenue |
| One-time purchase | Agensi.io | Simple but no recurring revenue |
| Three-tier (Rent/Learn/Own) | SquidBay | Flexible but complex UX |
| Commission (20%→5%) | Upwork | Proven at scale, universally hated |
| Micropayments (per-use) | SquidBay (Bitcoin Lightning, 2% fee) | Pay-for-value, Bitcoin adoption barrier |
| Freemium + premium | LarryBrain ($3K MRR, 50% rev share) | Working in practice |

### Key economic insights

1. **Complementarity determines value.** A skill's price depends on what it combines with, not individual quality. (arXiv: Stephany 2022, 121 citations)
2. **Specialization premium is 5x.** $150/hr (A/B Testing) vs. $30/hr (Data Processing) on Upwork. (Kaggle: 1.3M contracts)
3. **Exploration prevents stagnation.** Without epsilon-greedy exploration, cost savings drop from 20.3% to 1.9%. (arXiv: COALESCE)
4. **Monopolization risk is real.** Dominant agents can quickly corner markets through strategic self-improvement. (arXiv: Strategic Self-Improvement)
5. **Fixed-price dominates.** Clients prefer fixed-price over hourly. (Kaggle: Upwork data)
6. **Commodity skills trend to $0.** Only specialist and trust-verified skills sustain pricing.

---

## 6. The Academic Foundations

### Papers every agent should know about

| Paper | Key Contribution | Why It Matters |
|-------|-----------------|----------------|
| **SkillNet** (2603.04448) | 200K+ skills, SCEMC evaluation framework | Gold standard for skill quality measurement |
| **SoK: Agentic Skills** (2602.20867) | Full skill lifecycle, 7 design patterns, ClawHavoc case study | Most comprehensive security analysis |
| **Agent Exchange (AEX)** (2507.03904) | Auction-based marketplace architecture (USP/ASP/Hub/DMP) | Reference architecture for any marketplace |
| **COALESCE** (2502.10148) | Outsourcing with 41.8% task completion, 20.3% cost savings | Proof that agent marketplaces work economically |
| **Agent Skills Survey** (2602.12430) | 26.1% vulnerability rate, 4-tier governance, 7 open challenges | The definitive security survey |
| **Beyond the Sum** (2501.10388) | 4 infrastructure gaps for agent market participation | Infrastructure requirements roadmap |
| **Strategic Self-Improvement** (2512.04988) | Monopolization risk, systemic price deflation | Warning about market concentration |
| **SkillFlow** (lateral skill transfer) | P2P skill transfer between agents | Alternative to centralized distribution |
| **AgentSkillOS** | Capability trees, tree-based retrieval at 200K scale | Discovery architecture at scale |

### Research themes that recur

1. **Trust > Everything.** Every paper that touches marketplace design identifies trust/security as the binding constraint.
2. **Composability is under-studied.** Many papers mention it, few formalize it. DAG orchestration is assumed but not benchmarked.
3. **Hybrid human+AI is the white space.** No paper fully addresses a marketplace where both humans and AI offer skills.
4. **Fairness is neglected.** Tool selection bias (ToolTweak, BiasBusters) and marketplace fairness (hiring bias, team formation) are studied but not integrated into marketplace design.
5. **Evaluation is multi-dimensional.** Single-metric quality scores are insufficient. SCEMC (5 dimensions) or similar frameworks are necessary.

---

## 7. Competitive Intelligence

### Who's doing what (March 2026)

**Dominant by volume:** SkillsMP (500K+ skills), SkillsGate (45K+ indexed, security scanning)

**Dominant by influence:** phuryn/pm-skills (7.3K stars, domain-specific PM skills), VoltAgent (awesome lists with 11K+ stars)

**Most innovative:**
- **SquidBay** — Bitcoin Lightning micropayments, 3-tier pricing (Rent/Learn/Own), 2% platform fee, agent-to-agent commerce. The most complete economic system found.
- **SkillX** — Hybrid search (bge-base-en-v1.5 embeddings + SQLite FTS5 + reciprocal rank fusion), leaderboard, ratings. The most architecturally sophisticated open marketplace.
- **Shortcut** — Vertical (finance/Excel), beats analysts 89.1%, community marketplace. Proof that narrow verticals work.

**Enterprise entrants:** Block (Goose), Microsoft, HashiCorp, AWS Labs, Binance, Oracle, Salesforce

**Official platforms:** Anthropic (`anthropics/skills`, 94K+ stars — verified March 2026), OpenAI (`openai/skills` + agents/openai.yaml)

**What's missing from all of them:**
1. No hybrid human+AI marketplace
2. No dynamic pricing engine (price based on quality + demand + reputation simultaneously)
3. No universal cross-platform registry
4. No ride-sharing-like instant matching
5. No privacy-preserving skill evaluation
6. No enterprise internal skill marketplace (open-source)

### Our differentiators (from deep-research/README.md)

| What We Do | Nobody Else Does |
|------------|-----------------|
| Dual content types (skills + rules) | Most have only skills or only rules |
| Cross-platform install with idempotency | Most target one platform |
| 104 automated tests | Most have zero tests |
| PEP 723 zero-install Python scripts | Most require pip install |
| Research-backed decision making | Most build without market research |

### Where the ecosystem passed us

| Gap | What Others Have |
|-----|-----------------|
| Scale | SkillsMP: 500K+, SkillsGate: 45K+. We have ~15 skills. |
| Security scanning | ClawHub: VirusTotal. Agensi: 8-point scan. We have static tests only. |
| Web discovery | SkillX: semantic search. We have a README table. |
| openai.yaml support | OpenAI Codex uses it for UI metadata, icons, MCP deps. We don't support it. |
| Auto-indexing | SkillsGate indexes GitHub repos. We require manual catalog updates. |

---

## 8. What Makes This Marketplace Different

From the research, our strategic position is:

1. **Quality over quantity.** In a market where 26.1% of skills are vulnerable and 51.4% are spam, curated quality is the differentiator. Our 104-test safety net is unusual.

2. **Dual types.** Skills (on-demand capabilities) + Rules (always-on behavioral guidelines) is a unique combination. Rules are the harder problem — they shape agent behavior, not just add capabilities.

3. **Cross-platform.** Supporting Devin, Claude Code, Cursor, and Windsurf from a single source. Most marketplaces target one platform.

4. **Research-informed.** This knowledge base exists. Most competitors are building without systematic market intelligence.

5. **Portable format.** SKILL.md + PEP 723 means zero vendor lock-in. Skills work anywhere that reads Markdown and runs Python.

---

## 9. Open Questions

Things we've researched but don't have answers to yet:

1. **Can AI skills be monetized?** Reddit is split. The SaaS analogy suggests yes, but commodity pressure is real. The answer likely depends on the vertical and trust tier.

2. **Centralized vs. P2P distribution?** Centralized quality gates build trust (arXiv), but P2P lateral transfer is more resilient (SkillFlow). Probably both, in different layers.

3. **How to price composed skill pipelines?** No framework exists for attributing value when multiple skills chain together. (Research gap identified in SUMMARY_AND_CONCLUSIONS.md)

4. **Will SKILL.md evolve?** The format lacks versioning (semver + lockfiles), progressive disclosure (OpenAI's openai.yaml), and formal security metadata. These are likely needed at scale.

5. **Is the hybrid human+AI marketplace viable?** The biggest white space. $50B+ freelance market meets emerging AI skills economy. Nobody has tried it.

6. **How do you govern at scale?** Evolving policies, dispute resolution, skill deprecation, platform evolution — no marketplace has addressed long-term governance. (Research gap)
