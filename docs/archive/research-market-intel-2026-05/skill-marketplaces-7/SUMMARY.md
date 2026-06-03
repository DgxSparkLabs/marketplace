# Round 7 Summary: The Governance & Economics Reckoning

**Date**: March 16, 2026
**Files**: 7 reports, 2,758 lines, ~170KB
**Sources**: 45 GitHub repos, 50+ Twitter signals, 9 Reddit threads, 26 arXiv papers, 9 Kaggle datasets, 12 business/regulatory sources

---

## Executive Summary

Round 7 marks a phase transition in the skill marketplace ecosystem. The conversation has shifted from "how do we build marketplaces?" (R1-R4) and "how do we secure them?" (R5-R6) to **"how do we govern, price, and sustain them?"**

Three convergent forces define this moment:

1. **Governance frameworks arrived** — Singapore's IMDA framework is the first national standard for agentic AI, with a practical 4-tier risk matrix. IEEE P3709 was approved. OWASP published its Agentic Top 10. The fire code now exists.

2. **Pricing models are crystallizing** — The community consensus is clear: seat-based SaaS pricing is dead for agentic products. Three models are competing: outcome-based (pay per result), action-based (pay per run), and hybrid (base + variable). The "Cost of Pass" framework from Reddit is the most sophisticated pricing model in the wild.

3. **Agent markets ≠ human markets** — Academic research (ACES, Magentic Marketplace) empirically proves that agent buyers have systematic biases: 10-30x first-proposal bias, choice homogeneity, position bias even in text-only interfaces. Marketplace design must account for agent cognition.

---

## What's New Since Round 6

### Confirmed Changes
| Signal | R6 Status | R7 Status |
|--------|-----------|-----------|
| SKILL.md adoption | "15+ platforms" | **Format war declared over** — OpenAI made it *required* for Responses API |
| Security vulnerability rate | 26-36% | **41% in latest audit** (2,800 skills) |
| Governance frameworks | Colorado SB 24-205 only | **Singapore IMDA + IEEE P3709 + OWASP Top 10** |
| Crypto skill economy | Theoretical | **Live** — Binance, BNB Chain, SpoonOS, Agent.md shipping |
| Agent marketplace simulation | None | **Microsoft Magentic Marketplace** — first empirical study |
| Pricing models | "Unsolved" | **3 competing models** with real production data |
| A2A Protocol | Emerging | **30+ implementations** across 10+ languages |
| Market sizing | Fragmented estimates | **$12.1B by 2027**, 40% enterprise apps by end 2026 |

### Genuinely New Findings (Not in R1-R6)
1. **Moltbook collapse** — 1.5M "agents" social network exposed API keys within days, Karpathy reversed endorsement. Median time to first critical failure: 16 minutes.
2. **Agent behavioral economics** — Magentic Marketplace proves 10-30x first-proposal bias and scale degradation in agent markets
3. **SkillNet** — 200K+ skill repository with 5-dimensional evaluation (SCEMC: Safety, Completeness, Executability, Maintainability, Cost)
4. **ICL vs IWL pricing theory** — Skills as "rentals" (in-context learning) vs "purchases" (in-weight learning)
5. **PASTA compliance** — $3/eval automated compliance scoring at expert-level accuracy
6. **AgentBazaar architecture** — Validator/Escrow trust model with multi-turn negotiation
7. **Self-publishing agents** — Swarms Corp meta-skill for agents to publish themselves to marketplaces
8. **5 architectural layers identified** (GitHub) — Discovery, Trust, Payments, Orchestration, Governance

---

## Cross-Source Analysis

### Theme 1: The Pricing Revolution
**Sources**: Reddit (4 threads, 170+ comments), Twitter (multiple), Business Landscape, arXiv

The most practically useful finding in R7 is the crystallization of agent pricing models:

| Model | How It Works | Who's Using It | Viability |
|-------|-------------|----------------|-----------|
| **Outcome-based** | Pay per result (deal closed, meeting booked) | Sales agents, u/No_Boysenberry_6827 | High alignment, hard attribution |
| **Action-based** | Credits per run ($3-12/run) | Most B2C builders | Transparent but sticker shock |
| **Hybrid** | Base fee + performance kicker with caps | Enterprise deployments | Most pragmatic today |
| **Machine-based** | $99/month per deployment + 20% token markup | u/westoque (production) | Simple, scales poorly |
| **Cost of Pass** | Price = (Human labor rate) - (Agent cost per successful execution) | Framework by u/Greyveytrain-AI | Most sophisticated |
| **Crypto** | SOL/BNB micropayments, tokenized skills | SpoonOS, Agent.md, Binance | Frictionless, niche |

**Key framework** — Variable Margin Matrix:
- Tier 1 (Linear agents): 5-10% maintenance tax
- Tier 2 (Semi-autonomous): 15-20% + 10% HITL buffer
- Tier 3 (Fully autonomous): 30-40% + 20% hallucination buffer

**Consensus**: "SaaS metrics and token markups are dead for Agentic Ecosystems" — the labor framing wins because buyers compare against headcount, not feature lists.

### Theme 2: Trust Infrastructure as the Monetizable Layer
**Sources**: GitHub (SkillJury, ClawSecure, Conduit), Reddit (41% vuln audit), Twitter (security backlash), arXiv (Ev-Trust, PASTA)

The security numbers keep getting worse:
- R3-R4: 26% vulnerability rate
- R5-R6: 36% vulnerability rate
- **R7: 41% vulnerability rate** (2,800 audited OpenClaw skills)

But trust infrastructure is emerging:

| Project | Approach | Maturity |
|---------|----------|----------|
| **SkillJury** | Review + discovery site, SNYK/Socket scoring | Live, 4,274+ skills |
| **ClawSecure** | Post-install code change detection | ProductHunt launch |
| **Conduit** | Cryptographic audit (SHA-256 + Ed25519) | 420+ agents on SwarmSync |
| **Ev-Trust** | Game-theoretic trust (make deception unprofitable) | Paper (2512.16167) |
| **PASTA** | $3/eval automated compliance | Paper (2601.11702) |
| **Capiscio** | Dual compliance + trust scoring (0-100) | GitHub (4 stars) |

**Key insight**: The marketplace that solves trust first wins. Trust is not a feature — it's the product.

### Theme 3: Agent Markets Are Fundamentally Different
**Sources**: arXiv (ACES, Magentic Marketplace), Business Landscape, Reddit

Academic evidence that agent-driven marketplaces behave differently from human ones:

1. **10-30x first-proposal bias** — Agents overwhelmingly accept the first option presented (Magentic Marketplace)
2. **Choice homogeneity** — Demand concentrates on few "modal" products (ACES)
3. **Position bias** — Persists even in text-only "headless" interfaces (ACES)
4. **Model instability** — Model updates drastically reshuffle market shares (ACES)
5. **Scale degradation** — Marketplace quality decreases as agent count increases (Magentic)
6. **Anti-sponsored bias** — Agents penalize sponsored tags but reward platform endorsements (ACES)
7. **Gaming vulnerability** — Seller-side agents can drive significant market share via description tweaks (ACES)

**Implication**: Current marketplace UX (search, browse, compare) is designed for humans. Agent buyers need different ranking algorithms, anti-gaming mechanisms, and stability guarantees.

### Theme 4: Governance Is No Longer Optional
**Sources**: Business Landscape (DZone analysis), arXiv (COMPASS, PASTA), Twitter, GitHub

The governance stack is forming:

| Layer | Standard/Framework | Status |
|-------|-------------------|--------|
| **National** | Singapore IMDA Framework | Live (Jan 2026) |
| **Industry Architecture** | IEEE P3709 | Approved (Sep 2025) |
| **Security** | OWASP Agentic Top 10 | Published (Dec 2025) |
| **Identity** | Microsoft Entra Agent ID | Production |
| **Interoperability** | Agentic AI Foundation (Linux Foundation) | Launched |
| **Compliance** | PASTA ($3/eval) | Paper |
| **Multi-dimensional** | COMPASS (4-agent governance) | Paper |
| **Market-based** | Insurance + auditing + procurement | Theory |

**Key stat**: 60% of organizations have no mechanism to stop a misbehaving agent.
**Prediction**: 60% of Fortune 100 will appoint head of AI governance by end 2026 (Forrester).

### Theme 5: The Five Architectural Layers
**Sources**: GitHub (45 repos analyzed), arXiv (IoA, AWCP), Business Landscape

Every serious skill marketplace must address 5 layers. No single project covers all:

```
┌─────────────────────────────────┐
│  5. GOVERNANCE                  │  Singapore IMDA, IEEE P3709, COMPASS
│     Compliance, identity, audit │  
├─────────────────────────────────┤
│  4. ORCHESTRATION               │  A2A Protocol (30+ impls), AWCP
│     Multi-agent coordination    │  
├─────────────────────────────────┤
│  3. PAYMENTS                    │  x402, Stripe, crypto micropayments
│     Pricing, billing, escrow    │  
├─────────────────────────────────┤
│  2. TRUST                       │  SkillJury, ClawSecure, Conduit, Ev-Trust
│     Validation, reputation, QA  │  
├─────────────────────────────────┤
│  1. DISCOVERY                   │  SkillsMP, SKILL.md, ChainRec
│     Search, recommendation      │  
└─────────────────────────────────┘
```

The project that integrates all 5 layers first will likely become the dominant marketplace platform.

---

## Cumulative Metrics (Rounds 1-7)

| Metric | R6 Value | R7 Update |
|--------|----------|-----------|
| GitHub repos cataloged | 90+ | **135+** (+45) |
| arXiv papers analyzed | 33+ | **59+** (+26) |
| Twitter signals | 40+ | **90+** (+50) |
| Reddit threads analyzed | 30+ | **39+** (+9) |
| Kaggle datasets | 35+ | **44+** (+9) |
| Skills on SkillsMP | 400K+ | 400K+ (stable) |
| Vulnerability rate | 26-36% | **41%** (new audit) |
| SKILL.md platforms | 15+ | 15+ (format war over) |
| A2A implementations | N/A | **30+** (new metric) |
| Research files | 40 | **47** (+7) |
| Total research KB | 716KB | **~916KB** (+200KB) |

---

## Key Quotes

> "SaaS metrics and token markups are dead for Agentic Ecosystems. The only viable model is Cost of Pass." — u/Greyveytrain-AI, r/AI_Agents

> "An SDR costs $7,711/month fully loaded, quits in 14 months. An agent that does the same work for $999/month and gets BETTER over time? That's not a pricing conversation. That's a no-brainer." — u/No_Boysenberry_6827, r/AI_Agents

> "Agents don't browse. They don't scroll. They execute skills. Whoever writes the SKILL.md controls the workflow — and the revenue." — @notEezzy, X

> "Agentic markets are volatile and fundamentally different from human-centric commerce." — ACES paper, arXiv 2508.02630

> "It's a dumpster fire. I definitely do not recommend people run this stuff on their computers." — Andrej Karpathy on Moltbook

> "The boring infrastructure work is what matters long term. The flashy demos are easy." — u/olivermos273847, r/learnmachinelearning

> "Any organisation worth their salt will want to own the orchestration layer, not have 20 SaaS monoliths each with their own baked-in idea of what AI should be." — u/iainrfharper, r/AI_Agents

---

## What Round 8 Should Investigate

1. **A2A Protocol deep dive** — 30+ implementations discovered but not deeply analyzed. Which ones are gaining traction?
2. **Enterprise deployment case studies** — Deloitte says 35% deploying. Where are the actual case studies?
3. **SKILL.md ecosystem tooling** — skills.sh, skill-creator, Smidge — how mature are the creation tools?
4. **Crypto skill economy tracking** — Binance, SpoonOS, Agent.md shipping. What's getting usage?
5. **Trust infrastructure comparison** — SkillJury vs ClawSecure vs Conduit. Which approach works?
6. **Post-Moltbook regulatory response** — Did the collapse accelerate any regulatory action?
7. **Agent SEO and marketplace gaming** — ACES identified the problem. Are sellers already gaming?
8. **Insurance for agent failures** — AI Governance through Markets paper (2501.17755) suggests insurance as governance. Anyone building it?
