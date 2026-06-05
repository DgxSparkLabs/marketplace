# Skill Marketplaces Research — Round 4 Summary

> Date: March 16, 2026
> Focus: Governance, enterprise deployment, skill orchestration, self-evolving skills, agent distribution

## Executive Summary

Round 4 reveals the ecosystem crossing from developer tooling into enterprise infrastructure:

1. **Governance is the enterprise gate.** Microsoft's agent-governance-toolkit (6,100+ tests, OWASP 10/10, sub-millisecond policy enforcement) sets the standard. Enterprise adoption requires runtime governance at the execution layer — not application-level suggestions the agent can override.

2. **Skill orchestration via DAGs outperforms flat invocation.** AgentSkillOS (2603.02176) proves structured composition is the key to unlocking skill potential, tested from 200 to 200K skills. Tree-based retrieval approximates oracle skill selection.

3. **Self-evolving skills can work — with the right methodology.** EvoSkill (+7.3% to +12.1%) shows iterative failure analysis + Pareto selection produces transferable skills, nuancing SkillsBench's finding that naive self-generation provides zero benefit.

4. **The enterprise deployment pattern has crystallized.** Admin-curated catalog → engineer approval → permission-based sharing → auditable execution → skill promotion. Multiple independent sources (Reddit, Etienne, TeamCopilot) converge on the same pattern.

## What's New Since Rounds 1-3

### GitHub — 10+ New Repos/Tools

| Repo | Category | Significance |
|---|---|---|
| **microsoft/agent-governance-toolkit** | Governance | OWASP 10/10, 6,100+ tests, Python/TS/.NET |
| **microsoft/skills** | Enterprise catalog | 132 skills for Azure SDKs across 6 languages |
| **reflectt/agent-identity-governance-kit** | Identity | Crypto identity + RBAC, SOC 2/GDPR/HIPAA |
| **dash0hq/agent-skills** | Observability | OpenTelemetry skills across 8 languages |
| **BulloRosso/etienne** | Enterprise harness | RBAC, skill catalog curation, artifact collaboration |
| **mukul975/Anthropic-Cybersecurity-Skills** | Vertical | 611+ cybersecurity skills, MITRE ATT&CK mapped |
| **anthropics/skills#412** | Governance proposal | Community requesting governance skill patterns |
| **4th/Azure_GRC** | Governance | PolicyEngine + SkillRegistry + RAG Safety |
| **orosha-ai/agent-observability-dashboard** | Observability | Production-grade agent monitoring |
| **ColeMurray/claude-code-otel** | Observability | Claude Code cost + usage tracking |

### ArXiv — 6 New Papers

| Paper | ID | Key Finding |
|---|---|---|
| **AgentSkillOS** | 2603.02176 | DAG orchestration >> flat invocation; tested 200-200K skills |
| **EvoSkill** | 2603.02766 | Self-evolving skills via failure analysis; +7.3% to +12.1%; zero-shot transfer works |
| **SLM Skill Framework** | 2602.16653 | 12B-30B = sweet spot; tiny models fail skill selection; 80B matches frontier |
| **FormalJudge** | 2602.11136 | Formal verification: 7B judge polices 72B agent with 90%+ accuracy |
| **Agent Economy** | 2602.14219 | Blockchain foundation for agent economic autonomy (IoA) |
| **TARSE** | 2603.01241 | Test-time skill retrieval for model adaptation |

### Twitter/X — Discourse Shifts
- Curation > quantity as explicit consensus
- Enterprise B2B/B2C market split crystallizing
- Adoption S-curve: 3% (early 2025) → 12% (March 2026) → projected 30-40% (2027)
- Value shifting from tools to business outcomes

### Reddit — Enterprise Realities
- Real 300+ person enterprise deployment described (TeamCopilot.ai)
- Governance must be at execution layer, not application level
- Distribution's unsolved problem is credentials, not packaging
- Skills commoditizing — value moving to curation and domain judgment

### Kaggle — Agentic Competitions Emerging
- First explicitly "agentic" competition (legal information retrieval)
- Multi-agent solvers in competitive settings
- Benchmark datasets accumulating

---

## The Enterprise Deployment Model

Converged from 4 independent sources (Reddit/TeamCopilot, Etienne, Microsoft governance toolkit, identity kit):

```
1. AUTHOR  → Business expert + engineer co-create skill
2. REVIEW  → Admin/engineer approves skill (security + quality check)
3. PUBLISH → Skill enters curated company catalog (skill store)
4. DISCOVER → Business users browse approved skills per project
5. EXECUTE → Agent runs skill with permission-based tool access
6. AUDIT   → All actions logged to immutable, non-deletable audit trail
7. PROMOTE → Successful project skills promoted to org-wide catalog
```

**Critical design principle:** "Controls must be underneath, not at application level." — u/GarbageOk5505

**Implementation pattern:** Isolated runtime with explicitly granted network/filesystem/API access per agent. Agent cannot override policy.

---

## Updated Competitive Position

### New gaps identified in Round 4

| Capability | Who Has It | Our Status |
|---|---|---|
| **Runtime governance** | microsoft/agent-governance-toolkit | No enforcement layer |
| **OWASP Agentic compliance** | microsoft/agent-governance-toolkit | Not mapped |
| **Cryptographic agent identity** | reflectt kit, AgentMesh | Not applicable (file-based) |
| **DAG-based skill orchestration** | AgentSkillOS | Flat invocation only |
| **Enterprise skill catalog workflow** | Etienne, TeamCopilot | No admin approval flow |
| **Observability integration** | Dash0, ColeMurray | No OTel skills |
| **Vertical domain specialization** | Cybersecurity Skills (611+) | General-purpose only |
| **Self-evolving skill generation** | EvoSkill | No evolutionary mechanism |
| **MITRE ATT&CK mapping** | Cybersecurity Skills | No security framework mapping |

### Our advantages that remain strong

| Our Feature | Round 4 Validation |
|---|---|
| **Dual skills + rules** | No other marketplace has both |
| **Cross-platform install** | Microsoft uses `npx skills add` — install scripts are the norm |
| **104 automated tests** | Governance toolkit has 6,100+ — our test infra is right direction but needs expansion |
| **Quality over quantity** | "Context rot" warning from Microsoft validates selective loading |
| **PEP 723 scripts** | No one else has zero-install Python scripts |
| **Focused, modular design** | 12B-30B models benefit substantially; tiny models fail — focused skills serve more models |

---

## Updated Recommendations

### Immediate (from Round 4)

1. **Map to OWASP Agentic Top 10** — document how our `allowed-tools` and test infrastructure address each ASI category
2. **Add `version:` field to SKILL.md frontmatter** — ecosystem converging on semver (Microsoft, skillpm, skill-semver all use it)
3. **Consider vertical specialization** — 611 cybersecurity skills demonstrates domain-focused collections have clear value. Pick a domain (DevSecOps? Observability? Infrastructure?) and go deep

### Short-term (building on all 4 rounds)

4. **Build an observability skill** — Dash0 proves observability vendors see skills as distribution channel. An OpenTelemetry instrumentation skill would be high-value
5. **Document the enterprise deployment model** — the admin-approval → catalog → permission flow is the pattern. Even if we don't implement it, documenting how our skills fit into it helps enterprise adoption
6. **Publish to skills.sh** — still the highest-leverage distribution action (Snyk scanning included free)

### Medium-term (strategic insights from 4 rounds)

7. **DAG-based skill composition** — AgentSkillOS proves DAGs outperform flat invocation. Consider adding `depends-on:` or `composes-with:` metadata
8. **Evaluate EvoSkill methodology** — iterative failure analysis + Pareto selection for skill improvement could be applied to our existing skills
9. **Consider governance-as-a-skill** — the anthropics/skills#412 proposal shows demand; we could build governance patterns as a skill or rule

### Do NOT do (cumulative across all rounds)
- Don't auto-generate skills naively (SkillsBench: zero benefit) — EvoSkill's iterative approach is the only validated path
- Don't chase volume (context rot warning from Microsoft)
- Don't ignore MCP security (architectural flaws, 52.8% attack success)
- Don't build app-level governance (execution-layer is the only approach that works)

---

## Research Coverage — All 4 Rounds

| Platform | R1 | R2 | R3 | R4 | Total Unique |
|---|---|---|---|---|---|
| GitHub repos | 8 | 40+ | 12 | 10+ | 70+ |
| ArXiv papers | 5 | 4 | 6 | 6 | 21 |
| Web marketplaces | 12 | — | — | — | 12+ |
| Twitter/X signals | 5 | 7 | 8 | 6 | 26+ |
| Reddit threads | 5 | 5 | 6 | 5 | 21 |
| Kaggle | 2 | 3 | 5 | 5 | 8 |
| Industry reports | — | 1 | 1 | — | 2 |

### Cumulative Key Metrics

| Metric | Value | Source |
|---|---|---|
| Skills on SkillsMP | 400K+ | SkillsMP |
| Microsoft enterprise skills | 132 | microsoft/skills |
| Cybersecurity skills | 611+ | Anthropic-Cybersecurity-Skills |
| Skills on skills.sh | Growing at 147/day | Snyk blog |
| Vulnerability rate | 26-36% | ArXiv + Snyk |
| MCP attack success rate | 52.8% | ArXiv 2601.17549 |
| Curated skill benefit (average) | +16.2pp | SkillsBench |
| DAG orchestration benefit | Substantial vs flat | AgentSkillOS |
| Self-evolved skill benefit | +7.3% to +12.1% | EvoSkill |
| SLM skill sweet spot | 12B-30B parameters | 2602.16653 |
| Agents supporting SKILL.md | 20+ | Community |
| Governance tests | 6,100+ | microsoft/agent-governance-toolkit |
| ArXiv papers (total) | 21 | All rounds |

---

## Files in This Directory

| File | Lines | Content |
|---|---|---|
| github.md | ~170 | Governance toolkits, Microsoft 132 skills, observability, cybersecurity vertical, enterprise harness |
| arxiv.md | ~145 | AgentSkillOS, EvoSkill, SLM Framework, FormalJudge, Agent Economy, TARSE |
| twitter.md | ~55 | Curation signal, B2B/B2C split, adoption S-curve, business value shift |
| reddit.md | ~120 | Enterprise 300-person deployment, execution-layer governance, credential problem, skills commoditizing |
| kaggle.md | ~50 | Agentic competitions, LLM benchmarks, multi-agent solvers |
| SUMMARY.md | this file | Synthesis, enterprise deployment model, recommendations |
