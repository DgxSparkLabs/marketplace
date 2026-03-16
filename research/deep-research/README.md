# AI Agent Skill Marketplace — Deep Cross-Platform Research

*Date: 2026-03-16 | Sources: GitHub, Twitter/X, Reddit, ArXiv, Kaggle*

---

## 1. Executive Summary

The AI agent skill marketplace space has **exploded** in Q1 2026. What was a niche
concern of Cursor rule-sharers six months ago is now an ecosystem with:

- **Two official standards** — OpenAI (`openai/skills`) and Anthropic (`anthropics/skills`) both use `SKILL.md`
- **Academic security research** — ArXiv papers already document 157 confirmed malicious skills across 98K analyzed
- **A dozen+ web marketplaces** — SkillsGate (60K+), SkillzWave (42K+), SkillsMP (400K+), SkillHub (7K+), Agensi, etc.
- **Enterprise entry** — AWS Marketplace now lists AI agents/tools, Binance launched 7 Agent Skills, Salesforce launched an Agent Skills marketplace
- **Crypto/Web3 angle** — SafuSkill (BNB Chain), $SKILL token on Solana, agent-to-agent skill trading
- **Active academic study** — Supply chain security frameworks, automated skill mining, and agent registry surveys

Our marketplace is **architecturally well-positioned** (dual skills+rules, cross-platform installers, test suite) but the window to differentiate is closing fast as the ecosystem standardizes around SKILL.md.

---

## 2. GitHub Findings

### 2.1 Official Skill Catalogs (NEW since previous research)

#### anthropics/skills — Anthropic's Official Skills Repository

| Attribute | Value |
|---|---|
| URL | github.com/anthropics/skills |
| Stars | 75,600 (per ArXiv paper citation) |
| Format | **SKILL.md** (YAML frontmatter: name + description) |
| License | Apache 2.0 (example skills), Source-available (document skills) |
| Skills | algorithmic-art, brand-guidelines, canvas-design, docx, pdf, pptx, xlsx, music-production, svg-design, test-web-app, mcp-server-generator, communications, and more |
| Installation | Claude Code plugin: `/plugin marketplace add anthropics/skills` |
| Available in | Claude Code, Claude.ai, Claude API |

**Key insights:**
- Document skills (docx, pdf, pptx, xlsx) power Claude's native document creation features
- Plugin marketplace system: `/plugin install document-skills@anthropic-agent-skills`
- Skills are self-contained with `SKILL.md` + optional `templates/`, `references/`, `scripts/`
- Partner skills section — Notion already has official Claude skills

#### openai/skills — OpenAI's Codex Skills Catalog

| Attribute | Value |
|---|---|
| URL | github.com/openai/skills |
| Format | **SKILL.md** + optional `agents/openai.yaml` |
| Tiers | `.system/` (built-in), `.curated/`, `.experimental/` |
| Install | `$skill-installer <name>` in Codex |
| Scopes | REPO (.agents/skills/), USER (~/.agents/skills/), ADMIN (/etc/codex/skills/), SYSTEM |

**Key details from developer docs (scraped):**
- **Progressive disclosure**: Codex reads only name+description initially, loads full SKILL.md only when needed
- **Implicit invocation**: Skills auto-activate when user prompt matches description
- **agents/openai.yaml** supports: `display_name`, `icon_small/large`, `brand_color`, `default_prompt`, `allow_implicit_invocation`, and MCP tool dependencies
- **Skill scopes** — repo-level, user-level, admin-level, and system-level (similar to our global vs project install)
- **Config** — `~/.codex/config.toml` with `[[skills.config]]` entries to enable/disable skills

### 2.2 New Web Marketplace Projects

#### SkillsGate (skillsgate.ai) — 60K+ skills

| Attribute | Value |
|---|---|
| CLI | `npm install -g skillsgate` / `npx skillsgate search "query"` |
| Agents | 17 agents: Claude Code, Cursor, Windsurf, GitHub Copilot, Codex CLI, Cline, Continue, Amp, Goose |
| Key feature | **Security scanning** — `skillsgate scan @vercel/v0` uses your own AI agent to analyze skills for threats |
| MCP | Auto-configures MCP for Claude Code, Cursor, Windsurf |
| Trust | Verified publishers, crowd-sourced scan results |

**Most interesting new player.** The security-first approach (crowd-sourced vulnerability scanning via MCP) is a differentiator nobody else has.

#### SkillHub (skillhub.club) — 7K+ skills

| Attribute | Value |
|---|---|
| CLI | `npx @skill-hub/cli install <name>` |
| Key feature | **5-dimension AI evaluation** (Practicality, Clarity, Automation, Quality, Impact) |
| Ratings | S-rank (9.0+), A-rank (8.0+) system |
| Curated stacks | "OSS Investment Scorecard", "Solopreneur Toolkit", "NIW Petition Suite" |
| Agents | Claude Code, Codex, Gemini CLI, OpenCode, Cursor, Windsurf, Cline, Roo Code, etc. |

**Unique angle:** Pre-configured "Skill Stacks" (curated combinations for workflows) and AI-powered quality evaluation.

#### Agensi (agensi.io) — SKILL.md marketplace with security focus

Found via Reddit. Features security vulnerability scanning for skill files.

#### Claude Marketplaces ecosystem

Multiple sites have emerged:
- **claudemarketplaces.com** — Plugins, skills, tools directory
- **claude-plugins.dev** — Auto-indexes all public GitHub skills

---

## 3. Twitter/X Findings

### 3.1 Key Signals

**Skill marketplace as category is being recognized:**
- @dani_avila7: *"The Skills ecosystem is growing fast, and new marketplaces / registries are already emerging"*
- @singularityhack: *"Introducing SkillShop: The Skill Marketplace for Agents. AI skills are the new apps."*
- @betashop: *"Skills are the unlock. MCPs give agents tools. Skills give agents expertise."*

**Enterprise/crypto adoption:**
- **Binance** launched 7 AI Agent Skills for market analysis, risk assessment, trade execution
- **Pantheon Store** — 1,300+ biomedical AI agent skills (domain-specific marketplace)
- **SafuSkill** (BNB Chain) — security-first marketplace with GoPlus scanning
- **$SKILL token** on Solana — tokenized AI agent capabilities
- **TermiX** building "Skills Market" + "Claw Market" for agent strategies/tools
- **TutuoAI** — Browse-select-install agent skills marketplace

**Key insight from Twitter:** The narrative is shifting from "cursor rules" to "agent skills as the new app store." Multiple crypto projects are trying to financialize this.

### 3.2 Notable Threads

- @Xiaojie_Qiu: Pantheon Store launched with 1,300+ curated bio/medical AI skills — shows domain-specific skill marketplaces emerging
- @BNBCHAIN: SafuSkill as "security-first marketplace" — security scanning is becoming table stakes

---

## 4. Reddit Findings

### 4.1 Key Threads

**"Claude Skills are just .cursorrules, change my mind"** (r/ClaudeAI)
- Community debate on whether skills are just a rebranding of cursor rules
- Consensus: skills add structured metadata (name, description, triggers) and progressive disclosure that .cursorrules lacks

**"I indexed 45k AI agent skills into an open source marketplace"** (r/CLine, r/ClaudeAI, r/buildinpublic)
- SkillsGate launch posts — cross-posted to 4+ subreddits
- One-command install: `npx skillsgate add @username/skill-name`
- Community response: moderate interest, questions about quality control

**"I built a SKILL.md marketplace"** (r/AgentsOfAI)
- Agensi.io launch post
- Community asked about security vulnerability definitions
- Low engagement (5 comments) — marketplace fatigue starting to set in?

**"Agent Skills: The Open Standard for Custom AI Capabilities"** (r/cursor)
- Announcement of Agent Skills in Cursor
- Comments reference it working like the .cursor/rules system but more structured

**"Week 3 of building a marketplace for AI agent skills"** (r/buildinpublic)
- Build-in-public post about marketplace development
- Key feature: "automated scanner that checks every uploaded skill for malicious patterns — 8 checks including dangerous commands"
- Shows security scanning is considered essential

### 4.2 Reddit Sentiment Summary

- **Skills ≠ rules** is emerging as consensus — skills have metadata, progressive loading, and cross-agent portability
- **Security is the #1 concern** — multiple posts about malicious skills, scanner tools
- **Marketplace fatigue** — many "I built a marketplace" posts with decreasing engagement
- **Quality > quantity** — skepticism about 45K+ skill counts, preference for curated sets

---

## 5. ArXiv Findings — Academic Research

### 5.1 "Malicious Agent Skills in the Wild" (2602.06547, Feb 2026)

**Authors:** Liu Yi et al.

**Key findings:**
- Analyzed **98,380 skills** from two community registries
- Confirmed **157 malicious skills** with **632 vulnerabilities**
- Average malicious skill: **4.03 vulnerabilities** across 3 kill chain phases
- Two archetypes: **Data Thieves** (credential exfiltration) and **Agent Hijackers** (instruction manipulation)
- **Single actor** responsible for 54.1% of cases via templated brand impersonation
- **Shadow features** (undocumented capabilities) appear in 100% of advanced attacks
- Some skills exploit the platform's own hook system and permission flags
- Responsible disclosure → 93.6% removal within 30 days

**Implication for us:** Our `allowed-tools` permission model and test suite provide some protection, but the ecosystem needs formal security analysis.

### 5.2 "Formal Analysis and Supply Chain Security for Agentic AI Skills" (2603.00195, Feb 2026)

**Authors:** Bhardwaj, Varun Pratap

**Key findings:**
- OpenClaw marketplace: **228,000 GitHub stars** — massive adoption
- Anthropic Agent Skills: **75,600 stars**
- **ClawHavoc campaign** (Jan-Feb 2026): infiltrated **1,200+ malicious skills** into OpenClaw
- **MalTool** catalogued **6,487 malicious tools** evading conventional detection
- **12 reactive security tools** emerged — all heuristic, no formal guarantees
- Proposes **SkillFortify**: formal analysis framework achieving 96.95% F1, 100% precision
- Introduces: Dolev-Yao skill attacker model, capability-based sandboxing, trust score algebra

**Implication for us:** Supply chain attacks on skill ecosystems are already happening at scale. Formal verification is the next frontier.

### 5.3 "Automating Skill Acquisition through Large-Scale Mining" (2603.11808, Mar 2026)

**Authors:** Bi Shuzhen et al.

**Key findings:**
- Framework for **automated extraction of skills from GitHub repositories**
- Translates extracted capabilities to **standardized SKILL.md format**
- Focuses on visualization/education skills (Manim engine)
- Achieves **40% gains in knowledge transfer efficiency** vs. human-crafted tutorials
- Method: repository structural analysis → semantic skill identification → SKILL.md translation

**Implication for us:** Automated skill mining is a viable scaling strategy. This paper validates the approach used by awesome-cursor-rules-mdc.

### 5.4 "A Survey of AI Agent Registry Solutions" (2508.03095, Aug 2025, v3 Oct 2025)

**Authors:** Singh Aditi et al. (including Ramesh Raskar, MIT)

**Key findings:**
- Compares 5 registry approaches:
  1. **MCP Registry** — centralized mcp.json descriptors
  2. **A2A Agent Cards** — decentralized JSON capability manifests
  3. **AGNTCY Agent Directory** — IPFS DHT + OCI artifacts + Sigstore integrity
  4. **Microsoft Entra Agent ID** — enterprise SaaS + zero-trust
  5. **NANDA Index AgentFacts** — cryptographically verifiable, privacy-preserving
- Evaluated on: security, authentication, scalability, maintainability
- Concludes: need for verifiable identity, adaptive discovery, interoperable capability semantics

**Implication for us:** Agent registries are a solved academic problem with multiple competing standards. Our simple git-based approach is at the "centralized" end of the spectrum.

### 5.5 "Agent Skills Enable Trivially Simple Prompt Injections" (2510.26328)

**Key finding:** Agent Skills files are fundamentally insecure — malicious instructions can be hidden in long SKILL.md files and referenced scripts to exfiltrate sensitive data.

**Implication for us:** Our `allowed-tools` restrictions and minimal skill footprint are defensive advantages.

---

## 6. Kaggle Findings

### 6.1 Kaggle's 5-Day AI Agents Intensive Course (with Google)

Google and Kaggle ran a major course covering:
- Day 1: Introduction to AI agents
- Day 2: Agent Tools & MCP interoperability
- Capstone: Multi-agent systems with LLM, MCP tools, sessions

**Key quote:** *"AI Agent = LLM (Brain) + Tools (Hands)"*

### 6.2 Berkeley Gorilla Agent Marketplace (scraped)

UC Berkeley's Gorilla project built an **open-source search engine for LLM agents**:
- 150+ certified agents from Langchain, LlamaIndex, OpenAI, CrewAI
- Unified interface with user reviews
- Categories: Communication, Finance, Data, AI
- Forum for community discussion
- Agent validation progress bar

**Implication:** Academic research teams are building agent marketplaces as research infrastructure, not just commercial products.

### 6.3 AWS Marketplace — AI Agents and Tools (July 2025)

AWS Marketplace now offers AI agents and tools from AWS Partners:
- Streamlined procurement
- Multiple deployment options
- Third-party AI agent solutions

**Implication:** Enterprise cloud providers are adding "AI agents" as a marketplace category alongside traditional software.

---

## 7. Ecosystem Map (Complete)

### Official Standards & Catalogs

| Platform | Skills | Format | Install | Stars/Scale |
|---|---|---|---|---|
| **OpenAI Codex** | openai/skills | SKILL.md + agents/openai.yaml | `$skill-installer` | Codex-native |
| **Anthropic Claude** | anthropics/skills | SKILL.md | `/plugin marketplace add` | 75.6K stars |
| **agentskills.io** | Open standard | SKILL.md spec | N/A | Industry standard |

### Web Marketplaces

| Platform | Skills | Agents | Key Feature |
|---|---|---|---|
| **SkillsGate** | 60,000+ | 17 | Security scanning via MCP |
| **SkillsMP** | 400,000+ | 3+ | Mass aggregation |
| **SkillzWave** | 42,645+ | 22+ | ML quality scores, enterprise packages |
| **SkillHub** | 7,000+ | 9+ | 5-dimension AI evaluation, Skill Stacks |
| **skills.sh** | Directory | Many | Leaderboard by installs |
| **cursor.directory** | 5,000+ | Cursor | Community + web browsing |
| **Cursor Marketplace** | 50+ plugins | Cursor | Official, integrated in IDE |
| **Agensi** | Growing | Multiple | Security vulnerability scanning |
| **claude-plugins.dev** | Auto-indexed | Claude | Auto-indexes all public GitHub skills |

### Crypto/Web3 Marketplaces

| Platform | Chain | Concept |
|---|---|---|
| **SafuSkill** | BNB Chain | Security-first, GoPlus scanning |
| **$SKILL token** | Solana | Tokenized agent capabilities |
| **TermiX** | — | Skills Market + Claw Market |
| **SquidBay** | Bitcoin Lightning | Agent-to-agent skill trading |

### GitHub Collections

| Repo | Stars | Format | Key Feature |
|---|---|---|---|
| awesome-cursorrules | 38,481 | .cursorrules | Massive community |
| devin.cursorrules | 5,961 | .cursorrules | Agentic workflow |
| awesome-cursor-rules-mdc | 3,378 | .mdc | Auto-generation via LLM |
| agentic-cursorrules | 646 | .cursorrules | Multi-agent partitioning |
| cursor-security-rules | 367 | .cursor/rules/ | Security guardrails |
| task-magic | 242 | .cursor/rules/ | Task management system |

### Academic Research

| Paper | Date | Key Finding |
|---|---|---|
| Malicious Skills in the Wild | Feb 2026 | 157 malicious / 98K analyzed, two attack archetypes |
| Supply Chain Security (SkillFortify) | Feb 2026 | 1,200+ malicious skills in ClawHavoc campaign |
| Automating Skill Acquisition | Mar 2026 | GitHub mining → SKILL.md, 40% efficiency gain |
| Agent Registry Survey | Oct 2025 | 5 registry architectures compared |
| Prompt Injection via Skills | Oct 2025 | Skills enable trivially simple data exfiltration |

---

## 8. Key Trends

### 8.1 SKILL.md is the standard — period
Both OpenAI and Anthropic use it. Every web marketplace indexes it. The open standard at agentskills.io defines it. No other format matters for portable skills.

### 8.2 Security is the #1 problem
- 157 confirmed malicious skills in the wild (ArXiv)
- 1,200+ in ClawHavoc campaign
- 6,487 malicious tools catalogued by MalTool
- SkillsGate, SafuSkill, and SkillFortify all focused on security scanning
- Reddit community consistently asks about security first

### 8.3 Marketplace saturation is real
At least 10+ web marketplaces launched in <6 months. Content is largely the same (auto-indexed from GitHub). Differentiation is shifting from "how many skills" to "how safe and how curated."

### 8.4 Quality scoring is differentiating
SkillHub's 5-dimension AI evaluation, SkillzWave's ML quality scores, and SkillsGate's crowd-sourced security scans show that raw indexing is table stakes — quality/safety signals are the value add.

### 8.5 Enterprise is arriving
AWS Marketplace, Binance, Salesforce, and domain-specific marketplaces (Pantheon for biomedical) show enterprise adoption is starting.

### 8.6 Crypto is trying to financialize skills
$SKILL token, SafuSkill on BNB Chain, SquidBay on Lightning — the crypto world sees agent skills as a new asset class. Early and speculative, but watch this space.

---

## 9. Conclusions for Our Marketplace

### What we do that's unique:

1. **Dual content types** (skills + rules) — Nobody else formally separates always-on rules from on-demand skills with different formats and install mechanisms.

2. **Cross-platform install scripts** with idempotency, collision detection, bloat warnings — Tested, safe, production-ready. Nobody else has this.

3. **104 automated tests** — No other marketplace or collection tests anything.

4. **PEP 723 zero-install scripts** — Skills with real executable code, not just instruction text.

### Where the ecosystem has passed us:

1. **Scale** — We have 24 items. SkillsGate has 60K+. Curated counts, but we need more.

2. **agents/openai.yaml** — Codex skills support UI metadata, icon branding, invocation policy, and MCP dependencies. We don't have this.

3. **Security scanning** — SkillsGate scans skills via MCP before install. We have `allowed-tools` but no scanning.

4. **Progressive disclosure** — Codex loads only name+description first, full SKILL.md on activation. Our format supports this but our installer doesn't leverage it.

5. **Web discovery** — Every competitor has a web presence. We're CLI/git only.

6. **Auto-indexing** — claude-plugins.dev auto-indexes all GitHub skills. We require manual PR contribution.

### Recommended actions (priority order):

1. **Add `agents/` directory support** to SKILL.md format — include `openai.yaml` for Codex compatibility. This makes our skills installable via `$skill-installer`.

2. **Security scanning skill** — Build a marketplace skill that scans other skills before install (like SkillsGate's approach).

3. **Don't chase volume** — The 400K+ skill aggregators are full of noise. Our value is curated + tested + executable.

4. **Watch the supply chain security papers** — The malicious skill problem is real and growing. Our `allowed-tools` restriction and test infrastructure are defensive moats.

5. **Consider Anthropic plugin marketplace compatibility** — Add `.claude-plugin/marketplace.json` so our marketplace can be registered as a Claude Code plugin source.

---

## 10. Source Index

### GitHub Repos
| Name | URL | Stars |
|---|---|---|
| anthropics/skills | github.com/anthropics/skills | 75,600 |
| openai/skills | github.com/openai/skills | New |
| awesome-cursorrules | github.com/PatrickJS/awesome-cursorrules | 38,481 |
| devin.cursorrules | github.com/grapeot/devin.cursorrules | 5,961 |
| awesome-cursor-rules-mdc | github.com/sanjeed5/awesome-cursor-rules-mdc | 3,378 |
| agentic-cursorrules | github.com/s-smits/agentic-cursorrules | 646 |
| cursor-security-rules | github.com/matank001/cursor-security-rules | 367 |

### Web Marketplaces
| Name | URL |
|---|---|
| SkillsGate | skillsgate.ai |
| SkillsMP | skillsmp.com |
| SkillzWave | skillzwave.ai |
| SkillHub | skillhub.club |
| skills.sh | skills.sh |
| cursor.directory | cursor.directory |
| Cursor Marketplace | cursor.com/marketplace |
| Agensi | agensi.io |
| claude-plugins.dev | claude-plugins.dev |
| claudemarketplaces.com | claudemarketplaces.com |
| SafuSkill | safuskill.ai |

### ArXiv Papers
| Paper | ID | Date |
|---|---|---|
| Malicious Agent Skills in the Wild | 2602.06547 | Feb 2026 |
| Formal Analysis / Supply Chain Security | 2603.00195 | Feb 2026 |
| Automating Skill Acquisition | 2603.11808 | Mar 2026 |
| AI Agent Registry Survey | 2508.03095 | Aug 2025 |
| Prompt Injection via Skills | 2510.26328 | Oct 2025 |
| Open Ecosystems for LLM Apps | 2503.04596 | Mar 2025 |
| Agent Interoperability Protocols Survey | 2505.02279 | May 2025 |

### Twitter/X Signals
| Account | Signal |
|---|---|
| @Xiaojie_Qiu | Pantheon Store — 1,300+ biomedical skills |
| @binance / @bsc_daily | 7 Binance AI Agent Skills |
| @BNBCHAIN | SafuSkill security marketplace |
| @dani_avila7 | Skills ecosystem growth observation |
| @singularityhack | SkillShop marketplace launch |
| @betashop | "Skills are the unlock" thesis |
| @devhunt_ | TutuoAI marketplace |

### Reddit Threads
| Thread | Subreddit |
|---|---|
| Claude Skills are just .cursorrules | r/ClaudeAI |
| I indexed 45k skills (SkillsGate) | r/CLine, r/ClaudeAI |
| I built a SKILL.md marketplace (Agensi) | r/AgentsOfAI |
| Agent Skills: The Open Standard | r/cursor |
| Week 3 building marketplace | r/buildinpublic |

### Kaggle/Academic
| Resource | Source |
|---|---|
| 5-Day AI Agents Course | Kaggle + Google |
| Gorilla Agent Marketplace | UC Berkeley |
| AWS Marketplace AI agents | AWS |
| OpenAI Codex Skills docs | developers.openai.com |
| Agent Skills standard | agentskills.io |
