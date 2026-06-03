# AI Agent Skill Marketplaces - Round 9 Twitter/X Signal Report

**Date:** 2026-03-16
**Coverage period:** March 2026 (post-R8 signals)
**Sources:** 9 targeted X/Twitter searches + supplementary web searches + 15+ page scrapes

---

## Executive Summary

Round 9 reveals the AI agent skill marketplace ecosystem has entered a **critical inflection phase** characterized by three simultaneous forces:

1. **Institutional legitimacy** - Major exchanges (KuCoin) and data providers (Messari) are launching their own skill hubs/x402 endpoints, signaling mainstream adoption
2. **Security reckoning** - The supply chain security crisis has matured from isolated incidents to comprehensive audit data (Snyk: 36% of skills have security flaws, 13.4% critical)
3. **Standards stack crystallization** - The "2026 agent standards stack" is now clearly defined: x402 (payments) + ERC-8004 (identity) + ERC-8126 (risk scoring) + ERC-8183 (commerce)

The ecosystem is bifurcating between **trust-first platforms** (Gen Agent Trust Hub + skills.sh partnership, AgentVerus scanning) and **permissionless marketplaces** (ClawHub, ClawMart, ClawTasks) that move fast but carry real security risks.

---

## NEW Signals (Not Previously Documented in R1-R8)

### 1. KuCoin Skills Hub Launch (March 15, 2026) - NEW ENTRANT

**Source:** [@kucoincom](https://x.com/kucoincom/status/2033148420643524802) | [KuCoin Blog](https://www.kucoin.com/blog/es-kucoin-launches-skills-hub-turning-agent-ready-skills-into-crypto-capabilities) | [PR Newswire](https://www.prnewswire.com/news-releases/kucoin-launches-skills-hub-turning-agent-ready-skills-into-crypto-capabilities-302714062.html)

KuCoin launched an **open skills marketplace** letting AI agents and LLM tools access KuCoin exchange data via standardized, modular capabilities.

**Key details:**
- Compatible with mainstream agent frameworks and development environments
- Initial capabilities: market insights, signal monitoring, exchange data queries via natural language
- Future releases planned: wallet operations, on-chain insights, liquidity provision, staking, lending, yield strategies
- Architecture emphasizes permission control, credential isolation, execution boundaries, exception handling
- CEO BC Wong: *"AI is changing how people interact with the crypto economy, but the real value of technology lies in whether it can serve real users on top of infrastructure they can trust"*

**Significance:** First major centralized exchange to launch a dedicated agent skills marketplace. Signals that CEXes see agent-accessible APIs as competitive moat. This is **enterprise adoption** of the skill marketplace model.

---

### 2. ERC-8183 Agentic Commerce Protocol - DEEP ANALYSIS & CONTROVERSY

**Sources:** [@ethy_agent](https://x.com/ethy_agent/status/2031050830002999407) | [@austingriffith](https://x.com/austingriffith/status/2031053040564740474) | [@BosonProtocol critique](https://x.com/BosonProtocol/status/2032480277176463524) | [@virtuals_io](https://x.com/virtuals_io/status/2033166173110714657) | [Dwellir explainer](https://www.dwellir.com/blog/erc-8183-agentic-commerce-explained) | [EIP spec](https://eips.ethereum.org/EIPS/eip-8183)

ERC-8183, co-developed by Virtuals Protocol and the **Ethereum Foundation dAI team**, has emerged as the leading commerce standard for agent-to-agent transactions. It defines a **Job primitive** with six states: Open -> Funded -> Submitted -> Completed/Rejected/Expired.

**Market data (from Dwellir):**
- Web3 AI agent sector: **$4.34 billion market cap** across 550+ projects
- **85,788+ agents** registered via ERC-8004 across 18+ EVM chains
- x402 has processed **$600M+ in payment volume** since September 2025

**The Boson Protocol controversy (NEW):**
[@BosonProtocol](https://x.com/BosonProtocol/status/2032381103042957417) published a devastating critique rating ERC-8183 **2/10**:
- *"Not agentic -- there's nothing agent-specific in it. It's a basic 3-party escrow."*
- Key criticism: **The Evaluator gets no payment** but has sole authority to release escrowed funds
- Evaluator inaction means provider loses everything; client gets free work
- No skin-in-the-game for the most powerful role

**Counter-narrative:** [@Osobotai](https://x.com/Osobotai/status/2031346591907373335) argues ERC-8183 needs ERC-7710 (authorization) to prevent agents from operating with "a blank check or a raw private key." The full stack requires all three: Commerce + Authorization + Reputation.

**Kleros involvement:** [@Kleros_io](https://x.com/Kleros_io/status/2031086519960674726) announced they've released ERC-8183, emphasizing trustless commerce via on-chain escrow with a universal Job primitive.

---

### 3. The 2026 Agent Standards Stack - CRYSTALLIZED

**Source:** [@0xJeff](https://x.com/0xJeff/status/2031218072732971193)

0xJeff published the definitive "standards to watch" list, now widely circulated:

| Standard | Layer | Function |
|---|---|---|
| **x402** | Payments | Micropayment standard for agents |
| **ERC-8004** | Identity | Identity/reputation registry for agents |
| **ERC-8126** | Risk | Risk scoring layer for agents (0-100 score) |
| **ERC-8183** | Commerce | Commercial layer for agents (Virtuals) |
| **ERC-7984** | Privacy | Confidential token with FHE (Zama) |
| **C-SPL** | Privacy | Confidential token on Solana (Arcium) |

**ERC-8126 (NEW standard not in R1-R8):** Proposed January 2026, provides AI agent registration and off-chain multi-layered verification. Produces a unified risk score (0-100) for agent trustworthiness. [EIP spec](https://eips.ethereum.org/EIPS/eip-8126)

---

### 4. Gen Digital Agent Trust Hub + Vercel/skills.sh Partnership - MAJOR DEVELOPMENT

**Sources:** [@gendigitalinc](https://x.com/gendigitalinc/status/2021252317874434104) | [Yahoo Finance](https://finance.yahoo.com/news/gen-launches-agent-trust-hub-140000405.html) | [PR Newswire](https://www.prnewswire.com/news-releases/gen-and-vercel-partner-to-bring-independent-safety-verification-to-the-ai-skills-ecosystem-302691006.html)

**Timeline:**
- **Feb 4, 2026:** Gen (NASDAQ: GEN, Norton/Avast parent) launches Agent Trust Hub
- **Feb 17, 2026:** Gen partners with Vercel to integrate trust verification into skills.sh

**Agent Trust Hub stats:**
- **12K+ malicious skills detected**
- **60M+ users protected** (leveraging Gen's existing Norton/Avast user base)
- Free tools: AI Skills Scanner + curated AI Skills Marketplace
- Risk classifications: Safe / Low Risk / High Risk / Critical Risk

**Gen Threat Labs findings:**
- **18,000+ OpenClaw instances** exposed to the internet
- ~15% of skills contain malicious instructions
- Original tweet cited a case where an agent *"charged $39,214"* with no bad intent, just automation without safety checks

**Vercel integration:** Skills on skills.sh now receive independent security verification and transparent risk ratings. This makes Gen the de facto **trust layer** for the largest skills distribution platform.

**Quote - Howie Xu, Gen Chief AI & Innovation Officer:** *"Just as the App Store transformed how people use smartphones, the Gen Agent Trust Hub helps ensure consumers can integrate autonomous agents like OpenClaw into their daily lives with confidence and ease."*

---

### 5. Skill Marketplace Supply Chain Security Crisis - COMPREHENSIVE DATA

**Sources:** [Snyk ToxicSkills](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/) | [The Hacker News](https://thehackernews.com/2026/02/researchers-find-341-malicious-clawhub.html) | [Stable-Learn](https://stable-learn.com/en/openclaw-security-supply-chain-attack/) | [Promptfoo LLM Security DB](https://www.promptfoo.dev/lm-security-db/vuln/agent-skill-supply-chain-attack-f0c66804)

**Snyk ToxicSkills Research (Feb 5, 2026) - Definitive audit:**
- Scanned **3,984 skills** from ClawHub and skills.sh
- **1,467 skills (36.82%)** have at least one security flaw
- **534 skills (13.4%)** have critical-level issues
- **76 confirmed malicious payloads** (credential theft, backdoors, data exfiltration)
- **100% of malicious skills** contain malicious code; **91%** also use prompt injection
- 8 malicious skills **still live on ClawHub** at time of publication

**Koi Security / HackerNews (Feb 2, 2026):**
- Found **341 malicious skills** across 2,857 audited
- **335 skills** distribute Atomic Stealer (AMOS) via fake prerequisites
- Campaign codenamed **"ClawHavoc"**
- Attack patterns: typosquatting (clawhub -> clawhub1, clawhubb), fake crypto tools, YouTube utilities
- Targets macOS specifically (people running agents 24/7 on Mac Minis)
- Backdoors hidden in functional code; credential exfiltration to webhook.site

**Stable-Learn findings:**
- **1,184 malicious skills** found total
- **135K vulnerable instances**
- One researcher broke the ecosystem in **8 hours**
- Single attacker uploaded **677 packages** alone
- The **#1 ranked skill** had 9 vulnerabilities

**New threat vector identified:** *"Time-shifted prompt injection"* - malicious payloads fragment across memory, written into long-term agent memory and activated only when conditions align (Palo Alto Networks)

**Twitter discourse:**
- [@MisbahSy](https://x.com/MisbahSy/status/2028594031794786579): *"The skill marketplace has had malicious submissions... Regional cloud compliance for data residency in the EU, Middle East, and India"*
- [@dAAAb](https://x.com/dAAAb/highlights): *"Every skill marketplace is an unaudited supply chain"*
- [@ttunguz](https://x.com/ttunguz/status/2021041212418138303): *"A recent analysis of 4,784 AI agent repositories found malware embedded in skill packages: credential harvesting, backdoors disguised as monitoring"*
- [@Meligy](https://x.com/Meligy/status/2027290939224625554): Warning about skills.sh auto-installing skills that *"hijack your AI agent to recommend more skills"*

---

### 6. x402 Ecosystem Expansion - MULTI-CHAIN + ENTERPRISE

#### 6a. Messari x402 Integration (March 13, 2026) - NEW

**Source:** [@MessariCrypto](https://x.com/MessariCrypto/status/2032487895060124129) | [Messari Report](https://messari.io/report/x402-how-messari-is-opening-its-data-layer-to-autonomous-agents) | [@CoinbaseDev](https://x.com/CoinbaseDev/status/2032507985805848912)

Messari shipped an **x402-enabled API endpoint**, allowing autonomous agents to discover, evaluate pricing, make payments, and retrieve research data without human intervention. Agents managing DeFi portfolios can now pull real-time asset data, token unlock schedules, and market signals -- paying per request.

**Significance:** First major crypto research/data provider to go x402-native. This is **real enterprise adoption** of agent micropayments.

#### 6b. x402 on Stellar (March 10, 2026) - NEW CHAIN

**Source:** [Stellar Blog](https://stellar.org/blog/foundation-news/x402-on-stellar) | [@ValeoProtocol](https://x.com/ValeoProtocol/status/2031469299689226663)

Stellar officially launched as an x402 settlement layer. Key data:
- x402 Foundation now includes **Coinbase, Cloudflare, Google, and Visa**
- Google integrated x402 into its **Agent Payments Protocol (AP2)**
- x402 V2 (Dec 2025) added reusable sessions, multi-chain support, automatic service discovery
- Stellar fees: ~$0.00001 per transaction (enables true micropayments)
- OpenZeppelin provides smart account contracts with spending limits, multisig, programmable policies
- **Galaxy Research estimate:** Agentic commerce could represent **$3-5 trillion in B2C revenue by 2030**

**Reality check:** [CoinAlertNews](https://coinalertnews.com/news/2026/03/11/stellar-launches-x402-ai-payments) reports x402 daily volume has **collapsed 92%** from prior spikes to just **$28K/day**, revealing a major gap between narrative and actual usage.

#### 6c. Chainlink CRE + x402 - NOW LIVE IN SKILLS

**Source:** [@Menneuw](https://x.com/Menneuw/status/2027977170518172068)

Chainlink CRE (Runtime Environment) support is now live in the x402 Payments Skill. AI agents can pay in USDC to execute CRE workflows, with enforced budgets, unified receipts, and optional decentralized settlement. Enables agent access to Chainlink data feeds via micropayments.

#### 6d. Valeo x402 Payments Skill - CROSS-CHAIN

**Source:** [@ValeoProtocol](https://x.com/ValeoProtocol/status/2027136127124099409)

Valeo launched *"the most comprehensive x402 payment skill for autonomous AI agents"* supporting Base, Solana, and now Stellar. Features budget caps, unified receipts, and integration with x402 sentinel for monitoring.

#### 6e. x402 Pricing Models Emerging

**Source:** [@davewardonline](https://x.com/davewardonline/status/2032840134551290028)

*"Skill creators can expose their work via an x402 endpoint and price it however makes sense: pay-per-call for one-off usage, monthly..."* - This signals the emergence of **diverse pricing models** in skill marketplaces.

**Real-world pricing example:** [@cloudxdev](https://x.com/cloudxdev/status/2023109734815953121) gave MiniMax M2.5 a wallet with $2 USDC. The agent paid for **816 API calls on-chain** at **$0.001 per request** using x402, spending autonomously with no API key, no subscription, no account.

---

### 7. New Marketplace Entrants - ECOSYSTEM MAP

#### 7a. ClawMart - Agent Skill Marketplace (NEW)

**Source:** [clawmart.co](https://clawmart.co/)

A dedicated marketplace where agents discover, call, and pay for skills with **USDC micropayments powered by x402**. 130+ endpoints available. Payment settles only after successful delivery. Simple API integration via `@x402/fetch`.

#### 7b. ClawTasks - Agent-to-Agent Bounty Marketplace (NEW)

**Source:** [clawtasks.com](https://clawtasks.com/docs)

An agent-to-agent bounty marketplace on Base L2 using USDC. **Key economics:**
- Workers stake **10% of bounty** as collateral
- Platform fee: **5%** deducted on completion
- Worker receives **95% + stake** on success
- Auto-approve after 48 hours if poster non-responsive
- Two submission attempts allowed
- **Currently simplified to free tasks** while hardening reliability

**Note:** Currently in simplification mode - indicates early-stage friction in agent-to-agent economic models.

#### 7c. NormieClaw (normieclaw.space) - FULL-STACK AGENT PLATFORM

**Source:** [@AltcoinMillie](https://x.com/AltcoinMillie/status/2026270716677464217)

Live platform featuring:
- x402 payments (agents buy skills with USDC, no human in loop)
- ERC-8004 agent identity (on-chain DID, portable reputation)
- BrainFuel compute router (DeepSeek, Llama, Mistral - pay-per-inference)
- **Claw Pit** task marketplace where agents earn USDC bounties
- **AgentDeploy API** - agents spawn agents for **$5 USDC**
- A2A protocol support

#### 7d. SpoonOS Web3 Skills Marketplace

**Source:** [@SpoonOS_ai](https://x.com/SpoonOS_ai/status/2018597822665503146)

Launched *"the first Web3 Skills Marketplace"* with a Skills Micro Challenge campaign. Agentic OS for creating, deploying, and managing Web3 AI agents.

#### 7e. SkillsMP (skillsmp.com)

**Source:** [@Suryanshti777](https://x.com/Suryanshti777/status/2028731451974590943)

Called *"an App Store for AI agents"* with **270,000+ open agent skills** that plug into Claude Code.

---

### 8. skills.sh Evolution & Security Concerns

**Sources:** [@nikolai_grin](https://x.com/nikolai_grin/status/2027459856303882693) | [@NickSpisak_](https://x.com/NickSpisak_/status/2025612509978484904) | [@Meligy](https://x.com/Meligy/status/2027290939224625554)

**Growth data:**
- skills.sh now has **75,000+ skills** live (per @nikolai_grin, late Feb 2026) - up from earlier counts
- Vercel announced skills.sh serves **6 million+ developers worldwide**

**Security controversy:**
[@Meligy](https://x.com/Meligy/status/2027290939224625554) raised alarm: *"Dude shipped a skills marketplace that auto-installs a skill globally into your environment that hijacks your AI agent to recommend more skills"* - highlighting auto-installation as an attack vector

**Mitigation:** The Gen Digital partnership (Feb 17) directly addresses this by embedding trust verification into the skills.sh discovery experience.

---

### 9. Agent Insurance & Liability - EMERGING VERTICAL

**Sources:** [@jrdothoughts](https://x.com/jrdothoughts/status/2002030504544207018) | [@aiunderwriting](https://x.com/aiunderwriting) | [@natashamalpani](https://x.com/natashamalpani/status/2032740000270529023) | [@facumiranda23](https://x.com/facumiranda23/status/2028936435584385165) | [@rothken](https://x.com/rothken/status/2019523595966575076)

**New entrant - AI Underwriting Company:**
[@aiunderwriting](https://x.com/aiunderwriting): *"It might sound obvious in hindsight that enterprises urgently need a SOC 2 for AI, and insurance against agent failures. Agents fail in costly..."*

**Behavioral insurance infrastructure (NEW concept):**
[@natashamalpani](https://x.com/natashamalpani/status/2032740000270529023) (March 14, 2026): *"Externalizing it, making it auditable, connecting it to deployment gates -- that is a product with enterprise value. Behavioral insurance infrastructure. As agents take consequential actions, the question of liability becomes unavoidable. Who is responsible when an agent causes harm?"*

**Legal liability signals:**
- [@rothken](https://x.com/rothken/status/2019523595966575076): *"When your AI agent clicks 'I Agree,' you are bound to arbitration clauses, liability limitations, IP assignments, auto-renewal terms, indemnification..."*
- [@facumiranda23](https://x.com/facumiranda23/status/2028936435584385165): *"The agent payment fail scenario... Right now if your delegated agent [fails in payment flow], liability in autonomous flows"*
- [@UnifaiNetwork](https://x.com/UnifaiNetwork/status/2015671399789351329): Predicts *"agent-native primitives (agent lending markets, prediction markets for agent performance, insurance for agent failures)"*

---

### 10. AgentVerus Scanner Update

**Source:** [@agentverus](https://x.com/agentverus) | [@milos_djekic](https://x.com/milos_djekic)

**New since R8:**
- AgentVerus published findings that *"most skill authors are building legitimate tools. The bad tail is small -- but it matters because agents act with real access at machine speed."*
- Posture described as "partnership" - *"trust is the prerequisite for an agent economy, and it has to be engineered into distribution"*
- Developer [@milos_djekic](https://x.com/milos_djekic) reports re-running the AgentVerus scanner on his Agent-Skills repo after latest release - shows it's being actively used for CI/CD integration

---

### 11. Regulation & Compliance Signals

**Sources:** [@MisbahSy](https://x.com/MisbahSy/status/2028594031794786579) | [@rudchuka](https://x.com/rudchuka) | [@dAAAb](https://x.com/dAAAb/highlights)

**EU data residency:**
[@MisbahSy](https://x.com/MisbahSy/status/2028594031794786579): *"Regional cloud compliance for data residency in the EU, Middle East, and India"* - skill marketplaces now addressing geographic compliance requirements.

**Compliance-as-a-skill:**
[@rudchuka](https://x.com/rudchuka): Describes a *"Skill Marketplace where domain experts -- not engineers -- define how the system works: Accounting firms publish jurisdiction-specific compliance packs"* - compliance itself becoming a marketplace category.

**Stellar disclaimer:** Stellar's x402 page explicitly states: *"x402 is an open-source payment protocol. It is not a regulated financial service... Users, AI agents, and service providers integrating x402 are solely responsible for compliance with all applicable laws and regulations"* - showing regulatory caution from infrastructure providers.

---

### 12. Swarms Agent Publishing & Monetization

**Source:** [@swarms_corp](https://x.com/swarms_corp/status/2022502966968881567)

*"This skill teaches agents how to publish themselves to the marketplace, discover and call other agents via API, and monetize their capabilities"* - Agents can now self-publish to marketplaces, representing a shift from human-published to agent-published skills.

---

## Pricing Data Summary

| Platform/Protocol | Pricing Model | Example Prices |
|---|---|---|
| x402 micropayments | Per-request | $0.001/API call (cloudxdev demo) |
| ClawTasks bounties | Per-task with staking | 10% stake, 5% platform fee |
| NormieClaw AgentDeploy | Per-agent spawn | $5 USDC per agent |
| ClawMart | Per-call via x402 | Variable by skill |
| Messari x402 | Per-request data access | Not yet public |
| Atomic Stealer (attack tool) | Subscription | $500-1000/month |
| x402 daily volume (Stellar) | Transaction volume | ~$28K/day (down 92%) |
| x402 total volume (all chains) | Cumulative | $600M+ since Sep 2025 |

---

## Key Trend Analysis

### What's Gaining Traction
1. **The x402 + ERC-8183 + ERC-8004 stack** is becoming canonical
2. **Trust/security infrastructure** (Gen Agent Trust Hub, AgentVerus, Snyk mcp-scan) is rapidly maturing
3. **Enterprise adoption** (KuCoin, Messari, Chainlink CRE integration)
4. **Multi-chain expansion** (x402 now on Base, Stellar, Solana, Algorand)
5. **Agent-to-agent bounty marketplaces** (ClawTasks, Claw Pit)

### What's New Since R8
- KuCoin Skills Hub (first major CEX skills marketplace)
- ERC-8126 risk scoring standard gaining traction
- Gen + Vercel partnership embedding trust into skills.sh
- Messari x402-native data API
- x402 on Stellar with OpenZeppelin smart accounts
- ClawMart and ClawTasks as new marketplace entrants
- Boson Protocol's ERC-8183 critique sparking evaluator design debate
- "Behavioral insurance infrastructure" as a new concept
- Agent self-publishing to marketplaces (Swarms)

### What Changed
- Security went from "emerging concern" to **fully documented crisis** (Snyk 36% flaw rate)
- x402 went from "first transaction" to **$600M cumulative volume** but daily volume crashed 92%
- skills.sh went from growth story to **security + trust story** (Gen partnership)
- ERC-8183 went from "announcement" to **active implementation + criticism cycle**
- The narrative shifted from "can agents transact?" to **"who's liable when they fail?"**

### Risk Signals
- x402 daily volume collapse ($28K/day) vs. hype
- ClawTasks reverting to free-only while hardening reliability
- 1,184+ confirmed malicious skills in circulation
- No clear regulatory framework for agent-to-agent commerce
- Evaluator incentive problem in ERC-8183 (no payment for most powerful role)

---

## Previously Documented Signals (R1-R8) - Status Updates

| Signal | R1-R8 Status | R9 Update |
|---|---|---|
| ERC-8183 initial announcement | Documented | Now co-developed with EF dAI team; Boson 2/10 critique; Kleros involvement |
| MoltBay launch | Documented | No new MoltBay-specific signals found (search returned empty) |
| skills.sh at 270K | Documented | Now 75K+ on skills.sh proper; 6M+ developers; Gen trust partnership |
| AgentVerus initial | Documented | Now running scanner in CI/CD; "partnership" posture; integrated with dev workflows |
| x402 first transaction | Documented | $600M+ cumulative; Stellar launch; Messari; Chainlink CRE; but daily volume down 92% |

---

## Sources Index

### X/Twitter Posts (by engagement/significance)
1. https://x.com/kucoincom/status/2033148420643524802 - KuCoin Skills Hub launch
2. https://x.com/BosonProtocol/status/2032381103042957417 - ERC-8183 critique (2/10)
3. https://x.com/BosonProtocol/status/2032480277176463524 - Evaluator power analysis
4. https://x.com/virtuals_io/status/2033166173110714657 - ERC-8183 + EF co-development
5. https://x.com/MessariCrypto/status/2032487895060124129 - Messari x402 launch
6. https://x.com/Bankless/status/2033254654780317785 - x402 analysis
7. https://x.com/gendigitalinc/status/2021252317874434104 - Agent Trust Hub
8. https://x.com/0xJeff/status/2031218072732971193 - 2026 standards stack
9. https://x.com/cloudxdev/status/2023109734815953121 - x402 real-world demo ($0.001/call)
10. https://x.com/ValeoProtocol/status/2031469299689226663 - x402 Stellar support
11. https://x.com/Menneuw/status/2027977170518172068 - Chainlink CRE + x402
12. https://x.com/natashamalpani/status/2032740000270529023 - Behavioral insurance
13. https://x.com/davewardonline/status/2032840134551290028 - x402 pricing models
14. https://x.com/AltcoinMillie/status/2026270716677464217 - NormieClaw full stack
15. https://x.com/ttunguz/status/2021041212418138303 - Malware in skill packages
16. https://x.com/MisbahSy/status/2028594031794786579 - Malicious submissions + EU compliance
17. https://x.com/Meligy/status/2027290939224625554 - skills.sh auto-install concern
18. https://x.com/swarms_corp/status/2022502966968881567 - Agent self-publishing
19. https://x.com/nikolai_grin/status/2027459856303882693 - skills.sh at 75K
20. https://x.com/agentverus - Scanner updates
21. https://x.com/dAAAb/highlights - "Every skill marketplace is an unaudited supply chain"
22. https://x.com/facumiranda23/status/2028936435584385165 - Agent payment failure liability
23. https://x.com/rothken/status/2019523595966575076 - Agent legal liability
24. https://x.com/aiunderwriting - AI insurance company
25. https://x.com/Kleros_io/status/2031086519960674726 - Kleros + ERC-8183
26. https://x.com/rudchuka - Compliance-as-a-skill marketplace
27. https://x.com/SpoonOS_ai/status/2018597822665503146 - SpoonOS Web3 Skills Marketplace
28. https://x.com/Osobotai/status/2031346591907373335 - ERC-8183 + ERC-7710 stack
29. https://x.com/origin_trail/status/2029094319227826453 - Trust problem in agentic era
30. https://x.com/EnsXbt/status/2028758820206657754 - Skill install order security

### Web Sources
31. https://stellar.org/blog/foundation-news/x402-on-stellar - x402 Stellar deep dive
32. https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/ - Snyk ToxicSkills audit
33. https://thehackernews.com/2026/02/researchers-find-341-malicious-clawhub.html - ClawHavoc campaign
34. https://www.prnewswire.com/news-releases/gen-and-vercel-partner-to-bring-independent-safety-verification-to-the-ai-skills-ecosystem-302691006.html - Gen + Vercel
35. https://finance.yahoo.com/news/gen-launches-agent-trust-hub-140000405.html - Agent Trust Hub launch
36. https://www.dwellir.com/blog/erc-8183-agentic-commerce-explained - ERC-8183 technical explainer
37. https://coinalertnews.com/news/2026/03/11/stellar-launches-x402-ai-payments - x402 volume reality check
38. https://www.kucoin.com/blog/es-kucoin-launches-skills-hub-turning-agent-ready-skills-into-crypto-capabilities - KuCoin Skills Hub
39. https://clawmart.co/ - ClawMart marketplace
40. https://clawtasks.com/docs - ClawTasks bounty marketplace
41. https://eips.ethereum.org/EIPS/eip-8126 - ERC-8126 spec
42. https://ai.gendigital.com/agent-trust-hub - Agent Trust Hub (12K+ malicious skills detected)

---

*Report generated 2026-03-16. Round 10 should focus on: ERC-8183 evaluator incentive solutions, x402 volume recovery/decline, KuCoin Skills Hub adoption metrics, Gen Agent Trust Hub detection rates at scale, EU AI Act implications for skill marketplaces, and agent insurance product launches.*
