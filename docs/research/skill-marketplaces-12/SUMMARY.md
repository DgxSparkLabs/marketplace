# ROUND 12: DEEP RESEARCH SUMMARY & CONCLUSIONS

> **Date:** March 16, 2026
> **Research:** 12 searches across 5 platforms, 65+ results, 6 articles/threads scraped
> **New data points:** 52 new GitHub repos catalogued, 5 new arXiv papers, 4 new Kaggle datasets, 20+ Twitter signals, 5 Reddit threads
> **Cumulative:** 260+ sources across 12 research rounds

---

## WHAT CHANGED SINCE ROUND 11 (The Big Shifts)

### 1. The Scale Is Staggering — This Is No Longer "Early"

| Metric | Round 11 (Mar 16 AM) | Round 12 (Mar 16 PM) | Delta |
|--------|---------------------|----------------------|-------|
| anthropics/skills stars | Not tracked separately | **94,608** | Massive — official repo is now #1 |
| Total skills in ecosystem | 500K+ (SkillsMP) | **280K+ confirmed** (arXiv: AgentSkillOS) to 500K+ | Now academically verified |
| Top GitHub "agent skills" repo | 38K (awesome-openclaw) | **94.6K** (anthropics/skills) | Anthropic officially dominates |
| Skills growth rate | Unknown | **15.7% per day** (18.5x in 20 days) | Exponential confirmed |
| Major corporate entrants | Binance, Oracle | **+ Vercel (23K+10K), Google (20K), Anthropic (94K)** | Big tech fully in |
| arXiv papers | 8 | **13** | +5 new papers in days |
| Kaggle agent datasets | 0 dedicated | **1 agent ecosystem dataset + 19K tool directory** | Gap closing |

### 2. The "npm for Agents" Layer Crystallized

**Vercel's skills.sh** is emerging as the package manager for agent skills:
- vercel-labs/skills (10,413 stars) — the CLI tool
- vercel-labs/agent-skills (23,083 stars) — the official collection
- Twitter narrative: "skills.sh is the npm for AI agents"
- Provides `npx skills` for cross-platform install

This is significant because it means the **distribution layer is consolidating** even as the marketplace layer remains fragmented.

### 3. Orchestration Became a Research Focus

Two new papers address intelligent skill routing:
- **SkillOrchestra** (2602.19672): +22.5% over RL-based routing at 700x lower cost
- **XSkill** (2603.12056): Dual-stream continual learning from skills + experiences

This means the marketplace value chain is extending from **list skills -> discover skills -> orchestrate skills -> learn from skill usage**.

### 4. Security Crisis Deepened

New data from web scraping:
- **4 CVEs** in OpenClaw in weeks
- **1.5M tokens exposed** in platform breach
- **21,000+ instances** publicly accessible
- **First confirmed infostealer attack** in the wild
- **CVE-2026-25253** — the ClawHub supply chain attack got a CVE
- **Microsoft issued official OpenClaw security guidance**
- **Gen Digital launched GenAgentTrust Hub** — enterprise answer

### 5. Chinese Ecosystem Exploded

| Repo | Stars | Focus |
|------|-------|-------|
| clawdbot-ai/awesome-openclaw-skills-zh | 3,242 | Chinese OpenClaw skills (translated from official) |
| liyupi/ai-guide | 9,686 | Chinese AI resource guide covering Agent Skills |
| ageerle/ruoyi-ai | 4,914 | Chinese enterprise framework with Agent Skill protocol |
| countbot-ai/CountBot | 213 | Chinese AI agent compatible with OpenClaw skills |

The Chinese market is building its own parallel ecosystem. Internationalization is a real distribution strategy.

---

## CROSS-PLATFORM SYNTHESIS (Round 12)

| Platform | Key Round 12 Finding |
|----------|---------------------|
| **GitHub** | Corporate giants (Anthropic 94K, Vercel 33K, Google 20K) now dominate; distribution layer consolidating around skills.sh |
| **Twitter/X** | "npm for agents" narrative solidified; security crisis deepening (CVE, infostealers); Binance + BNB Chain building full stack |
| **Reddit** | Shifted from "can't monetize" to "can't discover"; 200K+ skills as new norm; SkillsGate + SkillFlow building trust layers |
| **arXiv** | Orchestration (SkillOrchestra) and continual learning (XSkill) as new frontiers; 13 papers total; 15.7% daily growth rate confirmed |
| **Kaggle** | First agent ecosystem dataset appeared; 19K tool directory; still no dedicated skill marketplace dataset (opportunity!) |

---

## UPDATED COMPETITIVE MAP

### Layer 1: Standards & Infrastructure (Settled)
- **SKILL.md** — de facto format (Anthropic, OpenAI, Vercel, Microsoft, Google all support)
- **MCP** — Model Context Protocol (97M+ downloads)
- **A2A** — Agent-to-Agent protocol (emerging)

### Layer 2: Distribution (Consolidating)
- **skills.sh / npx skills** (Vercel, 10K+ stars) — the npm
- **openskills** (9K stars) — universal loader
- **GitHub repos** — still the primary distribution channel

### Layer 3: Discovery (Fragmented — THE OPPORTUNITY)
- SkillsMP (500K+ skills, volume leader)
- SkillsGate (45K indexed, semantic search)
- SkillX.sh (semantic search + ratings + CLI)
- SkillFlow (trust metrics: success rate, total runs)
- NightMarket AI (moderated app store)
- Agensi.io (security scanning + manual review)

### Layer 4: Orchestration (Academic/Emerging)
- AgentSkillOS (DAG-based, 200K scale)
- SkillOrchestra (intelligent routing, 22.5% better)
- XSkill (continual learning from usage)

### Layer 5: Security (Critical Gap)
- SkillFortify (formal verification, 96.95% F1)
- SkillScan (static + LLM analysis, 86.7% precision)
- Snyk agent-scan (enterprise, 1.9K stars)
- GenAgentTrust Hub (Gen Digital, enterprise)
- Trail of Bits skills (security audit workflows)

### Layer 6: Commerce (Virtually Empty)
- SquidBay (Bitcoin Lightning micropayments)
- LarryBrain ($3K MRR, 50% revenue share)
- Agensi.io (one-time purchase)
- ... and almost nothing else

---

## STRATEGIC UPDATE: What Round 12 Changes

### The Discovery Layer Is the Battleground

Round 11 said "trust is the product." Round 12 confirms this AND adds: **discovery is equally critical**. With 200K-500K+ skills, finding the right one is harder than finding any one. SkillsGate's 45K semantic search and SkillFlow's trust metrics are the early answers, but neither has won.

### The Commerce Layer Is Still Wide Open

Despite 94K stars on Anthropic's official repo, 500K+ skills, and $52B projected market — there is **almost no commerce infrastructure**. SquidBay's Bitcoin payments and LarryBrain's $3K MRR are experiments. Stripe Connect for skill marketplaces doesn't exist yet. This is the gap.

### Orchestration Is the Next Moat

SkillOrchestra proves you can route tasks to skills with 22.5% better performance at 700x lower cost. XSkill proves skills can learn from usage. The marketplace that combines discovery + orchestration + learning has the deepest moat.

### Corporate Validation Is Complete

Anthropic (94K), Vercel (33K), Google (20K), Microsoft, Binance, Gate.io, Oracle, Salesforce — every major platform now has an agent skills strategy. This isn't speculative. The question is who builds the marketplace layer on top.

---

## FIVE CONCLUSIONS

1. **The distribution layer is consolidating (Vercel's skills.sh). The discovery/commerce layer is not. Build there.**

2. **Orchestration is the next moat.** Skill routing (SkillOrchestra) + continual learning (XSkill) = intelligent marketplace, not just a catalog.

3. **Security now has a CVE.** CVE-2026-25253 makes this real for enterprises. Formal verification (SkillFortify, 96.95% F1) is the standard to beat.

4. **200K-500K skills is the reality.** The problem isn't supply. It's discovery, trust, composition, and commerce.

5. **Chinese ecosystem is parallel opportunity.** 4+ major Chinese repos, dedicated translations, enterprise frameworks. Localization is a viable strategy.
