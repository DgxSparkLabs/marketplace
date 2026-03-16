# ArXiv Findings — Round 3

> Focus: MCP security papers, skill benchmarking, agent protocol threat modeling, skill acquisition automation

## Papers Not Covered in Rounds 1-2

### 1. SkillsBench — Benchmarking How Well Agent Skills Work (2602.12670)
- **Authors:** Li, Xiangyi et al. (30+ authors)
- **Date:** Feb 13, 2026 (v3: Mar 13, 2026)
- **License:** CC BY 4.0

**Key findings:**
- 86 tasks across 11 domains with curated Skills and deterministic verifiers
- 7 agent-model configurations tested over **7,308 trajectories**
- Curated Skills raise average pass rate by **+16.2 percentage points (pp)**
- Domain variance is enormous: +4.5pp (Software Engineering) to **+51.9pp (Healthcare)**
- **16 of 84 tasks show negative deltas** — Skills can hurt performance
- **Self-generated Skills provide NO benefit on average** — models cannot reliably author the procedural knowledge they benefit from consuming
- Focused Skills with **2-3 modules outperform comprehensive documentation**
- **Smaller models with Skills can match larger models without them**

**Implications for our marketplace:**
- Quality curation matters more than quantity — confirms our approach
- The 2-3 module sweet spot validates focused, modular skill design
- Self-generation failures mean human-authored skills retain value
- Negative deltas on 19% of tasks = need for per-domain evaluation (like waza provides)

---

### 2. Breaking the Protocol — MCP Security Analysis (2601.17549)
- **Authors:** Maloyan, Narek; Namiot, Dmitry
- **Date:** Jan 24, 2026
- **License:** CC BY 4.0

**Key findings:**
- First formal security analysis of MCP's architectural design
- Three fundamental protocol-level vulnerabilities identified:
  1. **Absence of capability attestation** — servers can claim arbitrary permissions
  2. **Bidirectional sampling without origin authentication** — server-side prompt injection
  3. **Implicit trust propagation** in multi-server configurations
- **MCPBench** framework: 847 attack scenarios across 5 MCP server implementations
- MCP architectural choices **amplify attack success rates by 23-41%** compared to non-MCP integrations
- **MCPSec** proposed: backward-compatible extension adding capability attestation + message authentication
- Attack success reduced from **52.8% to 12.4%** with 8.3ms median latency overhead
- **Conclusion:** "MCP's security weaknesses are architectural rather than implementation-specific, requiring protocol-level remediation"

**Implications:**
- Skills operating via MCP inherit these architectural vulnerabilities
- Our `allowed-tools` restrictions become critical defense layer
- MCPSec adoption should be tracked — may become standard

---

### 3. SMCP: Secure Model Context Protocol (2602.01129)
- **Authors:** Hou, Xinyi et al.
- **Date:** Feb 1, 2026

**Key contributions:**
- **Comprehensive threat catalog:** unauthorized access, tool poisoning, prompt injection, privilege escalation, supply chain attacks
- **SMCP adds 5 security layers:**
  1. Unified identity management
  2. Robust mutual authentication
  3. Ongoing security context propagation
  4. Fine-grained policy enforcement
  5. Comprehensive audit logging
- Practical examples demonstrating risk reduction

**Significance:** Proposes the most complete protocol-level security enhancement to MCP found in literature

---

### 4. Security Threat Modeling for AI-Agent Protocols (2602.11327)
- **Authors:** Anbiaee, Zeynab et al.
- **Date:** Feb 11, 2026

**Key contributions:**
- Comparative analysis of **4 protocols:** MCP, Agent2Agent (A2A), Agora, Agent Network Protocol (ANP)
- **12 protocol-level risks** identified across creation, operation, and update phases
- Qualitative risk assessment framework with likelihood × impact scoring
- **MCP case study:** Formalizes risk of missing validation for executable components
- Quantifies wrong-provider tool execution under multi-server composition
- **First cross-protocol security comparison** in literature

**Implications:** As skills interact with multiple protocols (MCP for tools, A2A for agent-to-agent), cross-protocol attack surfaces multiply

---

### 5. MCPSecBench — Security Benchmark (2508.13220)
- **Authors:** Yang, Yixuan et al.
- **Date:** Aug 17, 2025 (v3: Feb 12, 2026)

**Key contributions:**
- First formalization of a secure MCP and its required specifications
- **17 distinct attack types** across **4 primary attack surfaces**
- Modular benchmark with prompt datasets, MCP servers/clients, attack scripts, GUI test harness
- **All attack surfaces yield successful compromises** on Claude, OpenAI, and Cursor
- Core vulnerabilities universally affect all platforms
- **Current protection mechanisms achieve <30% success rate**
- "MCPSecBench standardizes the evaluation of MCP security and enables rigorous testing across all protocol layers"

**Implications:** The security testing infrastructure for MCP is maturing fast — relevant if we build MCP server integration

---

### 6. Automating Skill Acquisition from Repositories (2603.11808)
- **Authors:** Bi, Shuzhen et al.
- **Date:** Mar 12, 2026

**Key contributions (building on Round 2 mention):**
- Framework for automated skill extraction from open-source repos to SKILL.md format
- Repository structural analysis + semantic skill identification via dense retrieval
- Applied to TheoremExplainAgent and Code2Video (Manim mathematical animation)
- **40% gains in knowledge transfer efficiency** while maintaining pedagogical quality
- Combined with security governance and multi-dimensional evaluation metrics
- "Enables scalable acquisition of procedural knowledge that augments LLM capabilities without requiring model retraining"

**Significance:** Automated skill mining is becoming a viable pipeline — but SkillsBench shows self-generated skills provide no average benefit, creating tension with this approach

---

## MCP Security Paper Landscape (cumulative across all rounds)

| Paper | ID | Date | Focus |
|---|---|---|---|
| MCP Landscape Survey | 2503.23278 | Mar 2025 | Comprehensive MCP survey |
| Enterprise-Grade MCP Security | 2504.08623 | Apr 2025 | Threat modeling + security patterns |
| Securing MCP | 2511.20920 | Nov 2025 | Dynamic trust, new attack vectors |
| MCPSecBench | 2508.13220 | Aug 2025 | Benchmark: 17 attacks, 4 surfaces |
| Breaking the Protocol | 2601.17549 | Jan 2026 | Formal analysis, MCPSec extension |
| SMCP | 2602.01129 | Feb 2026 | Secure protocol extension |
| MCP Tool Descriptions Are Smelly | 2602.14878 | Feb 2026 | Tool description quality |
| Protocol Threat Modeling | 2602.11327 | Feb 2026 | Cross-protocol comparison (MCP/A2A/Agora/ANP) |
| Prompt Injection on Coding Assistants | 2601.17548 | Jan 2026 | Agent coding tool attacks |

**Total:** 9 MCP security papers in 12 months — academic community treating this as a critical research area.

## Key Takeaways

1. **Skills demonstrably help (+16.2pp average)** but can hurt on specific tasks (19% negative delta) — evaluation is essential
2. **Self-generated skills don't work** — human curation retains value, automated generation faces fundamental limitations
3. **MCP has architectural security flaws** — 52.8% attack success rate, amplifies attacks 23-41% vs non-MCP
4. **Security defenses are failing** — current protections achieve <30% success rate across platforms
5. **Protocol-level fixes exist** (MCPSec, SMCP) but require ecosystem-wide adoption
6. **The skill mining → SKILL.md pipeline is technically viable** but quality remains unproven at scale
