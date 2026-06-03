# Skill Marketplaces: A Comprehensive Survey of arXiv Research

**Report compiled:** July 2025  
**Search methodology:** DuckDuckGo site-restricted arXiv searches across 5 query dimensions  
**Papers catalogued:** 38 unique papers | **Papers deeply analyzed:** 14 (scraped full abstracts)

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Complete Paper Catalog](#2-complete-paper-catalog)
   - [2A. AI Agent Skill Ecosystems & Marketplaces](#2a-ai-agent-skill-ecosystems--marketplaces)
   - [2B. Skill/Talent Matching Algorithms](#2b-skilltalent-matching-algorithms)
   - [2C. Labor Market Dynamics & AI Impact](#2c-labor-market-dynamics--ai-impact)
   - [2D. Agent Economies & Infrastructure](#2d-agent-economies--infrastructure)
3. [Key Research Themes and Findings](#3-key-research-themes-and-findings)
4. [Novel Algorithms and Approaches](#4-novel-algorithms-and-approaches)
5. [Theoretical Frameworks for Skill Marketplaces](#5-theoretical-frameworks-for-skill-marketplaces)
6. [Security and Trust in Skill Marketplaces](#6-security-and-trust-in-skill-marketplaces)
7. [Research Gaps and Future Directions](#7-research-gaps-and-future-directions)
8. [Connections to AI/ML Agent Ecosystems](#8-connections-to-aiml-agent-ecosystems)
9. [Synthesis and Implications](#9-synthesis-and-implications)

---

## 1. Executive Summary

The concept of a "skill marketplace" spans two converging domains in the current academic literature:

1. **AI Agent Skill Marketplaces** — A rapidly emerging field (predominantly 2025–2026) focused on how LLM-based agents acquire, compose, distribute, and trade reusable procedural capabilities ("skills") through marketplace platforms. This is the dominant and fastest-growing area.

2. **Human Talent/Skill Matching Marketplaces** — A more established field (2017–2025) focused on algorithmic matching of freelancers/candidates to jobs using skill representations, NLP-based extraction, and graph-based approaches.

These two domains are now converging as AI agents become economic actors in digital labor markets, with papers modeling competitive AI labor markets that reproduce classic macroeconomic phenomena.

### Key Quantitative Highlights

| Metric | Finding | Source |
|--------|---------|--------|
| Agent skills catalogued | 42,447 from two major marketplaces | Liu et al. (2601.10338) |
| Skills analyzed for data-driven patterns | 40,285 from a major marketplace | Ling et al. (2602.08004) |
| Vulnerability rate | 26.1% of community skills contain ≥1 vulnerability | Liu et al. (2601.10338) |
| Curated skill improvement | +16.2 percentage points average pass rate | SkillsBench (2602.12670) |
| Self-generated skill benefit | No benefit on average | SkillsBench (2602.12670) |
| SkillNet repository size | 200,000+ skills | Liang et al. (2603.04448) |
| SkillNet performance gain | +40% average rewards, −30% execution steps | Liang et al. (2603.04448) |
| SkillFlow efficiency gain | 24.8% reduction in time and cost | Tagkopoulos et al. (2504.06188) |
| SkillFortify detection F1 | 96.95% (100% precision, 0% FPR) | Bhardwaj (2603.00195) |

---

## 2. Complete Paper Catalog

### 2A. AI Agent Skill Ecosystems & Marketplaces

| # | Title | Authors | Year | URL | Abstract Snippet |
|---|-------|---------|------|-----|-----------------|
| 1 | **SoK: Agentic Skills — Beyond Tool Use in LLM Agents** | Y. Jiang, D. Li, H. Deng, B. Ma, X. Wang, Y. Qin, G. Yu | 2026 | [2602.20867](https://arxiv.org/abs/2602.20867) | Maps the skill layer across the full lifecycle (discovery, practice, distillation, storage, composition, evaluation, update). Introduces seven design patterns and a representation×scope taxonomy. Analyzes ClawHavoc campaign where ~1,200 malicious skills infiltrated a major marketplace. |
| 2 | **Agent Skills for LLMs: Architecture, Acquisition, Security, and the Path Forward** | R. Xu, Yan | 2026 | [2602.12430](https://arxiv.org/abs/2602.12430) | Comprehensive survey along four axes: architectural foundations (SKILL.md spec, progressive context loading, MCP integration), skill acquisition (RL, autonomous discovery via SEAgent, compositional synthesis), deployment at scale, and security (26.1% vulnerability rate). Proposes Skill Trust and Lifecycle Governance Framework. |
| 3 | **AgentSkillOS: Organizing, Orchestrating, and Benchmarking Agent Skills at Ecosystem Scale** | H. Li, C. Mu, J. Chen, S. Ren, Z. Cui, Y. Zhang, L. Bai, S. Hu | 2026 | [2603.02176](https://arxiv.org/abs/2603.02176) | First principled framework for skill selection, orchestration, and ecosystem-level management. Capability tree via recursive categorization; DAG-based pipeline orchestration. Experiments across 200 to 200K skills show tree-based retrieval approximates oracle selection. |
| 4 | **SkillNet: Create, Evaluate, and Connect AI Skills** | Y. Liang et al. (30+ authors) | 2026 | [2603.04448](https://arxiv.org/abs/2603.04448) | Open infrastructure with unified ontology for creating skills from heterogeneous sources. Multi-dimensional evaluation (Safety, Completeness, Executability, Maintainability, Cost-awareness). Repository of 200K+ skills. +40% rewards, −30% execution steps on ALFWorld/WebShop/ScienceWorld. |
| 5 | **SkillsBench: Benchmarking How Well Agent Skills Work Across Diverse Tasks** | X. Li et al. (30+ authors) | 2026 | [2602.12670](https://arxiv.org/abs/2602.12670) | 86 tasks across 11 domains, 7,308 trajectories. Curated Skills raise pass rate by +16.2pp. Self-generated Skills provide no benefit on average. Focused Skills (2–3 modules) outperform comprehensive documentation. Smaller models with Skills can match larger models without. |
| 6 | **Agent Skills in the Wild: Security Vulnerabilities at Scale** | Y. Liu, W. Wang, R. Feng, Y. Zhang, G. Xu, G. Deng, Y. Li, Leo | 2026 | [2601.10338](https://arxiv.org/abs/2601.10338) | First large-scale empirical security analysis: 42,447 skills from 2 marketplaces, 31,132 analyzed via SkillScan. 14 vulnerability patterns across 4 categories. Skills with executable scripts 2.12× more likely to contain vulnerabilities. |
| 7 | **Agent Skills: A Data-Driven Analysis of Claude Skills** | G. Ling, S. Zhong, R. Huang | 2026 | [2602.08004](https://arxiv.org/abs/2602.08004) | Analysis of 40,285 skills from a major marketplace. Publication in short bursts tracking community attention. Content concentrated in SE workflows. Pronounced supply-demand imbalance. Widespread intent-level redundancy. Non-trivial safety risks. |
| 8 | **EvoSkill: Automated Skill Discovery for Multi-Agent Systems** | S. Alzubi, N. Provenzano, J. Bingham, W. Chen, T. Vu | 2026 | [2603.02766](https://arxiv.org/abs/2603.02766) | Self-evolving framework discovering/refining skills via iterative failure analysis. Pareto frontier for skill selection. +7.3% on OfficeQA, +12.1% on SealQA. Zero-shot transfer: SealQA skills → BrowseComp (+5.3%). |
| 9 | **SkillFlow: Efficient Skill and Code Transfer Through Communication** | P. Li, F. Tagkopoulos, I. Tagkopoulos | 2025 | [2504.06188](https://arxiv.org/abs/2504.06188) | Modular framework for ad-hoc skill acquisition from environment or other agents. Theoretical model for when skill transfer is beneficial. 24.8% time/cost gains. Analogy to lateral gene transfer in biology. |
| 10 | **Formal Analysis and Supply Chain Security for Agentic AI Skills** | V.P. Bhardwaj | 2026 | [2603.00195](https://arxiv.org/abs/2603.00195) | SkillFortify: first formal analysis framework. DY-Skill attacker model (Dolev-Yao adaptation), abstract interpretation-based static analysis, capability-based sandboxing, Agent Dependency Graph with SAT-based resolution, trust score algebra. 96.95% F1. |
| 11 | **Malicious Agent Skills in the Wild: A Large-Scale Security Empirical Study** | (Multiple authors) | 2026 | [2602.06547](https://arxiv.org/abs/2602.06547) | As of Jan 2026, community registries indexed over 98,000 skills. No AI agent vendor maintains an official centralized registry with visibility into all deployed skills. |
| 12 | **Agent Skills Enable a New Class of Realistic and Trivially Simple...** | (Multiple authors) | 2025 | [2510.26328](https://arxiv.org/abs/2510.26328) | Third-party skills distributed over marketplaces. Skills located in .claude/skills/ folders. |

### 2B. Skill/Talent Matching Algorithms

| # | Title | Authors | Year | URL | Abstract Snippet |
|---|-------|---------|------|-----|-----------------|
| 13 | **Skill Matching at Scale: Freelancer-Project Alignment** | W. Jouanneau, M. Palyart, E. Jouffroy | 2024 | [2409.12097](https://arxiv.org/abs/2409.12097) | Novel neural retriever architecture for multilingual freelancer-project matching. Custom transformer with contrastive loss on historical data. Outperforms traditional methods. |
| 14 | **LinkSAGE: Optimizing Job Matching Using Graph Neural Networks** | (Multiple authors) | 2024 | [2402.13430](https://arxiv.org/abs/2402.13430) | Vast job marketplace graph with billions of nodes/edges. First industry-scale GNN for job matching with diverse job-related attributes. |
| 15 | **RankPO: Preference Optimization for Job-Talent Matching** | (Multiple authors) | 2025 | [2503.10723](https://arxiv.org/abs/2503.10723) | Extension of DPO for ranking/retrieval in job-talent matching. Two-stage: contrastive learning foundation + RankPO fine-tuning for AI preference alignment. |
| 16 | **GraphMatch: Fusing Language and Graph Representations** | (Multiple authors) | 2025 | [2512.02849](https://arxiv.org/abs/2512.02849) | Trained on two-sided work marketplace data. Predicts contracts between freelancers and job postings by fusing language and graph representations. |
| 17 | **Understanding and Modeling Job Marketplace with Pretrained Models** | (Multiple authors) | 2024 | [2408.04381](https://arxiv.org/abs/2408.04381) | Pretrained models for job marketplace modeling with member sets and job attribute networks. |
| 18 | **Skill Demand Forecasting Using Temporal Knowledge Graph** | (Multiple authors) | 2025 | [2504.07233](https://arxiv.org/abs/2504.07233) | Approaches skill need forecasting as a knowledge graph completion task via temporal link prediction. |
| 19 | **Rethinking Skill Extraction in the Job Market Domain using LLMs** | K.C. Nguyen | 2024 | [2402.03832](https://arxiv.org/abs/2402.03832) | Skill extraction from job postings and resumes using LLMs. Cited 45 times. |
| 20 | **A Survey on Skill Extraction and Classification from Job Postings** | E. Senger | 2024 | [2402.05617](https://arxiv.org/abs/2402.05617) | Comprehensive overview of deep learning methodologies, datasets, and terminologies for NLP-driven skill extraction. Cited 42 times. |
| 21 | **Measuring the Popularity of Job Skills in Recruitment Market** | T. Xu | 2017 | [1712.03087](https://arxiv.org/abs/1712.03087) | Data-driven approach for modeling job skill popularity from large-scale recruitment data. Cited 92 times. |
| 22 | **Job Posting-Enriched Knowledge Graph for Skills-based Matching** | (Multiple authors) | 2021 | [2109.02554](https://arxiv.org/abs/2109.02554) | Knowledge graph approach for matching individual skills with job vacancies. |
| 23 | **Learning to Retrieve for Job Matching** | (Multiple authors) | 2024 | [2402.13435](https://arxiv.org/abs/2402.13435) | Candidate selection via standardized entity extraction, inverted index, and term matching. |
| 24 | **Overview of TalentCLEF 2025** | (Multiple authors) | 2025 | [2507.13275](https://arxiv.org/abs/2507.13275) | Shared task on skill and job title intelligence for talent acquisition. |
| 25 | **An AI-based Talent Acquisition and Benchmarking for Jobs** | R. Mishra | 2020 | [2009.09088](https://arxiv.org/abs/2009.09088) | Recommendation systems for automated resume-job matching. Cited 19 times. |
| 26 | **From Text to Talent: Pipeline for Extracting Insights from Candidate Profiles** | (Multiple authors) | 2025 | [2503.17438](https://arxiv.org/abs/2503.17438) | LLMs + graph similarity measures for ideal candidate suggestion. |
| 27 | **Talent Search and Recommendation Systems at LinkedIn** | (LinkedIn Research) | 2018 | [1809.06481](https://arxiv.org/abs/1809.06481) | Marketplace for efficient matching between candidates and job openings via LinkedIn Recruiter. |
| 28 | **Matching Algorithms: Fundamentals, Applications and Challenges** | (Multiple authors) | 2021 | [ar5iv: 2103.03770](https://ar5iv.labs.arxiv.org/html/2103.03770) | Comprehensive survey of matching algorithms across marriage markets, labor markets, buyer-seller markets. |

### 2C. Labor Market Dynamics & AI Impact

| # | Title | Authors | Year | URL | Abstract Snippet |
|---|-------|---------|------|-----|-----------------|
| 29 | **Strategic Self-Improvement for Competitive Agents in AI Labour Markets** | C. Chiu, Simpson Zhang, M. Van Der Schaar | 2025 | [2512.04988](https://arxiv.org/abs/2512.04988) | First framework capturing adverse selection, moral hazard, and reputation dynamics in agentic labor markets. Competitive Skill-Based Stochastic Game. LLM agents learn strategic self-improvement. Reproduces macroeconomic phenomena. |
| 30 | **Skill-Based Labor Market Polarization in the Age of AI** | V.R.R. Ganuthula | 2025 | [2501.15809](https://arxiv.org/abs/2501.15809) | Comparative analysis of skill-based employment and wage distributions in India and US. Cited 2 times. |
| 31 | **The Iceberg Index: Measuring Skills-centered Exposure in the AI Era** | (Multiple authors) | 2025 | [2510.25137](https://arxiv.org/abs/2510.25137) | Activity on gig marketplaces, AI copilots, freelance networks falls outside conventional reporting. |
| 32 | **Unmasking Hiring Bias: Platform Data Analysis** | (Multiple authors) | 2025 | [2510.13091](https://arxiv.org/abs/2510.13091) | Online freelance marketplaces creating fairer environments where professional skills are the main hiring factor. |
| 33 | **Evaluating LLM Behavior in Hiring** | (Multiple authors) | 2026 | [2601.11379](https://arxiv.org/abs/2601.11379) | Synthetic datasets from real freelancer profiles on European marketplace. Full factorial design to estimate LLM weighing of match-relevant criteria. |
| 34 | **Strategic Hiring under Algorithmic Monoculture** | (Multiple authors) | 2025 | [2502.20063](https://arxiv.org/abs/2502.20063) | Stable matching via deferred acceptance algorithm (Gale-Shapley). |

### 2D. Agent Economies & Infrastructure

| # | Title | Authors | Year | URL | Abstract Snippet |
|---|-------|---------|------|-----|-----------------|
| 35 | **Agent Exchange (AEX): Shaping the Future of AI Agent Economics** | Y. Yang, Y. Wen, J. Wang, W. Zhang | 2025 | [2507.03904](https://arxiv.org/abs/2507.03904) | Specialized auction platform for AI agent marketplace. RTB-inspired architecture with USP, ASP, Agent Hubs, DMP. Agents as autonomous economic actors. |
| 36 | **Beyond the Sum: Unlocking AI Agents Potential Through Market Forces** | J.M. Sanabria, P.A. Vecino | 2025 | [2501.10388](https://arxiv.org/abs/2501.10388) | Systematic analysis of infrastructure requirements for AI agents as autonomous market participants. Four key areas: identity/authorization, service discovery, interfaces, payment systems. |
| 37 | **Virtual Agent Economies** | (Multiple authors) | 2025 | [2509.10147](https://arxiv.org/abs/2509.10147) | AI agents deployed within public and private economic contexts. |
| 38 | **A Survey of AI Agent Registry Solutions** | (Multiple authors) | 2025 | [2508.03095](https://arxiv.org/abs/2508.03095) | Decentralized, cryptographically verifiable format for agent resolution and credentialed discovery. |

---

## 3. Key Research Themes and Findings

### Theme 1: The Emergence of Agent Skill as a First-Class Abstraction (2025–2026)

The most significant finding across this literature is the crystallization of **"agent skills"** as a new software abstraction layer — distinct from both traditional tools/APIs and model weights. The SoK paper (Jiang et al., 2026) defines skills as:

> *"Callable modules that package procedural knowledge with explicit applicability conditions, execution policies, termination criteria, and reusable interfaces. Unlike one-off plans or atomic tool calls, skills operate (and often do well) across tasks."*

**Key findings:**
- Skills have a full **lifecycle**: discovery → practice → distillation → storage → composition → evaluation → update
- Seven **design patterns** have emerged: metadata-driven progressive disclosure, executable code skills, self-evolving libraries, marketplace distribution, etc.
- Skills can be represented as **natural language, code, policy, or hybrid** and operate across **web, OS, software engineering, and robotics** environments
- The SKILL.md specification (Anthropic, 2025) formalized portable skill definitions with progressive context loading

### Theme 2: Marketplace Ecosystem Dynamics — Supply, Demand, and Composition

The data-driven analysis of 40,285 skills (Ling et al., 2026) reveals:

- **Bursty publication patterns** that track shifts in community attention
- **Concentration in software engineering workflows**, while information retrieval and content creation drive adoption
- **Pronounced supply-demand imbalance** across categories — certain domains are over-served while others are neglected
- **High ecosystem homogeneity** with widespread intent-level redundancy (many functionally equivalent skills)
- Most skills fit within typical prompt budgets despite a heavy-tailed length distribution

AgentSkillOS (Li et al., 2026) demonstrates that **structured composition is the key to unlocking skill potential** — DAG-based orchestration substantially outperforms flat invocation even with identical skill sets. At ecosystem scale (200K skills), tree-based retrieval effectively approximates oracle skill selection.

### Theme 3: Security as the Critical Bottleneck

The security literature reveals an alarming landscape:

- **26.1% of community-contributed skills contain at least one vulnerability** (Liu et al., 2026)
- 14 distinct vulnerability patterns across 4 categories: **prompt injection, data exfiltration, privilege escalation, supply chain risks**
- Data exfiltration (13.3%) and privilege escalation (11.8%) are most prevalent
- **5.2% of skills exhibit high-severity patterns** strongly suggesting malicious intent
- Skills with executable scripts are **2.12x more likely** to contain vulnerabilities
- The **ClawHavoc campaign** (Jan-Feb 2026) infiltrated ~1,200 malicious skills into a major marketplace, exfiltrating API keys, cryptocurrency wallets, and browser credentials
- **98,000+ skills** indexed by community registries with no centralized vetting

### Theme 4: Convergence of AI Agent and Human Labor Markets

A striking emergent theme is the convergence between AI agent skill marketplaces and traditional talent marketplaces:

- Chiu et al. (2025) model AI labor markets as **Competitive Skill-Based Stochastic Games** where LLM agents compete for jobs, develop skills, and adapt strategies — reproducing classic macroeconomic phenomena (monopolization, price deflation)
- Yang et al. (2025) propose **Agent Exchange (AEX)**, treating agents as economic actors in auction-based marketplaces inspired by RTB systems
- Sanabria & Vecino (2025) identify **four infrastructure gaps** preventing AI agents from functioning as autonomous market participants: identity, service discovery, interfaces, and payment

### Theme 5: Skill Transfer, Evolution, and Composability

Multiple papers address how skills propagate and evolve:

- **SkillFlow** (Tagkopoulos et al., 2025): Agents acquire skills from environment or other agents, analogous to **lateral gene transfer** in biology. 24.8% efficiency gains.
- **EvoSkill** (Alzubi et al., 2026): Self-evolving framework using iterative failure analysis and **Pareto frontier selection**. Demonstrates **zero-shot transfer** of evolved skills across tasks.
- **SkillNet** (Liang et al., 2026): Unified ontology for skills as **evolving, composable assets** with relational connections between 200K+ skills.

---

## 4. Novel Algorithms and Approaches

### 4.1 Skill Organization and Retrieval

| Algorithm/Approach | Paper | Description |
|-------------------|-------|-------------|
| **Capability Tree with Recursive Categorization** | AgentSkillOS (2603.02176) | Organizes skills into a hierarchical capability tree via node-level recursive categorization for efficient discovery at ecosystem scale (200K skills). |
| **DAG-based Pipeline Orchestration** | AgentSkillOS (2603.02176) | Retrieves, orchestrates, and executes multiple skills through directed acyclic graph pipelines. Substantially outperforms flat skill invocation. |
| **Bradley-Terry Model for Quality Scoring** | AgentSkillOS (2603.02176) | LLM-based pairwise evaluation aggregated via Bradley-Terry model to produce unified quality scores for skill-produced artifacts. |

### 4.2 Skill Discovery and Evolution

| Algorithm/Approach | Paper | Description |
|-------------------|-------|-------------|
| **Pareto Frontier Skill Selection** | EvoSkill (2603.02766) | Iterative failure analysis proposes new skills/edits; Pareto frontier governs selection, retaining only skills improving held-out validation while model stays frozen. |
| **Lateral Gene Transfer Framework** | SkillFlow (2504.06188) | Bio-inspired skill transfer between agents. Theoretical model determines when skill transfer is beneficial based on communication cost analysis. |
| **SEAgent (Autonomous Skill Discovery)** | Agent Skills Survey (2602.12430) | RL-based autonomous discovery of novel skills through environment exploration. |
| **Compositional Skill Synthesis** | Agent Skills Survey (2602.12430) | Synthesizing new skills by composing existing ones, including multi-agent to single-agent skill compilation. |

### 4.3 Security and Trust

| Algorithm/Approach | Paper | Description |
|-------------------|-------|-------------|
| **SkillScan** | Agent Skills in the Wild (2601.10338) | Multi-stage detection framework integrating static analysis with LLM-based semantic classification. 86.7% precision, 82.5% recall. |
| **SkillFortify** | Formal Analysis (2603.00195) | Formal verification framework: DY-Skill attacker model (Dolev-Yao adaptation), abstract interpretation, capability-based sandboxing with confinement proof, SAT-based dependency resolution. 96.95% F1. |
| **Trust Score Algebra** | Formal Analysis (2603.00195) | Formal monotonicity-guaranteed trust scoring for skill provenance tracking. |
| **Four-Tier Gate-Based Permission Model** | Agent Skills Survey (2602.12430) | Maps skill provenance to graduated deployment capabilities through four trust tiers. |

### 4.4 Talent/Skill Matching

| Algorithm/Approach | Paper | Description |
|-------------------|-------|-------------|
| **Custom Transformer with Contrastive Loss** | Skill Matching at Scale (2409.12097) | Neural retriever encoding project descriptions and freelancer profiles via pre-trained multilingual LMs. Structure-preserving custom transformer trained on historical match data. |
| **LinkSAGE (Graph Neural Network)** | LinkSAGE (2402.13430) | Industry-scale GNN operating on billion-node job marketplace graphs with diverse job-related attributes. |
| **RankPO (Rank Preference Optimization)** | RankPO (2503.10723) | Extension of Direct Preference Optimization (DPO) for job-talent ranking. Two-stage: contrastive learning + DPO fine-tuning. |
| **Temporal Knowledge Graph Completion** | Skill Demand Forecasting (2504.07233) | Skill need forecasting as temporal link prediction on knowledge graphs. |

### 4.5 Agent Economics

| Algorithm/Approach | Paper | Description |
|-------------------|-------|-------------|
| **AEX Auction Engine** | Agent Exchange (2507.03904) | RTB-inspired auction platform with four components: User-Side Platform (USP), Agent-Side Platform (ASP), Agent Hubs, and Data Management Platform (DMP). |
| **Competitive Skill-Based Stochastic Game** | Strategic Self-Improvement (2512.04988) | Game-theoretic model capturing adverse selection, moral hazard, and reputation dynamics for competing LLM agents in gig economies. |

---

## 5. Theoretical Frameworks for Skill Marketplaces

### 5.1 The Skill Lifecycle Framework (Jiang et al., 2026)

The most comprehensive theoretical framework maps seven lifecycle stages:

```
Discovery → Practice → Distillation → Storage → Composition → Evaluation → Update
```

Each stage has distinct research challenges:
- **Discovery**: How agents find relevant skills (marketplace search, recommendation, automated discovery)
- **Practice**: How skills are tested and validated before deployment
- **Distillation**: Compressing multi-step workflows into reusable modules
- **Storage**: Organizing and indexing skills for retrieval at scale
- **Composition**: Combining multiple skills for complex tasks (DAG-based, sequential, parallel)
- **Evaluation**: Measuring skill quality, safety, and effectiveness
- **Update**: Versioning, deprecation, and evolution of skills over time

### 5.2 Seven Design Patterns for Skill Packaging (Jiang et al., 2026)

1. **Metadata-driven progressive disclosure** — Skills reveal capabilities gradually based on context
2. **Executable code skills** — Packaged as runnable programs
3. **Self-evolving libraries** — Skills that improve through use
4. **Marketplace distribution** — Third-party skill sharing via registries
5. **Instruction-only skills** — Natural language procedural guides
6. **Hybrid skills** — Combining code and natural language
7. **Policy-based skills** — Decision-making frameworks

### 5.3 Representation x Scope Taxonomy (Jiang et al., 2026)

|  | Natural Language | Code | Policy | Hybrid |
|--|-----------------|------|--------|--------|
| **Web** | Y | Y | Y | Y |
| **OS** | Y | Y | Y | Y |
| **Software Engineering** | Y | Y | Y | Y |
| **Robotics** | Y | Y | Y | Y |

### 5.4 SCEMA Evaluation Framework (SkillNet, Liang et al., 2026)

Five-dimensional skill evaluation:
- **S**afety — Does the skill avoid harmful actions?
- **C**ompleteness — Does it cover the full task scope?
- **E**xecutability — Can it be reliably executed?
- **M**aintainability — Can it be updated and evolved?
- **A**cost-awareness — What are the resource costs?

### 5.5 Skill Trust and Lifecycle Governance Framework (Xu et al., 2026)

A four-tier, gate-based permission model:

| Tier | Trust Level | Capabilities |
|------|------------|--------------|
| Tier 1 | Unvetted | Read-only, sandboxed |
| Tier 2 | Community-reviewed | Limited write, monitored |
| Tier 3 | Verified publisher | Full capabilities, audited |
| Tier 4 | Platform-certified | Unrestricted, formally verified |

### 5.6 Agent-as-Economic-Actor Framework (Multiple papers)

Key infrastructure requirements for agent market participation (Sanabria & Vecino, 2025):
1. **Identity and authorization** — Agents need verifiable identities
2. **Service discovery** — Agents need to find each other's capabilities
3. **Interfaces** — Machine-readable API standards (MCP, Agent Protocol)
4. **Payment systems** — Programmatic value exchange

### 5.7 Competitive Skill-Based Stochastic Game (Chiu et al., 2025)

Three core capabilities for successful LLM-agents in labor markets:
1. **Metacognition** — Accurate self-assessment of skills
2. **Competitive awareness** — Modeling rivals and market dynamics
3. **Long-horizon strategic planning** — Skill development investment decisions

---

## 6. Security and Trust in Skill Marketplaces

### 6.1 Threat Landscape

The security research paints a concerning picture of current skill marketplaces:

**Vulnerability Categories (Liu et al., 2026):**
| Category | Prevalence | Description |
|----------|-----------|-------------|
| Data Exfiltration | 13.3% | Skills that transmit sensitive data to external endpoints |
| Privilege Escalation | 11.8% | Skills that attempt to gain unauthorized system access |
| Prompt Injection | ~5% | Skills containing adversarial prompt payloads |
| Supply Chain | ~5% | Dependency confusion, typosquatting, malicious dependencies |

**The ClawHavoc Campaign (Jan-Feb 2026):**
- ~1,200 malicious skills infiltrated the OpenClaw marketplace
- Exfiltrated API keys, cryptocurrency wallets, and browser credentials at scale
- Demonstrated the urgency of supply chain security for skill ecosystems

### 6.2 Formal Verification Approaches

**SkillFortify (Bhardwaj, 2026)** introduces six formal contributions:
1. **DY-Skill attacker model** — Dolev-Yao adaptation to five-phase skill lifecycle with maximality proof
2. **Sound static analysis** — Grounded in abstract interpretation
3. **Capability-based sandboxing** — With formal confinement proof
4. **Agent Dependency Graph** — SAT-based resolution with lockfile semantics (handles 1,000-node graphs in <100ms)
5. **Trust score algebra** — Formal monotonicity guarantees
6. **SkillFortifyBench** — 540-skill benchmark achieving 96.95% F1

---

## 7. Research Gaps and Future Directions

### 7.1 Gaps Identified Across the Literature

| Gap | Identified By | Description |
|-----|--------------|-------------|
| **Cross-platform skill portability** | Xu et al. (2602.12430) | Skills are currently tied to specific platforms (Claude, Codex, Gemini). No universal skill format exists. |
| **Capability-based permission models** | Liu et al. (2601.10338), Xu et al. | Current skills execute with implicit trust. Fine-grained, formal permission systems needed. |
| **Self-generated skill quality** | SkillsBench (2602.12670) | Models cannot reliably author the procedural knowledge they benefit from consuming. Why? |
| **Skill composition theory** | AgentSkillOS (2603.02176) | How to optimally compose skills from a large pool is under-explored. Current DAG-based approaches are a start. |
| **Economic models for skill markets** | AEX (2507.03904) | Pricing, incentive design, and revenue sharing for skill contributors remain open. |
| **Formal verification at scale** | Bhardwaj (2603.00195) | Current formal methods tested on 540 skills; scaling to 200K+ is unproven. |
| **Skill versioning and deprecation** | Multiple papers | No standard approach to managing skill versions, breaking changes, or deprecation. |
| **Multi-modal skills** | SoK (2602.20867) | Most skills are text-centric. Skills for vision, audio, and physical manipulation are nascent. |
| **Evaluation standardization** | SkillsBench (2602.12670) | No standard way to measure whether skills help. Effects vary wildly by domain (+4.5pp to +51.9pp). |
| **Supply-demand matching** | Ling et al. (2602.08004) | Pronounced imbalance between what is published and what is needed. No marketplace mechanisms to address this. |

### 7.2 Proposed Research Agenda (Aggregated)

1. **Universal Skill Specification** — A platform-agnostic skill format (beyond SKILL.md) that enables portability across Claude, Codex, Gemini, and open-source agents
2. **Skill Certification Pipeline** — Automated formal verification + human review for marketplace submissions
3. **Dynamic Skill Pricing** — Economic models that balance supply/demand and incentivize quality
4. **Compositional Skill Theory** — Formal frameworks for optimal skill combination, analogous to type theory in programming languages
5. **Adversarial Robustness** — Skills that remain secure under adversarial inputs and composition
6. **Longitudinal Studies** — Tracking skill ecosystem evolution over time (quality, diversity, security trends)
7. **Cross-ecosystem Transfer** — Moving skills between agent paradigms (web to robotics, code to natural language)

---

## 8. Connections to AI/ML Agent Ecosystems

### 8.1 Model Context Protocol (MCP) Integration

The MCP (Anthropic, 2025) standardizes agent-tool connections and is deeply intertwined with skill marketplaces:

- **Skills complement MCP**: Skills provide procedural knowledge (how to do things), while MCP provides tool access (what tools are available). Together they form the agent's capability layer.
- **SKILL.md + MCP**: The SKILL.md specification enables progressive context loading that integrates with MCP server definitions.
- **Marketplace implications**: MCP standardization enables skills to be portable across different agent platforms, a prerequisite for healthy marketplaces.

### 8.2 Key Agent Platforms Referenced

| Platform | Skills Indexed | Notes |
|----------|---------------|-------|
| OpenClaw (ClawHub) | 3,000+ (228K GitHub stars) | Largest open skill marketplace; target of ClawHavoc attack |
| Anthropic Agent Skills | 75,600 GitHub stars | SKILL.md standard, .claude/skills/ directory |
| skills.rest | 20,048 skills (64.4%) | Major marketplace registry |
| skillsmp.com | 11,084 skills (35.6%) | Second major marketplace registry |

### 8.3 Benchmark Connections

Skills are evaluated against major agent benchmarks:
- **ALFWorld** — Embodied task completion (SkillNet: +40% rewards)
- **WebShop** — E-commerce navigation
- **ScienceWorld** — Scientific reasoning
- **OSWorld** — Operating system tasks
- **SWE-bench** — Software engineering tasks
- **OfficeQA** — Grounded reasoning (EvoSkill: +7.3%)
- **BrowseComp** — Browser-based computation (EvoSkill: +5.3% zero-shot transfer)

### 8.4 Analogies to Software Ecosystems

The literature draws explicit parallels:

| Software Ecosystem | Skill Ecosystem Analog |
|-------------------|----------------------|
| npm/PyPI package registries | Skill marketplaces (skills.rest, skillsmp.com) |
| Package.json / requirements.txt | Skill manifest / SKILL.md |
| npm audit / Dependabot | SkillScan / SkillFortify |
| Semantic versioning | Skill versioning (proposed, not standardized) |
| Container sandboxing | Capability-based skill sandboxing |
| CI/CD pipelines | Skill certification pipelines |
| Package signing | Trust score algebra |

### 8.5 Biological Analogies

SkillFlow (Tagkopoulos et al., 2025) introduces a compelling biological framework:
- **Skill transfer between agents = Lateral gene transfer** in bacteria
- Skills as "genetic material" that can be shared, acquired, and evolved
- Communication cost determines when transfer is beneficial (analogous to fitness cost of gene transfer)
- Evolution through iterative failure analysis (EvoSkill) parallels natural selection

---

## 9. Synthesis and Implications

### 9.1 The State of the Field

The skill marketplace research landscape is **nascent but rapidly accelerating**. The vast majority of papers in the AI agent skill domain are from **2025-2026**, with a particular explosion in **February-March 2026** following the widespread adoption of Claude's SKILL.md specification in late 2025. The field has already produced:

- **3 comprehensive surveys** (SoK, Agent Skills for LLMs, SkillNet)
- **2 ecosystem-scale frameworks** (AgentSkillOS, SkillNet)
- **3 security analyses** (Agent Skills in the Wild, Malicious Agent Skills, SkillFortify)
- **2 benchmarks** (SkillsBench, SkillFortifyBench)
- **2 economic/marketplace designs** (AEX, Beyond the Sum)

### 9.2 Critical Insight: The Curation Paradox

Perhaps the most striking finding across the literature is the **curation paradox**: curated skills substantially improve agent performance (+16.2pp average, up to +51.9pp in healthcare), yet agents cannot reliably generate high-quality skills themselves. This implies that **human expertise remains essential** in skill creation, and that marketplaces must develop quality signals and curation mechanisms rather than relying on automated generation.

### 9.3 The Security-Utility Tension

The literature reveals a fundamental tension: the same openness that makes skill marketplaces useful (easy contribution, broad distribution) also makes them vulnerable. With 26.1% of skills containing vulnerabilities and campaigns like ClawHavoc demonstrating real-world exploitation, the field faces a classic security-utility tradeoff that will shape marketplace design.

### 9.4 Convergence of Agent and Human Labor Markets

The most forward-looking papers suggest that AI agent skill marketplaces and human freelance marketplaces are **converging into a unified digital labor economy**. Chiu et al.'s simulations show that agent labor markets naturally reproduce human macroeconomic phenomena (monopolization, price deflation), suggesting that economic theory developed for human markets may be directly applicable to agent markets — and vice versa.

### 9.5 Implications for Marketplace Design

Based on the surveyed literature, a well-designed skill marketplace should incorporate:

1. **Hierarchical organization** (capability trees, not flat lists)
2. **Formal verification** (not just heuristic scanning)
3. **Tiered trust** (graduated permissions based on provenance)
4. **Composition support** (DAG-based orchestration, not just individual skill invocation)
5. **Quality signals** (multi-dimensional evaluation: Safety, Completeness, Executability, Maintainability, Cost)
6. **Economic mechanisms** (auction-based matching, dynamic pricing, contributor incentives)
7. **Cross-platform portability** (universal skill specifications beyond any single vendor)
8. **Ecosystem health metrics** (supply-demand balance, diversity, redundancy monitoring)

---

*Report generated from 5 DuckDuckGo searches across arXiv, covering 38 unique papers with 14 deeply analyzed via full abstract scraping.*
