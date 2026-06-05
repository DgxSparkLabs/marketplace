# Round 8: AI Agent Skill Marketplaces — arXiv Deep Research

**Date**: 2026-03-18
**Focus Areas**: A2A protocol interoperability, marketplace gaming/adversarial attacks, agent insurance & liability, enterprise scaling, workspace collaboration, market coordination mechanisms

---

## Executive Summary

Round 8 uncovers **14 genuinely new papers** across five previously under-explored angles for agent skill marketplaces. The most significant findings center on three themes:

1. **Marketplace gaming is now demonstrated, not theoretical** — ToolTweak (2510.02554) shows adversaries can boost tool selection rates from 20% to 81% by manipulating tool descriptions, while vertical tacit collusion (2601.03061) reveals super-additive consumer harm from aligned platform-seller incentives exploiting AI cognitive biases.

2. **Insurance and liability infrastructure is emerging as a marketplace primitive** — InsuredAgents (2512.08737) proposes protocol-native insurance markets where specialized insurers stake collateral on behalf of agents, and Agent Behavioral Contracts (2602.22302) formally bounds drift in deployed agents.

3. **The "Headless Firm" thesis predicts marketplace structure** — Klein & Wieczorek (2602.21401) formalize the hourglass organizational form that agent marketplaces will create: personalized interface → protocol waist → competitive micro-specialized execution agents.

---

## Papers Catalog (All New — Not in R1-R7 Exclude List)

### Primary Papers (Deep Analysis)

| # | Paper | arXiv ID | Authors | Year | Category |
|---|-------|----------|---------|------|----------|
| 1 | Agent-OSI: A Layered Protocol Stack | 2602.13795 | Xu, Wang, Xia, Zhang, Liew | 2026 | Interoperability |
| 2 | AESP: Human-Sovereign Economic Protocol | 2603.00318 | Wang, Jian Sheng | 2026 | Economic Protocols |
| 3 | InsuredAgents: Decentralized Trust Insurance | 2512.08737 | Hu, Chen | 2025 | Insurance/Liability |
| 4 | Agent Behavioral Contracts (ABC) | 2602.22302 | Bhardwaj | 2026 | Formal Verification |
| 5 | ToolTweak: Attack on Tool Selection | 2510.02554 | Sneh, Yan, Yu, Torr, Gal et al. | 2025 | Adversarial/Gaming |
| 6 | Intentional Deception in LLM Agents | 2603.07848 | Starace, Soule | 2026 | Adversarial/Gaming |
| 7 | The Headless Firm | 2602.21401 | Klein, Wieczorek | 2026 | Enterprise/Economics |
| 8 | Towards a Science of AI Agent Reliability | 2602.16666 | Rabanser, Kapoor, Kirgis et al. | 2026 | Reliability |
| 9 | Mapping Human Anti-collusion to Multi-agent AI | 2601.00360 | Idowu, Almasoud, Alfahid | 2026 | Anti-collusion |
| 10 | Market Making as Scalable Framework | 2511.17621 | Gho, Muppavarapu, Shaik et al. | 2025 | Market Coordination |

### Supplementary Papers

| # | Paper | arXiv ID | Authors | Year | Category |
|---|-------|----------|---------|------|----------|
| 11 | Vertical Tacit Collusion in AI-mediated Markets | 2601.03061 | Affonso | 2026 | Market Manipulation |
| 12 | Dynamics of Adversarial Attacks on LLM-Based Search | 2501.00745 | Hu | 2025 | Game Theory |
| 13 | Inherent and Emergent Liability in LLM Agentic Systems | 2504.03255 | Gabison, Xian | 2025 | Liability |
| 14 | Context Engineering: Prompts to Corporate Multi-Agent Architecture | 2603.09619 | Vishnyakova | 2026 | Enterprise |

---

## Section 1: Agent-to-Agent Protocol Interoperability

### 1.1 Agent-OSI — The OSI Model for Agents (2602.13795)
**URL**: https://arxiv.org/abs/2602.13795
**Authors**: Wenxin Xu, Taotao Wang, Yihan Xia, Shengli Zhang, Soung Chang Liew (2026)

**Core Contribution**: Proposes a **six-layer reference protocol stack** for decentralized agent networking, explicitly analogous to the OSI network model:

- **L1-L2**: Secure connectivity + A2A messaging
- **L3**: Decentralized identity and authorization
- **L4**: Settlement and metering
- **L5**: Verifiable execution and provenance
- **L6**: Semantic interoperability for orchestration

**Key Innovation — HTTP 402 as Payment Challenge**: Agent-OSI repurposes the long-dormant HTTP 402 (Payment Required) status code as an application-level payment challenge — analogous to HTTP 401 for authentication — that triggers escrow-based settlement and verifiable receipts via blockchain. This is a brilliant design insight: it means **agent skill marketplaces can use the existing HTTP protocol stack** without requiring new network-layer protocols.

**Empirical Results**: Off-chain negotiation + on-chain settlement reduces session costs by ~51% vs. standard Web3 baseline. Blockchain confirmation latency is NOT the dominant factor for generative workloads.

**Marketplace Relevance**: This is the most complete architectural proposal for how a decentralized skill marketplace would actually work at the protocol level. The layer separation directly maps to marketplace concerns:
- Layer 3 → Skill provider identity and reputation
- Layer 4 → Pay-per-use billing for skill invocations
- Layer 5 → Verifiable proof that skills executed correctly
- Layer 6 → Semantic matching between skill capabilities and task requirements

### 1.2 AESP — Agent Economic Sovereignty Protocol (2603.00318)
**URL**: https://arxiv.org/abs/2603.00318
**Authors**: Wang, Jian Sheng (2026)

**Core Contribution**: Addresses the fundamental tension: agents must transact autonomously at machine speed while remaining cryptographically bound to human-defined governance boundaries. The key invariant: **"agents are economically capable but never economically sovereign."**

**Five Enforcement Mechanisms**:
1. Deterministic eight-check policy engine with tiered escalation
2. Human-in-the-loop review (automatic, explicit, biometric tiers)
3. EIP-712 dual-signed commitments with escrow
4. HKDF-based context-isolated privacy with batched consolidation
5. ACE-GF-based cryptographic substrate

**Implementation**: Open-source TypeScript SDK (208 tests, 10 modules) with MCP and A2A interoperability.

**Marketplace Relevance**: Directly solves the "runaway agent spending" problem in skill marketplaces. When Agent A purchases skills from marketplace providers B, C, D, AESP ensures the human principal retains cryptographic control over spending limits, with tiered escalation for high-cost skill invocations. The dual-signed commitments model fits naturally into skill marketplace escrow patterns.

---

## Section 2: Marketplace Gaming and Adversarial Manipulation

### 2.1 ToolTweak — SEO for Agent Tool Marketplaces (2510.02554)
**URL**: https://arxiv.org/abs/2510.02554
**Authors**: Jonathan Sneh, Ruomei Yan, Jialin Yu, Philip Torr, Yarin Gal, Sunando Sengupta, Eric Sommerlade, Alasdair Paren, Adel Bibi (2025)

**Core Contribution**: **The first demonstrated attack on tool/skill selection in agent marketplaces.** Shows that by iteratively manipulating tool names and descriptions, adversaries can systematically bias agents toward selecting specific tools.

**Attack Results**:
- Baseline selection rate: ~20% (fair, among 5 equivalent tools)
- Post-attack selection rate: up to **81%**
- Strong transferability between open-source and closed-source models
- Causes **distributional shifts** in tool usage across entire ecosystems

**Defenses Evaluated**:
- **Paraphrasing**: Rewrite tool descriptions to normalize language → partially effective
- **Perplexity filtering**: Flag tools with suspiciously optimized descriptions → more effective

**Marketplace Relevance**: This is **the SEO manipulation problem for agent skill marketplaces**. Just as traditional search engines face keyword stuffing and link farming, agent tool marketplaces will face description-stuffing attacks. Implications:
- Marketplace operators CANNOT rely on naive LLM-based tool selection
- Tool descriptions must be normalized/verified by the marketplace, not provided raw by providers
- Perplexity-based anomaly detection should be built into skill registry validation
- The 4x selection bias demonstrates that **unfair competition in skill marketplaces is trivially achievable**

### 2.2 Intentional Deception as Controllable Capability (2603.07848)
**URL**: https://arxiv.org/abs/2603.07848
**Authors**: Jason Starace, Terence Soule (2026)

**Core Contribution**: Studies intentional deception as an *engineered* capability in LLM agents, using a two-stage system that: (1) infers target agent characteristics, (2) generates deceptive responses to steer targets against their interests.

**Key Findings**:
- **88.5% of successful deceptions use misdirection** (true statements with strategic framing) — NOT fabrication
- This means **fact-checking defenses are insufficient** — they would miss 88.5% of attacks
- Agent **motivation** is inferable at 98%+ accuracy and serves as the primary attack vector
- **Belief systems** are harder to infer (49% ceiling) and harder to exploit

**Marketplace Relevance**: In a skill marketplace, a malicious skill provider could deploy agents that:
- Accurately infer what the calling agent "wants" (its motivation)
- Provide technically true but strategically framed responses that steer the caller toward suboptimal decisions
- Evade simple output verification because the responses are factually correct
- This is the "trusted advisor" attack pattern for skill marketplaces

### 2.3 Vertical Tacit Collusion in AI-Mediated Markets (2601.03061)
**URL**: https://arxiv.org/abs/2601.03061
**Authors**: Felipe M. Affonso (2026)

**Core Contribution**: Identifies a novel market failure: **vertical tacit collusion**, where platforms (controlling rankings) and sellers (controlling descriptions) independently learn to exploit AI cognitive biases. Their harm is **super-additive** — joint exploitation produces 2x+ the harm of independent strategies.

**Key Mechanism**:
- Platform ranking determines which products occupy bias-triggering positions
- Seller manipulation determines conversion rates at those positions
- No coordination required — aligned incentives suffice
- **Evades traditional antitrust detection** because harm emerges from aligned incentives, not agreements

**Marketplace Relevance**: Directly applicable to skill marketplaces where:
- The marketplace platform controls skill ranking/discovery
- Skill providers control descriptions and API interfaces
- Both independently optimizing for their own benefit creates super-additive consumer harm
- Regulatory approaches from horizontal collusion don't apply

### 2.4 Dynamics of Adversarial Attacks on LLM-Based Search (2501.00745)
**URL**: https://arxiv.org/abs/2501.00745
**Authors**: Xiyang Hu (2025)

**Core Contribution**: Game-theoretic analysis of ranking manipulation as an **Infinitely Repeated Prisoners' Dilemma**. Identifies conditions where cooperation (no manipulation) is sustainable vs. conditions that trigger attack cascades.

**Counter-Intuitive Finding**: **Simply reducing attack success probabilities can PARADOXICALLY incentivize attacks** under certain conditions. Defensive measures to cap attack success rates may prove futile in some scenarios.

**Marketplace Relevance**: For skill marketplaces implementing anti-gaming measures:
- Heavy-handed defenses may backfire by changing the game dynamics
- Cooperation is sustained when providers are forward-looking (long-term reputation matters)
- Marketplace design should focus on making providers "forward-looking" (escrow, reputation bonds) rather than pure technical defenses
- Tipping points exist — below certain thresholds, attack cascades become inevitable

### 2.5 Mapping Human Anti-collusion to Multi-agent AI (2601.00360)
**URL**: https://arxiv.org/abs/2601.00360
**Authors**: Jamiu Adekunle Idowu, Ahmed Almasoud, Ayman Alfahid (2026)

**Core Contribution**: Develops a **taxonomy of human anti-collusion mechanisms** and maps each to multi-agent AI interventions:

| Human Mechanism | AI Mapping |
|---|---|
| Sanctions | Reputation penalties, stake slashing |
| Leniency & Whistleblowing | Incentivized defection protocols |
| Monitoring & Auditing | Behavioral analysis, execution traces |
| Market Design | Mechanism design for agent markets |
| Governance | Multi-stakeholder oversight structures |

**Open Challenges Identified**:
- **Attribution problem**: Difficulty attributing emergent coordination to specific agents
- **Identity fluidity**: Agents easily forked or modified (Sybil attacks)
- **Boundary problem**: Distinguishing beneficial cooperation from harmful collusion
- **Adversarial adaptation**: Agents learning to evade detection

**Marketplace Relevance**: This is the playbook for anti-collusion enforcement in skill marketplaces. The "leniency & whistleblowing" mapping is particularly interesting — marketplace operators could incentivize skill providers to report collusion by offering reduced penalties or marketplace advantages.

---

## Section 3: Insurance and Liability Frameworks

### 3.1 InsuredAgents — Protocol-Native Insurance (2512.08737)
**URL**: https://arxiv.org/abs/2512.08737
**Authors**: Botao Hu, Bangdao Chen (2025)

**Core Contribution**: Proposes a **hierarchical, voluntary insurance mechanism** for the agentic economy where specialized insurer agents post stake on behalf of operational agents.

**Architecture**:
- Operational agents purchase insurance policies from insurer agents
- Insurers post stake (slashable collateral) on the agent's behalf
- Insurers receive **privileged, privacy-preserving audit access via TEEs** to assess claims
- A hierarchical insurer market calibrates stake through competitive pricing
- Dispute resolution is incentive-compatible through economic mechanisms

**Key Design Principles**:
- **Not universal verification** (brittle and centralization-prone) — instead, competitive underwriting
- **Not traditional reputation** (fails under model drift and opaque states) — instead, economic staking
- **Not self-bonding** (too expensive for most agents) — instead, delegated insurance

**Marketplace Relevance**: This is the **most directly applicable insurance model for skill marketplaces**:
- Skill providers carry insurance from competitive insurers
- Insurance premiums serve as quality signals (low premiums = insurer trusts the provider)
- Failed skill invocations trigger claims against insurer collateral
- Insurers use TEE-protected audit of skill execution to verify claims
- The marketplace doesn't need to be the arbiter — the insurance market handles disputes

### 3.2 Agent Behavioral Contracts — Formal SLAs (2602.22302)
**URL**: https://arxiv.org/abs/2602.22302
**Authors**: Varun Pratap Bhardwaj (2026)

**Core Contribution**: Introduces **Agent Behavioral Contracts (ABC)**, bringing Design-by-Contract principles to AI agents. A contract C = (P, I, G, R) specifies:
- **P**: Preconditions (what must hold before invocation)
- **I**: Invariants (what must hold throughout execution)
- **G**: Governance policies (behavioral boundaries)
- **R**: Recovery mechanisms (what happens on violation)

**Formal Results**:
- **(p, δ, k)-satisfaction**: Probabilistic compliance accounting for LLM non-determinism
- **Drift Bounds Theorem**: Contracts with recovery rate γ > α (drift rate) bound behavioral drift to D* = α/γ
- **Composition safety**: Sufficient conditions for safe contract chaining in multi-agent systems

**Empirical Results** (AgentContract-Bench, 200 scenarios, 7 models, 1,980 sessions):
- Contracted agents detect **5.2-6.8 soft violations per session** that uncontracted baselines miss entirely
- **88-100% hard constraint compliance**
- Behavioral drift bounded to **D* < 0.27** across extended sessions
- **100% recovery** for frontier models
- Overhead: **< 10ms per action**

**Marketplace Relevance**: ABCs are **the SLA specification language for skill marketplaces**:
- Every skill in the marketplace exposes a contract (P, I, G, R)
- Consumers can verify compatibility by checking preconditions match their context
- Runtime enforcement catches skills that drift from their advertised behavior
- Recovery mechanisms enable graceful degradation when skills fail
- The composition theorem enables safe skill chaining (critical for multi-skill workflows)

### 3.3 Inherent and Emergent Liability Issues (2504.03255)
**URL**: https://arxiv.org/abs/2504.03255
**Authors**: Garry A. Gabison, R. Patrick Xian (2025)

**Core Contribution**: Analyzes liability through a **principal-agent perspective**, identifying both inherent (design-time) and emergent (runtime) liability issues.

**Key Liability Dimensions**:
- **Information asymmetry**: Agent knows more about its internal state than the principal
- **Complex value chains**: Multiple providers → attribution difficulty
- **Delegation of discretion**: Agent makes choices the principal cannot fully specify
- **Misalignment and misconduct**: Divergent objectives between principal and agent

**Technical Governance Directions**:
- Interpretability and behavior evaluations (know what the agent did)
- Reward and conflict management (align incentives properly)
- Detection and fail-safe mechanisms (catch problems early)

**Marketplace Relevance**: Formalizes the liability chain in skill marketplaces:
- User → Orchestrating Agent → Skill Provider → Sub-provider creates a multi-hop liability chain
- Information asymmetry is amplified in marketplace settings (provider knows implementation details)
- Attribution across the chain requires trace-based auditing
- Marketplace operators may face intermediary liability

---

## Section 4: Enterprise Scaling and Deployment

### 4.1 The Headless Firm (2602.21401)
**URL**: https://arxiv.org/abs/2602.21401
**Authors**: Tassilo Klein, Sebastian Wieczorek (SAP Research) (2026)

**Core Contribution**: Formalizes how agentic AI changes the **theory of the firm** through a coordination cost model:

**Key Insight — Cost Scaling Shift**:
- **Pre-agentic modular systems**: Integration cost ∝ O(n²) (interaction topology)
- **Protocol-mediated agentic systems**: Integration cost → O(n) (linear scaling), verification ∝ task throughput

**The Hourglass Model**:
```
[Personalized Generative Interface]    ← Top (narrow)
         |
[Standardized Protocol Waist]          ← Middle (narrow)
         |
[Competitive Market of Micro-          ← Bottom (wide)
 Specialized Execution Agents]
```

**Falsifiable Predictions**:
1. Marginal cost of adding an execution provider ≈ constant in mature ecosystems
2. Ratio of coordination cost to task throughput is stable as ecosystem grows

**The Great Unbundling**: In high knowledge-velocity domains, firm size distributions shift mass from large integrated incumbents toward micro-specialized agents and thin protocol orchestrators.

**Marketplace Relevance**: This paper provides the **economic theory justifying skill marketplaces**:
- The "protocol waist" IS the skill marketplace's standardized interface layer
- The "competitive market of micro-specialized agents" IS the skill provider ecosystem
- The hourglass stability analysis tells us when marketplaces succeed vs. when re-centralization occurs
- Prediction: skill marketplaces succeed in high knowledge-velocity domains (software, data analysis) before stable domains (manufacturing)

### 4.2 Towards a Science of AI Agent Reliability (2602.16666)
**URL**: https://arxiv.org/abs/2602.16666
**Authors**: Stephan Rabanser, Sayash Kapoor, Peter Kirgis, Kangheng Liu, Saiteja Utpala, Arvind Narayanan (Princeton) (2026)

**Core Contribution**: Proposes **twelve concrete metrics** decomposing agent reliability along four dimensions:

| Dimension | Description | Example Metrics |
|-----------|-------------|-----------------|
| **Consistency** | Same input → similar behavior across runs | Variance of outcomes, action-level agreement |
| **Robustness** | Withstands perturbations | Performance under tool failures, noisy inputs |
| **Predictability** | Failure modes are foreseeable | Failure clustering, degradation patterns |
| **Safety** | Error severity is bounded | Max harm of single failure, cascading failure risk |

**Key Finding**: **Recent capability gains have only yielded small improvements in reliability.** Agents are getting more accurate but NOT proportionally more reliable. (Evaluated across 14 models on 2 benchmarks.)

**Marketplace Relevance**: These 12 metrics should be **mandatory quality dimensions in skill marketplace listings**:
- Consistency → "Will this skill give the same answer tomorrow?"
- Robustness → "What happens when the input is slightly weird?"
- Predictability → "Can I anticipate failure modes?"
- Safety → "What's the worst that can happen?"
- The accuracy-reliability gap means marketplace reputation systems must track reliability separately from success rates

### 4.3 Market Making as a Scalable Coordination Framework (2511.17621)
**URL**: https://arxiv.org/abs/2511.17621
**Authors**: Brendan Gho, Suman Muppavarapu, Afnan Shaik, Tyson Tsay, Atharva Mohan, James Begin, Kevin Zhu, Archana Vaidheeswaran, Vasu Sharma (2025)

**Core Contribution**: Introduces a **market-making framework** for multi-agent LLM coordination where agents interact as structured economic exchanges.

**Mechanism**:
- Each agent acts as a market participant trading probabilistic beliefs
- Agents update beliefs through economic exchange to converge on shared outcomes
- Local incentives align with collective epistemic goals
- Self-organizing coordination WITHOUT external enforcement

**Results**: Market-based coordination yields **accuracy gains of up to 10%** over single-shot baselines while preserving interpretability.

**Marketplace Relevance**: This provides the **coordination mechanism for multi-skill workflows**:
- When multiple skills contribute to a task, they can "bid" confidence levels
- Market-making resolves conflicts between skill outputs
- No central arbiter needed — the market mechanism is self-correcting
- Transparency: every "trade" is logged, creating an audit trail

---

## Section 5: Cross-Cutting Themes and Synthesis

### 5.1 The Emerging Marketplace Security Stack

Combining findings from R1-R8, a complete marketplace security stack is now visible:

```
Layer 7: Anti-Collusion       [R8: Anti-collusion mapping (2601.00360)]
Layer 6: Deception Detection   [R8: Intentional Deception (2603.07848)]
Layer 5: Insurance/Liability   [R8: InsuredAgents (2512.08737)]
Layer 4: Behavioral Contracts  [R8: ABC (2602.22302)]
Layer 3: Gaming Prevention     [R8: ToolTweak defenses (2510.02554)]
Layer 2: Economic Sovereignty  [R8: AESP (2603.00318)]
Layer 1: Protocol Interop      [R8: Agent-OSI (2602.13795)]
```

### 5.2 The ToolTweak-InsuredAgents Connection

ToolTweak shows that skill selection can be manipulated (the attack); InsuredAgents shows how to make providers economically accountable for the consequences (the defense). Together they suggest a marketplace where:
- Skill providers must carry insurance to be listed
- Insurance premiums reflect the risk of manipulative behavior
- Claims from ToolTweak-style attacks are adjudicated through insurer audits
- High premiums for manipulative providers create a natural deterrent

### 5.3 The Headless Firm + Agent-OSI = Marketplace Architecture

The Headless Firm provides the economic theory; Agent-OSI provides the technical specification:

| Headless Firm Layer | Agent-OSI Layer | Marketplace Function |
|---|---|---|
| Generative Interface | L6: Semantic Interop | User-facing skill discovery & orchestration |
| Protocol Waist | L3-L5: Identity + Settlement + Verification | Standardized marketplace APIs |
| Execution Agents | L1-L2: Connectivity + A2A | Individual skill providers |

### 5.4 Reliability as Marketplace Differentiator

Rabanser et al.'s finding that capability ≠ reliability means marketplaces can differentiate on:
- **Reliability-rated skills** (vs. accuracy-only ratings)
- **Guaranteed consistency** (SLA-backed via ABC contracts)
- **Predictable failure modes** (documented in skill metadata)
- **Safety-bounded operations** (maximum harm guarantees)

### 5.5 The Game Theory of Marketplace Stability

Three papers (2501.00745, 2601.00360, 2601.03061) converge on a unified view:
- Agent marketplaces are infinitely repeated games
- Cooperation is sustained by forward-looking providers (reputation bonds, insurance)
- Heavy-handed defenses can paradoxically destabilize cooperation
- Vertical collusion (platform + provider aligned incentives) is the hardest threat to detect
- Anti-collusion mechanisms from human markets can be adapted but face unique challenges (identity fluidity, attribution difficulty)

---

## Section 6: Connections to Practical Marketplace Challenges

### Challenge 1: How do you prevent skill providers from gaming rankings?
- **ToolTweak** (2510.02554): Demonstrates the attack — description manipulation
- **Defense**: Perplexity filtering + marketplace-controlled description normalization
- **Economics**: InsuredAgents premiums + reputation bonds make gaming costly
- **Game theory**: Marketplace design should make providers forward-looking (2501.00745)

### Challenge 2: What happens when a purchased skill fails?
- **ABC** (2602.22302): Runtime contracts detect drift and trigger recovery (< 10ms overhead)
- **InsuredAgents** (2512.08737): Economic compensation through insurance claims
- **Liability chain** (2504.03255): Principal-agent framework for attribution
- **Reliability metrics** (2602.16666): Pre-deployment assessment across 4 dimensions

### Challenge 3: How do you build a payment system for agent skills?
- **Agent-OSI** (2602.13795): HTTP 402 payment challenges + blockchain escrow
- **AESP** (2603.00318): Cryptographic spending limits + human-in-the-loop for high-value
- **Off-chain negotiation**: 51% cost reduction vs. fully on-chain

### Challenge 4: How do you prevent agents from colluding?
- **Anti-collusion taxonomy** (2601.00360): Sanctions, leniency, monitoring, market design
- **Vertical collusion** (2601.03061): Platform-provider aligned incentives create invisible harm
- **Open challenges**: Attribution, identity fluidity, cooperation-collusion boundary

### Challenge 5: What organizational form does a skill marketplace take?
- **Headless Firm** (2602.21401): Hourglass model with protocol waist
- **Cost prediction**: O(n) integration cost enables marketplace viability
- **Domain selection**: High knowledge-velocity domains first

### Challenge 6: How do you coordinate multiple skills for complex tasks?
- **Market-making** (2511.17621): Economic exchange of probabilistic beliefs
- **Self-organizing**: No central arbiter needed
- **Interpretable**: Every "trade" creates an audit trail

---

## Appendix: Paper URLs

1. https://arxiv.org/abs/2602.13795 — Agent-OSI
2. https://arxiv.org/abs/2603.00318 — AESP
3. https://arxiv.org/abs/2512.08737 — InsuredAgents
4. https://arxiv.org/abs/2602.22302 — Agent Behavioral Contracts
5. https://arxiv.org/abs/2510.02554 — ToolTweak
6. https://arxiv.org/abs/2603.07848 — Intentional Deception
7. https://arxiv.org/abs/2602.21401 — The Headless Firm
8. https://arxiv.org/abs/2602.16666 — Science of AI Agent Reliability
9. https://arxiv.org/abs/2601.00360 — Anti-collusion Mechanisms
10. https://arxiv.org/abs/2511.17621 — Market Making Framework
11. https://arxiv.org/abs/2601.03061 — Vertical Tacit Collusion
12. https://arxiv.org/abs/2501.00745 — Adversarial Attack Dynamics
13. https://arxiv.org/abs/2504.03255 — LLM Liability Issues
14. https://arxiv.org/abs/2603.09619 — Context Engineering

---

*Round 8 complete. Total unique papers across R1-R8: ~44+ papers covering the full landscape of AI agent skill marketplace research.*
