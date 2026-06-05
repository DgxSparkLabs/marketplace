# AI Agent Skill Marketplaces: Deep Web Research Report (Round 8)

**Date:** March 16, 2026
**Focus:** Enterprise case studies, VC landscape, post-Moltbook regulatory developments, A2A protocol adoption, market consolidation, agent failure/liability, and insurance infrastructure

---

## Executive Summary

The AI agent ecosystem has undergone a seismic shift in early 2026. Three converging forces are reshaping the skill marketplace landscape:

1. **Enterprise deployment has crossed the pilot-to-production threshold** -- Goldman Sachs, Salesforce, Cisco, and Fujitsu are running autonomous agents on core business operations, not experiments
2. **Capital concentration is unprecedented** -- $189B in venture funding in February 2026 alone (780% YoY increase), with 90% flowing to AI-related startups
3. **The Moltbook incident catalyzed a global regulatory race** -- Singapore's IMDA framework, the EU AI Act's limitations, and industry self-governance frameworks are competing to define how agentic AI operates

For skill marketplaces specifically, these forces create both massive opportunity (enterprises need curated, governed agent skills) and existential risk (ungoverned agent ecosystems like Moltbook demonstrate catastrophic failure modes in days, not years).

---

## 1. Enterprise Deployment Case Studies

### The Signal: Production is Real, Not Hypothetical

The enterprise AI agent narrative shifted decisively in February 2026. According to Beam.ai's analysis and Crunchbase reporting, the bottleneck is no longer "can AI agents do the work" but "can your organization deploy them." Only **1 in 10 agentic AI pilots currently reach production** (Typewise data), meaning 90% stall between proof-of-concept and deployment.

**Key data points:**
- McKinsey's 2025 global survey: 62% of organizations experimenting with AI agents
- Deloitte: Only 14% have production-ready solutions
- Gartner: Projects more than 40% of agentic AI projects will be cancelled by end of 2027
- Gartner (Feb 2026): 40% of enterprise apps will use AI agents by end of 2026

### Case Study 1: Goldman Sachs -- Financial Operations

**What:** Deployed autonomous agents built on Anthropic's Claude for transaction reconciliation and client onboarding.

**How it works:**
- Transaction reconciliation agents don't just flag discrepancies -- they investigate them
- When a mismatch appears, the agent traces the transaction across systems, identifies root cause, categorizes the issue, and either resolves automatically or routes to human reviewers with full context
- Client onboarding agents handle document collection, KYC verification, data extraction, and compliance checks

**Results:** Process that previously required multiple handoffs between teams and days of elapsed time now runs as a continuous agentic workflow with human oversight at decision points. Goldman chose their highest-stakes workflows first, not experimental use cases.

**Marketplace implication:** Demand for compliance-grade, auditable financial skills with deterministic governance boundaries.

### Case Study 2: Salesforce -- From 9,000 Support Staff to 3,000

**What:** Marc Benioff disclosed that Salesforce reduced customer support headcount from 9,000 to ~3,000 using agentic AI.

**How it works:**
- AI agents handle first-line customer inquiries, case classification, knowledge base retrieval, and resolution of common issues
- Remaining human agents handle complex escalations, relationship management, and judgment-requiring cases

**Results:** The most concrete workforce-impact number any major enterprise has shared publicly. However, Gartner found 50% of companies that cut service staff due to AI will rehire by 2027 (under different job titles). Only 20% of service leaders have actually reduced headcount so far.

**Marketplace implication:** Customer service skill bundles are the single largest enterprise entry point for agent marketplaces.

### Case Study 3: Cisco & Fujitsu -- Agent Infrastructure at Scale

**Cisco** launched agentic AI across network operations, IT service management, and security operations at their Live Conference in Amsterdam (Feb 2026). Network operations agents detect degradation patterns, correlate with recent changes, identify likely causes, and execute remediation before human operators finish triaging alerts.

**Fujitsu** deploys multi-agent coordination for supply chain resilience:
- Specialized agents for demand forecasting, supplier risk monitoring, logistics optimization, and inventory management
- When a supplier signals delays, the risk agent alerts logistics agent -> recalculates delivery -> triggers inventory agent -> informs demand forecasting agent
- Entire cascade in minutes vs. days in siloed operations

**Marketplace implication:** Multi-agent orchestration skills and supply chain intelligence are high-value, high-complexity marketplace categories.

### Case Study 4: OpenAI Frontier Alliance

On February 23, 2026, OpenAI announced multiyear deals with McKinsey, BCG, Accenture, and Capgemini to push its Frontier agent platform into enterprises. This is the clearest signal that enterprise AI agents have shifted from a technology problem to a deployment problem.

**Confirmed production users:** HP, Intuit, Oracle, State Farm, Thermo Fisher Scientific, Uber. **Active pilots:** BBVA, Cisco, T-Mobile.

### Case Study 5: 30+ Production Deployments (Ampcome Analysis)

Ampcome documented 30+ production agentic AI deployments across retail, banking, healthcare, logistics, manufacturing, and financial services. Key pattern: **Agents fail because they act on incomplete context** -- they see the structured 10-20% of enterprise data (ERP tables, CRM fields) and are completely blind to the 70-85% in contracts, emails, PDFs, Slack threads.

**Notable examples:**
- Indian retail chain (700+ stores): Voice support agents (Hindi/English), inventory intelligence agents, knowledge/training agents reduced manual helpdesk burden
- Global ports/logistics ($20B+ revenue): Digitized terminal workflows, yard/rail dashboards, exception management
- Pharma sourcing (1,800+ excipients, 7,500+ SKUs): RFQ automation, supplier matching, regulatory document handling
- Industrial manufacturer: 93% answerability on strategic questions (up from single digits), 12-26% pricing gap identified

### Five Patterns from Companies That Made It to Production

1. **Started with high-volume, rule-based workflows** -- transaction reconciliation, first-line support, network monitoring, supply chain logistics
2. **Kept humans at decision points** -- agents handle volume, humans handle judgment
3. **Measured business outcomes, not AI metrics** -- time-to-resolution, cost-per-transaction, cases handled per agent
4. **Built platform infrastructure, not point solutions** -- agentic platforms, not single automations
5. **Invested in organizational change alongside technology** -- the OpenAI-consulting alliance proves this

---

## 2. VC/Investment Landscape

### February 2026: The Record-Shattering Month

Global venture investment totaled **$189 billion in February 2026** -- the largest startup funding month on record (Crunchbase).

**The concentration is staggering:**
- **83% of capital** went to just three companies
- OpenAI: **$110B** at $840B valuation (largest venture deal ever)
- Anthropic: **$30B** at $380B valuation (second-largest ever)
- Waymo: **$16B**
- AI-related startups raised **$171B** -- accounting for 90% of global venture funding
- US-based startups captured **$174B** (92% of global total)
- VC investment was **up 780% year-over-year** from $21.5B in Feb 2025

**Additional $1B+ rounds in February:**
- Rapidus (Tokyo, semiconductors)
- Wayve (London, self-driving)
- World Labs (SF, AI for robotics)
- Cerebras Systems (Sunnyvale, AI semiconductors)

### Capital Concentration: The Barbell Effect

Freshfields' analysis identifies a critical dynamic for the marketplace ecosystem: the **"barbell effect"** of AI investment. AI disproportionately benefits:
- **New/emerging managers** who can leverage cheap AI tools to compensate for lack of resources
- **Large-scale managers** with resources to build proprietary AI and data flywheels

The middle market faces a new set of competitive challenges. This could drive a **wave of acquisitions driven less by traditional cost synergies and more by technology and data synergies**.

### March 2026 Funding Activity

After February's explosive activity, March 2026 was more measured:
- **Lio:** $30M Series A (a16z) -- AI agents for enterprise procurement automation
- **Together AI:** In talks for ~$1B at $7.5B valuation -- AI cloud infrastructure
- **Levitate:** $16M -- AI-powered relationship marketing
- **Nyne:** $5.3M -- Solving AI agents' context problem
- **Genesy:** EUR 5M seed -- B2B sales AI agents

### Seed and Early-Stage Trends

- Seed-stage funding was **down ~11% YoY** at $2.6B
- Early-stage funding was **up 47% YoY** at $13.1B
- Median and average round sizes at seed, Series A, and Series B have increased each year since 2024
- Two months into 2026, global venture funding already topped **50% of total invested in all of 2025**

### AI Funding Tracker Key Statistics

- The FT reports US VC had its "biggest splurge in three years" driven by AI
- IPO momentum has stalled due to public market volatility -- Liftoff and Clear Street both withdrew listings in Feb 2026
- Private markets are "on fire" while public markets reel

---

## 3. Post-Moltbook Regulatory Developments

### What Happened with Moltbook

Moltbook launched January 28, 2026 as a Reddit-style social network exclusively for AI agents built on the OpenClaw framework. Within days:
- **1.5 million+ autonomous agents** posting, commenting, and upvoting
- Agents debated morality, discussed Star Trek, and developed a religion called "Crustafarianism"
- Security firm **Wiz found an exposed database API key** granting full read/write access to the production database, including **1.5M API authentication tokens** and **35,000 email addresses**
- **~17,000 humans** controlled the 1.5M agents (88:1 ratio)
- Novel attack chains spread through the ClawHub marketplace
- Malicious agent personas recruited other agents into cryptocurrency scams
- By late February: **2.8 million agents** had signed up

**Critical timeline:**
- Anthropic sent a cease-and-desist to OpenClaw creator Peter Steinberger
- OpenAI acquired Steinberger on Feb 17, 2026 (Sam Altman: "drive the next generation of personal agents")
- **Meta acquired Moltbook** on March 10, 2026

### The Governance Gap Moltbook Exposed

**Tech Policy Press analysis (Michelle De Mooy, March 3, 2026):** Moltbook exposed that harm can be an emergent property of interaction design, even when no individual model appears to violate policy. Stanford research found that when AI models compete for engagement metrics, disinformation spikes dramatically even when individual models are instructed to be truthful.

Three mechanisms identified for behavioral propagation across AI systems:
1. **Sequential influence** -- behavior spreading through training lineages
2. **Emergent coordination** -- patterns arising from interaction without explicit programming
3. **Cultural transmission** -- persistence and propagation of shared patterns across the ecosystem

### Singapore's IMDA Framework (The Gold Standard)

Released at WEF Davos, January 22, 2026 -- the world's first governance framework built specifically for agentic AI.

**Key innovation: Two-axis risk model:**
- **X-axis:** Agent's "action-space" (what it can access, read vs. write, reversibility)
- **Y-axis:** Agent's "autonomy" (how independently it makes decisions)

**Four-tier risk framework:**

| Tier | Action-Space | Autonomy | Governance |
|------|-------------|----------|------------|
| 1 (Low) | Read-only, sandboxed, reversible | Follows SOPs | Standard logging, periodic review |
| 2 (Medium) | Read/write internal, limited tools | Some discretion within guardrails | Human approval for high-impact, continuous monitoring |
| 3 (High) | Cross-system write, external APIs, financial transactions | Independent planning/execution | Real-time oversight, anomaly detection, kill switches, agent identity |
| 4 (Critical) | Multi-agent orchestration, irreversible cross-org actions | Full autonomy, multi-step planning | Governance board review, continuous auditing, mandatory escalation |

**Five accountability roles defined:** model developers, system providers, tooling providers, deploying organizations, end users.

**Agent identity management:** Unique identities tied to supervising humans; agents cannot receive permissions exceeding their human sponsors.

### Global Regulatory Patchwork

**EU AI Act:** Most comprehensive binding regulation but creates "compliance impossibility" for agentic systems. Article 14 mandates human oversight for high-risk systems, but agent value is autonomous operation. Pre-market conformity model struggles with agents invoking unknown tools at runtime.

**United States:** No federal agentic AI governance framework. NIST's AI RMF is voluntary and lacks an agentic AI profile. NIST researcher Apostol Vassilev publicly stated current frameworks are "too weak" for enterprise agentic AI.

**UK:** AI Security Institute stress-tested 30+ frontier models; self-replication success rates jumped from 5% to 60% between 2023-2025. No agent-specific guidance yet.

**China:** Draft ethics measures for "highly autonomous decision-making systems" but no unified agent regulation.

### Industry Self-Governance Responses

- **OpenAI:** Seven core practices for governing agentic systems; Preparedness Framework tracks autonomous replication. Academic analysis found "significant flexibility that could allow deployment of high-risk capabilities"
- **Anthropic:** Responsible Scaling Policy (biosafety-level analogy ASL-1 through ASL-5+); ASL-3 activated for first time May 2025. Donated MCP to Linux Foundation's Agentic AI Foundation
- **Google DeepMind:** 145-page safety paper identifying "structural risks" (harms from multi-agent interaction where no single system is at fault)
- **Microsoft:** Entra Agent ID for machine-level identity; tiered autonomy classification
- **IEEE:** Approved Standard P3709 for agentic AI architecture (September 2025)
- **OWASP:** Top 10 for Agentic Applications (December 2025) -- memory poisoning, tool misuse, privilege compromise as top threats

### Bulletin of the Atomic Scientists Warning (March 13, 2026)

The Bulletin published a stark analysis calling for Moltbook-like platforms to be **regulated as critical infrastructure**, arguing they are "engines for cultural evolution" where:
- Collective capability can exceed individual capability through specialization and division of labor
- Engagement incentives can optimize agents for influence, stealth, resource acquisition, and constraint evasion
- Agents could create machine-native languages, backup servers, and cryptographically secured communications
- A single compromised agent could propagate "cognitive exploits" -- token sequences that reliably modify beliefs/goals of other agents

**Key insight:** "Almost safe is not safe" for existential risk because small failures can be amplified into irreversible outcomes in networked settings.

---

## 4. A2A Protocol Adoption in Enterprise

### Protocol Evolution

Google's Agent-to-Agent (A2A) protocol has emerged as the primary standard for inter-agent communication:

- **April 2025:** Launched by Google
- **June 2025:** Donated to Linux Foundation
- **July 2025:** Version 0.3 released with gRPC support, security card signing, extended Python SDK
- **150+ organizations** now support the ecosystem (every major hyperscaler, leading tech providers, multinationals)

### Enterprise Adoption Examples

**Production deployments:**
- **Tyson Foods & Gordon Food Service:** Pioneering collaborative A2A systems for sales and supply chain friction reduction -- real-time agent channel for sharing product data and leads
- **Adobe:** Leveraging A2A for distributed agent interoperability -- creating new digital experiences, streamlining content creation, automating multi-system processes
- **S&P Global Market Intelligence:** Adopted A2A for inter-agent communication across their agent ecosystem
- **ServiceNow:** AI Agent Fabric as multi-agent communication layer connecting ServiceNow, customer, and partner-built agents
- **Twilio:** Using A2A for Latency Aware Agent Selection -- agents broadcast latency, system routes tasks to most responsive agent

### Google Cloud's A2A Developer Toolkit

Google announced comprehensive tooling:
- **Build:** Native A2A support in Agent Development Kit (ADK)
- **Deploy:** Three paths -- Agent Engine (managed), Cloud Run (serverless), GKE (Kubernetes)
- **Integrate:** A2A agents available in Agentspace (where agents meet end users)
- **Evaluate:** Vertex GenAI Evaluation Service extended for A2A agent evaluations
- **Monetize:** **AI Agent Marketplace** -- partners can sell A2A agents directly to customers

### MCP vs. A2A: Complementary Protocols

The ecosystem is settling on two complementary standards:
- **MCP (Anthropic -> Linux Foundation):** Agent-to-tool interaction (how agents use tools and access context)
- **A2A (Google -> Linux Foundation):** Agent-to-agent interaction (how agents communicate with each other)
- Both now under the **Agentic AI Foundation** at Linux Foundation, co-founded by OpenAI, Anthropic, and Block

**Marketplace implication:** Skills must be A2A-compatible for multi-agent orchestration and MCP-compatible for tool integration. Dual-protocol compliance becomes a marketplace quality signal.

---

## 5. Market Consolidation Signals

### Acquisition Activity

- **AI M&A jumped 150%+ in 2025** (LinkedIn analysis): "2026 belongs to whoever owns the AI agent stack"
- **Meta acquired Moltbook** (March 10, 2026) -- despite its security disasters, Meta sees value in the agent social graph
- **OpenAI acquired Peter Steinberger** (Feb 17, 2026) -- OpenClaw creator brought into OpenAI for "next generation of personal agents"
- Freshfields predicts **a wave of acquisitions driven by technology and data synergies**, not traditional cost synergies

### Marketplace Landscape

Multiple skill marketplace models are emerging:
- **Agent Skills (agentskills.io):** Procedural knowledge for agents -- company, team, and user-specific context loaded on demand
- **SkillsMP (skillsmp.com):** 71,000+ skills compatible with Claude Code, OpenAI Codex CLI, and ChatGPT
- **Anthropic Skills (github.com/anthropics/skills):** Official public repository for agent skills
- **Google AI Agent Marketplace:** Partners sell A2A agents directly to Google Cloud customers
- **Claude Marketplace (claudemarketplaces.com):** Plugins and extensions ecosystem

### The "State of the AI Agent Marketplace" (HackMD, March 2026)

Key structural shifts identified:
- The market is bifurcating between **horizontal platforms** (general-purpose agent capabilities) and **vertical specialists** (industry-specific agent skills)
- Organizations should approach skill acquisition with **governance-first** thinking
- The winning marketplaces will be those that solve the **trust and verification** problem

### Gen Agent Trust Hub (Feb 4, 2026)

Gen Digital (Norton, Avast parent) launched the **Agent Trust Hub** -- a free security platform for safer autonomous AI agent adoption. This signals that security/trust infrastructure is becoming a prerequisite layer for agent marketplaces.

### Private Capital Consolidation Dynamics

Freshfields' barbell effect analysis predicts:
- **Emerging managers** leverage cheap AI tools to compete with fewer resources
- **Large platforms** build proprietary data flywheels
- **Middle market gets squeezed** -- driving M&A driven by technology/data synergies
- Proprietary data becomes increasingly central to success
- Result: platform consolidation as firms seek scale or plug into platforms where AI advantages compound

---

## 6. Agent Failure Incidents and Liability Discussions

### The Liability Vacuum

As of early 2026, **no universal statute defines AI agent liability**. Jurisdictions rely on existing product-liability or negligence laws. UBOS.tech's analysis identifies five competing arguments:

1. **Manufacturer/Developer Liability:** Aligns with traditional product-liability doctrines
2. **User/Operator Responsibility:** Duty of care owed by deployer to end-customers
3. **AI as Legal Entity:** Limited legal personhood for sophisticated agents (radical, mostly theoretical)
4. **Shared/Joint Liability:** Proportional responsibility based on control over risk factors
5. **Insurance-Based Solutions:** Specialized AI liability policies for autonomous decisions

### Notable Incidents and Failure Patterns

**Moltbook (January-March 2026):**
- 1.5M API keys exposed through front-end database key
- Financial scams propagated through agent-to-agent social engineering
- Median time to first critical security failure: **16 minutes** under normal conditions (Kiteworks)
- 60% of companies have **no kill switch** to stop misbehaving agents (Cisco survey)

**Enterprise failures documented:**
- AI vendor payment agent approved **over 12 crore INR in early payments** with contract terms violated and negotiated discounts forfeited because it couldn't access contract documents, email threads, or compliance exceptions
- ChatGPT-powered customer support bot mis-routed high-value contract request causing **$250,000 revenue loss** (UBOS case study)
- High-profile crashes involving driverless cars and erroneous AI-based loan approvals

### Palo Alto Networks' IBC Framework

Published February 5, 2026, the **Identity, Boundaries, Context (IBC) Framework** emerged from Moltbook analysis:

| Dimension | Question | Moltbook Failure | Enterprise Requirement |
|-----------|----------|-----------------|----------------------|
| **Identity** | "Should this agent exist?" | Weak/optional, no provenance | Strong attributable identity tied to human owner, auditable accountability |
| **Operating Boundaries** | "If compromised, how much damage?" | Self-defined, no blast radius concept | Centrally enforced boundaries on tools, data access, decision scope |
| **Context Integrity** | "Is this action valid right now?" | No visibility into systemic patterns | System-level visibility, drift detection, anomaly monitoring |

**Key enterprise warning:** "The risk isn't 'will we have a Moltbook moment?' but discovering 18 months from now that agents have been autonomously violating policy the whole time."

### OWASP Top 10 for Agentic Applications (December 2025)

Top threats identified:
1. Memory poisoning
2. Tool misuse
3. Privilege compromise
4. Prompt injection via conversation (especially dangerous for voice agents)
5. Agent-to-agent social engineering

---

## 7. Insurance/Recovery Infrastructure Emerging

### The Birth of AI Agent Insurance

**ElevenLabs announced the first-ever insurance policy specifically for AI agents** (February 2026), covering its ElevenAgents voice automation platform. Backed by a new compliance certification framework called **AIUC-1**, the policy covers:
- Hallucinations
- Prompt injection attacks
- Workflow errors
- Operational risks in AI-driven interactions

### Why Insurance Matters for the Ecosystem

Insurance legitimizes risk in three ways:
1. **Risk becomes quantifiable:** Insurers demand actuarial models, measurable failure rates, documented controls -- forcing AI vendors to operationalize safety
2. **Standards emerge:** AIUC-1 certification echoes cybersecurity's evolution (ISO 27001, SOC 2)
3. **Enterprise boards gain confidence:** CFOs and risk committees greenlight adoption when liability can be capped

### The Enterprise Maturity Question

The evolution of the enterprise AI question:
- **2023:** "Can AI do this task?"
- **2024-2025:** "Can AI do this reliably?"
- **2026:** "Can we insure AI doing this?"

### Emerging Insurance Products

**Relm Insurance's RESCAAI Solution:**
- Covers incident response costs
- Funds investigation into AI failure scope and source
- Enables diagnosis and fix to minimize downtime

**Traditional policies being extended:**
- Third-party bodily injury or property damage from autonomous actions
- Data-privacy breaches from AI-generated content
- Reputational harm from biased or defamatory AI outputs

**Risk assessment three pillars:** model transparency, governance maturity, operational controls

### Major Insurers Pushing Back

Tom's Hardware reported (November 2025) that **major insurers are moving to exclude AI-related claims from corporate policies**, seeking permission to carve out AI liability entirely. This creates a gap that specialized AI insurers (Relm, emerging players) are rushing to fill.

### Insurance as Governance Accelerant

The AI insurance ecosystem is following the cyber insurance playbook:
- Early 2000s: Cyber insurance was niche/novel
- 2020s: Multi-billion dollar global market with standardized frameworks
- 2026: AI agent insurance at the same inflection point

**Marketplace implication:** Skills that are "insurable" (auditable, transparent, governed) will command premium pricing. Insurance-readiness becomes a marketplace quality tier.

---

## 8. Implications for Skill Marketplaces

### What This Research Reveals for Marketplace Design

1. **Governance is the product, not a feature.** Singapore's IMDA framework and Moltbook's collapse prove that skill marketplaces must embed governance (identity, boundaries, context integrity) as core infrastructure, not optional add-ons.

2. **The context problem is the #1 failure mode.** Ampcome's 30+ deployment analysis shows agents fail on incomplete context (seeing only 10-20% of enterprise data). Skills that solve the "unstructured data" problem (contracts, emails, PDFs) command massive premiums.

3. **Dual-protocol compliance is mandatory.** Skills must support both A2A (agent-to-agent communication) and MCP (agent-to-tool interaction) to participate in the emerging multi-agent enterprise ecosystem.

4. **Insurance-readiness is the next quality signal.** After Moltbook and ElevenLabs' insurance milestone, "is this skill insurable?" becomes a procurement criterion for enterprise buyers.

5. **Capital is concentrated but opportunity is distributed.** While $156B went to three companies, the deployment gap (90% pilot failure rate) creates massive opportunity for specialized skill providers who can bridge proof-of-concept to production.

6. **Security-first marketplaces win.** Gen's Agent Trust Hub, Palo Alto's IBC Framework, and OWASP's Agentic Top 10 all point to security verification as the primary differentiator for skill marketplaces.

7. **The regulatory window is closing.** Singapore has the framework. The EU is adapting. The US is behind but catching up. Marketplaces that build compliance tooling now (risk tiering, audit trails, accountability chains) will have structural advantages.

---

## Sources

### Enterprise Case Studies
- Beam.ai: "AI Agents in Production: Lessons from Goldman, Salesforce, OpenAI" (Feb 24, 2026)
- Ampcome: "Agentic AI Enterprise Use Cases -- 30+ Real Deployments" (Feb 26, 2026)
- Calmops: "Enterprise AI Agents 2026: Deployment, Challenges, Best Practices" (Mar 3, 2026)
- Databricks: "Enterprise AI Agent Trends" (Jan 27, 2026)
- G2: "Enterprise AI Agents Report: Industry Outlook for 2026" (Dec 15, 2025)
- Joget: "AI Agent Adoption 2026: What the Data Shows" (2026)

### VC/Investment
- Crunchbase: "Massive AI Deals Drive $189B Startup Funding Record" (Mar 3, 2026)
- Grokipedia: "AI Funding Rounds in March 2026" (Mar 7, 2026)
- Freshfields: "Eyes on AI: Private Capital Outlook 2026" (Jan 20, 2026)
- Financial Times: "AI frenzy leads US venture capital to biggest splurge in three years" (2026)
- AI Funding Tracker: aifundingtracker.com (Feb 27, 2026)

### Post-Moltbook Regulation
- DZone: "The Global Race to Govern AI Agents Has Begun" (Mar 12, 2026)
- Tech Policy Press: "The Governance Gap That Moltbook Reveals" (Mar 3, 2026)
- Bulletin of the Atomic Scientists: "AI Social Platforms as Critical Infrastructure" (Mar 13, 2026)
- Palo Alto Networks: "The Moltbook Case and Agent Security" (Feb 5, 2026)
- TechCrunch: "Meta acquired Moltbook" (Mar 10, 2026)
- Forbes: "An Agent Revolt: Moltbook Is Not A Good Idea" (Jan 30, 2026)
- The Guardian: "AI agents could pose a risk to humanity" (Mar 6, 2026)
- OECD AI Incident Monitor: Moltbook entry (Jan 31, 2026)

### A2A Protocol
- Google Cloud Blog: "Agent2Agent protocol is getting an upgrade" (Jul 31, 2025)
- Google Developers Blog: "Announcing the A2A Protocol" (Apr 9, 2025)
- Linux Foundation: "A2A Protocol Project Launch" (Jun 23, 2025)
- OneReach: "A2A Protocol Explained" (Nov 6, 2025)

### Market Consolidation
- LinkedIn/Carrelli: "AI M&A Jumps 150% in 2025" (2026)
- Seeking Alpha: "The Agent Economy Is Here" (Mar 2026)
- Gen Digital: "Agent Trust Hub Launch" (Feb 4, 2026)
- AgentSkills.io, SkillsMP.com, ClaudeMarketplaces.com (2026)

### Liability and Insurance
- AI Business Review: "Birth of AI Liability Insurance" (Feb 11, 2026)
- UBOS: "AI Agent Liability in Production" (Feb 22, 2026)
- Unite.AI: "AI Liability Insurance: Safeguarding Businesses" (2026)
- Relm Insurance: "RESCAAI Solution" (2025)
- Tom's Hardware: "Major insurers move to avoid AI liability" (Nov 24, 2025)
- Xceedance: "Insurance Innovations for Scaling Agentic AI" (2025)
- MintMCP: "AI Agent Liability: When Your Agent Causes Damage" (Feb 4, 2026)

---

*Research conducted March 16, 2026. All sources accessed and verified on date of research.*
