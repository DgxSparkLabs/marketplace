# GitHub Findings — Round 3

> Focus: Skill creation tooling, testing/evaluation frameworks, package management, mega-collections, skills for small models

## 1. Skill Testing & Evaluation

### microsoft/waza — CLI for Agent Skill Evaluation
- **URL:** https://github.com/microsoft/waza
- **Language:** Go | **Date:** 2026-02-27
- **What it is:** Microsoft's official CLI/framework for creating, testing, measuring, and improving agent skill quality
- **Key capabilities:**
  - `waza init` — scaffold project with `skills/` and `evals/` directories
  - `waza new skill` — create skill with scaffolded evaluation suite
  - `waza new eval` — generate eval from existing SKILL.md
  - `waza run` — execute evaluations against skills
  - `waza grade` — grade output from previous runs
  - `waza compare` — compare results across models (e.g., GPT-4 vs Sonnet)
  - `waza tokens count/compare/suggest` — token budget analysis and optimization
  - `waza check` — readiness validation before submission
  - `waza suggest` — AI-generated eval suite from SKILL.md
- **CI/CD:** Ships `.github/workflows/eval.yml` for automated eval on PR
- **Distribution:** Install script, Go install, or Azure Developer CLI extension (`azd waza`)
- **Significance:** First official vendor tool for skill quality measurement. Establishes eval-driven development as the standard for skill authorship

### fugazi/test-automation-skills-agents
- **URL:** https://github.com/fugazi/test-automation-skills-agents
- Practical library of agents, instructions, and skills for QA Automation Engineers
- Production-oriented solutions focus

## 2. Skill Package Management (NEW ecosystem layer)

### skillpm — npm-based Package Manager for Agent Skills
- **URL:** https://github.com/musharrafsaroof-123/skillpm
- **Date:** 2026-03-09
- **Problem:** "The Agent Skills spec defines what a skill is -- but not how to publish, install, version, or share them. There's no registry, no dependency management, no way for one skill to build on another."
- **Solution:** Maps agent skills onto npm's ecosystem — same package.json, node_modules, registry
- **Key features:**
  - `skillpm install` — npm install + scan node_modules for SKILL.md + link into agent dirs + configure MCP servers
  - `skillpm publish` — publish to npmjs.org (validates "agent-skill" keyword)
  - `skillpm init` — scaffold new skill package
  - `skillpm sync` — re-wire agent dirs without reinstalling
  - `skillpm mcp add/list` — configure MCP servers transitively
  - Full dependency tree resolution (transitive skills + MCP servers)
  - Agent wiring for Claude, Cursor, VS Code, Codex, and more
- **Size:** ~630 lines of code, 3 runtime dependencies
- **Orchestrates:** npm + `skills` CLI + `add-mcp`
- **Significance:** First serious attempt at transitive dependency resolution for skills

### FastSkill — Package Manager + Registry + Semantic Search
- **URL:** https://github.com/gofastskill
- **Date:** 2026-03-10
- **What it is:** Package manager and operational toolkit for the AI agent ecosystem
- **Key features:**
  - Install from Git, local folders, ZIP, or registry
  - Semantic search via OpenAI embeddings + natural language queries
  - Registry services: publish, version, distribute
  - Manifest system with lock files for reproducible installations
  - HTTP API for agent integration
  - Web UI for browsing/managing
- **CLI:** `fastskill add`, `fastskill search`, `fastskill publish`
- **Install:** curl script or manual binary download
- **Target users:** Skill authors, agent devs, teams (private registries), CI/CD pipelines

### neovateai/agent-skill-npm-boilerplate
- **URL:** https://github.com/neovateai/agent-skill-npm-boilerplate
- **Date:** 2026-01-09
- **What it is:** Template for publishing skills as npm packages
- **Key insight:** "Skills become proper software artifacts with semantic versioning, dependency management, private registries, and global discovery. Same infrastructure that distributes React and Express."
- Supports Claude Code, Cursor, Windsurf; auto-detects global vs project install
- Fork → edit SKILL.md → `npm publish` → installable worldwide

### agentskills/agentskills — skills.json Manifest RFC
- **URL:** https://github.com/agentskills/agentskills/discussions/210
- Proposal for a `skills.json` manifest file alongside SKILL.md
- Declares dependencies, versions, and distribution metadata
- Enables skills to be distributed as packages with resolved dependency trees

### cathy-kim/skill-semver
- **URL:** https://github.com/cathy-kim/skill-semver
- **Date:** 2026-01-30
- Automatic version control for Claude Code Skills with semantic versioning
- Auto-backup and changelog generation

## 3. Skill Management CLIs

### jkitchin/skillz — Cross-Platform Skill Manager
- **URL:** https://github.com/jkitchin/skillz
- **Date:** 2025-11-29
- **What it is:** CLI tool for managing AI assistant skills and slash commands
- **Supported platforms:** Claude Code, OpenCode, Codex, Gemini
- **Key features:**
  - `skillz install/uninstall` — install skills to any platform
  - `skillz search` — find by keywords and descriptions
  - `skillz create` — interactive wizard or AI-assisted creation via Claude CLI
  - `skillz validate` — ensure format compliance
  - `skillz hooks` — lifecycle hooks (formatting, logging, security, notifications)
  - `skillz agents` — manage specialized subagents (code review, debugging, testing, docs)
- **Config:** `~/.config/skillz/config.yaml` with per-platform paths
- **Install:** `uv pip install -e .` or standard pip

## 4. Mega-Collections

### sickn33/antigravity-awesome-skills — 1,259+ Skills
- **URL:** https://github.com/sickn33/antigravity-awesome-skills
- **Date:** 2026-01-14 | **Version:** V7.9.1
- **Scale:** 1,259+ skills across planning, coding, debugging, testing, security, infra, product thinking
- **Unique features:**
  - Curated bundles ("Web Wizard", "Security Engineer", "Essentials")
  - Includes a **skill-creator** skill with `init_skill.py` and `package_skill.py` scripts
  - Lint-and-validate skill for quality checking
  - npx installer: `npx antigravity-awesome-skills`
  - Comprehensive agent compatibility table (Claude Code, Gemini CLI, Codex CLI, Kiro, Antigravity, Cursor, Copilot)
- **Note:** Claims "battle-tested" but unclear quality assessment methodology

### LerianStudio/ring — 83 Skills + 37 Agents
- **URL:** https://github.com/LerianStudio/ring
- **Date:** 2025-10-30
- **What it is:** "Mandatory workflow system enforcing software engineering best practices and quality gates for AI agents"
- **Scale:** 83 skills (21 core + 24 dev-team + 15 product + 7 FinOps + 7 technical writing + 9 PMO) + 37 agents
- **Agent categories:**
  - Review & Planning (10): code-reviewer, business-logic-reviewer, security-reviewer, test-reviewer, nil-safety-reviewer, consequences-reviewer, dead-code-reviewer, review-slicer, write-plan, codebase-explorer
  - Developer (11): backend-engineer-golang, backend-engineer-typescript, devops-engineer, frontend-bff, frontend-designer, frontend-engineer, prompt-quality-reviewer, qa-analyst, qa-analyst-frontend, sre, ui-engineer
  - Product Research (4): repo-research, best-practices, framework-docs, product-designer
  - Technical Writing (3): functional-writer, api-writer, [third]
  - FinOps (3) + PMO (6)
- **Philosophy:** "Without Ring, AI assistants skip tests, jump to implementation, claim tasks complete without verification, forget to check for existing solutions, repeat known mistakes"
- **Currently:** Claude Code plugin marketplace with 6 active plugins
- **Significance:** Most comprehensive opinionated workflow enforcement system found

## 5. Skills for Small Models

### AI6130-LLMs-Group-Project/tiny-agent-skills
- **URL:** https://github.com/AI6130-LLMs-Group-Project/tiny-agent-skills
- **Date:** 2026-01-29 | **Version:** 2.0.1
- **Problem:** Claude's skills work because of rich docs + reasoning. Small models (2B-7B) have limited context, weak reasoning, poor function calling (<60% accuracy), no error recovery
- **Solution:** User writes markdown skill documentation → framework auto-compiles to optimized tool-calling schemas for small models
- **Architecture:**
  - DAG pipeline for complex multi-step tasks
  - FSM-based method for structured skill execution
  - React-based method for flexible reasoning
  - Qwen3-VL-2B as default model (runs on llama.cpp)
- **Testing:** SkillFever evaluation benchmark included
- **Significance:** Democratizes SKILL.md for local AI — anyone can build domain-specific assistants without cloud dependencies

## 6. Engineering Standards as Skills

### HoangNguyen0403/agent-skills-standard
- **URL:** https://github.com/HoangNguyen0403/agent-skills-standard
- **Date:** 2026-01-15
- Modular framework for distributing, syncing, and version-controlling engineering standards across major AI agents
- Targets: Cursor, Claude Code, GitHub Copilot, Windsurf, Kiro, Gemini, Antigravity
- Includes CHANGELOG.md with formal versioning

## 7. Vercel/skills.sh Ecosystem (deep dive not in prior rounds)

### Vercel skills CLI + skills.sh Directory
- **URL:** https://github.com/vercel-labs/skills | https://skills.sh
- **Launched:** January 20, 2026
- **Adoption stats (from Snyk/InfoQ):**
  - Top skill: 20,000+ installs within 6 hours of launch
  - `find-skills` utility: 235,000+ weekly installs
  - Stripe shipped skills within hours of launch
  - Average: 147 new skills per day
  - 110,000+ installs in first 4 days
- **Supported agents:** Claude Code, Cursor, Windsurf, Goose, GitHub Copilot, Gemini CLI, Amp, Kimi Code CLI, and more
- **Install:** `npx skills add <package>`
- **Security:** Snyk partnership provides real-time scanning at install time (see arxiv.md)

### Snyk + Vercel Partnership (Feb 17, 2026)
- Every `npx skills add` triggers Snyk's high-throughput scanning API
- Multi-layer analysis: traditional code analysis + LLM-based judges for prompt injection
- CRITICAL-level detectors: 90-100% recall on confirmed malicious, 0% false positive on top 100 legitimate
- "Security Verified" badge on skills.sh
- Continuous monitoring — re-evaluation as detection improves
- Built on **agent-scan** (mcp-scan) from Invariant Labs (ETH Zurich acquisition)
- 8 security policy categories

## Key Patterns Observed

1. **Package management is the hot problem.** Three independent implementations (skillpm, FastSkill, npm-boilerplate) plus an RFC for skills.json — all solving dependency resolution, versioning, and distribution
2. **Evaluation is formalizing.** microsoft/waza establishes eval-driven development as the standard approach
3. **Mega-collections are growing but quality is unverified.** 1,259 skills (antigravity) with no clear quality gates
4. **Workflow enforcement via skills** (Ring) represents a new pattern — skills as governance, not just capability
5. **Skills for small models** (tiny-agent-skills) opens the door to local/offline/privacy-preserving agent capabilities
6. **Vercel/skills.sh is the npm of skills** — fastest adoption, strongest security story (Snyk), 17+ supported agents
