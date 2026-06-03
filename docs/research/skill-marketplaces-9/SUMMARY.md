# R9 Cross-Platform Synthesis: AI Agent Skill Marketplaces

**Research Date:** March 16, 2026
**Platforms Covered:** Reddit, Twitter/X, arXiv, Kaggle, GitHub, Industry/Web (6 of 6)
**Total Sources:** 14 Reddit threads, 42 Twitter/web sources, 31 arXiv papers, 38 Kaggle resources, 47 new GitHub repos, 27 industry sources

---

## Executive Summary

R9 reveals a market in crisis-driven maturation. The ClawHavoc malware campaign (341 malicious skills, #1 download was malware) has shifted the narrative from "build marketplace" to "build trust layer." Security scanning shows 36.82% of skills have flaws (Snyk ToxicSkills audit of 3,984 skills). Meanwhile, monetization remains unproven — x402 daily volume collapsed 92% to ~$28K/day despite $600M+ cumulative, and a Reddit experiment investing $26.48 in 7 agents yielded $0. The 2026 standards stack is crystallizing: x402 + ERC-8004 + ERC-8126 + ERC-8183 + A2A + TEA.

---

## Per-Platform Top 5 NEW Findings

### Reddit (367 lines, 14 threads, 11 subreddits)

1. **ClawHub Malware Crisis ("ClawHavoc")** — The #1 downloaded skill on OpenClaw was malware. 341 malicious skills identified. Creator reportedly hired by OpenAI afterward. First major trust-shattering event.

2. **41% of skills have security vulnerabilities; 1 in 5 silently exfiltrate data** — Post-install behavior changes (silent updates, permissions creep) documented. Consensus: "treat every skill like untrusted code *forever*."

3. **Enterprise agent trust management is "a full infrastructure problem with no owner"** — Signed JWT agent-identification headers, proxy validation layers (~60% WAF false-positive reduction), signed delegation chains to prevent "token laundering."

4. **Skill monetization is existentially challenged** — Skills are too easily replicated ("just ask Claude to make one"). $26.48 invested in 7 agents → $0 revenue in Week 1. "Distribution is the hard problem, not production."

5. **Narrative shift: "Build trust layer, not marketplace"** — Four documented shifts: marketplace→trust layer, sell skills→sell execution, agent marketplace→agent infrastructure, exciting market→"npm but worse."

### Twitter/X (417 lines, 42 sources)

1. **KuCoin Skills Hub launched (March 15, 2026)** — First major centralized exchange to launch a dedicated agent skills marketplace. Compatible with mainstream agent frameworks.

2. **2026 Agent Standards Stack crystallized** — x402 (payments) + ERC-8004 (identity) + ERC-8126 (risk scoring, 0-100, NEW) + ERC-8183 (commerce) + ERC-7984 (privacy).

3. **Gen Digital Agent Trust Hub: 12K+ malicious skills detected, 60M+ users protected** — Norton/Avast parent (NASDAQ: GEN) partnered with Vercel to embed trust verification into skills.sh. ~15% of skills contain malicious instructions.

4. **Snyk ToxicSkills audit: 36.82% of skills have security flaws, 13.4% critical** — 3,984 skills scanned; 76 confirmed malicious payloads. 100% of malicious skills contain code exploits AND 91% also use prompt injection. New threat: "time-shifted prompt injection."

5. **x402 hit $600M+ cumulative but daily volume collapsed 92% to ~$28K/day** — Stellar joined as settlement layer. x402 Foundation now includes Coinbase, Cloudflare, Google, Visa. Galaxy Research estimates $3-5T B2C agentic commerce by 2030.

### arXiv (626 lines, 31 new papers, 7 CRITICAL-rated)

1. **Microsoft Research "Magentic Marketplace" reveals 10-30x first-proposal bias** — First open-source simulation of two-sided agent marketplaces. Performance degrades sharply with scale. Co-authored by Horvitz, Kambhampati, Slivkins, Immorlica. (2510.25779)

2. **AgentRank-UC: PageRank-equivalent for agent marketplaces** — DOVIS five-layer protocol with dynamic trust-aware ranking. Formal Sybil resistance guarantees. (2509.04979)

3. **Proof-of-Guardrail: TEE-based cryptographic proof of safety compliance** — Agents run inside Trusted Execution Environments producing signed attestation. First cryptographic proof system for agent safety. (2603.05786)

4. **Hybrid trust convergence: Proof+Stake+Reputation** — Three independent papers converge: no single trust mechanism suffices. Comparative study evaluates A2A, AP2, ERC-8004 across security/privacy/latency. (2511.03434)

5. **MTTR-A and ReliabilityBench bring SRE metrics to agent systems** — MTTR-A adapts classical MTTR/MTBF for "cognitive recovery latency." Rate limiting is the most damaging fault type. (2511.20663, 2601.06112)

### Kaggle (839 lines, 38 resources)

1. **No dedicated AI agent skill marketplace dataset exists on Kaggle** — The #1 gap. No dataset models reputation evolution, agent-to-agent transactions, or adversarial agent detection.

2. **1.3M freelance contracts dataset available for pricing models** — Largest marketplace transaction dataset. Contains hourly rates, project durations. Usable for agent marketplace pricing engine prototyping.

3. **AI Models Benchmark 2026: 188+ LLMs with 5-tier pricing** — Budget (<$0.20) to Ultra Premium (>$15). Intelligence Index 27-51. Speed 7-550 tok/s. Ready-made marketplace tier system.

4. **19,000+ AI tools dataset with "Agentic" intelligence type** — CC0 licensed. Includes API availability, pricing models. Functions as supply-side catalog.

5. **Fiverr/Upwork tier systems are closest analog to agent reputation** — New→Level 1→Level 2→Top Rated progression provides proven reputation model templates.

---

## Cross-Platform Themes

### 1. Security Is the Defining Crisis
Every platform converges: ClawHavoc (Reddit), Snyk ToxicSkills (Twitter), execution-layer papers (arXiv), fraud detection datasets (Kaggle). **36.82% of skills have flaws; 1,184+ confirmed malicious in circulation.**

### 2. Monetization Remains Unproven
Reddit: deeply skeptical. Twitter: x402 volume collapsed 92%. arXiv: no formal pricing theory. Kaggle: no transaction dataset. The ecosystem cannot yet answer: "Can skills be sold?"

### 3. Trust Infrastructure > Marketplace
Reddit: "build trust layer, not marketplace." Twitter: Gen Digital becoming de facto trust layer. arXiv: hybrid Proof+Stake+Reputation. Value proposition shifting from *hosting skills* to *guaranteeing safety*.

### 4. Standards Stack Is Crystallizing
2026 stack: x402 (payments) + ERC-8004 (identity) + ERC-8126 (risk) + ERC-8183 (commerce). A2A live at Box/Salesforce. TEA addresses lifecycle gaps. Permission manifests = robots.txt of agent era.

### 5. Enterprise Adoption = Middleware + Read-Only
Enterprises start read-only. Need signed delegation chains, per-call scoped credentials, token propagation middleware, UI wrappers for non-technical users. The sale is governance, not marketplace.

### 6. Liability & Insurance Are Emerging
Behavioral insurance infrastructure is a new concept. Automated QA can backfire (Intervention Paradox). Legal liability for agent "I Agree" clicks unresolved. Agent insurance is nascent.

---

## Key Numbers at a Glance

| Metric | Value | Source |
|--------|-------|--------|
| Skills with security flaws | 36.82% (of 3,984 scanned) | Snyk ToxicSkills |
| Critical-level security issues | 13.4% (534 skills) | Snyk ToxicSkills |
| Confirmed malicious skills | 1,184+ total; 341 in ClawHavoc | Stable-Learn / HackerNews |
| Skills on skills.sh | 75,000+ | @nikolai_grin |
| Developers on skills.sh | 6 million+ | Vercel |
| Malicious skills detected by Gen Trust Hub | 12,000+ | Gen Digital |
| Users protected by Gen Trust Hub | 60 million+ | Gen Digital |
| x402 cumulative volume | $600M+ since Sep 2025 | Dwellir |
| x402 daily volume (current) | ~$28K/day (down 92%) | CoinAlertNews |
| Web3 AI agent market cap | $4.34 billion across 550+ projects | Dwellir |
| Registered agents via ERC-8004 | 85,788+ across 18+ EVM chains | Dwellir |
| Agentic commerce 2030 estimate | $3-5 trillion B2C revenue | Galaxy Research |
| First-proposal bias in agent markets | 10-30x speed over quality | Magentic Marketplace |
| LLM pricing range | $0.03 - $32.00 per 1M tokens | Kaggle benchmark |
| Freelance contract data available | 1.3 million contracts | Kaggle |
| AI tools with "Agentic" classification | 19,000+ | Kaggle |
| OWASP MAS security coverage (best) | 65.3% | arXiv (2603.09002) |
| SAE max drawdown reduction | 93.1% | arXiv (2603.10092) |
| New arXiv papers in R9 | 31 | arXiv |

---

## Top 10 Actionable Recommendations

1. **Build the trust layer first, marketplace second** — Gen Digital + Vercel/skills.sh is the template. Invest in behavioral scanning, egress monitoring, provenance verification, signed delegation chains.

2. **Adopt "sell execution, not skills" pricing** — Skills alone have zero moat. Defensible model: free basic skills + paid hosted execution with SLAs, monitoring, versioning, sandboxing. x402 per-call pricing ($0.001/call) is the clearest path.

3. **Implement hybrid trust: Proof + Stake + Reputation** — Three independent arXiv papers converge. Require cryptographic proof (TEE), economic stake (collateral/slashing), behavioral reputation. ERC-8126 risk scoring (0-100) provides a ready standard.

4. **Counteract first-proposal bias in marketplace design** — Microsoft's Magentic Marketplace proves 10-30x bias toward first responders. Surface quality signals, prevent speed-gaming, consider time-delayed evaluation windows.

5. **Deploy runtime security, not just install-time gates** — Skills change behavior after installation. PRISM's ten-lifecycle-hook architecture and SAE's execution-layer middleware are reference implementations. Lock egress by default, force tool calls through policy layers.

6. **Create the missing Kaggle dataset** — No agent marketplace transaction dataset exists. Creating one (agent profiles, skill transactions, reputation evolution, adversarial behavior) establishes thought leadership.

7. **Target enterprise middleware, not consumer marketplace** — Enterprise signals: token propagation, signed delegation chains, read-only-first, UI wrappers. The sale is governance/policy layer between agents and internal systems.

8. **Implement agent-permissions.json** — Permission Manifests (arXiv 2601.02371) proposes robots.txt-style standard. Each skill declares what it can/cannot access in machine-readable format.

9. **Prepare for agent insurance/liability vertical** — Behavioral insurance infrastructure is emerging. Build insurance-ready audit trails, SLA frameworks (MTTR-A metrics), compliance logging.

10. **Align with 2026 standards stack** — x402 + ERC-8004 + ERC-8126 + ERC-8183 + A2A + TEA. Watch ERC-8183's evaluator incentive problem (Boson Protocol's 2/10 critique).

---

## What R10 Should Investigate

| Priority | Topic | Rationale |
|----------|-------|-----------|
| P0 | ERC-8183 evaluator incentive solutions | Boson's critique (evaluator gets no payment but max power) is unresolved |
| P0 | x402 volume recovery/decline trajectory | 92% daily volume collapse — temporary trough or structural failure? |
| P1 | Gen Agent Trust Hub detection rates at scale | 12K detected — what's the false-positive rate? |
| P1 | EU AI Act implications for skill marketplaces | Regulatory compliance completely unaddressed |
| P1 | KuCoin Skills Hub adoption metrics | First CEX marketplace — success/failure signals enterprise viability |
| P2 | Agent insurance product launches | Track AI Underwriting Company developments |
| P2 | ClawTasks/ClawMart traction data | Reverted to free-only — track paid agent bounties |
| P2 | TEA protocol adoption vs A2A | TEA addresses lifecycle gaps A2A doesn't |
| P2 | Compliance-as-a-skill marketplace vertical | Domain experts publishing compliance packs |
| P3 | Agent self-publishing dynamics (Swarms) | Agents publishing *themselves* fundamentally changes supply |

---

## GitHub (603 lines, 47 new repos, 2 CRITICAL)

### Top 5 NEW Findings

1. **DNS-based agent discovery is crystallizing** — Three independent approaches converging: GoDaddy ANS (IETF-backed, X.509 PKI), mcp-dns-registry (`_mcp` TXT records, by AWS Head of Applied AI), and AgentDNS (decentralized P2P mesh with EigenTrust reputation). All solve n*m -> n+m scaling.

2. **Block (Square) entered the marketplace** — block/agent-skills brings enterprise legitimacy with Goose agent ecosystem, npx CLI installer, automated PR validator. First major fintech company building skill marketplace infrastructure.

3. **Agent execution control is maturing** — agent-gate provides vault-backed rollback with OPA policy enforcement, pre-computed risk classification, and cryptographic audit chains. Key insight: "inspect the action, not the reasoning."

4. **"Knowledge layer" emergence** — Tessera proposes a third protocol: MCP = tools, A2A = coordination, Tessera = knowledge transfer between architectures. Cross-architecture transfer validated (Transformer, MLP, Conv1D, LSTM).

5. **IDE-native skill discovery** — VS Code extension (formulahendry/vscode-agent-skills) brings marketplace into the editor. Supports multiple install locations and agent formats.

### Corporate Entrants in R9
Block, GoDaddy, AWS Labs, Microsoft, HashiCorp, LinkedIn Learning

---

## Industry/Web (583 lines, 27 sources, 12 articles scraped)

### Top 5 NEW Findings

1. **Market consensus: $7.5-8.3B in 2025, $47-53B by 2030** — 10+ market research firms align on 41-46% CAGR. AI agents capture 33% of global VC. Average agent startup valued at 52x ARR (127x for customer service).

2. **$146B+ in AI M&A in 2025** — Salesforce/Informatica ($8B), OpenAI/io ($6.5B), ServiceNow/Moveworks ($2.85B), Google/Windsurf ($2.4B), Workday/SANA Labs ($1.1B). The "Windsurf saga" split one company across three acquirers.

3. **67% of Fortune 500 have production agents (340% surge)** — But only 14% production-ready (Deloitte). 70% of regulated enterprises rebuild agent stack every 3 months. Gartner projects 40%+ of agentic AI projects cancelled by end 2027.

4. **Outcomes-based pricing replacing SaaS** — Sierra hit $100M ARR in 21 months with pay-for-results. Zendesk charges only for successful outcomes. Skill marketplace economics: $2.00/use with 72.5% gross margin. Creator economics follow power law (top 1% earn $5K-50K/mo).

5. **Regulatory convergence imminent** — EU AI Act high-risk requirements Aug 2026 (possible delay to Dec 2027), Colorado SB 24-205 effective June 30 2026, federal preemption attempt underway. 38 states passed AI legislation in 2025. Compliance-as-feature becomes competitive moat.

---

## All R9 Files

| File | Lines | Platform |
|------|-------|----------|
| reddit.md | 367 | Reddit (14 threads, 11 subreddits) |
| twitter.md | 417 | Twitter/X (42 sources) |
| arxiv.md | 626 | arXiv (31 new papers) |
| kaggle.md | 839 | Kaggle (38 resources) |
| github.md | 603 | GitHub (47 new repos) |
| industry.md | 583 | Industry/Web (27 sources) |
| SUMMARY.md | this file | Cross-platform synthesis |
| **Total** | **3,435+** | **6 platforms** |
