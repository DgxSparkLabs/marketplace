# Skill Marketplaces Research — Round 3 Summary

> Date: March 16, 2026
> Focus: Package management, skill evaluation, MCP security, enterprise tooling, ecosystem maturation

## Executive Summary

Round 3 reveals three seismic shifts since Rounds 1-2:

1. **Package management is here.** Three independent implementations (skillpm, FastSkill, Vercel skills CLI) plus an RFC (skills.json manifest) are building the npm/pip equivalent for agent skills. Dependency resolution, semver, lock files, and transitive MCP server configuration are now real.

2. **Evaluation is formalizing.** SkillsBench (86 tasks, 7,308 trajectories) proves curated skills help (+16.2pp average) but self-generated skills provide zero benefit. Microsoft's `waza` CLI establishes eval-driven development as the standard. These findings validate quality curation over volume.

3. **MCP has architectural security flaws.** Nine academic papers document 17 attack types, 52.8% attack success rates, and <30% effectiveness of current protections. The security crisis is no longer limited to malicious skills — the protocol itself amplifies attacks by 23-41%.

## What's New Since Rounds 1-2

### GitHub — 12 New Repos/Tools

| Repo | Category | Significance |
|---|---|---|
| **microsoft/waza** | Evaluation | Official Microsoft CLI for skill quality measurement |
| **skillpm** | Package management | npm-based with transitive dependencies + MCP config |
| **FastSkill** | Package management | Registry + semantic search + lock files + Web UI |
| **neovateai/agent-skill-npm-boilerplate** | Distribution | Template for skills as npm packages |
| **cathy-kim/skill-semver** | Versioning | Automatic semver for skills |
| **agentskills discussions/210** | Standards | RFC: skills.json manifest for dependency resolution |
| **jkitchin/skillz** | CLI management | Cross-platform skill manager (Claude/OpenCode/Codex/Gemini) |
| **LerianStudio/ring** | Workflow enforcement | 83 skills + 37 agents, mandatory quality gates |
| **sickn33/antigravity-awesome-skills** | Collection | 1,259+ skills with bundles and npx installer |
| **tiny-agent-skills** | Small models | SKILL.md for 2B-7B local models via auto-compilation |
| **HoangNguyen0403/agent-skills-standard** | Standards | Engineering standards as cross-agent skills |
| **fugazi/test-automation-skills-agents** | QA | QA automation skills library |

### ArXiv — 6 New Papers

| Paper | ID | Key Finding |
|---|---|---|
| **SkillsBench** | 2602.12670 | Curated skills +16.2pp; self-generated = 0; 2-3 modules optimal |
| **Breaking the Protocol** | 2601.17549 | MCP amplifies attacks 23-41%; MCPSec reduces to 12.4% |
| **SMCP** | 2602.01129 | Secure MCP with 5 security layers |
| **Protocol Threat Modeling** | 2602.11327 | Cross-protocol comparison: MCP/A2A/Agora/ANP; 12 risks |
| **MCPSecBench** | 2508.13220 | 17 attack types; protections <30% effective |
| **Skill Acquisition Mining** | 2603.11808 | Automated SKILL.md extraction; 40% knowledge transfer gain |

### Twitter/X — New Patterns
- Google Antigravity officially announces agent skills support
- Vercel skills.sh: 110K+ installs in 4 days, 147 new skills/day
- Multi-agent skill composition emerging (45-subagent skills)
- Anthropic publishes 32-page skill authoring guide
- Manus AI (Meta-backed) adopts agent skills standard
- Skill-specific reputation scoring discussed in 22K-member community

### Reddit — Documented Incidents
- 6 CVEs in 2026, 824+ malicious skills (up from 341), 42K exposed instances
- capability-evolver (14K downloads) exfiltrating to ByteDance/Feishu — first state-adjacent targeting
- r/better_claw maintains ongoing ClawHavoc campaign timeline
- Community consensus: unaudited marketplaces are fundamentally unsafe

### Kaggle
- No direct marketplace activity
- Benchmark datasets (SWE-Bench, AI Models 2026) useful for skill evaluation
- Google's agent evaluation methodology from 5-Day course applicable to skills

---

## Three New Ecosystem Layers

### Layer 1: Package Management
The skill ecosystem is rapidly developing its "package infrastructure moment":

```
Skill Author → Package (SKILL.md + package.json/manifest) → Registry → Install CLI → Agent Dirs
```

**Current implementations:**

| Tool | Approach | Registry | Dependencies | MCP Config |
|---|---|---|---|---|
| **Vercel skills CLI** | `npx skills add` | skills.sh | Via npm | No |
| **skillpm** | npm orchestration | npmjs.org | Transitive | Yes (transitive) |
| **FastSkill** | Custom binary | Self-hosted | Manifest + lock | No |
| **npm-boilerplate** | npm template | npmjs.org | Standard npm | No |

**Observation:** The ecosystem hasn't converged on one approach yet. Vercel has adoption momentum (235K+ weekly installs for find-skills), but skillpm has the most complete feature set (transitive deps + MCP config).

### Layer 2: Evaluation & Quality
Two complementary approaches are emerging:

1. **Academic benchmarking** (SkillsBench): Domain-specific evaluation across 11 domains with deterministic verifiers. Proves skills work but shows massive variance.
2. **Developer tooling** (microsoft/waza): Eval-driven development workflow — scaffold evals from SKILL.md, run benchmarks, compare across models, check readiness.

**Key insight from SkillsBench:** Self-generated skills provide no benefit on average. This means automated skill generation (which Rounds 1-2 flagged as a trend) faces a fundamental quality ceiling. Human curation retains value.

### Layer 3: Security Infrastructure
The Snyk + Vercel partnership (Feb 17, 2026) is the first production supply chain security integration:

- Every `npx skills add` triggers real-time Snyk scanning
- Multi-layer: code analysis + LLM-based judges for prompt injection
- CRITICAL detectors: 90-100% recall, 0% false positive on top 100
- "Security Verified" badge on skills.sh
- Built on agent-scan/mcp-scan from Invariant Labs (ETH Zurich)

**The security paper landscape is dense:**
- 9 MCP security papers in 12 months
- 17 distinct attack types documented
- All major platforms (Claude, OpenAI, Cursor) vulnerable
- Current protections achieve <30% effectiveness
- Protocol-level fixes proposed but require ecosystem adoption

---

## Updated Competitive Position

### What we have that others don't (unchanged)
- Dual skills + rules format
- Cross-platform install scripts with idempotency + collision detection
- 104 automated tests
- PEP 723 zero-install Python scripts
- Global install rules

### What the ecosystem added since Round 2

| Capability | Who Has It | Our Gap |
|---|---|---|
| **Transitive dependency resolution** | skillpm, FastSkill | We have no dependency system |
| **Eval-driven development** | waza, SkillsBench | We have tests but no eval framework |
| **Real-time security scanning** | Snyk + Vercel | We have no scanning integration |
| **Semantic version management** | skill-semver, skillpm | Our skills aren't versioned |
| **Semantic search for skills** | FastSkill | We have no search |
| **Lock files for reproducible installs** | FastSkill | We have no lock system |
| **Package manager CLI** | skillpm, FastSkill, npx skills | We have install.sh |
| **Workflow enforcement agents** | Ring (37 agents) | We have rules but no review agents |
| **Skills for small local models** | tiny-agent-skills | Not our focus but notable |
| **Multi-agent orchestration skills** | Ring, antigravity | We have single-agent skills |

### What we have that's newly validated

| Our Feature | Validation |
|---|---|
| **Curated, human-authored skills** | SkillsBench: self-generated = 0 benefit |
| **Focused, modular skills** | SkillsBench: 2-3 modules > comprehensive docs |
| **`allowed-tools` restrictions** | MCP papers: architectural flaws amplify attacks 23-41% |
| **Test infrastructure** | waza establishes eval-driven development as standard |
| **Quality over quantity** | Community consensus: unaudited marketplaces unsafe |

---

## Updated Recommendations

### Immediate (validated by Round 3 findings)

1. **Add `agents/openai.yaml` support** — still the top gap (unchanged from Rounds 1-2)
2. **Add version metadata to skills** — the ecosystem is moving to semver; we should at minimum add `version:` to SKILL.md frontmatter
3. **Document security posture** — our `allowed-tools` and test infrastructure are now validated defensive measures; write a SECURITY.md

### Short-term (new from Round 3)

4. **Evaluate waza integration** — microsoft/waza provides eval-driven development; could use it to validate our skills
5. **Add skill dependency declarations** — even a simple `requires:` field in SKILL.md frontmatter would enable future dependency resolution
6. **Publish to skills.sh** — Vercel's directory has adoption momentum; publishing there gets visibility + free Snyk security scanning
7. **Build a security scanning skill** — using Snyk's open-source mcp-scan/agent-scan as the engine

### Medium-term (strategic)

8. **Consider skillpm/FastSkill compatibility** — if the ecosystem converges on npm-based distribution, our skills should be publishable as npm packages
9. **Build workflow enforcement skills** (like Ring) — mandatory quality gates, review checklists, TDD enforcement
10. **Track MCP security standardization** — MCPSec (2601.17549) and SMCP (2602.01129) may become standards; prepare to support them

### Do NOT do (validated)
- **Don't auto-generate skills** — SkillsBench proves self-generated skills provide zero average benefit
- **Don't chase volume** — 1,259-skill collections exist; quality + testing + security is the differentiator
- **Don't ignore MCP security** — the protocol has architectural flaws that skills inherit

---

## Research Coverage Across All 3 Rounds

| Platform | Round 1 | Round 2 | Round 3 | Total Unique Items |
|---|---|---|---|---|
| GitHub repos | 8 | 40+ | 12 new | 60+ |
| ArXiv papers | 4 | 4 new | 6 new | 14 |
| Web marketplaces | 12 | 12 (same) | — (covered) | 12+ |
| Twitter/X signals | 5 | 7 | 8 new | 20+ |
| Reddit threads | 5 | 5 | 6 new | 16 |
| Kaggle | 2 | 3 | 5 | 5 |
| Industry reports | — | 1 (Snyk) | 1 (Snyk+Vercel) | 2 |

### Cumulative Key Metrics

| Metric | Value | Source |
|---|---|---|
| Skills on SkillsMP | 400K+ | SkillsMP |
| Skills analyzed (security) | 98K+ | ArXiv 2601.10338 |
| Skills on skills.sh | Growing at 147/day | Snyk blog |
| Vulnerability rate | 26-36% | ArXiv + Snyk |
| Confirmed malicious | 76-824+ | Snyk + Reddit |
| MCP attack success rate | 52.8% | ArXiv 2601.17549 |
| Skill benefit (average) | +16.2pp | ArXiv 2602.12670 |
| Self-generated skill benefit | 0pp | ArXiv 2602.12670 |
| Agents supporting SKILL.md | 20+ | Community tracking |
| MCP security papers | 9 | ArXiv |
| Package managers for skills | 4 | GitHub |

---

## Files in This Directory

| File | Lines | Content |
|---|---|---|
| github.md | ~200 | 12 new repos: waza, skillpm, FastSkill, Ring, tiny-agent-skills, etc. |
| arxiv.md | ~170 | 6 new papers: SkillsBench, MCP security (4), skill mining |
| twitter.md | ~100 | Skill composition, Vercel npm-moment, Google Antigravity, Manus AI |
| reddit.md | ~100 | Security incidents: 6 CVEs, ByteDance exfil, ClawHavoc timeline |
| kaggle.md | ~60 | Benchmarks, agent evaluation, SWE-Bench |
| SUMMARY.md | this file | Synthesis across all platforms |
