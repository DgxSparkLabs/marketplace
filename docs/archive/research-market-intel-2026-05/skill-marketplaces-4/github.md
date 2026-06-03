# GitHub Findings — Round 4

> Focus: Governance toolkits, observability skills, enterprise skill catalogs, agent distribution, self-evolving frameworks

## 1. Agent Governance

### microsoft/agent-governance-toolkit — Runtime Governance for AI Agents
- **URL:** https://github.com/microsoft/agent-governance-toolkit
- **Date:** 2026-03-02
- **Description:** "The only toolkit covering all 10 OWASP Agentic risks with 6,100+ tests"
- **Languages:** Python, TypeScript, .NET (PyPI, npm, NuGet)
- **Key components:**
  - **Agent OS Kernel** — deterministic policy enforcement (<0.1ms per evaluation), capability model, audit logging, MCP gateway
  - **AgentMesh** — Ed25519 cryptographic identity, SPIFFE/SVID credentials, trust scoring (0-1000 scale), protocol bridges (A2A/MCP/IATP)
  - **Agent Runtime** — 4-tier privilege rings, saga orchestration, termination control, kill switch, append-only audit log
  - **Agent SRE** — SLOs, error budgets, replay debugging, chaos engineering, circuit breakers, progressive delivery
  - **Agent Marketplace** — plugin marketplace with compliance & attestation
- **Framework integrations:** LangChain, CrewAI, AutoGen, Dify, LlamaIndex, OpenAI Agents, Google ADK, Microsoft Agent Framework (12+)
- **OWASP coverage:** 10/10 Agentic Top 10 (ASI-01 through ASI-10)
- **NIST mapping:** Mapped to NIST AI Agent Security RFI (2026-00206)
- **Significance:** Most comprehensive open-source governance toolkit. The `allowed_tools` + `denied_tools` pattern mirrors our approach but with runtime enforcement at sub-millisecond latency

### reflectt/agent-identity-governance-kit
- **URL:** https://github.com/reflectt/agent-identity-governance-kit
- **Date:** 2026-02-05
- **Problem:** "Shadow AI epidemic where 1-17 agents per employee run ungoverned in enterprises"
- **Features:**
  - RSA-2048 key pairs per agent with rotation + audit trail
  - RBAC with granular permissions (5 predefined roles: readonly, standard, developer, admin, compliance)
  - Immutable audit trails with cryptographic verification
  - SOC 2, GDPR, HIPAA compliance patterns
  - Approval gates for sensitive operations
  - Rate limiting and quotas per role

### anthropics/skills issue #412 — agent-governance skill proposal
- **URL:** https://github.com/anthropics/skills/issues/412
- **Significance:** Community requesting governance patterns as a skill — safety patterns for AI agent systems including policy enforcement, threat detection, trust scoring, audit trails

### 4th/Azure_GRC — Policy-driven Agentic AI Governance
- **URL:** https://github.com/4th/Azure_GRC
- **Features:** PolicyEngine, SkillRegistry, RAG Safety Envelopes, Constraint Evaluators, evidence-based compliance automation

## 2. Microsoft Skills — Official Enterprise Catalog

### microsoft/skills — 132 Skills for Azure SDKs
- **URL:** https://github.com/microsoft/skills
- **Date:** 2026-01-16
- **Scale:** 132 skills across 6 languages (Python 41, .NET 28, TypeScript 25, Java 25, Rust 7, Core 9)
- **Installation:** `npx skills add microsoft/skills` (wizard-based selection)
- **Architecture:**
  - Flat structure with language suffixes for automatic discovery
  - Plugins (deep-wiki, azure-skills, etc.)
  - Custom agents (backend, frontend, infrastructure, planner)
  - AGENTS.md templates
  - MCP server configurations
- **Key categories:** Foundry & AI (7), AI Services (8), Data & Storage (7), Security & Identity (4), Messaging (6), DevOps (4)
- **Design principle:** "Use skills selectively. Loading all skills causes context rot: diluted attention, wasted tokens, conflated patterns."
- **Significance:** Microsoft now ships 132 enterprise skills — largest vendor-curated collection. The "context rot" warning validates focused skill design

## 3. Observability Skills

### dash0hq/agent-skills — OpenTelemetry Skills
- **URL:** https://github.com/dash0hq/agent-skills
- **Date:** 2026-02-24
- **What:** OpenTelemetry instrumentation skills for AI coding assistants
- **Covers:** Node.js, Go, Python, Java, .NET, Ruby, PHP, Browser, Next.js
- **Features:**
  - Semantic conventions adherence
  - Instrumentation Score specification alignment
  - Collector pipeline configuration (traces, metrics, logs)
  - OTTL expression guidance
  - High-cardinality metric optimization
- **Significance:** First commercial observability vendor creating agent skills — enterprise observability companies entering the skills ecosystem

### Additional observability projects found:
- `orosha-ai/agent-observability-dashboard` — production-grade observability for OpenClaw agents (metrics, traces, alerts)
- `TheAIuniversity/multi-agent-dashboard` — real-time multi-agent monitoring dashboard
- `agentic-layer/observability-dashboard` — OpenTelemetry-based multi-agent system monitoring
- `ColeMurray/claude-code-otel` — OpenTelemetry observability for Claude Code (cost tracking, usage patterns)

## 4. Enterprise Agent Harness

### BulloRosso/etienne — Coding Agent Harness for Business
- **URL:** https://github.com/BulloRosso/etienne
- **Date:** 2025-09-30 (updated 2026-03-05)
- **What:** Integration harness that wraps coding agents for non-technical business users
- **Key features:**
  - **Role-based access control** (admin/user roles)
  - **Skill catalog curation:** Admin curates skills → security check → skill store → business users browse and select
  - **Artifact-based collaboration:** Agent generates drafts, user refines via click or chat
  - **Project isolation:** Knowledge graphs, decision graphs, workflows scoped to mission statement
  - **Deterministic controls:** CRON scheduling, finite state machines for workflows, ontology graphs
  - **World model skill:** Prevents endless codebase analysis, guides agent to relevant locations
- **Philosophy:** "Business knowledge meets technical capability in a single, portable folder"
- **Skill promotion flow:** Project-level skills → admin review → company skill store → available to all users
- **Significance:** Shows the enterprise deployment pattern for skills: curated catalog → admin approval → scoped deployment → promotion

## 5. Cybersecurity Skills Collection

### mukul975/Anthropic-Cybersecurity-Skills — 611+ Security Skills
- **URL:** https://github.com/mukul975/Anthropic-Cybersecurity-Skills
- **Date:** 2026-02-25
- **Scale:** 611+ skills across 24 cybersecurity categories
- **Categories include:** Cloud Security (48), Threat Intelligence (43), Web App Security (41), Threat Hunting (35), Malware Analysis (34), Digital Forensics (34), SOC Operations (33), Network Security (33), IAM (33), OT/ICS Security (28), API Security (28), Container Security (26), Red Teaming (24), Incident Response (24), Pen Testing (23), Zero Trust (17), DevSecOps (16), Cryptography (13)
- **Format:** agentskills.io standard with progressive disclosure
- **All MITRE ATT&CK mapped**
- **Installation:** `npx skills add` / Claude Code plugin / git clone
- **Significance:** Largest domain-specific skills collection found. Demonstrates vertical specialization as a viable strategy

## 6. Multi-Agent Orchestration

### Notable orchestration projects using skills:
- **win4r/team-tasks** — Multi-agent pipeline coordination: Linear, DAG, and parallel patterns (uses OpenClaw skills)
- **bsamud/openfoundry-agentic-framework** — Protocol-first, DAG-executing multi-agent orchestration with Forge, Conveyor, Shield, Watchtower modules
- **kyegomez/swarms** — Enterprise-grade parallel processing pipelines, sequential workflow orchestration, graph-based agent networks, dynamic agent composition
- **ssdeanx/AgentStack** — 60+ enterprise tools, 48+ specialized agents, 21 workflows, 12 agent networks

## Key Patterns

1. **Governance is the enterprise entry point.** Microsoft's governance toolkit (6,100+ tests, OWASP 10/10) and identity kits show governance as prerequisite for enterprise skills adoption
2. **Microsoft is the most aggressive vendor** — 132 SDK skills + governance toolkit + waza evaluator = full stack for enterprise skills
3. **Observability vendors entering skills** — Dash0 shipping OTel skills signals commercial adoption
4. **Business user deployment requires curated catalogs** — Etienne's admin-approval → skill-store → user-selection pattern is the enterprise deployment model
5. **Vertical specialization works** — 611 cybersecurity skills with MITRE ATT&CK mapping demonstrates domain-focused collections have clear value
6. **Context rot is acknowledged** — Microsoft explicitly warns against loading all skills. Focused selection is the norm, not the exception
