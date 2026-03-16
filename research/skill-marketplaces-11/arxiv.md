# Round 11: arXiv Skill Marketplace Research

**Date:** March 2026
**Source:** DuckDuckGo site:arxiv.org search (28 results), 8 papers scraped in full

---

## Papers Analyzed (Ordered by Relevance)

### 1. Agent Skills: A Data-Driven Analysis of Claude Skills (2602.08004)
- **Authors:** Ling, George, Zhong, Shanshan, Huang, Richard
- **Date:** Feb 8, 2026
- **Category:** cs.SE (Software Engineering)
- **Key Contribution:** First large-scale quantitative analysis of 40,285 skills from a major marketplace (skills.sh)
- **Findings:**
  - Skill publication occurs in **short bursts tracking community attention**
  - Content heavily concentrated in **software engineering workflows**
  - Information retrieval and content creation dominate **adoption** (not creation)
  - Pronounced **supply-demand imbalance** across categories
  - Most skills fit within **typical prompt budgets** despite heavy-tailed length distribution
  - Strong **ecosystem homogeneity** with widespread intent-level redundancy
  - Non-trivial **safety risks** including state-changing/system-level actions
- **Relevance:** Definitive empirical snapshot of the skills marketplace ecosystem

---

### 2. SoK: Agentic Skills -- Beyond Tool Use in LLM Agents (2602.20867)
- **Authors:** Jiang, Yanna, Li, Delong, Deng, Haiyu, et al.
- **Date:** Feb 24, 2026
- **Category:** cs.CR (Cryptography and Security)
- **Key Contribution:** Systematization of Knowledge paper mapping the full skill lifecycle
- **Seven Design Patterns:** Metadata-driven progressive disclosure, executable code skills, self-evolving libraries, marketplace distribution, and more
- **Representation x Scope Taxonomy:** Skills categorized by what they ARE (natural language, code, policy, hybrid) and WHERE they operate (web, OS, SE, robotics)
- **ClawHavoc Case Study:** ~1,200 malicious skills infiltrated a major marketplace, exfiltrating API keys, crypto wallets, and browser credentials at scale
- **Key Finding:** Curated skills substantially improve agent success rates while self-generated skills may degrade them
- **Open Challenges:** Robust, verifiable, and certifiable skills for real-world autonomous agents

---

### 3. Organizing, Orchestrating, and Benchmarking Agent Skills at Ecosystem Scale (2603.02176)
- **Authors:** Li, Hao, Mu, Chunjiang, Chen, Jianhao, et al.
- **Date:** Mar 2, 2026
- **Category:** cs.CL (Computation and Language)
- **Key Contribution:** AgentSkillOS — first principled framework for skill selection, orchestration, ecosystem management
- **Two Stages:**
  1. **Manage Skills:** Capability tree via node-level recursive categorization
  2. **Solve Tasks:** DAG-based pipelines for retrieval, orchestration, execution
- **Benchmark:** 30 artifact-rich tasks across 5 categories (data computation, document creation, motion video, visual design, web interaction)
- **Scale Tested:** 200 to 200K skills
- **Key Finding:** Tree-based retrieval effectively approximates oracle skill selection; DAG-based orchestration substantially outperforms flat invocation
- **Code:** github.com/ynulihao/AgentSkillOS

---

### 4. Formal Analysis and Supply Chain Security for Agentic AI Skills (2603.00195)
- **Authors:** Bhardwaj, Varun Pratap
- **Date:** Feb 27, 2026
- **Category:** cs.CR
- **Key Contribution:** SkillFortify — first formal analysis framework for agent skill supply chains
- **Six Contributions:**
  1. DY-Skill attacker model (Dolev-Yao adaptation to 5-phase skill lifecycle)
  2. Sound static analysis via abstract interpretation
  3. Capability-based sandboxing with confinement proof
  4. Agent Dependency Graph with SAT-based resolution and lockfile semantics
  5. Trust score algebra with formal monotonicity
  6. SkillFortifyBench: 540-skill benchmark
- **Results:** 96.95% F1, 100% precision, 0% false positive rate on 540 skills; SAT-based resolution handles 1,000-node graphs in <100ms
- **Context:** ClawHavoc infiltrated 1,200+ malicious skills; MalTool catalogued 6,487 malicious tools evading conventional detection

---

### 5. SkillNet: Create, Evaluate, and Connect AI Skills (2603.04448)
- **Authors:** Liang, Yuan, Zhong, Ruobin, Xu, Haoming, et al. (30+ authors)
- **Date:** Feb 26, 2026 (submitted as Mar 6, 2026 on page)
- **Category:** cs.AI
- **Key Contribution:** Open infrastructure for creating, evaluating, and organizing AI skills at scale
- **Unified Ontology:** Skills from heterogeneous sources with rich relational connections
- **Multi-Dimensional Evaluation:** Safety, Completeness, Executability, Maintainability, Cost-awareness
- **Scale:** 200,000+ skills in repository
- **Results:** 40% improvement in average rewards, 30% reduction in execution steps across ALFWorld, WebShop, and ScienceWorld
- **Key Insight:** Formalizing skills as evolving, composable assets provides foundation for durable agent mastery

---

### 6. Agent Skills in the Wild: Empirical Security Study at Scale (2601.10338)
- **Authors:** Liu, Yi, Wang, Weizhe, Feng, Ruitao, et al.
- **Date:** Jan 15, 2026
- **Category:** cs.CR
- **Key Contribution:** First large-scale empirical security analysis of agent skill ecosystem
- **SkillScan Framework:** Multi-stage detection: static analysis + LLM-based semantic classification
- **Data:** 42,447 skills from two major marketplaces, 31,132 analyzed
- **Findings:**
  - **26.1%** of skills contain at least one vulnerability
  - 14 distinct vulnerability patterns across 4 categories: prompt injection, data exfiltration, privilege escalation, supply chain
  - Data exfiltration (13.3%) and privilege escalation (11.8%) most prevalent
  - **5.2%** exhibit high-severity patterns suggesting malicious intent
  - Scripts bundled with skills are **2.12x** more likely to contain vulnerabilities (OR=2.12, p<0.001)
- **Detection Results:** 86.7% precision, 82.5% recall

---

### 7. Agent Skills for LLMs: Architecture, Acquisition, Security, and Path Forward (2602.12430)
- **Authors:** Xu, Renjun, Yan
- **Date:** Feb 12, 2026 (v3: Feb 17, 2026)
- **Category:** cs.MA (Multiagent Systems)
- **Key Contribution:** Comprehensive survey along 4 axes:
  1. **Architecture:** SKILL.md spec, progressive context loading, MCP integration
  2. **Skill Acquisition:** RL with skill libraries, autonomous discovery (SEAgent), compositional synthesis
  3. **Deployment at Scale:** Computer-use agent (CUA) stack, GUI grounding, benchmark progress
  4. **Security:** 26.1% vulnerability rate motivates Skill Trust and Lifecycle Governance Framework
- **Proposed Framework:** Four-tier, gate-based permission model mapping skill provenance to deployment capabilities
- **Seven Open Challenges:** Cross-platform portability, capability-based permissions, and more
- **Code:** github.com/scienceaix/agentskills

---

### 8. SkillsBench: Benchmarking How Well Agent Skills Work (2602.12670)
- **Authors:** Li, Xiangyi, Chen, Wenbo, et al. (30+ authors)
- **Date:** Feb 13, 2026 (v3: Mar 13, 2026)
- **Category:** cs.AI
- **Key Contribution:** First standardized benchmark for measuring whether skills actually help
- **Benchmark:** 86 tasks across 11 domains, paired with curated skills and deterministic verifiers
- **Three Conditions:** No skills, curated skills, self-generated skills
- **Scale:** 7 agent-model configurations, 7,308 trajectories
- **Results:**
  - Curated skills raise average pass rate by **+16.2 percentage points**
  - Effects vary widely: +4.5pp (Software Engineering) to +51.9pp (Healthcare)
  - 16 of 84 tasks show **negative deltas** (skills can hurt)
  - **Self-generated skills provide no benefit on average**
  - Focused skills (2-3 modules) outperform comprehensive documentation
  - **Smaller models with skills can match larger models without them**

---

## Additional Papers Found

| Paper | arXiv ID | Key Topic |
|-------|----------|-----------|
| Scaling Laws for Educational AI Agents | 2603.11709 | Skill composition enables specialization in education |
| OpenClaw AI Agents as Informal Learners | 2602.18832 | Multi-platform learning cycle: deploy -> share via marketplaces -> discuss on social |
| SkillCraft: Can LLM Agents Learn to Use Tools Skillfully? | 2603.00718 | Compositional tool-use scenarios with difficulty scaling |
| Automating Skill Acquisition through Large-Scale Mining | 2603.11808 | Extracting skills from repositories using structural decomposition |
| Your Echos are Heard | 2204.10920 | Alexa skill marketplace security analysis (historical reference) |

---

## Research Landscape Summary

### Volume of Academic Work
- **8 major papers** directly about AI agent skill marketplaces in Jan-Mar 2026
- **5 additional papers** touching on skill marketplaces tangentially
- This represents an **unprecedented explosion** of academic interest — more papers in Q1 2026 than all prior years combined

### Consensus Points Across All Papers
1. **Skills are the modular unit of the future** — composable, reusable, transferable
2. **Security is critical and unsolved** — 26.1% vulnerability rate, supply chain attacks proven
3. **Curated > self-generated** — human-curated skills consistently outperform AI-generated
4. **DAG orchestration > flat invocation** — structured composition unlocks skill potential
5. **Formal verification is needed** — heuristic detection is insufficient (SkillFortify)
6. **200K+ skills already exist** — the scale demands ecosystem-level management tools

### Key Research Gaps
1. Cross-platform skill portability verification
2. Real-time runtime sandboxing (not just pre-deployment scanning)
3. Economic models for skill composition pricing
4. Long-term skill maintenance and decay detection
5. Privacy-preserving skill evaluation
6. Federated trust across multiple marketplaces
