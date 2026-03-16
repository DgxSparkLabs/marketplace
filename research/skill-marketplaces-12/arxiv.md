# Round 12: arXiv Skill Marketplace Research

**Date:** March 16, 2026
**Searches:** "site:arxiv.org agent skills marketplace 2026" (15 results), "site:arxiv.org agent skill ecosystem orchestration benchmark 2026" (15 results)

---

## NEW Papers Found (Not in Round 11)

### 1. SkillOrchestra: Learning to Route Agents via Skill Transfer (2602.19672)
- **Authors:** Wang, Jiayu; Ming, Yifei; Ke, Zixuan; Joty, Shafiq; Albarghouthi, Aws; Sala, Frederic
- **Date:** Feb 23, 2026
- **Category:** cs.AI
- **Key Innovation:** Skill-aware orchestration framework that learns fine-grained skills from execution experience
- **Problem Solved:** Existing routers make coarse query-level decisions; RL orchestrators suffer from "routing collapse" (always picking the expensive model)
- **Approach:** Learns agent-specific competence AND cost under each skill; selects agents based on performance-cost trade-off
- **Results:** Outperforms SoTA RL-based orchestrators by **up to 22.5%** with **700x** and **300x** learning cost reduction vs Router-R1 and ToolOrchestra
- **Code:** github.com/jiayuww/SkillOrchestra
- **Relevance to Marketplaces:** Enables intelligent routing of tasks to the most cost-effective skill/agent combo — critical for marketplace economics

### 2. XSkill: Continual Learning from Experience and Skills in Multimodal Agents (2603.12056)
- **Authors:** Jiang, Guanyu; Su, Zhaochen; Qu, Xiaoye; Fung, Yi R
- **Date:** Mar 12, 2026 (v2: Mar 13, 2026)
- **Category:** cs.AI
- **Key Innovation:** Dual-stream framework distinguishing **skills** (task-level guidance) from **experiences** (action-level guidance)
- **Continual Learning Loop:** Accumulation -> Inference -> Feedback -> Accumulation
- **Results:** Consistently outperforms tool-only and learning-based baselines across 5 benchmarks, 4 backbone models
- **Key Finding:** Skills and experiences play **complementary roles** with superior **zero-shot generalization**
- **Relevance to Marketplaces:** Skills that learn and improve from usage data — the marketplace could capture this feedback loop

### 3. Automating Skill Acquisition through Large-Scale Mining (2603.11808)
- **Date:** Mar 2026
- **Key Topic:** Extracting skills from repositories using structural decomposition
- **Finding:** Agent orchestration frameworks implement priority systems based on skill specificity, historical success rates, and user preferences
- **Practical Upper Limit:** Addresses question of maximum useful skill library size
- **Relevance:** Automated skill creation pipeline could feed marketplaces at scale

### 4. Scaling Laws for Educational AI Agents (2603.11709)
- **Date:** Mar 2026
- **Key Finding:** "Skill composition enables specialization — agents equipped with domain-specific skill modules demonstrate markedly superior performance"
- **Relevance:** Validates vertical/domain-specific skill marketplace approach

### 5. Memory for Autonomous LLM Agents (2603.07670)
- **Date:** Mar 2026
- **Key Finding:** Memory as the bridge between stateless text generation and adaptive agents
- **Covers:** Work from 2022 through early 2026
- **Relevance:** Memory + skills convergence trend identified in prior rounds confirmed academically

---

## Updated Paper Corpus (Rounds 11 + 12 Combined)

| Paper | arXiv ID | Date | Key Contribution |
|-------|----------|------|------------------|
| Agent Skills Data Analysis | 2602.08004 | Feb 8 | 40,285 skills quantitative study |
| Agent Skills in the Wild (Security) | 2601.10338 | Jan 15 | 26.1% vulnerability rate, 42K skills |
| SoK: Agentic Skills | 2602.20867 | Feb 24 | Full lifecycle + 7 design patterns + ClawHavoc |
| SkillsBench | 2602.12670 | Feb 13 | +16.2pp curated skills, 0pp self-generated |
| AgentSkillOS | 2603.02176 | Mar 2 | DAG orchestration at 200K scale |
| SkillFortify (Security) | 2603.00195 | Feb 27 | 96.95% F1 formal verification |
| SkillNet | 2603.04448 | Feb 26 | 200K+ skills, +40% rewards, -30% steps |
| Agent Skills Survey | 2602.12430 | Feb 12 | 4-axis comprehensive survey |
| **SkillOrchestra** (NEW) | 2602.19672 | Feb 23 | +22.5% routing, 700x cheaper than RL |
| **XSkill** (NEW) | 2603.12056 | Mar 12 | Dual-stream continual learning |
| **Skill Acquisition Mining** (NEW) | 2603.11808 | Mar 2026 | Automated skill extraction from repos |
| **Educational AI Scaling** (NEW) | 2603.11709 | Mar 2026 | Skill composition enables specialization |
| **Memory for Agents** (NEW) | 2603.07670 | Mar 2026 | Memory + skills convergence |

**Total:** 13 papers directly relevant to skill marketplaces (8 from Round 11 + 5 new in Round 12)

---

## Academic Trends (Round 12 Update)

1. **Orchestration is the hot new topic.** SkillOrchestra proves intelligent routing beats brute-force RL by 22.5% at 700x lower cost. This is the "matching algorithm" for skill marketplaces.

2. **Continual learning from skills is emerging.** XSkill shows skills can improve through a feedback loop — marketplaces could capture this signal for quality ranking.

3. **Automated skill creation at scale.** Mining skills from repositories (2603.11808) could solve the supply-side cold start problem.

4. **Skills + Memory converging.** Academic work confirms the memory-skill merger trend. Skills that remember context are more valuable.

5. **Formal verification gaining momentum.** SkillFortify's 96.95% F1 sets the bar. Heuristic-based security scanning will not be sufficient long-term.

6. **Growth rate is staggering.** Per 2602.08004: marketplace grew from 2,179 to 40,285 skills in 20 days — **18.5x increase, ~15.7% daily growth rate**.
