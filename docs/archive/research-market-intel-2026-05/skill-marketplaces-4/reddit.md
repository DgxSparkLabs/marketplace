# Reddit Findings — Round 4

> Focus: Enterprise deployment patterns, agent distribution, large team AI adoption

## Key Threads Not Covered in Rounds 1-3

### 1. r/AI_Agents — Enterprise Agent Deployment at Scale
- **Thread:** "Those deploying AI agents in large organizations -- what use-cases are actually making it to production, and what's blocking the rest?"
- **Link:** https://www.reddit.com/r/AI_Agents/comments/1rrj8zr/

**Key enterprise deployment pattern discovered (u/ilovefunc, 300+ person org):**
- **Shared agent environment:** Agent on server, web UI, all chat sessions non-deletable and auditable. A separate audit agent summarizes what people are doing.
- **Permission-based skills:** Anyone can create skills, but must explicitly share with others before the agent sees them. Critical skills (infra changes) coexist safely with non-technical users.
- **Approval flows:** Every skill/tool must be approved by an engineer. Any changes to approved skills require re-approval.
- **Platform:** TeamCopilot.ai built on OpenCode agent (anomalyco/opencode)

**Key insight on governance enforcement (u/GarbageOk5505):**
> "If the answer is 'the agent's config' or 'the system prompt' then you don't have governance, you have suggestions. The agent or whoever deployed it can change those at any time."
> "Policy enforcement at the execution environment, not the application. The agent runs in an isolated runtime where network access, filesystem access, API access are explicitly granted per agent."
> "The controls need to be underneath."

**Blockers identified:**
1. Knowledge gap of non-technical employees
2. Waiting for agent integration into existing tools (Jira, Salesforce, ServiceNow)
3. No enforcement layer — governance at application level doesn't work

### 2. r/AI_Agents — Agent Distribution Problem
- **Thread:** "how are we actually supposed to distribute and sell local agents to normal users?"
- **Link:** https://www.reddit.com/r/AI_Agents/comments/1rtradm/

**Key insights:**
- **The credential problem is the real blocker** — OAuth flows assume a web server, running locally means embedding HTTP server (security nightmare) or building a credential broker
- **Docker as middle ground** — ship container with local web UI, user pulls image, opens localhost:8080. Better than "clone this repo and edit .env" but Docker Desktop is still a hurdle for non-technical users
- **ClawHub as npm for skills:** "You publish a SKILL.md with your system prompts, tool routing logic, and expected schemas"
- **Desktop vault pattern:** Agent package contains zero auth logic; requests tokens from desktop client's vault which handles OS-level OAuth. Keeps agent code light.
- **Tauri > Electron** for packaging (smaller binary, Rust backend for secure credential vault)
- **"Early internet" framing recurs** — multiple users comparing current state to early web (pre-app store)
- **Security warning:** "throwing thousands of 3rd party agent skills into a centralized llm platform is a massive supply chain vulnerability... npm dependency problem on steroids"

### 3. r/golang — AI Coding for Large Teams (90 Go Developers)
- **Thread:** "ai coding for large teams in Go - is anyone actually getting consistent value?"
- **Link:** https://www.reddit.com/r/golang/comments/1rp70e7/

**Key insights for skills:**
- AGENTS.md / CLAUDE.md quality is critical — "It is important to craft a good AGENTS.md. That is not trivial."
- One user forces AI to not edit CLAUDE.md itself — treats it as a "constitution" curated by hand, with a separate editable rules file
- Go's simplicity = better AI results. Languages with multiple frameworks/patterns confuse models more
- **Plan mode** strongly recommended for complex tasks
- Model quality matters enormously — Opus >> Sonnet >> GPT-x for code generation

### 4. r/AI_Agents — "5 agent skills I'd install before starting any new agent project in 2026"
- Listed on r/AI_Agents front page — skills becoming standard onboarding advice for new projects

### 5. r/buildinpublic — Security SaaS for AI Developers
- **Thread:** "Built a security saas for AI developers - 47 users, $0 revenue, lessons learned"
- **Key comment:** "Security for agent skills is way more of a ticking time bomb than people think, so you're sitting on a real pain, not a vitamin."

### 6. r/accelerate — What Devs Get Paid For in 2026
- **Key exchange:** "Isn't half of this just an Agent Skills aka markdown with..." → "Design, solution architecture, product direction, taste."
- **Implication:** Skills are becoming so commodity that the differentiation shifts to architecture and design judgment

## Community Patterns (Round 4 vs Previous)

| Aspect | Rounds 1-3 | Round 4 |
|---|---|---|
| Enterprise deployment | Theoretical | Real 300+ person org described |
| Governance approach | "We need security" | "Controls must be underneath, not at app level" |
| Distribution | "Use npx skills add" | Credential broker + desktop vault + Tauri packaging |
| Skill authorship | Agent-generated vs human | "AGENTS.md as constitution, curated by hand" |
| Market position | Tools category | "Half of dev value is just markdown" (commoditizing) |
| Security awareness | Abstract concern | "Ticking time bomb, pain not vitamin" |

## Key Takeaways

1. **Enterprise pattern crystallized:** Admin-curated skill catalog → engineer approval → permission-based sharing → auditable execution. This is the deployment model.
2. **Governance must be at execution layer** — not application level. Config-based governance = "suggestions the agent can override."
3. **Distribution's unsolved problem is credentials** — not packaging. OAuth flows for local agents are the real bottleneck.
4. **Skills are commoditizing** — value shifting to curation, architecture, and domain judgment
5. **The "early internet" analogy is consensus** — multiple independent threads compare current state to pre-app-store web
