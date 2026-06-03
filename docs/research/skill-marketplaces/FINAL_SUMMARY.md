# Skill Marketplaces: Comprehensive Deep Research Report

> **Archival.** This is the R1-R9 round synthesis. The canonical master summary is [`research/SUMMARY_AND_CONCLUSIONS.md`](../SUMMARY_AND_CONCLUSIONS.md). This file is preserved for provenance — it contains detailed regulatory, blockchain, and enterprise data not yet fully merged into the canonical file.

*Compiled March 16, 2026 | 9 research rounds | 58 files | ~15,500+ lines of raw research*
*Sources: GitHub, Twitter/X, Reddit, arXiv, Kaggle, Industry/Web, DuckDuckGo web scraping*

---

## 1. Executive Summary

The **AI agent skill marketplace** is the defining infrastructure category of 2026. What began as Cursor rule-sharing in late 2024 has exploded into a full ecosystem with:

- **450,000+ published skills** across 12+ web marketplaces (skills.sh alone at 75K+ with 6M+ developers)
- **90+ academic papers** on arXiv studying marketplace dynamics, security, and economics
- **135+ GitHub repositories** building marketplace infrastructure
- **4 major vendors** (Anthropic, OpenAI, Microsoft, Google) converged on SKILL.md
- **$7.5-8.3B market in 2025**, ~$12B in 2026, consensus $47-53B by 2030 (CAGR 41-46%)
- **A catastrophic security crisis**: 36.82% of skills have vulnerabilities (Snyk audit of 3,984), 12K+ malicious detected by Gen Trust Hub
- **67% of Fortune 500** have production agentic AI deployments (340% surge from 19% in 2024)
- **$146B+ in AI M&A** in 2025; AI agents capture 33% of global VC funding

The ecosystem has progressed through distinct phases:
- **R1-R2** (Early 2026): Discovery and mapping
- **R3-R4**: Security alarms and marketplace saturation
- **R5-R6**: Monetization experiments and regulatory pressure
- **R7**: Governance, pricing, and agent behavioral economics
- **R8**: A2A protocol adoption, on-chain escrow, trust certification, and gaming threats
- **R9**: ClawHavoc crisis, trust layer pivot, industry economics, regulatory reckoning, standards crystallization

---

## 2. Platform-by-Platform Findings

### 2.1 GitHub (182+ repos catalogued across R1-R9)

**Key discoveries:**
| Category | Count | Notable Examples |
|----------|-------|-----------------|
| AI Agent Skill Marketplaces | 60+ repos | phuryn/pm-skills (7,311 stars), block/agent-skills, SkillX |
| Awesome Lists/Registries | 15+ | VoltAgent (11,412 stars), 549+ curated skills |
| Security Tools | 15+ | Trail of Bits (3,589 stars), SkillFortify, mcp-scan, agent-gate |
| A2A Protocol Implementations | 30+ | 8 languages (TS, Python, Rust, Go, Java, PHP, C#, Django) |
| Agent DNS/Discovery | 10+ repos | godaddy/ans-registry (IETF), mcp-dns-registry (AWS), AgentDNS |
| Trust Infrastructure | 6 repos | trust-mcp, Praesidia (OAuth 2.0), capiscio (crypto validation) |
| Enterprise Patterns | 8+ | Block/Goose, Microsoft/skills, HashiCorp/agent-skills, AWS Labs |
| Failure Recovery | 6+ repos | clawback (regression learning), agent-gate (vault rollback) |

**Top repos by stars:**
1. **VoltAgent/awesome-agent-skills** - 11,412 stars - De facto skill directory
2. **phuryn/pm-skills** - 7,311 stars - 65+ PM skills, 36 workflows, 8 plugins
3. **Trail of Bits/skills** - 3,589 stars - Security research skills
4. **daymade/claude-code-skills** - 652 stars - 42 skills + meta-skill-creator
5. **binance/binance-skills-hub** - 462 stars - Enterprise crypto skills

**Architectural pattern**: Skills (SKILL.md) -> Commands (chained workflows) -> Plugins (packaged bundles) -> Marketplaces (discovery + trust)

**R9 critical discoveries:**
- **godaddy/ans-registry** - IETF-backed Agent Name Service with X.509 PKI, Merkle transparency logs. GoDaddy building "DNS for agents"
- **mariothomas/mcp-dns-registry** - DNS-based MCP discovery via `_mcp` TXT records. Written by AWS Head of Applied AI. Live reference implementation
- **block/agent-skills** - Block (Square) enters with marketplace + Goose agent ecosystem + npx CLI installer
- **Tessera (knowledge layer)** - Third protocol: MCP = tools, A2A = coordination, Tessera = knowledge transfer between architectures
- **agent-gate** - Vault-backed execution control with OPA policies. "Inspect the action, not the reasoning"
- **IDE-native marketplace** - VS Code extension (formulahendry/vscode-agent-skills) brings skill discovery into the editor

**Business models observed:**
- SquidBay: Rent/Learn/Own via Bitcoin Lightning
- SkillX: Centralized search + ratings (34 stars)
- MCPBundler: Curated aggregation
- ClawMart: Managed AI workforce (hire teams, not skills)

### 2.2 Twitter/X (130+ signals across R1-R9)

**Key trends and voices:**
- **ERC-8183 (Agentic Commerce)** dropped Feb 25 - Ethereum Foundation + Virtuals Protocol. The escrow/commerce layer for agent jobs
- **ERC-8004 + ERC-8183 flywheel** - Discovery -> commerce -> reputation -> discovery loop
- **2026 Standards Stack crystallized** - x402 (payments) + ERC-8004 (identity) + ERC-8126 (risk scoring, 0-100) + ERC-8183 (commerce) + ERC-7984 (privacy)
- **Skills.sh at 75K+ skills, 6M+ developers** - Vercel-backed, supports 35+ agents
- **Gen Digital Agent Trust Hub** - 12K+ malicious skills detected, 60M+ users protected, partnered with Vercel
- **Snyk ToxicSkills audit** - 36.82% of 3,984 skills have flaws, 13.4% critical, 76 confirmed malicious. New threat: "time-shifted prompt injection"
- **KuCoin Skills Hub launched (March 15, 2026)** - First major centralized exchange with dedicated agent skills marketplace
- **x402 hit $600M+ cumulative** but daily volume collapsed 92% to ~$28K/day
- **MoltBay** - First A2A-native marketplace where agents hire other agents autonomously
- **AgentVerus** - Trust certification ("SSL for skills") with CI integration
- **Mastercard AgentPay** live for US cardholders; Stripe/OpenAI Agentic Commerce Protocol launching
- **Galaxy Research estimates $3-5T B2C agentic commerce by 2030**

**Sentiment evolution:** Security alarm discourse rose from ~15% to ~45% of all Twitter discussion. Narrative shifted from "marketplace" to "trust layer."

### 2.3 Reddit (53+ threads analyzed across R1-R9)

**Key community insights:**
- **ClawHub Malware Crisis ("ClawHavoc")** - #1 downloaded skill on OpenClaw was malware. 341 malicious skills. Creator reportedly hired by OpenAI afterward
- **41% of skills have vulnerabilities; 1 in 5 silently exfiltrate data** - Post-install behavior changes documented
- **Production gap is massive** - 71% deploy agents, only 11% reach production
- **Enterprise agent trust is "a full infrastructure problem with no owner"** - Signed JWT headers, proxy validation (~60% WAF false-positive reduction), delegation chains
- **"Friction is a feature"** - Moltbook collapsed because interactions were too cheap
- **Skill monetization existentially challenged** - $26.48 invested in 7 agents → $0 revenue in Week 1. "Distribution is the hard problem, not production"
- **Narrative shift: "Build trust layer, not marketplace"** - Four documented shifts: marketplace→trust layer, sell skills→sell execution, agent marketplace→agent infrastructure, exciting→"npm but worse"
- **A2A Protocol moving to production** - Box, Salesforce, municipal governments piloting

**Pricing consensus (from 170+ comments):**
| Model | Description | Who Uses It |
|-------|-------------|-------------|
| Outcome-based | Pay per result | Sales agents |
| Action-based | Credits per run ($3-12) | Most B2C builders |
| Hybrid | Base + performance kicker | Enterprise |
| Machine-based | $99/mo per deployment + 20% token markup | Simple, scales poorly |
| Cost of Pass | Human rate minus agent cost | Most sophisticated |
| Crypto | SOL/BNB micropayments | Frictionless, niche |

### 2.4 arXiv (90+ papers analyzed across R1-R9)

**Landmark papers:**

| Paper | ID | Key Finding |
|-------|-----|-------------|
| **COALESCE** | 2506.01900 | First skill-based labour exchange; 41.8% cost reduction |
| **ACES** | 2508.02630 | Agent buyers have 10-30x first-proposal bias, choice homogeneity |
| **Magentic Marketplace** | Microsoft | Quality degrades as agent count scales |
| **SkillFortify** | 2603.00195 | Formal verification; 96.95% F1 with 0% false positives |
| **Skill-Inject** | 2602.20156 | 80% attack success on frontier models |
| **SkillOrchestra** | 2602.19672 | 22.5% better than RL at 700x lower cost |
| **Institutional AI** | 2601.11369 | Prompt governance = zero benefit; only runtime enforcement works |
| **ToolTweak** | 2510.02554 | Adversaries boost tool selection 20% -> 81% via description manipulation |
| **InsuredAgents** | 2512.08737 | Protocol-native insurance with TEE-protected audits |
| **Agent Behavioral Contracts** | 2602.22302 | Formal Design-by-Contract for agents; <10ms overhead |
| **The Headless Firm** | 2602.21401 | Agentic AI shifts integration cost O(n^2) -> O(n) |
| **Agent-OSI** | 2602.13795 | Six-layer protocol stack; HTTP 402 for payments; 51% cost reduction |
| **AESP** | 2603.00318 | Cryptographic human sovereignty over agent spending |
| **Vertical Tacit Collusion** | 2601.03061 | Platform-seller aligned incentives = super-additive consumer harm |
| **Anti-collusion Mapping** | 2601.00360 | Human anti-collusion -> multi-agent AI interventions |
| **AI Agent Reliability** | 2602.16666 | 12 metrics across 4 dimensions; capability != reliability |
| **Magentic Marketplace** | 2510.25779 | Microsoft: 10-30x first-proposal bias; quality degrades at scale |
| **AgentRank-UC** | 2509.04979 | PageRank-equivalent for agent marketplaces; DOVIS five-layer protocol |
| **Proof-of-Guardrail** | 2603.05786 | TEE-based cryptographic proof of safety compliance |
| **MTTR-A** | 2511.20663 | SRE metrics adapted for agents; rate limiting most damaging fault |

**Critical academic findings:**
1. Agent markets are fundamentally different from human markets (ACES, Magentic)
2. Prompt-only governance provides ZERO reliable improvement (Institutional AI)
3. Model scaling does NOT solve skill security (FASA, Skill-Inject)
4. Quality beats quantity - curated skills improve success; self-generated may degrade it
5. A single malicious actor accounts for 54.1% of all skill attacks
6. Hybrid trust (Proof+Stake+Reputation) needed — no single mechanism suffices (3 independent papers)
7. First-proposal bias (10-30x) makes agent marketplace UX design critical (Magentic Marketplace)

### 2.5 Kaggle (44+ datasets)

**Key datasets for marketplace builders:**
- **O*NET + ESCO skill embeddings** - Foundational taxonomy for any skill marketplace
- **1.3M freelance contracts** - Largest marketplace economic dataset
- **AI-era job roles** - LLM Engineer, RAG Engineer, AI Agent Developer with demand scores
- **25+ directly relevant datasets** for skill matching, pricing, and quality prediction
- **Production ML pipelines** demonstrated: text vectorization + skill embeddings + XGBoost

---

## 3. The Security Crisis (Quantified)

| Metric | Value | Source |
|--------|-------|--------|
| Skills with security flaws (Snyk audit) | 36.82% of 3,984 scanned | Snyk ToxicSkills |
| Critical-level security issues | 13.4% (534 skills) | Snyk ToxicSkills |
| Skills with at least one vulnerability | 26-41% | Multiple studies |
| Confirmed malicious skills (total) | 1,184+ | Stable-Learn / HackerNews |
| ClawHavoc campaign | 341 malicious skills; #1 download was malware | Reddit / HackerNews |
| Malicious skills detected by Gen Trust Hub | 12,000+ | Gen Digital |
| Users protected by Gen Trust Hub | 60 million+ | Gen Digital |
| Malicious tools catalogued (MalTool) | 6,487 | arXiv 2603.00195 |
| Attack success rate on frontier models | 80% | Skill-Inject benchmark |
| Credential theft from single fake skill | 6K+ users | Reddit/caterpillar scanner |
| OpenClaw instances worldwide | 63,026 | GitHub security report |
| Data exfiltration prevalence | 13.3% of all skills | Multiple |
| Third-party content injection | 17.7% of skills | Multiple |
| Malicious skills with code exploits | 100% | Snyk ToxicSkills |
| Malicious skills also using prompt injection | 91% | Snyk ToxicSkills |

**Why agent skills are worse than package ecosystems:**
- Traditional packages: isolated execution. Agent skills: **full agent permissions** (shell, filesystem, env vars, email)
- New attack vectors with no package-ecosystem analog: **prompt injection, memory poisoning, time-shifted payload assembly**
- Memory poisoning **survives uninstallation, agent restarts, and platform updates**

---

## 4. The Five Architectural Layers

Every viable skill marketplace must address all 5:

```
+------------------------------------------+
|  5. GOVERNANCE                           |  Singapore IMDA, IEEE P3709,
|     Compliance, identity, audit          |  OWASP Agentic Top 10, COMPASS
+------------------------------------------+
|  4. ORCHESTRATION                        |  A2A Protocol (30+ impls),
|     Multi-agent coordination             |  SkillOrchestra, AWCP
+------------------------------------------+
|  3. PAYMENTS                             |  x402, Stripe AgentPay,
|     Pricing, billing, escrow             |  Mastercard, crypto micropayments
+------------------------------------------+
|  2. TRUST                                |  AgentVerus, SkillJury, Conduit,
|     Validation, reputation, QA           |  Ev-Trust, ClawSecure
+------------------------------------------+
|  1. DISCOVERY                            |  SkillsMP, skills.sh, SKILL.md,
|     Search, recommendation               |  ChainRec, semantic search
+------------------------------------------+
```

**No single project covers all 5 layers. The first to integrate them wins.**

---

## 5. Market Landscape (March 2026)

### Market Size & Economics (R9 Industry Report)

| Metric | Value | Source |
|--------|-------|--------|
| AI agent market 2025 | ~$7.5-8.3B | 10+ market research firms consensus |
| AI agent market 2026 | ~$12B | Business Research Co. / Fortune BI |
| AI agent market 2030 | $47-53B (CAGR 41-46%) | Multi-source consensus |
| AI M&A activity 2025 | $146B+ in disclosed deals | MightyBot |
| AI agents' share of global VC | 33% | CB Insights |
| Fortune 500 with production agents | 67% (up from 19% in 2024) | McKinsey / Beam AI |
| Agent companies (claimed) | 2,000+ (only ~130 real per Gartner) | Gartner |
| Skill marketplace TAM 2026 | $500M-1B, growing 80-100% annually | AI Skill Market |
| Top agent startup valuation | Anysphere (Cursor) $29.3B | AI Funding Tracker |
| Agent revenue multiples | 52x ARR average; 127x for customer service | CB Insights |
| Infrastructure investment 2026 | $650B planned across Big Tech | Industry reports |

**Top Funded AI Agent Startups (Q1 2026):**
Anysphere/Cursor ($29.3B), Cognition/Devin ($10.2B), Sierra ($10B), Replit ($9B), Glean ($7.2B), Lovable ($6.6B), Harvey AI ($5B), n8n ($2.5B)

**Outcomes-based pricing is replacing seat licenses:** Sierra hit $100M ARR in 21 months with pay-for-results. Zendesk charges only for successful outcomes. Traditional SaaS pricing declared dead for agents.

**The Great Filter:** Of 2,000+ "agentic AI" companies, Gartner says ~130 are real. 42% of companies abandoned most AI initiatives in 2025. Next 12 months determine survivors.

### Regulatory Landscape

| Regulation | Jurisdiction | Effective Date | Key Impact |
|-----------|-------------|---------------|------------|
| EU AI Act high-risk requirements | EU | Aug 2026 (possible delay to Dec 2027) | Conformity assessment, documentation, human oversight |
| Colorado SB 24-205 | Colorado, US | June 30, 2026 | Impact assessments, discrimination prevention, $20K/violation |
| Federal AI procurement (OMB M-26-04) | US Federal | March 11, 2026 | Model cards, evaluation artifacts required |
| California SB 53 | California, US | Signed Sep 2025 | Safety frameworks, catastrophic risk assessments |
| FTC enforcement (Air AI case) | US | Active | Marketing substantiation for agent claims |

38 US states passed AI legislation in 2025. 42 state AGs sent letters to major AI companies demanding pre-release safety testing.

### Web Marketplaces

| Platform | Skills | Key Differentiator |
|----------|--------|-------------------|
| **SkillsMP** | 400K+ | Mass aggregation, largest by count |
| **skills.sh** | 75K+ (6M+ devs) | Vercel-backed, Gen Digital trust partnership |
| **SkillsGate** | 60K+ | Security scanning via MCP |
| **SkillzWave** | 42K+ | ML quality scores |
| **SkillHub** | 7K+ | 5-dimension AI evaluation |
| **SquidBay** | Agent commerce | Bitcoin Lightning payments |
| **SpoonOS** | Web3 | Neo blockchain, first Web3 marketplace |
| **MoltBay** | A2A-native | Agents hiring agents autonomously |
| **Agensi** | Growing | 8-layer security, first paid skill sold |

### Internal Talent Marketplace Platforms (Enterprise)

| Platform | Key Feature |
|----------|-------------|
| **Gloat** | Best "pure-play" internal marketplace |
| **Eightfold AI** | Best skills AI + talent intelligence |
| **Fuel50** | Best career pathing experience (92% G2 score) |
| **Workday** | Integrated HCM + marketplace |
| **SAP SuccessFactors** | Enterprise ERP integration |
| **ServiceNow** | IT-centric skill matching |
| **Degreed** | Learning + skills marketplace |

**Internal talent marketplace market**: $12.1B projected by 2027, 40% CAGR.

### Blockchain/Web3 Skill Marketplaces

| Platform | Chain | Mechanism |
|----------|-------|-----------|
| **ERC-8183** | Ethereum | Escrow/commerce layer for agent jobs |
| **VelaNetwork** | Multi-chain | On-chain escrow with judge agents |
| **AgenC** | Unknown | ZK proofs for skill verification |
| **Rialo/SCALE** | Unknown | Reputation-staked marketplace |
| **Meta402** | Unknown | HTTP 402 payment challenges |
| **Rentaclaw** | Solana | $0.00025/tx micro-rentals |
| **SafuSkill** | BNB Chain | GoPlus security scanning |

---

## 6. Key Conclusions

### What's Working
1. **SKILL.md is the standard** - Format war is over. All 4 major vendors converged.
2. **Vertical specialization wins** - PM (7,311 stars), security (3,589), crypto (462), legal (176)
3. **Discovery is solved at the basic level** - Multiple marketplaces with 10K+ skills
4. **A2A protocol gaining real traction** - 30+ implementations, Fortune 500 piloting

### What's Broken
1. **Security is catastrophically bad** - 1 in 4 skills has a vulnerability
2. **No integrated trust layer** - Trust is fragmented across 6+ partial solutions
3. **Production gap** - 71% deploy, only 11% reach production
4. **Agent buyers are terrible** - 10-30x first-proposal bias, gaming vulnerability
5. **Prompt governance doesn't work** - Zero reliable benefit (academic proof)
6. **Marketplace fatigue** - Too many overlapping, undifferentiated marketplaces

### What's Missing (Biggest Opportunities)
1. **Full-stack marketplace integrating all 5 layers** - Discovery + Trust + Payments + Orchestration + Governance
2. **Agent-native discovery** - Current UX is for humans; agents need different ranking
3. **Insurance/failure recovery** - InsuredAgents paper exists but no production implementation
4. **Skill versioning and dependency resolution** - SKILL.md needs semver + lockfiles
5. **Cross-marketplace portability** - Skills are locked to individual marketplaces
6. **Agent DNS/registry** - No universal agent identity/discovery standard
7. **Anti-gaming infrastructure** - ToolTweak shows 20% -> 81% manipulation is trivial

---

## 7. Strategic Recommendations

### If You're Building a Skill Marketplace:

**Do:**
1. **Start with trust, not discovery** - "The marketplace that solves trust first wins"
2. **Pick a vertical and go deep** - Horizontal aggregation is saturated (400K+ undifferentiated skills)
3. **Implement runtime governance, not prompts** - Only governance graphs + runtime enforcement works
4. **Build for agent buyers, not human browsers** - Anti-first-proposal-bias, anti-gaming
5. **Adopt SKILL.md + semver + lockfiles** - The standard is settled; add versioning
6. **Price on outcomes, not seats** - "SaaS metrics are dead for agentic ecosystems"
7. **Add friction intentionally** - Moltbook collapsed because interactions were too cheap

**Don't:**
1. Don't chase volume - 400K skills exist, 90%+ undifferentiated
2. Don't trust model scaling for security - 80% attack success even on frontier models
3. Don't rely on prompt-based governance - Proven zero benefit
4. Don't auto-generate skills naively - Only evolutionary approaches work
5. Don't ignore regulation - Colorado SB 24-205 effective June 30, 2026

### The Winning Architecture (Predicted):

```
Agent requests capability
  -> Discovery layer: semantic SKILL.md search + agent-optimized ranking
  -> Trust layer: AgentVerus-style certification + runtime scanning
  -> Payment layer: outcome-based pricing with escrow
  -> Orchestration layer: A2A + SkillOrchestra competence matrices
  -> Governance layer: runtime enforcement + audit logs + compliance
```

---

## 8. Research Coverage Summary

| Platform | Items Analyzed | Key Metric |
|----------|---------------|------------|
| GitHub | 182+ repos | 47 new repos in R9; 2 CRITICAL (GoDaddy ANS, MCP-DNS) |
| Twitter/X | 130+ signals | Gen Digital protecting 60M+ users |
| Reddit | 53+ threads | ClawHavoc: 341 malicious skills, #1 download was malware |
| arXiv | 90+ papers | 31 new in R9; Proof-of-Guardrail TEE verification |
| Kaggle | 44+ datasets | 1.3M freelance contracts (largest) |
| Industry/Web | 40+ sources | $47-53B market by 2030, $146B M&A in 2025 |
| Research files | 58 files | ~15,500+ lines |

---

## 9. The Big Picture

The skill marketplace space in March 2026 looks remarkably similar to the **npm ecosystem circa 2015** - explosive growth, terrible security, competing registries, nascent monetization. But with one critical difference: **agent skills execute with full system permissions**, making the security stakes orders of magnitude higher.

The three forces that will determine winners:
1. **Trust** - Who solves verification, scanning, and reputation first
2. **Agent-native design** - Who builds for agent buyers (not human browsers)
3. **Governance** - Who integrates compliance as a product (not an afterthought)

The marketplace that integrates all 5 architectural layers (Discovery + Trust + Payments + Orchestration + Governance) into a coherent product will likely become the dominant platform - much as npm, PyPI, and Docker Hub became dominant in their respective ecosystems.

**The window is open. The standards are set. The security crisis creates urgency. Build now.**

---

*This report synthesizes 9 rounds of research across 6 platforms (GitHub, Twitter/X, Reddit, arXiv, Kaggle, Industry/Web), 58 research files, and ~15,500+ lines of findings. R9 added 5 new platform reports (Reddit, Twitter, arXiv, Kaggle, Industry) plus a comprehensive GitHub catalog of 47 new repos.*

*Generated March 16, 2026*
