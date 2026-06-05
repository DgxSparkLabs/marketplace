# GitHub Findings — AI Agent Skill Marketplaces

## Official Vendor Skill Catalogs

### anthropics/skills (75,600 stars per ArXiv citation)

- Official Anthropic skills repo for Claude Code
- Format: SKILL.md with YAML frontmatter (name + description)
- License: Apache 2.0 (example skills), Source-available (document skills)
- Skills include: algorithmic-art, brand-guidelines, canvas-design, docx, pdf, pptx, xlsx, music-production, svg-design, test-web-app, mcp-server-generator, communications, skill-creator, template
- Install: `/plugin marketplace add anthropics/skills`
- Document skills (docx, pdf, pptx, xlsx) power Claude's native document creation features
- Partner skills section — Notion already has official Claude skills
- Skills are self-contained with SKILL.md + optional templates/, references/, scripts/

### openai/skills (Codex Skills Catalog)

- Format: SKILL.md + optional agents/openai.yaml
- Tiers: .system/ (built-in), .curated/, .experimental/
- Install: `$skill-installer <name>` in Codex
- Scopes: REPO (.agents/skills/), USER (~/.agents/skills/), ADMIN (/etc/codex/skills/), SYSTEM
- Progressive disclosure: Codex reads only name+description initially, loads full SKILL.md only when needed
- Implicit invocation: Skills auto-activate when user prompt matches description
- agents/openai.yaml supports: display_name, icon_small/large, brand_color, default_prompt, allow_implicit_invocation, MCP tool dependencies
- Config: ~/.codex/config.toml with [[skills.config]] entries

### MicrosoftDocs/Agent-Skills

- "Curated Agent Skills for Microsoft & Azure"
- Gives AI coding assistants structured, real-time expertise from Microsoft Learn docs
- Pre-compiles documentation knowledge into actions, choices, and guardrails
- Works with: Claude Code, Gemini CLI, Codex CLI, Antigravity IDE, GitHub Copilot, Cursor, OpenCode, AdaL CLI
- Uses progressive disclosure (3 levels: Discovery, Instructions, Resources)
- Includes skills for: Azure Functions, Container Apps, API Management, Cosmos DB, etc.

### google-labs-code/stitch-skills

- Skills designed for the Stitch MCP server
- Follows Agent Skills open standard
- Skills: stitch-design, stitch-loop, design-md, enhance-prompt, react:components, remotion, shadcn-ui
- Install: `npx skills add google-labs-code/stitch-skills --skill <name>`
- Standardized structure: SKILL.md + scripts/ + resources/ + examples/

### block/agent-skills (Block/Square)

- "A marketplace for agent skills" maintained by Block
- Portable across agents (Goose, Claude Desktop, others)
- Install: `npx skills add https://github.com/block/Agent-Skills --skill api-setup`
- Web marketplace at block.github.io/goose/skills
- Required frontmatter: name, description, author, version, tags
- Has automated skills validator for PRs

### openclaw/clawhub

- Public skill registry for Clawdbot/OpenClaw
- Features: browse, publish, version, search text-based agent skills
- Vector search via OpenAI embeddings (text-embedding-3-small)
- CLI: clawhub login, search, install, uninstall, publish, sync
- onlycrabs.ai is the SOUL.md registry (system lore)
- GitHub OAuth auth, Convex backend
- VirusTotal scanning for published skills since Feb 2026

### Vendor Catalog Comparison

| Vendor | Repo | Format | Install Method | Progressive Disclosure | License |
|---|---|---|---|---|---|
| Anthropic | anthropics/skills | SKILL.md + YAML frontmatter | `/plugin marketplace add` | — | Apache 2.0 / Source-available |
| OpenAI | openai/skills | SKILL.md + agents/openai.yaml | `$skill-installer <name>` | Yes (name+desc first) | — |
| Microsoft | MicrosoftDocs/Agent-Skills | Agent Skills standard | Manual / multi-agent | Yes (3 levels) | — |
| Google | google-labs-code/stitch-skills | SKILL.md + scripts/resources/examples | `npx skills add` | — | — |
| Block | block/agent-skills | SKILL.md + frontmatter | `npx skills add` | — | — |
| OpenClaw | openclaw/clawhub | Text-based skills | `clawhub install` | — | — |

---

## Major Community Collections

### VoltAgent/awesome-agent-skills (500+ skills)

- "Claude Code Skills and 500+ agent skills from official dev teams and the community"
- Features official skills from: Anthropic, Google Labs, Vercel, Stripe, Cloudflare, Netlify, Trail of Bits, Sentry, Expo, Hugging Face, Supabase, Hashicorp, Sanity, Firecrawl, Neon, ClickHouse, Remotion, Replicate, Typefully, Better Auth, Tinybird, ComposioHQ
- Also has VoltAgent's own skills for their TypeScript agent framework
- Compatible with Claude Code, Codex, Antigravity, Gemini CLI, Cursor, GitHub Copilot, OpenCode, Windsurf
- Curated, not mass-generated. Emphasizes "real-world Agent Skills created by actual engineering teams"
- Security warning: "Agent skills can include prompt injections, tool poisoning, hidden malware payloads"

### tech-leads-club/agent-skills

- "The secure, validated skill registry for professional AI coding agents"
- Key claim: "In an ecosystem where over 13% of marketplace skills contain critical vulnerabilities"
- Security: 100% open source, static analysis in CI/CD, immutable integrity via lockfiles and content hashing, human-curated prompts, Snyk Agent Scan before publishing
- Interactive CLI wizard: `npx @tech-leads-club/agent-skills`
- Supports 18+ agents across 3 tiers (Popular, Rising, Enterprise)
- Has MCP server built-in
- Featured skills: tlc-spec-driven, aws-advisor, playwright-skill, figma, security-best-practices

### latestaiagents/agent-skills

- 67 professional skills + 7 full-featured plugins
- Organized by audience: Safety, Developer, DevOps/SRE, RAG Engineer, Security, QA/Testing, HR
- Works with Claude Code, Claude Cowork, Cursor, Codex, Windsurf, and 35+ other agents
- Safety skills category includes: destructive-operation-guard, migration-safety, database-safety, file-operation-safety, git-safety

### Community Collection Comparison

| Collection | Scale | Focus | Security Posture | Agent Compatibility |
|---|---|---|---|---|
| VoltAgent/awesome-agent-skills | 500+ skills | Official dev team skills | Warning only | 8+ agents |
| tech-leads-club/agent-skills | Curated registry | Enterprise/professional | Static analysis, Snyk, lockfiles, content hashing | 18+ agents (3 tiers) |
| latestaiagents/agent-skills | 67 skills + 7 plugins | Role-based categories | Safety skills category | 35+ agents |
| agent-skills-hub/agent-skills-hub | 790+ skills | Universal registry | — | — |

### Other Notable Collections

- **heilcheng/awesome-agent-skills** — curated list of skills/tools/tutorials
- **skillmatic-ai/awesome-agent-skills** — "The definitive" collection, modular SKILL.md packages
- **philipbankier/awesome-agent-skills** — cross-platform directory covering ALL agent skill ecosystems
- **BehiSecc/awesome-claude-skills** — curated Claude skills including Playwright
- **agent-skills-hub/agent-skills-hub** — 790+ skills universal registry
- **xiaoqiangkx/agent-skills-catalog** — curated directory with official skills from Anthropic, Vercel, Cloudflare, Stripe, HuggingFace, Trail of Bits
- **ZhanlinCui/Agent-Skills-Hunter** — "Ultimate Agent Skills Collection"
- **dmgrok/agent_skills_directory** — with LGTM validation, gitleaks secret scanning, prompt injection checks
- **numman-ali/n-skills** — "Curated plugin marketplace for AI agents", notes AGENTS.md adopted by 20,000+ repos
- **callstackincubator/agent-skills** — React Native agent skills
- **jabrena/cursor-rules-java** — Java-specific cursor rules + skills
- **FrancyJGLisboa/agent-skill-creator** — "Turn any workflow into reusable AI agent skills that install on 14+ tools"

---

## Auto-Generation Projects

- **Arasoai/daily-2026-skills** (a.k.a. trending-skills): GitHub Actions cron runs every 15 minutes, fetches trending repos, uses Claude Sonnet to generate SKILL.md, publishes to skills.sh
- **VoltAgent/awesome-openclaw-skills**: Curated list of OpenClaw skills, 13,729 community-built skills in ClawHub as of Feb 28 2026

---

## Security-Focused Projects

- **adibirzu/openclaw-security-monitor**: Found 12% of ClawHub skills were malicious (341 of 2,857)
- **prompt-security/clawsec**: Security skill suite for OpenClaw's agents, SOUL.md drift detection
- **knownsec/openclaw-security**: Security guide, 63,026 identifiable OpenClaw instances worldwide
- **centminmod/explain-openclaw**: Documents marketplace risks, automated vetting via VirusTotal

### Security Statistics

| Source | Finding |
|---|---|
| adibirzu/openclaw-security-monitor | 12% of ClawHub skills malicious (341 / 2,857) |
| tech-leads-club/agent-skills | 13%+ of marketplace skills contain critical vulnerabilities |
| knownsec/openclaw-security | 63,026 identifiable OpenClaw instances worldwide |
| openclaw/clawhub | VirusTotal scanning since Feb 2026 |

---

## Marketplace Infrastructure

- **aiskillstore/marketplace**: "The official AI Skills marketplace for Claude Code and Codex"
- **nibzard/skills-marketplace**: "Centralized platform for distributing and discovering Agent Skills"
- **DaimaRuge/Skill-Marketplace**: "AI Agent Skills Trading Platform Business Plan"

---

## Business Models (from GitHub Gist)

A gist (ryudi84) documents "AI Agent Business Models That Actually Make Money in 2026":

- **Skill Marketplace Sales**: Publish skills on ClawHub/ClawMart, 3,286+ skills listed, free to publish, revenue from premium skills
- **API Services via x402 Protocol**: Build APIs that other AI agents pay to use
