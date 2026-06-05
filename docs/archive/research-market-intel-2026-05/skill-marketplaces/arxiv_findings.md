# arXiv Research Findings: Skill Marketplaces

> **Generated:** July 2025  
> **Search Method:** DuckDuckGo site-restricted search (9 queries) + arXiv direct search (3 queries) + individual paper scraping (24 papers)  
> **Total unique papers found:** 30+ across AI agent skill ecosystems, talent/freelance marketplaces, two-sided market design, and gig economy matching

---

## Table of Contents

1. [Category A: AI Agent Skill Marketplaces & Ecosystems](#category-a-ai-agent-skill-marketplaces--ecosystems)
2. [Category B: Agent Marketplace Economics & Auction Design](#category-b-agent-marketplace-economics--auction-design)
3. [Category C: Skill Marketplace Security & Trust](#category-c-skill-marketplace-security--trust)
4. [Category D: Tool/Skill Selection & Fairness in Marketplaces](#category-d-toolskill-selection--fairness-in-marketplaces)
5. [Category E: Freelance & Talent Marketplace Matching](#category-e-freelance--talent-marketplace-matching)
6. [Category F: Two-Sided Market Design & Theory](#category-f-two-sided-market-design--theory)
7. [Category G: Gig Economy Platforms & Matching Algorithms](#category-g-gig-economy-platforms--matching-algorithms)
8. [Category H: Decentralized Multi-Agent Coordination](#category-h-decentralized-multi-agent-coordination)
9. [Category I: Skill Extraction & Labor Market Intelligence](#category-i-skill-extraction--labor-market-intelligence)
10. [Key Themes & Insights](#key-themes--insights)
11. [Search Queries Used](#search-queries-used)

---

## Category A: AI Agent Skill Marketplaces & Ecosystems

### 1. AgentSkillOS: Organizing, Orchestrating, and Benchmarking Agent Skills at Ecosystem Scale

- **arXiv ID:** [2603.02176](https://arxiv.org/abs/2603.02176)
- **Authors:** Hao Li, Chunjiang Mu, Jianhao Chen, Siyue Ren, Zhiyao Cui, Yiqun Zhang, Lei Bai, Shuyue Hu
- **Date:** March 2, 2026
- **Category:** cs.CL (Computation and Language)
- **License:** CC BY 4.0

**Abstract:** The rapid proliferation of Claude agent skills has raised the central question of how to effectively leverage, manage, and scale the agent skill ecosystem. This paper proposes AgentSkillOS, the first principled framework for skill selection, orchestration, and ecosystem-level management. AgentSkillOS comprises two stages: (i) Manage Skills, which organizes skills into a capability tree via node-level recursive categorization for efficient discovery; and (ii) Solve Tasks, which retrieves, orchestrates, and executes multiple skills through DAG-based pipelines. Experiments across three skill ecosystem scales (200 to 200K skills) show that tree-based retrieval effectively approximates oracle skill selection, and that DAG-based orchestration substantially outperforms native flat invocation even when given the identical skill set.

**Key Contributions:**
- First principled framework for skill selection, orchestration, and ecosystem-level management
- Capability-tree-based organization for efficient skill discovery
- DAG-based multi-skill orchestration pipelines
- Benchmark of 30 artifact-rich tasks across 5 categories
- Scales from 200 to 200K skills effectively

**Relevance:** *Extremely high* -- Directly addresses skill marketplace organization and orchestration at ecosystem scale. The capability tree and DAG orchestration patterns are directly applicable to skill marketplace design.

**GitHub:** https://github.com/ynulihao/AgentSkillOS

---

### 2. SkillNet: Create, Evaluate, and Connect AI Skills

- **arXiv ID:** [2603.04448](https://arxiv.org/abs/2603.04448)
- **Authors:** Yuan Liang, Ruobin Zhong, Haoming Xu, Chen Jiang, Fang Yi, Runnan Gu, Shumin Deng, Yunzhi Yao, et al. (30+ authors)
- **Date:** February 26, 2026
- **Category:** cs.AI (Artificial Intelligence)

**Abstract:** Current AI agents can flexibly invoke tools and execute complex tasks, yet their long-term advancement is hindered by the lack of systematic accumulation and transfer of skills. Without a unified mechanism for skill consolidation, agents frequently "reinvent the wheel", rediscovering solutions in isolated contexts without leveraging prior strategies. SkillNet is an open infrastructure designed to create, evaluate, and organize AI skills at scale. It structures skills within a unified ontology that supports creating skills from heterogeneous sources, establishing rich relational connections, and performing multi-dimensional evaluation across Safety, Completeness, Executability, Maintainability, and Cost-awareness. The infrastructure integrates a repository of over 200,000 skills, an interactive platform, and a versatile Python toolkit.

**Key Contributions:**
- Unified ontology for skill creation, evaluation, and organization
- Multi-dimensional evaluation framework (Safety, Completeness, Executability, Maintainability, Cost-awareness)
- Repository of 200,000+ skills with an interactive platform
- 40% improvement in average rewards, 30% reduction in execution steps across multiple backbone models
- Skills formalized as evolving, composable assets

**Relevance:** *Extremely high* -- Directly defines the infrastructure for a skill marketplace with evaluation, organization, and discovery. The SECEM evaluation framework and skill ontology are foundational for marketplace quality assurance.

---

### 3. Agent Skills: A Data-Driven Analysis of Claude Skills for Extending LLM Functionality

- **arXiv ID:** [2602.08004](https://arxiv.org/abs/2602.08004)
- **Authors:** (Multiple authors)
- **Date:** February 8, 2026
- **Category:** cs.AI

**Abstract:** Agent skills extend large language model (LLM) agents with reusable, program-like modules that define triggering conditions, procedural logic, and tool interactions. As these skills proliferate in public marketplaces, it is unclear what types are available, how users adopt them, and what risks they pose. This paper conducts a large-scale, data-driven analysis of 40,285 publicly listed skills from a major marketplace (skills.sh).

**Key Contributions:**
- First large-scale empirical analysis of a real agent skill marketplace (40,285 skills)
- Taxonomy of skill types and adoption patterns
- Risk analysis of publicly distributed skills
- Dataset constructed by crawling the skills.sh marketplace

**Relevance:** *Extremely high* -- The only paper that empirically analyzes an existing, real-world skill marketplace at scale. Provides essential data on what kinds of skills are created, how they're adopted, and what risks emerge.

---

### 4. SoK: Agentic Skills -- Beyond Tool Use in LLM Agents

- **arXiv ID:** [2602.20867](https://arxiv.org/abs/2602.20867)
- **Authors:** Yanna Jiang, Delong Li, Haiyu Deng, Baihe Ma, Xu Wang, Yu Qin, Guangsheng
- **Date:** February 24, 2026
- **Category:** cs.CR (Cryptography and Security)
- **License:** CC BY 4.0

**Abstract:** This paper maps the skill layer across the full lifecycle (discovery, practice, distillation, storage, composition, evaluation, and update) and introduces two complementary taxonomies. The first is a system-level set of seven design patterns capturing how skills are packaged and executed in practice, from metadata-driven progressive disclosure and executable code skills to self-evolving libraries and marketplace distribution. The second is an orthogonal representation x scope taxonomy. Includes a case study of the ClawHavoc campaign in which nearly 1,200 malicious skills infiltrated a major agent marketplace.

**Key Contributions:**
- Full lifecycle mapping of agentic skills: discovery, practice, distillation, storage, composition, evaluation, update
- Seven design patterns for skill packaging and execution
- Representation x scope taxonomy (natural language, code, policy, hybrid)
- Security analysis including ClawHavoc campaign case study
- Marketplace distribution as a key design pattern

**Relevance:** *Extremely high* -- The definitive systematization of knowledge (SoK) paper for agentic skills. The marketplace distribution pattern and full lifecycle analysis are directly foundational for skill marketplace architecture.

---

### 5. SkillFlow: Efficient Skill and Code Transfer Through Communication in Adapting AI Agents

- **arXiv ID:** [2504.06188](https://arxiv.org/abs/2504.06188)
- **Authors:** Pagkratios Tagkopoulos, Fangzhou Li, Ilias Tagkopoulos
- **Date:** April 8, 2025
- **Category:** cs.AI
- **License:** CC BY-NC-ND 4.0

**Abstract:** SkillFlow is a modular, technology-agnostic framework that allows agents to expand their functionality in an ad-hoc fashion by acquiring new skills from their environment or other agents. A theoretical model examines under which conditions this framework would be beneficial, with real-world application in scheduling agents for calendar events. SkillFlow leads to considerable (24.8%, p-value = 6.4x10^-3) gains in time and cost, especially when communication cost is high. Draws analogies to lateral gene transfer in biological systems.

**Key Contributions:**
- Framework for peer-to-peer skill transfer between agents
- Theoretical model for when skill exchange is beneficial
- 24.8% efficiency gains demonstrated in scheduling tasks
- Biological analogy to lateral gene transfer for skill propagation

**Relevance:** *High* -- Models the dynamics of skill exchange between agents, directly relevant to marketplace mechanics of how skills propagate and get adopted.

---

### 6. COALESCE: Economic and Security Dynamics of Skill-Based Task Outsourcing Among Autonomous LLM Agents

- **arXiv ID:** [2506.01900](https://arxiv.org/abs/2506.01900)
- **Authors:** Manish Bhatt, Ronald F. Del Rosario, Vineeth Sai Narajala, Idan Habler
- **Date:** June 2, 2025
- **Category:** cs.AI
- **License:** CC BY 4.0

**Abstract:** COALESCE (Cost-Optimized and Secure Agent Labour Exchange via Skill-based Competence Estimation) is a novel framework enabling autonomous LLM agents to dynamically outsource specific subtasks to specialized, cost-effective third-party LLM agents. Integrates hybrid skill representation, dynamic skill discovery, automated task decomposition, a unified cost model, market-based decision-making algorithms, and standardized communication protocol. Validation through 239 theoretical simulations demonstrates 41.8% cost reduction potential; 240 real LLM tasks confirms 20.3% cost reduction.

**Key Contributions:**
- Dynamic marketplace for agent capabilities with cost optimization
- Hybrid skill representation and dynamic skill discovery
- Unified cost model comparing internal vs. external execution
- Market-based decision-making algorithms
- Leverages Google's Agent2Agent (A2A) protocol
- 41.8% theoretical / 20.3% empirical cost reduction

**Relevance:** *Extremely high* -- Directly implements a skill marketplace where LLM agents outsource tasks to specialized agents. The economics (cost models, pricing) and skill discovery mechanisms are directly applicable.

---

## Category B: Agent Marketplace Economics & Auction Design

### 7. Agent Exchange (AEX): Shaping the Future of AI Agent Economics

- **arXiv ID:** [2507.03904](https://arxiv.org/abs/2507.03904)
- **Authors:** Yingxuan Yang, Ying Wen, Jun Wang, Weinan Zhang
- **Date:** July 5, 2025
- **Category:** cs.AI
- **License:** CC BY 4.0
- **Citations:** 9

**Abstract:** The rise of LLMs has transformed AI agents from passive computational tools into autonomous economic actors. We propose Agent Exchange (AEX), a specialized auction platform designed to support the dynamics of the AI agent marketplace. AEX offers optimized infrastructure for agent coordination and economic participation. Inspired by Real-Time Bidding (RTB) in online advertising, AEX serves as the central auction engine, facilitating interactions among: User-Side Platform (USP), Agent-Side Platform (ASP), Agent Hubs, and Data Management Platform (DMP).

**Key Contributions:**
- First formal auction platform design for AI agent marketplace
- Four-component architecture: USP, ASP, Agent Hubs, DMP
- Real-Time Bidding (RTB) adaptation for agent services
- Agent capability representation and performance tracking
- Secure knowledge sharing and fair value attribution

**Relevance:** *Extremely high* -- The most directly relevant paper for skill marketplace design. Provides the economic infrastructure (auction mechanisms, platform architecture) for an AI agent marketplace.

---

### 8. Magentic Marketplace: An Open-Source Environment for Studying Agentic Markets

- **arXiv ID:** [2510.25779](https://arxiv.org/abs/2510.25779)
- **Authors:** G. Bansal et al.
- **Date:** October 2025
- **Category:** cs.AI
- **Citations:** 1

**Abstract:** Investigates two-sided agentic marketplaces where Assistant agents represent consumers and Service agents represent providers. Provides an open-source simulation environment to answer questions such as: How effectively can agents discover and transact with one another? How do marketplace dynamics emerge?

**Key Contributions:**
- Open-source simulation environment for two-sided agentic marketplaces
- Models agent discovery and transaction dynamics
- Studies how marketplace equilibria emerge with AI agents

**Relevance:** *Extremely high* -- Directly studies two-sided agentic marketplaces, providing simulation infrastructure and empirical insights into marketplace dynamics.

---

### 9. What Is Your AI Agent Buying? Evaluation, Biases, Model Dependence, & Implications for Agentic E-Commerce

- **arXiv ID:** [2508.02630](https://arxiv.org/abs/2508.02630)
- **Authors:** Amine Allouah, Omar Besbes, Josue D. Figueroa, Yash Kanoria, Akshit Kumar
- **Date:** August 4, 2025 (v3: December 17, 2025)
- **Category:** cs.AI
- **License:** CC BY 4.0
- **Citations:** 2

**Abstract:** Online marketplaces will be transformed by autonomous AI agents acting on behalf of consumers. Investigates agent behavior using ACES, a provider-agnostic auditing framework. Reveals agents exhibit choice homogeneity (concentrating demand on few products), unstable preferences (model updates reshuffle market shares), position biases, and demonstrates that sellers can respond with agent-optimized descriptions.

**Key Contributions:**
- ACES: provider-agnostic framework for auditing agent decision-making in marketplaces
- Identifies choice homogeneity, position bias, and model-dependent preferences
- Shows seller-side agents can game the marketplace
- Demonstrates agentic markets are fundamentally different from human-centric commerce

**Relevance:** *High* -- Studies how AI agents behave as marketplace participants, revealing critical design challenges (bias, gaming, instability) that any skill marketplace must address.

---

### 10. LLM-based Multi-Agent System for Simulating Strategic and Goal-Oriented Data Marketplaces

- **arXiv ID:** [2511.13233](https://arxiv.org/abs/2511.13233)
- **Authors:** Jun Sashihara, Yukihisa Fujita, Kota Nakamura, Masahiro Kuwahara, Teruaki Hayashi
- **Date:** November 17, 2025
- **Category:** cs.MA (Multiagent Systems)
- **License:** CC BY 4.0

**Abstract:** Proposes an LLM-MAS for data marketplaces where buyer and seller agents autonomously perform strategic actions (planning, searching, purchasing, pricing, updating). Agents reason about market dynamics, forecast demand, and adjust strategies. Demonstrates more faithful reproduction of real marketplace trading patterns compared to traditional approaches.

**Key Contributions:**
- LLM-powered buyer/seller agents with autonomous marketplace behavior
- Strategic actions: planning, searching, purchasing, pricing, updating
- Market dynamics reasoning and demand forecasting
- More realistic marketplace simulation than rule-based approaches

**Relevance:** *High* -- The marketplace simulation patterns (agent pricing, search, purchasing strategies) are directly applicable to skill marketplace dynamics.

---

## Category C: Skill Marketplace Security & Trust

### 11. Formal Analysis and Supply Chain Security for Agentic AI Skills

- **arXiv ID:** [2603.00195](https://arxiv.org/abs/2603.00195)
- **Authors:** Varun Pratap Bhardwaj
- **Date:** February 27, 2026
- **Category:** cs.CR
- **License:** CC BY 4.0

**Abstract:** The ClawHavoc campaign (January-February 2026) infiltrated over 1,200 malicious skills into the OpenClaw marketplace, while MalTool catalogued 6,487 malicious tools evading conventional detection. Presents SkillFortify, the first formal analysis framework for agent skill supply chains with: DY-Skill attacker model (Dolev-Yao adaptation), sound static analysis, capability-based sandboxing, Agent Dependency Graph with SAT-based resolution, trust score algebra, and SkillFortifyBench (540-skill benchmark). Achieves 96.95% F1 with 100% precision.

**Key Contributions:**
- DY-Skill attacker model for five-phase skill lifecycle
- Formal verification framework achieving 96.95% F1
- Capability-based sandboxing with confinement proofs
- Trust score algebra with formal monotonicity
- Agent Dependency Graph with SAT-based resolution

**Relevance:** *Extremely high* -- Security is critical for any skill marketplace. This paper provides the formal security framework needed for skill vetting, trust scoring, and supply chain protection.

**GitHub:** https://github.com/varun369/skillfortify

---

### 12. Agent Skills in the Wild: An Empirical Study of Security Vulnerabilities at Scale

- **arXiv ID:** [2601.10338](https://arxiv.org/abs/2601.10338)
- **Authors:** Yi Liu, Weizhe Wang, Ruitao Feng, Yao Zhang, Guangquan Xu, Gelei Deng, Yuekang Li, Leo
- **Date:** January 15, 2026
- **Category:** cs.CR
- **License:** CC BY 4.0

**Abstract:** First large-scale empirical security analysis of the agent skill ecosystem. Collected 42,447 skills from two major marketplaces, analyzed 31,132 using SkillScan (multi-stage detection framework). Findings: 26.1% of skills contain at least one vulnerability across 14 patterns in 4 categories (prompt injection, data exfiltration, privilege escalation, supply chain risks). Data exfiltration (13.3%) and privilege escalation (11.8%) most prevalent; 5.2% show high-severity malicious patterns.

**Key Contributions:**
- First large-scale security analysis: 42,447 skills from two marketplaces
- SkillScan: multi-stage detection framework (86.7% precision, 82.5% recall)
- Vulnerability taxonomy: 14 patterns across 4 categories
- 26.1% of skills contain vulnerabilities; 5.2% appear malicious
- Skills with executable scripts 2.12x more likely to be vulnerable

**Relevance:** *Extremely high* -- Quantifies the security risks in real skill marketplaces. Essential for designing trust and safety systems in any new marketplace.

---

### 13. Agent Skills Enable a New Class of Realistic and Trivially Simple Prompt Injection Attacks

- **arXiv ID:** [2510.26328](https://arxiv.org/abs/2510.26328)
- **Authors:** (Multiple authors)
- **Date:** October 30, 2025

**Abstract:** Agent Skills enable an agent to dynamically include knowledge related to different tasks and environments in their context window. This paper demonstrates how skills create new attack vectors for prompt injection.

**Key Contributions:**
- Identifies skills as a novel prompt injection attack surface
- Demonstrates trivially simple attack vectors through skill marketplace distribution

**Relevance:** *High* -- Important security consideration for skill marketplace design.

---

## Category D: Tool/Skill Selection & Fairness in Marketplaces

### 14. ToolTweak: An Attack on Tool Selection in LLM-based Agents

- **arXiv ID:** [2510.02554](https://arxiv.org/abs/2510.02554)
- **Authors:** Jonathan Sneh, Ruomei Yan, Jialin Yu, Philip Torr, Yarin Gal, Sunando Sengupta, Eric Sommerlade, Alasdair Paren, Adel Bibi
- **Date:** October 2, 2025
- **Category:** cs.CR

**Abstract:** Shows that the tool selection process in LLM agents harbors a critical vulnerability: adversaries can manipulate tool names and descriptions to bias agents toward selecting specific tools. ToolTweak increases selection rates from ~20% baseline to 81%, with strong transferability between models. Reveals risks to fairness, competition, and security in emerging tool ecosystems.

**Key Contributions:**
- Demonstrates tool selection manipulation attacks in marketplace settings
- 20% -> 81% selection rate through adversarial name/description optimization
- Strong cross-model transferability
- Defenses: paraphrasing and perplexity filtering
- Reveals competition and fairness risks in tool marketplaces

**Relevance:** *High* -- Directly addresses the fairness and competition challenges in tool/skill marketplaces where providers compete for selection.

---

### 15. BiasBusters: Uncovering and Mitigating Tool Selection Bias in Large Language Models

- **arXiv ID:** [2510.00307](https://arxiv.org/abs/2510.00307)
- **Authors:** Thierry Blankenstein, Jialin Yu, Zixuan Li, Vassilis Plachouras, Sunando Sengupta, Philip Torr, Yarin Gal, Alasdair Paren, Adel Bibi
- **Date:** September 30, 2025 (v2: March 10, 2026)
- **Category:** cs.AI

**Abstract:** LLM agents increasingly rely on external tools drawn from marketplaces where multiple providers offer functionally equivalent options. Introduces a benchmark for evaluating tool-selection bias across 7 LLMs. Findings: (1) semantic alignment between queries and tool metadata is the strongest selection driver; (2) small description perturbations significantly shift choices; (3) repeated pre-training exposure amplifies provider-level bias. Proposes a filter-then-sample mitigation strategy.

**Key Contributions:**
- Benchmark for evaluating tool selection bias in marketplace settings
- Three root causes of bias identified (semantic alignment, description sensitivity, pre-training exposure)
- Lightweight filter-then-sample mitigation strategy
- Open-source code and benchmark

**Relevance:** *High* -- Essential for ensuring fair competition among skill providers in a marketplace setting.

**GitHub:** https://github.com/thierry123454/tool-selection-bias

---

## Category E: Freelance & Talent Marketplace Matching

### 16. GraphMatch: Fusing Language and Graph Representations in a Dynamic Two-Sided Work Marketplace

- **arXiv ID:** [2512.02849](https://arxiv.org/abs/2512.02849)
- **Authors:** Mikolaj Sacha, Hammad Jafri, Mattie Terzolo, Ayan Sinha, Andrew Rabinovich
- **Date:** December 2, 2025
- **Category:** cs.LG (Machine Learning)

**Abstract:** Introduces GraphMatch, a large-scale recommendation framework that fuses pre-trained language models with graph neural networks for matching in a text-rich, dynamic two-sided marketplace. Employs adversarial negative sampling and point-in-time subgraph training. Evaluated on Upwork interaction data at large scale. Outperforms language-only and graph-only baselines.

**Key Contributions:**
- Fuses LLMs with GNNs for two-sided marketplace matching
- Adversarial negative sampling with temporal awareness
- Deployed on Upwork labor marketplace at scale
- Low-latency inference for real-time use
- Bridges pretrained LMs and large-scale graph representations

**Relevance:** *Very high* -- State-of-the-art matching algorithm for a real freelance marketplace (Upwork). The LLM + GNN approach is directly applicable to skill marketplace matching.

---

### 17. Talent Search and Recommendation Systems at LinkedIn

- **arXiv ID:** [1809.06481](https://arxiv.org/abs/1809.06481)
- **Authors:** Sahin Cem Geyik, Qi Guo, Bo Hu, Cagri Ozcaglar, Ketan Thakkar, Xianren Wu, Krishnaram Kenthapadi
- **Date:** September 18, 2018
- **Category:** cs.AI

**Abstract:** LinkedIn Talent Solutions contributes ~65% of LinkedIn's annual revenue. The job ecosystem is designed as a platform to connect job providers and job seekers, serving as a marketplace for efficient matching. Highlights unique information retrieval, system, and modeling challenges associated with talent search and recommendation at scale.

**Key Contributions:**
- Production system design for talent marketplace at LinkedIn scale
- Information retrieval challenges for skill-based matching
- Marketplace efficiency through recommendation systems
- Lessons learned from 65% revenue-generating business

**Relevance:** *High* -- The canonical industry paper on talent marketplace search and recommendation. Provides practical design patterns from the world's largest professional talent marketplace.

---

### 18. UpBench: A Dynamically Evolving Real-World Labor-Market Agentic Benchmark

- **arXiv ID:** [2511.12306](https://arxiv.org/abs/2511.12306)
- **Authors:** Darvin Yi, Teng Liu, Mattie Terzolo, Lance Hasson, Ayan Sinha, Pablo Mendes, Andrew Rabinovich
- **Date:** November 15, 2025 (v2: December 12, 2025)
- **Category:** cs.AI

**Abstract:** UpBench is a dynamically evolving benchmark grounded in real jobs from the Upwork labor marketplace. 322 real, economically verified jobs where expert freelancers create rubric-based evaluation criteria. Provides a scalable, human-centered foundation for evaluating agentic systems in authentic labor-market contexts.

**Key Contributions:**
- Real-world benchmark from Upwork marketplace (322 verified jobs)
- Rubric-based evaluation by expert freelancers
- Dynamic task refresh reflecting evolving labor market
- Evaluates AI agents on real professional tasks

**Relevance:** *High* -- Provides benchmarking methodology for evaluating AI agents in marketplace contexts. The rubric-based evaluation approach is applicable to skill quality assessment.

---

### 19. Unmasking Hiring Bias: Platform Data Analysis and Controlled Experiments on Bias in Online Freelance Marketplaces

- **arXiv ID:** [2510.13091](https://arxiv.org/abs/2510.13091)
- **Authors:** (Multiple authors)
- **Date:** October 14, 2025
- **Category:** cs.CY

**Abstract:** Online freelance marketplaces are creating environments where professional skills should be the main hiring factor. Analyzes bias in these platforms using RAG-LLM generated content, examining whether personal information in profiles leads to discrimination.

**Key Contributions:**
- Empirical analysis of hiring bias in freelance marketplaces
- RAG-LLM methodology for controlled bias experiments
- Skills as the primary hiring criterion in ideal marketplaces

**Relevance:** *Medium-high* -- Addresses fairness in skill-based marketplace matching, important for equitable marketplace design.

---

### 20. Evaluating LLM Behavior in Hiring: Implicit Weights, Fairness Across Groups

- **arXiv ID:** [2601.11379](https://arxiv.org/abs/2601.11379)
- **Authors:** (Multiple authors)
- **Date:** January 16, 2026

**Abstract:** Builds synthetic datasets from real freelancer profiles and project descriptions from a major European online freelance marketplace. Uses full factorial design to estimate how LLMs weigh different match-relevant criteria when evaluating freelancer-project fit.

**Key Contributions:**
- Reveals how LLMs implicitly weight different matching criteria
- Full factorial design for analyzing LLM hiring behavior
- Based on real European freelance marketplace data

**Relevance:** *Medium* -- Understanding LLM biases in marketplace matching is important for AI-driven skill marketplaces.

---

### 21. FaMA: LLM-Empowered Agentic Assistant for Consumer-to-Consumer Marketplace

- **arXiv ID:** [2509.03890](https://arxiv.org/abs/2509.03890)
- **Authors:** Yineng Yan, Xidong Wang, Jin Seng Cheng, Ran Hu, Wentao Guan, Nahid Farahmand, Hengte Lin, Yue Li
- **Date:** September 4, 2025
- **Category:** cs.AI
- **License:** CC BY 4.0
- **Citations:** 2

**Abstract:** Facebook Marketplace Assistant (FaMA) is an LLM-powered agentic assistant that serves as a conversational entry point to a C2C marketplace. Shifts the primary interaction model from complex GUI to intuitive AI agent. Automates high-friction workflows for sellers (listing updates, bulk messages) and buyers (conversational search). Achieves 98% task success rate and up to 2x speedup.

**Key Contributions:**
- Conversational AI interface for marketplace interactions
- 98% task success rate on marketplace tasks
- 2x speedup in interaction time
- Shifts marketplace UX from GUI to conversational agent

**Relevance:** *Medium-high* -- Demonstrates how AI agents can serve as marketplace interfaces, relevant to UX design of skill marketplaces.

---

### 22. Algorithms for Fair Team Formation in Online Labour Marketplaces

- **arXiv ID:** [2002.11621](https://arxiv.org/abs/2002.11621)
- **Authors:** Giorgio Barnabo, Adriano Fazzone, Stefano Leonardi, Chris Schwiegelshohn
- **Date:** February 14, 2020
- **Category:** cs.CY
- **Venue:** WWW 2019 / FATES 2019

**Abstract:** Defines the Fair Team Formation problem: given an online labour marketplace where workers possess skills and belong to demographic classes, find a team with all required skills while maintaining equal class representation. Provides inapproximability results and four algorithms, tested on real marketplace data.

**Key Contributions:**
- Formal definition of Fair Team Formation in skill marketplaces
- Inapproximability results for the general problem
- Four practical algorithms with real-world evaluation
- Fairness constraints in skill-based team assembly

**Relevance:** *High* -- Directly addresses skill-based team formation with fairness constraints in online labor marketplaces.

---

### 23. Algorithms for Hiring and Outsourcing in the Online Labor Market

- **arXiv ID:** [2002.07618](https://arxiv.org/abs/2002.07618)
- **Authors:** (Multiple authors)
- **Date:** February 16, 2020
- **Venue:** KDD 2018

**Abstract:** Studies the coexistence of freelancing and salaried employment, designing algorithms for when to hire versus outsource in online labor marketplaces.

**Key Contributions:**
- Algorithms for hire-vs-outsource decisions
- Practical marketplace task allocation strategies

**Relevance:** *Medium* -- The hire-vs-outsource framework applies to decisions about using marketplace skills vs. building in-house.

---

## Category F: Two-Sided Market Design & Theory

### 24. A Framework for Fairness in Two-Sided Marketplaces

- **arXiv ID:** [2006.12756](https://arxiv.org/abs/2006.12756)
- **Authors:** Kinjal Basu, Cyrus DiCiccio, Heloise Logan, Noureddine El Karoui
- **Date:** June 23, 2020
- **Category:** cs.AI
- **Citations:** 17

**Abstract:** Proposes a definition and end-to-end framework for achieving fairness in two-sided marketplaces at scale. Develops an optimization framework handling fairness constraints from both source and destination sides, as well as dynamic aspects. Applicable to job recommendations, recruiter searches, and similar matching problems.

**Key Contributions:**
- Formal fairness definition for two-sided marketplaces
- Optimization framework for dual-sided fairness constraints
- Dynamic fairness handling at scale
- Applicable to job/talent marketplace settings

**Relevance:** *High* -- Foundational fairness framework directly applicable to skill marketplaces that must balance provider and consumer interests.

---

### 25. Integrating Predictive Models into Two-Sided Recommendations: A Matching-Theoretic Approach

- **arXiv ID:** [2602.19689](https://arxiv.org/abs/2602.19689)
- **Authors:** Kazuki Sekiya, Suguru Otani, Yuki Komatsu, Sachio Ohkawa, Shunya Noda
- **Date:** February 23, 2026
- **Category:** econ.GN
- **License:** CC BY 4.0

**Abstract:** Two-sided platforms must recommend users to users where matches require mutual interest. Proposes exposure-constrained deferred acceptance (ECDA) that limits receiver exposure, using congestion-adjusted metrics. Field experiment confirms improved equity and matching efficiency.

**Key Contributions:**
- Exposure-constrained deferred acceptance (ECDA) algorithm
- Congestion-adjusted matching metrics
- Field experiment validation on a large platform
- Matching theory applied to two-sided recommendations

**Relevance:** *Medium-high* -- The matching-theoretic approach and congestion management are directly applicable to skill marketplace matching where popular providers get overloaded.

---

### 26. Online Two-Sided Markets: Many Buyers Enhance Learning

- **arXiv ID:** [2503.01529](https://arxiv.org/abs/2503.01529)
- **Authors:** (Multiple authors)
- **Date:** March 3-5, 2025

**Abstract:** Studies repeated trading in two-sided markets with single seller and multiple buyers. Generalizes bilateral trade to multi-buyer environments, showing how more buyers improve mechanism designer's learning and matching efficiency.

**Key Contributions:**
- Multi-buyer extensions to bilateral trade mechanisms
- Information learning advantages of larger buyer pools
- Theoretical foundations for marketplace scaling

**Relevance:** *Medium* -- Theoretical foundations for understanding how marketplace growth improves matching.

---

## Category G: Gig Economy Platforms & Matching Algorithms

### 27. Tight Competitive and Variance Analyses of Matching Policies in Gig Platforms

- **arXiv ID:** [2401.13842](https://arxiv.org/abs/2401.13842)
- **Authors:** P. Xu et al.
- **Date:** January 24, 2024
- **Citations:** 3

**Abstract:** Introduces a stochastic optimization model for matching and pricing in gig economy platforms. Initiates variance analysis for online matching algorithms under Known Heterogeneous Distribution (KHD). Addresses the tension between instant matching (low patience) and optimal allocation.

**Key Contributions:**
- Stochastic optimization model for matching and pricing
- First variance analysis for online matching algorithms
- Addresses real-time matching with low-patience agents
- Applicable to gig economy platforms broadly

**Relevance:** *Medium* -- The matching and pricing algorithms under uncertainty are applicable to skill marketplace design where providers and consumers arrive dynamically.

---

### 28. Nonparametric Estimation of Matching Efficiency and Elasticity in Online Spot Work Platforms

- **arXiv ID:** [2412.19024](https://arxiv.org/abs/2412.19024)
- **Authors:** (Multiple authors)
- **Date:** December 26, 2024

**Abstract:** First paper to estimate matching efficiency and elasticity in an online spot work matching platform (Timee), providing insights into private online job search trends.

**Key Contributions:**
- Matching efficiency and elasticity estimation for gig platforms
- Proprietary data from Timee platform
- Long-term insights into labor market matching dynamics

**Relevance:** *Medium* -- Methodology for measuring marketplace efficiency applicable to skill marketplace analytics.

---

### 29. OpenCourier: An Open Protocol for Building a Decentralized Ecosystem for Gig Work

- **arXiv ID:** [2511.02455](https://arxiv.org/abs/2511.02455)
- **Authors:** (Multiple authors)
- **Date:** November 4, 2025

**Abstract:** Open protocol for a decentralized gig work ecosystem, addressing the centralization problems of existing platforms.

**Key Contributions:**
- Decentralized protocol design for gig marketplaces
- Open standards for worker-platform interactions

**Relevance:** *Medium* -- The decentralization approach is relevant if designing a permissionless skill marketplace.

---

## Category H: Decentralized Multi-Agent Coordination

### 30. AgentNet: Decentralized Evolutionary Coordination for LLM-based Multi-Agent Systems

- **arXiv ID:** [2504.00587](https://arxiv.org/abs/2504.00587)
- **Authors:** Yingxuan Yang, Huacan Chai, Shuai Shao, Yuanyi Song, Siyuan Qi, Renting Rui, Weinan Zhang
- **Date:** April 1, 2025 (v2: May 29, 2025)
- **Category:** cs.MA
- **License:** CC BY 4.0

**Abstract:** Proposes AgentNet, a decentralized RAG-based framework where LLM agents specialize, evolve, and collaborate in a dynamic DAG. Key innovations: (1) fully decentralized coordination without central orchestrator; (2) dynamic agent graph topology adapting to task demands; (3) retrieval-based memory for continual skill refinement. Enables fault-tolerant, privacy-preserving collaboration across organizations.

**Key Contributions:**
- Decentralized coordination eliminates central orchestrator
- Dynamic DAG topology for agent specialization
- Retrieval-based memory for skill refinement
- Privacy-preserving cross-organization collaboration

**Relevance:** *High* -- The decentralized skill specialization and dynamic topology are highly relevant to marketplace architectures where agents discover and collaborate without central control.

---

### 31. Fetch.ai: An Architecture for Modern Multi-Agent Systems

- **arXiv ID:** [2510.18699](https://arxiv.org/abs/2510.18699)
- **Authors:** Michael J. Wooldridge, Attila Bagoly, Jonathan J. Ward, Emanuele La Malfa, Gabriel Paludo Licks
- **Date:** October 21, 2025
- **Category:** cs.MA

**Abstract:** Introduces the Fetch.ai architecture: industrial-strength platform integrating classical MAS principles with modern AI. Multi-layered solution: decentralized blockchain for verifiable identity/discovery/transactions, development framework for secure interoperable agents, cloud deployment platform, and intelligent orchestration layer. Demonstrated in decentralized logistics use case.

**Key Contributions:**
- Blockchain-based verifiable identity and discovery for agents
- Decentralized transaction infrastructure
- Agent-native LLM for translating goals into multi-agent workflows
- Production-deployed decentralized logistics marketplace

**Relevance:** *High* -- Production multi-agent marketplace architecture with blockchain identity, discovery, and transaction mechanisms directly applicable to skill marketplace infrastructure.

---

### 32. MIRIX: Multi-Agent Memory System for LLM-Based Agents (Agent Memory Marketplace)

- **arXiv ID:** [2507.07957](https://arxiv.org/abs/2507.07957)
- **Authors:** Yu Wang, Xi Chen
- **Date:** July 10, 2025
- **Category:** cs.CL
- **License:** CC BY 4.0

**Abstract:** MIRIX introduces six memory types (Core, Episodic, Semantic, Procedural, Resource Memory, Knowledge Vault) with a multi-agent framework. Notably proposes an "Agent Memory Marketplace" -- a decentralized ecosystem where memory is exchanged, reused, and built collaboratively.

**Key Contributions:**
- Agent Memory Marketplace concept for decentralized memory exchange
- Six-type memory architecture for persistent agent knowledge
- Memory as a tradeable, composable asset

**Relevance:** *Medium-high* -- The Agent Memory Marketplace concept extends the skill marketplace idea to include experiential knowledge and memory as tradeable assets.

---

## Category I: Skill Extraction & Labor Market Intelligence

### 33. Skill Demand Forecasting Using Temporal Knowledge Graph Embeddings

- **arXiv ID:** [2504.07233](https://arxiv.org/abs/2504.07233)
- **Authors:** (Multiple authors)
- **Date:** April 9, 2025

**Abstract:** Approaches skill demand forecasting as a knowledge graph completion task using temporal link prediction. Predicts future skill demand trends from labor market data.

**Key Contributions:**
- Temporal knowledge graph approach to skill demand forecasting
- Predictive analytics for skill marketplace demand signals

**Relevance:** *Medium* -- Skill demand forecasting is valuable for marketplace supply/demand balancing.

---

### 34. Rethinking Skill Extraction in the Job Market Domain using Large Language Models

- **arXiv ID:** [2402.03832](https://arxiv.org/abs/2402.03832)
- **Authors:** KC Nguyen et al.
- **Date:** 2024
- **Citations:** 45

**Abstract:** Addresses skill extraction from job postings and resumes using LLMs. Identifies and classifies skills from unstructured text.

**Key Contributions:**
- LLM-based skill extraction from job postings
- Improved skill identification accuracy

**Relevance:** *Medium* -- Skill extraction technology is essential for populating and searching skill marketplace catalogs.

---

### 35. A Survey on Skill Extraction and Classification from Job Postings

- **arXiv ID:** [2402.05617](https://arxiv.org/abs/2402.05617)
- **Authors:** E. Senger et al.
- **Date:** 2024
- **Citations:** 42

**Abstract:** Comprehensive survey of deep learning methodologies, datasets, and terminologies for NLP-driven skill extraction and classification.

**Key Contributions:**
- Comprehensive survey of skill extraction methods
- Dataset and methodology overview

**Relevance:** *Medium* -- Provides the NLP foundations for skill taxonomy and classification in marketplace systems.

---

### 36. CrowdSim: A Hybrid Simulation Model for Failure Prediction in Crowdsourced Software Development

- **arXiv ID:** (Not assigned specific ID)
- **Authors:** (Multiple authors)
- **Date:** March 17, 2021

**Abstract:** Models a crowdsourcing software development (CSD) marketplace as a dynamic ecosystem with task demands and freelancer supply. Predicts task failure due to competition over shared worker supply and project uncertainty.

**Key Contributions:**
- Simulation model for crowdsourcing marketplace dynamics
- Failure prediction from supply-demand competition
- Worker supply modeling in task marketplaces

**Relevance:** *Medium* -- Marketplace dynamics simulation applicable to understanding skill marketplace failures and competition effects.

---

## Key Themes & Insights

### Theme 1: AI Agent Skill Ecosystems Are Rapidly Emerging (2025-2026)
The most active research area is the emergence of AI agent skill marketplaces. Papers like AgentSkillOS, SkillNet, SoK: Agentic Skills, and the empirical analysis of 40K+ Claude skills document an ecosystem that has grown explosively. Key patterns:
- **Skill organization** via capability trees and ontologies
- **Orchestration** through DAG-based pipelines
- **Evaluation** across multiple dimensions (safety, cost, executability)
- **Marketplace distribution** as a core design pattern

### Theme 2: Economics & Auction Mechanisms for Agent Marketplaces
Agent Exchange (AEX) and COALESCE introduce formal economic infrastructure for agent skill trading. Key insights:
- Real-Time Bidding (RTB) from advertising can be adapted for agent services
- Cost models comparing internal execution vs. marketplace outsourcing
- 20-41% cost reductions achievable through skill outsourcing
- Four-component platform architecture (USP, ASP, Agent Hubs, DMP)

### Theme 3: Security Is the #1 Challenge
Multiple papers (SkillFortify, SkillScan, ClawHavoc analysis) reveal that **26.1% of marketplace skills contain vulnerabilities** and **5.2% appear malicious**. Critical security needs:
- Supply chain security for skill packages
- Formal verification and trust scoring
- Capability-based sandboxing
- Mandatory vetting before marketplace listing

### Theme 4: Fairness & Bias in Marketplace Selection
ToolTweak and BiasBusters demonstrate that LLM agents have significant biases in tool/skill selection:
- Position bias favoring first-listed tools
- Semantic manipulation of descriptions can capture 81% selection rate
- Pre-training exposure creates unfair provider advantages
- Mitigation: filter-then-sample strategies

### Theme 5: Two-Sided Marketplace Matching at Scale
GraphMatch (Upwork), LinkedIn Talent Search, and matching theory papers provide algorithms for:
- LLM + GNN hybrid matching in dynamic marketplaces
- Exposure-constrained matching to prevent provider overload
- Congestion-aware metrics for marketplace efficiency
- Fairness across both provider and consumer sides

### Theme 6: Decentralized vs. Centralized Architecture
AgentNet, Fetch.ai, and OpenCourier explore decentralized alternatives:
- Blockchain-based identity and transaction verification
- DAG-based dynamic topology without central orchestrator
- Privacy-preserving cross-organization collaboration
- Trade-off: decentralization enables trust but adds complexity

---

## Search Queries Used

### DuckDuckGo Searches (9 queries)
1. `site:arxiv.org skill marketplace` -- 20 results
2. `site:arxiv.org talent marketplace platform` -- 16 results
3. `site:arxiv.org freelance marketplace matching` -- 6 results
4. `site:arxiv.org AI agent marketplace` -- 10 results
5. `site:arxiv.org skill exchange decentralized` -- 0 results
6. `site:arxiv.org gig economy platform matching` -- 13 results
7. `site:arxiv.org multi-agent skill marketplace` -- 10 results
8. `site:arxiv.org LLM tool marketplace` -- 10 results
9. `arxiv skill marketplace two-sided market` -- 15 results

### arXiv Direct Searches (3 queries)
1. `skill+marketplace` -- 18 results
2. `talent+marketplace+AI` -- 0 results
3. `agent+skill+exchange` -- 21 results

### Individual Papers Scraped: 24 papers with full abstracts

---

## Citation Summary

| Paper | Year | Citations | Relevance |
|-------|------|-----------|-----------|
| AgentSkillOS | 2026 | New | Extremely High |
| SkillNet | 2026 | New | Extremely High |
| Agent Skills Analysis (Claude) | 2026 | New | Extremely High |
| SoK: Agentic Skills | 2026 | New | Extremely High |
| COALESCE | 2025 | New | Extremely High |
| Agent Exchange (AEX) | 2025 | 9 | Extremely High |
| SkillFortify (Security) | 2026 | New | Extremely High |
| Agent Skills in the Wild | 2026 | New | Extremely High |
| Magentic Marketplace | 2025 | 1 | Extremely High |
| GraphMatch (Upwork) | 2025 | New | Very High |
| SkillFlow | 2025 | New | High |
| ToolTweak | 2025 | New | High |
| BiasBusters | 2025 | New | High |
| AgentNet | 2025 | New | High |
| Fetch.ai MAS | 2025 | New | High |
| AI Agent Buying | 2025 | 2 | High |
| Fair Team Formation | 2020 | -- | High |
| LinkedIn Talent Search | 2018 | -- | High |
| Fairness Two-Sided | 2020 | 17 | High |
| LLM Data Marketplace | 2025 | New | High |
| UpBench (Upwork) | 2025 | New | High |
| FaMA (FB Marketplace) | 2025 | 2 | Medium-High |
| MIRIX Memory Marketplace | 2025 | New | Medium-High |
| Matching ECDA | 2026 | New | Medium-High |
| Hiring Bias Freelance | 2025 | New | Medium-High |
| Gig Matching Policies | 2024 | 3 | Medium |
| Skill Demand Forecasting | 2025 | New | Medium |
| Skill Extraction LLM | 2024 | 45 | Medium |
| Skill Extraction Survey | 2024 | 42 | Medium |
| LLM Hiring Behavior | 2026 | New | Medium |
