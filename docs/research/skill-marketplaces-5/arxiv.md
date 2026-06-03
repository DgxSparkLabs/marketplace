# arXiv Findings: Skill Marketplaces

> Searched: March 16, 2026
> Queries: "site:arxiv.org skill marketplace", "site:arxiv.org skills marketplace platform AI agent", "site:arxiv.org talent marketplace matching algorithm", "site:arxiv.org freelance marketplace skill matching", "site:arxiv.org agent tool marketplace composable skills"
> Total relevant papers found: 20+

## Category 1: AI Agent Skills — Security & Ecosystem Analysis

### Paper 1: Agent Skills in the Wild: An Empirical Study of Security Vulnerabilities
- **ID:** arXiv:2601.10338
- **Authors:** (Security research group)
- **Key Finding:** First large-scale empirical security analysis of the AI agent skill ecosystem. Collected **42,447 skills from two major marketplaces** and systematically analyzed 31,132.
- **Vulnerability Rate:** 26-36% of skills contain security issues
- **Implication:** The skill marketplace ecosystem has a serious security problem at scale

### Paper 2: Malicious Agent Skills in the Wild: A Large-Scale Security Analysis
- **ID:** arXiv:2602.06547
- **Key Finding:** Community registries have indexed over **98,000 skills**. Analyzes malicious patterns including prompt injection via skill payloads.
- **Implication:** Supply-chain attacks through skill marketplaces are a real and growing threat

### Paper 3: Agent Skills: A Data-Driven Analysis of Claude Skills
- **ID:** arXiv:2602.08004
- **Authors:** G Ling et al. (2026, cited by 1)
- **Abstract:** "As these skills proliferate in public marketplaces, it is unclear what types are available, how users adopt them, and what risks they pose."
- **Key Contribution:** First systematic data-driven analysis of the Claude skills ecosystem

### Paper 4: SoK: Agentic Skills — Beyond Tool Use in LLM Agents
- **ID:** arXiv:2602.20867
- **Authors:** Y Jiang et al. (2026)
- **Key Finding:** Comprehensive systematization of knowledge on agentic skills. Analyzes security and governance implications covering supply-chain risks, prompt injection via skill payloads.
- **Implication:** Skills are more than tools — they represent a new capability paradigm for agents

### Paper 5: Agent Skills Enable a New Class of Realistic and Trivially [Deployable Agents]
- **ID:** arXiv:2510.26328
- **Key Quote:** "These third-party skills can then be distributed over marketplaces that do not necessarily pose strong restrictions on..."
- **Implication:** Skills lower the barrier to agent deployment, but marketplace governance is lagging

### Paper 6: OpenClaw Security Analysis
- **Key Finding:** MCP attack success rate of **52.8%** in tested scenarios
- **Implication:** The Model Context Protocol layer that skills rely on has fundamental security challenges

## Category 2: Skill Orchestration & Composition

### Paper 7: Organizing, Orchestrating, and Benchmarking Agent Skills at Scale (AgentSkillOS)
- **ID:** arXiv:2603.02176
- **Date:** March 2, 2026
- **Key Finding:** DAG-based skill orchestration **dramatically outperforms flat invocation**. Tested from 200 to 200,000 skills. Tree-based retrieval approximates oracle skill selection.
- **All skills sourced from public skill marketplace and GitHub repositories**
- **Critical Insight:** Structured composition is the key to unlocking skill potential at scale

### Paper 8: EvoSkill — Self-Evolving Skills
- **ID:** arXiv:2603.02766
- **Key Finding:** Iterative failure analysis + Pareto selection produces transferable self-evolving skills. Improvement of **+7.3% to +12.1%** over baselines.
- **Contrast:** SkillsBench found naive self-generation provides **zero benefit** — only EvoSkill's structured approach works

### Paper 9: SkillFlow: Efficient Skill and Code Transfer Through Communication
- **ID:** arXiv:2504.06188
- **Date:** April 8, 2025
- **Key Finding:** "A modular, technology-agnostic framework that allows agents to expand their functionality in an ad-hoc fashion by acquiring new skills"
- **Implication:** Agents can learn new skills on-the-fly through inter-agent communication

## Category 3: Job/Talent Market & Skill Matching

### Paper 10: Skill Demand Forecasting Using Temporal Knowledge Graph
- **ID:** arXiv:2504.07233
- **Date:** April 9, 2025
- **Key Approach:** Treats skill need forecasting as a knowledge graph completion task (temporal link prediction)
- **Application:** Predicting which skills will be in demand

### Paper 11: Skill-Based Labor Market Polarization in the Age of AI
- **ID:** arXiv:2501.15809
- **Authors:** VRR Ganuthula et al. (2025, cited by 2)
- **Key Finding:** Examines labor market polarization through skill-based employment and wage distributions in India and the US
- **Implication:** AI is creating skill-based economic divides

### Paper 12: Rethinking Skill Extraction in the Job Market Domain using LLMs
- **ID:** arXiv:2402.03832
- **Authors:** KC Nguyen et al. (2024, cited by 45)
- **Key Contribution:** Skill extraction from job postings and resumes using LLMs
- **High Citation Count:** This is a foundational paper in the field

### Paper 13: A Survey on Skill Extraction and Classification from Job Postings
- **ID:** arXiv:2402.05617
- **Authors:** E Senger et al. (2024, cited by 42)
- **Key Contribution:** Comprehensive overview of deep learning methodologies for NLP-driven skill extraction
- **Also highly cited:** Shows this is an active research area

### Paper 14: Measuring the Popularity of Job Skills in Recruitment Market
- **ID:** arXiv:1712.03087
- **Authors:** T Xu et al. (2017, cited by 92)
- **Key Contribution:** Data-driven approach for modeling job skill popularity from large-scale analysis
- **Foundational:** The most-cited paper in this space

### Paper 15: Understanding and Modeling Job Marketplace with Pretrained Models
- **ID:** arXiv:2408.04381
- **Key Contribution:** Using pretrained language models to understand job marketplace dynamics

## Category 4: Enterprise/Infrastructure

### Paper 16: SLM Skill Framework
- **ID:** arXiv:2602.16653
- **Key Finding:** 12B-30B parameter models are the sweet spot for skill execution. Tiny models fail skill selection. 80B matches frontier models.
- **Implication:** Not all models can use skills effectively — model size matters

### Paper 17: FormalJudge
- **ID:** arXiv:2602.11136
- **Key Finding:** Formal verification allows a 7B judge model to police a 72B agent with 90%+ accuracy
- **Implication:** Small models can effectively govern large agent skill execution

### Paper 18: Agent Economy
- **ID:** arXiv:2602.14219
- **Key Contribution:** Blockchain foundation for agent economic autonomy (Internet of Agents)
- **Implication:** Economic frameworks for agent-to-agent skill trading

### Paper 19: TARSE — Test-Time Skill Retrieval
- **ID:** arXiv:2603.01241
- **Key Contribution:** Test-time skill retrieval for model adaptation — agents can find and use skills dynamically

## Research Themes Summary

| Theme | Papers | Maturity |
|-------|--------|----------|
| **Security of skill ecosystems** | 4 papers | High — major concern, well-studied |
| **Skill orchestration at scale** | 3 papers | Medium — DAGs proven, needs more validation |
| **Job market skill matching** | 5 papers | High — 45-92 citations, established field |
| **Agent economic frameworks** | 2 papers | Low — theoretical, blockchain-based |
| **Formal governance** | 2 papers | Medium — promising results (FormalJudge) |
| **Self-evolving skills** | 1 paper | Low — EvoSkill is first proof of concept |

## Key Research Gaps

1. **No comprehensive taxonomy** of AI agent skill types across marketplaces
2. **No standard benchmark** for skill marketplace quality/safety evaluation
3. **Limited work on skill pricing models** — economic theory for digital skill markets
4. **No study on skill composition patterns** beyond DAGs (e.g., recursive, conditional)
5. **Missing: cross-platform skill portability** — how skills transfer between agent frameworks
6. **Limited longitudinal studies** — how skill ecosystems evolve over time
