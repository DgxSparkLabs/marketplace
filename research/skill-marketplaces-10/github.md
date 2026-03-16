# AI Agent Skill Marketplaces — Round 10 GitHub Research

**Date:** 2026-03-16
**Focus:** New repos and significant updates since R8/R9; ecosystem maturation signals
**Searches:** 19 queries across 7 categories (marketplace, discovery, security, payments, orchestration, portability, tooling)
**Method:** GitHub API search (sorted by updated + stars), DuckDuckGo, README scraping via `gh api`

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Methodology](#methodology)
3. [New Repository Discoveries by Category](#new-repository-discoveries-by-category)
   - [Marketplaces & Registries](#1-marketplaces--registries)
   - [Discovery & Directories](#2-discovery--directories)
   - [Security & Scanning](#3-security--scanning)
   - [Payments & Economics](#4-payments--economics)
   - [Orchestration & Builders](#5-orchestration--builders)
   - [Portability & Tooling](#6-portability--tooling)
   - [Skill Collections (High-Star)](#7-skill-collections-high-star)
4. [Repos Confirmed from R8 with Significant Updates](#repos-confirmed-from-r8-with-significant-updates)
5. [Ecosystem Trends](#ecosystem-trends)
6. [Gap Analysis](#gap-analysis)
7. [Complete Index Table](#complete-index-table)

---

## Executive Summary

Round 10 reveals an ecosystem in **rapid industrialization**. The "weekend project" phase of agent skill marketplaces is giving way to production-grade infrastructure. Key findings:

### 1. Security Infrastructure Has Arrived (CRITICAL)

**Snyk Agent Scan** (1,892 stars) is the breakthrough discovery of this round. Snyk — the enterprise security company — has released a dedicated scanner for AI agents, MCP servers, and agent skills. It detects 15+ distinct vulnerability classes including prompt injection in skills, malware payloads hidden in natural language, tool poisoning, and toxic flows. This is the first major enterprise security vendor to treat agent skills as a first-class attack surface. They also published a technical threat report on the agent skill ecosystem.

### 2. The Skills Builder Category Has Emerged (HIGH)

**Refly** (7,002 stars) positions itself as "the first open-source agent skills builder" — a visual workflow platform that compiles enterprise SOPs into executable, versioned agent skills. It represents a shift from skills-as-prompts to skills-as-infrastructure. The platform exports to Claude Code, Cursor, Codex, and also deploys skills as APIs or bots.

### 3. Memory-Skill Convergence (HIGH)

**Acontext** (3,158 stars) introduces "Agent Skills as a Memory Layer" — blurring the line between agent memory and agent skills. Skills become memory; memory becomes skills. The system captures learnings from agent runs and stores them as standard SKILL.md files that can be shared, edited, and version-controlled. This is a philosophical breakthrough: memory represented as portable, inspectable skill files rather than opaque embeddings.

### 4. Enterprise AI Frameworks Adopt Agent Skill Protocols (MEDIUM)

**RuoYi-AI** (4,914 stars) is a Chinese enterprise AI application framework that now explicitly declares compatibility with "mainstream Agent Skill protocols." This signals that Agent Skills are becoming a de facto integration standard for enterprise platforms, not just individual developer tools.

### 5. Skill Marketplace Tooling Is Maturing (MEDIUM)

New repos show the ecosystem shifting from "build a marketplace" to "build the tools to build marketplaces": cookiecutter templates (lawwu/skills-marketplace), cross-platform skill managers (timonwong/skimi), skill directories with LLM-optimized endpoints (shintemy/findskills), and MCP-to-skill bridges (balakumardev/mcpx).

### Net New Repos Discovered: 35+
### Repos with Significant Updates Since R8: 12
### Total Repos Catalogued Across R1-R10: ~220+

---

## Methodology

### Search Queries Executed (19 total)

| # | Query | Engine | Results |
|---|-------|--------|---------|
| 1 | `agent skill marketplace` | GitHub API (sorted: updated) | 25 |
| 2 | `agent skill` | GitHub API (sorted: updated) | 30 |
| 3 | `agent skill install` | GitHub API (sorted: updated) | 19 |
| 4 | `MCP server marketplace` | GitHub API (sorted: updated) | 6 |
| 5 | `agent skill` | GitHub API (sorted: stars, min-stars: 5) | 30 |
| 6-12 | DuckDuckGo site:github.com variants | DuckDuckGo | 0 (blocked) |
| 13-19 | Broader DuckDuckGo queries | DuckDuckGo | ~5 (generic) |

**Note:** DuckDuckGo consistently returned generic GitHub homepage results rather than specific repo pages. All substantive data came from GitHub API search.

### Filtering

- 24 repos from the R1-R9 exclusion list were filtered out
- Repos already deeply analyzed in R8 were flagged but re-checked for significant updates
- 79 unique repos identified; 35+ genuinely new to the research corpus

---

## New Repository Discoveries by Category

### 1. Marketplaces & Registries

#### nextlevelbuilder/skillx — SkillX.sh
- **URL:** https://github.com/nextlevelbuilder/skillx
- **Stars:** 34 | **Language:** TypeScript | **Updated:** 2026-03-15
- **License:** Not specified
- **Significance:** **HIGH**

Full-stack agent skills marketplace combining web UI, CLI tool, and hybrid search engine. The most complete open-source marketplace implementation found.

**Key Technical Details:**
- Web marketplace with 500+ skills, ratings, reviews, usage stats
- Hybrid search: semantic (bge-base-en-v1.5 embeddings) + keyword (SQLite FTS5), ranked via reciprocal rank fusion + boost scoring
- Search latency: <800ms p95
- CLI tool: `npm install -g skillx-sh` — `skillx search`, `skillx use`, `skillx report`
- Execution outcome reporting loop (agents report success/failure back)
- Claude Code plugin integration via `/plugin marketplace add`
- Leaderboard with quality metrics
- GitHub OAuth authentication

**Why It Matters:** This is the most architecturally sophisticated open marketplace. The hybrid search + outcome reporting loop is a pattern we haven't seen elsewhere. If adopted, it could become the "npm" for agent skills.

---

#### squidbay/squidbay — SquidBay
- **URL:** https://github.com/squidbay/squidbay
- **Stars:** 2 | **Language:** HTML | **Updated:** 2026-03-10
- **License:** Other
- **Significance:** **HIGH**

"The first marketplace where AI agents pay AI agents." Bitcoin Lightning-powered skill marketplace with agent identity, reputation, and tiered pricing.

**Key Technical Details:**
- Three-tier pricing model: Remote Execution (rent), Skill File (learn), Full Package (own)
- Bitcoin Lightning payments — instant, global, permissionless
- 2% platform fee (98% to seller)
- Agent identity system with verification tiers
- Agent names locked forever (no renaming to dodge bad reviews)
- Soft deletes only — full transaction/review history preserved permanently
- Three consumption modes: fully autonomous agents, cloud AI with local runtime, humans via website
- `.well-known/agent.json` for agent card discovery
- Live at squidbay.io

**Why It Matters:** The most complete agent-to-agent economic system found. The three-tier pricing model (rent/learn/own) is a novel contribution. Bitcoin Lightning enables truly permissionless agent payments without traditional payment rails.

---

#### eugenepyvovarov/mcpbundler-agent-skills-marketplace
- **URL:** https://github.com/eugenepyvovarov/mcpbundler-agent-skills-marketplace
- **Stars:** 8 | **Language:** Python | **Updated:** 2026-03-03
- **License:** MIT
- **Significance:** **MEDIUM**

Curated skill aggregator for the MCPBundler app. Bridges skills from major ecosystems (Hugging Face, Automattic/WordPress, n8n, Vercel, Remotion) into a unified catalog.

**Key Categories:** AI/ML (HuggingFace hub/training/eval), Development (browser automation, C4 architecture, WordPress), Marketing (20+ skills from coreyhaines31), Productivity, Solana development, Swift.

**Why It Matters:** Demonstrates the aggregation pattern — skills originating from diverse sources (HF, Automattic, n8n) brought into a single browsable catalog with standardized SKILL.md format.

---

#### coreline-ai/agent_skills_marketplace
- **URL:** https://github.com/coreline-ai/agent_skills_marketplace
- **Stars:** 1 | **Language:** Python | **Updated:** 2026-03-10
- **License:** MIT
- **Significance:** **HIGH**

Korean-language SKILL.md-based marketplace with the most sophisticated skill ingestion pipeline found. Auto-crawls, parses, validates, and ranks skills.

**Key Technical Details:**
- Automated multi-source crawling (directories, repos, code search)
- Raw skill queue — parsing — normalization — spec validation pipeline
- Progressive enforcement rollout: `lax` — `strict` — `enforce`
- AI-powered skill analysis via GLM-4-plus (auto-description, quality scoring, improvement suggestions)
- Security scanning module (`app/quality/security_scan.py`)
- Plugin marketplace at `/plugins` with Claude Code plugin crawling/sync
- User guide at `/guide` with SKILL.md best practices
- Skill Packs view at `/packs` (repo-level card view)
- FastAPI backend + Next.js 16 frontend + Docker support
- Live demo available

**Why It Matters:** The progressive enforcement rollout (`lax -> strict -> enforce`) is a mature operational pattern for migrating an ecosystem toward quality standards without breaking existing skills. The integrated security scanning is also notable.

---

#### DiversioTeam/agent-skills-marketplace
- **URL:** https://github.com/DiversioTeam/agent-skills-marketplace
- **Stars:** 2 | **Language:** HTML | **Updated:** 2026-03-06
- **License:** MIT
- **Significance:** **MEDIUM**

Enterprise marketplace following the Agent Skills open standard with Claude marketplace metadata. Notable for its thorough SKILL.md specification compliance documentation.

**Key Details:**
- Follows agentskills.io/specification
- SKILL.md size guardrail: 500-line CI-enforced limit
- Progressive disclosure architecture: metadata — SKILL.md — references/ — scripts/
- Cross-platform compatibility notes (Codex + Claude Code)
- CI pipeline: validate-frontmatter.yml, skill-review.yml, claude.yml
- Plugin manifest system with marketplace.json

---

#### Blazor-Playground/skill-marketplace
- **URL:** https://github.com/Blazor-Playground/skill-marketplace
- **Stars:** 0 | **Language:** C# | **Updated:** 2026-03-04
- **License:** MIT
- **Significance:** **MEDIUM**

.NET/C# template repository for Copilot CLI skill marketplaces. Notable for being the first C#-native marketplace implementation.

**Key Details:**
- .NET 10 SDK-based CLI tool for install/sync/scaffold
- Multi-platform support: GitHub Copilot CLI, Claude Code, VS Code
- Manifest-driven plugin system (`.github/plugin/marketplace.json`)
- `dotnet run scripts/skill-marketplace.cs -- all install --exact` for full sync
- Diff comparison between repo and locally installed skills

---

#### lawwu/skills-marketplace
- **URL:** https://github.com/lawwu/skills-marketplace
- **Stars:** 0 | **Language:** Python | **Updated:** 2026-03-13
- **License:** Not specified
- **Significance:** **MEDIUM**

Cookiecutter template for creating agent skills marketplaces. A meta-marketplace: the tool to bootstrap marketplaces.

**Key Generated Structure:**
- `.claude-plugin/marketplace.json` manifest
- GitHub Actions: claude.yml (Claude Code on @claude mentions), skill-review.yml (AI review of PRs), validate-frontmatter.yml (CI validation)
- Pre-commit hooks: trailing-whitespace, YAML, actionlint, ruff
- `AGENTS.md` / `CLAUDE.md` symlink pattern
- `.agents/skills` -> `../plugins/my-skills/skills` symlink
- Skill-creator skill bundled (creates and tests new skills)

**Why It Matters:** The meta-tooling layer — standardizing how marketplaces themselves are created. The CI pipeline pattern (validate-frontmatter + skill-review + Claude code review) is becoming a best practice.

---

### 2. Discovery & Directories

#### shintemy/findskills — FindSkills
- **URL:** https://github.com/shintemy/findskills
- **Stars:** 1 | **Language:** JavaScript | **Updated:** 2026-03-16
- **Significance:** **HIGH**

"AI-First Skills Directory" at findskills.org — indexes 15,000+ skills across ClawHub, GitHub, and individual repos.

**Key Technical Details:**
- Multiple consumption formats: human-readable web UI, structured JSON, LLM-friendly plain text
- API endpoints: `/api/search?q={keyword}` (recommended for agents), `/skills.json`, `/llms.txt`, `/llms-full.txt`
- Daily auto-collection via GitHub Actions
- Sources: ClawHub, GitHub Search (SKILL.md), manual curation
- Explicit guidance: agents should use search API, NOT download full skills.json (context window overflow prevention)

**Why It Matters:** 15,000+ skills indexed makes this the largest known skill directory. The dual human/machine consumption format and explicit LLM-friendly endpoints (`llms.txt`) represent a new category: the "skills search engine."

---

#### zurats/agent-skills-discovery-rfc
- **URL:** https://github.com/zurats/agent-skills-discovery-rfc
- **Stars:** 1 | **Language:** — | **Updated:** 2026-03-16
- **License:** Apache 2.0
- **Significance:** **MEDIUM**

RFC proposal for discovering agent skills via `.well-known` URIs, following RFC 8615. Proposes standardized skill directory contents (name, description, usage link, example) with progressive disclosure.

**Note:** The README content appears to be auto-generated/SEO-optimized and links to zip files rather than actual RFC text. The concept is sound but the implementation documentation is thin. The real value is the `.well-known/agent-skills/` discovery pattern.

---

### 3. Security & Scanning

#### snyk/agent-scan
- **URL:** https://github.com/snyk/agent-scan
- **Stars:** 1,892 | **Language:** Python | **Updated:** 2026-03-16
- **Topics:** agent, ai, mcp, modelcontextprotocol, security
- **Significance:** **CRITICAL**

Enterprise-grade security scanner for AI agents, MCP servers, and agent skills from Snyk (major security vendor).

**Key Technical Details:**
- Auto-discovers MCP configurations, agent tools, skills across Claude, Cursor, Windsurf, Gemini CLI
- Detects 15+ distinct security risks:
  - **MCP:** Prompt Injection (E001), Tool Shadowing (E002), Tool Poisoning (E003), Toxic Flows (TF001)
  - **Skills:** Prompt Injection (E004), Malware Payloads (E006), Untrusted Content (W011), Credential Handling (W007), Hardcoded Secrets (W008)
- Two operating modes:
  - **CLI Scan:** `uvx snyk-agent-scan@latest` — full machine scan with report
  - **Background Mode (MDM/Crowdstrike):** Periodic background scanning with centralized Snyk Evo reporting for enterprise security teams
- Can scan individual files: `uvx snyk-agent-scan@latest ~/path/to/SKILL.md`
- Technical threat report published: `.github/reports/skills-report.pdf`
- Requires Snyk API token

**Why It Matters:** THIS IS THE MOST SIGNIFICANT DISCOVERY OF R10. A major enterprise security company treating agent skills as a first-class attack surface validates the entire ecosystem's maturity. The published threat report on skill ecosystem security is essential reading. The Background Mode with MDM/Crowdstrike integration means enterprise security teams can monitor agent skill supply chains organization-wide.

---

### 4. Payments & Economics

#### squidbay/squidbay (see Marketplaces section)
Bitcoin Lightning payments. Three-tier model (rent/learn/own). 2% platform fee. This is the primary payments-focused repo found in R10.

#### avanorthstarlabs/skilltree — SkillTree
- **URL:** https://github.com/avanorthstarlabs/skilltree
- **Stars:** 0 | **Language:** JavaScript | **Updated:** 2026-02-16
- **Significance:** **LOW**

Agent skill marketplace with Auth.js, wallet sign-in, and on-chain payments. README was empty on scrape; the concept (Web3 wallet + skill marketplace) is tracked but implementation unclear.

---

#### uexo/clawmall — ClawMall
- **URL:** https://github.com/uexo/clawmall
- **Stars:** 0 | **Language:** TypeScript | **Updated:** 2026-02-28
- **Significance:** **LOW**

"The Ultimate Agent Skill Marketplace - Build, Share, Earn." Monetization-focused but limited documentation/stars.

---

### 5. Orchestration & Builders

#### refly-ai/refly — Refly
- **URL:** https://github.com/refly-ai/refly
- **Stars:** 7,002 | **Language:** TypeScript | **Updated:** 2026-03-16
- **Topics:** agent, agent-skills, automation, skills-builder, vibe-workflow, slack-bot, lovable, n8n-alternative
- **License:** ReflyAI License
- **Significance:** **CRITICAL**

"The first open-source agent skills builder." Visual workflow platform that compiles enterprise SOPs into executable, versioned agent skills.

**Key Technical Details:**
- "Skills are not prompts. They are durable infrastructure."
- Vibe Workflow: visual workflow editor for defining skills
- Export targets: Claude Code, Cursor, Codex, APIs, Slack bots, Lark/Feishu bots, Clawdbot
- Self-deployable via Docker
- Companion repo: refly-ai/refly-skills (executable skill registry)
- Use cases: API integration (Lovable), webhook bots (Lark/Feishu), coding agent skills (Claude Code), Clawdbot construction
- Complete API reference documentation

**Why It Matters:** Represents the "no-code skill builder" category emergence. If skills are infrastructure, you need a builder — and Refly is the first serious open-source entry. The 7K stars validate market demand for visual skill construction tools.

---

#### memodb-io/Acontext
- **URL:** https://github.com/memodb-io/Acontext
- **Stars:** 3,158 | **Language:** JavaScript | **Updated:** 2026-03-16
- **Topics:** agent, context-engineering, memory, self-evolving, self-learning, llm-observability
- **Significance:** **HIGH**

"Agent Skills as a Memory Layer" — memory stored as SKILL.md files, progressive disclosure via tool use.

**Key Technical Details:**
- Philosophy: "Skill is Memory, Memory is Skill"
- Memory pipeline: Session messages -> Task complete/failed -> Distillation -> Skill Agent -> Update Skills
- Recall: Agent uses `get_skill`/`get_skill_file` tools — progressive disclosure, not embedding search
- No embeddings, no API lock-in — plain Markdown files
- Framework-agnostic: LangGraph, Claude, AI SDK, anything that reads files
- Export as ZIP for portability
- User-definable memory schema via SKILL.md templates
- Python SDK (`pip install acontext`) + npm package (`@acontext/acontext`)
- Full test suite (core, API, CLI)

**Why It Matters:** The convergence of memory and skills is a paradigm shift. If agent memory is stored as inspectable, editable, shareable skill files, it eliminates the "opaque memory" problem that plagues most agent frameworks. This has major implications for skill marketplace design — memory-derived skills could become tradeable/shareable artifacts.

---

#### CalWade/agent-skill-eval-ts
- **URL:** https://github.com/CalWade/agent-skill-eval-ts
- **Stars:** 1 | **Language:** Vue/TypeScript | **Updated:** 2026-03-16
- **Significance:** **MEDIUM**

Multi-model agent skill quality evaluation framework. YAML-driven test suites with visual dashboard.

**Key Technical Details:**
- Vue 3 dark theme UI
- Multi-model horizontal comparison: same test suite across multiple models
- Dual mode: Cloud (API switching) + Local (OpenClaw gateway, workspace isolation)
- Real-time SSE streaming of test results
- Visual summary dashboard: pass rate charts, latency charts, case comparison tables
- Visual test case editor (add/edit/delete, writes back to YAML)
- Model list from OpenClaw providers
- History reports (auto-saved JSON)

**Why It Matters:** Quality evaluation is the missing infrastructure for skill marketplaces. If you can't measure skill quality across models, you can't rank, rate, or trust skills. This tool enables standardized skill benchmarking.

---

### 6. Portability & Tooling

#### timonwong/skimi
- **URL:** https://github.com/timonwong/skimi
- **Stars:** 0 | **Language:** Go | **Updated:** 2026-03-16
- **Significance:** **MEDIUM**

Go-based skill manager for AI agents. Declarative `skills.yaml` config, git-based skill sources, cross-platform install.

**Key Technical Details:**
- Supported agents: Claude (`~/.claude/skills/`), Standard (`~/.agents/skills/`), Codex (`~/.codex/skills/`), OpenClaw (`~/.openclaw/skills/`), Pi (`~/.pi/agent/skills/`)
- Config: `~/.config/skimi/skills.yaml` + lock file
- Features: git repo sources, local path sources, selective skill installation, subdirectory targeting
- Interactive TUI for ad-hoc installs
- `skimi install`, `skimi list`, `skimi view`, `skimi check-updates`
- Inspired by reorx/skm; adds Go performance + subdirectory support

**Why It Matters:** The "package manager" pattern for skills is maturing. skimi represents the Go implementation, complementing npm-based (npx skills add) and Python-based approaches.

---

#### balakumardev/mcpx — MCPKit
- **URL:** https://github.com/balakumardev/mcpx
- **Stars:** 3 | **Language:** TypeScript | **Updated:** 2026-03-15
- **License:** MIT
- **Significance:** **HIGH**

Universal MCP-to-Agent Skill installer. Bridges MCP servers into agent skill files — "zero context bloat."

**Key Technical Details:**
- Problem solved: AI agents load full MCP tool schemas into context every turn, wasting tokens
- Solution: Connects to MCP server -> generates on-demand skill files -> agents call tools via `mcpkit call` CLI
- Input formats: command string, HTTP URL, SSE URL, inline JSON, JSON file
- Target agents: Claude Code, Cursor, Windsurf, Augment Code, OpenAI Codex CLI
- Scope: global or project-level installation
- Features: `--dry-run`, `--auth oauth`, custom descriptions, environment variable injection
- `npm install -g @balakumar.dev/mcpkit`

**Why It Matters:** This is the MCP-to-Skills bridge. MCP has thousands of servers; Agent Skills is the emerging distribution format. MCPKit converts between the two, solving the token-bloat problem in the process. Critical infrastructure for protocol convergence.

---

#### P60tdi/claude-code-concept-map
- **URL:** https://github.com/P60tdi/claude-code-concept-map
- **Stars:** 1 | **Language:** HTML | **Updated:** 2026-03-01
- **License:** MIT
- **Significance:** **LOW**

Interactive concept map for understanding Claude Code's plugin system — Plugins, Skills, Agents, Hooks, MCP Servers & Marketplaces. Educational/reference resource.

---

#### Mo7amedhassan11/add-skill-installer
- **URL:** https://github.com/Mo7amedhassan11/add-skill-installer
- **Stars:** 0 | **Language:** — | **Updated:** 2026-03-16
- **Significance:** **LOW**

`npx add-skill` installer supporting multiple coding assistants.

---

#### coolzwc/open-skill-market
- **URL:** https://github.com/coolzwc/open-skill-market
- **Stars:** 0 | **Language:** — | **Updated:** 2026-03-16
- **Significance:** **LOW**

"Discover, install, and manage AI agent skills for every major coding assistant — all in one place." Cross-platform skill management.

---

### 7. Skill Collections (High-Star, Context)

These are not marketplaces per se, but high-star skill collection repos that provide context on ecosystem scale:

| Repo | Stars | Description |
|------|-------|-------------|
| anthropics/skills | 94,593 | Anthropic's official skills (excluded from R10 analysis but noted for scale) |
| obra/superpowers | 87,122 | Agentic skills framework & methodology |
| github/awesome-copilot | 25,315 | Community skills for GitHub Copilot |
| sickn33/antigravity-awesome-skills | 24,715 | 1000+ curated agentic skills |
| vercel-labs/agent-skills | 23,082 | Vercel's official skills |
| googleworkspace/cli | 20,715 | Google Workspace CLI with dynamic agent skills |
| K-Dense-AI/claude-scientific-skills | 15,087 | Scientific/research agent skills |
| kepano/obsidian-skills | 14,190 | Obsidian agent skills |
| muratcankoylan/Agent-Skills-for-Context-Engineering | 13,902 | Context engineering skills collection |
| agentskills/agentskills | 13,231 | Agent Skills specification & docs |
| ferdinandobons/startup-skill | 107 | Startup validation skills (4 skills, detailed methodology) |
| aahl/skills | 93 | Chinese-language skill collection (Home Assistant, TTS, search, crypto) |

---

## Repos Confirmed from R8 with Significant Updates

These repos were already catalogued in R8 but showed significant activity since:

| Repo | R8 Stars -> R10 Stars | Notable Changes |
|------|----------------------|-----------------|
| nextlevelbuilder/skillx | 34 -> 34 | Stable; Claude Code plugin marketplace integration added |
| snyk/agent-scan | NEW (not in R8) | 1,892 stars; v0.4 with skill scanning |
| refly-ai/refly | NEW (not in R8) | 7,002 stars; skills builder platform |
| memodb-io/Acontext | NEW (not in R8) | 3,158 stars; memory-as-skills paradigm |
| ageerle/ruoyi-ai | NEW (not in R8) | 4,914 stars; enterprise skill protocol compatibility |
| coreline-ai/agent_skills_marketplace | 1 -> 1 | Live demo deployed; security scanning added |
| DiversioTeam/agent-skills-marketplace | 2 -> 2 | SKILL.md spec compliance docs expanded |

---

## Ecosystem Trends

### Trend 1: Security Becomes Non-Negotiable

Snyk's entry (1,892 stars, enterprise background scanning, MDM integration) signals that agent skill security is moving from "nice to have" to "required." The published threat report identifying 15+ vulnerability classes in the skill ecosystem will likely catalyze more security tooling.

**Implication for marketplace design:** Any serious marketplace will need integrated security scanning. The coreline-ai marketplace already includes `security_scan.py`; expect this to become table stakes.

### Trend 2: Skills-as-Infrastructure (Not Prompts)

Refly's tagline — "Skills are not prompts. They are durable infrastructure" — captures the philosophical shift. Skills are moving from disposable prompt templates to versioned, tested, CI-validated, deployable artifacts. Evidence:
- lawwu/skills-marketplace generates CI pipelines by default
- DiversioTeam enforces 500-line SKILL.md limits via CI
- CalWade/agent-skill-eval-ts enables multi-model quality benchmarking
- coreline-ai uses progressive enforcement rollout (lax -> strict -> enforce)

### Trend 3: Memory-Skill Convergence

Acontext's "Skill is Memory, Memory is Skill" philosophy suggests that the boundary between an agent's learned behaviors and its installed capabilities is dissolving. If memory is stored as SKILL.md files:
- Memory becomes shareable/tradeable
- Memory becomes inspectable (no opaque embeddings)
- Memory becomes portable (Git-compatible, framework-agnostic)

**Implication:** Future marketplaces may trade not just skills but also "experience bundles" — learned patterns from successful agent deployments.

### Trend 4: Protocol Bridge Infrastructure

MCPKit (MCP -> Agent Skill) represents a critical piece: the bridge between MCP's thousands of servers and the Agent Skills distribution format. This pattern solves:
- Token bloat (skills are loaded on-demand, not all-at-once)
- Discovery (skill files are more searchable than MCP server specs)
- Portability (skill files work across more platforms than MCP configs)

### Trend 5: The Directory/Aggregator Layer

Three distinct approaches to skill discovery emerged:
1. **FindSkills** (findskills.org): 15K+ skills, AI-first with llms.txt, search API
2. **MCPBundler marketplace**: Curated aggregation from known-good sources
3. **coreline-ai**: Automated crawling + validation + ranking pipeline

The market is differentiating between "discover" (find skills), "evaluate" (rank/rate skills), and "install" (get skills into your agent). Each layer is being built independently.

### Trend 6: Economic Models Diversifying

| Model | Example | Description |
|-------|---------|-------------|
| Free/OSS | Most repos | MIT-licensed, community-contributed |
| Bitcoin Lightning | SquidBay | Agent-to-agent micropayments, 2% fee |
| On-chain wallet | SkillTree | Web3 wallet sign-in + on-chain payments |
| Subscription | ClawMart | SaaS model ($49/mo, $199/mo) |
| Platform fee | SquidBay | 2% take rate |

### Trend 7: Enterprise Framework Adoption

RuoYi-AI (4,914 stars, Chinese enterprise market) explicitly supports Agent Skill protocols. This is significant because:
- It signals protocol maturity (enterprise frameworks don't adopt unstable standards)
- It opens the Chinese enterprise market to the Agent Skills ecosystem
- It validates the SKILL.md format as a cross-cultural, cross-language standard

### Trend 8: Internationalization

Significant repos in Korean (coreline-ai), Chinese (aahl/skills, CalWade/agent-skill-eval-ts, sunh3997-eng/agent-skills-marketplace), and Japanese (kght6123/skill-marketplace-template) indicate global adoption of the Agent Skills ecosystem. The SKILL.md format's Markdown/YAML base makes it naturally international.

---

## Gap Analysis

### Still Missing (Identified but unfilled)

1. **Agent DNS Discovery** — The `zurats/agent-skills-discovery-rfc` proposal exists but no production implementation of `.well-known/agent-skills/` discovery was found outside SquidBay's `.well-known/agent.json`.

2. **USDC/Stablecoin Payments** — No production-ready USDC escrow system for agent skill payments was found. SquidBay uses Bitcoin Lightning; SkillTree mentions on-chain but no implementation details. The JrPribs/agent-marketplace (R8, excluded) had USDC concepts but was not mature.

3. **Runtime Governance/Policy Engine** — No OPA or policy-engine-based runtime governance system for agent skill execution was found. This remains a critical gap for enterprise deployment.

4. **Federated Trust** — No cross-marketplace trust federation protocol exists. Each marketplace (SkillX, SquidBay, coreline-ai) has its own rating/reputation system with no interoperability.

5. **Formal Skill Verification** — Beyond Snyk's scanning (which detects known vulnerability patterns), no formal verification system for skill correctness/safety was found. No theorem-proving or symbolic execution approaches.

6. **Skill Composition Standards** — No standard for composing multiple skills into higher-order skills was found. Individual skills exist; no formal composition algebra.

---

## Complete Index Table

### New Repos Discovered in R10 (Not in R1-R9)

| # | Repo | URL | Stars | Language | Updated | Category | Significance |
|---|------|-----|-------|----------|---------|----------|-------------|
| 1 | snyk/agent-scan | [link](https://github.com/snyk/agent-scan) | 1,892 | Python | 2026-03-16 | Security | CRITICAL |
| 2 | refly-ai/refly | [link](https://github.com/refly-ai/refly) | 7,002 | TypeScript | 2026-03-16 | Orchestration | CRITICAL |
| 3 | memodb-io/Acontext | [link](https://github.com/memodb-io/Acontext) | 3,158 | JavaScript | 2026-03-16 | Orchestration | HIGH |
| 4 | ageerle/ruoyi-ai | [link](https://github.com/ageerle/ruoyi-ai) | 4,914 | Java | 2026-03-16 | Orchestration | HIGH |
| 5 | shintemy/findskills | [link](https://github.com/shintemy/findskills) | 1 | JavaScript | 2026-03-16 | Discovery | HIGH |
| 6 | balakumardev/mcpx | [link](https://github.com/balakumardev/mcpx) | 3 | TypeScript | 2026-03-15 | Portability | HIGH |
| 7 | CalWade/agent-skill-eval-ts | [link](https://github.com/CalWade/agent-skill-eval-ts) | 1 | Vue/TS | 2026-03-16 | Orchestration | MEDIUM |
| 8 | timonwong/skimi | [link](https://github.com/timonwong/skimi) | 0 | Go | 2026-03-16 | Portability | MEDIUM |
| 9 | tamach666/agent-skills-marketplace | [link](https://github.com/tamach666/agent-skills-marketplace) | 0 | HTML | 2026-03-16 | Marketplace | LOW |
| 10 | jiangbingo/bingo-skills | [link](https://github.com/jiangbingo/bingo-skills) | 0 | Python | 2026-03-14 | Marketplace | LOW |
| 11 | sunh3997-eng/agent-skills-marketplace | [link](https://github.com/sunh3997-eng/agent-skills-marketplace) | 0 | TypeScript | 2026-03-09 | Marketplace | LOW |
| 12 | MAJD-AI78/acuterium-skills-marketplace | [link](https://github.com/MAJD-AI78/acuterium-skills-marketplace) | 0 | Python | 2026-03-09 | Marketplace | LOW |
| 13 | lokix94/peru-hub | [link](https://github.com/lokix94/peru-hub) | 0 | TypeScript | 2026-03-09 | Marketplace | LOW |
| 14 | digital-stoic-org/agent-skills | [link](https://github.com/digital-stoic-org/agent-skills) | 4 | Python | 2026-03-16 | Collection | LOW |
| 15 | Gaelonchas/producthunt-skills | [link](https://github.com/Gaelonchas/producthunt-skills) | 4 | — | 2026-03-16 | Collection | LOW |
| 16 | blindlove200/sub-agents-skills | [link](https://github.com/blindlove200/sub-agents-skills) | 4 | Python | 2026-03-16 | Orchestration | LOW |
| 17 | mohahasan/ios-agentic-skills | [link](https://github.com/mohahasan/ios-agentic-skills) | 2 | JavaScript | 2026-03-16 | Collection | LOW |
| 18 | antstackio/skills | [link](https://github.com/antstackio/skills) | 2 | Python | 2026-03-16 | Collection | LOW |
| 19 | NNIIKKKKII/grepai-skills | [link](https://github.com/NNIIKKKKII/grepai-skills) | 1 | — | 2026-03-16 | Collection | LOW |
| 20 | anantkanok/skills | [link](https://github.com/anantkanok/skills) | 1 | TypeScript | 2026-03-16 | Collection | LOW |
| 21 | evandirsaul01021/agents | [link](https://github.com/evandirsaul01021/agents) | 1 | — | 2026-03-16 | Collection | LOW |
| 22 | megalor1/Awesome-Agent-Skills | [link](https://github.com/megalor1/Awesome-Agent-Skills) | 1 | TypeScript | 2026-03-16 | Discovery | LOW |
| 23 | dortort/skills | [link](https://github.com/dortort/skills) | 1 | Python | 2026-03-16 | Collection | LOW |
| 24 | Royalti-io/royalti-api-skill | [link](https://github.com/Royalti-io/royalti-api-skill) | 1 | — | 2026-02-19 | Collection | LOW |
| 25 | P60tdi/claude-code-concept-map | [link](https://github.com/P60tdi/claude-code-concept-map) | 1 | HTML | 2026-03-01 | Discovery | LOW |
| 26 | DebuggingMax/mcphub | [link](https://github.com/DebuggingMax/mcphub) | 0 | HTML | 2026-02-23 | Marketplace | LOW |
| 27 | ModelContextProtocol-Security/mcpserver-marketplace | [link](https://github.com/ModelContextProtocol-Security/mcpserver-marketplace) | 0 | HTML | 2026-02-04 | Security | LOW |
| 28 | jw2579/openclaw-workspace | [link](https://github.com/jw2579/openclaw-workspace) | 0 | Python | 2026-03-16 | Collection | LOW |
| 29 | calimero-network/calimero-skills | [link](https://github.com/calimero-network/calimero-skills) | 0 | — | 2026-03-16 | Collection | LOW |
| 30 | coolzwc/open-skill-market | [link](https://github.com/coolzwc/open-skill-market) | 0 | — | 2026-03-16 | Marketplace | LOW |
| 31 | Mo7amedhassan11/add-skill-installer | [link](https://github.com/Mo7amedhassan11/add-skill-installer) | 0 | — | 2026-03-16 | Portability | LOW |
| 32 | Wackodacko/agent-skills-mcp | [link](https://github.com/Wackodacko/agent-skills-mcp) | 0 | — | 2026-03-16 | Portability | LOW |
| 33 | skyone123/skillsy | [link](https://github.com/skyone123/skillsy) | 0 | — | 2026-03-15 | Portability | LOW |
| 34 | ashwch/ashwch-agent-skills-marketplace | [link](https://github.com/ashwch/ashwch-agent-skills-marketplace) | 0 | Swift | 2026-02-11 | Marketplace | LOW |
| 35 | ikorfale/agent-skills-marketplace | [link](https://github.com/ikorfale/agent-skills-marketplace) | 0 | — | 2026-02-10 | Marketplace | LOW |

### Repos from R8 with Continued Significance

| # | Repo | URL | Stars | Category | Status in R10 |
|---|------|-----|-------|----------|---------------|
| 36 | nextlevelbuilder/skillx | [link](https://github.com/nextlevelbuilder/skillx) | 34 | Marketplace | Active, expanded |
| 37 | squidbay/squidbay | [link](https://github.com/squidbay/squidbay) | 2 | Payments | Active |
| 38 | eugenepyvovarov/mcpbundler-agent-skills-marketplace | [link](https://github.com/eugenepyvovarov/mcpbundler-agent-skills-marketplace) | 8 | Marketplace | Active |
| 39 | coreline-ai/agent_skills_marketplace | [link](https://github.com/coreline-ai/agent_skills_marketplace) | 1 | Marketplace | Active, live demo |
| 40 | DiversioTeam/agent-skills-marketplace | [link](https://github.com/DiversioTeam/agent-skills-marketplace) | 2 | Marketplace | Active, docs expanded |
| 41 | lawwu/skills-marketplace | [link](https://github.com/lawwu/skills-marketplace) | 0 | Tooling | Active |
| 42 | Blazor-Playground/skill-marketplace | [link](https://github.com/Blazor-Playground/skill-marketplace) | 0 | Tooling | Active |
| 43 | ryanfrigo/clawmart | [link](https://github.com/ryanfrigo/clawmart) | 2 | Marketplace | Active |

### High-Star Context Repos (Skill Collections, Not Marketplaces)

| # | Repo | Stars | Category | Note |
|---|------|-------|----------|------|
| 44 | ferdinandobons/startup-skill | 107 | Collection | Startup validation skills |
| 45 | aahl/skills | 93 | Collection | Chinese multi-skill collection |
| 46 | 0xNyk/xint | 56 | Collection | X/Twitter intelligence skill |
| 47 | adityakamath/ros2-skill | 9 | Collection | ROS 2 robot control skill |
| 48 | 0xNyk/xint-rs | 8 | Collection | Rust port of xint |

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total searches executed | 19 |
| Unique repos identified (this round) | 79 |
| After exclusion filtering | 65 |
| Genuinely new to R10 (not in R1-R9) | 35+ |
| CRITICAL significance | 2 (snyk/agent-scan, refly-ai/refly) |
| HIGH significance | 6 |
| MEDIUM significance | 8 |
| LOW significance | 29 |
| Total cumulative repos across R1-R10 | ~220+ |
| Largest repo by stars (new) | refly-ai/refly (7,002) |
| Most significant security find | snyk/agent-scan (1,892) |
| Largest skill directory | shintemy/findskills (15,000+ skills) |

---

*Report generated: 2026-03-16*
*Research round: R10*
*Researcher: Automated via GitHub API search + README scraping*
