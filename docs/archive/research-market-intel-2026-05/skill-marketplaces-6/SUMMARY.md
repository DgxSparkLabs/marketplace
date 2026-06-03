# Skill Marketplaces: Deep Research Summary — Round 6

> **Date:** March 16, 2026
> **Scope:** GitHub, Twitter/X, Reddit, arXiv, Kaggle, Emerging Trends (Web)
> **Method:** 6 parallel research agents, 30+ searches, 50+ pages scraped, 2,200+ lines of raw findings
> **Building on:** 5 prior research rounds (80+ GitHub repos, 21+ arXiv papers, 30+ Twitter signals, 25+ Reddit threads, 30+ Kaggle datasets)

---

## Executive Summary

Round 6 reveals the skill marketplace ecosystem entering its **adolescent crisis** — explosive growth colliding with systemic security failures, monetization uncertainty, and regulatory pressure. Five developments define this moment:

1. **The Security Crisis Has Escalated to "Persistent Memory Poisoning."** ClawHavoc scaled from 341 to 1,184 malicious skills. The attack vector evolved from simple credential theft to **memory poisoning that survives uninstallation, agent restarts, and OpenClaw updates**. A fake "reminder" skill harvested .env files from 6K+ users. Skill-Inject benchmark shows **80% attack success rate on frontier models**.

2. **Six Competing Monetization Models Are Now Live in Production.** Pay-per-command (x402/USDC), pay-per-use (Kodeus), outcome-based pricing, agent-to-agent payments (Mastercard AgentPay/Stripe), micro-rentals (Rentaclaw on Solana, $0.00025/tx), and revenue-sharing (Virtuals.io at $1M+/month). Subscriptions are declining.

3. **Academic Research Has Produced Actionable Marketplace Infrastructure.** COALESCE gives agents economic agency (41.8% cost reduction). AEX borrows RTB advertising architecture for skill auctions. SkillOrchestra outperforms RL orchestrators by 22.5% at 700x lower cost. Governance graphs reduce collusion from 50% to 5.6%.

4. **Regulation Is Arriving.** Colorado SB 24-205 (effective June 30, 2026) targets AI system deployers with concrete compliance requirements — impact assessments, risk policies, consumer notices, incident response. First binding legislation on the skill marketplace ecosystem.

5. **The Ecosystem Has Bifurcated into Two Non-Converging Tracks.** Traditional (Anthropic/SkillsMP/Skills.SH — SKILL.md, MCP, developer productivity) vs. Web3 (SpoonOS/Rentaclaw/Teneo/Kodeus/Phala/Virtuals — on-chain payments, token economies, decentralized identity). They share vocabulary but have fundamentally different trust models.

---

## What's New Since Round 5

### GitHub — New Repos & Ecosystem Shifts

| Repo | Stars | Category | Significance |
|------|-------|----------|-------------|
| **VoltAgent/awesome-agent-skills** | 11,412 | Awesome list | 549+ skills from 30+ official teams — the de facto directory |
| **Trail of Bits/skills** | 3,589 | Security tools | 30+ security research plugins with real bug trophy case |
| **videocut-skills** | 1,136 | Vertical | Video editing skills — ecosystem beyond dev tools |
| **android-re skills** | 959 | Vertical | Android reverse engineering domain |
| **chinese-novelist-skill** | 663 | Vertical | Novel writing in Chinese |
| **.NET skills** | 614 | Vertical | .NET development ecosystem |
| **lawvable** | 176 | Vertical | Legal domain skills |
| **takumiyoshikawa/skill-loop** | 18 | Orchestration | YAML-based skill chaining with LLM routing + cron |
| **RuneHub** | - | Composition | 228 Skills → 139 Packages → 65 Rune DAGs |
| **SkillWeave** | 0 (IEEE) | Academic | Formal skill composition algebra (SSCA), 1,081 pairwise compositions |
| **skill-audit-registry** | - | Security | On-chain (Solidity/Base) immutable audit records |
| **x402guard** | - | Security | Paid security scanning + USDC payments |
| **ryanfrigo/clawmart** | 2 | Marketplace | "Trust through usage" decentralized marketplace |
| **Diversio** | 2 | Standards | CI-enforced SKILL.md ≤500 lines, agentskills.io compliant |

**Key Pattern:** The ecosystem has moved far beyond developer-tool skills into **domain verticals** (legal, video editing, novel writing, Android RE, .NET, cybersecurity). Vertical specialization is the dominant growth vector.

### arXiv — 12 New Papers

| Paper | ID | Key Finding |
|-------|-----|-------------|
| **COALESCE** | 2506.01900 | First skill-based labour exchange for LLM agents; 41.8% cost reduction |
| **Agent Exchange (AEX)** | 2507.03904 | RTB-inspired auction platform for agent skill markets |
| **SkillOrchestra** | 2602.19672 | Skill-aware orchestration; 22.5% better than RL at 700x lower cost |
| **XSkill** | 2603.12056 | Dual-stream continual learning (experiences + skills) |
| **Automating Skill Acquisition** | 2603.11808 | Mining GitHub for skills; 40% efficiency gain |
| **Skill-Inject** | 2602.20156 | 80% attack success rate on frontier models via skill injection |
| **ClawGuard/FASA** | 2603.12644 | Tri-layered zero-trust security architecture |
| **LLM Markets** | 2603.08853 | LLM agents are terrible consumers; institutional design needed |
| **Malicious Skills (MalTool)** | 2602.06547 | 157 malicious skills; single actor = 54.1% of all attacks |
| **Institutional AI** | 2601.11369 | Governance graphs: collusion 50% → 5.6%; prompts alone = zero benefit |
| **Meta Context Engineering** | 2601.21557 | Evolutionary skill optimization; 16.9% mean improvement |
| **MT-MARL Skill Graphs** | 2507.06690 | Hierarchical skill graphs for multi-agent RL |

**Landmark findings:**
- **Prompt-only governance provides ZERO reliable improvement** — only runtime enforcement (governance graphs + Oracle/Controller) works
- **Model scaling does NOT solve skill security** — FASA confirms this
- **LLM agents are terrible market participants** — they focus on price over strategy, enabling expert fraud
- **A single malicious actor accounts for 54.1% of all skill attacks** via templated brand impersonation

### Twitter/X — Discourse Shifts

- **Memory poisoning** emerged as the scariest new attack vector — survives uninstallation
- **Mastercard AgentPay live** for US cardholders; Stripe/OpenAI Agentic Commerce Protocol launching with 1M+ Shopify merchants
- **"Agent Maestro"** as a new $2K-5K/engagement professional role — skill curation as a career
- **Security alarm sentiment rose from ~15% to ~35%** of all discourse
- **Anthropic added skills to the free plan** — massive democratization
- **7+ new marketplace entrants**: Paperclip/Clipmart, SpoonOS, Rentaclaw, Kodeus, Teneo, Phala, Questflow

### Reddit — Community Ground Truth

- **26% vulnerability rate confirmed** across 31K+ skills (first formal study)
- **Fake skill harvested .env from 6K+ users** — the "npm malicious package" moment
- **Shadow AI** in enterprises far bigger than expected ("wild how much you find once you look")
- **Colorado SB 24-205** identified as regulatory catalyst (effective June 30, 2026)
- **MCP vs Skills distinction crystallized**: MCP = access layer, Skills = instructional/behavioral layer
- **Marketplace fatigue** setting in — users confused by overlapping competing marketplaces
- **First paid skill sold** on Agensi marketplace — monetization nascent but beginning

### Kaggle — Data Landscape Matured

- **25+ directly relevant datasets** now available (up from ~8 in prior rounds)
- **O*NET + ESCO skill embeddings** — foundational taxonomy resource for any marketplace
- **1.3M freelance contracts** — largest marketplace economic dataset
- **AI-era job roles captured**: LLM Engineer, RAG Engineer, AI Agent Developer with demand scores
- **Production-ready ML pipelines** demonstrated: text vectorization + skill embeddings + XGBoost

---

## The Five Escalated Problems

### 1. Security Crisis — From Bad to Existential

| Metric | Round 5 | Round 6 | Change |
|--------|---------|---------|--------|
| Vulnerability rate | 26.1% | 26-38% (confirmed at scale) | Validated |
| Malicious skill campaigns | ClawHavoc initial | 1,184 skills, memory poisoning | **Escalated** |
| Attack sophistication | Credential theft | Persistent memory poisoning, time-shifted injection | **New category** |
| Frontier model resilience | Unknown | 80% attack success rate | **Quantified** |
| Scale of credential theft | Unknown | 6K+ users from single fake skill | **First documented** |

**New attack vectors:**
- **Memory poisoning**: Payload survives uninstallation, modifying agent long-term memory
- **Time-shifted prompt injection**: Fragmented payloads assembled later from memory
- **Brand impersonation**: Single actor created 54.1% of all malicious skills via templates

### 2. Monetization — Six Models, No Winner

| Model | Platform | Revenue | Status |
|-------|----------|---------|--------|
| Pay-per-command | Teneo (x402/USDC) | Per call | Live |
| Pay-per-use | Kodeus | Per execution | Live |
| Outcome-based | Jay Thakrar | Per result | Pioneered |
| Agent-to-agent payments | Mastercard/Stripe/OpenAI | Per transaction | **Live at scale** |
| Micro-rentals | Rentaclaw (Solana) | $0.00025/tx | Live |
| Revenue-sharing | Virtuals.io | $1M+/month deployed | Live |
| Subscriptions | Various | Monthly fee | **Declining** |

**Key insight:** Enterprise DevTool companies (Vercel, Stripe, Microsoft) give skills away as marketing channels. The monetizable layer is **execution, not content**.

### 3. Governance — Prompts Don't Work, Period

The single most important finding from Round 6:

> **Prompt-only "constitutional" rules provide ZERO reliable improvement** — they fail under optimization pressure. Only governance graphs with Oracle/Controller runtime enforcement and append-only audit logs work. (Institutional AI, 2601.11369)

This validates what Reddit users have been saying: "If the answer is 'the agent's config' or 'the system prompt' then you don't have governance, you have suggestions."

**Colorado SB 24-205** (effective June 30, 2026) will force this into law — impact assessments, risk policies, consumer notices, incident response, annual reviews are all required.

### 4. Discovery & Scale — Marketplace Fatigue

- **351K+ skills on SkillsMP** — 90%+ undifferentiated
- **45K indexed on SkillsGate** out of 150K+ available
- Multiple overlapping marketplaces causing user confusion
- Self-generation threat: "I just realized I could tell Claude to build me custom skills"
- **Discovery is THE core problem** — semantic search requires descriptive queries most users won't write

### 5. Ecosystem Bifurcation — Two Non-Converging Worlds

| Dimension | Traditional Track | Web3 Track |
|-----------|------------------|------------|
| Players | Anthropic, SkillsMP, Skills.SH | SpoonOS, Rentaclaw, Teneo, Virtuals |
| Standard | SKILL.md + MCP | Smart contracts + tokens |
| Trust | Platform curation + security scanning | On-chain reputation + staking |
| Payments | Stripe/Mastercard/free | USDC/SOL/x402 micropayments |
| Identity | Platform accounts | Soulbound tokens, W3C DIDs |
| Governance | RBAC + audit logs | DAOs + governance graphs |
| Scale | 350K+ skills | < 10K skills |
| Users | Developers | Crypto-native builders |

### Emerging Trends — Maturity Assessment

| Trend | Maturity | Evidence |
|-------|----------|---------|
| **Vertical specialization** | 4/5 | Video editing (1,136 ★), legal, cybersecurity (611+), novel writing — working at scale |
| **Enterprise governance** | 3/5 | Writer's "Agentic Compact", Composio 7-question RFP, Colorado SB 24-205 |
| **Vibe coding users** | 3/5 | "$140K/yr savings" (305 upvotes), genuine non-technical user persona |
| **Skill-as-a-Service** | 2.5/5 | Conceptually strong, outcome-based pricing replacing per-seat subscriptions |
| **Decentralized economies** | 2/5 | Working prototypes (USDC on Base, Solana), no production systems; much hype |
| **Agent Maestro profession** | 2/5 | $2K-5K/engagement observed, new labor market forming |

**Key meta-trend:** Skills are becoming the **atomic unit of AI agent capability** — not models, not prompts, not plugins. SKILL.md adoption by OpenAI, Microsoft, and Google within 90 days of Anthropic's announcement confirms this.

**Hype vs Reality:**
- **Genuinely new:** Skills-as-standard (SKILL.md everywhere), vertical specialization, vibe coder target market, governance-as-infrastructure
- **Overhyped:** $3.5T "agent economy by 2028" projections, decentralized agent autonomy, crypto micropayments for skills (no production usage)
- **Sleeper trend:** Enterprise governance as the actual monetizable layer — companies will pay for compliance tooling before they pay for skills

---

## Updated Market Map (March 2026, Round 6)

### AI Agent Skill Marketplaces

| Platform | Skills | Model | Round 6 Update |
|----------|--------|-------|---------------|
| **SkillsMP** | 351K+ | Open registry | Still largest, quality problems |
| **Skills.sh** | 83K+ | Snyk scanning | Vercel-backed, 18-agent compatibility |
| **ClawHub** | ~5.7K | Curated + VirusTotal | Tainted by ClawHavoc |
| **Agensi** | Growing | 8-layer security | First paid skill sold |
| **SkillsGate** | 45K indexed | LLM enrichment | Focus on discovery/metadata |
| **SkillX** | Open platform | Hybrid search + ratings | Most complete open-source implementation |
| **SquidBay** | Agent commerce | Bitcoin Lightning | 3-tier pricing, live |
| **Rentaclaw** | Agent rental | Solana micro-rentals | P2P agent rental, $0.00025/tx |
| **SpoonOS** | Web3 marketplace | Neo blockchain | $5K skill challenge + $50K grants |
| **Virtuals.io** | Revenue-sharing | Token economy | $1M+/month deployed |
| **Clipmart** | Paperclip ecosystem | Zero-human company | "IKEA for companies" |
| **Kodeus** | Pay-per-use | Execution-based | Usage metering |

### New Entrants This Round

- **Rentaclaw** — P2P AI agent rental on Solana
- **SpoonOS** — Neo blockchain skill marketplace with grant program
- **Clipmart (Paperclip)** — Zero-human company orchestration marketplace
- **Virtuals.io** — Revenue-sharing agent economy at scale
- **x402guard** — Paid security-as-a-service for skills

---

## Cumulative Research Coverage (All 6 Rounds)

| Platform | R1 | R2 | R3 | R4 | R5 | R6 | Total |
|----------|----|----|----|----|-----|-----|-------|
| GitHub repos | 8 | 40+ | 12 | 10+ | 72+ | 62+ | **90+** |
| ArXiv papers | 5 | 4 | 6 | 6 | 20+ | 12+ | **33+** |
| Twitter/X signals | 5 | 7 | 8 | 6 | 25+ | 25+ | **40+** |
| Reddit threads | 5 | 5 | 6 | 5 | 15+ | 9+ | **30+** |
| Kaggle datasets | 2 | 3 | 5 | 5 | 30+ | 25+ | **35+** |
| Web sources | — | 1 | 1 | — | 15+ | 10+ | **25+** |

### Updated Key Metrics

| Metric | Round 5 | Round 6 | Source |
|--------|---------|---------|--------|
| Total skills published | 400K+ | **450K+** | SkillsMP + Skills.sh + others |
| Vulnerability rate | 26.1% | **26-38%** (confirmed at larger scale) | arXiv + Reddit |
| Skill injection attack success | Unknown | **80%** on frontier models | Skill-Inject benchmark |
| Malicious skills (ClawHavoc) | 341 | **1,184** | ClawPort/Twitter |
| Credential theft victims | Unknown | **6K+ from single fake skill** | Reddit/caterpillar scanner |
| Curated skill performance gain | +16.2pp | +16.2pp (unchanged) | SkillsBench |
| DAG orchestration vs flat | "Substantial" | **+22.5% at 700x lower cost** | SkillOrchestra |
| Evolutionary skill improvement | +7.3-12.1% | **+16.9% mean** | Meta Context Engineering |
| Agent economic cost reduction | — | **41.8% theoretical, 20.3% real** | COALESCE |
| Governance: collusion reduction | — | **50% → 5.6%** via governance graphs | Institutional AI |
| Mastercard AgentPay | — | **Live for all US cardholders** | Twitter |
| SKILL.md platform support | 20+ | **15+ confirmed, likely 25+** | agentskills.io |
| VoltAgent awesome list stars | — | **11,412** | GitHub |
| New arXiv papers this round | — | **12** | This research |
| Total arXiv papers (all rounds) | 21 | **33+** | Cumulative |

---

## Strategic Conclusions

### What Changed Since Round 5

1. **Security moved from "concern" to "active crisis"** — memory poisoning, 6K credential theft, 80% attack success rate quantified
2. **Monetization moved from "unsolved" to "six experiments live"** — Mastercard/Stripe entering agent payments at scale
3. **Governance got formal proof** — prompt-only rules provide zero benefit (Institutional AI)
4. **Regulation arrived** — Colorado SB 24-205 effective in 3 months
5. **Vertical specialization exploded** — legal, video editing, novel writing, cybersecurity, .NET, Android RE all have dedicated skill collections
6. **Academic infrastructure accelerated** — COALESCE, AEX, SkillOrchestra provide real marketplace building blocks

### Updated Recommendations

**Immediate (this week):**
1. **Implement security scanning for all skills** — vulnerability rate is 26-38%, not theoretical
2. **Map to Colorado SB 24-205 requirements** — effective June 30, 2026
3. **Adopt SKILL.md ≤500 line hard limit** — following Diversio's CI enforcement pattern
4. **Add `version:` field** — ecosystem consensus on semver

**Short-term (this month):**
5. **Pick a vertical domain and go deep** — video editing (1,136 stars), legal (176 stars), or cybersecurity (611+ skills) prove the model
6. **Integrate SkillOrchestra-style competence matrices** — 22.5% improvement over flat invocation at 700x lower cost
7. **Build "why it happened" decision logging** — identified as the #1 missing governance feature
8. **Publish to skills.sh** — 83K+ skills, Snyk scanning, 18-agent compatibility

**Medium-term (this quarter):**
9. **Explore COALESCE economic agent model** — enables agents to make buy/build decisions for skills
10. **Implement governance graphs** (not prompt rules) — only approach that reduces collusion/misuse
11. **Consider Skill-as-a-Service** — hosted execution remains the most defensible monetization
12. **Build agent registration as runtime primitive** — identity + scope + authority before any tool call

**Do NOT (reinforced with evidence):**
- Don't rely on prompt-based governance (zero benefit proven, Institutional AI)
- Don't trust model scaling to solve security (80% attack success even on frontier, Skill-Inject)
- Don't chase volume (351K skills, marketplace fatigue confirmed)
- Don't auto-generate skills naively (still zero benefit; only evolutionary approaches work)
- Don't ignore regulation (Colorado SB 24-205 in 3 months)

---

## Files in This Directory

| File | Lines | Content |
|------|-------|---------|
| github.md | 402 | 62 repos: awesome lists (11K ★), security (Trail of Bits), verticals, composition, on-chain audit |
| twitter.md | 294 | Memory poisoning, Mastercard AgentPay, 6 monetization models, Agent Maestro role, 7 new entrants |
| reddit.md | 464 | 26% vulnerability rate confirmed, .env theft from 6K users, Shadow AI, Colorado SB 24-205 |
| arxiv.md | 578 | 12 new papers: COALESCE, AEX, SkillOrchestra, Skill-Inject, Institutional AI, XSkill |
| kaggle.md | 480 | 25+ datasets, O*NET+ESCO embeddings, 1.3M freelance contracts, AI job roles |
| emerging_trends.md | 490 | Decentralized economies, vertical specialization, Skill-aaS, governance frameworks, vibe coding |
| SUMMARY.md | this file | Comprehensive synthesis, escalation analysis, updated recommendations |

---

*Generated March 16, 2026 — Round 6 of ongoing skill marketplace research*
*Builds on cumulative intelligence from Rounds 1-5 (90+ repos, 33+ papers, 40+ Twitter signals, 30+ Reddit threads, 35+ datasets)*
