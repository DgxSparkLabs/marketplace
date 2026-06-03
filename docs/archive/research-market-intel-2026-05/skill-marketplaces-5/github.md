# GitHub Findings: Skill Marketplaces

> Searched: March 16, 2026
> Queries: "skill marketplace", "skills marketplace platform", "AI agent skill marketplace", "talent marketplace", "freelance marketplace open source"
> Total unique repos found: 60+

## Category 1: AI Agent Skill Marketplaces (Claude Code / OpenClaw Ecosystem)

This is by far the **dominant category** on GitHub right now. The Claude Code skills ecosystem has exploded.

### Top Repos by Stars

| # | Repo | Stars | Forks | Lang | Description |
|---|------|-------|-------|------|-------------|
| 1 | **phuryn/pm-skills** | 7,311 | 706 | - | PM Skills Marketplace: 100+ agentic skills, commands, and plugins — discovery to strategy, execution, launch, growth |
| 2 | **daymade/claude-code-skills** | 652 | 100 | Python | Professional Claude Code skills marketplace with production-ready skills |
| 3 | **mhattingpete/claude-skills-marketplace** | 469 | 51 | HTML | Claude Code Skills for SE workflows — Git automation, testing, code review |
| 4 | **binance/binance-skills-hub** | 462 | 86 | - | Open skills marketplace giving AI agents native access to crypto |
| 5 | **ahmedasmar/devops-claude-skills** | 97 | 12 | Python | Claude Code Skills Marketplace for DevOps workflows |
| 6 | **adrianpuiu/claude-skills-marketplace** | 86 | 9 | Python | Project Architect skill for detailed AI-assisted development planning |
| 7 | **obie/skills** | 78 | 1 | - | Claude Code skills marketplace — production-ready enhanced dev workflows |
| 8 | **nextlevelbuilder/skillx** | 34 | 6 | TypeScript | SkillX.sh — AI agent skills marketplace with semantic search, leaderboard, ratings, CLI |
| 9 | **rawveg/skillsforge-marketplace** | 26 | 4 | Python | A Claude Code Marketplace |
| 10 | **lucas-flatwhite/pm-skills-ko** | 26 | 8 | - | PM Skills Marketplace Korean Version |
| 11 | **terrylica/cc-skills** | 20 | 4 | TypeScript | ADR-driven development, DevOps automation, ClickHouse, semantic versioning |
| 12 | **dylantarre/animation-principles** | 18 | 4 | - | Disney's 12 Animation Principles — Claude Code Skill Marketplace |
| 13 | **tommy-ca/notion-skills** | 12 | - | - | Claude Skills for Notion workflows |
| 14 | **hasanator3000/ClawdOS** | 12 | 1 | TypeScript | Web GUI for OpenClaw (237K+ stars) — skill marketplace |
| 15 | **SylphAI-Inc/skills** | 11 | 1 | Shell | AdaL Skills Marketplace — community-shareable skills for AdaL CLI |
| 16 | **gate/gate-skills** | 10 | 3 | Shell | Gate Skills — AI agents with native access to Gate crypto ecosystem |
| 17 | **0xmythril/clawdtm** | 9 | 1 | TypeScript | Reviewable skill marketplace for OpenClaw agents. 1,600+ skills with ratings |

### AI Agent Marketplace Platforms (Smaller/Emerging)

| Repo | Lang | Description |
|------|------|-------------|
| **Array-Ventures/coworker** | TypeScript | Open-source AI agent with MCP UI, A2A protocol, skills marketplace. Built with Mastra |
| **Sompote/tiger_cowork** | TypeScript | Self-hosted AI workspace with skill marketplace. Any OpenAI-compatible API |
| **squidbay/squidbay** | HTML | AI agent skill marketplace — agents buy/sell capabilities using Bitcoin Lightning |
| **eli5-claw/agent-skills-marketplace** | TypeScript | Buy and sell OpenClaw/Bankr skills |
| **DemonDamon/AgenticX-AgentSkills** | Python | Modern marketplace for discovering, downloading, deploying AI agent skills |
| **letsgotoplay/skillmarketplace** | TypeScript | Enterprise AI Agent Skills Marketplace |
| **MyLifeOS-Corp/skillforge-marketplace** | TypeScript | SkillForge/MoltStore — AI Agent Skills Marketplace |
| **matthew-mskim/agenthub** | PLpgSQL | AI Agent Skill Marketplace & Collaboration Community |
| **atilaahmettaner/skills-plane** | TypeScript | AI agent skills marketplace |

## Category 2: Talent / Freelance Marketplaces

| Repo | Stars | Lang | Description |
|------|-------|------|-------------|
| **zer0-A1/Emineon** | 8 | TypeScript | Consulting OS — AI agents for skill-matching, workflow management, talent marketplace |
| **felipevcc/holbie-talent-hub** | 6 | TypeScript | Web app for Talent Marketplace |
| **anndimi/Tech-Talent-Marketplace** | 2 | JavaScript | Tech talent marketplace |
| **holyaustin/Tallent-Musica-Ripple** | 2 | Assembly | Web3 DApp — music talent NFT marketplace on Ripple |

## Category 3: Enterprise Governance & Infrastructure

| Repo | Stars | Description |
|------|-------|-------------|
| **microsoft/agent-governance-toolkit** | 6,100+ tests | OWASP 10/10, Python/TS/.NET governance for AI agents |
| **microsoft/skills** | - | 132 enterprise skills for Azure SDKs across 6 languages |
| **reflectt/agent-identity-governance-kit** | - | Crypto identity + RBAC, SOC 2/GDPR/HIPAA |
| **dash0hq/agent-skills** | - | OpenTelemetry observability skills across 8 languages |
| **BulloRosso/etienne** | - | Enterprise harness — RBAC, skill catalog curation |
| **mukul975/Anthropic-Cybersecurity-Skills** | - | 611+ cybersecurity skills, MITRE ATT&CK mapped |
| **a-pavithraa/springboot-skills-marketplace** | 16 | Java/Spring Boot skills marketplace |

## Key Patterns Observed

### 1. Claude Code Skills Domination
The overwhelming majority of "skill marketplace" repos on GitHub (March 2026) are Claude Code / OpenClaw skill collections. The SKILL.md format has become a de-facto standard.

### 2. Crypto/Web3 Integration
Multiple repos explore crypto-based agent economies:
- **Binance** and **Gate** both have official skill hubs
- **squidbay** uses Bitcoin Lightning for agent-to-agent skill trading
- **Tallent-Musica-Ripple** uses NFTs for talent marketplace

### 3. Domain Specialization
Vertical skill collections are emerging:
- DevOps (ahmedasmar)
- Cybersecurity/MITRE ATT&CK (mukul975, 611+ skills)
- Notion workflows (tommy-ca)
- Animation principles (dylantarre)
- Protein Design (mentioned on X)

### 4. Enterprise Infrastructure Layer
Microsoft leads with governance toolkit (6,100+ tests, OWASP compliance). Enterprise adoption requires runtime governance, not application-level controls.

### 5. Tech Stack Convergence
- **TypeScript** is the dominant language for marketplace platforms
- **Python** dominates for individual skills
- **SKILL.md** is the de-facto skill description format
- **MCP** (Model Context Protocol) integration is standard
