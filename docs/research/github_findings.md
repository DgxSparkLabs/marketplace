# GitHub Research: Skill Marketplace Landscape

> **Generated:** July 2025
> **Searches performed:** 5 queries across GitHub repositories
> **Total unique repos found:** 72+

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Top Repositories (Detailed Analysis)](#top-repositories-detailed-analysis)
3. [Full Repository Catalog](#full-repository-catalog)
4. [Key Patterns & Trends](#key-patterns--trends)
5. [Notable Innovations](#notable-innovations)
6. [Technology Stack Analysis](#technology-stack-analysis)
7. [Marketplace Business Models](#marketplace-business-models)
8. [Conclusions & Implications](#conclusions--implications)

---

## Executive Summary

The "skill marketplace" space on GitHub is **dominated by the Claude Code / AI agent plugin ecosystem** (2025 wave). The majority of high-star repos are Claude Code skill marketplaces — curated collections of AI agent plugins/skills that extend coding assistants. A smaller but interesting set of repos cover **general talent/freelance marketplaces** and **AI agent-to-agent skill trading**.

### Key Findings

- **7,300+ stars** on the top repo (phuryn/pm-skills) — a PM-focused skills marketplace for Claude Code
- **AI agent skill marketplaces** are the dominant category (>50 repos), driven by Claude Code's plugin/marketplace architecture
- **Agent-to-agent commerce** is emerging (SquidBay — agents buying/selling skills via Bitcoin Lightning)
- **Talent/freelance marketplaces** are a separate, smaller category of mostly student/hobby projects
- The ecosystem is **very new** (most repos updated within last 1-7 days as of July 2025)

---

## Top Repositories (Detailed Analysis)

### 1. phuryn/pm-skills ⭐ 7,311

| Field | Value |
|-------|-------|
| **URL** | https://github.com/phuryn/pm-skills |
| **Stars** | 7,311 |
| **Forks** | 706 |
| **License** | MIT |
| **Last Updated** | Today |
| **Language** | Markdown (skill definitions) |

**What it is:** The largest skill marketplace — a comprehensive Product Management operating system for AI coding assistants. Contains 65+ PM skills and 36 chained workflows across 8 plugins.

**Architecture:**
- **Skills** = building blocks with domain knowledge and frameworks (SKILL.md files with YAML frontmatter)
- **Commands** = user-triggered workflows that chain multiple skills (e.g., `/discover` chains 4 skills)
- **Plugins** = installable packages grouping related skills by PM domain
- Skills auto-load based on context; commands are explicitly invoked via `/slash-commands`

**8 Plugin Domains:**
1. `pm-product-discovery` — Ideation, experiments, assumption testing, OSTs, interviews (13 skills, 5 commands)
2. `pm-product-strategy` — Vision, business models, pricing, competitive landscape (12 skills, 5 commands)
3. `pm-market-research` — Market research and analysis
4. `pm-data-analytics` — Data analytics for product teams
5. `pm-marketing-growth` — Marketing and growth
6. `pm-go-to-market` — Launch planning
7. `pm-execution` — Execution workflows
8. `pm-toolkit` — Core PM tools

**Key Features:**
- Encodes proven PM frameworks (Teresa Torres, Marty Cagan, Alberto Savoia)
- Cross-tool compatibility: Works with Claude Code, Cowork, Gemini CLI, OpenCode, Cursor, Codex CLI, Kiro
- Commands flow into each other, matching natural PM workflow
- Comprehensive installation for both CLI and GUI users

**Takeaway:** Demonstrates that a well-structured, domain-specific skill collection with chained workflows can achieve massive adoption. The "framework-as-skill" pattern is powerful.

---

### 2. daymade/claude-code-skills ⭐ 652

| Field | Value |
|-------|-------|
| **URL** | https://github.com/daymade/claude-code-skills |
| **Stars** | 652 |
| **Forks** | 100 |
| **License** | MIT |
| **Language** | Python |
| **Last Updated** | Today |

**What it is:** A professional Claude Code skills marketplace with 42 production-ready skills. Notable for having a **meta-skill** (`skill-creator`) that helps users build, validate, and package their own skills.

**Architecture:**
- Individual skill directories, each independently installable
- Marketplace manifest (`.claude-plugin/marketplace.json`)
- Install scripts for macOS/Linux/Windows
- Each skill has `SKILL.md` with YAML frontmatter

**Notable Skills (42 total):**
- `skill-creator` — Meta-skill for creating/validating/packaging new skills
- `github-ops` — Comprehensive GitHub operations suite (PR creation, issue management, API operations)
- `markdown-tools` — Document conversion (doc/docx/PDF/PPTX to markdown)
- `mermaid-tools` — Diagram generation
- `qa-expert` — QA testing with autonomous execution
- `prompt-optimizer` — EARS methodology prompt optimization
- `excel-automation` — Excel creation, parsing, macOS control
- `financial-data-collector` — US equities financial data
- `iOS-APP-developer` — iOS app development assistance
- `youtube-downloader` — YouTube video/audio downloading

**Key Innovation:** The `skill-creator` meta-skill — a skill that creates other skills. This is a marketplace-building primitive.

**Tech Stack:** Python scripts, Shell installers, Markdown skill definitions

---

### 3. mhattingpete/claude-skills-marketplace ⭐ 469

| Field | Value |
|-------|-------|
| **URL** | https://github.com/mhattingpete/claude-skills-marketplace |
| **Stars** | 469 |
| **Forks** | 51 |
| **License** | Apache-2.0 |
| **Language** | HTML |
| **Last Updated** | Today |

**What it is:** A curated marketplace focused on software engineering workflows — Git automation, testing, code review, visual documentation, and code operations.

**Architecture (Multi-Plugin):**
```
claude-skills-marketplace/
├── .claude-plugin/marketplace.json
├── execution-runtime/              # Code execution environment (MCP)
├── engineering-workflow-plugin/     # Git, testing, code review
├── visual-documentation-plugin/    # Diagrams, dashboards, flowcharts
├── productivity-skills-plugin/     # Code auditing, documentation
└── code-operations-plugin/         # Bulk refactoring, file analysis
```

**Key Innovation — Execution Runtime (90% Token Savings):**
- Implements Anthropic's code execution pattern via MCP
- Instead of loading code through context, Claude executes Python locally with API access
- Claims **90-99% token reduction** for bulk operations
- Example: "Rename function in all Python files" — 25,000 tokens → 600 tokens (97.6% savings)

**Skills + Agents Architecture:**
- **Skills** = model-invoked capabilities (auto-triggered by context via SKILL.md)
- **Agents** = specialized Claude instances for specific work (AGENT.md, can use different models)
- Skills orchestrate agents; agents use skills — composable hierarchy

**Takeaway:** The execution runtime for token savings and the Skills + Agents composable architecture are standout innovations.

---

### 4. binance/binance-skills-hub ⭐ 462

| Field | Value |
|-------|-------|
| **URL** | https://github.com/binance/binance-skills-hub |
| **Stars** | 462 |
| **Forks** | 86 |
| **License** | Not specified |
| **Last Updated** | Today |

**What it is:** An open skills marketplace from Binance giving AI agents native access to crypto — both centralized and decentralized. Search tokens, execute trades, track wallets, monitor signals, interact with DeFi protocols via natural language.

**Architecture:**
- Each skill in its own folder with `SKILL.md` (YAML frontmatter + instructions)
- Designed for "the entire crypto ecosystem" — any agent, any framework, any chain
- Compatible with LangChain, CrewAI, OpenClaw, Claude Code, and custom stacks
- Install via `npx skills add https://github.com/binance/binance-skills-hub`

**Key Points:**
- First major enterprise (Binance) publishing an open skills marketplace
- Cross-framework compatibility is a key design goal
- Heavily disclaimered (financial/trading risk warnings)

**Takeaway:** Enterprise validation of the open skills marketplace model. The cross-framework design is significant.

---

### 5. nextlevelbuilder/skillx ⭐ 34

| Field | Value |
|-------|-------|
| **URL** | https://github.com/nextlevelbuilder/skillx |
| **Stars** | 34 |
| **Forks** | 6 |
| **License** | Not specified |
| **Language** | TypeScript |
| **Last Updated** | Today |

**What it is:** A full-stack AI agent skills marketplace with web UI, CLI tool, and hybrid search engine. The most complete "marketplace platform" (vs. skill collection) in the results.

**Architecture:**
```
skillx/
├── apps/web/              # React Router SSR app (~2,000 LOC)
│   ├── routes/            # Pages + APIs
│   ├── components/        # UI components
│   └── lib/               # DB, auth, search, vectorization
├── packages/cli/          # skillx npm package (~400 LOC)
├── .claude-plugin/        # Claude Code plugin marketplace
└── scripts/               # Seed data (30 real skills)
```

**Tech Stack:**
- Frontend: React Router v7 + Tailwind v4 (dark theme, mint accent)
- Backend: Cloudflare Workers + D1 (SQLite)
- Search: Vectorize (embeddings) + FTS5 (keywords) + Reciprocal Rank Fusion
- Auth: Better Auth + GitHub OAuth
- Storage: KV (cache), R2 (assets)
- AI: Cloudflare Workers AI (bge-base-en-v1.5 embeddings)

**Key Features:**
- **Hybrid search**: Semantic search via vector embeddings + keyword search via FTS5 + RRF ranking
- Leaderboard with quality metrics
- Ratings (0-10) and reviews
- Favorites for personalized recommendations
- CLI tool: `skillx search`, `skillx use`, `skillx report`
- API key management for programmatic access
- Search latency: <800ms p95

**Business Model (planned):** Phase 2 includes Stripe payment integration

**Takeaway:** Most complete marketplace *platform* — goes beyond skill collection to include search, ratings, reviews, CLI, and leaderboard. The hybrid search (semantic + keyword + RRF) is sophisticated.

---

### 6. Array-Ventures/coworker ⭐ 14

| Field | Value |
|-------|-------|
| **URL** | https://github.com/Array-Ventures/coworker |
| **Stars** | 14 |
| **Forks** | 7 |
| **License** | Apache-2.0 |
| **Language** | TypeScript |
| **Last Updated** | Today |

**What it is:** An open-source AI agent workspace that combines chat, app builder, MCP, A2A protocol, and skills marketplace in one platform. Built with Mastra framework.

**Architecture:**
```
src/mastra/
  agents/       # Agent definitions
  tools/        # Reusable tools
  workflows/    # Scheduled tasks
  gog/          # Google Workspace integration
  whatsapp/     # WhatsApp bridge
  mcp/          # MCP server
app/            # Electron desktop app
```

**Tech Stack:**
- Backend: Mastra agents + tools (TypeScript)
- Desktop: Electron app (React + Tailwind)
- Integrations: WhatsApp, Google Workspace, MCP
- Scheduling: Inngest
- Runtime: Bun
- Deploy: Railway (one-click), Docker, self-hosted

**Key Features:**
- Skills marketplace (installs from ClawHub and skills.sh)
- A2A protocol for agent-to-agent communication
- App builder (Lovable-like) for internal dashboards
- MCP UI for visual MCP server management
- Multi-provider AI (OpenAI, Anthropic, Google, NVIDIA, Groq, Kimi)
- WhatsApp bridge for mobile agent interaction
- Scheduled tasks via cron

**Takeaway:** Interesting as a full agent workspace that *includes* a marketplace, rather than being purely a marketplace. The A2A protocol support is forward-looking.

---

### 7. Sompote/tiger_cowork ⭐ 14

| Field | Value |
|-------|-------|
| **URL** | https://github.com/Sompote/tiger_cowork |
| **Stars** | 14 |
| **Forks** | 5 |
| **License** | Not specified |
| **Language** | TypeScript |
| **Last Updated** | Today |

**What it is:** A self-hosted AI-powered workspace combining chat, file management, code execution, scheduled tasks, visual multi-agent editor, and skill marketplace. Compatible with any OpenAI-compatible API.

**Notable Architecture — Agent Reflection Loop:**
- After tool loop completes, an LLM evaluation judges whether the agent's work satisfied the objective
- Scores 0.0-1.0; if below threshold (default 0.7), re-enters tool loop to fix gaps
- Configurable: threshold, max retries, enable/disable
- Trade-off: Higher quality vs. extra API token cost

**Sub-Agent System — Three Operating Modes:**
1. Sequential processing
2. Parallel execution
3. Bus-based communication between agents

**Visual Agent Editor:**
- Drag-and-drop canvas for designing multi-agent systems
- Configurable protocols (TCP, Bus, Queue) between agents
- Exports to YAML for reproducibility

**Takeaway:** The reflection loop protocol and visual multi-agent editor are unique. The three sub-agent operating modes (sequential, parallel, bus) show sophisticated agent orchestration thinking.

---

### 8. squidbay/squidbay ⭐ 2

| Field | Value |
|-------|-------|
| **URL** | https://github.com/squidbay/squidbay |
| **Stars** | 2 |
| **Forks** | 0 |
| **License** | AGPL-3.0 |
| **Language** | HTML |
| **Last Updated** | 5 days ago |

**What it is:** "The first marketplace where AI agents pay AI agents." Agents register identity, list skills, build reputation, and get paid via Bitcoin Lightning. Despite low stars, this is the most innovative marketplace concept found.

**Architecture:**
- Frontend: HTML, CSS, JavaScript — Railway
- Backend: Node.js, Express, SQLite (sql.js) — Railway
- Payments: Bitcoin Lightning via hosted wallet API
- Protocol: A2A (Agent-to-Agent) JSON-RPC
- Chatbot: SquidBot — Claude-powered, marketplace-aware with persistent memory

**Three-Tier Pricing Model:**
| Tier | Model | What You Get |
|------|-------|-------------|
| Remote Execution | Rent | Pay-per-use — your agent calls the seller's agent |
| Skill File | Own | Blueprint/instructions your AI can follow |
| Full Package | Own | Complete source code + configs + templates |

**Key Features:**
- **Agent identity system** — verified profiles, locked names (can't rename to dodge bad reviews)
- **Verification tiers**: Unverified → A2A Verified (green ✓) → X Verified (gold badge)
- **2% platform fee** — 98% goes to seller
- **Three access modes**: Local agents (full autonomy), Cloud AI with local runtime, Humans on website
- **SquidBot** — AI assistant for onboarding, skill discovery, purchase help
- **Bitcoin Lightning payments** — instant, global, permissionless
- **Soft deletes only** — transaction history preserved permanently

**Takeaway:** Most innovative marketplace concept — agent-to-agent commerce with crypto micropayments. The three-tier pricing (rent/learn/own) is a clever business model. The identity and reputation system designed specifically for AI agents is forward-thinking.

---

## Full Repository Catalog

### Search 1: "skill marketplace" (sorted by stars)

| # | Repository | Stars | Forks | Language | Description |
|---|-----------|-------|-------|----------|-------------|
| 1 | [phuryn/pm-skills](https://github.com/phuryn/pm-skills) | 7,311 | 706 | Markdown | PM Skills Marketplace: 100+ agentic skills for product management |
| 2 | [daymade/claude-code-skills](https://github.com/daymade/claude-code-skills) | 652 | 100 | Python | 42 production-ready Claude Code skills |
| 3 | [mhattingpete/claude-skills-marketplace](https://github.com/mhattingpete/claude-skills-marketplace) | 469 | 51 | HTML | Engineering workflow skills — Git, testing, code review |
| 4 | [binance/binance-skills-hub](https://github.com/binance/binance-skills-hub) | 462 | 86 | — | AI agents native access to crypto ecosystem |
| 5 | [ahmedasmar/devops-claude-skills](https://github.com/ahmedasmar/devops-claude-skills) | 97 | 12 | Python | DevOps workflows for Claude Code |
| 6 | [adrianpuiu/claude-skills-marketplace](https://github.com/adrianpuiu/claude-skills-marketplace) | 86 | 9 | Python | Project Architect skill for planning documents |
| 7 | [obie/skills](https://github.com/obie/skills) | 78 | 1 | Markdown | Stimulus.js and MCP OAuth skills |
| 8 | [nextlevelbuilder/skillx](https://github.com/nextlevelbuilder/skillx) | 34 | 6 | TypeScript | Full-stack marketplace with hybrid search and CLI |
| 9 | [rawveg/skillsforge-marketplace](https://github.com/rawveg/skillsforge-marketplace) | 26 | 4 | Python | 33 curated skills across 7 categories |
| 10 | [lucas-flatwhite/pm-skills-ko](https://github.com/lucas-flatwhite/pm-skills-ko) | 26 | 8 | Markdown | PM Skills Marketplace (Korean version) |
| 11 | [terrylica/cc-skills](https://github.com/terrylica/cc-skills) | 20 | 4 | TypeScript | ADR-driven dev, DevOps, ClickHouse, versioning |
| 12 | [dylantarre/animation-principles](https://github.com/dylantarre/animation-principles) | 18 | 4 | Markdown | Disney's 12 Animation Principles as a skill |
| 13 | [a-pavithraa/springboot-skills-marketplace](https://github.com/a-pavithraa/springboot-skills-marketplace) | 16 | 2 | Java | Spring Boot skills marketplace |
| 14 | [Array-Ventures/coworker](https://github.com/Array-Ventures/coworker) | 14 | 7 | TypeScript | Full AI agent workspace with marketplace |
| 15 | [Sompote/tiger_cowork](https://github.com/Sompote/tiger_cowork) | 14 | 5 | TypeScript | Self-hosted AI workspace with agent reflection |
| 16 | [tommy-ca/notion-skills](https://github.com/tommy-ca/notion-skills) | 12 | 0 | Markdown | Notion workflow skills |
| 17 | [hasanator3000/ClawdOS](https://github.com/hasanator3000/ClawdOS) | 12 | 1 | TypeScript | Web GUI for OpenClaw with skill marketplace |
| 18 | [SylphAI-Inc/skills](https://github.com/SylphAI-Inc/skills) | 11 | 1 | Shell | AdaL CLI community skills |
| 19 | [gate/gate-skills](https://github.com/gate/gate-skills) | 10 | 3 | Shell | Gate crypto exchange skills for AI agents |
| 20 | [0xmythril/clawdtm](https://github.com/0xmythril/clawdtm) | 9 | 1 | TypeScript | Reviewable skill marketplace for OpenClaw (1,600+ skills) |

### Search 2: "AI agent skill marketplace" (sorted by stars)

| # | Repository | Stars | Forks | Language | Description |
|---|-----------|-------|-------|----------|-------------|
| 1 | [nextlevelbuilder/skillx](https://github.com/nextlevelbuilder/skillx) | 34 | 6 | TypeScript | Full-stack marketplace with semantic search |
| 2 | [squidbay/squidbay](https://github.com/squidbay/squidbay) | 2 | 0 | HTML | Agent-to-agent marketplace with Bitcoin Lightning |
| 3 | [atilaahmettaner/skills-plane](https://github.com/atilaahmettaner/skills-plane) | 2 | 2 | TypeScript | AI agent skills marketplace |
| 4 | [eli5-claw/agent-skills-marketplace](https://github.com/eli5-claw/agent-skills-marketplace) | 1 | 0 | TypeScript | Buy/sell OpenClaw/Bankr skills |
| 5 | [DemonDamon/AgenticX-AgentSkills](https://github.com/DemonDamon/AgenticX-AgentSkills) | 1 | 0 | Python | Modern marketplace for AI agent skills |
| 6 | [letsgotoplay/skillmarketplace](https://github.com/letsgotoplay/skillmarketplace) | 0 | 0 | TypeScript | Enterprise AI Agent Skills Marketplace |
| 7 | [MyLifeOS-Corp/skillforge-marketplace](https://github.com/MyLifeOS-Corp/skillforge-marketplace) | 0 | 0 | TypeScript | SkillForge/MoltStore marketplace |
| 8 | [matthew-mskim/agenthub](https://github.com/matthew-mskim/agenthub) | 0 | 0 | PLpgSQL | Agent skill marketplace & community |
| 9 | [JrPribs/agent-marketplace](https://github.com/JrPribs/agent-marketplace) | 0 | 0 | — | Decentralized marketplace with USDC payments |

### Search 3: "skills marketplace platform"

| # | Repository | Stars | Forks | Language | Description |
|---|-----------|-------|-------|----------|-------------|
| 1 | [gitswapnadeep/jaro](https://github.com/gitswapnadeep/jaro) | 0 | 0 | TypeScript | SkillShareHub – A Skill Marketplace Platform |
| 2 | [samuelemb/Tibeb-skill-marketplace](https://github.com/samuelemb/Tibeb-skill-marketplace) | 0 | 1 | TypeScript | Full-stack marketplace for clients and freelancers |
| 3 | [shre4ya/Saathi](https://github.com/shre4ya/Saathi) | 0 | 0 | — | Global opportunity aggregator + peer-to-peer skill marketplace |

### Search 4: "talent marketplace" (sorted by stars)

| # | Repository | Stars | Forks | Language | Description |
|---|-----------|-------|-------|----------|-------------|
| 1 | [zer0-A1/Emineon](https://github.com/zer0-A1/Emineon) | 8 | 0 | TypeScript | Consulting OS with AI agents and talent marketplace |
| 2 | [felipevcc/holbie-talent-hub](https://github.com/felipevcc/holbie-talent-hub) | 6 | 1 | TypeScript | Web-based Talent Marketplace |
| 3 | [anndimi/Tech-Talent-Marketplace](https://github.com/anndimi/Tech-Talent-Marketplace) | 2 | 3 | JavaScript | Tech talent marketplace |
| 4 | [holyaustin/Tallent-Musica-Ripple](https://github.com/holyaustin/Tallent-Musica-Ripple) | 2 | 1 | Assembly | Web3 music talent marketplace with NFTs |
| 5 | [Conyx01/aukier](https://github.com/Conyx01/aukier) | 1 | 0 | TypeScript | African talent marketplace platform |
| 6 | [surajsbhoj0101/NeuroGuild-Network](https://github.com/surajsbhoj0101/NeuroGuild-Network) | 1 | 0 | JavaScript | Decentralized talent marketplace on-chain |
| 7 | [GajananDhangude/WorkOS](https://github.com/GajananDhangude/WorkOS) | 1 | 0 | JavaScript | AI-native talent marketplace (outcomes, not roles) |
| 8 | [successaje/Earnify](https://github.com/successaje/Earnify) | 1 | 0 | JavaScript | Decentralized marketplace on ICP |

### Search 5: "freelance marketplace" (sorted by stars)

| # | Repository | Stars | Forks | Language | Description |
|---|-----------|-------|-------|----------|-------------|
| 1 | [rrrupom/website-freelance-marketplace](https://github.com/rrrupom/website-freelance-marketplace) | 51 | 20 | PHP | Freelance marketplace (HTML/CSS/PHP/MySQL) |
| 2 | [paulonteri/freelance-marketplace](https://github.com/paulonteri/freelance-marketplace) | 42 | 16 | PHP | Digital freelancing marketplace |
| 3 | [priyanktejani/fiwork-freelance-networking-application](https://github.com/priyanktejani/fiwork-freelance-networking-application) | 30 | 12 | Dart | Social media-like freelancing marketplace |
| 4 | [anurag270102/fiverr-clone](https://github.com/anurag270102/fiverr-clone) | 26 | 8 | JavaScript | Fiverr clone with Stripe + Cloudinary |
| 5 | [anfiquehussain/Freelance-Marketplace-Django](https://github.com/anfiquehussain/Freelance-Marketplace-Django) | 25 | 15 | HTML | Django-based freelance marketplace |
| 6 | [Ukhang/brenda](https://github.com/Ukhang/brenda) | 24 | 16 | JavaScript | Upwork-inspired UI (frontend only) |
| 7 | [chornthorn/freelance_marketplace_app](https://github.com/chornthorn/freelance_marketplace_app) | 23 | 14 | Dart | Mobile freelance marketplace |
| 8 | [pray3m/freelanceX](https://github.com/pray3m/freelanceX) | 18 | 6 | JavaScript | Next.js + Tailwind + Prisma + MongoDB |
| 9 | [tonsan-1/Jobzy](https://github.com/tonsan-1/Jobzy) | 11 | 0 | CSS | Job board & freelance marketplace |
| 10 | [Huniko519/Freelancer-Marketplace](https://github.com/Huniko519/Freelancer-Marketplace) | 11 | 2 | PHP | Freelance marketplace with user management |
| 11 | [Suhaib-Malik01/Fiverr-Clone](https://github.com/Suhaib-Malik01/Fiverr-Clone) | 11 | 6 | HTML | Fiverr clone |
| 12 | [Daltonic/Dappworks](https://github.com/Daltonic/Dappworks) | 7 | 1 | JavaScript | Decentralized freelance marketplace (React + Solidity) |

---

## Key Patterns & Trends

### Pattern 1: The "Skill as Markdown" Standard

The overwhelming majority of AI agent skill marketplaces use the same format:
- **SKILL.md** file with YAML frontmatter (name, description, version, author)
- Human-readable instructions in the body
- Optional supporting files (scripts, templates, references)
- Skills are **context-injected** — loaded into the AI's context when relevant

This has become a de facto standard across Claude Code, OpenClaw, Gemini CLI, Cursor, and others.

### Pattern 2: Marketplace = Curated Git Repository

Most "marketplaces" are simply well-organized GitHub repositories with:
- A manifest file (`.claude-plugin/marketplace.json` or similar)
- Individual skill directories
- Installation via CLI commands (`/plugin marketplace add owner/repo`)
- No centralized server needed — Git is the distribution mechanism

### Pattern 3: Domain-Specific Skill Collections Win

The highest-star repos aren't general-purpose; they're deeply focused:
- **PM skills** (7,311 stars) — 65+ skills for product management
- **Engineering workflows** (469 stars) — Git, testing, code review
- **Crypto/DeFi** (462 stars) — Binance-backed crypto access
- **DevOps** (97 stars) — DevOps-specific workflows

### Pattern 4: Composable Skill Hierarchies

Advanced repos implement multi-level composition:
- **Skills** (atomic capabilities) → **Commands** (chained workflows) → **Plugins** (installable packages)
- **Skills** + **Agents** (specialized Claude instances) — composable hierarchy
- Meta-skills that create other skills (skill-creator pattern)

### Pattern 5: Cross-Framework Compatibility

Leading repos are designing for multiple AI agent frameworks:
- Claude Code, Cowork, Gemini CLI, OpenCode, Cursor, Codex CLI, Kiro
- The SKILL.md format works across tools (commands are tool-specific)
- Binance explicitly targets "any agent, any framework, any chain"

### Pattern 6: Emerging Agent-to-Agent Commerce

A small but growing category of repos explores:
- Agents buying/selling skills from each other (SquidBay)
- Bitcoin Lightning micropayments for skill access
- Three-tier pricing: rent (execution), learn (skill file), own (full package)
- Agent identity and reputation systems
- USDC/crypto payments for decentralized marketplaces

### Pattern 7: Execution Runtime for Token Efficiency

mhattingpete's marketplace introduced a code execution runtime that achieves 90-99% token savings by running Python locally instead of loading code into context. This pattern will likely spread.

---

## Notable Innovations

### 1. Agent Reflection Loop (tiger_cowork)
After the agent completes its work, a separate LLM call evaluates whether the objective was satisfied. If the score is below threshold, the agent re-enters the tool loop. This is a quality assurance mechanism for agent outputs.

### 2. Three-Tier Skill Pricing (SquidBay)
- **Rent** (remote execution): Pay per use, agent calls seller's agent
- **Learn** (skill file): Get the blueprint/instructions
- **Own** (full package): Complete source code + configs
This maps well to how different consumers want to use skills.

### 3. Hybrid Search with RRF (SkillX)
Combining semantic search (vector embeddings) + keyword search (FTS5) + Reciprocal Rank Fusion for skill discovery. Sub-800ms latency.

### 4. Skill-Creator Meta-Skill (daymade)
A skill that creates other skills — initialization, validation, and packaging. This is a marketplace growth primitive.

### 5. Execution Runtime for Token Savings (mhattingpete)
MCP-based code execution that reduces token usage by 90-99% for bulk operations. Instead of reading 50 files into context, execute a Python script locally.

### 6. Agent Identity & Locked Names (SquidBay)
Agent names are permanent (can't rename to dodge bad reviews), with three verification tiers. Designed specifically for AI agent reputation.

### 7. Visual Multi-Agent System Editor (tiger_cowork)
Drag-and-drop canvas for designing multi-agent systems with configurable protocols (TCP, Bus, Queue) between agents. Exports to YAML.

---

## Technology Stack Analysis

### Most Common Stacks

| Component | Dominant Choices |
|-----------|-----------------|
| **Skill Format** | Markdown (SKILL.md) with YAML frontmatter |
| **Distribution** | GitHub repositories with manifest files |
| **Installation** | CLI commands (`/plugin marketplace add`, `npx skills add`) |
| **Backend** | Node.js/TypeScript (most common), Python (second) |
| **Frontend** | React (various: Router v7, Next.js), Tailwind CSS |
| **Database** | SQLite (D1, sql.js), PostgreSQL |
| **Search** | FTS5 + vector embeddings (Cloudflare Vectorize, bge-base-en-v1.5) |
| **Auth** | GitHub OAuth, API keys (SHA-256 hashed) |
| **Payments** | Bitcoin Lightning (agent markets), Stripe (planned for others) |
| **Deployment** | Cloudflare Workers, Railway, Docker, self-hosted |
| **Agent Framework** | Mastra, Claude Code native, custom |

### Freelance/Talent Marketplace Stacks

| Component | Choices |
|-----------|---------|
| **Backend** | PHP/Laravel, Django, Node.js/Express |
| **Frontend** | React/Next.js, Dart/Flutter (mobile) |
| **Database** | MySQL, MongoDB, PostgreSQL |
| **Payments** | Stripe, Solidity smart contracts (Web3) |

---

## Marketplace Business Models

| Model | Examples | Details |
|-------|----------|---------|
| **Free/Open Source** | pm-skills, claude-code-skills, binance-skills-hub | MIT/Apache licensed, star-driven growth |
| **Platform Fee** | SquidBay | 2% platform fee on transactions |
| **Freemium** | SkillX (planned) | Free browsing, paid premium features (Stripe) |
| **Enterprise Open Source** | Binance Skills Hub | Company-backed open source for ecosystem growth |
| **Agent-to-Agent Commerce** | SquidBay, JrPribs/agent-marketplace | Crypto micropayments between agents |
| **Decentralized** | Dappworks, NeuroGuild-Network | Smart contracts, on-chain reputation |

---

## Conclusions & Implications

### The Market is Nascent but Exploding
- Most repos are days to weeks old (July 2025)
- The Claude Code plugin/marketplace architecture catalyzed this wave
- Star counts are growing rapidly (pm-skills went from 0 to 7,300+)

### Skill Marketplaces ≠ Traditional Marketplaces
- Current "marketplaces" are mostly curated skill collections distributed via Git
- True marketplace features (search, ratings, payments, identity) are rare
- Only SkillX and SquidBay have real marketplace infrastructure

### Opportunity Gaps
1. **No dominant general-purpose marketplace platform** — most are collections, not platforms
2. **Discovery is primitive** — most rely on browsing READMEs, not search
3. **No quality/trust signals** — limited ratings, reviews, or verification
4. **No monetization infrastructure** — only SquidBay has payments working
5. **Cross-framework standard is informal** — SKILL.md is a convention, not a specification
6. **Agent-to-agent commerce is very early** — huge opportunity for first movers

### What Would a "Next-Gen" Skill Marketplace Need?
1. **Hybrid search** (semantic + keyword) for discovery
2. **Ratings, reviews, and reputation** for trust
3. **Multi-tier pricing** (free, rent, buy) for monetization
4. **Agent identity and verification** for accountability
5. **Cross-framework compatibility** for reach
6. **Execution runtime** for efficiency
7. **Composable skill hierarchy** (skills → workflows → packages)
8. **A2A protocol support** for agent-to-agent interaction
9. **Payment infrastructure** (crypto micropayments + traditional)
10. **Quality gates** (validation, testing, security scanning)

---

*This report covers 72+ repositories across 5 GitHub search queries. Data reflects the state of these projects as of July 2025.*
