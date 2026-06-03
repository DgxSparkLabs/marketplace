# AI Agent Skills & Rules Marketplace — Landscape Research

*Date: 2026-03-16*

---

## 1. Executive Summary

The AI agent skills/rules marketplace space is young but rapidly segmenting into
four distinct tiers. At the top sits the **official platform** tier (Cursor
Marketplace, OpenAI Codex Skills), which defines canonical formats. Below that, a
**web marketplace** tier (SkillzWave, SkillsMP, cursor.directory, skills.sh)
aggregates community content at scale. A **GitHub curation** tier (awesome-
cursorrules, awesome-cursor-rules-mdc) relies on open-source collections. Finally,
a **tooling** tier (Rulix, agentic-cursorrules, rules-gen, cursor-windsurf-convert)
solves the cross-IDE synchronization and generation problems.

Our marketplace occupies a unique niche: **a self-contained, repo-based
marketplace that combines skills AND rules with cross-platform install scripts,
test infrastructure, and a unified SKILL.md/rule.md format.** No other project in
the landscape does all of these together.

---

## 2. Detailed Findings

### Tier 1: Official Platforms

#### 2.1 Cursor Marketplace (`cursor.com/marketplace`)

| Attribute | Value |
|---|---|
| URL | https://cursor.com/marketplace |
| Type | Official IDE marketplace |
| Content | Plugins (skills, subagents, rules, hooks, commands, MCP servers) |
| Format | Manifest-based (manifest.json) |
| Installation | Built into Cursor IDE |
| Content volume | 50+ featured plugins, growing rapidly |
| Notable plugins | Datadog, Slack, Figma, Linear, PagerDuty, Redis, Clerk |
| Monetization | Free (vendor-sponsored) |

**Analysis:** The 800-pound gorilla. Cursor's official marketplace uses a
proprietary manifest format and is tightly integrated into the IDE. Plugins can
bundle skills, rules, MCP servers, hooks, and commands together. This is the
direction the market is heading — unified plugin bundles with automatic
installation. **However**, it's Cursor-only and vendor-locked.

#### 2.2 OpenAI Codex Skills (`openai/skills` + `agentskills.io`)

| Attribute | Value |
|---|---|
| GitHub | https://github.com/openai/skills |
| Stars | New repo (just launched) |
| Type | Official skills catalog for Codex |
| Format | **SKILL.md** (open standard at agentskills.io) |
| Structure | `skills/.system/`, `skills/.curated/`, `skills/.experimental/` |
| Installation | `$skill-installer` within Codex |
| Skill structure | `SKILL.md` + `agents/openai.yaml` + `references/` + `scripts/` |
| License | Per-skill licensing (LICENSE.txt in each skill) |

**Analysis:** This is the most significant development in the space. OpenAI has
published an **open standard** at agentskills.io for agent skills. The SKILL.md
format is explicitly designed for cross-agent portability: "Build capabilities
once and deploy them across multiple agent products." Skills include procedural
knowledge, scripts, and reference materials. The three-tier organization
(system/curated/experimental) is a mature content pipeline.

**Our marketplace already uses SKILL.md format**, which means we're aligned with
what's becoming the industry standard. Their structure (references/, scripts/,
agents/) is very similar to ours.

---

### Tier 2: Web Marketplaces

#### 2.3 SkillzWave (`skillzwave.ai`)

| Attribute | Value |
|---|---|
| URL | https://skillzwave.ai |
| Type | Vendor-agnostic skills marketplace |
| Content volume | 42,645+ skills |
| CLI | `skilz install <skill-name>` (pip install skilz) |
| Supported agents | 22+ agents (Claude Code, Codex, Cursor, Gemini, Aider, Windsurf, Zed, RooCode, Devin, etc.) |
| Features | ML-powered quality scores, 4-level taxonomy, enterprise packages |
| Business model | Free + premium domain packages (Legal, Real Estate, Finance — "Coming Soon") |
| Target | Developers + business professionals |

**Analysis:** The largest aggregator by content volume. Interesting vendor-
agnostic positioning with support for 22+ agents. The `skilz` CLI is their
differentiator. Enterprise packages for specific industries (legal, finance, real
estate) show commercial ambition. However, many skills appear auto-generated, and
the quality scores are ML-based rather than human-curated.

#### 2.4 SkillsMP (`skillsmp.com`)

| Attribute | Value |
|---|---|
| URL | https://skillsmp.com |
| Type | Agent skills marketplace |
| Content volume | 400,000+ skills (claimed) |
| Format | SKILL.md (open standard) |
| Supported agents | Claude Code, Codex CLI, ChatGPT |

**Analysis:** Claims the largest catalog (400K+), likely through aggressive
scraping/aggregation. Uses the SKILL.md open standard format. Less data available
on quality controls.

#### 2.5 skills.sh

| Attribute | Value |
|---|---|
| URL | https://skills.sh |
| Type | Agent skills directory/leaderboard |
| Format | SKILL.md |
| Installation | Single command |
| Top sources | microsoft/github-copilot-for-azure (2.5M installs), microsoft/azure-skills (810K), inferen-sh/skills (476K) |

**Analysis:** More of a directory/leaderboard than a marketplace. Aggregates
skills from GitHub repos and ranks them by install count. Shows the scale of
adoption from Microsoft's official skill repos. Microsoft alone has millions of
skill installs.

#### 2.6 cursor.directory

| Attribute | Value |
|---|---|
| URL | https://cursor.directory |
| Type | Community platform for Cursor |
| Content | Rules, plugins, MCP servers, news, jobs |
| Target | Cursor IDE users |

**Analysis:** The community hub for Cursor enthusiasts. Provides curated rules,
MCP server integrations, and a social layer (board posts, job listings). Less
structured than a marketplace, more like a community forum with a rules browser.

---

### Tier 3: GitHub Collections

#### 2.7 PatrickJS/awesome-cursorrules ⭐ 38,481 stars

| Attribute | Value |
|---|---|
| GitHub | https://github.com/PatrickJS/awesome-cursorrules |
| Stars | 38,481 |
| Forks | 3,258 |
| License | CC0-1.0 |
| Language | MDX |
| Format | `.cursorrules` files |
| Organization | By category (Frontend, Backend, Mobile, CSS, State, DB, Testing, etc.) |
| Rule count | 100+ rules |
| Monetization | Sponsorships (Warp, CodeRabbit, Unblocked) |

**Analysis:** By far the largest community-curated collection by star count. Uses
the older `.cursorrules` file format (single file in project root). Rules are
organized by technology stack. No CLI, no installer — just copy-paste into your
project. The sponsorship model shows commercial viability of curation alone.

**Strengths:** Massive community, comprehensive technology coverage.
**Weaknesses:** Outdated format (.cursorrules vs .mdc), no cross-IDE support, no
installation tooling, no quality scoring.

#### 2.8 sanjeed5/awesome-cursor-rules-mdc ⭐ 3,378 stars

| Attribute | Value |
|---|---|
| GitHub | https://github.com/sanjeed5/awesome-cursor-rules-mdc |
| Stars | 3,378 |
| Forks | 397 |
| License | CC0-1.0 |
| Format | `.mdc` (Markdown Cursor — newer Cursor format) |
| Key feature | **Auto-generates rules** using Exa + LLM (Gemini/OpenAI/Anthropic) |
| Tool | `uv run src/generate_mdc_files.py` |

**Analysis:** The evolutionary successor to awesome-cursorrules. Uses the modern
`.mdc` format and — crucially — **automates rule generation** via semantic search
(Exa) + LLM. You add a library name to `rules.json` and it generates a
comprehensive .mdc rule file automatically. Uses `uv` for dependency management
(like us). This is a significant approach: scaling through automation rather than
manual curation.

**Key insight:** Auto-generation could be a feature for our marketplace. Their
approach is: 1) semantic search for best practices, 2) LLM synthesis, 3) output
to standard format.

#### 2.9 grapeot/devin.cursorrules ⭐ 5,961 stars

| Attribute | Value |
|---|---|
| GitHub | https://github.com/grapeot/devin.cursorrules |
| Stars | 5,961 |
| Forks | 769 |
| License | MIT |
| Concept | "Turn Cursor/Windsurf into 90% of Devin" |
| Features | Planner-executor, web tools, self-evolution, scratchpad |
| Setup | Cookiecutter template or manual file copy |

**Analysis:** Not a marketplace but a single opinionated ruleset that transforms
Cursor/Windsurf into a Devin-like agent. Key concepts:
- **Scratchpad** for persistent memory across sessions
- **Self-evolution** — AI updates its own rules based on corrections
- **Extended tools** — web scraping, search, LLM analysis
- **Multi-agent** — planner (o1) + executor (Claude/GPT)

**Key insight:** Self-evolution and persistent memory (scratchpad) are powerful
concepts our marketplace skills could adopt. The "rules as behavior templates"
approach is valuable.

---

### Tier 4: Cross-IDE Tooling

#### 2.10 danielcinome/rulix ⭐ 2 stars

| Attribute | Value |
|---|---|
| GitHub | https://github.com/danielcinome/rulix |
| Type | CLI tool — single-source rule sync across IDEs |
| Supported targets | Cursor (.mdc), Claude Code, AGENTS.md, Windsurf, Copilot |
| Format | Unified `.rulix/rules/` → generates per-IDE output |
| Language | TypeScript (npm package) |
| License | MIT |

**Analysis:** Directly addresses our same problem — rule format fragmentation.
Rulix takes a single `.rulix/rules/` directory and generates tool-specific
configs for Cursor, Claude Code, Windsurf, Copilot, and AGENTS.md. Handles
frontmatter differences, scoping semantics, and token budgets automatically.

**Very relevant to our marketplace.** This is the same problem our `install.sh`
scripts solve, but Rulix approaches it as a compile-time transformation rather
than an install-time copy. Small repo (2 stars) but well-architected idea.

#### 2.11 s-smits/agentic-cursorrules ⭐ 646 stars

| Attribute | Value |
|---|---|
| GitHub | https://github.com/s-smits/agentic-cursorrules |
| Stars | 646 |
| Concept | File-tree partitioning for multi-agent workflows |
| Key feature | Generates per-domain markdown files with explicit boundaries |
| Tool | `uv run agentic-cursorrules --init` |

**Analysis:** Solves a different problem: when you have multiple AI agents
working on the same codebase, how do you prevent them from stepping on each
other? Generates domain-scoped rule files (`@agent_backend_api.md`) that
constrain agents to specific file trees. Uses `uv` (like us).

**Key insight:** Domain partitioning is relevant for large teams. This could be
a skill in our marketplace.

#### 2.12 matank001/cursor-security-rules ⭐ 367 stars

| Attribute | Value |
|---|---|
| GitHub | https://github.com/matank001/cursor-security-rules |
| Stars | 367 |
| Concept | Security guardrails for AI coding agents |
| Topics | Secure coding, MCP safety, no secrets in frontend, safe commands |

**Analysis:** Focused collection of security rules — preventing agents from
generating unsafe code, exposing secrets, or running dangerous commands. Simple
approach: just drop `.cursor/rules/` files into your project.

**Key insight:** Security rules are high-value and could be a rule category in
our marketplace. Our `AGENTS.md` global rules already include similar safety
concepts.

#### 2.13 iannuttall/task-magic ⭐ 242 stars

| Attribute | Value |
|---|---|
| GitHub | https://github.com/iannuttall/task-magic |
| Stars | 242 |
| Concept | Task management system via Cursor/Windsurf rules |
| Structure | `.ai/plans/`, `.ai/tasks/`, `.ai/memory/` |
| Target | Cursor + Windsurf |

**Analysis:** A complete project management system implemented entirely as IDE
rules. Three layers: Plans (PRDs) → Tasks (work items) → Memory (archived
history). Rules use `_index.md` files for automatic context and on-demand rule
loading via descriptions. Avoids the "AI loop of death" by breaking work into
focused, testable tasks.

**Key insight:** The `.ai/memory/` concept for persistent agent memory is
powerful. This could be both a skill and a rule in our marketplace.

#### 2.14 nextlevelbuilder/skillx ⭐ 34 stars

| Attribute | Value |
|---|---|
| GitHub | https://github.com/nextlevelbuilder/skillx |
| Stars | 34 |
| Type | Full-stack skills marketplace |
| Stack | React Router v7, Cloudflare Workers, D1, Vectorize |
| CLI | `skillx search`, `skillx use`, `skillx report` |
| Features | Semantic search, leaderboard, ratings, reviews, favorites |
| Claude plugin | Yes (Claude Code marketplace integration) |
| Content | 500+ skills (seed data is 30 real skills) |

**Analysis:** The most feature-complete marketplace implementation. Has web UI,
CLI, hybrid search (semantic + keyword), user accounts, ratings/reviews,
leaderboard, API keys, and usage reporting. Also integrates as a Claude Code
plugin. Technically ambitious but low adoption (34 stars). Shows what a
full-featured marketplace could look like.

---

## 3. Format Comparison

| Format | Used by | Structure | Cross-IDE? |
|---|---|---|---|
| **SKILL.md** (YAML frontmatter + markdown) | Our marketplace, OpenAI Codex, SkillzWave, SkillsMP, skills.sh, agentskills.io | name, description, allowed-tools + prompt body | ✅ Open standard |
| `.cursorrules` | awesome-cursorrules, devin.cursorrules | Single file, plain text | ❌ Cursor only (legacy) |
| `.mdc` (YAML frontmatter + markdown) | awesome-cursor-rules-mdc, Cursor official | description, globs, alwaysApply | ❌ Cursor only |
| `.windsurf/rules/*.md` | Windsurf | trigger frontmatter + markdown | ❌ Windsurf only |
| `AGENTS.md` | Our marketplace, Claude Code, Devin CLI | Plain markdown, heading-delimited | ✅ Multi-agent |
| `rule.md` | Our marketplace | Plain markdown, no frontmatter | ✅ With install scripts |
| `manifest.json` | Cursor Marketplace | JSON manifest with skills, rules, hooks, commands | ❌ Cursor only |
| `.rulix/rules/*.md` | Rulix | Unified source → compile to targets | ✅ Build-time |

**The SKILL.md format is winning.** OpenAI's endorsement via agentskills.io as
an open standard, plus adoption by SkillzWave (42K+ skills), SkillsMP (400K+),
and skills.sh means it's becoming the de facto standard for portable agent
skills.

---

## 4. Competitive Analysis — Our Position

### What we do that nobody else does:

1. **Skills + Rules in one marketplace** — Everyone else is either skills-only or
   rules-only. We're the only repo that has both, with distinct formats and
   install mechanisms for each.

2. **Cross-platform install scripts** — Each rule has `install.sh` that handles
   Devin/Cursor/Windsurf format differences, with idempotency, scope collision
   detection, and bloat warnings. Nobody else has this level of installation
   safety.

3. **Test infrastructure** — 104 automated tests validating structure, formats,
   installer behavior, and content parity. No other marketplace or collection has
   tests at all.

4. **Python-first with PEP 723** — Scripts use inline metadata and `uv run` for
   zero-install execution. Clean and portable.

5. **Global install.py** — TUI installer that manages all skills and rules across
   platforms from a single command.

### Where we lag:

1. **Scale** — We have ~15 skills and ~5 rules. SkillzWave has 42K+, awesome-
   cursorrules has 100+. Content volume is our biggest gap.

2. **No web UI** — SkillX, SkillzWave, cursor.directory all have web interfaces
   for browsing and discovery. We're CLI/repo only.

3. **No search** — SkillX has semantic search, SkillzWave has ML-powered quality
   scores. We have no discovery mechanism beyond README.

4. **No auto-generation** — awesome-cursor-rules-mdc generates rules with LLM.
   We create everything manually.

5. **No ratings/reviews** — SkillX has a full rating system. We have no feedback
   mechanism.

6. **No CLI package** — SkillzWave has `skilz`, SkillX has `skillx`, OpenAI has
   `$skill-installer`. We have `install.py` but it's not a published package.

---

## 5. Key Trends & Patterns

### 5.1 The SKILL.md standard is consolidating
OpenAI's agentskills.io, Codex's native support, and adoption by multiple
marketplaces mean SKILL.md is the format to bet on. Our existing use of it is a
strategic advantage.

### 5.2 Cross-IDE portability is the unsolved problem
Every IDE has its own format. Rulix, our install scripts, and SkillzWave's 22-
agent support all show that the market badly wants write-once-run-anywhere rules.
The winner will be whoever makes cross-IDE deployment frictionless.

### 5.3 Auto-generation is the scaling strategy
Manual curation doesn't scale to 40K+ skills. awesome-cursor-rules-mdc and
SkillzWave both use LLM-based generation. This is the only viable path to
content scale.

### 5.4 Agent memory and self-evolution are emerging
devin.cursorrules' scratchpad and self-evolution, task-magic's `.ai/memory/`, and
our own `PROGRESS.md` approach all point to persistent agent memory as a key
differentiator.

### 5.5 Security rules are high-value
cursor-security-rules (367 stars) shows strong demand. Security guardrails for
AI agents are an underserved category.

### 5.6 Enterprise is the monetization path
SkillzWave's "domain packages" for legal, finance, and real estate, plus Cursor
Marketplace's vendor-sponsored plugins, show that B2B is where the money is.

---

## 6. Conclusions & Recommendations

### Our strategic advantages:
- **Quality over quantity** — Test-driven, safe, idempotent installers
- **Dual format** — Skills + rules in one place
- **Standards-aligned** — Already using SKILL.md before it became the standard
- **Self-contained** — No external dependencies, no accounts, no API keys needed

### Recommended actions:

1. **Keep using SKILL.md** — It's becoming the industry standard. Consider
   adding `agents/` directory with agent-specific config (like OpenAI's
   `agents/openai.yaml`) for maximum compatibility.

2. **Consider auto-generation tooling** — A skill/rule generator (like
   awesome-cursor-rules-mdc's approach) could scale our catalog rapidly.

3. **Domain security rules** — High demand, good fit for our quality-focused
   approach. A "security" rule pack would be immediately useful.

4. **Cross-IDE is our strongest angle** — Nobody else has tested, idempotent
   install scripts. Lean into this as a differentiator.

5. **Don't chase content volume** — SkillzWave's 42K skills include a lot of
   noise. Our value proposition is curated, tested, production-ready content.

6. **Watch Cursor Marketplace** — If Cursor's manifest.json becomes dominant, we
   may need to support it as an export format.

---

## 7. Source Index

| # | Name | URL | Stars | Type |
|---|---|---|---|---|
| 1 | Cursor Marketplace | cursor.com/marketplace | — | Official |
| 2 | OpenAI Skills / agentskills.io | github.com/openai/skills | New | Official |
| 3 | SkillzWave | skillzwave.ai | — | Web marketplace |
| 4 | SkillsMP | skillsmp.com | — | Web marketplace |
| 5 | skills.sh | skills.sh | — | Directory |
| 6 | cursor.directory | cursor.directory | — | Community |
| 7 | awesome-cursorrules | github.com/PatrickJS/awesome-cursorrules | 38,481 | Collection |
| 8 | awesome-cursor-rules-mdc | github.com/sanjeed5/awesome-cursor-rules-mdc | 3,378 | Generator |
| 9 | devin.cursorrules | github.com/grapeot/devin.cursorrules | 5,961 | Ruleset |
| 10 | Rulix | github.com/danielcinome/rulix | 2 | Sync tool |
| 11 | agentic-cursorrules | github.com/s-smits/agentic-cursorrules | 646 | Partitioning |
| 12 | cursor-security-rules | github.com/matank001/cursor-security-rules | 367 | Security |
| 13 | task-magic | github.com/iannuttall/task-magic | 242 | Task mgmt |
| 14 | SkillX | github.com/nextlevelbuilder/skillx | 34 | Full marketplace |
| 15 | cursor-rules-collection | github.com/HaiDong-Once/cursor-rules-collection | 23 | Collection (CN) |
| 16 | rules-gen | github.com/blencorp/rules-gen | 16 | CLI generator |
| 17 | cursor-windsurf-convert | github.com/gmickel/cursor-windsurf-convert | 5 | Converter |
