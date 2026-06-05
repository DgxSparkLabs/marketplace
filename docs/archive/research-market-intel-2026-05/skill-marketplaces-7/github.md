# Skill Marketplaces Research - Round 7: GitHub Repository Survey

**Date:** 2025-07-14  
**Focus Areas:** Testing/QA Frameworks, Pricing/Billing, Skill Composition/Orchestration, Governance/Compliance, A2A Protocol Ecosystem  
**Searches Run:** 15+ queries across agent marketplaces, tool registries, orchestration, governance, A2A protocol, MCP marketplaces, and workflow composition  

---

## Executive Summary

Round 7 reveals a **dramatic acceleration** in the agent marketplace space, with three clear mega-trends:

1. **Microsoft enters the arena** — `microsoft/multi-agent-marketplace` (Magentic Marketplace) brings academic rigor to marketplace simulation with 147 stars in its first months
2. **A2A Protocol explosion** — Google's Agent-to-Agent protocol has spawned 30+ implementations across every major language (Rust, Go, Python, TypeScript, PHP, Nim, Common Lisp)
3. **Cryptographic trust + agent economics** — Multiple projects now combine audit trails, reputation systems, and micropayments into integrated trust layers

The most significant finding is the emergence of **five architectural layers** that any serious skill marketplace must address: Discovery, Trust/Validation, Payments, Orchestration, and Governance. No single project covers all five, but the puzzle pieces are falling into place.

---

## Table of Contents

1. [Tier 1: High-Signal Repos (Deep Dives)](#tier-1-high-signal-repos)
2. [Tier 2: Notable Repos](#tier-2-notable-repos)
3. [Tier 3: Emerging / Niche](#tier-3-emerging--niche)
4. [A2A Protocol Ecosystem](#a2a-protocol-ecosystem)
5. [Thematic Analysis](#thematic-analysis)
6. [Architecture Patterns](#architecture-patterns)
7. [Implications for Our Marketplace](#implications-for-our-marketplace)

---

## Tier 1: High-Signal Repos (Deep Dives)

### 1. microsoft/multi-agent-marketplace (Magentic Marketplace)

| Field | Value |
|-------|-------|
| **URL** | https://github.com/microsoft/multi-agent-marketplace |
| **Stars** | 147 |
| **Forks** | 33 |
| **Language** | Python |
| **License** | MIT |
| **Updated** | Today (actively maintained) |
| **Paper** | [arXiv:2510.25779](https://arxiv.org/abs/2510.25779) |

**What it does:** A Python framework for **simulating AI-powered two-sided markets**. Configure LLM-based buyer and seller agents, run marketplace simulations, and measure economic outcomes (welfare, fairness, efficiency).

**Why it matters:**
- **Microsoft Research backing** — Multi-author team including Eric Horvitz, published at academic venues
- **Model comparison** — Compare how different LLMs (OpenAI, Claude, Gemini, local models) perform as marketplace agents
- **Economic rigor** — Measures welfare outcomes, identifies biases, tests manipulation resistance
- **Extensible** — Adaptable beyond restaurants/contractors to any two-sided market

**Architecture:**
- CLI-driven: `magentic-marketplace run data/mexican_3_9 --experiment-name test_exp`
- Analysis pipeline: `magentic-marketplace analyze test_exp`
- Docker Compose for database
- `uv` for dependency management

**Key Insight:** This is the first **simulation framework** for agent marketplaces. Instead of building a marketplace, it lets you test marketplace *designs* before deploying them. Critical for understanding pricing dynamics, agent manipulation vectors, and welfare optimization.

---

### 2. ertugrulakben/HYRVE-AI

| Field | Value |
|-------|-------|
| **URL** | https://github.com/ertugrulakben/HYRVE-AI |
| **Stars** | 9 |
| **Language** | — (docs-focused) |
| **License** | MIT |
| **Updated** | Today |

**What it does:** "The First AI Agent Marketplace" where agents are **economic citizens** — they earn income, build reputation, transact with humans AND other agents, and get paid in fiat (Stripe) or crypto (USDT).

**Why it matters — BILLING/PRICING MODEL:**
- **85/15 commission split** — Agent developers keep 85%, platform takes 15%
- **48-hour escrow** — Secure payment protection with customer review period
- **Dual payment rails** — Stripe (USD/EUR) + USDT (TRC-20, ERC-20)
- **Agent-to-Agent trading** — Agents can hire other agents
- **Self-registration via SKILL.md** — Agents read `https://www.hyrveai.com/skill.md` and register themselves
- **3-layer sandbox** — Isolated execution environment for security

**Pricing Examples:**
- Content writing: $2 per 500 words (~$300/month projected)
- Data entry: $0.05 per file (~$350/month)
- SEO audits: $20 per report (~$600/month)

**CashClaw Middleware:** Open-source npm package that transforms any AI agent into an "autonomous freelance business engine" with 7 business skills, Stripe integration, earnings dashboard, and HYRVE marketplace bridge.

**Key Insight:** The SKILL.md self-registration pattern and the CashClaw middleware layer represent a **novel onboarding architecture** — agents discover the marketplace, read structured instructions, and register themselves without human intervention.

---

### 3. bkauto3/Conduit + SwarmSync.ai

| Field | Value |
|-------|-------|
| **URL** | https://github.com/bkauto3/Conduit |
| **Stars** | 2 |
| **Language** | Python |
| **License** | Other |
| **Updated** | 1 day ago |

**What it does:** The only headless browser with a **cryptographic audit layer**. Every action is written to a tamper-evident SHA-256 hash chain, signed with Ed25519 identity keys. Powers the SwarmSync.ai agent marketplace (420+ agents).

**Why it matters — GOVERNANCE/AUDIT:**
- **SHA-256 hash-chained audit log** — Every click, navigation, JS execution is chained
- **Ed25519 signed session proofs** — Self-verifiable proof bundles with zero dependencies
- **JavaScript source stored in chain** — Not just results, but the actual code that ran
- **Billing ledger + cost enforcement** — Budget limits for agent actions
- **Compliance mapping** — SOC 2 (CC7.2, CC6.1), GDPR, HIPAA, SOX audit trails
- **MCP server integration** — Works as browser engine for Claude Code agents

**Proof Bundle Structure:**
```
session_proof/
├── audit_log.jsonl      # Full hash-chained log
├── manifest.json        # Session metadata + final chain hash
├── public_key.pem       # Ed25519 public key
├── session_sig.txt      # Signature over final chain hash
└── verify.py            # Self-contained verifier (stdlib only)
```

**SwarmSync.ai Connection:** Conduit proof bundles serve as the **trust layer** for agent-to-agent transactions. When Agent A hires Agent B for web research, the proof bundle proves the work was done. SwarmSync is where 420+ agents negotiate, execute, and get paid.

**Key Insight:** This is the strongest implementation of **verifiable agent execution** we have seen. The pattern of cryptographic proof bundles as a trust layer for marketplace transactions is directly applicable to skill marketplace quality assurance.

---

### 4. ucsandman/AI-Agent-Governance-Compliance-Kit

| Field | Value |
|-------|-------|
| **URL** | https://github.com/ucsandman/AI-Agent-Governance-Compliance-Kit |
| **Stars** | 1 |
| **Language** | JavaScript |
| **Updated** | 2 days ago |

**What it does:** Maps agent guardrail policies to regulatory frameworks and generates audit-ready compliance reports.

**Why it matters — GOVERNANCE:**
- **Framework coverage:** SOC 2, ISO 27001, GDPR, NIST AI RMF, Singapore IMDA (Agentic AI Framework, January 2026)
- **Policy to Control mapping** — Matches guardrail YAML to specific regulatory controls
- **Gap analysis** — Identifies which controls are covered, partial, or missing
- **Evidence integration** — Pulls real guard decision data from DashClaw for evidence
- **Report generation** — Markdown/JSON/PDF compliance reports with coverage matrices

**Example Output:**
```
## Summary
- Controls Covered: 8/12 (67%)
- Controls with Gaps: 4
- Risk Level: MEDIUM

### CC6.1 — Logical Access Security COVERED
Policies: all_exec_commands_blocked, destructive_operations_blocked
Evidence: 142 guard decisions enforced in last 30 days, 0 bypasses
```

**Key Insight:** First open-source project mapping **agent guardrails directly to enterprise compliance frameworks**. The DashClaw integration pattern (pulling real enforcement data as evidence) is crucial for any marketplace needing to demonstrate compliance.

---

### 5. capiscio/capiscio-node + capiscio-sdk-python

| Field | Value |
|-------|-------|
| **URL (CLI)** | https://github.com/capiscio/capiscio-node |
| **URL (SDK)** | https://github.com/capiscio/capiscio-sdk-python |
| **Stars** | 4 + 1 |
| **Language** | Go core, Node.js + Python wrappers |
| **License** | Apache-2.0 |

**What it does:** An **A2A validation platform** — validates agent cards for cryptographic trust, schema compliance, and live endpoint functionality. The Python SDK provides runtime security middleware for agent interactions.

**Why it matters — TESTING/TRUST:**
- **Agent Card Validation** — Schema compliance, cryptographic trust, live endpoint checks
- **Badge System** — Self-signed (dev) and verified badges with Ed25519
- **Multi-dimensional Scoring:**
  - Compliance Score (0-100): core fields, skills quality, format compliance, data quality
  - Trust Score (0-100): signatures, provider, security, documentation
- **Runtime Security Middleware** — Always-on validation, signature verification, rate limiting
- **Zero-config identity** — Auto-generates Ed25519 keys and `agent-card.json` on first run
- **Replay protection** — 60-second token expiration, SHA-256 body hash verification
- **<1ms overhead** — Performance telemetry via Server-Timing headers

**FastAPI Integration (3 lines):**
```python
guard = SimpleGuard(dev_mode=True)
app = FastAPI()
app.add_middleware(CapiscioMiddleware, guard=guard)
```

**Key Insight:** CapiscIO represents the most mature **agent trust infrastructure** — combining validation, scoring, badges, and runtime enforcement. The compliance + trust dual scoring system is directly applicable to skill marketplace quality tiers.

---

### 6. GenseeAI/cognify

| Field | Value |
|-------|-------|
| **URL** | https://github.com/GenseeAI/cognify |
| **Stars** | 273 |
| **Forks** | 30 |
| **Language** | Python |
| **License** | Apache-2.0 |
| **Updated** | 6 days ago |
| **Paper** | Accepted at KDD 2025 |

**What it does:** Multi-faceted AI agent and workflow **auto-tuning**. Automatically optimizes LangChain, LangGraph, DSPy programs for better quality, lower latency, and lower cost.

**Why it matters — TESTING/QUALITY:**
- **2.8x quality improvement** with just $5 and 24 minutes
- **10x cost reduction** via workflow-level optimization
- **2.7x latency reduction** via hierarchical optimization
- **Pareto frontier output** — Multiple optimized versions with different quality-cost-latency tradeoffs
- **Framework-agnostic** — Works with unmodified LangChain, DSPy source code
- **CLI-driven:** `cognify optimize /your/ai/agent.py`

**Key Insight:** Cognify solves a crucial marketplace problem — **how do you objectively compare skill quality?** By auto-tuning agents and producing Pareto-optimal configurations, it provides a framework for benchmarking skills on quality, cost, and latency simultaneously. KDD 2025 acceptance validates the approach.

---

### 7. silent-architects/auxilo

| Field | Value |
|-------|-------|
| **URL** | https://github.com/silent-architects/auxilo |
| **Stars** | 0 (very new) |
| **Language** | JavaScript |
| **License** | MIT |
| **Updated** | 17 days ago |

**What it does:** Agent capability discovery + knowledge marketplace with x402 micropayments on Base.

**Why it matters — PRICING/DISCOVERY:**
- **Dual product:** Skill Discovery (30 skills, 8 categories) + Knowledge Marketplace
- **Knowledge monetization** — Agents share operational learnings; contributors earn 70% when others unlock
- **x402 micropayments** — HTTP-native payments, no accounts/API keys/subscriptions needed
- **Tiered pricing:**
  - Free: categories, stats, learn submission
  - $0.001: discover, skill lookup
  - $0.0005: knowledge search
  - Dynamic (min $0.005): knowledge unlock (70% to contributor)
- **MCP server integration** — Claude Desktop can search Auxilo directly
- **Rating system** — 1-5 helpfulness ratings affect ranking

**Key Insight:** The **knowledge marketplace** concept is novel — agents pay to access learnings from other agents' real-world experiences. "E2B sessions timeout after 5 min idle — send a no-op every 3 minutes" is the kind of operational knowledge that has real value. The 70/30 revenue split incentivizes quality contributions.

---

### 8. pratikjadhav2726/agentverse-marketplace

| Field | Value |
|-------|-------|
| **URL** | https://github.com/pratikjadhav2726/agentverse-marketplace |
| **Stars** | 2 |
| **Language** | TypeScript |
| **License** | MIT |
| **Updated** | 26 days ago |

**What it does:** Full-stack marketplace platform with semantic search, visual workflow builder, credit system, and Stripe integration.

**Why it matters — FULL PLATFORM:**
- **Managed Agent Runtime SDK** — Python/Node.js SDK abstracting A2A protocol
- **Auto Dockerfile generation** — Infers dependencies, builds images, deploys
- **Visual Workflow Builder** — Drag-and-drop canvas with ReactFlow for multi-agent orchestration
- **Credit system** — 1 credit = $1, Stripe integration, wallet-based
- **Semantic agent search** — Intent-based discovery, not just keyword matching
- **Hierarchical agent management** — Manager agents orchestrate worker agents
- **Security model:** JWT cookies, AES-256-CBC credential encryption, parameterized SQL

**Tech Stack:** Next.js 14, TypeScript, Tailwind CSS, shadcn/ui, ReactFlow, Supabase/SQLite

**Key Insight:** Most complete open-source marketplace implementation found so far. The combination of visual workflow builder, credit system, and agent runtime SDK covers the full lifecycle from development to monetization.

---

## Tier 2: Notable Repos

### 9. win4r/openclaw-a2a-gateway

| Field | Value |
|-------|-------|
| **URL** | https://github.com/win4r/openclaw-a2a-gateway |
| **Stars** | 236 |
| **Language** | TypeScript |
| **Updated** | Today |

**Description:** OpenClaw plugin implementing A2A v0.3.0 protocol — bidirectional agent communication gateway. Exposes JSON-RPC + REST endpoints, publishes Agent Cards at `/.well-known/agent-card.json`, handles TextPart/FilePart/DataPart, supports bearer token auth and Tailscale mesh networking.

**Relevance:** Highest-starred A2A protocol implementation. Shows how to bridge existing agent systems (OpenClaw) to the A2A standard. The Tailscale integration pattern is notable for private marketplace deployments.

---

### 10. Sevii/agent-marketplace (Claude Code Plugin Marketplace)

| Field | Value |
|-------|-------|
| **URL** | https://github.com/Sevii/agent-marketplace |
| **Stars** | 20 |
| **Language** | Python |
| **License** | MIT |
| **Updated** | 1 month ago |

**Description:** Curated collection of Claude Code plugins — elevator music for idle prompts, desktop notifications, hook loggers. Uses `/plugin marketplace add` and `/plugin install` patterns.

**Relevance:** Shows the emerging **Claude Code plugin distribution model**. The `plugin marketplace add` + `plugin install` CLI pattern is becoming a de facto standard for agent skill distribution.

---

### 11. settlemint-archive/agent-marketplace

| Field | Value |
|-------|-------|
| **URL** | https://github.com/settlemint-archive/agent-marketplace |
| **Stars** | 5 |
| **Language** | Python |
| **License** | MIT |
| **Updated** | 6 days ago |

**Description:** Portable agent setup for Claude Code and Codex that works identically in local CLI and cloud environments. Bundles 37 skills, 10 commands, and complete workflow enforcement.

**Why notable:**
- **37 skills across domains** — TDD, debugging, security (Semgrep, CodeQL), quality review, docs generation
- **Workflow enforcement via CLAUDE.md** — Task classification (Trivial to Complex) with mandatory phases and gate checks
- **Cloud parity** — Same agent behavior whether running locally or in Claude Code web/remote
- **Codex + Claude Code** — Dual-agent support with shared skill infrastructure

**Key Insight:** The **"portable agent marketplace in a repo"** pattern — everything bundled so agents behave identically across environments. The workflow enforcement via CLAUDE.md is a governance mechanism enforced through natural language instructions rather than code.

---

### 12. animeshkundu/condukt

| Field | Value |
|-------|-------|
| **URL** | https://github.com/animeshkundu/condukt |
| **Stars** | 0 (new) |
| **Language** | TypeScript |
| **Updated** | 3 days ago |

**Description:** Composable AI agent workflow framework — graph-based execution with DAG scheduling, fan-out/fan-in parallelism, event-sourced state, and full React UI.

**Why notable — COMPOSITION:**
- **4 node types:** agent (LLM), deterministic (pure function), gate (human approval), verify (iterative validation)
- **Event-sourced state** — Every execution event persisted; projections recomputed from log
- **12 sub-path exports** — Modular imports, consumers install only what they need
- **Full React UI** — Interactive flow graph with 50+ tool formatters, dark theme

**Key Insight:** The `gate` (human approval) and `verify` (iterative validation with retries) node types are directly applicable to skill marketplace quality gates and approval workflows.

---

### 13. ben-mengz/EDMA (Event-Driven Multi-Agent)

| Field | Value |
|-------|-------|
| **URL** | https://github.com/ben-mengz/EDMA |
| **Stars** | 3 |
| **Language** | Python |
| **License** | Apache-2.0 |
| **Updated** | 6 days ago |

**Description:** Event-driven multi-agent workflow framework built on FastMCP. Agents communicate through structured events via a central Event Hub rather than prompt sequences.

**Why notable — COMPOSITION:**
- **Event Hub architecture** — Central MCP server for event ingestion, persistence, and rebroadcasting via SSE
- **OpenAI Agents SDK bridge** — Dynamically fetches remote agent profiles and reconstructs them as OpenAI Agent primitives
- **Server-to-Client push** — Bidirectional event flow between backend agents and UI
- **ThreadHelper** — Async-to-GUI-thread bridge solving deadlock problems

**Key Insight:** The event-driven architecture (vs. prompt-driven) makes complex multi-agent workflows more transparent and controllable. The pattern of reconstructing remote agents as local primitives is relevant to marketplace skill discovery.

---

### 14. proxygate-official/cli

| Field | Value |
|-------|-------|
| **URL** | https://github.com/proxygate-official/cli |
| **Stars** | 4 |
| **Language** | TypeScript |
| **License** | Other |
| **Updated** | 2 days ago |

**Description:** "The Airbnb for AI Agents" — CLI for buying APIs, selling agent capacity, exposing services via tunnels, and posting jobs. USDC on Solana.

**Why notable — BILLING/MARKETPLACE:**
- **Full marketplace CLI** — `proxygate pricing`, `proxygate proxy`, `proxygate tunnel`, `proxygate jobs`
- **Tunnel-based selling** — Sellers expose local services through gateway, traffic scanned by Model Armor
- **Job marketplace** — Post tasks with rewards, agents/humans claim and submit
- **Settlement system** — `proxygate settlements --role seller` for earnings history
- **Claude Code skills** — `/pg-setup`, `/pg-buy`, `/pg-sell`, `/pg-status` slash commands
- **Trust scores** — API catalog includes availability and trust metrics

---

### 15. user14232/human-governed-ai-framework (DevOS)

| Field | Value |
|-------|-------|
| **URL** | https://github.com/user14232/human-governed-ai-framework |
| **Stars** | 0 |
| **Language** | Python |
| **Updated** | Today |

**Description:** Governance kernel for AI-assisted development — deterministic workflows, artifact-driven handoffs, append-only decision logs.

**Why notable — GOVERNANCE:**
- **Explicit anti-autonomy** — "DevOS is explicitly not an autonomous system"
- **System primitives:** Run -> Workflow -> Agent -> Artifact -> Decision -> Event -> Knowledge
- **Artifact-only communication** — Agents can ONLY communicate through structured artifacts
- **Append-only decision log** — Every human decision recorded immutably
- **State machine enforcement** — INIT -> PLANNING -> ARCH_CHECK -> TEST_DESIGN -> IMPLEMENTING -> TESTING -> REVIEWING
- **OS metaphor:** Process = Run, Program = Workflow, Worker = Agent, Filesystem = Artifacts

**Key Insight:** The most rigorous governance framework found. The principle of **artifact-only handoffs** (no side channels) and append-only decision logs creates a fully auditable agent execution trail.

---

## Tier 3: Emerging / Niche

### 16. geofmureithi/agentium

| Field | Value |
|-------|-------|
| **URL** | https://github.com/geofmureithi/agentium |
| **Stars** | 11 |
| **Language** | Rust |
| **License** | GPL-3.0 |

**Description:** Rust-based framework for building interoperable agents using **WASM modules** following A2A protocol standards. Agents as WebAssembly modules with `agent.toml` descriptors, end-to-end encrypted communication, and DAG-based workflow orchestration.

**Key Insight:** WASM-based agents enable **sandboxed execution** across hosts — a crucial primitive for marketplace trust.

---

### 17. valory-xyz/autonolas-marketplace (Mech Marketplace)

| Field | Value |
|-------|-------|
| **URL** | https://github.com/valory-xyz/autonolas-marketplace |
| **Stars** | 4 |
| **Language** | Solidity |
| **License** | MIT |

**Description:** On-chain agent marketplace with smart contracts for agent registration, request delivery, karma/reputation system, balance tracking, and buy-back-burn tokenomics. Built on the Olas (Autonolas) protocol.

**Key Insight:** Most mature **on-chain marketplace implementation** with real tokenomics (buy-back-burn), multi-token payments (native, OLAS, USDC), and smart contract-based reputation.

---

### 18. pluginagentmarketplace/claude-plugin-ecosystem-hub

| Field | Value |
|-------|-------|
| **URL** | https://github.com/pluginagentmarketplace/claude-plugin-ecosystem-hub |
| **Stars** | 14 |
| **Updated** | 10 days ago |

**Description:** Comprehensive directory of 500+ Claude AI extensions — plugins, skills, MCPs, commands, agents, and marketplaces. Includes comparison tables, security notes, and installation guides.

**Key Insight:** Serves as a **meta-index** of the Claude Code ecosystem. Documents 10,000+ MCP servers and 500+ plugins with verification dates and status tracking.

---

### 19. jjhiza/core-foundry

| Field | Value |
|-------|-------|
| **URL** | https://github.com/jjhiza/core-foundry |
| **Stars** | 2 |
| **Language** | Python |
| **License** | MIT |

**Description:** LLM-agnostic tool registry micro-framework. Decorator-based tool registration (`@registry.register`), auto-discovery from Python packages, Pydantic schema validation, and adapter pattern for any LLM provider.

**Key Insight:** Clean separation between tool **registration** (CoreFoundry) and **orchestration** (LangChain/CrewAI/etc.). The "micro-framework for tool management only" philosophy avoids framework lock-in.

---

### 20. Samk1710/ALTnode (AITnode)

| Field | Value |
|-------|-------|
| **URL** | https://github.com/Samk1710/ALTnode |
| **Stars** | 12 |
| **Language** | TypeScript |
| **License** | MIT |

**Description:** Decentralized no-code AI agent marketplace — agents minted as NFTs on EDU-CHAIN, metadata encrypted via Lit Protocol, stored on IPFS. Each agent can issue its own ERC-20 tokens.

**Key Insight:** The **AI-agent-as-NFT** pattern enables unique ownership and on-chain provenance tracking. Lit Protocol encryption ensures only NFT owners can execute agents.

---

### 21. shariqazeem/parallaxpay_x402

| Field | Value |
|-------|-------|
| **URL** | https://github.com/shariqazeem/parallaxpay_x402 |
| **Stars** | 3 |
| **Language** | TypeScript |

**Description:** Autonomous AI agent marketplace with distributed compute, x402 micropayments ($0.001/inference), swarm intelligence with consensus algorithms, and on-chain reputation on Solana. Features 6 specialized agent types and MCP server integration.

---

### 22. vishalmysore/a2awebagent

| Field | Value |
|-------|-------|
| **URL** | https://github.com/vishalmysore/a2awebagent |
| **Stars** | 12 |
| **Language** | HTML/Java |
| **License** | MIT |

**Description:** A2A protocol + Selenium for AI-driven web automation, test execution, and evidence capture. Ideal for intelligent testing frameworks.

**Key Insight:** Demonstrates **A2A protocol applied to testing** — agents control browsers, validate UI flows, and record structured evidence. Applicable to skill testing/QA.

---

## A2A Protocol Ecosystem

The Agent-to-Agent protocol has spawned a rich ecosystem. Here are the key implementations found:

| Repo | Stars | Language | Focus |
|------|-------|----------|-------|
| win4r/openclaw-a2a-gateway | 236 | TypeScript | Bidirectional gateway, OpenClaw integration |
| geofmureithi/agentium | 11 | Rust | WASM agents, encrypted communication |
| vishalmysore/a2awebagent | 12 | Java/HTML | Web automation + testing via A2A |
| sierracatalina/agent-aware-starter | 13 | JavaScript | Intent layer for A2A + RAG discovery |
| inference-gateway/adl-cli | 8 | Go | CLI scaffold for enterprise A2A agents |
| 5enxia/langgraph-a2a-server | 6 | Python | LangGraph to A2A bridge |
| flyryan/dify-a2a-plugin | 6 | Python | Dify to A2A bridge |
| greenpdx/rsadk | 6 | Rust | Full Rust ADK inspired by Google ADK |
| capiscio/capiscio-node | 4 | Go/Node.js | Agent card validation + trust scoring |
| colours93/a2a-rs | 3 | Rust | Rust SDK for A2A |
| jsulmont/mcp-lisp | 3 | Common Lisp | MCP + A2A in Lisp |
| Sawyer-G/Open-A2A | 2 | Python | Decentralized A2A collaboration |
| Aganium/a2a-protocol | 1 | — | agent:// URI scheme spec |
| capiscio/capiscio-sdk-python | 1 | Python | Runtime security middleware |
| v-checha/a2akit | 1 | TypeScript | "NestJS for AI agents" |
| andreibesleaga/a2a-php | 1 | PHP | PHP SDK (v0.2.5-0.3.0) |
| daniprol/django-a2a | 1 | Python | Django integration |
| jasagiri/a2a-nim | 1 | Nim | Nim implementation |
| JonathanGrocott/A2A-MQTT | 1 | Python | MQTT transport for A2A |

**Key Observations:**
- A2A has implementations in **10+ languages** — this level of cross-language adoption is rare for protocols this young
- The `/.well-known/agent-card.json` discovery pattern is becoming standard
- Bridge projects (LangGraph-A2A, Dify-A2A, Django-A2A) show integration demand
- The `agent://` URI scheme (Aganium) hints at a future DNS-like agent identity layer

---

## Thematic Analysis

### 1. Testing & Quality Assurance

| Project | Approach | Maturity |
|---------|----------|----------|
| **GenseeAI/cognify** | Auto-tuning for quality/cost/latency Pareto optimization | High (KDD 2025) |
| **capiscio/capiscio-node** | Multi-dimensional agent card scoring (compliance + trust) | Medium |
| **bkauto3/Conduit** | Cryptographic proof bundles for verifiable execution | Medium |
| **vishalmysore/a2awebagent** | A2A + Selenium for automated UI testing | Low-Medium |
| **animeshkundu/condukt** | `verify` node type with iterative validation + retries | Low (new) |

**Emerging pattern:** Quality assurance is splitting into **static validation** (schema/card checking) and **dynamic verification** (runtime proof bundles, auto-tuning benchmarks).

### 2. Pricing, Billing & Metering

| Project | Model | Payment Rails |
|---------|-------|---------------|
| **HYRVE-AI** | 85/15 commission, 48h escrow | Stripe + USDT |
| **Auxilo** | x402 micropayments ($0.001/query) | USDC on Base |
| **ParallaxPay** | $0.001/inference, swarm consensus | USDC on Solana |
| **ProxyGate** | API proxy billing, job marketplace | USDC on Solana |
| **AgentVerse** | Credit system (1 credit = $1) | Stripe |
| **Autonolas** | On-chain balance tracker, buy-back-burn | Native/OLAS/USDC |
| **ALTnode** | NFT ownership + ERC-20 agent tokens | On-chain |

**Emerging pattern:** Three payment architectures competing:
1. **Traditional SaaS** — Stripe, credits, commission splits (AgentVerse, HYRVE)
2. **Micropayments** — x402 protocol, per-request pricing (Auxilo, ParallaxPay)
3. **On-chain tokenomics** — NFTs, agent tokens, buy-back-burn (Autonolas, ALTnode)

### 3. Skill Composition & Orchestration

| Project | Model | Key Pattern |
|---------|-------|-------------|
| **condukt** | DAG execution with fan-out/fan-in | Graph-based, event-sourced state |
| **EDMA** | Event-driven via central Event Hub | Event pub/sub, SSE streaming |
| **microsoft/multi-agent-marketplace** | Simulation-based market design | Economic outcome measurement |
| **settlemint agent-marketplace** | CLAUDE.md workflow enforcement | Natural language governance |
| **DevOS** | State machine with artifact-only handoffs | Deterministic execution |

**Emerging pattern:** Composition models range from **declarative DAGs** (condukt) to **event-driven** (EDMA) to **state machines** (DevOS). The DAG approach dominates for predictable workflows; event-driven for dynamic, real-time scenarios.

### 4. Governance & Compliance

| Project | Approach | Frameworks |
|---------|----------|------------|
| **AI-Agent-Governance-Compliance-Kit** | Policy-to-control mapping, gap analysis | SOC2, ISO27001, GDPR, NIST AI RMF, IMDA |
| **Conduit** | SHA-256 hash chains + Ed25519 proofs | SOC2, GDPR, HIPAA, SOX |
| **DevOS** | Append-only decision logs, artifact-only handoffs | Custom deterministic governance |
| **settlemint** | CLAUDE.md workflow enforcement | Gate checks, phase progression |
| **capiscio** | Runtime security middleware, rate limiting | A2A protocol compliance |

**Emerging pattern:** Governance is splitting into **regulatory compliance** (mapping to SOC2/GDPR/etc.) and **operational governance** (enforcing execution patterns). Both are needed for enterprise marketplace adoption.

---

## Architecture Patterns

### Pattern 1: "Trust Layer Sandwich"
```
+-- Application Layer -------------------------+
|  Marketplace UI, Agent Dashboard, CLI        |
+-- Trust Layer --------------------------------+
|  Agent Cards, Badges, Proof Bundles          |
|  Compliance Scores, Trust Ratings            |
+-- Execution Layer ----------------------------+
|  Sandbox, WASM, Containers                   |
|  Hash Chains, Audit Logs                     |
+-- Payment Layer ------------------------------+
|  x402, Stripe, Escrow, Credits               |
+-- Protocol Layer -----------------------------+
   A2A, MCP, JSON-RPC, SSE
```

### Pattern 2: "Self-Registering Agent Economy"
(HYRVE-AI / CashClaw model)
1. Agent reads `SKILL.md` from marketplace
2. Agent collects its own capability metadata
3. Agent registers itself via API
4. Agent receives and executes jobs autonomously
5. Agent gets paid through escrow -> settlement

### Pattern 3: "Composable Workflow Marketplace"
(condukt / EDMA / AgentVerse model)
1. Skills registered as individual nodes
2. Users compose workflows via visual builder or YAML
3. DAG scheduler handles execution with quality gates
4. Event-sourced state enables replay/audit
5. Results flow through verification nodes before delivery

### Pattern 4: "Verifiable Execution"
(Conduit / CapiscIO model)
1. Every agent action enters a hash chain
2. Chain is signed with agent's Ed25519 key
3. Proof bundle generated as self-verifiable archive
4. Trust scores derived from verification history
5. Marketplace uses proof bundles as transaction receipts

---

## Implications for Our Marketplace

### Critical Gaps to Address

1. **No single project covers all 5 layers** (discovery, trust, payments, orchestration, governance). The market is fragmented — our marketplace can be the integration layer.

2. **x402 micropayments gaining traction** — Three independent projects (Auxilo, ParallaxPay, ProxyGate) all chose x402 on Solana/Base. Worth monitoring as a payment standard.

3. **CapiscIO's dual scoring** (compliance + trust, each 0-100 with breakdowns) is the most sophisticated quality framework found. Consider adapting for skill quality ratings.

4. **Cognify's auto-tuning** provides an objective benchmark mechanism — skills could be compared on quality/cost/latency Pareto frontiers.

5. **SKILL.md self-registration** (HYRVE) is an elegant onboarding pattern that reduces marketplace friction to near-zero.

6. **The governance gap is real** — Only 2 projects (AI-Agent-Governance-Compliance-Kit, DevOS) address enterprise compliance, and both are early-stage.

### Recommended Integrations

| Component | Recommended Approach | Reference Project |
|-----------|---------------------|-------------------|
| Quality Scoring | Multi-dimensional (compliance + trust + performance) | CapiscIO |
| Execution Verification | SHA-256 hash chains + Ed25519 proofs | Conduit |
| Workflow Composition | DAG-based with event sourcing | condukt |
| Pricing Model | Hybrid (credits + micropayments) | AgentVerse + Auxilo |
| Compliance | Policy-to-framework mapping | Governance-Compliance-Kit |
| Agent Onboarding | SKILL.md self-registration | HYRVE-AI |
| Marketplace Simulation | Pre-launch economic testing | Microsoft Magentic |

---

## Full Repo Index

| # | Repo | Stars | Language | License | Category | Updated |
|---|------|-------|----------|---------|----------|---------|
| 1 | microsoft/multi-agent-marketplace | 147 | Python | MIT | Simulation | Today |
| 2 | GenseeAI/cognify | 273 | Python | Apache-2.0 | Auto-tuning | 6d ago |
| 3 | win4r/openclaw-a2a-gateway | 236 | TypeScript | — | A2A Gateway | Today |
| 4 | Sevii/agent-marketplace | 20 | Python | MIT | Plugin Marketplace | 1mo ago |
| 5 | tryanything-ai/agent_marketplace | 18 | TypeScript | — | Decentralized | 5mo ago |
| 6 | pluginagentmarketplace/claude-plugin-ecosystem-hub | 14 | — | MIT | Directory | 10d ago |
| 7 | sierracatalina/agent-aware-starter | 13 | JavaScript | — | A2A Discovery | 17d ago |
| 8 | Samk1710/ALTnode | 12 | TypeScript | MIT | NFT Marketplace | 22d ago |
| 9 | vishalmysore/a2awebagent | 12 | HTML/Java | MIT | A2A Testing | 16d ago |
| 10 | geofmureithi/agentium | 11 | Rust | GPL-3.0 | WASM Agents | 1mo ago |
| 11 | muratcankoylan/actual_code | 11 | Python | MIT | A2A Assessment | 2mo ago |
| 12 | ertugrulakben/HYRVE-AI | 9 | — | MIT | Agent Economy | Today |
| 13 | inference-gateway/adl-cli | 8 | Go | MIT | A2A CLI | 1mo ago |
| 14 | ESJavadex/claude-homeassistant-plugins | 7 | Python | MIT | Home Assistant | 9d ago |
| 15 | phuryn/pm-skills | 7,312 | — | MIT | PM Skills | Today |
| 16 | aiagenta2z/ai-agent-marketplace | 6 | Python | — | Directory | 5d ago |
| 17 | 5enxia/langgraph-a2a-server | 6 | Python | MIT | A2A Bridge | 6d ago |
| 18 | flyryan/dify-a2a-plugin | 6 | Python | Apache-2.0 | A2A Bridge | 1mo ago |
| 19 | greenpdx/rsadk | 6 | Rust | — | Rust ADK | 1mo ago |
| 20 | ChaosChain/fin-studio | 6 | TypeScript | MIT | A2A Finance | 5mo ago |
| 21 | settlemint-archive/agent-marketplace | 5 | Python | MIT | Portable Skills | 6d ago |
| 22 | NikhilRaikwar/SomniaX | 5 | TypeScript | MIT | Blockchain | 2mo ago |
| 23 | zero-point-module/based-agents | 5 | TypeScript | — | Agent Builder | 1mo ago |
| 24 | valory-xyz/autonolas-marketplace | 4 | Solidity | MIT | On-chain | 1mo ago |
| 25 | oldschoolag/Faivr | 4 | TypeScript | Other | Marketplace | 17d ago |
| 26 | capiscio/capiscio-node | 4 | Go/Node.js | Apache-2.0 | A2A Validation | 16d ago |
| 27 | proxygate-official/cli | 4 | TypeScript | Other | API Marketplace | 2d ago |
| 28 | akmenon1996/ai-agent-marketplace | 4 | TypeScript | MIT | Gen AI | 3mo ago |
| 29 | shriguhanp/AI-Agent-Marketplace | 4 | JavaScript | — | Marketplace | 2d ago |
| 30 | 0xYudhishthra/adapt.ai | 4 | Rust | — | DeFi Agents | 3mo ago |
| 31 | shariqazeem/parallaxpay_x402 | 3 | TypeScript | — | Compute Market | 4d ago |
| 32 | ben-mengz/EDMA | 3 | Python | Apache-2.0 | Event-Driven | 6d ago |
| 33 | jsulmont/mcp-lisp | 3 | Common Lisp | — | MCP+A2A | Today |
| 34 | colours93/a2a-rs | 3 | Rust | MIT | A2A SDK | 20d ago |
| 35 | bkauto3/Conduit | 2 | Python | Other | Audit/Trust | 1d ago |
| 36 | pratikjadhav2726/agentverse-marketplace | 2 | TypeScript | MIT | Full Platform | 26d ago |
| 37 | jjhiza/core-foundry | 2 | Python | MIT | Tool Registry | 18d ago |
| 38 | Sawyer-G/Open-A2A | 2 | Python | Other | Decentralized | 2d ago |
| 39 | HuaweiCloudDeveloper/mcp-server-marketplace | 2 | HTML | — | MCP Directory | 6mo ago |
| 40 | esbmc/agent-marketplace | 2 | C | MIT | Claude Plugin | 16d ago |
| 41 | capiscio/capiscio-sdk-python | 1 | Python | Apache-2.0 | Runtime Security | 3d ago |
| 42 | ucsandman/AI-Agent-Governance-Compliance-Kit | 1 | JavaScript | — | Governance | 2d ago |
| 43 | silent-architects/auxilo | 0 | JavaScript | MIT | Knowledge Market | 17d ago |
| 44 | user14232/human-governed-ai-framework | 0 | Python | — | Governance | Today |
| 45 | animeshkundu/condukt | 0 | TypeScript | — | Orchestration | 3d ago |

---

*Report generated from 15+ GitHub searches covering agent marketplaces, tool registries, A2A protocol, MCP marketplaces, workflow composition, governance, testing, and pricing. 20+ repos scraped for deep analysis.*
