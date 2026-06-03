# AI Agent Skill Marketplaces - Round 9 GitHub Research Report

**Date:** 2026-03-15
**Round:** 9 of ongoing deep research
**Prior rounds:** R1-R8 catalogued 135+ repos
**Methodology:** 7 DuckDuckGo searches across targeted categories, with deep README scraping of top repos

---

## Executive Summary

Round 9 reveals a maturing ecosystem with **47 new unique repos** not previously catalogued. Key signals:

1. **DNS-based agent discovery is crystallizing** as the dominant discovery pattern, with GoDaddy, AWS, and independent projects converging on `_mcp` TXT records and Agent Name Services
2. **Block (Square) entered the marketplace** with `block/agent-skills`, bringing enterprise legitimacy and the Goose agent ecosystem
3. **Escrow-based agent economies** are emerging on-chain (Base, Solana, Stacks, Stellar) with USDC as the settlement layer
4. **Cross-platform portability** has become a first-class concern, with multiple tools translating SKILL.md across 14-17 agent formats
5. **Failure recovery** is evolving from simple retry logic to sophisticated vault-backed rollback with cryptographic receipts and regression learning
6. **A2A+MCP convergence** is accelerating, with bridge implementations, domain-specific A2A specs (hospitality), and a "knowledge layer" (Tessera) emerging between the protocols
7. **VS Code marketplace integration** via `formulahendry/vscode-agent-skills` signals IDE-native skill discovery

---

## Table of Contents

1. [Skill Marketplaces & Registries](#1-skill-marketplaces--registries)
2. [Agent Discovery & DNS](#2-agent-discovery--dns)
3. [Protocol Convergence (A2A/MCP)](#3-protocol-convergence-a2amcp)
4. [Cross-Platform Skill Portability](#4-cross-platform-skill-portability)
5. [Escrow & Agent Payments](#5-escrow--agent-payments)
6. [Failure Recovery & Rollback](#6-failure-recovery--rollback)
7. [Knowledge Transfer & Orchestration](#7-knowledge-transfer--orchestration)
8. [Signals & Notable Issues/Discussions](#8-signals--notable-issuesdiscussions)
9. [Ecosystem Trends](#9-ecosystem-trends)

---

## 1. Skill Marketplaces & Registries

### block/agent-skills
- **URL:** https://github.com/block/agent-skills
- **Description:** A marketplace for agent skills maintained by Block (formerly Square). Skills designed to be portable across Goose, Claude Desktop, and other agents supporting the Agent Skills standard. Includes CLI installer (`npx skills add`), web marketplace at block.github.io/goose/skills, and community contribution workflow.
- **Last Updated:** 2026-01-27
- **Key Technologies:** SKILL.md, npx CLI, Goose agent, skills validator CI
- **Significance:** **HIGH** - Major tech company entering the skill marketplace space. Block's Goose agent + marketplace creates a vertically integrated skill economy. The automated PR validator sets a quality bar for community contributions.

### tech-leads-club/agent-skills
- **URL:** https://github.com/tech-leads-club/agent-skills
- **Description:** "The secure, validated skill registry for professional AI coding agents." Claims that over 13% of marketplace skills contain security issues. Focuses on validated, security-audited skills.
- **Last Updated:** ~2 days ago (very active)
- **Key Technologies:** Security validation, skill auditing
- **Significance:** **HIGH** - First registry explicitly focused on security validation. The "13% contain issues" claim highlights a critical ecosystem problem.

### formulahendry/vscode-agent-skills
- **URL:** https://github.com/formulahendry/vscode-agent-skills
- **Description:** VS Code extension providing a full marketplace for discovering, installing, and managing Agent Skills. Features search, one-click install, rich markdown rendering, configurable sources (supports anthropics/skills, github/awesome-copilot, pytorch/pytorch, openai/skills repos). Install location configurable: `.github/skills`, `.claude/skills`, `~/.copilot/skills`.
- **Last Updated:** 2026-03-07
- **Key Technologies:** VS Code Extension API, GitHub Trees API, raw.githubusercontent.com, markdown-it
- **Significance:** **HIGH** - IDE-native skill marketplace is a major UX advancement. Published on VS Code Marketplace and Open VSX. Smart caching + lazy loading + parallel fetching shows production maturity. Supports multiple install locations for different agents.

### aiskillstore/marketplace
- **URL:** https://github.com/aiskillstore/marketplace
- **Description:** "AI Skillstore - Agent Skills Marketplace. The official AI Skills marketplace for Claude Code and Codex." Follows the Agent Skills specification.
- **Last Updated:** Recent
- **Key Technologies:** Agent Skills specification
- **Significance:** MEDIUM - Another marketplace entrant following the standard.

### Arephan/agentic-skills-marketplace
- **URL:** https://github.com/Arephan/agentic-skills-marketplace
- **Description:** "A central marketplace that taps into the 100k+ AI agent users looking for reusable capabilities. Inspired by the superpowers movement (+5,167 stars in 3 days). Lets creators build once and monetize infinitely."
- **Last Updated:** Recent
- **Key Technologies:** Monetization focus
- **Significance:** MEDIUM - Notable for the creator monetization angle.

### nibzard/skills-marketplace
- **URL:** https://github.com/nibzard/skills-marketplace
- **Description:** "The Skills Marketplace provides a centralized platform for distributing and discovering Agent Skills that extend Claude Code's capabilities."
- **Last Updated:** 2026-01-31
- **Key Technologies:** Claude Code integration
- **Significance:** MEDIUM - Claude Code-focused marketplace.

### agents-inc/skills
- **URL:** https://github.com/agents-inc/skills
- **Description:** "Curated skills and pre-built stacks installable via AgentsInc CLI. Structured content (YAML + markdown) with metadata for giving subagents domain-specific knowledge."
- **Last Updated:** Recent
- **Key Technologies:** YAML + markdown, AgentsInc CLI
- **Significance:** MEDIUM - Interesting "stacks" concept for bundling related skills.

### latestaiagents/agent-skills
- **URL:** https://github.com/latestaiagents/agent-skills
- **Description:** "67 professional skills + 7 full-featured plugins for AI coding agents. Organized by audience. Works with Claude Code, Claude Cowork, Cursor, Codex, Windsurf, and 35+ other AI agents."
- **Last Updated:** Recent
- **Key Technologies:** Multi-agent compatibility
- **Significance:** MEDIUM - Large skill collection with broad agent support.

### numman-ali/n-skills
- **URL:** https://github.com/numman-ali/n-skills
- **Description:** "n-skills is a curated marketplace. Install via openskills or use your agent's native installer."
- **Last Updated:** 2026-01-17
- **Key Technologies:** openskills CLI
- **Significance:** LOW-MEDIUM - Another CLI-based marketplace.

### shyamsridhar123/Skills-Registry-CLI
- **URL:** https://github.com/shyamsridhar123/Skills-Registry-CLI
- **Description:** "CLI tool for managing and registering AI agent skills. Enables discovery, versioning, and orchestration of modular agent capabilities."
- **Last Updated:** Recent
- **Key Technologies:** CLI, versioning, orchestration
- **Significance:** MEDIUM - Focuses on the registry + versioning problem.

### kai98k/agent-skills-registry
- **URL:** https://github.com/kai98k/agent-skills-registry
- **Description:** Skills registry with emphasis on consumers reviewing SKILL.md and scripts before production use. Recommends pinning specific versions and auditing skills.
- **Last Updated:** 2026-03-03
- **Key Technologies:** Version pinning, skill auditing
- **Significance:** MEDIUM - Security-conscious registry approach.

### gofastskill (FastSkill)
- **URL:** https://github.com/gofastskill
- **Description:** "Builds on Anthropic's standardized Skills format, adding registry services, semantic search, version management, and deployment tooling."
- **Last Updated:** 2026-03-04
- **Key Technologies:** Semantic search, version management, deployment tooling
- **Significance:** MEDIUM - Registry with semantic search is a differentiator.

---

## 2. Agent Discovery & DNS

### godaddy/ans-registry
- **URL:** https://github.com/godaddy/ans-registry
- **Description:** **Agent Name Service (ANS) Registry** based on the IETF draft (draft-narajala-ans-00). Production-ready registry for secure AI agent discovery and identity verification. Features FQDN-anchored identity, dual certificate model (public server + private identity certs), Merkle tree transparency log, PKI-based trust, and protocol-agnostic support (A2A, MCP, ACP). Solves the O(n^2) bilateral agreement scaling problem.
- **Last Updated:** 2025-11-19
- **Key Technologies:** X.509 PKI, Merkle trees, ACME DNS-01 validation, OpenAPI, REST
- **Significance:** **CRITICAL** - GoDaddy (a domain registrar) building agent DNS is strategically brilliant. IETF draft backing, cryptographic identity, transparency logs, and protocol-agnostic design make this potentially foundational infrastructure. The Registration Authority + Transparency Log + KMS architecture mirrors Certificate Authority infrastructure.

### mariothomas/mcp-dns-registry
- **URL:** https://github.com/mariothomas/mcp-dns-registry
- **Description:** DNS-based discovery for MCP using `_mcp` TXT records. Organisations publish a single DNS TXT record at `_mcp.yourdomain.com` pointing to their MCP registry. The registry IS itself an MCP server -- agents discover it using standard `tools/list` and `tools/call`. Deployable on AWS (CloudFront + Lambda@Edge + DynamoDB), with Cloudflare/Azure alternatives planned. Running live reference at mcp.mariothomas.com. Written by Mario Thomas (Head of Applied AI, AWS).
- **Last Updated:** 2026-02-25 (v1.4.1)
- **Key Technologies:** DNS TXT records, CloudFront, Lambda@Edge, DynamoDB Global Tables, JWT, JSON-RPC
- **Significance:** **CRITICAL** - Elegant "DNS as bootstrap" approach. The registry-as-MCP-server insight means zero new client behavior needed. The n+m vs n*m scaling argument is compelling. Live reference implementation + architecture paper (v1.4) with 6 revisions shows maturity. Author's AWS position adds credibility.

### zyndai/AgentDNS
- **URL:** https://github.com/zyndai/AgentDNS
- **Description:** Decentralized registry and discovery network for AI agents. Like DNS maps domains to IPs, AgentDNS maps natural-language queries to discoverable, verifiable AI agents across a federated P2P mesh. Features Ed25519 cryptographic identity, hybrid search (BM25 + semantic vectors), EigenTrust reputation, bloom filter routing, gossip propagation, and two-tier caching.
- **Last Updated:** 2026-03-03
- **Key Technologies:** Go, PostgreSQL, Redis, Ed25519, EigenTrust, BM25 + cosine similarity, gossip protocol, bloom filters, Docker Compose
- **Significance:** **HIGH** - Most technically sophisticated discovery system found. The decentralized P2P mesh with gossip, EigenTrust reputation, and hybrid semantic+keyword search is genuinely novel. The multi-signal ranking formula (text 30%, semantic 30%, trust 20%, freshness 10%, availability 10%) is well-thought-out.

### agentcommunity/agent-identity-discovery
- **URL:** https://github.com/agentcommunity/agent-identity-discovery
- **Description:** "Uses a single DNS TXT record to make any agent service -- whether it speaks MCP, A2A, or another protocol -- instantly discoverable. No more manual configuration."
- **Last Updated:** 2026-02-06
- **Key Technologies:** DNS TXT records, protocol-agnostic
- **Significance:** HIGH - Protocol-agnostic discovery via DNS.

### awslabs/a2a-agent-registry-on-aws
- **URL:** https://github.com/awslabs/a2a-agent-registry-on-aws
- **Description:** Scalable agent registry using A2A protocol AgentCards with semantic search. AWS serverless architecture (Lambda, S3 Vectors, Bedrock Titan embeddings). Includes Python SDK with retry logic and React Web UI with Cognito auth. Estimated cost: $22.65/month for 1M requests.
- **Last Updated:** 2026-03-06
- **Key Technologies:** AWS Lambda, S3 Vectors, Amazon Bedrock Titan embeddings, API Gateway, CDK, React + Cloudscape, Cognito
- **Significance:** **HIGH** - AWS official labs project. The semantic search via Bedrock embeddings + S3 Vectors is production-grade. Cost estimate ($22.65/mo for 1M requests) validates serverless economics. Python SDK + React UI = full-stack solution.

### kenhuangus/dns-for-agents
- **URL:** https://github.com/kenhuangus/dns-for-agents
- **Description:** "A secure registry and management API for multi-agent AI systems. Agents can register, renew, deactivate, and query their status, all with strong JSON Schema validation."
- **Last Updated:** Recent
- **Key Technologies:** JSON Schema, management API
- **Significance:** MEDIUM - Lifecycle management (register/renew/deactivate) adds operational maturity.

### zerocmd/acdp
- **URL:** https://github.com/zerocmd/acdp
- **Description:** Agent Communication & Discovery Protocol. Agents register with both DNS (SRV/TXT records) and a central registry. Agents discover each other through the registry and maintain peer lists.
- **Last Updated:** Recent
- **Key Technologies:** DNS SRV/TXT, central registry, peer lists
- **Significance:** MEDIUM - Dual DNS + registry approach is pragmatic.

### StevenJohnson998/agent-registry
- **URL:** https://github.com/StevenJohnson998/agent-registry
- **Description:** "An MCP-first 'DNS' for the Agentic Web. Enables orchestrators to dynamically discover, evaluate, and invoke specialized micro-agents based on semantic intent, verifiable reliability, and contextual performance."
- **Last Updated:** Recent
- **Key Technologies:** MCP-first, semantic intent matching
- **Significance:** MEDIUM - The "semantic intent" matching for discovery is interesting.

### AgentDNS/AgentDNS
- **URL:** https://github.com/AgentDNS/AgentDNS
- **Description:** "A root-domain naming and service discovery system designed for LLM Agents. Provides service registration, discovery, proxying, and management."
- **Last Updated:** Recent
- **Key Technologies:** Python, root-domain naming
- **Significance:** MEDIUM - Different approach: root-domain system rather than subdomain TXT records.

### Yann-Favin-Leveque/agent-discovery-protocol
- **URL:** https://github.com/Yann-Favin-Leveque/agent-discovery-protocol
- **Description:** "Services describe themselves at `/.well-known/agent`, agents discover them at runtime through a searchable registry, and a single gateway handles all communication."
- **Last Updated:** Recent
- **Key Technologies:** `.well-known/agent`, gateway pattern
- **Significance:** MEDIUM - The `.well-known/agent` convention mirrors `.well-known/openid-configuration` and could become standard.

---

## 3. Protocol Convergence (A2A/MCP)

### Killea/AgentChatBus
- **URL:** https://github.com/Killea/AgentChatBus
- **Description:** "An MCP project that supports multiple agents. Fully compatible with A2A protocol as a peer alongside MCP: MCP -- how agents connect to tools, A2A -- how agents communicate with each other."
- **Last Updated:** 2026-03-01
- **Key Technologies:** MCP, A2A protocol bridge
- **Significance:** HIGH - Practical A2A+MCP bridge implementation.

### incocreativedev/tessera-core
- **URL:** https://github.com/incocreativedev/tessera-core
- **Description:** An activation-based protocol for AI-to-AI knowledge transfer across architectures. Enables trained neural networks to transfer learned knowledge to untrained models across different architectures via a Universal Hub Space. "MCP connects models to tools, A2A coordinates agents, and Tessera lets them teach each other." Features Mode A transfer, TBF binary format, differential privacy, and drift metrics.
- **Last Updated:** 2026-02-21
- **Key Technologies:** PyTorch 2.0+, Universal Hub Space (2048-dim), Ed25519, TBF v1.1 binary format, InfoNCE, differential privacy
- **Significance:** **HIGH** - Genuinely novel "knowledge layer" concept. If MCP = tools and A2A = coordination, Tessera = knowledge transfer. Cross-architecture transfer validated across Transformer, MLP, Conv1D, and LSTM. The formal specification suite (6 documents) shows serious intent. Could enable skill knowledge to be transferred between agent architectures.

### A2A-hospitality/specs
- **URL:** https://github.com/A2A-hospitality/specs
- **Description:** Domain semantics for AI agent discovery and booking in hospitality. Defines venues, booking terms, trust, and lifecycle -- what agents need to understand and book places to eat, drink, stay, and play.
- **Last Updated:** Recent
- **Key Technologies:** A2A protocol, domain-specific semantics
- **Significance:** **HIGH** - First domain-specific A2A extension found. Hospitality as a vertical demonstrates A2A moving from protocol spec to industry application.

### Intelligent-Internet/CommonGround
- **URL:** https://github.com/Intelligent-Internet/CommonGround
- **Description:** "The Sociotechnical OS for Multi-Agent Collaboration." A protocol-first OS kernel (not a Python library) based on cybernetics. Features immutable CardBox ledger, worker-agnostic execution, dynamic topology (beyond rigid DAGs), "Humans Are Agents" philosophy, zero-brain-split physical law (Postgres + NATS). Planned A2A/ACP ingress support.
- **Last Updated:** 2026-02-16
- **Key Technologies:** Postgres (state truth), NATS JetStream (doorbell), Docker Compose, Gemini/OpenAI/Kimi, OTel + Jaeger, UTP protocol
- **Significance:** **HIGH** - Ambitious "OS for agents" concept with strong systems engineering. The L0 (protocol) / L1 (kernel) / L2 (ecosystem) layering is well-designed. "Humans Are Agents" as first-class protocol participants is philosophically interesting.

### elvinagam/a2a-mcp-agents-protocols
- **URL:** https://github.com/elvinagam/a2a-mcp-agents-protocols
- **Description:** "Demonstrates how autonomous agents can coordinate via A2A and invoke external services via MCP to build resilient, flexible, and interoperable ML workflows."
- **Last Updated:** Recent
- **Key Technologies:** A2A, MCP, ML workflows
- **Significance:** MEDIUM - Reference implementation for A2A+MCP integration.

### marimerllc/rockbot
- **URL:** https://github.com/marimerllc/rockbot
- **Description:** "Framework for building multi-agent AI systems where agents communicate exclusively through a message bus. No shared memory."
- **Last Updated:** Recent
- **Key Technologies:** Message bus architecture
- **Significance:** MEDIUM - Pure message-bus multi-agent framework.

---

## 4. Cross-Platform Skill Portability

### gotalab/skillport
- **URL:** https://github.com/gotalab/skillport
- **Description:** "Bring Agent Skills to Any AI Agent and Coding Agent -- via CLI or MCP. Manage once, serve anywhere." Features search-first loading (~100 tokens/skill metadata, full instructions on demand), validation against Agent Skills spec, metadata management, category/tag organization, and per-agent filtering. Works with Cursor, Copilot, Windsurf, Cline, Codex.
- **Last Updated:** 2025-12-01
- **Key Technologies:** Python (uv), MCP server, CLI, Agent Skills specification
- **Significance:** **HIGH** - The search-first loading pattern (inspired by Anthropic's Tool Search Tool) is elegant for scaling to 50+ skills. Dual-mode (MCP + CLI) delivery ensures broad compatibility. Published on PyPI.

### FrancyJGLisboa/agent-skill-creator
- **URL:** https://github.com/FrancyJGLisboa/agent-skill-creator
- **Description:** "Turn any skill into a cross-platform installer. Auto-detects all 14 supported tools, generates format adapters for Cursor (.mdc) and Windsurf (.md rules) automatically, creates universal ~/.agents/skills/ symlink."
- **Last Updated:** Recent
- **Key Technologies:** Shell scripting, format adapters, symlinks
- **Significance:** HIGH - Solves the practical N-format problem with auto-detection and adapter generation.

### BenedictKing/skill-master
- **URL:** https://github.com/BenedictKing/skill-master
- **Description:** "Cross-platform skill package manager for AI coding agents, fully compatible with npx skills CLI."
- **Last Updated:** Recent
- **Key Technologies:** npx, package management
- **Significance:** MEDIUM - Package manager approach to skill distribution.

### xdemocle/stackformers-agent-skills
- **URL:** https://github.com/xdemocle/stackformers-agent-skills
- **Description:** "The same SKILL.md works across any platform that supports the Agent Skills standard. How skills are loaded depends on the platform."
- **Last Updated:** Recent
- **Key Technologies:** Agent Skills standard
- **Significance:** MEDIUM - Cross-platform collection.

### mystilleef/llm-agent-skills
- **URL:** https://github.com/mystilleef/llm-agent-skills
- **Description:** "Skills offer cross-platform, portable, reusable, flexible, token-efficient, context-preserving, and composable functionality. Use commands as proxies to launch orchestration skills."
- **Last Updated:** 2026-01-19
- **Key Technologies:** Command-proxy pattern
- **Significance:** MEDIUM - The command-proxy pattern for skill invocation is interesting.

### shinpr/sub-agents-skills
- **URL:** https://github.com/shinpr/sub-agents-skills
- **Description:** "Cross-LLM sub-agent orchestration as an Agent Skill. Route tasks to Codex, Claude Code, Cursor, or Gemini from any compatible tool."
- **Last Updated:** Recent
- **Key Technologies:** Multi-LLM routing
- **Significance:** MEDIUM - Skill that orchestrates across different LLM backends.

### osolmaz/skillflag
- **URL:** https://github.com/osolmaz/skillflag
- **Description:** "A simple CLI flag convention for listing and installing agent skills. Bundle and publish your tool's skill directly with your package."
- **Last Updated:** 2026-01-11
- **Key Technologies:** CLI convention, `--skill` flag
- **Significance:** MEDIUM - Proposes a universal CLI flag convention for skill discovery.

### ionclaw-org/ionclaw
- **URL:** https://github.com/ionclaw-org/ionclaw
- **Description:** "A cross-platform AI agent orchestrator in C++ that turns any device -- including your phone -- into a self-contained, multi-agent automation system."
- **Last Updated:** ~6 days ago
- **Key Technologies:** C++, cross-platform (including mobile)
- **Significance:** MEDIUM - C++ agent orchestrator targeting edge/mobile is unique.

### neovateai/agent-skill-npm-boilerplate
- **URL:** https://github.com/neovateai/agent-skill-npm-boilerplate
- **Description:** Boilerplate for publishing agent skills as npm packages with scoped registry support.
- **Last Updated:** Recent
- **Key Technologies:** npm, scoped packages
- **Significance:** LOW-MEDIUM - Template for npm-based skill distribution.

---

## 5. Escrow & Agent Payments

### JrPribs/agent-marketplace
- **URL:** https://github.com/JrPribs/agent-marketplace
- **Description:** Decentralized marketplace where AI agents list, purchase, and fulfill skills/services using USDC. Features reputation staking (higher stake = more trust), escrow with staged release (50% preview / 50% final), auto-release after 48h verification window, dispute resolution with evidence submission, and multi-agent collaborative project splitting with auto-distributed payment.
- **Last Updated:** 2026-02-04
- **Key Technologies:** Base (Coinbase L2), USDC, Solidity + Foundry, Next.js + wagmi + RainbowKit, The Graph
- **Significance:** **HIGH** - Most complete agent economy design found. The two-way trust model (agents AND buyers stake), staged escrow, and collaborative revenue splits address real marketplace dynamics. Built for OpenClaw USDC Hackathon 2026.

### Essie9/skill-marketplace
- **URL:** https://github.com/Essie9/skill-marketplace
- **Description:** "Smart contract creating a trustless freelance platform on the Stacks blockchain. Service providers offer skills, clients hire with confidence through automated escrow, both parties build verifiable on-chain reputation."
- **Last Updated:** Recent
- **Key Technologies:** Stacks blockchain, Clarity smart contracts
- **Significance:** MEDIUM - Stacks/Clarity ecosystem alternative.

### blessrow44/skillmarketplace
- **URL:** https://github.com/blessrow44/skillmarketplace
- **Description:** "Direct peer-to-peer job agreements with built-in escrow, milestone-based payments, dispute resolution, and reputation tracking -- all without intermediaries."
- **Last Updated:** Recent
- **Key Technologies:** Smart contracts, P2P
- **Significance:** MEDIUM - P2P focus with milestone-based payments.

### letiuhai/skill-marketplace
- **URL:** https://github.com/letiuhai/skill-marketplace
- **Description:** "Decentralized marketplace on Celo where users can list skills as NFTs, book services from others, with built-in escrow protection and reputation tracking."
- **Last Updated:** Recent
- **Key Technologies:** Celo blockchain, NFTs
- **Significance:** MEDIUM - Skills-as-NFTs is an interesting tokenization approach.

### PayAINetwork/plugin-payai
- **URL:** https://github.com/PayAINetwork/plugin-payai
- **Description:** "Eliza plugin for the PayAI marketplace. PayAI is a marketplace that allows agent creators to monetize their agents!"
- **Last Updated:** Recent
- **Key Technologies:** Eliza framework, PayAI marketplace
- **Significance:** MEDIUM - Agent monetization via Eliza plugin ecosystem.

### Alman8904/Skill-Marketplace-Reputation-Based-Freelancing
- **URL:** https://github.com/Alman8904/Skill-Marketplace-Reputation-Based-Freelancing
- **Description:** "Consumers hire providers for specific skills, payments held in escrow until work approved, every user builds a public trust profile automatically from order history."
- **Last Updated:** Recent
- **Key Technologies:** Smart contracts, reputation scoring
- **Significance:** LOW-MEDIUM - Reputation-first approach.

---

## 6. Failure Recovery & Rollback

### sene1337/clawback
- **URL:** https://github.com/sene1337/clawback
- **Description:** Git checkpoint, runtime-state recovery, and regression tracking for OpenClaw agents. Three linked mechanisms: (1) checkpoint before destructive ops, (2) mandatory regression logging on rollback (what broke, why, what principle violated), (3) dual-surface git model (workspace repo + local ops-state). Tracks self-caught (green) vs human-caught (red) failures as a learning metric.
- **Last Updated:** 2026-02-14
- **Key Technologies:** Bash + Git, dual-surface git model, regression log format
- **Significance:** **HIGH** - The "failure as learning" philosophy is genuinely novel. Mechanically enforced regression logging (can't skip on rollback) creates an institutional memory that survives context compaction. The green/red ratio as an agent learning metric is brilliant. References StructMemEval (Yandex Research) for empirical backing.

### SeanFDZ/agent-gate
- **URL:** https://github.com/SeanFDZ/agent-gate
- **Description:** Execution authority layer for AI agents with vault-backed rollback and policy enforcement. Sits between agent's proposed tool calls and execution. Features: pre-computed risk classification, directory envelope enforcement, agent-unreachable vault for backups, rate limiting with circuit breakers, identity binding (AARM R6 levels), parameter modification (e.g., chmod 777 -> chmod 755), OPA policy backend support.
- **Last Updated:** 2026-02-23
- **Key Technologies:** Python, YAML/Rego policies, OPA, Ed25519 (vault), AARM R6 identity model, circuit breakers
- **Significance:** **HIGH** - Most sophisticated agent execution control system found. The key insight: "make every action safe to allow" rather than blocking destructive actions. Vault outside agent's envelope, cryptographic audit chains, identity binding at 4 AARM levels, and OPA integration for enterprise policy composition. The "inspect the action, not the reasoning" principle is sound.

### agentralabs/agentic-workflow
- **URL:** https://github.com/agentralabs/agentic-workflow
- **Description:** Universal orchestration engine for AI agents. 24 capabilities across 6 categories, 124 MCP tools, .awf binary format. Rust core. Features failure-classified retry (different strategies per error type), per-step rollback with cryptographic receipts, circuit breaker intelligence, dead letter processing, approval gates with escalation chains, and natural language workflow creation.
- **Last Updated:** 2026-03-14
- **Key Technologies:** Rust, MCP, .awf binary format, DAG/FSM/batch/stream processing
- **Significance:** **HIGH** - Ambitious "Airflow+Temporal+GitHub Actions replacement" for agents. The per-step rollback with cryptographic receipts and failure-classified retry go beyond any existing orchestration tool. Performance benchmarks (<50ms for 1,000-step DAG validation) validate the Rust choice. Zero infrastructure requirement (single .awf binary) is a strong differentiator.

### LinkedInLearning/operating-AI-agents-failure-and-recovery-8020004
- **URL:** https://github.com/LinkedInLearning/operating-AI-agents-failure-and-recovery-8020004
- **Description:** LinkedIn Learning course materials on implementing rollback mechanisms, building automated recovery workflows, and creating agent health/status reports.
- **Last Updated:** 2026-01-30
- **Key Technologies:** GitHub Codespaces, educational
- **Significance:** MEDIUM - LinkedIn Learning creating courses on agent failure recovery signals mainstream adoption of the pattern.

### RobertGumeny/agent-orchestrator
- **URL:** https://github.com/RobertGumeny/agent-orchestrator
- **Description:** "A stateful bash orchestrator with intelligent failure recovery: automatic retry with rollback on failures, bug interruption system (discovers bugs during feature work, pauses to fix them, then resumes)."
- **Last Updated:** Recent
- **Key Technologies:** Bash, stateful orchestration
- **Significance:** MEDIUM - The bug interruption system (pause feature work -> fix bug -> resume) is a practical pattern.

### blakeox/llm-skills
- **URL:** https://github.com/blakeox/llm-skills
- **Description:** Specialized agent skills including: reliability.agent.md (observability, retries, failure handling, recovery), migration.agent.md (staged rollout, schema/data transition, rollback).
- **Last Updated:** Recent
- **Key Technologies:** Agent skills as .agent.md files
- **Significance:** LOW-MEDIUM - Reliability and migration as dedicated agent specializations.

---

## 7. Knowledge Transfer & Orchestration

### microsoft/skills
- **URL:** https://github.com/microsoft/skills
- **Description:** "Skills, MCP servers, Custom Agents, Agents.md for SDKs." Official Microsoft collection. Coding agents like Copilot CLI and GitHub Copilot in VS Code lack domain knowledge about your SDKs -- skills provide the activation context.
- **Last Updated:** ~2 days ago (very active)
- **Key Technologies:** MCP servers, Agents.md, SDK patterns
- **Significance:** HIGH - Microsoft's official skill collection. The "activation context" framing (skills surface patterns already in model weights) is important.

### refly-ai/refly
- **URL:** https://github.com/refly-ai/refly
- **Description:** "The first open-source agent skills builder. Define skills with governance and reliability infrastructure for deploying AI across the entire organization."
- **Last Updated:** Recent
- **Key Technologies:** Agent skills builder, enterprise governance
- **Significance:** MEDIUM - Enterprise-focused skill builder with governance.

### hashicorp/agent-skills
- **URL:** https://github.com/hashicorp/agent-skills
- **Description:** "A collection of Agent skills and Claude Code plugins for HashiCorp products: Terraform (HCL, modules, providers), Vault, Consul, Nomad."
- **Last Updated:** Recent
- **Key Technologies:** Terraform, Vault, Consul, Nomad
- **Significance:** MEDIUM - HashiCorp creating official agent skills validates the pattern for infrastructure tooling.

### callstackincubator/agent-skills
- **URL:** https://github.com/callstackincubator/agent-skills
- **Description:** "A collection of agent-optimized React Native skills for AI coding assistants."
- **Last Updated:** Recent
- **Key Technologies:** React Native
- **Significance:** LOW-MEDIUM - Domain-specific (React Native) skill collection.

### agentskills/agentskills
- **URL:** https://github.com/agentskills/agentskills
- **Description:** "Specification and documentation for Agent Skills. A simple, open format for giving agents new capabilities and expertise. Write once, use everywhere."
- **Last Updated:** Recent
- **Key Technologies:** Specification standard
- **Significance:** MEDIUM - The specification itself as a separate repo/org.

---

## 8. Signals & Notable Issues/Discussions

### vercel-labs/agent-skills (Issue #20)
- **URL:** https://github.com/vercel-labs/agent-skills/issues/20
- **Description:** "[RFC] Versioning and Claude Code Marketplace Compatibility" - Proposes versioning mechanism for skills and `/plugin install` support for Claude Code.
- **Significance:** Vercel engaging with skill versioning signals enterprise interest.

### mlflow/mlflow (Issue #21255)
- **URL:** https://github.com/mlflow/mlflow/issues/21255
- **Description:** "[FR] Support Agent Skills (SKILL.md) as reusable evaluation criteria" - Proposes registering skills in MLflow's tracking store for team-wide sharing and versioning.
- **Significance:** MLflow integration would bring skills into the ML experiment tracking ecosystem.

### anthropics/claude-agent-sdk-python (Issue #653)
- **URL:** https://github.com/anthropics/claude-agent-sdk-python/issues/653
- **Description:** "What We'd Love to See" - Community requesting A2A task card support, agent discovery, and message format in the Claude Agent SDK.
- **Significance:** Community pressure for A2A support in official Anthropic SDK.

### a2aproject/A2A (Issue #1295)
- **URL:** https://github.com/a2aproject/A2A/issues/1295
- **Description:** "[Proposal]: New Repo: a2a-registry" - Formal proposal for an official A2A registry where agents ask "Where is an active endpoint that handles 'flight booking' and speaks A2A v1?"
- **Significance:** Official A2A project considering a centralized registry.

### openclaw/openclaw (Issue #17700)
- **URL:** https://github.com/openclaw/openclaw/issues/17700
- **Description:** "feat: atomic config management with validation and crash-loop rollback" - Agents writing bad configs that crash gateways with no automated recovery.
- **Significance:** Real-world failure mode driving rollback feature development.

### openclaw/openclaw (Discussion #21064)
- **URL:** https://github.com/openclaw/openclaw/discussions/21064
- **Description:** "trust-escrow skill -- escrow for agent-to-agent task payments" - SKILL.md published for smart contract + npm package handling USDC escrow for agent-to-agent tasks.
- **Significance:** Escrow as an installable agent skill is a powerful pattern.

### openclaw/openclaw (PR #9186)
- **URL:** https://github.com/openclaw/openclaw/pull/9186
- **Description:** "Add MoltBazaar skill - AI Agent Job Marketplace" - Humans post tasks, AI agents compete to complete them, payments via USDC escrow.
- **Significance:** Human-to-agent job marketplace emerging within skill ecosystems.

### anomalyco/opencode (Issue #8386)
- **URL:** https://github.com/anomalyco/opencode/issues/8386
- **Description:** "Skill Registry + Installer for Awesome-Claude-Skills" - Proposes registry metadata including skill name, description, category tags, license info, version info (tag or commit SHA).
- **Significance:** Metadata standardization discussion.

### nibzard/awesome-agentic-patterns
- **URL:** https://github.com/nibzard/awesome-agentic-patterns/blob/main/patterns/canary-rollout-and-automatic-rollback-for-agent-policy-changes.md
- **Description:** "Canary Rollout and Automatic Rollback for Agent Policy Changes" - Treat agent policy changes like production releases: ship to small traffic slice, monitor, auto-rollback.
- **Significance:** DevOps patterns (canary releases) being applied to agent policy management.

---

## 9. Ecosystem Trends

### Trend 1: DNS as the Discovery Layer
Three independent approaches are converging:
- **`_mcp` TXT records** (mariothomas/mcp-dns-registry) - Simple, MCP-native
- **Agent Name Service** (godaddy/ans-registry) - IETF-backed, PKI-heavy
- **Decentralized P2P** (zyndai/AgentDNS) - Federated mesh with gossip

All solve the n*m -> n+m scaling problem differently. The `_mcp` TXT record approach has the lowest barrier to entry; ANS has the strongest trust model; AgentDNS has the best search capabilities.

### Trend 2: Security as a First-Class Concern
- tech-leads-club/agent-skills claims 13% of marketplace skills have security issues
- kai98k/agent-skills-registry recommends version pinning and auditing
- SeanFDZ/agent-gate provides vault-backed execution control
- Agent Gate's "inspect the action, not the reasoning" principle separates content safety from execution safety

### Trend 3: The Agent Economy Stack is Forming
Clear layering emerging:
1. **Discovery:** DNS/registry (godaddy, mariothomas, awslabs)
2. **Trust:** Cryptographic identity + reputation (ANS, EigenTrust, staking)
3. **Negotiation:** Scope agreements + pricing (JrPribs/agent-marketplace)
4. **Payment:** USDC escrow with staged release (Base, Solana, Stacks)
5. **Dispute:** Evidence-based arbitration (JrPribs/agent-marketplace)

### Trend 4: IDE-Native Skill Discovery
formulahendry/vscode-agent-skills brings the marketplace INTO the developer's primary tool. This mirrors how VS Code extensions work but for agent capabilities.

### Trend 5: Failure Recovery Becoming Sophisticated
Evolution from simple retry -> classified retry -> vault-backed rollback -> regression learning:
- agentralabs/agentic-workflow: failure-classified retry with cryptographic receipts
- sene1337/clawback: mandatory regression logging with learning metrics
- SeanFDZ/agent-gate: pre-computed policy with vault isolation

### Trend 6: "Knowledge Layer" Emergence
incocreativedev/tessera-core proposes a third protocol layer:
- MCP = tools (model-to-tool)
- A2A = coordination (agent-to-agent)
- Tessera = knowledge transfer (model-to-model)

If validated, this could enable skills to be "taught" between architectures rather than just described in SKILL.md.

### Trend 7: Domain-Specific A2A Extensions
A2A-hospitality/specs is the first domain vertical built on A2A. Expect more verticals (healthcare, finance, logistics) as the protocol matures.

### Trend 8: Major Companies Entering
New corporate entrants in R9:
- **Block** (agent-skills marketplace + Goose)
- **GoDaddy** (ANS Registry, IETF draft)
- **AWS Labs** (A2A Agent Registry)
- **Microsoft** (official skills repo)
- **HashiCorp** (infrastructure agent skills)
- **LinkedIn Learning** (agent recovery courses)

---

## Appendix: Complete New Repo Index

| # | Repo | Category | Significance |
|---|------|----------|-------------|
| 1 | block/agent-skills | Marketplace | HIGH |
| 2 | tech-leads-club/agent-skills | Registry/Security | HIGH |
| 3 | formulahendry/vscode-agent-skills | IDE Marketplace | HIGH |
| 4 | godaddy/ans-registry | Discovery/DNS | CRITICAL |
| 5 | mariothomas/mcp-dns-registry | Discovery/DNS | CRITICAL |
| 6 | zyndai/AgentDNS | Discovery/DNS | HIGH |
| 7 | awslabs/a2a-agent-registry-on-aws | Discovery/Registry | HIGH |
| 8 | agentcommunity/agent-identity-discovery | Discovery/DNS | HIGH |
| 9 | Killea/AgentChatBus | Protocol/A2A+MCP | HIGH |
| 10 | incocreativedev/tessera-core | Knowledge Transfer | HIGH |
| 11 | A2A-hospitality/specs | Protocol/Domain A2A | HIGH |
| 12 | Intelligent-Internet/CommonGround | Orchestration/OS | HIGH |
| 13 | gotalab/skillport | Portability | HIGH |
| 14 | FrancyJGLisboa/agent-skill-creator | Portability | HIGH |
| 15 | JrPribs/agent-marketplace | Escrow/Payments | HIGH |
| 16 | sene1337/clawback | Recovery/Rollback | HIGH |
| 17 | SeanFDZ/agent-gate | Recovery/Execution | HIGH |
| 18 | agentralabs/agentic-workflow | Orchestration | HIGH |
| 19 | microsoft/skills | Skills Collection | HIGH |
| 20 | aiskillstore/marketplace | Marketplace | MEDIUM |
| 21 | Arephan/agentic-skills-marketplace | Marketplace | MEDIUM |
| 22 | nibzard/skills-marketplace | Marketplace | MEDIUM |
| 23 | agents-inc/skills | Marketplace | MEDIUM |
| 24 | latestaiagents/agent-skills | Skills Collection | MEDIUM |
| 25 | numman-ali/n-skills | Marketplace | MEDIUM |
| 26 | shyamsridhar123/Skills-Registry-CLI | Registry | MEDIUM |
| 27 | kai98k/agent-skills-registry | Registry/Security | MEDIUM |
| 28 | gofastskill (org) | Registry | MEDIUM |
| 29 | kenhuangus/dns-for-agents | Discovery | MEDIUM |
| 30 | zerocmd/acdp | Discovery | MEDIUM |
| 31 | StevenJohnson998/agent-registry | Discovery | MEDIUM |
| 32 | AgentDNS/AgentDNS | Discovery | MEDIUM |
| 33 | Yann-Favin-Leveque/agent-discovery-protocol | Discovery | MEDIUM |
| 34 | elvinagam/a2a-mcp-agents-protocols | Protocol | MEDIUM |
| 35 | marimerllc/rockbot | Orchestration | MEDIUM |
| 36 | BenedictKing/skill-master | Portability | MEDIUM |
| 37 | xdemocle/stackformers-agent-skills | Portability | MEDIUM |
| 38 | mystilleef/llm-agent-skills | Portability | MEDIUM |
| 39 | shinpr/sub-agents-skills | Portability | MEDIUM |
| 40 | osolmaz/skillflag | Portability | MEDIUM |
| 41 | ionclaw-org/ionclaw | Portability/Edge | MEDIUM |
| 42 | Essie9/skill-marketplace | Escrow | MEDIUM |
| 43 | blessrow44/skillmarketplace | Escrow | MEDIUM |
| 44 | letiuhai/skill-marketplace | Escrow/NFT | MEDIUM |
| 45 | PayAINetwork/plugin-payai | Payments | MEDIUM |
| 46 | refly-ai/refly | Skills Builder | MEDIUM |
| 47 | hashicorp/agent-skills | Skills Collection | MEDIUM |

---

*Report generated as part of Round 9 deep research on AI agent skill marketplaces.*
*47 new repos identified. 14 scraped in depth. 8 ecosystem trends documented.*
