---

# Round 7: arXiv Findings — Quality Evaluation, Pricing Mechanisms & Governance Frameworks

## Research Focus
New papers on skill quality evaluation, agent marketplace pricing mechanisms, multi-agent collaboration protocols, governance frameworks. Excluding 17+ papers already covered in R1-R6 (AgentSkillOS 2603.02176, EvoSkill 2603.02766, SkillsBench 2602.12670, SkillFortify, SoK 2602.20867, SLM Framework 2602.16653, FormalJudge 2602.11136, COALESCE 2506.01900, AEX 2507.03904, SkillOrchestra 2602.19672, XSkill 2603.12056, Skill-Inject 2602.20156, ClawGuard 2603.12644, LLM Markets 2603.08853, MalTool 2602.06547, Institutional AI 2601.11369, MCE 2601.21557).

## Papers Discovered (26 New, 11 Deeply Analyzed)

### Tier 1: High-Impact New Papers

#### 1. SkillNet: Create, Evaluate, and Connect AI Skills
- **URL**: https://arxiv.org/abs/2603.04448
- **Date**: Feb 26, 2026
- **Authors**: Liang, Yuan; Zhong, Ruobin; + 25 co-authors
- **Key contribution**: Open infrastructure for creating, evaluating, and organizing AI skills at scale
- **Multi-dimensional evaluation**: Safety, Completeness, Executability, Maintainability, Cost-awareness (SCEMC)
- **Scale**: Repository of **200,000+ skills** with unified ontology
- **Results**: 40% improvement in average rewards, 30% reduction in execution steps across ALFWorld, WebShop, ScienceWorld
- **Significance**: First large-scale infrastructure treating skills as first-class evolving composable assets with multi-dimensional quality metrics

#### 2. Automating Skill Acquisition from GitHub Repos
- **ID**: 2603.11808
- **Key insight**: Solves cold-start supply problem via automated skill mining + SKILL.md format generation
- **Approach**: Mining open-source repositories to extract reusable agent skills automatically
- **Marketplace relevance**: Addresses the biggest marketplace challenge — getting initial supply of quality skills

#### 3. Internet of Agents (IoA) — Survey
- **ID**: 2505.07176
- **Focus**: Infrastructure blueprint for agent interoperability
- **Coverage**: Discovery mechanisms, task matching algorithms, incentive models for agent cooperation
- **Marketplace relevance**: Provides the theoretical infrastructure blueprint — how agents find, evaluate, and transact with each other

#### 4. Magentic Marketplace (Microsoft Research)
- **ID**: 2510.25779
- **Key finding**: First empirical study of agent marketplace dynamics
- **Critical discoveries**:
  - **10-30x first-proposal bias**: Agents overwhelmingly accept the first option presented
  - **Scale degradation**: Marketplace quality decreases as number of agents increases
  - **Implications**: Marketplace design must account for behavioral biases in agent buyers
- **Significance**: Empirical evidence that agent marketplaces behave fundamentally differently from human marketplaces

#### 5. Ev-Trust: Evolutionary Game Theory for Trust
- **ID**: 2512.16167
- **Approach**: Making deception unprofitable via revenue coupling in evolutionary game theoretic framework
- **Key mechanism**: Trust scores that evolve over time, punishing deceptive behavior through economic penalties
- **Marketplace relevance**: Solves the "41% vulnerability" problem not through scanning but through economic incentives

#### 6. What Is Your AI Agent Buying? (ACES Framework)
- **URL**: https://arxiv.org/abs/2508.02630
- **Date**: Aug 4, 2025 (revised Dec 17, 2025)
- **Authors**: Allouah, Besbes, Figueroa, Kanoria, Kumar
- **ACES**: Provider-agnostic framework for auditing agent decision-making
- **Critical findings**:
  - **Choice homogeneity**: Agents concentrate demand on few "modal" products
  - **Model instability**: Updates drastically reshuffle market shares
  - **Position bias**: Persists even in text-only "headless" interfaces
  - **Agents penalize sponsored tags** but reward platform endorsements
  - **Seller-side agents** drive significant market share gains via description tweaks
- **Quote**: "Agentic markets are volatile and fundamentally different from human-centric commerce"

### Tier 2: Collaboration & Composition Papers

#### 7. AWCP: Agent Workspace Collaboration Protocol
- **ID**: 2602.20493
- **Innovation**: Missing workspace layer — agents share execution environments, not just messages
- **Architecture**: Workspace delegation model where agents collaborate through shared state
- **Marketplace relevance**: Skills that compose need shared execution contexts, not just API calls

#### 8. CoWork-X: Co-Evolution Framework
- **ID**: 2602.05004
- **Approach**: HTN-based skill retrieval + budget-aware runtime composition
- **Key mechanism**: Skills and agents co-evolve, with budget constraints driving optimization
- **Marketplace relevance**: Dynamic skill pricing based on composition complexity and budget

#### 9. Modular Memory Position Paper (26 authors)
- **ID**: 2603.01761
- **Key insight**: **ICL = skill rental vs IWL = skill internalization**
  - In-Context Learning (ICL): Agent "rents" a skill for one session (pay-per-use)
  - In-Weight Learning (IWL): Agent permanently internalizes a skill (one-time purchase)
- **New pricing model**: This distinction maps directly to marketplace pricing — rental vs purchase
- **Significance**: Theoretical foundation for two-tier marketplace pricing

#### 10. ACuRL: Autonomous Continual Learning
- **ID**: 2602.10356
- **Innovation**: Zero-human-data skill generation + CUAJudge auto-evaluator
- **Approach**: Agents autonomously discover and learn new skills through continual interaction
- **Marketplace relevance**: Skills that self-improve over time — dynamic quality that evolves post-purchase

### Tier 3: Governance & Compliance Papers

#### 11. AI Governance through Markets
- **ID**: 2501.17755
- **Approach**: Insurance, auditing, and procurement as governance vectors
- **Key argument**: Market mechanisms (not just regulation) can govern AI behavior
- **Marketplace relevance**: Insurance for skill failures, auditing for quality, procurement standards

#### 12. COMPASS: Multi-Dimensional Governance
- **ID**: 2603.11277
- **Architecture**: 4-agent governance system covering sovereignty, sustainability, compliance, ethics
- **Approach**: Governance itself is agentic — AI agents governing other AI agents
- **Marketplace relevance**: Marketplace governance could be automated through COMPASS-like systems

#### 13. PASTA: Automated Compliance Evaluation
- **ID**: 2601.11702
- **Cost**: **$3/eval** for automated multi-policy compliance at expert-level accuracy
- **Approach**: Multi-policy compliance evaluation using structured templates
- **Marketplace relevance**: Every skill listing could have automated compliance scoring for ~$3

### Tier 4: Evaluation & Benchmarking Surveys

#### 14. Evaluation and Benchmarking of LLM Agents: A Survey
- **URL**: https://arxiv.org/abs/2507.21504
- **Date**: Jul 29, 2025
- **Authors**: Mohammadi, Li, Lo, Yip
- **Taxonomy**: (1) evaluation objectives (behavior, capabilities, reliability, safety) × (2) evaluation process (interaction modes, datasets, metrics, tooling)
- **Enterprise gaps**: Role-based access, reliability guarantees, dynamic/long-horizon interactions, compliance

#### 15. Survey on Evaluation of LLM-based Agents (IBM Research)
- **URL**: https://arxiv.org/abs/2503.16416
- **Date**: Mar 20, 2025
- **Scope**: Surveyed **120 agent evaluation frameworks**
- **Missing enterprise requirements**: Multistep granular evaluation, cost-efficiency measurement, safety focus, live adaptive benchmarks

#### 16. MAPS: Multilingual Agent Benchmark
- **URL**: https://arxiv.org/abs/2505.15935
- **Gap**: All existing benchmarks English-only. Skills need multilingual evaluation.

#### 17. EVMbench: Smart Contract Security
- **URL**: https://arxiv.org/abs/2603.04915
- **Relevance**: As crypto/DeFi skills emerge, security evaluation of blockchain agent skills is critical

## 5 Emerging Research Directions

### 1. Supply-Side Automation
Automated skill mining from open-source repos (2603.11808) solves the cold-start supply problem. Instead of waiting for developers to author skills manually, mine existing codebases and generate SKILL.md files automatically.

### 2. Agent Behavioral Economics
Magentic Marketplace (Microsoft) reveals that agent buyers have systematic biases:
- 10-30x first-proposal bias (accept first option)
- Scale degradation (more agents = worse outcomes)
- ACES shows position bias persists in text-only interfaces
**Implication**: Marketplace ranking algorithms must be designed for agent cognition, not human browsing.

### 3. Workspace-Level Collaboration
AWCP moves beyond message-passing to environment sharing. Skills that compose need shared execution contexts — current MCP model is insufficient for complex multi-skill workflows.

### 4. Continual Learning as Marketplace Primitive
- ICL = skill rental (pay-per-use, temporary)
- IWL = skill ownership (one-time, permanent)
- ACuRL enables zero-human skill generation
**Implication**: Two-tier marketplace model where skills can be rented or purchased, with prices reflecting whether knowledge is temporary or permanent.

### 5. Multi-Dimensional Governance
COMPASS (4 agents), market-based governance (insurance + auditing), and PASTA ($3/eval compliance) collectively suggest governance will be:
- Automated (agent-governed agents)
- Market-driven (insurance, procurement standards)
- Cheap ($3/eval enables universal compliance scoring)

## Cross-Paper Evaluation Frameworks Comparison

| Framework | Dimensions | Scale | Enterprise Focus |
|-----------|-----------|-------|-----------------|
| SkillNet SCEMC | 5 (Safety, Completeness, Executability, Maintainability, Cost) | 200K+ skills | Moderate |
| SkillsBench (R3) | 3 conditions × 7 models | 86 tasks, 7,308 trajectories | Low |
| ACES | Bias, stability, position effects | E-commerce specific | Moderate |
| Mohammadi Survey | 2-axis taxonomy | Meta-survey | High |
| Yehudai Survey (IBM) | 4 dimensions + enterprise gaps | 120 frameworks surveyed | High |
| PASTA | Multi-policy compliance | $3/eval automated | High |
| Magentic Marketplace | Behavioral dynamics | Empirical marketplace | High |

## The Agent Market Volatility Problem

ACES + Magentic Marketplace together reveal a fundamental challenge:

1. **Choice homogeneity**: Agents concentrate demand on top-ranked skills → winner-take-all
2. **First-proposal bias**: 10-30x bias means listing position is everything
3. **Model instability**: Model updates reshuffle rankings unpredictably
4. **Gaming vulnerability**: Seller-side agents manipulate descriptions for market share
5. **Scale degradation**: Quality decreases as marketplace grows

This mirrors traditional marketplace problems (Amazon Buy Box, Google rankings) but with **additional unpredictability from model updates** and **no human intervention in purchase decisions**.

## Connection to Practical Marketplace Problems

| Research Paper | Practical Problem Solved |
|---------------|------------------------|
| SkillNet SCEMC | Multi-dimensional skill quality scoring |
| Automating Skill Acquisition | Cold-start supply via automated mining |
| IoA Survey | Agent-to-agent discovery and matching |
| Magentic Marketplace | Understanding agent buyer behavior |
| Ev-Trust | Making malicious skills economically unviable |
| ACES | Auditing agent purchasing decisions |
| AWCP | Multi-skill composition environments |
| Modular Memory | Rental vs purchase pricing model |
| COMPASS | Automated marketplace governance |
| PASTA | Cheap universal compliance scoring |
| ACuRL | Self-improving skill quality |
