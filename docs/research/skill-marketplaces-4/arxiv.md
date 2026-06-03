# ArXiv Findings — Round 4

> Focus: Skill orchestration at scale, self-evolving skills, small model skill frameworks, formal verification, agent economy

## Papers Not Covered in Rounds 1-3

### 1. AgentSkillOS — Organizing, Orchestrating, and Benchmarking at Ecosystem Scale (2603.02176)
- **Authors:** Li, Hao et al.
- **Date:** Mar 2, 2026
- **License:** CC BY 4.0

**Key contributions:**
- First principled framework for skill selection, orchestration, and ecosystem-level management
- **Two-stage architecture:**
  1. **Manage Skills** — organizes skills into a capability tree via node-level recursive categorization for efficient discovery
  2. **Solve Tasks** — retrieves, orchestrates, and executes multiple skills through **DAG-based pipelines**
- **Benchmark:** 30 artifact-rich tasks across 5 categories (data computation, document creation, motion video, visual design, web interaction)
- **Quality evaluation:** LLM-based pairwise evaluation aggregated via Bradley-Terry model
- **Experiments across 3 scales: 200 → 200K skills**
- **Key findings:**
  - Tree-based retrieval effectively approximates oracle skill selection
  - **DAG-based orchestration substantially outperforms native flat invocation** even with identical skill sets
  - "Structured composition is the key to unlocking skill potential"
- **GitHub:** https://github.com/ynulihao/AgentSkillOS

**Implications:** Validates that multi-skill orchestration via DAGs is strictly better than flat skill loading. Our current flat invocation model leaves performance on the table.

---

### 2. EvoSkill — Automated Skill Discovery for Multi-Agent Systems (2603.02766)
- **Authors:** Alzubi, Salaheddin et al.
- **Date:** Mar 3, 2026
- **License:** CC BY 4.0

**Key contributions:**
- Self-evolving framework that automatically discovers and refines agent skills through iterative failure analysis
- **Process:** Analyze execution failures → propose new skills or edits → materialize into structured skill folders
- **Pareto frontier** governs selection — retains only skills that improve held-out validation while model stays frozen
- **Results:**
  - OfficeQA: +7.3% exact-match accuracy (60.6% → 67.9%)
  - SealQA: +12.1% gain (26.6% → 38.7%)
  - **Zero-shot transfer:** Skills evolved on SealQA transfer to BrowseComp, improving accuracy by +5.3% without modification
- "Skill-level optimization produces transferable capabilities beyond the training task"

**Implications:** Contradicts SkillsBench (Round 3) finding that self-generated skills provide zero benefit — but EvoSkill uses iterative failure analysis + Pareto selection, not naive generation. The quality ceiling for automated skill generation depends on the generation methodology.

---

### 3. Agent Skill Framework — Small Language Models in Industrial Environments (2602.16653)
- **Authors:** Xu, Yangjie et al.
- **Date:** Feb 18, 2026
- **License:** CC BY-NC-SA 4.0

**Key contributions:**
- Formal mathematical definition of the Agent Skill process
- Systematic evaluation across multiple model sizes on 3 use cases (2 open-source + 1 real-world insurance claims)
- **Key findings:**
  - **Tiny models struggle with reliable skill selection** — cannot determine which skill to apply
  - **Moderately sized SLMs (12B-30B) benefit substantially** from Agent Skills
  - **Code-specialized ~80B models achieve performance comparable to closed-source baselines** with better GPU efficiency
  - Industrial deployment sweet spot: 12B-30B for cost-sensitive, 80B for quality-critical

**Implications:** Defines the minimum model size for effective skill utilization. Validates that skills aren't just for frontier models — 12B+ models benefit significantly.

---

### 4. FormalJudge — Neuro-Symbolic Paradigm for Agentic Oversight (2602.11136)
- **Authors:** Zhou, Jiayi et al.
- **Date:** Feb 11, 2026
- **License:** CC BY 4.0

**Key contributions:**
- Uses Dafny specifications + Z3 SMT solving for mathematical guarantees (not probabilistic scores)
- Bidirectional Formal-of-Thought: top-down decomposition of intent → bottom-up compliance proofs
- **Results:**
  - +16.6% improvement over LLM-as-a-Judge baselines
  - **Weak-to-strong generalization:** 7B judge achieves >90% accuracy detecting deception from 72B agents
  - Near-linear safety improvement through iterative refinement

**Implications:** Formal verification can make skill safety evaluation dramatically more reliable than LLM-based scoring. A 7B model with formal methods can police a 72B agent.

---

### 5. The Agent Economy — Blockchain Foundation for Autonomous Agents (2602.14219)
- **Authors:** Xu, Minghui
- **Date:** Feb 15, 2026

**Key contributions:**
- Five-layer architecture for agent economic autonomy:
  1. Physical Infrastructure (DePIN protocols)
  2. Identity & Agency (W3C DIDs, reputation capital)
  3. Cognitive & Tooling (RAG, MCP)
  4. Economic & Settlement (account abstraction)
  5. Collective Governance (Agentic DAOs)
- Proposes "Internet of Agents (IoA)" — global decentralized network
- Permissionless participation, trustless settlement, machine-to-machine micropayments

**Implications:** Academic framing of the crypto/blockchain agent economy. Connects to the $SKILL token and SafuSkill trends noted in Round 1. Adds theoretical depth to the monetization angle.

---

### 6. TARSE — Test-Time Adaptation via Retrieval of Skills and Experiences (2603.01241)
- **Date:** Mar 2, 2026
- Agent retrieves both relevant skills and experiences from curated libraries
- Performs lightweight test-time adaptation to align with task requirements
- **Significance:** Skills as a retrieval target for test-time adaptation — academic validation of the "skill library" concept beyond coding agents

## Cumulative ArXiv Paper Count (All Rounds)

| Round | Papers | Focus |
|---|---|---|
| Round 1 | 5 | Security, skill mining, registry survey |
| Round 2 | 4 | Security crisis (SkillScan, SoK, SkillFortify, Defensible Design) |
| Round 3 | 6 | Benchmarking (SkillsBench), MCP security (4), skill mining |
| Round 4 | 6 | Orchestration (AgentSkillOS), self-evolution (EvoSkill), SLMs, formal verification, agent economy, retrieval |
| **Total** | **21** | |

## Key Takeaways

1. **DAG-based skill orchestration > flat invocation** — validated at scales from 200 to 200K skills (AgentSkillOS)
2. **Self-evolving skills CAN work** but require iterative failure analysis + Pareto selection, not naive generation (EvoSkill)
3. **12B-30B models are the industrial sweet spot** for Agent Skills — tiny models fail, frontier models aren't needed (SLM Framework)
4. **Formal verification enables weak-to-strong safety** — 7B judge can police 72B agent with 90%+ accuracy (FormalJudge)
5. **Skill retrieval at test-time** is an emerging academic pattern — skills becoming infrastructure for model adaptation
