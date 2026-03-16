# ArXiv Findings — AI Agent Skill Marketplace Research

*Searched: 2026-03-16*

---

## Papers Found (8 total)

### 1. "Agent Skills in the Wild: An Empirical Study of Security Vulnerabilities at Scale" (2601.10338, Jan 15 2026)

**Authors:** Liu Yi, Wang Weizhe, Feng Ruitao, Zhang Yao, Xu Guangquan, Deng Gelei, Li Yuekang, Leo

**The first large-scale empirical security analysis of the agent skills ecosystem.**

- Collected **42,447 skills** from two major marketplaces
- Systematically analyzed **31,132** using SkillScan (multi-stage: static analysis + LLM-based semantic classification)
- **26.1% of skills contain at least one vulnerability** (8,126 vulnerable skills)
- 14 distinct vulnerability patterns across 4 categories:
  - **Data exfiltration: 13.3%** (most prevalent)
  - **Privilege escalation: 11.8%**
  - **Prompt injection: 9.7%**
  - **Supply chain risks: 8.5%**
- **5.2% exhibit high-severity patterns strongly suggesting malicious intent**
- Skills with executable scripts are **2.12x more likely** to contain vulnerabilities (OR=2.12, p<0.001)
- Detection: 86.7% precision, 82.5% recall
- Contributions: vulnerability taxonomy, detection methodology, open dataset + toolkit

**Key insight:** Instruction-only skills are significantly safer than skills bundling executable scripts. This validates our marketplace's approach of using PEP 723 inline metadata for scripts (transparent, auditable).

---

### 2. "Malicious Agent Skills in the Wild: A Large-Scale Security Empirical Study" (2602.06547, Feb 6 2026)

**Authors:** Liu Yi, Chen Zhihao, Zhang Yanjun, Deng Gelei, Li Yuekang, Ning Jianting, Leo Yu

**First labeled dataset of confirmed malicious skills.**

- Behaviorally verified **98,380 skills** from two community registries
- Confirmed **157 malicious skills** with **632 vulnerabilities**
- Average malicious skill: **4.03 vulnerabilities** across median 3 kill chain phases
- Two archetypes:
  - **Data Thieves**: credential exfiltration via supply chain techniques
  - **Agent Hijackers**: subvert agent decision-making via instruction manipulation
- **Single actor** responsible for 54.1% of cases (templated brand impersonation)
- **Shadow features** (capabilities absent from public documentation): 0% in basic attacks, 100% in advanced
- Some skills exploit the platform's own hook system and permission flags
- Responsible disclosure led to **93.6% removal within 30 days**
- Released dataset and analysis pipeline

**Key insight:** A single dedicated threat actor can dominate a marketplace's malicious skill count through templated attacks. Low barrier to publish enables this.

---

### 3. "Agent Skills for Large Language Models: Architecture, Acquisition, Security, and the Path Forward" (2602.12430, Feb 12 2026)

**Authors:** Xu Renjun, Yan

**The definitive survey paper on agent skills — comprehensive treatment of the entire landscape.**

Organizes the field along 4 axes:
1. **Architectural foundations**: SKILL.md spec, progressive context loading, complementary roles of skills and MCP
2. **Skill acquisition**: RL with skill libraries, autonomous skill discovery (SEAgent), compositional skill synthesis
3. **Deployment at scale**: Computer-use agent (CUA) stack, GUI grounding, OSWorld/SWE-bench benchmarks
4. **Security**: 26.1% vulnerability rate, proposes Skill Trust and Lifecycle Governance Framework — 4-tier gate-based permission model mapping skill provenance to graduated deployment capabilities

7 open challenges identified:
- Cross-platform skill portability
- Capability-based permission models
- Trustworthy self-improving skill ecosystems
- And 4 others

**Key insight:** This paper formalizes "progressive disclosure" as the core architectural principle and proposes a 4-tier trust model (System → Curated → Community → Untrusted) that directly maps to our marketplace's structure.

---

### 4. "SoK: Agentic Skills — Beyond Tool Use in LLM Agents" (2602.20867, Feb 24 2026)

**Authors:** Jiang Yanna, Li Delong, Deng Haiyu, Ma Baihe, Wang Xu, Qin Yu, Guangsheng

**Systematization of Knowledge (SoK) paper mapping the full skill lifecycle.**

Two complementary taxonomies:
1. **Seven design patterns**: metadata-driven progressive disclosure, executable code skills, self-evolving libraries, marketplace distribution, and 3 others
2. **Representation x Scope taxonomy**: What skills ARE (natural language, code, policy, hybrid) x What environments they operate over (web, OS, software engineering, robotics)

Security analysis grounded by ClawHavoc campaign case study:
- Nearly **1,200 malicious skills** infiltrated a major agent marketplace
- Exfiltrated: API keys, cryptocurrency wallets, browser credentials at scale

Key finding: **Curated skills can substantially improve agent success rates while self-generated skills may degrade them.** This validates the "curated > mass-generated" approach.

---

### 5. "Formal Analysis and Supply Chain Security for Agentic AI Skills" (2603.00195, Feb 27 2026)

**Authors:** Bhardwaj, Varun Pratap

**First formal verification framework for agent skill supply chains.**

Scale context:
- OpenClaw: **228,000 GitHub stars**
- Anthropic Agent Skills: **75,600 stars**
- ClawHavoc campaign (Jan-Feb 2026): **1,200+ malicious skills** infiltrated OpenClaw marketplace
- MalTool: **6,487 malicious tools** evading conventional detection
- **12 reactive security tools** emerged — all heuristic, no formal guarantees

Proposes **SkillFortify** with 6 contributions:
1. DY-Skill attacker model (Dolev-Yao adaptation to 5-phase skill lifecycle)
2. Sound static analysis framework (abstract interpretation)
3. Capability-based sandboxing with confinement proof
4. Agent Dependency Graph with SAT-based resolution and lockfile semantics
5. Trust score algebra with formal monotonicity
6. SkillFortifyBench: 540-skill benchmark

Results: **96.95% F1, 100% precision, 0% false positive rate** on 540 skills. SAT-based resolution handles 1,000-node graphs in <100ms.

**Key insight:** The skills ecosystem has grown so fast that formal security tools can't keep up. Only heuristic approaches exist in production today.

---

### 6. "Defensible Design for OpenClaw: Securing Autonomous Tool-Invoking Agents" (2603.13151, Mar 13 2026)

**Authors:** Li Zongwei, Wenkai, Xiaoqi

- OpenClaw-like agents are "insecure by default" — untrusted inputs, autonomous action, extensibility, privileged system access in single execution loop
- Proposes blueprint for defensible design: risk taxonomy, secure engineering principles, practical research agenda
- Goal: transition from isolated vulnerability patching to systematic defensive engineering

---

### 7. "Automating Skill Acquisition through Large-Scale Mining" (2603.11808, Mar 12 2026)

**Authors:** Bi Shuzhen et al.

- Framework for automated extraction of skills from GitHub repositories
- Translates capabilities to standardized SKILL.md format
- Achieves **40% gains in knowledge transfer efficiency**
- Method: repository structural analysis → semantic skill identification → SKILL.md translation

---

### 8. "A Survey of AI Agent Registry Solutions" (2508.03095, Aug 2025, v3 Oct 2025)

**Authors:** Singh Aditi et al. (including Ramesh Raskar, MIT)

Compares 5 registry architectures:
1. MCP Registry — centralized mcp.json descriptors
2. A2A Agent Cards — decentralized JSON capability manifests
3. AGNTCY Agent Directory — IPFS DHT + OCI + Sigstore integrity
4. Microsoft Entra Agent ID — enterprise SaaS + zero-trust
5. NANDA Index AgentFacts — cryptographically verifiable, privacy-preserving

---

## Summary Statistics

| Metric | Value | Source |
|---|---|---|
| Skills analyzed (largest study) | 98,380 | 2602.06547 |
| Skills with vulnerabilities | 26.1% | 2601.10338 |
| Confirmed malicious skills | 157 | 2602.06547 |
| ClawHavoc campaign malicious skills | ~1,200 | 2602.20867, 2603.00195 |
| Malicious tools catalogued (MalTool) | 6,487 | 2603.00195 |
| Skills with executable scripts: vulnerability odds ratio | 2.12x | 2601.10338 |
| Snyk ToxicSkills: skills with any security issue | 36.82% | Snyk blog (not ArXiv) |
| Snyk ToxicSkills: confirmed malicious payloads | 76 | Snyk blog |
| OpenClaw instances worldwide | 63,026 | GitHub security report |

## Key Themes Across Papers

1. **Security is the #1 research focus** — 6 of 8 papers directly address security
2. **Supply chain framing** — researchers consistently compare skill marketplaces to npm/PyPI ecosystem with similar vulnerabilities but worse permissions model
3. **Formal methods emerging** — SkillFortify shows formal verification is feasible and achieves near-perfect precision
4. **Progressive disclosure is the architectural consensus** — every paper references it as the core design principle
5. **Curated > auto-generated** — SoK paper shows curated skills improve agent success while self-generated may degrade it
6. **Single threat actors dominate** — one actor responsible for 54.1% of confirmed malicious skills
