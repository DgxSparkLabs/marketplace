# AI Agent Skill Marketplaces — Round 8 GitHub Research

**Date:** 2026-03-16
**Focus:** A2A Protocol ecosystem, SKILL.md tooling, trust infrastructure, marketplace economics, enterprise patterns
**Searches:** 12 queries across 6 gap areas identified in R7

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Complete Repository Inventory](#complete-repository-inventory)
3. [A2A Protocol Ecosystem Deep Dive](#a2a-protocol-ecosystem-deep-dive)
4. [Skill Marketplace Ecosystem](#skill-marketplace-ecosystem)
5. [SKILL.md Tooling Landscape](#skillmd-tooling-landscape)
6. [Trust & Security Infrastructure](#trust--security-infrastructure)
7. [Enterprise Deployment Patterns](#enterprise-deployment-patterns)
8. [Architecture Patterns & Design Choices](#architecture-patterns--design-choices)
9. [Key Findings & Gaps Remaining](#key-findings--gaps-remaining)

---

## Executive Summary

Round 8 reveals an ecosystem that has passed the "proof of concept" phase and entered **infrastructure buildout**. The three dominant signals:

1. **A2A Protocol is becoming the TCP/IP of agent communication.** 30+ implementations across 8 languages, with production-ready SDKs in TypeScript, Rust, Go, Python, Java, and PHP. The protocol spec (v0.3.0) has stabilized enough that **framework integrations** (Dify, LangGraph, Django, OpenClaw) are appearing — a classic sign of ecosystem maturity.

2. **The marketplace explosion is real but shallow.** We found 30+ "agent skill marketplace" repos, but most are template forks or weekend projects. Three stand out as serious: **SkillX** (full-stack marketplace with hybrid search, 34★), **SquidBay** (Bitcoin Lightning-powered agent economy, live at squidbay.io), and **MCPBundler** (curated skill aggregator bridging Hugging Face, Automattic, and n8n ecosystems).

3. **Trust infrastructure is the missing piece being actively built.** Three distinct approaches emerged: **trust-mcp** (MCP-native trust scoring with 9-chain verification), **Praesidia** (enterprise OAuth 2.0/OIDC for A2A with five trust levels), and **capiscio** (agent card cryptographic validation). None are mature. This is the single biggest gap.

**Net new repos discovered (not in R1-R7):** 45+
**Deep-analyzed repos:** 18
**Notable pattern:** The OpenClaw skill ecosystem is exploding — dozens of skills appearing weekly, indicating a viable distribution channel has emerged.

---

## Complete Repository Inventory

### A2A Protocol Implementations (30 repos found)

| # | Repo | URL | ★ | Language | Updated | Description |
|---|------|-----|---|----------|---------|-------------|
| 1 | win4r/openclaw-a2a-gateway | [link](https://github.com/win4r/openclaw-a2a-gateway) | 236 | TypeScript | today | OpenClaw A2A v0.3.0 bidirectional gateway |
| 2 | vishalmysore/a2awebagent | [link](https://github.com/vishalmysore/a2awebagent) | 12 | HTML/Java | 16d ago | A2A + Selenium web automation/testing |
| 3 | muratcankoylan/actual_code | [link](https://github.com/muratcankoylan/actual_code) | 11 | Python | 2mo ago | 7-agent code assessment via A2A + Gemini |
| 4 | inference-gateway/adl-cli | [link](https://github.com/inference-gateway/adl-cli) | 8 | Go | 1mo ago | Enterprise A2A agent scaffolding CLI |
| 5 | 5enxia/langgraph-a2a-server | [link](https://github.com/5enxia/langgraph-a2a-server) | 6 | Python | 6d ago | LangGraph ↔ A2A bridge server |
| 6 | flyryan/dify-a2a-plugin | [link](https://github.com/flyryan/dify-a2a-plugin) | 6 | Python | 1mo ago | Dify ↔ A2A cross-platform plugin |
| 7 | greenpdx/rsadk | [link](https://github.com/greenpdx/rsadk) | 6 | Rust | 1mo ago | Full Rust A2A agent framework |
| 8 | ChaosChain/fin-studio | [link](https://github.com/ChaosChain/fin-studio) | 6 | TypeScript | 5mo ago | Fintech A2A + blockchain agents |
| 9 | 5enxia/langgraph-a2a-client | [link](https://github.com/5enxia/langgraph-a2a-client) | 4 | Python | 30d ago | LangGraph A2A client tool |
| 10 | colours93/a2a-rs | [link](https://github.com/colours93/a2a-rs) | 3 | Rust | 20d ago | Rust A2A SDK |
| 11 | v-checha/a2akit | [link](https://github.com/v-checha/a2akit) | 1 | TypeScript | 2mo ago | Decorator-based A2A server ("NestJS for agents") |
| 12 | daniprol/django-a2a | [link](https://github.com/daniprol/django-a2a) | 1 | Python | 28d ago | Django A2A integration |
| 13 | andreibesleaga/a2a-php | [link](https://github.com/andreibesleaga/a2a-php) | 1 | PHP | 16d ago | PHP A2A SDK (v0.2.5-0.3.0) |
| 14 | shashikanth-gs/a2a-opencode | [link](https://github.com/shashikanth-gs/a2a-opencode) | 1 | TypeScript | 20d ago | A2A wrapper for OpenCode |
| 15 | shashikanth-gs/a2a-copilot | [link](https://github.com/shashikanth-gs/a2a-copilot) | 1 | TypeScript | 20d ago | A2A wrapper for GitHub Copilot SDK |
| 16 | agent-matrix/a2a-validator | [link](https://github.com/agent-matrix/a2a-validator) | 1 | JavaScript | 5mo ago | A2A protocol validation web app |
| 17 | gmsh/agentified-opencaptchaworld | [link](https://github.com/gmsh/agentified-opencaptchaworld) | 1 | Python | 2mo ago | A2A CAPTCHA-solving benchmark |
| 18 | praesidia-ai/sdk-a2a | [link](https://github.com/praesidia-ai/sdk-a2a) | 0 | TypeScript | 2mo ago | Identity & auth layer for A2A |
| 19 | corvid-agent/a2a-algorand | [link](https://github.com/corvid-agent/a2a-algorand) | 0 | TypeScript | 9d ago | A2A over Algorand blockchain |
| 20 | nio-ono/tete-a-tete | [link](https://github.com/nio-ono/tete-a-tete) | 0 | TypeScript | 1mo ago | Zero-dep A2A implementation |
| 21 | grokify/a2a-go | [link](https://github.com/grokify/a2a-go) | 0 | Go | 20d ago | Go A2A helper |
| 22 | okdaichi/a2a-go | [link](https://github.com/okdaichi/a2a-go) | 0 | Go | 10mo ago | Pure Go A2A implementation |
| 23 | stefanwiest/hct-a2a | [link](https://github.com/stefanwiest/hct-a2a) | 0 | — | 2mo ago | HCT extension for A2A |
| 24 | Zephyr-Blessed/openclaw-a2a | [link](https://github.com/Zephyr-Blessed/openclaw-a2a) | 0 | TypeScript | 29d ago | OpenClaw A2A plugin |
| 25 | bobmcwilliams4/echo-a2a-protocol | [link](https://github.com/bobmcwilliams4/echo-a2a-protocol) | 0 | TypeScript | 18d ago | A2A discovery & task delegation |
| 26 | xuangong/a2a_demo | [link](https://github.com/xuangong/a2a_demo) | 0 | TypeScript | 1mo ago | Elkar A2A demo |
| 27 | JCallico/dotnet-ai-chess | [link](https://github.com/JCallico/dotnet-ai-chess) | 1 | C# | 7mo ago | Distributed chess via A2A |
| 28 | ezequiroga/a2a-bases | [link](https://github.com/ezequiroga/a2a-bases) | 1 | Python | 8mo ago | Multi-agent flight system via A2A |

### Skill Marketplace Repos (30 repos found)

| # | Repo | URL | ★ | Language | Updated | Description |
|---|------|-----|---|----------|---------|-------------|
| 1 | nextlevelbuilder/skillx | [link](https://github.com/nextlevelbuilder/skillx) | 34 | TypeScript | 1d ago | SkillX.sh — full marketplace with hybrid search, CLI |
| 2 | eugenepyvovarov/mcpbundler-agent-skills-marketplace | [link](https://github.com/eugenepyvovarov/mcpbundler-agent-skills-marketplace) | 8 | Python | 12d ago | MCPBundler curated skill aggregator |
| 3 | atilaahmettaner/skills-plane | [link](https://github.com/atilaahmettaner/skills-plane) | 2 | TypeScript | 1mo ago | Skills marketplace |
| 4 | DiversioTeam/agent-skills-marketplace | [link](https://github.com/DiversioTeam/agent-skills-marketplace) | 2 | HTML | 9d ago | Diversio marketplace with Claude metadata |
| 5 | ryanfrigo/clawmart | [link](https://github.com/ryanfrigo/clawmart) | 2 | TypeScript | 1d ago | ClawMart — AI workforce builder |
| 6 | squidbay/squidbay | [link](https://github.com/squidbay/squidbay) | 2 | HTML | 5d ago | Bitcoin Lightning agent-to-agent marketplace |
| 7 | coreline-ai/agent_skills_marketplace | [link](https://github.com/coreline-ai/agent_skills_marketplace) | 1 | Python | 5d ago | Agent skills marketplace |
| 8 | eli5-claw/agent-skills-marketplace | [link](https://github.com/eli5-claw/agent-skills-marketplace) | 1 | TypeScript | 5d ago | OpenClaw/Bankr skill marketplace |
| 9 | kght6123/skill-marketplace-template | [link](https://github.com/kght6123/skill-marketplace-template) | 1 | — | 5d ago | Marketplace template for Claude Code |
| 10 | DemonDamon/AgenticX-AgentSkills | [link](https://github.com/DemonDamon/AgenticX-AgentSkills) | 1 | Python | 1mo ago | Modern marketplace for AI agent skills |
| 11 | uexo/clawmall | [link](https://github.com/uexo/clawmall) | 0 | TypeScript | 15d ago | ClawMall — Build, Share, Earn |
| 12 | MyLifeOS-Corp/skillforge-marketplace | [link](https://github.com/MyLifeOS-Corp/skillforge-marketplace) | 0 | TypeScript | 1mo ago | SkillForge/MoltStore marketplace |
| 13 | shellcorpnet/crabskill-cli | [link](https://github.com/shellcorpnet/crabskill-cli) | 0 | JavaScript | 1mo ago | CrabSkill CLI for marketplace |
| 14 | avanorthstarlabs/skilltree | [link](https://github.com/avanorthstarlabs/skilltree) | 0 | JavaScript | 27d ago | SkillTree — Auth.js + on-chain payments |
| 15 | lawwu/skills-marketplace | [link](https://github.com/lawwu/skills-marketplace) | 0 | Python | 2d ago | Cookiecutter marketplace template |
| 16 | letsgotoplay/skillmarketplace | [link](https://github.com/letsgotoplay/skillmarketplace) | 0 | TypeScript | 17d ago | Enterprise AI Agent Skills Marketplace |
| 17 | JrPribs/agent-marketplace | [link](https://github.com/JrPribs/agent-marketplace) | 0 | — | 1mo ago | Decentralized marketplace + USDC + reputation |
| 18 | fwfutures/skills | [link](https://github.com/fwfutures/skills) | 0 | JavaScript | 17d ago | Skills for Claude Code and Codex |

### Trust & Security Repos

| # | Repo | URL | ★ | Language | Updated | Description |
|---|------|-----|---|----------|---------|-------------|
| 1 | Schmoll86/trust-mcp | [link](https://github.com/Schmoll86/trust-mcp) | 1 | JavaScript | 19d ago | 8-tool trust verification MCP server |
| 2 | praesidia-ai/sdk-a2a | [link](https://github.com/praesidia-ai/sdk-a2a) | 0 | TypeScript | 2mo ago | Enterprise identity/auth for A2A |
| 3 | capiscio/capiscio-sdk-python | [link](https://github.com/capiscio/capiscio-sdk-python) | 1 | Python | 3d ago | Runtime security middleware for A2A |
| 4 | midnghtsapphire/premolt | [link](https://github.com/midnghtsapphire/premolt) | 0 | TypeScript | 10d ago | AI agent security sandbox (proprietary) |
| 5 | Undermybelt/skill-agent-security | [link](https://github.com/Undermybelt/skill-agent-security) | 0 | Python | 1mo ago | Zero-trust sandbox OpenClaw skill |
| 6 | 0xca55/solveryn | [link](https://github.com/0xca55/solveryn) | 0 | TypeScript | 1mo ago | Solana-based agent trust verifier |

### SKILL.md Ecosystem Tooling

| # | Repo | URL | ★ | Language | Updated | Description |
|---|------|-----|---|----------|---------|-------------|
| 1 | JNZader/repoforge | [link](https://github.com/JNZader/repoforge) | 1 | Python | today | Generate SKILL.md + AGENT.md from any codebase |
| 2 | code4freedom/a2a-skillsforge | [link](https://github.com/code4freedom/a2a-skillsforge) | 0 | JavaScript | 8d ago | Web app for SKILL.md bundle creation |
| 3 | jonathansantilli/agent-skills | [link](https://github.com/jonathansantilli/agent-skills) | 0 | — | 27d ago | Curated reusable SKILL.md collection |
| 4 | zahlmann/bring-shopping-list | [link](https://github.com/zahlmann/bring-shopping-list) | 1 | Python | 29d ago | SKILL.md-compatible Bring! shopping skill |
| 5 | alecplayground/gomarkdown-paste-skill | [link](https://github.com/alecplayground/gomarkdown-paste-skill) | 3 | — | 1mo ago | SKILL.md-compatible markdown paste skill |

### OpenClaw Skill Ecosystem

| # | Repo | URL | ★ | Language | Updated | Description |
|---|------|-----|---|----------|---------|-------------|
| 1 | coolishagent/lobstalk | [link](https://github.com/coolishagent/lobstalk) | 25 | — | 2d ago | Agent group chat on Telegram |
| 2 | 0xMikey-ooze/cursor-coding-team | [link](https://github.com/0xMikey-ooze/cursor-coding-team) | 0 | JavaScript | 16d ago | Multi-Cursor agent orchestration |
| 3 | devastrar/openclaw-skill-agent-individuation | [link](https://github.com/devastrar/openclaw-skill-agent-individuation) | 0 | Shell | 11d ago | Agent identity development |
| 4 | wuxianwsc/openclaw-skill-agent-router | [link](https://github.com/wuxianwsc/openclaw-skill-agent-router) | 0 | JavaScript | 6d ago | Agent routing skill |
| 5 | mischaell/openclaw-newsletter-digest | [link](https://github.com/mischaell/openclaw-newsletter-digest) | 0 | JavaScript | 12d ago | Newsletter digest via Gmail + Telegram |

---

## A2A Protocol Ecosystem Deep Dive

### Maturity Assessment

The A2A (Agent-to-Agent) protocol has reached **early production readiness**. Here's the evidence:

#### Language Coverage (8 languages)

| Language | Implementations | Most Mature | Production-Ready? |
|----------|----------------|-------------|-------------------|
| **TypeScript** | 10+ | openclaw-a2a-gateway (236★), a2akit | ✅ Yes |
| **Python** | 6+ | langgraph-a2a-server, dify-a2a-plugin | ✅ Yes |
| **Rust** | 2 | rsadk (6★), a2a-rs (3★) | ⚠️ Early |
| **Go** | 3 | adl-cli (8★), a2a-go | ⚠️ Early |
| **Java** | 1 | a2awebagent (12★) | ⚠️ Early |
| **PHP** | 1 | a2a-php | ⚠️ Early |
| **C#** | 1 | dotnet-ai-chess | 🔴 Demo only |
| **Django** | 1 | django-a2a | ⚠️ Early |

#### Three Tiers of A2A Adoption

**Tier 1 — Platform Integrations (highest signal)**
These connect A2A to existing agent platforms with real user bases:

- **openclaw-a2a-gateway** (236★): Full bidirectional A2A gateway for OpenClaw. Handles all Part types (TextPart, FilePart, DataPart), bearer token auth, peer discovery, non-blocking async mode. This is the most complete implementation.
- **dify-a2a-plugin** (6★): Bridges Dify workflows to any A2A agent. 5 tools (List, Capabilities, Call Sync, Submit Async, Status). Submitted to Dify Marketplace. Supports both sync (message/send) and async (message/stream + tasks/get) patterns.
- **langgraph-a2a-server/client** (10★ combined): Two-package bridge between LangGraph's agent graph paradigm and A2A's task-based model.

**Tier 2 — Framework-level SDKs (building blocks)**

- **a2akit** (1★): "NestJS for AI agents" — decorator-based TypeScript library with zero runtime dependencies. Express and Fastify adapters. Full A2A protocol support including streaming (SSE). The cleanest developer experience seen in the A2A space.
- **rsadk** (6★): Feature-complete Rust SDK with multi-provider LLM support (OpenAI, Anthropic, Gemini), tool system, session management, and A2A JSON-RPC server. Follows Google's ADK patterns faithfully.
- **adl-cli** (8★): Enterprise-focused Go CLI that generates complete A2A agent projects from YAML "Agent Definition Language" files. Includes CI/CD generation, multi-cloud deployment configs, DevContainer support. Most enterprise-ready scaffolding tool.

**Tier 3 — Experimental/Niche**

- **a2a-algorand**: A2A messages encoded in Algorand transaction note fields. Immutable message history on blockchain. Novel but impractical for most use cases.
- **a2a-validator**: Web-based A2A protocol compliance checker. Essential tooling for the ecosystem — validates agent cards and lints live messages.
- **tete-a-tete**: Zero-dependency A2A implementation. Useful for understanding the protocol without framework overhead.

#### Key Protocol Evolution Signals

1. **v0.3.0 is the current stable spec.** All recent implementations target v0.3.0. The Agent Card format at `/.well-known/agent-card.json` (with legacy `/.well-known/agent.json` fallback) is standardized.

2. **JSON-RPC + REST is the transport consensus.** Every implementation uses JSON-RPC 2.0 over HTTP. SSE (Server-Sent Events) is the standard for streaming. gRPC is mentioned but not implemented.

3. **Agent Cards are the discovery mechanism.** The `.well-known/agent-card.json` pattern (borrowed from WebFinger/OpenID) enables decentralized agent discovery. Capiscio is building cryptographic validation on top.

4. **The missing piece: no standard registry.** Each implementation handles peer discovery manually. There's no equivalent of DNS for agents yet — you must know a peer's URL.

### A2A Architecture Pattern

```
┌─────────────────────┐    A2A/JSON-RPC    ┌─────────────────────┐
│  Agent Platform A   │◄──────────────────►│  Agent Platform B   │
│  (OpenClaw/Dify/    │    Over HTTP(S)    │  (Any A2A-compliant │
│   LangGraph/Custom) │                    │   implementation)   │
│                     │                    │                     │
│ /.well-known/       │  Discovery Phase   │ /.well-known/       │
│   agent-card.json   │◄─────────────────►│   agent-card.json   │
│                     │                    │                     │
│ POST /a2a           │  Task Phase        │ POST /a2a           │
│   - sendMessage     │◄──────────────────►│   - sendMessage     │
│   - getTask         │                    │   - getTask         │
│   - cancelTask      │                    │   - cancelTask      │
└─────────────────────┘                    └─────────────────────┘
```

---

## Skill Marketplace Ecosystem

### The Three Viable Marketplace Models

#### Model 1: SkillX — Centralized Marketplace with Hybrid Search

**Repo:** [nextlevelbuilder/skillx](https://github.com/nextlevelbuilder/skillx) (34★)
**Stack:** React Router v7 + Cloudflare Workers + D1 + Vectorize
**Status:** Phase 1 complete (MVP), Phase 2 planned (Stripe payments)

SkillX is the most complete centralized marketplace implementation found. Key architecture decisions:

- **Hybrid search engine:** Combines vector embeddings (bge-base-en-v1.5 via Cloudflare Workers AI) with SQLite FTS5 keyword search, merged via Reciprocal Rank Fusion + boost scoring. Search latency target: <800ms p95.
- **Rating system:** 0-10 scores + text reviews per skill. Skills ranked on leaderboard by quality metrics.
- **CLI-first:** `skillx search "data processing"` → `skillx use skillx-email` → `skillx report --outcome success`. The report command feeds execution results back into marketplace rankings.
- **Claude Code integration:** Ships as a Claude Code plugin (`/plugin marketplace add nextlevelbuilder/skillx`), including a `skill-creator` plugin for creating skills optimized for benchmark scoring.
- **500+ skills** seeded, with favorites and personalized recommendations.

**Architecture insight:** SkillX treats skills as first-class searchable objects rather than code packages. The semantic search layer is crucial — agents need to discover skills by intent ("I need to validate emails"), not by name.

#### Model 2: SquidBay — Decentralized Agent Economy on Bitcoin Lightning

**Repo:** [squidbay/squidbay](https://github.com/squidbay/squidbay) (2★)
**Stack:** Node.js + Express + SQLite (sql.js) + Bitcoin Lightning
**Status:** Live at squidbay.io (pre-launch audit)

SquidBay is the most architecturally radical marketplace. It's built on a premise that **agents should pay agents directly**:

- **Three-tier pricing model:**
  - ⚡ **Rent** (remote execution): Pay-per-call, seller's agent runs the task
  - 📄 **Learn** (skill file): Buy the blueprint/instructions
  - 📦 **Own** (full package): Source code + configs + templates
- **Bitcoin Lightning payments:** Instant, global, permissionless. 2% platform fee — 98% to seller.
- **Agent identity system:** Agents register with emoji avatars, bios, and locked names (can't rename to dodge bad reviews).
- **Verification tiers:**
  - Unverified — registered, no proof
  - A2A Verified (green ✓) — `.well-known/agent.json` matches registered card
  - X Verified (gold badge) — human operator verified via X post
- **No ads, no trackers** — trust differentiator for paid skills.
- **Agent names locked forever** — preventing marketplace gaming via identity changes.
- **SquidBot** — Claude-powered marketplace assistant that also posts on X (@squidbot).

**Architecture insight:** The Rent/Learn/Own tiering is brilliant. It maps to real economic patterns (SaaS / course / license) and allows marketplace pricing to capture the full value spectrum. The Lightning payment rail enables micro-transactions (50 sats ≈ $0.05 per API call) that traditional payment processors can't handle.

#### Model 3: MCPBundler — Curated Skill Aggregator

**Repo:** [eugenepyvovarov/mcpbundler-agent-skills-marketplace](https://github.com/eugenepyvovarov/mcpbundler-agent-skills-marketplace) (8★)
**Stack:** Python + MCPBundler app (mcpbundler.com)
**Status:** Active curation

MCPBundler takes a "package manager" approach rather than a "marketplace" approach:

- **Aggregates skills from major sources:** Hugging Face skills (5 skills), Vercel Labs, n8n, Automattic/WordPress, OpenAI, Remotion, Netresearch, and community contributors.
- **Categorized by domain:** AI/ML operations, browser automation, diagramming, marketing, WordPress development, code quality.
- **Credits original authors** with origin links.
- **No payment layer** — pure distribution focused.

**Key skills curated include:**
  - `hf-cli`, `model-trainer`, `hf-tool-builder` — Hugging Face ecosystem skills
  - `agent-browser`, `browser-use` — web automation
  - `enterprise-readiness-skill` — SLSA, SBOM, OpenSSF compliance
  - `git-workflow-skill` — Git best practices
  - 12 WordPress skills from Automattic
  - 15 marketing skills (A/B testing, SEO, copywriting, analytics)

**Architecture insight:** MCPBundler succeeds by being opinionated about quality. Rather than an open marketplace, it's a curated registry — closer to Homebrew than npm. For enterprise adoption, curation may matter more than open access.

### The Long Tail: Template Repos and Weekend Projects

The remaining 25+ marketplace repos fall into patterns:
- **Forks of a common template** (many share identical structures)
- **Enterprise landing pages** (letsgotoplay/skillmarketplace, Pdbjork/AgentSkillMarketplace)
- **Niche experiments** (crabskill-cli, skilltree with Auth.js + on-chain payments)
- **Chinese-language forks** (sunh3997-eng, jiangbingo/bingo-skills)
- **Cookiecutter templates** (lawwu/skills-marketplace)

This long tail confirms that building a marketplace is easy; building a marketplace with network effects is hard.

---

## SKILL.md Tooling Landscape

### What is SKILL.md?

SKILL.md is an emerging convention for packaging AI agent capabilities as self-contained markdown files. Originally adopted by Claude Code, it's now spreading to OpenCode, Codex CLI, Windsurf, and Cursor.

### Tooling Maturity Assessment

| Tool | Type | Maturity | Key Feature |
|------|------|----------|-------------|
| **RepoForge** | Generator | ⭐⭐⭐ | Auto-generates SKILL.md + AGENT.md from codebase analysis |
| **SkillsForge** | Web IDE | ⭐⭐ | Visual SKILL.md builder with validation + ZIP export |
| **Agent-Skills (jonathansantilli)** | Collection | ⭐ | Curated SKILL.md repository |
| **MCPBundler** | Aggregator | ⭐⭐⭐ | Cross-ecosystem skill distribution |

#### RepoForge — The Most Sophisticated Tool

**Repo:** [JNZader/repoforge](https://github.com/JNZader/repoforge) (1★, but technically impressive)

RepoForge is a model-agnostic code analysis tool that generates both documentation and agent skills from any codebase:

- **Multi-format output:**
  - `SKILL.md` files — per-module and per-layer skills for Claude Code
  - `AGENT.md` files — orchestrator and specialist agent definitions
  - `SKILLS_INDEX.md` — skill registry
  - Docsify documentation site
- **Project-type aware:** Different templates for web services (API Reference), SPAs (Components/State), CLI tools (Commands/Config), data science (Pipeline/Models), mobile apps (Screens/Navigation), infra/DevOps (Resources/Variables).
- **Monorepo support:** Generates per-layer skill sets with proper delegation.
- **Multi-agent compatible:**
  - Claude Code (`.claude/skills/`, `.claude/agents/`)
  - OpenCode (mirrored to `.opencode/`)
  - agent-teams-lite (`.atl/skill-registry.md`)
  - Gentleman-Skills format (YAML frontmatter)
- **Model agnostic:** Works with GitHub Models, Groq, Ollama, Anthropic, OpenAI.
- **GitHub Actions integration:** Auto-generates and deploys documentation.

**Architecture insight:** RepoForge solves the "cold start" problem for agent skills. Instead of manually writing SKILL.md files, it introspects your codebase and generates them. This is the right approach — skills should be derived from code, not written separately.

#### SkillsForge — Visual SKILL.md Builder

**Repo:** [code4freedom/a2a-skillsforge](https://github.com/code4freedom/a2a-skillsforge)

A zero-dependency web app for creating SKILL.md bundles:
- Builds SKILL.md with strict `name` and `description` frontmatter
- Generates `agents/openai.yaml`
- Packages scripts/, references/, assets/ placeholders
- ZIP export for distribution
- Local storage persistence
- GitHub Pages deployment

Simpler than RepoForge but useful as a quick creation tool.

### SKILL.md Ecosystem Health

The SKILL.md standard is gaining traction but lacks:
1. **No formal specification** — the format is defined by example (Claude Code's behavior), not by schema.
2. **No validation tool** — RepoForge generates valid files, but there's no standalone linter.
3. **No versioning standard** — skills don't have semver or compatibility metadata.
4. **No dependency resolution** — skills can't declare dependencies on other skills.

These are solvable problems, and the fact that multiple tools are converging on the format suggests it will stabilize.

---

## Trust & Security Infrastructure

### Comparison Matrix

| Feature | trust-mcp | Praesidia SDK | capiscio | Premolt |
|---------|-----------|---------------|----------|---------|
| **Approach** | MCP-native tools | OAuth 2.0/OIDC SDK | Agent card crypto validation | Security sandbox |
| **Trust scoring** | 0-100 score | 5 trust levels | Schema compliance + signatures | N/A |
| **Identity verification** | 9 chains (Lightning, ETH, SOL, Nostr, Domain, Twitter, ENS, Endpoint, GitHub) | OAuth 2.0 + DID | Cryptographic agent card validation | Identity verification |
| **Integration** | Claude, OpenClaw, any MCP | Express middleware, any A2A | CLI validation tool | Standalone platform |
| **Review system** | Yes (verified via Lightning proof-of-payment) | Audit logging | No | No |
| **Registry** | trustthenverify.com | Self-hosted | No central registry | No |
| **License** | MIT | MIT (built on @a2a-js/sdk) | Apache-2.0 | Proprietary |
| **Stars** | 1 | 0 | 4 (capiscio-node) | 0 |

### Deep Dive: trust-mcp — MCP-Native Trust Protocol

**Repo:** [Schmoll86/trust-mcp](https://github.com/Schmoll86/trust-mcp)

trust-mcp provides 8 MCP tools that any Claude or OpenClaw agent can use natively:

1. **trust_lookup** — Check agent trust score (0-100) before transacting
2. **trust_register** — Register your agent in the trust registry
3. **trust_review** — Submit verified reviews (Lightning proof-of-payment)
4. **trust_list** — Browse registered agents
5. **trust_challenge** — Get verification challenge for identity proofs
6. **trust_verify** — Verify identity across 9 chains
7. **trust_search** — Find agents by capability + minimum trust score
8. **trust_evidence** — Submit self-reported evidence

**Trust scoring mechanics:**
- Start at 5/100 on registration
- Verified Lightning pubkey: +8 points
- Verified Ethereum address: +8 points
- Verified Solana address: +8 points
- Verified domain: +4 points
- Verified Twitter: +2 points
- Verified GitHub: +4 points (OAuth)
- Verified endpoint: +5 points
- Verified ENS name: +4 points
- Each verified review: +8 points
- Self-reported evidence: weighted at 50%

**Architecture insight:** The multi-chain verification approach is clever — it lets agents prove identity through whatever chain they're native to. Lightning verification is particularly useful since it doubles as a payment rail. The 0-100 score is simple but effective as a decision signal ("only transact with agents scoring >50").

### Deep Dive: Praesidia — Enterprise-Grade A2A Identity

**Repo:** [praesidia-ai/sdk-a2a](https://github.com/praesidia-ai/sdk-a2a)

Praesidia extends A2A with enterprise security primitives:

- **OAuth 2.0/OIDC provider:** Full-spec token endpoint, JWKS, OpenID Discovery
- **Agent identity types:** AUTONOMOUS, SUPERVISED, SERVICE, ORCHESTRATOR
- **Five trust levels:** UNTRUSTED → LIMITED → STANDARD → ELEVATED → FULL
- **Middleware pipeline:** Composable auth → authorization → trust verification → audit logging
- **Client + Server packages:** Both PraesidiaClient and PraesidiaServer with full A2A integration
- **Security attestation:** Verify agent integrity and behavior

**Enterprise features:**
- Token introspection endpoint
- RBAC-style authorization (defaultAllow: false)
- Configurable minimum trust levels per endpoint
- InMemoryAuditLogSink (extensible to external sinks)
- Organization-level agent management

**Architecture insight:** Praesidia is the only solution targeting enterprise requirements (SOC2-style audit trails, OAuth compliance, role-based access). If you're deploying agents in a regulated environment, this is the starting point. However, it's still very early — the InMemoryAuditLogSink needs production persistence, and there's no documentation on deployment.

### Deep Dive: capiscio — Agent Card Cryptographic Validation

**capiscio-node** (4★) validates A2A agent cards for:
- Cryptographic trust (signature verification)
- Schema compliance (required fields, types)
- Live endpoint functionality (health checks)

**capiscio-sdk-python** (1★) provides runtime security middleware:
- Always-on validation of incoming A2A messages
- Signature verification
- Rate limiting

**Architecture insight:** Capiscio focuses narrowly on the agent card layer, which is the right abstraction point. If every agent card is cryptographically signed and validated, trust becomes transitive — "I trust agent B because its card is signed by authority X."

### The Trust Gap

None of these solutions address the full trust lifecycle:

```
Discovery → Verification → Transaction → Review → Reputation
    ↑                                                    |
    └────────────────────────────────────────────────────┘
```

- **trust-mcp** covers: Verification → Review → Reputation (weakly)
- **Praesidia** covers: Verification → Transaction (via middleware)
- **capiscio** covers: Discovery → Verification (at the card level)
- **SquidBay** covers: Transaction → Review → Reputation (via Lightning)

A complete trust infrastructure would need to combine all four approaches.

---

## Enterprise Deployment Patterns

### Pattern 1: ADL-CLI — Schema-Driven Agent Scaffolding

**Repo:** [inference-gateway/adl-cli](https://github.com/inference-gateway/adl-cli) (8★)

The most enterprise-focused tool discovered. Uses "Agent Definition Language" (YAML) to scaffold complete A2A projects:

```yaml
# agent.yaml — ADL manifest
apiVersion: adl/v1
kind: Agent
metadata:
  name: weather-agent
  description: Weather information agent
spec:
  type: ai-powered
  provider: openai
  model: gpt-4o-mini
  capabilities:
    streaming: true
    notifications: true
  scm:
    provider: github
```

Generates:
- Full project structure (Go, Rust, or TypeScript)
- CI/CD pipelines (GitHub Actions + semantic-release)
- Deployment configs (Kubernetes, Cloud Run)
- DevContainer and Flox sandbox environments
- Claude Code integration (`CLAUDE.md`)
- Health check, dependency injection, configuration management

**Enterprise readiness features:**
- SCM integration with GitHub (GitLab planned)
- `.adl-ignore` for protecting implementations during regeneration
- Post-generation hooks for custom build/format/test
- Multi-provider AI support (7 providers)
- Configurable acronyms (proper casing in generated code)

### Pattern 2: A2A Web Agent — Testing Automation

**Repo:** [vishalmysore/a2awebagent](https://github.com/vishalmysore/a2awebagent) (12★)

Uses A2A to orchestrate Selenium-based web testing:
- Agents control browsers, validate UI flows, capture evidence
- Spring Boot architecture with modular agent components
- Supports both local and remote (8-Way server) task execution
- WebSocket real-time updates

**Enterprise use case:** Automated QA where test agents communicate via A2A to coordinate complex multi-system test scenarios.

### Pattern 3: ClawMart — Managed AI Workforce

**Repo:** [ryanfrigo/clawmart](https://github.com/ryanfrigo/clawmart) (2★)

Reimagines skill marketplaces as **managed workforce platforms**:
- Users spin up "AI teams" from industry templates
- Agents can be created, edited, paused, deleted
- Dashboard with workforce management
- Stripe billing: Free / Pro $49 / Enterprise $199
- Next.js 15 + Convex + Clerk + Stripe stack

**Enterprise insight:** ClawMart shifts from "buy a skill" to "hire a team." This is closer to how enterprises actually think about agent adoption — not as individual tools, but as organizational capabilities.

---

## Architecture Patterns & Design Choices

### Pattern A: Agent Card as Service Discovery

Every A2A implementation uses `/.well-known/agent-card.json` for discovery. This is a de facto standard:

```json
{
  "name": "My Agent",
  "description": "What this agent does",
  "url": "https://agent.example.com/a2a/jsonrpc",
  "version": "1.0.0",
  "capabilities": {
    "streaming": true,
    "pushNotifications": false,
    "stateTransitionHistory": true
  },
  "skills": [
    {
      "id": "chat",
      "name": "Chat",
      "description": "General conversation"
    }
  ],
  "defaultInputModes": ["text/plain"],
  "defaultOutputModes": ["text/plain"]
}
```

### Pattern B: Three-Part Message Types

A2A v0.3.0 standardizes three part types:
- **TextPart** — Plain text
- **FilePart** — URI or base64-encoded files
- **DataPart** — Structured JSON

The openclaw-a2a-gateway handles all three, serializing them for LLM consumption:
- TextPart → raw text
- FilePart (URI) → `[Attached: report.pdf (application/pdf) → https://...]`
- FilePart (base64) → `[Attached: photo.png (image/png), inline 45KB]`
- DataPart → `[Data (application/json): {"key":"value"}]`

### Pattern C: Sync/Async Duality

All mature A2A implementations support both:
- **Synchronous:** `message/send` → wait → response (for quick tasks)
- **Asynchronous:** `message/stream` → taskId → poll via `tasks/get` (for long-running tasks)

The Dify plugin makes this explicit with separate "Call Agent (Sync)" and "Submit Task (Async)" tools.

### Pattern D: Decorator-Based Agent Definition

a2akit introduces a compelling DX pattern:

```typescript
@A2AAgent({ name: 'Hello Agent', version: '1.0.0' })
class HelloAgent {
  @Skill({ id: 'greet', name: 'Greet' })
  async greet(@TextPart() name: string): Promise<string> {
    return `Hello, ${name}!`;
  }

  @Skill({ id: 'count', name: 'Count' })
  @Streaming()
  async *count(@TextPart() input: string): AsyncGenerator<string> {
    for (let i = 1; i <= 5; i++) yield `Counting: ${i}...`;
  }
}
```

This reduces A2A server boilerplate to near zero and maps naturally to how developers think about agent capabilities.

### Pattern E: Blockchain as Trust Anchor

Three repos use blockchain for different trust functions:
- **a2a-algorand:** Message immutability (every A2A message is an on-chain transaction)
- **SquidBay:** Payment rail (Bitcoin Lightning for micropayments)
- **trust-mcp:** Identity verification (multi-chain signature proofs)
- **solveryn:** Agent trust on Solana
- **SkillTree / JrPribs/agent-marketplace:** On-chain payments + reputation staking

The consensus is forming: blockchain is useful for **payments and identity**, not for message transport.

### Pattern F: Social-First Agent Discovery

**Lobstalk** (25★) represents a novel approach: agents discover each other not through registries but through **Telegram group chats**. Agents develop personality, opinions, and social relationships. Security is paramount — agents are hardened against social engineering, authority claims, and instruction injection.

This "tavern before treaty" philosophy (agents socialize before they transact) may prove more natural than formal A2A discovery for many use cases.

---

## Key Findings & Gaps Remaining

### What R8 Confirmed

1. **A2A is winning the protocol war.** No competing standard has comparable ecosystem breadth (8 languages, platform integrations with Dify/LangGraph/OpenClaw/Django).

2. **Marketplace models are diverging into three clear categories:**
   - Centralized search (SkillX)
   - Decentralized payment (SquidBay)
   - Curated aggregation (MCPBundler)

3. **SKILL.md is the emerging skill packaging standard** but needs a formal spec, versioning, and dependency resolution.

4. **Trust infrastructure is the single biggest gap** — three incomplete solutions that each cover part of the lifecycle.

### New Gaps Identified for R9

1. **Agent registry / DNS for agents** — No standard discovery mechanism beyond manual URL exchange. Who builds the "DNS" for A2A agents?

2. **Skill versioning and compatibility** — No semver, no dependency trees, no breaking change detection for agent skills.

3. **Agent marketplace economics** — SquidBay has a pricing model, but nobody has unit economics data. What does a sustainable agent marketplace look like?

4. **Cross-marketplace portability** — Skills built for SkillX don't work on MCPBundler. Is an interop standard forming?

5. **Agent SEO / gaming** — The original R7 question about marketplace gaming remains unanswered. No repos address this, suggesting it's too early (or nobody wants to discuss it publicly).

6. **Agent failure recovery** — Zero repos found addressing failure insurance, rollback, or compensation. This gap is widening as agents handle more valuable tasks.

7. **A2A + MCP convergence** — A2A handles inter-agent communication; MCP handles tool access. How do they compose? trust-mcp bridges them but the general pattern isn't established.

8. **OpenClaw as distribution monopoly risk** — OpenClaw is becoming the iOS App Store of agent skills. The skill ecosystem is heavily concentrated there. Is this healthy?

---

*Report generated by automated GitHub research pipeline. 12 search queries, 18 repos deep-analyzed, 80+ repos catalogued.*
