# Round 12: Reddit Skill Marketplace Research

**Date:** March 16, 2026
**Searches:** "site:reddit.com skill marketplace AI agent skills 2026" (20 results), 3 threads scraped

---

## Key New Threads Found

### 1. "I indexed 45k AI agent skills into an open source marketplace" (r/ClaudeAI)
**Author:** u/orngcode (SkillsGate builder) | **Comments:** 10

**Key Takeaways:**
- **45K skills indexed** with 150K+ waiting to be indexed — budget-constrained rollout
- **Semantic search** is the discovery mechanism (requires sign-in to protect against abuse)
- **LLM enrichment pipeline** assigns categories, capabilities, and metadata to each skill
- Descriptive queries work much better than short keywords for search quality
- Plan to add filtering by popular/trusted authors
- Cross-platform: Claude Code, Cursor, Windsurf, and other AI coding agents

**Community Reception:** Positive but questions about licensing, quality filtering, and discovery

---

### 2. "I spent a month testing every AI agent marketplace" (r/AgentsOfAI)
**Author:** u/BeatNo8512 | **Comments:** 3

**Key Takeaways:**
- After testing every marketplace: "the ecosystem is still early and the discovery layer is weak"
- "Most platforms list thousands of agents but no reliable way to verify real results"
- "Ratings are easy to game and many 'agents' are just thin wrappers around existing models"
- **Narrow workflows win:** "support automation example worked because the agent is trained for a narrow workflow instead of trying to be a general service"
- **NightMarket AI** recommended as "app store for agents" with moderation
- Comparison to "early days of app marketplaces — technology works in some cases, but discovery and trust layer still needs to mature"

---

### 3. "Skills Marketplace for AI Agents — 200K+ Skills" (r/AgentsOfAI)
**URL:** reddit.com/r/AgentsOfAI/comments/1rrirse/
- An open-source skill marketplace claiming 200K+ skills
- Aligns with SkillNet paper's 200K+ repository

### 4. "Agent Skills — Am I missing something?" (r/Anthropic)
- User questions whether skills are just YAML/markdown or something deeper
- Community response: "The standardization itself has merit — having a common format makes skills portable and shareable"
- Core value = portability + shareability, not technical complexity

### 5. "SkillFlow — marketplace with real trust metrics" (r/ChatGPT)
**Author:** u/SkillFlow builder
- SkillFlow (skillflow.builders) — curated marketplace with transparent trust metrics
- Metrics: success rate, total runs, verified reviews
- Addressing the core trust gap identified in all prior research rounds

---

## Reddit Sentiment Evolution (Round 11 -> Round 12)

| Metric | Round 11 | Round 12 |
|--------|----------|----------|
| **Dominant subreddits** | r/ClaudeCode, r/ClaudeAI | r/AgentsOfAI, r/ClaudeAI, r/ChatGPT |
| **Tone** | Skeptical about monetization | Accepting ecosystem is real, frustrated by quality |
| **#1 complaint** | "Can't monetize text files" | "Discovery and trust are broken" |
| **New theme** | — | "Tested all marketplaces — none are great yet" |
| **Marketplace builders posting** | Agensi.io | SkillsGate, SkillFlow, NightMarket AI |
| **Scale awareness** | "45K skills" was impressive | "200K+ skills" is the new norm |
| **Cross-platform** | Claude-centric | Multi-agent (Claude, Cursor, Windsurf, Codex) |

---

## Key Insights

1. **Discovery > Supply.** The problem has shifted from "not enough skills" to "can't find the right ones among 200K+"
2. **Trust metrics gaining traction.** SkillFlow's success rate + total runs model is what Reddit users want
3. **LLM-powered search/enrichment** is the emerging discovery pattern (SkillsGate)
4. **Cross-platform portability** is now expected, not differentiating
5. **"Early app store" analogy** is the dominant community mental model
6. **Narrow > general** continues to be the strongest user-validated pattern
