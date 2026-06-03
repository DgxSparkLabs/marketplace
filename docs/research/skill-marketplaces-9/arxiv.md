# AI Agent Skill Marketplaces - Round 9 arXiv Paper Survey

**Date**: March 2026  
**Round**: 9 (supplementing R1-R8, which catalogued 59+ papers)  
**New papers found**: 31  
**Search methodology**: 8 DuckDuckGo site:arxiv.org searches + 2 arXiv native search pages, with full abstract scraping of each new paper  

---

## Executive Summary

Round 9 identifies **31 new papers** not covered in R1-R8, spanning 8 thematic categories. Key emerging trends include:

1. **Agentic economy theorization** - Major economics-focused papers from Microsoft Research and others modeling two-sided agent marketplaces with rigorous economic theory
2. **Execution-layer security hardening** - The "ClawHavoc" campaign fallout drives new runtime defense architectures (PRISM, SAE, Proof-of-Guardrail)
3. **Inter-agent trust infrastructure** - Multiple papers proposing DID/VC-based identity, hybrid trust models (Proof+Stake+Reputation), and agent ranking algorithms
4. **A2A protocol commercialization** - Concrete extensions to Google's A2A protocol with micropayments (x402), ledger-anchored identities, and security analysis
5. **Reliability engineering for agents** - New benchmarks (ReliabilityBench, MAS-FIRE) and metrics (MTTR-A) bringing SRE practices to agent systems
6. **Governance-as-a-Service** - Runtime policy enforcement layers that treat governance as infrastructure

---

## Table of Contents

- [A. Skill Ecosystem & Marketplace Analysis](#a-skill-ecosystem--marketplace-analysis) (2 papers)
- [B. Agentic Economy & Market Economics](#b-agentic-economy--market-economics) (4 papers)
- [C. Multi-Agent Orchestration & Composition](#c-multi-agent-orchestration--composition) (3 papers)
- [D. Trust, Reputation & Identity](#d-trust-reputation--identity) (6 papers)
- [E. Agent-to-Agent Protocol & Commerce](#e-agent-to-agent-protocol--commerce) (4 papers)
- [F. Security & Defense](#f-security--defense) (5 papers)
- [G. Governance, Regulation & Compliance](#g-governance-regulation--compliance) (3 papers)
- [H. Reliability, Failure Recovery & Insurance](#h-reliability-failure-recovery--insurance) (4 papers)

---

## A. Skill Ecosystem & Marketplace Analysis

### A1. Agent Skills: A Data-Driven Analysis of Claude Skills for Extending Large Language Model Functionality

| Field | Value |
|-------|-------|
| **arXiv ID** | [2602.08004](https://arxiv.org/abs/2602.08004) |
| **Authors** | George Ling, Shanshan Zhong, Richard Huang |
| **Date** | 2026-02-08 |
| **Category** | cs.SE |

**Abstract Summary**: Conducts the first large-scale data-driven analysis of 40,285 publicly listed agent skills from a major marketplace (skills.sh). Finds that skill publication occurs in short bursts tracking community attention shifts, content is concentrated in software engineering workflows, and there exists a pronounced supply-demand imbalance. Identifies strong ecosystem homogeneity with widespread intent-level redundancy and non-trivial safety risks from skills enabling system-level actions.

**Key Contribution**: Quantitative marketplace characterization - supply/demand imbalance analysis, adoption patterns, content concentration metrics, and safety risk profiling across 40K+ skills.

**Relevance**: **HIGH** - Direct marketplace ecosystem analysis providing empirical evidence for skill categorization, adoption dynamics, and market inefficiencies.

---

### A2. Execution Is the New Attack Surface: Survivability-Aware Agentic Crypto Trading with OpenClaw-Style Local Executors

| Field | Value |
|-------|-------|
| **arXiv ID** | [2603.10092](https://arxiv.org/abs/2603.10092) |
| **Authors** | Ailiya Borjigin, Igor Stadnyk, Ben Bilski, Serhii Hovorov, Sofiia Pidturkina |
| **Date** | 2026-03-10 |
| **Category** | cs.CR |

**Abstract Summary**: Addresses the shift from "wrong answers" to "execution-induced loss" in skill-enabled agent systems. Skill marketplaces (e.g., skills.sh) create a growing capability supply chain where untrusted prompts or compromised skills can trigger irreversible side effects. Proposes Survivability-Aware Execution (SAE), an execution-layer middleware enforcing non-bypassable last-mile invariants. SAE reduces maximum drawdown by 93.1% and attack success from 1.00 to 0.728 on crypto trading benchmarks.

**Key Contribution**: Introduces the Delegation Gap (DG) metric for measuring execution safety in skill-marketplace-sourced agents, with formal execution contracts.

**Relevance**: **HIGH** - Directly models skill marketplace supply chain risks and proposes execution-layer defenses for marketplace-sourced capabilities.

---

## B. Agentic Economy & Market Economics

### B1. The Agentic Economy

| Field | Value |
|-------|-------|
| **arXiv ID** | [2505.15799](https://arxiv.org/abs/2505.15799) |
| **Authors** | David M. Rothschild, Markus Mobius, Jake M. Hofman, Eleanor W. Dillon, Daniel G. Goldstein, Nicole Immorlica, Sonia Jaffe, Brendan Lucier, Aleksandrs Slivkins, Matthew Vogel |
| **Date** | 2025-05-21 (revised 2025-05-29) |
| **Category** | cs.CY |

**Abstract Summary**: Explores implications of an agentic economy where assistant agents (consumer-side) and service agents (business-side) interact programmatically. Distinguishes "unscripted" interactions (enabled by NL and protocol advances) from "unrestricted" interactions (dependent on market structures and governance). Examines tensions between agentic walled gardens vs. open web of agents, implications for advertising/discovery, micro-transactions, and unbundling/rebundling of digital goods.

**Key Contribution**: Foundational economic framing of two-sided agentic markets from Microsoft Research economists; introduces the unscripted vs. unrestricted interaction taxonomy.

**Relevance**: **CRITICAL** - Core theoretical paper on agent marketplace economics, authored by prominent Microsoft Research economists including Slivkins and Immorlica.

---

### B2. An Economy of AI Agents

| Field | Value |
|-------|-------|
| **arXiv ID** | [2509.01063](https://arxiv.org/abs/2509.01063) |
| **Authors** | Gillian K. Hadfield, Andrew Koh |
| **Date** | 2025-09-01 |
| **Category** | econ.GN |

**Abstract Summary**: Surveys how AI agents with the ability to plan and execute complex tasks over long horizons may be deployed across the economy. Highlights open questions for economists: how agents interact with humans and each other, shape markets and organizations, and what institutions might be required for well-functioning markets.

**Key Contribution**: Economics-discipline survey of AI agent economic participation; identifies institutional requirements for agent-mediated markets.

**Relevance**: **HIGH** - Theoretical economics perspective on institutional design for agent marketplaces.

---

### B3. Magentic Marketplace: An Open-Source Environment for Studying Agentic Markets

| Field | Value |
|-------|-------|
| **arXiv ID** | [2510.25779](https://arxiv.org/abs/2510.25779) |
| **Authors** | Gagan Bansal, Wenyue Hua, Adam Fourney, Amanda Swearngin, Will Epperson, Tyler Payne, Jake M. Hofman, Brendan Lucier, Chinmay Singh, Markus Mobius, Akshay Nambi, Archana Yadav, Kevin Gao, David M. Rothschild, Aleksandrs Slivkins, Daniel G. Goldstein, Hussein Mozannar, Nicole Immorlica, Maya Murad, Matthew Vogel, Subbarao Kambhampati, Eric Horvitz, Saleema Amershi |
| **Date** | 2025-10-27 |
| **Category** | cs.MA |

**Abstract Summary**: Develops Magentic-Marketplace, a simulated environment for studying two-sided agentic marketplaces where Assistant agents represent consumers and Service agents represent businesses. Experiments reveal frontier models can approach optimal welfare under ideal conditions but performance degrades sharply with scale. All models exhibit **severe first-proposal bias**, creating 10-30x advantages for response speed over quality.

**Key Contribution**: First open-source simulation environment for agent marketplace research; empirical discovery of first-proposal bias as a critical market failure mechanism.

**Relevance**: **CRITICAL** - Directly addresses agent marketplace dynamics with empirical simulation; from Microsoft Research with Horvitz, Kambhampati et al.

---

### B4. Beyond the Sum: Unlocking AI Agents Potential Through Market Forces

| Field | Value |
|-------|-------|
| **arXiv ID** | [2501.10388](https://arxiv.org/abs/2501.10388) |
| **Authors** | Jordi Montes Sanabria, Pol Alvarez Vecino |
| **Date** | 2024-12-19 (revised 2025-01-23) |
| **Category** | cs.CY |

**Abstract Summary**: Systematic analysis of infrastructure requirements for AI agents to function as autonomous participants in digital markets. Examines four key areas: identity and authorization, service discovery, interfaces, and payment systems. Shows existing human-centric infrastructure actively impedes agent participation and argues infrastructure changes represent a fundamental step toward new forms of economic organization.

**Key Contribution**: Infrastructure gap analysis identifying four critical barriers to agent market participation (identity, discovery, interfaces, payments).

**Relevance**: **HIGH** - Directly maps the infrastructure stack needed for agent skill marketplaces to function.

---

## C. Multi-Agent Orchestration & Composition

### C1. Verified Multi-Agent Orchestration: A Plan-Execute-Verify-Replan Framework

| Field | Value |
|-------|-------|
| **arXiv ID** | [2603.11445](https://arxiv.org/abs/2603.11445) |
| **Authors** | Xing Zhang, Yanwei Cui, Guanghui Wang, Qucy Wei Qiu, Ziyuan Li, Fangwei Han, Yajing Huang, Hengzhi, Bin Zhu, Peiyang He |
| **Date** | 2026-03-12 |
| **Category** | cs.AI |

**Abstract Summary**: Presents VMAO, a framework that coordinates specialized LLM-based agents through a verification-driven iterative loop. Decomposes complex queries into DAGs of sub-questions, executes through domain-specific agents in parallel, verifies completeness via LLM-based evaluation, and adaptively replans. Improves answer completeness from 3.1 to 4.2 and source quality from 2.6 to 4.1 on 5-point scale vs. single-agent baseline.

**Key Contribution**: DAG-based parallel skill execution with verification-driven quality assurance loop.

**Relevance**: **MEDIUM** - Demonstrates orchestration patterns applicable to multi-skill composition in marketplaces.

---

### C2. AgentOrchestra: Orchestrating Multi-Agent Intelligence with the TEA Protocol

| Field | Value |
|-------|-------|
| **arXiv ID** | [2506.12508](https://arxiv.org/abs/2506.12508) |
| **Authors** | Wentao Zhang, Liang Zeng, Yuzhen Xiao, Yongcong Li, Ce Cui, Yilei Zhao, Rui Hu, Zhou Yang, Yahui, Bo An |
| **Date** | 2025-06-14 (revised 2026-01-11, v5) |
| **Category** | cs.AI |

**Abstract Summary**: Addresses limitations of existing agent protocols (A2A, MCP) which under-specify cross-entity lifecycle management, version tracking, and environment integration. Introduces the Tool-Environment-Agent (TEA) protocol, modeling environments, agents, and tools as first-class resources with explicit lifecycles and versioned interfaces. TEA enables continual self-evolution through closed feedback loops. AgentOrchestra achieves 89.04% on GAIA benchmark, establishing SOTA.

**Key Contribution**: TEA protocol unifying tool/agent/environment lifecycle management with versioned interfaces - directly addresses marketplace composability.

**Relevance**: **HIGH** - TEA protocol provides formal lifecycle and version management critical for skill marketplace interoperability.

---

### C3. Structure Matters: Evaluating Multi-Agents Orchestration in Generative Therapeutic Chatbots

| Field | Value |
|-------|-------|
| **arXiv ID** | [2603.00774](https://arxiv.org/abs/2603.00774) |
| **Authors** | Sina Elahimanesh, Mohammadali Mohammadkhani, Sara Zahedi Movahed, Mohammadmahdi Abootorabi, Shayan Salehi, Abbas Edalat |
| **Date** | 2026-02-28 |
| **Category** | cs.HC |

**Abstract Summary**: Compares three architectural variants for therapeutic chatbots: multi-agent system with FSM orchestration, single-agent with same knowledge, and unguided LLM. RCT with N=66 shows multi-agent FSM system is perceived as significantly more natural and human-like, demonstrating that orchestration architecture matters as much as prompting.

**Key Contribution**: RCT evidence that multi-agent orchestration architecture (not just prompt engineering) determines quality in skill-composed systems.

**Relevance**: **MEDIUM** - Empirical evidence for orchestration architecture value, applicable to marketplace skill composition patterns.

---

## D. Trust, Reputation & Identity

### D1. Internet 3.0: Architecture for a Web-of-Agents with AgentRank-UC

| Field | Value |
|-------|-------|
| **arXiv ID** | [2509.04979](https://arxiv.org/abs/2509.04979) |
| **Authors** | Rajesh Tembarai Krishnamachari, Srividya Rajesh |
| **Date** | 2025-09-05 |
| **Category** | cs.AI |

**Abstract Summary**: Proposes DOVIS, a five-layer protocol (Discovery, Orchestration, Verification, Incentives, Semantics) enabling privacy-preserving performance aggregation across agent ecosystems. Implements AgentRank-UC, a dynamic trust-aware algorithm combining usage frequency and competence (quality, cost, safety, latency) into unified ranking. Provides theoretical guarantees on convergence, robustness, and Sybil resistance.

**Key Contribution**: PageRank-equivalent for agent marketplaces (AgentRank-UC) with formal Sybil resistance guarantees and privacy-preserving performance aggregation.

**Relevance**: **CRITICAL** - Directly addresses agent marketplace ranking/discovery with formal guarantees - analogous to PageRank for the agent web.

---

### D2. The Trust Fabric: Decentralized Interoperability and Economic Coordination for the Agentic Web

| Field | Value |
|-------|-------|
| **arXiv ID** | [2507.07901](https://arxiv.org/abs/2507.07901) |
| **Authors** | Sree Bhargavi Balija, Rekha Singal, Ramesh Raskar, Erfan Darzi, Raghu Bala, Thomas Hardjono, Ken Huang |
| **Date** | 2025-07-10 (revised 2025-07-22) |
| **Category** | cs.CR |

**Abstract Summary**: Presents the Nanda Unified Architecture for decentralized agent interoperability. Three core innovations: DID-based agent discovery, semantic agent cards with verifiable credentials and composability profiles, and a dynamic trust layer integrating behavioral attestations with policy compliance. Introduces X42/H42 micropayments and MAESTRO security framework. Real-world deployments demonstrate 99.9% compliance in healthcare.

**Key Contribution**: Production-deployed decentralized trust architecture unifying MIT trust research with Cisco/Synergetics deployments; micropayment integration.

**Relevance**: **HIGH** - Comprehensive trust-and-commerce infrastructure for agent marketplaces with real deployments.

---

### D3. AI Agents with Decentralized Identifiers and Verifiable Credentials

| Field | Value |
|-------|-------|
| **arXiv ID** | [2511.02841](https://arxiv.org/abs/2511.02841) |
| **Authors** | Sandro Rodriguez Garzon, Awid Vaziry, Enis Mert Kuzu, Dennis Enrique Gehrmann, Buse Varkan, Alexander Gaballa, Axel Kupper |
| **Date** | 2025-10-01 (revised 2025-12-15) |
| **Category** | cs.CR |

**Abstract Summary**: Presents a framework where each agent has a self-sovereign digital identity combining W3C DID (ledger-anchored) with W3C Verifiable Credentials (third-party issued). Agents prove DID ownership for authentication and establish cross-domain trust via VC exchange. Prototype evaluation demonstrates feasibility but reveals limitations when LLMs solely control security procedures.

**Key Contribution**: Working prototype of DID+VC identity for agents with A2A protocol integration; identifies LLM limitations in controlling security procedures autonomously.

**Relevance**: **HIGH** - Identity infrastructure directly applicable to agent marketplace authentication and trust establishment.

---

### D4. Inter-Agent Trust Models: A Comparative Study (A2A, AP2, ERC-8004, and Beyond)

| Field | Value |
|-------|-------|
| **arXiv ID** | [2511.03434](https://arxiv.org/abs/2511.03434) |
| **Authors** | Botao Hu, Helena Rong |
| **Date** | 2025-11-05 |
| **Category** | cs.HC |

**Abstract Summary**: Comprehensive comparative study of six trust model primitives: Brief (verifiable claims), Claim (self-proclaimed identity), Proof (cryptographic verification including ZKP and TEE), Stake (bonded collateral with slashing), Reputation (crowd feedback), and Constraint (sandboxing). Evaluates A2A, AP2, and ERC-8004 protocols against security, privacy, latency/cost, and social robustness metrics. Argues for trustless-by-default architectures anchored in Proof+Stake, augmented by Brief and Reputation.

**Key Contribution**: First systematic taxonomy of trust primitives for agent protocols with cross-protocol comparison; recommends hybrid Proof+Stake+Reputation trust architecture.

**Relevance**: **CRITICAL** - Directly addresses trust model design for agent marketplaces with concrete protocol comparisons and design guidelines.

---

### D5. Architecting Trust in Artificial Epistemic Agents

| Field | Value |
|-------|-------|
| **arXiv ID** | [2603.02960](https://arxiv.org/abs/2603.02960) |
| **Authors** | Nahema Marchal, Stephanie Chan, Matija Franklin, Manon Revel, Geoff Keeling, Roberta Fischli, Gabriel Bilva, Iason |
| **Date** | 2026-03-03 |
| **Category** | cs.AI |

**Abstract Summary**: Proposes a normative framework for trust in AI agents functioning as epistemic agents (knowledge creators/curators). Centers on three pillars: cultivating trustworthiness (epistemic competence, falsifiability, virtuous behaviors), aligning with human epistemic goals, and reinforcing socio-epistemic infrastructure including "knowledge sanctuaries" and provenance systems.

**Key Contribution**: Normative trust framework for agent knowledge ecosystems; introduces "knowledge sanctuaries" concept for protecting human epistemic resilience.

**Relevance**: **MEDIUM** - Provides theoretical trust foundations applicable to marketplace curation and knowledge-agent service quality.

---

### D6. Designing Reputation Systems for Manufacturing Data Trading Markets

| Field | Value |
|-------|-------|
| **arXiv ID** | [2511.19930](https://arxiv.org/abs/2511.19930) |
| **Authors** | Kenta Yamamoto, Teruaki Hayashi |
| **Date** | 2025-11-25 |
| **Category** | cs.GT |

**Abstract Summary**: Develops a multi-agent data-market simulator evaluating five reputation systems (Time-decay, Bayesian-beta, PageRank, PowerTrust, PeerTrust) for manufacturing data marketplaces. Integrates RL for adaptive agent behavior and IRL for utility estimation. Finds PeerTrust achieves strongest price-quality alignment while preventing monopolistic dominance. Develops a hybrid mechanism combining strengths of multiple reputation systems.

**Key Contribution**: Systematic comparison of 5 reputation mechanisms in simulated data marketplace; proposes hybrid reputation design outperforming individual systems.

**Relevance**: **HIGH** - Reputation system design directly transferable to agent skill marketplace quality assurance.

---

## E. Agent-to-Agent Protocol & Commerce

### E1. Towards Multi-Agent Economies: Enhancing A2A with Ledger-Anchored Identities and x402 Micropayments

| Field | Value |
|-------|-------|
| **arXiv ID** | [2507.19550](https://arxiv.org/abs/2507.19550) |
| **Authors** | Awid Vaziry, Sandro Rodriguez Garzon, Axel Kupper |
| **Date** | 2025-07-24 |
| **Category** | cs.MA |

**Abstract Summary**: Extends Google's A2A protocol with DLT-based agent discovery (on-chain AgentCards as smart contracts) and x402 micropayments (blockchain-agnostic HTTP-based payments via HTTP 402 status code). Enables agents to seamlessly discover, authenticate, and compensate each other across organizational boundaries.

**Key Contribution**: Concrete A2A extension with working micropayment layer (x402) and on-chain identity - directly enables agent commerce.

**Relevance**: **CRITICAL** - Core agent marketplace commerce infrastructure extending the dominant A2A protocol with payments.

---

### E2. Building A Secure Agentic AI Application Leveraging A2A Protocol

| Field | Value |
|-------|-------|
| **arXiv ID** | [2504.16902](https://arxiv.org/abs/2504.16902) |
| **Authors** | Idan Habler, Ken Huang, Vineeth Sai Narajala, Prashant Kulkarni |
| **Date** | 2025-04-23 (revised 2025-05-02) |
| **Category** | cs.CR |

**Abstract Summary**: Comprehensive security analysis of Google's A2A protocol using the MAESTRO framework. Assesses Agent Card management, task execution integrity, and authentication methodologies. Recommends secure development methodologies and architectural best practices. Explores A2A + MCP synergy for secure interoperability.

**Key Contribution**: First dedicated security analysis of A2A protocol with MAESTRO threat modeling; practical security guidelines for A2A deployments.

**Relevance**: **HIGH** - Security foundation for A2A-based agent marketplaces.

---

### E3. Agentic Services Computing

| Field | Value |
|-------|-------|
| **arXiv ID** | [2509.24380](https://arxiv.org/abs/2509.24380) |
| **Authors** | Shuiguang Deng, Hailiang Zhao, Ziqi Wang, Guanjie Cheng, Peng Chen, Wenzhuo Qian, Zhiwei Ling, Jianwei Yin, Albert Y. Zomaya, Schahram Dustdar |
| **Date** | 2025-09-29 (revised 2025-10-10) |
| **Category** | cs.SE |

**Abstract Summary**: Proposes Agentic Services Computing (ASC), reimagining services as autonomous, adaptive, collaborative agents. Organized around a four-phase lifecycle (Design, Deployment, Operation, Evolution) and four research dimensions: perception/context modeling, autonomous decision-making, multi-agent collaboration, and evaluation with trustworthiness. Surveys representative works across academia and industry.

**Key Contribution**: Comprehensive SOA-to-agent paradigm mapping with four-phase lifecycle framework for agent-as-service ecosystems.

**Relevance**: **HIGH** - Bridges traditional services computing with agent marketplace paradigms; lifecycle framework applicable to skill marketplace design.

---

### E4. Agoran: An Agentic Open Marketplace for 6G RAN Automation

| Field | Value |
|-------|-------|
| **arXiv ID** | [2508.09159](https://arxiv.org/abs/2508.09159) |
| **Authors** | Ilias Chatzistefanidis, Navid Nikaein, Andrea Leone, Ali Maatouk, Leandros Tassiulas, Roberto Morabito, Ioannis Pitsiorlas, Marios Kountouris |
| **Date** | 2025-08-05 (revised 2025-08-21) |
| **Category** | cs.NI |

**Abstract Summary**: Introduces Agoran, an agentic marketplace for 6G network automation modeled on the ancient Greek agora. Features three autonomous AI branches: Legislative (compliance via RAG-LLMs), Executive (real-time awareness), and Judicial (Trust Score with malicious behavior detection). Stakeholder Negotiation Agents and Mediator Agent negotiate Pareto-optimal offers. Achieves 37% throughput increase, 73% latency reduction on 5G testbed.

**Key Contribution**: Working agentic marketplace deployment for network resource trading with three-branch governance architecture and real testbed results.

**Relevance**: **HIGH** - Concrete marketplace implementation with trust scoring, negotiation agents, and governance separation - patterns transferable to skill marketplaces.

---

## F. Security & Defense

### F1. Proof-of-Guardrail in AI Agents and What (Not) to Trust from It

| Field | Value |
|-------|-------|
| **arXiv ID** | [2603.05786](https://arxiv.org/abs/2603.05786) |
| **Authors** | Xisen Jin, Michael Duan, Qin Lin, Aaron Chan, Zhenglun Chen, Junyi Du, Xiang Ren |
| **Date** | 2026-03-06 |
| **Category** | cs.CR |

**Abstract Summary**: Proposes proof-of-guardrail, enabling developers to provide cryptographic proof that responses are generated after a specific open-source guardrail is executed. Runs agent and guardrail inside a Trusted Execution Environment (TEE) producing signed attestation verifiable offline. Implemented for OpenClaw agents. Highlights risk of malicious developers actively jailbreaking the guardrail.

**Key Contribution**: TEE-based verifiable guardrail execution for marketplace agents; first cryptographic proof system for agent safety compliance.

**Relevance**: **CRITICAL** - Directly enables verifiable safety guarantees in skill marketplaces - agents can prove guardrail compliance to marketplace.

---

### F2. Security Risks of AI Agents Hiring Humans: An Empirical Marketplace Study

| Field | Value |
|-------|-------|
| **arXiv ID** | [2602.19514](https://arxiv.org/abs/2602.19514) |
| **Authors** | Pulak Mehta |
| **Date** | 2026-02-23 |
| **Category** | cs.CR |

**Abstract Summary**: Empirical measurement study of RENTAHUMAN.AI, a marketplace where AI agents hire humans via APIs and MCP. Analyzes 303 bounties; 32.7% originate from programmatic channels. Identifies six abuse classes: credential fraud, identity impersonation, automated reconnaissance, social media manipulation, authentication circumvention, and referral fraud - all purchasable for median $25/worker.

**Key Contribution**: First empirical study of agent-to-human marketplace abuse; quantifies the attack surface when agents are buyers rather than sellers.

**Relevance**: **HIGH** - Novel marketplace security threat model where agents are buyers; directly relevant to marketplace trust design.

---

### F3. Security Considerations for Multi-agent Systems

| Field | Value |
|-------|-------|
| **arXiv ID** | [2603.09002](https://arxiv.org/abs/2603.09002) |
| **Authors** | Tam Nguyen, Moses Ndebugre, Dheeraj Arremsetty |
| **Date** | 2026-03-09 |
| **Category** | cs.CR |

**Abstract Summary**: Systematically characterizes MAS threat landscape and quantitatively evaluates 16 security frameworks. Identifies 193 distinct threat items across nine risk categories. No framework achieves majority coverage of any category. Non-Determinism (mean 1.231/3) and Data Leakage (1.340/3) are most under-addressed. OWASP Agentic Security Initiative leads at 65.3% coverage.

**Key Contribution**: First cross-framework security comparison for MAS; reveals critical gaps in Non-Determinism and Data Leakage coverage across all 16 frameworks evaluated.

**Relevance**: **HIGH** - Comprehensive security gap analysis directly applicable to marketplace security framework selection.

---

### F4. Contextualized Privacy Defense for LLM Agents

| Field | Value |
|-------|-------|
| **arXiv ID** | [2603.02983](https://arxiv.org/abs/2603.02983) |
| **Authors** | Yule Wen, Yanzhe Zhang, Jianxun Lian, Xiaoyuan Yi, Xing Xie, Diyi Yang |
| **Date** | 2026-03-03 |
| **Category** | cs.CR |

**Abstract Summary**: Proposes Contextualized Defense Instructing (CDI), a privacy defense paradigm where an instructor model generates step-specific, context-aware privacy guidance during agent execution. Trained via RL using failure trajectories with privacy violations. Achieves 94.2% privacy preservation with 80.6% helpfulness, outperforming static defenses.

**Key Contribution**: RL-trained privacy instructor that provides context-aware guidance during agent execution; superior privacy-helpfulness trade-off.

**Relevance**: **MEDIUM** - Privacy defense mechanism applicable to marketplace agents handling sensitive user data during skill execution.

---

### F5. OpenClaw PRISM: A Zero-Fork, Defense-in-Depth Runtime Security Layer

| Field | Value |
|-------|-------|
| **arXiv ID** | [2603.11853](https://arxiv.org/abs/2603.11853) |
| **Authors** | Frank Li |
| **Date** | 2026-03-12 |
| **Category** | cs.CR |

**Abstract Summary**: Runtime security layer for OpenClaw-based agent gateways. PRISM distributes enforcement across ten lifecycle hooks spanning message ingress, prompt construction, tool execution, result persistence, outbound messaging, sub-agent spawning, and startup. Integrates hybrid heuristic+LLM scanning, session-scoped risk accumulation with TTL decay, policy-enforced controls, and tamper-evident audit.

**Key Contribution**: Production-ready defense-in-depth runtime security with ten lifecycle enforcement hooks specifically designed for agent gateway/marketplace architectures.

**Relevance**: **HIGH** - Directly applicable to skill marketplace runtime security; ten-hook lifecycle provides comprehensive enforcement points.

---

## G. Governance, Regulation & Compliance

### G1. Governance-as-a-Service: A Multi-Agent Framework for AI System Compliance and Policy Enforcement

| Field | Value |
|-------|-------|
| **arXiv ID** | [2508.18765](https://arxiv.org/abs/2508.18765) |
| **Authors** | Suyash Gaurav, Jukka Heikkonen, Jatin Chaudhary |
| **Date** | 2025-08-26 (revised 2025-08-27) |
| **Category** | cs.LG |

**Abstract Summary**: Introduces Governance-as-a-Service (GaaS), a modular policy-driven enforcement layer that regulates agent outputs at runtime without altering model internals. Uses declarative rules and Trust Factor scoring based on compliance and severity-weighted violations. Supports coercive, normative, and adaptive interventions with graduated enforcement. Evaluated with LLaMA3, Qwen3, DeepSeek-R1 across content generation and financial trading.

**Key Contribution**: Runtime governance layer treating compliance as infrastructure service; Trust Factor mechanism for dynamic agent trust scoring.

**Relevance**: **CRITICAL** - GaaS pattern directly applicable to marketplace governance; Trust Factor scoring enables marketplace-level quality enforcement.

---

### G2. Permission Manifests for Web Agents

| Field | Value |
|-------|-------|
| **arXiv ID** | [2601.02371](https://arxiv.org/abs/2601.02371) |
| **Authors** | Samuele Marro, Alan Chan, Xinxing Ren, Lewis Hammond, Jesse Wright, Gurjyot Wanga, Tiziano Piccardi, Nuno Campos, Tobin South, Jialin Yu, Sunando Sengupta, Eric Sommerlade, Alex Pentland, Philip Torr, Jiaxin Pei |
| **Date** | 2025-12-07 (revised 2026-01-12) |
| **Category** | cs.CY |

**Abstract Summary**: Introduces agent-permissions.json, a robots.txt-style manifest where websites specify allowed agent interactions. Low-friction coordination: site owners write a simple JSON file, agents parse and implement provisions. Extends the spirit of robots.txt to LLM-mediated interaction era.

**Key Contribution**: Standardized permission manifest for web agent interactions; practical governance mechanism analogous to robots.txt for the agent era.

**Relevance**: **HIGH** - Permission manifest pattern directly applicable to skill marketplace capability declarations and access control.

---

### G3. Policy or Community?: Supporting Individual Model Creators in Model Marketplaces

| Field | Value |
|-------|-------|
| **arXiv ID** | [2602.19354](https://arxiv.org/abs/2602.19354) |
| **Authors** | Eun Jeong Kang, Fengyang Lin, Angel Hsing-Chi Hwang |
| **Date** | 2026-02-22 |
| **Category** | cs.HC |

**Abstract Summary**: Semi-structured interviews with 19 individual model creators examining challenges with marketplace regulation compliance. Identifies three regulatory needs: reducing downstream harms, recognizing contributions/originality, and securing model ownership. Finds creators repurpose RAI tools for self-protection and community norms shape responsibility more than formal policies.

**Key Contribution**: Qualitative evidence that marketplace governance must account for community dynamics, not just formal policies; identifies creator-side compliance friction.

**Relevance**: **HIGH** - Directly studies model marketplace governance from creator perspective; findings applicable to skill marketplace policy design.

---

## H. Reliability, Failure Recovery & Insurance

### H1. MAS-FIRE: Fault Injection and Reliability Evaluation for LLM-Based Multi-Agent Systems

| Field | Value |
|-------|-------|
| **arXiv ID** | [2602.19843](https://arxiv.org/abs/2602.19843) |
| **Authors** | Jin Jia, Zhiling Deng, Zhuangbin Chen, Yingqi Wang, Zibin Zheng |
| **Date** | 2026-02-23 |
| **Category** | cs.SE |

**Abstract Summary**: Defines a taxonomy of 15 MAS-specific fault types across intra-agent and inter-agent failures. Injects faults via prompt modification, response rewriting, and message routing manipulation. Discovers four-tier fault tolerance hierarchy: mechanism, rule, prompt, and reasoning. Finds stronger models don't uniformly improve robustness; iterative closed-loop designs neutralize 40% of faults causing catastrophic collapse in linear workflows.

**Key Contribution**: 15-fault taxonomy for MAS with four-tier fault tolerance hierarchy; empirical evidence that architecture topology matters more than model strength.

**Relevance**: **HIGH** - Fault taxonomy and tolerance tiers directly applicable to assessing skill marketplace reliability and designing resilient skill composition.

---

### H2. The Intervention Paradox: Accurate Failure Prediction Does Not Imply Effective Failure Prevention

| Field | Value |
|-------|-------|
| **arXiv ID** | [2602.03338](https://arxiv.org/abs/2602.03338) |
| **Authors** | Rakshith Vasudev, Melisa Russak, Dan Bikel, Waseem Alshikh |
| **Date** | 2026-02-03 |
| **Category** | cs.CL |

**Abstract Summary**: Demonstrates that a binary LLM critic with strong offline accuracy (AUROC 0.94) can cause 26 percentage point performance collapse. Identifies the disruption-recovery tradeoff: interventions may recover failing trajectories but also disrupt succeeding ones. Proposes a 50-task pre-deployment pilot test to estimate intervention benefit/harm.

**Key Contribution**: The "Intervention Paradox" - accurate failure detection can worsen outcomes; proposes pre-deployment safety assessment methodology.

**Relevance**: **MEDIUM-HIGH** - Critical insight for marketplace quality assurance: automated skill monitoring/intervention can backfire; informs marketplace SLA design.

---

### H3. ReliabilityBench: Evaluating LLM Agent Reliability Under Production-Like Stress

| Field | Value |
|-------|-------|
| **arXiv ID** | [2601.06112](https://arxiv.org/abs/2601.06112) |
| **Authors** | Aayush Gupta |
| **Date** | 2026-01-03 |
| **Category** | cs.AI |

**Abstract Summary**: Benchmark evaluating agent reliability across three dimensions: consistency under repeated execution (pass^k), robustness to semantic perturbations (epsilon), and fault tolerance under tool/API failures (lambda). Defines unified reliability surface R(k,epsilon,lambda). Evaluates across 1,280 episodes. Rate limiting is most damaging fault. ReAct more robust than Reflexion under stress.

**Key Contribution**: Unified reliability surface R(k,epsilon,lambda) for agent evaluation; chaos-engineering-style fault injection framework for production readiness.

**Relevance**: **HIGH** - Reliability surface framework directly applicable to marketplace skill certification and SLA enforcement.

---

### H4. MTTR-A: Measuring Cognitive Recovery Latency in Multi-Agent Systems

| Field | Value |
|-------|-------|
| **arXiv ID** | [2511.20663](https://arxiv.org/abs/2511.20663) |
| **Authors** | Barak Or |
| **Date** | 2025-11-08 (revised 2025-12-26, v5) |
| **Category** | cs.MA |

**Abstract Summary**: Introduces MTTR-A (Mean Time-to-Recovery for Agentic Systems), adapting classical dependability theory to agentic orchestration. Measures cognitive recovery latency - time to detect reasoning drift and restore coherent operation. Defines MTBF and normalized recovery ratio (NRR). Establishes theoretical bounds linking recovery latency to long-run cognitive uptime.

**Key Contribution**: Classical reliability engineering (MTTR/MTBF) adapted for cognitive agent failures; formal bounds on cognitive uptime.

**Relevance**: **HIGH** - MTTR-A metric directly applicable to marketplace SLA definition and skill reliability guarantees.

---

## Cross-Cutting Themes & Gaps

### Key Patterns Across R9 Papers

1. **The "Marketplace-as-Infrastructure" paradigm**: Multiple papers (GaaS, ASC, PRISM) converge on treating governance, security, and reliability as marketplace infrastructure layers rather than agent-internal properties.

2. **Trust model convergence on hybrid approaches**: Papers [2511.03434], [2507.07901], [2511.02841] independently arrive at hybrid trust architectures combining cryptographic proof, economic stake, and reputation signals - no single mechanism suffices.

3. **First-mover advantage bias in agent markets**: Magentic Marketplace [2510.25779] empirically demonstrates 10-30x speed-over-quality bias, suggesting marketplace design must actively counteract positional advantages.

4. **Execution-layer security as the new frontier**: Post-ClawHavoc papers [2603.10092, 2603.11853, 2603.05786] shift security focus from content filtering to execution-layer invariants, TEE-based verification, and runtime policy enforcement.

5. **Reliability metrics gap**: Classical SRE concepts (MTTR, MTBF, chaos engineering) are being adapted for agent systems [2511.20663, 2601.06112, 2602.19843], but no standard has emerged for marketplace-level reliability guarantees.

### Remaining Research Gaps

- **Marketplace pricing theory**: No paper provides formal pricing mechanisms for agent skills (auction design, dynamic pricing, bundling)
- **Skill versioning and migration**: TEA protocol begins to address this, but marketplace-scale version management is unexplored
- **Cross-marketplace portability**: No work on skill portability standards across competing marketplaces
- **Insurance/warranty mechanisms**: Despite the Intervention Paradox, no paper proposes formal insurance or warranty contracts for skill marketplace transactions
- **Regulatory compliance automation**: While GaaS exists, no paper maps specific regulatory requirements (EU AI Act, etc.) to skill marketplace obligations

---

## Summary Statistics

| Category | Count | Critical | High | Medium |
|----------|-------|----------|------|--------|
| Skill Ecosystem & Analysis | 2 | 0 | 2 | 0 |
| Agentic Economy & Economics | 4 | 2 | 2 | 0 |
| Orchestration & Composition | 3 | 0 | 1 | 2 |
| Trust, Reputation & Identity | 6 | 2 | 3 | 1 |
| A2A Protocol & Commerce | 4 | 1 | 3 | 0 |
| Security & Defense | 5 | 1 | 3 | 1 |
| Governance & Compliance | 3 | 1 | 2 | 0 |
| Reliability & Recovery | 4 | 0 | 3 | 1 |
| **Total** | **31** | **7** | **19** | **5** |

### Newly Catalogued arXiv IDs (for exclusion in R10)

```
2602.08004, 2603.10092, 2505.15799, 2509.01063, 2510.25779, 2501.10388,
2603.11445, 2506.12508, 2603.00774, 2509.04979, 2507.07901, 2511.02841,
2511.03434, 2603.02960, 2511.19930, 2507.19550, 2504.16902, 2509.24380,
2508.09159, 2603.05786, 2602.19514, 2603.09002, 2603.02983, 2603.11853,
2508.18765, 2601.02371, 2602.19354, 2602.19843, 2602.03338, 2601.06112,
2511.20663
```
