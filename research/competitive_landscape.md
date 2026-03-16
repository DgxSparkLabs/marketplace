# Skill Marketplace Competitive Landscape Research

> **Research Date:** December 2025 – March 2026
> **Sources:** 20+ articles, reports, and primary sources scraped via DuckDuckGo + web scraping
> **Scope:** AI agent skill marketplaces, MCP ecosystem, talent marketplaces, funding landscape

---

## Table of Contents

1. [Market Overview & Sizing](#1-market-overview--sizing)
2. [Key Players & Their Models](#2-key-players--their-models)
3. [Funding Landscape](#3-funding-landscape)
4. [Technology Trends](#4-technology-trends)
5. [What's Working vs. What's Failing](#5-whats-working-vs-whats-failing)
6. [Market Gaps & White Spaces](#6-market-gaps--white-spaces)
7. [Strategic Recommendations](#7-strategic-recommendations)

---

## 1. Market Overview & Sizing

### The AI Agent Market Is Exploding

The skill/agent marketplace space sits at the intersection of two massive trends: **AI agent proliferation** and **the standardization of agent-tool connectivity via MCP**.

| Metric | Value | Source |
|--------|-------|--------|
| AI Agents market (2025) | **$7.84B** | Grand View Research / MindStudio |
| AI Agents market (2030 projected) | **$52.62B** (46.3% CAGR) | MarketsandMarkets |
| AI Agents market (2033 projected) | **$182.97B** (49.6% CAGR) | Grand View Research |
| Enterprise AI agent adoption | **62% experimenting**, 23% scaling | McKinsey 2025 Survey |
| Organizations using AI (any function) | **88%** | McKinsey 2025 |
| Vertical AI agents growth rate | **62.7% CAGR** through 2030 | MarketsandMarkets |
| Corporate AI agents (2024→2025) | **$5B → $13B** | Various |
| Enterprise apps embedding agents by 2026 | **40%** (up from <5% in 2025) | Industry estimates |

### The MCP Ecosystem — The "USB-C for AI"

The Model Context Protocol (MCP) has become the dominant standard in record time:

| MCP Metric | Nov 2024 | May 2025 | Dec 2025 |
|------------|----------|----------|----------|
| MCP Servers | ~100 | 4,000+ | **5,800+** |
| MCP Clients | ~10 | ~150 | **300+** |
| Monthly SDK Downloads | ~100K | 8M+ | **97M+** |
| Published MCP Servers | N/A | N/A | **10,000+** |

- **MCP ecosystem projected market**: $1.2B (2022) → $4.5B (2025)
- **Governance**: Donated to Linux Foundation's Agentic AI Foundation (Dec 2025)
- **Backing**: Anthropic, OpenAI, Google, Microsoft, AWS, Cloudflare, Bloomberg
- MCP achieved industry-standard status in ~15 months — faster than TCP/IP, REST, or USB-C

### The Agent Skills Marketplace — A New Category

The "agent skills" marketplace is an emerging sub-category focused on distributing **procedural knowledge** (SKILL.md files, prompt patterns, workflow definitions) for AI coding agents:

| Platform | Skills Indexed | Launch | Model |
|----------|---------------|--------|-------|
| Skills.sh (Vercel) | 35,000+ community submissions | Jan 2026 | Free, open-source |
| SkillsGate | 60,000+ | Late 2025 | Open-source, freemium |
| SkillsMP | 500,000+ | 2025 | Open directory |
| Skillgate.app | 222+ curated packs | 2025 | Freemium ($19/mo unlimited) |
| Agensi.io | Growing catalog | 2025 | Buy-once, own-forever |

### Internal Talent Marketplaces (Adjacent Space)

The internal talent/skills marketplace space for HR is a mature adjacent market:

- **By 2030**: 85 million jobs may go unfilled due to skill shortages (McKinsey)
- **94%** of employees would stay longer if companies invested in career development (LinkedIn 2024)
- **60%** of large enterprises expected to implement AI-powered skills marketplaces by 2025 (Gartner)
- Companies with strong internal mobility see **2x employee retention** (LinkedIn)
- Key players: **Gloat, Fuel50, Workday, Eightfold AI, SAP SuccessFactors, Phenom**

---

## 2. Key Players & Their Models

### Tier 1: Enterprise AI Agent Marketplaces

#### Oracle AI Agent Marketplace
- **Model**: Embedded natively in Oracle AI Agent Studio for Fusion Applications customers
- **Approach**: Partner-built agent templates (Infosys, IBM, KPMG, Box, Stripe, RChilli)
- **Cost**: Custom AI subscription fee; no additional partner charge for templates
- **Moat**: 21-point enterprise readiness checklist; Oracle provides support even for partner templates
- **Key insight**: Enterprise-grade, embedded in existing workflow — not standalone

#### Google Cloud AI Agent Marketplace
- **Model**: Part of Google Cloud Marketplace
- **Approach**: Agent builders get global reach, channel sales, co-selling with Google Cloud
- **Launched**: October 2025

#### Salesforce Agentforce
- **Model**: Integrated into Salesforce ecosystem
- **Approach**: Pre-built agents + partner ecosystem

### Tier 2: AI Agent Marketplaces (Standalone)

#### Enso (NFX Portfolio)
- **Model**: "Vertical AI Agents marketplace for SMBs"
- **Pricing**: $49/month — fraction of alternatives
- **Approach**: 300+ micro-agents (LinkedIn writers, SEO experts, Instagram designers, lead finders)
- **Key features**: Persistent memory, learns over time
- **Target**: SMBs ($750B in IT spending, chronically underserved)
- **Backed by**: NFX (marquee VC in marketplace building)

#### MindStudio
- **Model**: No-code agent builder with built-in app marketplace
- **Revenue models supported**: Subscription, usage-based, outcome-based, enterprise licensing
- **Key features**: 200+ AI models, model routing, block-based interface, multiple deployment options
- **Agent economics**: Lead qualification agents ($500-2,000 setup + $200-500/mo); Support agents ($0.50-2.00/ticket); Enterprise licensing ($10K-500K/yr)

### Tier 3: AI Agent Skills Marketplaces (Developer-Focused)

#### Skills.sh (Vercel)
- **What it is**: Open directory & leaderboard for AI agent skills ("npm for agent behaviors")
- **Launched**: January 2026 by Vercel
- **Format**: SKILL.md files — Markdown + optional scripts
- **Installation**: `npx skills add <owner/repo>` — one command, auto-detects agent
- **Agent support**: Claude Code, Cursor, GitHub Copilot, Aider, OpenCode, Codex CLI, 30+ agents
- **Scale**: 35,000+ community submissions
- **Revenue model**: **None** — free forever, GitHub-based
- **Quality problem**: "80% of skills are AI slop" (@pablocubico); no curation, no verification badges, no ratings
- **Privacy concerns**: No published privacy policy or ToS
- **Strength**: One-command install, agent-agnostic, Vercel brand recognition
- **Weakness**: No quality control, no monetization, no enterprise features (audit, SSO)

#### SkillsGate
- **What it is**: Open marketplace for AI agent skills with semantic search
- **Scale**: 60,000+ skills indexed, 17 agents supported
- **Key differentiators vs Skills.sh**:
  - AI-powered semantic search (intent-based, not just keywords)
  - Security scanning via your own AI agent (crowd-sourced scan results)
  - Verified publishers with trust tiers (Verified, Established, New)
  - MCP server integration for direct agent access
- **Installation**: `npx skillsgate install <skill-name>` or via MCP
- **Revenue model**: Free for search/install; potential premium features unclear
- **Origin**: Solo developer project, launched on Reddit/HN (45K skills indexed)
- **Community reception**: Positive ("semantic search angle solves a real pain point")
- **Open questions**: Versioning, skill decay, community curation at scale

#### Agensi.io
- **What it is**: "Buy once, own forever" marketplace for AI agent skills
- **Model**: **One-time purchase** — install instantly, own forever
- **Format**: Built on open SKILL.md standard
- **Agent support**: Claude Code, Codex CLI, Cursor, 20+ agents
- **Traction**: Hit 100 users, first paid skill listed (as of Reddit post ~Jan 2026)
- **Listed on Crunchbase**: Private, 1-10 employees
- **Key differentiator**: Paid marketplace model (vs. free directories)
- **Strength**: Clear monetization path for skill creators
- **Weakness**: Very early stage, tiny scale

#### Skillgate.app (different from SkillsGate)
- **What it is**: Production-ready, security-vetted AI agent skill packs
- **Scale**: 222+ skill packs
- **Pricing**: 35 free packs; Unlimited at $19/month
- **Key differentiator**: Quality-first approach — sandboxed evaluation, benchmark testing, reviewed for security
- **Categories**: Security Auditors, Sprint Planners, Growth Scouts, Data Agents, Support Co-Pilots, Release Commanders
- **Claim**: "Skills built by AI" — generated and refined by autonomous agent teams

#### SkillsMP (skillsmp.com)
- **Scale**: 500,000+ agent skills
- **Format**: SKILL.md open standard
- **Agent support**: Claude Code, Codex CLI, ChatGPT
- **Focus**: Volume with daily automated updates

### Tier 4: MCP Infrastructure & Discovery

#### MCP Registries/Directories

| Registry | Servers Listed | Focus |
|----------|---------------|-------|
| Official MCP Registry | Curated, verified | Official standard |
| PulseMCP | 5,500+ | Discovery platform |
| Glama | 5,800+ | Catalog |
| Smithery | Growing | Early discovery, South Park Commons backed |
| MCPez.com | 11,790+ | Comprehensive directory |
| Docker Desktop MCP Catalog | 113+ | Containerized servers |

#### MCP Marketplace (mcpmarketplace.com)
- Revenue model: **85/15 rev-share** for server authors
- Status: Has revenue model but not scale
- Only platform with live payment infrastructure for MCP server authors alongside Apify

### Tier 5: Internal Talent Marketplaces (Enterprise HR)

| Platform | Focus | Notable |
|----------|-------|---------|
| **Gloat** | Internal mobility | AI-powered, breaks organizational silos |
| **Fuel50** | Career ecosystems | AI-driven marketplace, smart-matching algorithms |
| **Workday** | Workforce management | Skills Cloud, comprehensive suite |
| **Eightfold AI** | Talent intelligence | Deep skills ontology |
| **SAP SuccessFactors** | Enterprise HR | Partner: TalenTeam |
| **Phenom** | Talent experience | Internal + external marketplace |

---

## 3. Funding Landscape

### Agentic AI Funding Summary (2022-2025)

| Year | Deals | Total Raised | Avg Deal Size | Key Insight |
|------|-------|-------------|---------------|-------------|
| 2022 | 6 | **$648M** | $108M | Market barely existed; Uniphore $400M = 62% |
| 2023 | 26 | **$1,001M** | $39M | Post-ChatGPT wave; Adept AI $350M, Imbue $212M |
| 2024 | 54 | **$2,018M** | $37M | Peak year; 9x deal volume from 2022 |
| 2025 | 15 | **$767M** | $51M | Infrastructure focus; deal sizes trending up |
| **Total** | **101** | **$4.4B** | **$44M** | |

### Largest Funding Rounds in Agentic AI

| Company | Amount | Year | Round | Valuation |
|---------|--------|------|-------|-----------|
| Uniphore | $400M | 2022 | Series E | - |
| Adept AI | $350M+| 2023 | Series B | $1B |
| H Company | $220M | 2024 | Seed (!!) | - |
| Imbue | $212M | 2023 | Series B | $1B+ |
| Cognition AI (Devin) | $175M | 2024 | Series A ext. | $2B |
| Sierra AI | $175M | 2024 | Growth | $4.5B |
| AppZen | $180M | 2025 | Growth | - |
| Kore.ai | $150M | 2024 | Series D | - |
| LangChain | $125M | 2025 | Series B | $1.25B |
| Parloa | $120M | 2025 | Series C | $1B |

### Top AI Agent Startups by Valuation (2025-2026)

| Company | Valuation | Focus |
|---------|-----------|-------|
| Cursor (Anysphere) | **$29B** | AI coding |
| Sierra AI | **$10B** | Customer service agents |
| Glean | **$7.2B** | Enterprise search/agents |
| Harvey | **$5B** | Legal AI agents |
| Cognition AI (Devin) | **$2B** | Autonomous software engineering |
| Imbue | **$1B+** | Reasoning AI agents |

### Most Active Investors in Agentic AI

| Investor | Deals | Notable Bets |
|----------|-------|-------------|
| General Catalyst | 7 | Adept AI, Parloa, Hippocratic AI |
| Sequoia Capital | 7 | Harvey AI, Sierra AI, Factory, Dust |
| Y Combinator | 7 | Darrow, Artisan AI, Retell AI, Bland AI |
| SV Angel | 6 | Adept AI, Harvey AI, 11x.ai |
| NVIDIA / NVentures | 5 | Adept AI, Imbue, Kore.ai (~$779M aggregate) |
| Benchmark | 5 | LangChain, Sierra AI, Manus AI |
| Accel | 5 | H Company, Decagon, Ema |
| Insight Partners | 5 | CrewAI, Wonderful, Tavily |

### MCP-Specific Infrastructure Funding

| Company | Amount | Investor | Focus |
|---------|--------|----------|-------|
| Manufact | $6.3M seed | Peak XV (ex-Sequoia India), YC | MCP SDK/tooling ("Stripe for tool calls") |
| StackOne | $20M Series A | GV (Google Ventures) | MCP security |
| Lakera | $20M Series A | 2024 | Prompt injection defense |
| Temporal | $300M Series D | a16z | AI agent infrastructure |

### Funding Category Breakdown (2022-2025)

| Category | Deals | Total Funding | % of Total |
|----------|-------|--------------|------------|
| Customer Support & CX Agents | 19 | **~$1,628M** | 37% |
| Enterprise Automation & Workflow | 15 | **~$1,301M** | 29% |
| AI Coding & Software Engineering | 11 | **~$487M** | 11% |
| Agent Infrastructure & Platforms | 18 | **~$396M** | 9% |
| Other (legal, sales, vertical) | 38 | **~$588M** | 14% |

### Five Unicorns Minted (2022-2025)
1. **Adept AI** — $1B
2. **Imbue** — $1B+
3. **Sierra AI** — $4.5B → $10B
4. **Cresta** — $1B+
5. **LangChain** — $1.25B

---

## 4. Technology Trends

### 4.1 MCP as Universal Standard
- **Protocol war is over**: MCP won. All major model providers (Anthropic, OpenAI, Google, Microsoft) + cloud providers (AWS, Azure, Cloudflare) support it
- **Linux Foundation governance** ensures vendor neutrality
- **97M+ monthly SDK downloads** — faster adoption than almost any infrastructure standard in history
- JSON-RPC 2.0 based, exposing Tools + Resources + Prompts as primitives

### 4.2 SKILL.md as Emerging Standard for Agent Skills
- Markdown-based format for packaging procedural knowledge
- Adopted by Skills.sh (Vercel), SkillsGate, Agensi, SkillsMP
- Agent-agnostic: works with Claude Code, Cursor, Copilot, Codex CLI, Aider, 30+ agents
- Think "npm for agent behaviors" — but still very early

### 4.3 Agent-as-a-Service Economics
- Shifting from "selling software access" to "selling completed work"
- AI SDR costs ~$1,000/month vs. human SDR at $100K/year
- Invoice processing: manual = $13/invoice, AI agent = pennies
- **Outcome-based pricing** gaining traction (e.g., Paid raised $32.5M for pay-per-outcome billing)

### 4.4 Multi-Agent Systems
- Moving from single-purpose agents to **orchestrated multi-agent workflows**
- Companies like LangChain, Sema4.ai, Relevance AI emphasizing multi-agent coordination
- Google's A2A protocol for agent-to-agent communication (complementary to MCP)

### 4.5 Enterprise AI Agent Adoption Pattern
1. **Start with customer support** (measurable ROI within weeks)
2. **Expand to finance/back-office** (AppZen, invoice processing)
3. **Layer in coding/dev agents** (Cursor, Devin, Claude Code)
4. **Build multi-agent orchestration** across departments

### 4.6 Skills Disruption
- **39% of workers' core skills** expected to change by 2030 (WEF Future of Jobs 2025)
- **50% of workforce** has completed training as part of long-term learning strategies (up from 41%)
- Top growing skills: ML/AI, Python, Cloud (AWS/Azure), Prompt Engineering, Cybersecurity
- Declining skills: Manual testing, data entry, legacy web tech, cold calling

---

## 5. What's Working vs. What's Failing

### What's Working

| Pattern | Evidence | Why It Works |
|---------|----------|-------------|
| **Vertical agents for specific industries** | Sierra AI ($10B), Harvey ($5B), Parloa ($1B) | Clear ROI, domain expertise creates moat |
| **SMB-focused agent marketplaces** | Enso (300+ agents, $49/mo), NFX thesis | SMBs have everything to gain, low switching costs |
| **Infrastructure plays** | LangChain ($1.25B), Temporal ($300M), Cloudflare MCP hosting | Picks-and-shovels strategy during gold rush |
| **Enterprise-embedded marketplaces** | Oracle AI Agent Marketplace, Salesforce Agentforce | Built into existing workflows, zero adoption friction |
| **Free/open-source for adoption** | Skills.sh (35K submissions), SkillsGate (60K), MCP (97M downloads) | Fastest path to ecosystem lock-in |
| **Customer support agents** | $1.6B in funding (37% of all agentic AI VC) | Measurable ROI, high volume, proven technology |
| **One-command installation** | Skills.sh, SkillsGate | Developer experience matters enormously |
| **Agent-agnostic design** | SKILL.md standard, MCP protocol | Avoids vendor lock-in, broader adoption |

### What's Failing

| Pattern | Evidence | Why It Fails |
|---------|----------|-------------|
| **Quality-free open directories** | "80% of skills are AI slop" (Skills.sh) | No curation = noise > signal |
| **General-purpose horizontal agents** | Only Manus AI ($75M) got large funding for horizontal | Hard to differentiate, race to bottom |
| **Standalone MCP hosting startups** | Cloudflare, Vercel, Docker all launched competing hosting | Cloud giants bundle hosting; hard to compete |
| **Free without monetization** | Manufact has 5M+ SDK downloads, zero revenue | Open-source paradox: adoption ≠ revenue |
| **Pure catalog/directory play** | Smithery, PulseMCP — scale but no revenue model | Discovery without trust/economics is a feature, not a business |
| **Individual agent marketing** | Per NFX: marketing cost per standalone agent never justifies it | Marketplace aggregation is required |
| **Incumbent labor marketplaces adapting** | Upwork, Fiverr conflicted on AI agents replacing their supply side | Risk undermining existing revenue |
| **Agent skills without versioning** | Community concern on SkillsGate, Skills.sh | Skills built for old agent versions break silently |

---

## 6. Market Gaps & White Spaces

### Gap 1: Enterprise MCP Gateway / Governance Layer (HIGHEST OPPORTUNITY)
> *"The first company to ship a production-grade MCP security gateway will find a market of enterprises that cannot proceed without it."* — Primitives AI

- **What's missing**: Control plane between enterprise AI systems and MCP servers
- **Features needed**: Policy enforcement, compliance-grade audit trails, approval workflows, SOC2/GDPR/HIPAA reporting
- **Target**: Regulated industries (financial services, healthcare, legal)
- **Revenue model**: Per-agent-action pricing + enterprise subscription
- **Analogy**: "Okta for agent tool calls"
- **Competition**: None purpose-built yet; Lakera and StackOne address prompt injection broadly

### Gap 2: Curated MCP/Skills Marketplace with Trust Infrastructure
- **What's missing**: The "App Store" for MCP servers — combining quality curation, security scanning, compatibility testing, support SLAs, and monetization
- **Current state**: MCP Marketplace has rev-share (85/15) but no scale; Smithery has scale but no rev model
- **Opportunity**: npm/PyPI/iOS App Store captured enormous value from distribution + trust + economic infrastructure
- **Key features needed**: Security scanning, compatibility testing, verified publishers, usage-based billing, rev-share

### Gap 3: Quality Curation for Agent Skills
- **Problem**: Skills.sh has 35K+ skills but "80% are AI slop"; SkillsGate has 60K+ but no quality signal
- **What's needed**: Verification badges, community ratings, automated quality testing, skill versioning
- **Analogy**: The npm quality problem, but earlier in the lifecycle
- **Potential approach**: Combine automated testing + community ratings + verified publisher badges

### Gap 4: MCP Observability & Debugging
- **What's missing**: Purpose-built MCP observability (tool call replay, response diffing, latency attribution, anomaly detection)
- **Current state**: General-purpose AI observability (LangSmith, Arize, Langfuse) doesn't cover MCP-specific failure modes
- **Opportunity**: Treat client-server interaction as primary unit of analysis

### Gap 5: Agent Skill Monetization Infrastructure
- **Problem**: Best way to get adoption is free, but free doesn't support production-grade infrastructure
- **What's needed**: Payment rails for skill creators, usage tracking, license enforcement
- **Only current solution**: MCP Marketplace (85/15 rev-share), Agensi (buy-once model), Skillgate ($19/mo)

### Gap 6: Cross-Agent Tool-Access Governance
- **Problem**: In multi-agent systems, sub-agents need different tool access scopes
- **What's missing**: Authorization policies when agents spawn sub-agents dynamically
- **Status**: Completely unsolved architecture

### Gap 7: Semantic Versioning for MCP/Skills
- **Problem**: MCP servers and skills can change schemas, breaking agent pipelines silently
- **What's needed**: Contract enforcement, compatibility testing, semantic versioning
- **Status**: No infrastructure exists

---

## 7. Strategic Recommendations

### For a New Skill Marketplace Entrant

#### Positioning Strategy: The "Trust Layer" for Agent Skills

Based on the competitive landscape analysis, the optimal positioning is at the intersection of **quality curation**, **security verification**, and **monetization infrastructure** — the three things the current leaders (Skills.sh, SkillsGate) explicitly lack.

#### Recommended Business Model

| Component | Approach | Rationale |
|-----------|----------|-----------|
| **Free tier** | Search, browse, install open skills | Match Skills.sh/SkillsGate adoption model |
| **Creator monetization** | Rev-share (80/20 or 85/15) on premium skills | Agensi proves willingness to pay; marketplace economics work |
| **Pro tier** ($19-49/mo) | Verified skills, security scanning, team features | Skillgate.app validates this price point |
| **Enterprise tier** | Private registries, audit logs, SSO, compliance | Massive unmet demand per MCP research |
| **Skill verification** | Automated testing + community reviews + publisher tiers | Key differentiator vs. all competitors |

#### Key Differentiators to Build

1. **Security-first**: Automated security scanning before listing (detect prompt injection, data exfiltration, malicious code)
2. **Quality curation**: Automated testing against multiple agents + community ratings + editorial picks
3. **Skill versioning**: Semantic versioning, compatibility matrices, deprecation workflows
4. **Enterprise readiness**: SOC2/GDPR compliance, audit trails, SSO, role-based access
5. **Cross-ecosystem**: Support SKILL.md + MCP servers + custom formats
6. **Creator economics**: Clear path to monetization for skill authors (rev-share, analytics, promotion tools)

#### Market Entry Strategy

**Phase 1 — Developer Adoption (Months 1-6)**
- Launch as open directory with quality signals (vs. Skills.sh's zero curation)
- Target Claude Code + Cursor users (largest agent user base)
- One-command install: `npx <tool> install <skill>`
- Free tier with community ratings and verification badges
- Aim: 10K+ skills indexed, 1K+ monthly active users

**Phase 2 — Creator Economy (Months 6-12)**
- Launch premium skill listings with rev-share
- Add skill versioning and compatibility testing
- Introduce verified publisher program
- Aim: First $100K in creator payouts, 100+ paid skills

**Phase 3 — Enterprise (Months 12-24)**
- Private skill registries for teams
- Audit logging and compliance features
- SSO integration
- Enterprise security scanning
- Aim: 10+ enterprise customers, $500K+ ARR

#### What to Avoid

1. **Don't try to be everything**: Focus on agent skills (SKILL.md/MCP), not general AI model hosting
2. **Don't ignore quality**: The #1 complaint about Skills.sh is quality — this is your wedge
3. **Don't go paid-only**: Free tier is table stakes for developer adoption
4. **Don't build a standalone hosting play**: Cloudflare/Vercel/Docker will eat you; build the trust/discovery layer instead
5. **Don't compete with incumbent labor marketplaces**: Upwork/Fiverr are conflicted on AI; build the AI-native marketplace instead

#### Key Metrics to Track

| Metric | Target (Year 1) | Benchmark |
|--------|-----------------|-----------|
| Skills indexed | 50K+ | SkillsGate: 60K |
| Monthly active users | 5K+ | Skills.sh: viral but unknown MAU |
| Paid skills | 100+ | Agensi: ~first paid skill |
| Creator payouts | $100K+ | Market creating |
| Enterprise customers | 10+ | Nobody has this yet |
| NPS among creators | 50+ | - |

#### The Big Thesis

> The MCP ecosystem is where the internet was in 1995 — the protocol is established, adoption is exploding, but the **commerce layer** (discovery, trust, payments, governance) doesn't exist yet. The company that builds the "App Store" for agent capabilities — combining quality curation, security verification, and creator economics — will capture a disproportionate share of the $52B+ AI agent market by 2030.

---

## Appendix A: Source URLs

1. TalenTeam — "2025 Talent Trends: Skills Marketplaces & Internal Mobility" (Feb 2025) — https://talenteam.com/blog/2025-talent-trends-the-rise-of-skills-marketplaces-and-internal-mobility/
2. JobsPikr — "Shifting Skill Trends in 2025" (May 2025) — https://www.jobspikr.com/insights/2025-skill-trends-analysis/
3. World Economic Forum — "Future of Jobs Report 2025: Skills Outlook" (Jan 2025) — https://www.weforum.org/publications/the-future-of-jobs-report-2025/in-full/3-skills-outlook/
4. NFX — "The Next 10 Years Will Be About the AI Agent Economy" (Feb 2025) — https://www.nfx.com/post/ai-agent-marketplaces
5. McKinsey — "Agentic Commerce: How Agents Are Ushering in a New Era" (Oct 2025) — https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-agentic-commerce-opportunity
6. MindStudio — "How to Build and Monetize AI Agents as a Business" (Feb 2026) — https://www.mindstudio.ai/blog/build-monetize-ai-agents-business
7. Oracle — "Introducing AI Agent Marketplace" (Nov 2025) — https://blogs.oracle.com/fusioninsider/introducing-ai-agent-marketplace
8. Deepak Gupta — "MCP Guide: Enterprise Adoption 2025" (Dec 2025) — https://guptadeepak.com/the-complete-guide-to-model-context-protocol-mcp-enterprise-adoption-market-trends-and-implementation-strategies/
9. Primitives AI (Substack) — "The MCP Ecosystem" (Mar 2026) — https://primitivesai.substack.com/p/the-mcp-ecosystem-how-a-protocol
10. Vibe Coding — "Skills.sh Review (2026)" — https://vibecoding.app/blog/skills-sh-review
11. John Oct — "Skills.sh: The Missing Package Manager for AI Agent Capabilities" (Feb 2026) — https://johnoct.github.io/blog/2026/02/12/skills-sh-open-agent-skills-ecosystem/
12. SkillsGate.ai — Homepage (2026) — https://skillsgate.ai/
13. Skillgate.app — "Best AI Skills Marketplace in 2026" — https://skillgate.app/blog/best-ai-skills-marketplace
14. Reddit r/vibecoding — "I indexed 45k AI agent skills" (SkillsGate launch thread) — https://www.reddit.com/r/vibecoding/comments/1rrfdp3/
15. Agensi.io — Homepage — https://www.agensi.io/
16. Reddit r/claude — "Agensi hit 100 users" — https://www.reddit.com/r/claude/comments/1rqrsom/
17. New Market Pitch — "Agentic AI Market Funding Trends (2022-2026)" (Feb 2026) — https://newmarketpitch.com/blogs/news/agentic-ai-funding-trends
18. AI Agents Directory — "Agentic AI Startups Raise $2.8B in H1 2025" (Aug 2025) — https://aiagentsdirectory.com/blog/agentic-ai-venture-funding-explodes
19. AI Funding Tracker — "Top AI Agent Startups 2026" — https://aifundingtracker.com/top-ai-agent-startups/
20. HiPeople — "5 Best Talent Marketplace Platforms 2025" — https://www.hipeople.io/blog/talent-marketplace-platforms
21. Partnerfleet — "What is an AI Agent Marketplace?" (Dec 2025) — https://www.partnerfleet.io/blog/what-is-an-ai-agent-marketplace
22. Google Cloud — "AI Agent Marketplace" (Oct 2025) — https://cloud.google.com/blog/topics/partners/google-cloud-ai-agent-marketplace
23. Sprad — "7 Best Internal Talent Marketplace Platforms 2025" (Sep 2025) — https://sprad.io/blog/internal-talent-marketplace-software-in-2025

---

## Appendix B: Competitive Matrix

| Platform | Type | Skills/Agents | Revenue Model | Quality Control | Enterprise Ready | Agent Agnostic |
|----------|------|---------------|---------------|-----------------|-----------------|----------------|
| Skills.sh | Open directory | 35K+ | Free (none) | None | No | Yes (30+) |
| SkillsGate | Open marketplace | 60K+ | Free/TBD | Crowd-sourced scans | No | Yes (17+) |
| Agensi.io | Paid marketplace | Small | Buy-once | Manual review | No | Yes (20+) |
| Skillgate.app | Curated packs | 222+ | Freemium ($19/mo) | Production-tested | Partial | Yes |
| SkillsMP | Directory | 500K+ | Free | None | No | Yes |
| Oracle AI Agent Marketplace | Enterprise | Growing | Subscription | 21-point checklist | Yes | No (Oracle only) |
| MCP Marketplace | Paid MCP servers | Small | 85/15 rev-share | Unknown | No | MCP-compatible |
| Enso | SMB agent marketplace | 300+ | $49/mo | Curated | No | N/A |
| MindStudio | Agent builder + marketplace | Growing | Multiple (sub/usage/outcome) | Platform review | Partial | Multi-model |
