# Reddit Findings — AI Agent Skill Marketplaces

*Searched: 2026-03-16 via DuckDuckGo site:reddit.com queries*

---

## Threads Found

Note: Reddit blocks most scraping — search yielded limited results compared to other platforms. DuckDuckGo showed page descriptions as "The site owner hides the web page description." for most Reddit results. Findings are synthesized from snippets and cross-referenced with other platform data.

### Thread 1: "Claude Skills are just .cursorrules, change my mind" (r/ClaudeAI)

**Context:** Community debate on whether Anthropic's Agent Skills are fundamentally different from Cursor rules files.

**Key arguments:**
- Skills add structured YAML metadata (name, description, triggers) that .cursorrules lack
- Progressive disclosure (3-level loading) is architecturally different from flat rule files
- Skills are portable across agents; .cursorrules are Cursor-only
- Counter-argument: at the end of the day both are just markdown instructions for an LLM

**Consensus emerging:** Skills are an evolution of cursor rules with meaningful structural improvements, not just a rebrand.

### Thread 2: "I indexed 45k AI agent skills into an open source marketplace" (r/CLine, r/ClaudeAI, r/buildinpublic, r/vibecoding)

**Context:** SkillsGate launch announcement, cross-posted to 4+ subreddits.

**Key details:**
- SkillsGate indexes 45K+ skills
- One-command install: `npx skillsgate add @username/skill-name`
- Community response: moderate interest, primary questions about quality control
- Concerns about mass-indexing without quality vetting

### Thread 3: "I built a SKILL.md marketplace" (r/AgentsOfAI)

**Context:** Agensi.io launch post by u/BadMenFinance.

**Key details:**
- Features security vulnerability scanning for skill files
- Low engagement (5 comments)
- Community asked "What is defined as a security vulnerability in a skill file?"
- Author pointed to agensi.io/security for definitions
- Symptom of "marketplace fatigue" — too many "I built a marketplace" posts

### Thread 4: "Agent Skills: The Open Standard for Custom AI Capabilities" (r/cursor)

**Context:** Announcement that Cursor now supports Agent Skills.

**Key details:**
- Skills install to `.cursor/skills/` and work alongside cursor rules
- One-command install support
- Comments reference it working like .cursor/rules system but more structured
- Issue #158 on PatrickJS/awesome-cursorrules GitHub repo also tracks this

### Thread 5: "Week 3 of building a marketplace for AI agent skills" (r/buildinpublic)

**Context:** Build-in-public posts about marketplace development.

**Key details:**
- Feature highlight: "automated scanner that checks every uploaded skill for malicious patterns — 8 checks including dangerous commands"
- Shows security scanning is considered essential even for small/indie marketplaces

---

## Sentiment Analysis

### Positive Signals
- Agent Skills are seen as a real improvement over raw cursor rules
- Cross-platform portability is valued
- Security-first marketplaces are generating interest

### Negative Signals
- **Marketplace fatigue**: Too many "I built a skill marketplace" posts with decreasing engagement
- **Quality > quantity skepticism**: Community doesn't trust 45K+ skill counts, prefers curated sets
- **Security anxiety**: Multiple threads express concern about installing untrusted skills
- **"Just markdown" dismissal**: Some view skills as overhyped text files

### Key Community Preferences
1. Curated, tested skills over mass-indexed collections
2. Security scanning before installation
3. Clear provenance and authorship
4. Skills from known vendors/teams (Anthropic, Vercel, Stripe) are trusted; random community skills are not
5. Portable across agents — nobody wants vendor lock-in
