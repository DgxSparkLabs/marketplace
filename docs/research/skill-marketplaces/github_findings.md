# GitHub Skill Marketplace Research Findings

> **Research Date:** July 2025  
> **Search Terms Used:** "skill marketplace", "skills marketplace platform", "freelance skill marketplace", "AI skill marketplace", "agent skill marketplace", "talent marketplace", "skill exchange platform"  
> **Sources:** GitHub API search + DuckDuckGo site:github.com queries  
> **Total unique repositories analyzed:** 100+ across all searches

---

## Table of Contents

1. [Key Takeaways](#key-takeaways)
2. [Category A: Major AI Agent Skill Marketplaces (Enterprise/Official)](#category-a-major-ai-agent-skill-marketplaces-enterpriseofficial)
3. [Category B: Claude Code & LLM Skills Marketplaces (Community)](#category-b-claude-code--llm-skills-marketplaces-community)
4. [Category C: AI Agent Skill Marketplace Infrastructure & Tools](#category-c-ai-agent-skill-marketplace-infrastructure--tools)
5. [Category D: Decentralized / Web3 Skill & Talent Marketplaces](#category-d-decentralized--web3-skill--talent-marketplaces)
6. [Category E: Traditional Freelance & Talent Marketplaces](#category-e-traditional-freelance--talent-marketplaces)
7. [Category F: Peer-to-Peer Skill Exchange / Swap Platforms](#category-f-peer-to-peer-skill-exchange--swap-platforms)
8. [Emerging Trends](#emerging-trends)

---

## Key Takeaways

1. **AI Agent Skills are the dominant "skill marketplace" category on GitHub right now.** The Claude Code / OpenClaw / Anthropic "Agent Skills" ecosystem has exploded. Most top-starred repos (7,000+ stars for pm-skills) are about AI agent skills, not human freelancing.
2. **Two distinct worlds exist:** (a) AI agent skill marketplaces (code plugins, MCP servers, SKILL.md files) and (b) traditional human skill/talent marketplaces (freelance platforms, skill exchange apps).
3. **Enterprise players are active:** Anthropic (`anthropics/skills`), Block (`block/agent-skills`), Microsoft (`microsoft/skills`), Binance (`binance/binance-skills-hub`), Supabase (`supabase/agent-skills`), and Callstack (`callstackincubator/agent-skills`) all have official agent skills repos.
4. **Web3/decentralized marketplaces** are a significant sub-trend, with projects on Ethereum, Solana, Bitcoin OP_NET, and ICP.
5. **Skill exchange (barter) platforms** are popular as hackathon/student projects but have low traction (1-8 stars).
6. **TypeScript/Next.js** is the dominant stack across both AI skill marketplaces and traditional platforms.

---

## Category A: Major AI Agent Skill Marketplaces (Enterprise/Official)

These are maintained by major companies or Anthropic's official ecosystem. They represent the "new wave" of skill marketplaces where AI agents discover, install, and use skills.

### 1. phuryn/pm-skills
- **URL:** https://github.com/phuryn/pm-skills
- **Stars/Forks:** 7,312 stars | 707 forks
- **License:** MIT
- **Last Activity:** Updated today (active)
- **Description:** PM Skills Marketplace: 100+ agentic skills, commands, and plugins — from discovery to strategy, execution, launch, and growth. Each skill gives Claude domain knowledge, analytical frameworks, or a guided workflow for a specific PM task.
- **Key Technologies:** Agent Skills spec (SKILL.md), Claude Code
- **Notable Features:** 100+ production skills covering product management lifecycle, categorized by PM workflow stage

### 2. anthropics/skills
- **URL:** https://github.com/anthropics/skills
- **Stars/Forks:** N/A (official Anthropic repo)
- **Last Activity:** Active
- **Description:** Official public repository for Agent Skills. Skills are folders of instructions, scripts, and resources that Claude loads dynamically to improve performance on specialized tasks.
- **Key Technologies:** SKILL.md specification, Claude Code
- **Notable Features:** Defines the official Agent Skills standard that the entire ecosystem follows. The foundational specification.

### 3. binance/binance-skills-hub
- **URL:** https://github.com/binance/binance-skills-hub
- **Stars/Forks:** 462 stars | 87 forks
- **Last Activity:** Updated today (active)
- **Description:** Binance Skills Hub is an open skills marketplace that gives AI agents native access to crypto. Market analysis, derivatives monitoring, and one-click MCP setup through natural language.
- **Key Technologies:** MCP (Model Context Protocol), Agent Skills
- **Notable Features:** Enterprise crypto-focused agent skills, MCP integration, natural language crypto operations

### 4. block/agent-skills
- **URL:** https://github.com/block/agent-skills
- **Stars/Forks:** N/A (high-profile; from Block/Square)
- **Last Activity:** Active
- **Description:** A marketplace and collection of reusable Agent Skills maintained by Block to help AI agents perform real-world tasks more effectively. Skills are reusable sets of instructions and supporting resources that teach an AI agent how to perform a specific workflow.
- **Key Technologies:** Agent Skills spec, SKILL.md
- **Notable Features:** Enterprise-grade skills from Jack Dorsey's Block (Square), designed to be composable and reusable

### 5. microsoft/skills
- **URL:** https://github.com/microsoft/skills
- **Stars/Forks:** N/A (Microsoft official)
- **Last Activity:** Updated 2 days ago (active)
- **Description:** Skills, MCP servers, Custom Agents, AGENTS.md templates, and MCP configurations for AI coding agents working with Azure SDKs and Microsoft AI Foundry.
- **Key Technologies:** MCP, AGENTS.md, Azure SDKs, AI Foundry
- **Notable Features:** Microsoft's official agent skills for Azure ecosystem, includes custom agent templates and MCP server configs

### 6. supabase/agent-skills
- **URL:** https://github.com/supabase/agent-skills
- **Stars/Forks:** N/A (Supabase official)
- **Last Activity:** Active
- **Description:** Agent Skills to help developers using AI agents with Supabase. Skills are folders of instructions, scripts, and resources that agents like Claude Code, Cursor, GitHub Copilot, etc. can discover and use.
- **Key Technologies:** Supabase, PostgreSQL, Agent Skills spec
- **Notable Features:** Multi-agent compatible (Claude Code, Cursor, Copilot), database-focused skills

### 7. callstackincubator/agent-skills
- **URL:** https://github.com/callstackincubator/agent-skills
- **Stars/Forks:** N/A (Callstack official)
- **Last Activity:** Active
- **Description:** A collection of agent-optimized React Native skills for AI coding assistants. Install as Claude Code Plugin via marketplace.
- **Key Technologies:** React Native, Agent Skills spec, Claude Code plugin system
- **Notable Features:** React Native-specific agent skills, installable via `/plugin marketplace add`

### 8. gate/gate-skills
- **URL:** https://github.com/gate/gate-skills
- **Stars/Forks:** 10 stars | 3 forks
- **License:** N/A
- **Last Activity:** Updated today (active)
- **Description:** Gate Skills is an open skills marketplace that empowers AI agents with native access to Gate's cryptocurrency ecosystem. Market analysis, derivatives monitoring, one-click MCP setup — all through natural language.
- **Key Technologies:** MCP, Shell, Agent Skills
- **Notable Features:** Crypto exchange (Gate.io) agent skills, similar concept to Binance Skills Hub

---

## Category B: Claude Code & LLM Skills Marketplaces (Community)

Community-built skill marketplaces specifically for Claude Code and other AI coding agents.

### 9. daymade/claude-code-skills
- **URL:** https://github.com/daymade/claude-code-skills
- **Stars/Forks:** 652 stars | 100 forks
- **Language:** Python
- **License:** MIT
- **Last Activity:** Updated today (active)
- **Description:** Professional Claude Code skills marketplace featuring production-ready skills for enhanced development workflows.
- **Notable Features:** Production-ready, high community adoption

### 10. mhattingpete/claude-skills-marketplace
- **URL:** https://github.com/mhattingpete/claude-skills-marketplace
- **Stars/Forks:** 469 stars | 51 forks
- **Language:** HTML
- **License:** Apache-2.0
- **Last Activity:** Updated today (active)
- **Description:** Claude Code Skills for software engineering workflows — Git automation, testing, and code review. A curated marketplace of Claude Code plugins.
- **Notable Features:** Git automation, testing workflows, code review skills, skill loading demos

### 11. ahmedasmar/devops-claude-skills
- **URL:** https://github.com/ahmedasmar/devops-claude-skills
- **Stars/Forks:** 97 stars | 12 forks
- **Language:** Python
- **Last Activity:** Updated 1 day ago
- **Description:** A Claude Code Skills Marketplace for DevOps workflows.
- **Notable Features:** DevOps-specific: CI/CD, infrastructure, monitoring skills

### 12. adrianpuiu/claude-skills-marketplace
- **URL:** https://github.com/adrianpuiu/claude-skills-marketplace
- **Stars/Forks:** 86 stars | 9 forks
- **Language:** Python
- **Last Activity:** Updated 2 days ago
- **Description:** A comprehensive skill that establishes Claude as a Project Architect to generate detailed planning documents that serve as blueprints for AI-assisted software development.
- **Notable Features:** Architecture-focused, planning document generation, blueprint creation

### 13. obie/skills
- **URL:** https://github.com/obie/skills
- **Stars/Forks:** 78 stars | 1 fork
- **License:** MIT
- **Last Activity:** Updated 1 day ago
- **Description:** Claude Code skills marketplace — Production-ready skills for enhanced development workflows. Fork, create a new skill directory under skills/, write your SKILL.md.
- **Notable Features:** Community contribution model via fork-and-PR, SKILL.md standard

### 14. nextlevelbuilder/skillx
- **URL:** https://github.com/nextlevelbuilder/skillx
- **Stars/Forks:** 34 stars | 6 forks
- **Language:** TypeScript
- **Last Activity:** Updated 1 day ago
- **Description:** SkillX.sh — The Only Skill That Your AI Agent Needs. AI agent skills marketplace with semantic search, leaderboard, ratings, and CLI.
- **Notable Features:** Semantic search across skills, leaderboard/rating system, CLI interface, multi-agent support

### 15. rawveg/skillsforge-marketplace
- **URL:** https://github.com/rawveg/skillsforge-marketplace
- **Stars/Forks:** 26 stars | 4 forks
- **Language:** Python
- **Last Activity:** Updated 12 days ago
- **Description:** A Claude Code Marketplace.
- **Notable Features:** Marketplace platform for browsing and installing Claude Code skills

### 16. terrylica/cc-skills
- **URL:** https://github.com/terrylica/cc-skills
- **Stars/Forks:** 20 stars | 4 forks
- **Language:** TypeScript
- **License:** MIT
- **Last Activity:** Updated today (active)
- **Description:** Claude Code Skills Marketplace: plugins, skills for ADR-driven development, DevOps automation, ClickHouse management, semantic versioning, and productivity workflows.
- **Notable Features:** ADR-driven development, ClickHouse management, semantic versioning, productivity workflows

### 17. tommy-ca/notion-skills
- **URL:** https://github.com/tommy-ca/notion-skills
- **Stars/Forks:** 12 stars
- **License:** MIT
- **Last Activity:** Updated 2 days ago
- **Description:** Claude Skills marketplace for productive Notion workflows: knowledge capture, meeting intelligence, research documentation, and spec-to-implementation planning.
- **Notable Features:** Notion-specific workflows, meeting intelligence, research documentation

### 18. SylphAI-Inc/skills
- **URL:** https://github.com/SylphAI-Inc/skills
- **Stars/Forks:** 11 stars | 1 fork
- **Language:** Shell
- **Last Activity:** Updated 14 days ago
- **Description:** AdaL Skills Marketplace — Community-shareable skills for AdaL CLI.
- **Notable Features:** Skills for AdaL (non-Claude) CLI, alternative agent ecosystem

### 19. aiskillstore/marketplace
- **URL:** https://github.com/aiskillstore/marketplace
- **Stars/Forks:** N/A
- **Last Activity:** Active
- **Description:** AI Skillstore — Agent Skills Marketplace. Security-audited skills for Claude Code and Codex. Discover, install, and manage AI agent skills following the Agent Skills specification.
- **Notable Features:** Security-audited skills, multi-agent support (Claude + Codex), formal specification compliance

### 20. nibzard/skills-marketplace
- **URL:** https://github.com/nibzard/skills-marketplace
- **Stars/Forks:** N/A
- **Last Activity:** January 2026 (active)
- **Description:** A marketplace for discovering, sharing, and managing Agent Skills. The Skills Marketplace provides a centralized platform for distributing and discovering Agent Skills that extend Claude Code's capabilities.
- **Notable Features:** Centralized discovery platform, skill distribution infrastructure

---

## Category C: AI Agent Skill Marketplace Infrastructure & Tools

Curated lists, registries, security tools, and infrastructure for the agent skills ecosystem.

### 21. VoltAgent/awesome-agent-skills
- **URL:** https://github.com/VoltAgent/awesome-agent-skills
- **Stars/Forks:** N/A (high-profile awesome list)
- **Last Activity:** Active
- **Description:** Claude Code Skills and 500+ agent skills from official dev teams and the community, compatible with Codex, Antigravity, Gemini CLI, Cursor and others.
- **Notable Features:** 500+ curated skills, multi-agent compatibility (Codex, Gemini CLI, Cursor, Antigravity)

### 22. heilcheng/awesome-agent-skills
- **URL:** https://github.com/heilcheng/awesome-agent-skills
- **Last Activity:** Active
- **Description:** A curated list of skills, tools, tutorials, and capabilities for AI coding agents (Claude, Codex, Antigravity, Copilot, etc.)
- **Notable Features:** Comprehensive awesome list covering multiple AI coding agent ecosystems

### 23. tech-leads-club/agent-skills
- **URL:** https://github.com/tech-leads-club/agent-skills
- **Last Activity:** Updated 2 days ago (active)
- **Description:** The secure, validated skill registry for professional AI coding agents. In an ecosystem where over 13% of marketplace skills contain security issues.
- **Notable Features:** Security-focused skill validation, addresses the trust problem in agent skill marketplaces (13% of skills contain security issues!)

### 24. zack0whocare/awesome-ai-skill-marketplace
- **URL:** https://github.com/zack0whocare/awesome-ai-skill-marketplace
- **Last Activity:** Updated 13 days ago
- **Description:** A curated list of AI skill marketplaces, tools, and resources for AI agents. Featuring SkillForge (skillmarket.live) and more.
- **Notable Features:** Meta-list of AI skill marketplaces, references to live marketplace sites

### 25. numman-ali/n-skills
- **URL:** https://github.com/numman-ali/n-skills
- **Last Activity:** January 2026
- **Description:** n-skills is a curated plugin marketplace for AI agents. Install via openskills or use your agent's native installer.
- **Notable Features:** Cross-installer support (openskills + native), curated quality approach

### 26. democra-ai/candy-shop
- **URL:** https://github.com/democra-ai/candy-shop
- **Language:** TypeScript
- **License:** MIT
- **Last Activity:** Updated 2 days ago
- **Description:** The Open-Source AI Skill Marketplace — Discover, match, and trade 240+ AI agent skills in a two-sided marketplace. Web + Desktop.
- **Notable Features:** Two-sided marketplace model, 240+ skills, Web + Desktop apps, matching algorithm

### 27. 0xmythril/clawdtm
- **URL:** https://github.com/0xmythril/clawdtm
- **Stars/Forks:** 9 stars | 1 fork
- **Language:** TypeScript
- **License:** MIT
- **Last Activity:** Updated 2 days ago
- **Description:** Reviewable skill marketplace for OpenClaw agents. Browse 1,600+ skills with ratings from humans and AI agents.
- **Notable Features:** 1,600+ skills catalog, dual rating system (human + AI agent reviews), OpenClaw ecosystem

### 28. gengirish/skillstore
- **URL:** https://github.com/gengirish/skillstore
- **Language:** TypeScript
- **Last Activity:** Updated today
- **Description:** BuildwithAiGiri MVP #4 — AI Skill Marketplace MCP Server. Discover, share & install AI skills directly from Claude Code & Cursor. 3-tier SaaS (Free/Pro/Enterprise).
- **Key Technologies:** Next.js 14, TypeScript, Supabase, Stripe, Fly.io
- **Notable Features:** MCP Server-based marketplace, 3-tier SaaS model, integrated billing (Stripe), Supabase backend

### 29. Array-Ventures/coworker
- **URL:** https://github.com/Array-Ventures/coworker
- **Stars/Forks:** 14 stars | 7 forks
- **Language:** TypeScript
- **License:** Apache-2.0
- **Last Activity:** Updated 1 day ago
- **Description:** Open-source AI agent with MCP UI, app builder, A2A protocol, skills marketplace, and multi-provider chat. Built with Mastra. Alternative to OpenClaw.
- **Key Technologies:** TypeScript, Mastra framework, MCP, A2A protocol
- **Notable Features:** Full AI agent platform with built-in skills marketplace, A2A (Agent-to-Agent) protocol, app builder

### 30. Sompote/tiger_cowork
- **URL:** https://github.com/Sompote/tiger_cowork
- **Stars/Forks:** 14 stars | 5 forks
- **Language:** TypeScript
- **Last Activity:** Updated today (active)
- **Description:** A self-hosted AI-powered workspace that combines chat, file management, code execution, scheduled tasks, and a skill marketplace — all in one web interface. Compatible with any OpenAI-compatible API.
- **Key Technologies:** TypeScript, OpenAI-compatible API (OpenRouter, TigerBot, Ollama)
- **Notable Features:** Self-hosted, multi-LLM provider support, skill marketplace integrated into workspace

### 31. hasanator3000/ClawdOS
- **URL:** https://github.com/hasanator3000/ClawdOS
- **Stars/Forks:** 12 stars | 1 fork
- **Language:** TypeScript
- **License:** MIT
- **Last Activity:** Updated today
- **Description:** The web GUI & productivity workspace for OpenClaw (237K+ stars) — tasks, news, dashboards, package tracking, skill marketplace. Self-hosted & private.
- **Notable Features:** OpenClaw ecosystem GUI, integrated skill marketplace with task management

### 32. eugenepyvovarov/mcpbundler-agent-skills-marketplace
- **URL:** https://github.com/eugenepyvovarov/mcpbundler-agent-skills-marketplace
- **Stars/Forks:** 8 stars | 2 forks
- **Language:** Python
- **License:** MIT
- **Last Activity:** Updated 12 days ago
- **Description:** Agent skills marketplace for MCP bundler (can be used with other AI tools with support of agent skills marketplaces).
- **Notable Features:** MCP Bundler integration, cross-tool compatible, credits skill authors

---

## Category D: Decentralized / Web3 Skill & Talent Marketplaces

Projects leveraging blockchain for trustless skill/talent marketplaces.

### 33. squidbay/squidbay
- **URL:** https://github.com/squidbay/squidbay
- **Stars/Forks:** 2 stars
- **Language:** HTML
- **Last Activity:** Updated 5 days ago
- **Description:** AI agent skill marketplace — where agents buy and sell capabilities from each other using Bitcoin Lightning.
- **Key Technologies:** Bitcoin Lightning Network, HTML
- **Notable Features:** Agent-to-agent skill commerce via Bitcoin Lightning payments, novel economic model for AI

### 34. mktrades29/neuromarket-dapp
- **URL:** https://github.com/mktrades29/neuromarket-dapp
- **Language:** TypeScript
- **Last Activity:** Updated 15 days ago
- **Description:** NeuroMarket — Decentralized AI Skill Marketplace on Bitcoin OP_NET. Buy & sell AI skills with $MOTO & $PILL tokens. Built for Vibecode contest.
- **Key Technologies:** TypeScript, Bitcoin OP_NET, custom tokens
- **Notable Features:** Token-based skill economy, decentralized AI skill trading, Bitcoin layer

### 35. BlocklanceHQ/interface
- **URL:** https://github.com/BlocklanceHQ/interface
- **Last Activity:** Active
- **Description:** Blocklance is a decentralized freelance platform on the blockchain, connecting buyers (clients, businesses) with sellers (Freelancers/Talents) through cutting-edge blockchain technology.
- **Key Technologies:** Blockchain, smart contracts
- **Notable Features:** Decentralized escrow, dispute resolution, freelancer reputation on-chain

### 36. shivam6862/DigiFreelance-hub
- **URL:** https://github.com/shivam6862/DigiFreelance-hub
- **Last Activity:** Active
- **Description:** DigiFreelance-hub is an innovative decentralized freelance platform, seamlessly integrating Next.js for the frontend, Solidity for smart contracts.
- **Key Technologies:** Next.js, Solidity, Ethereum
- **Notable Features:** Smart contract-based freelance agreements, decentralized payments

### 37. successaje/Earnify
- **URL:** https://github.com/successaje/Earnify
- **Stars/Forks:** 1 star
- **Language:** JavaScript
- **Last Activity:** Updated 9 months ago
- **Description:** Earnify is a decentralized talent marketplace built on the Internet Computer Protocol (ICP) that connects skilled professionals with opportunities to earn, learn, and grow.
- **Key Technologies:** ICP (Internet Computer Protocol), JavaScript
- **Notable Features:** ICP-based, earn-to-learn model, decentralized identity

### 38. surajsbhoj0101/NeuroGuild-Network
- **URL:** https://github.com/surajsbhoj0101/NeuroGuild-Network
- **Stars/Forks:** 1 star
- **Language:** JavaScript
- **Last Activity:** Updated today (active)
- **Description:** Decentralized talent marketplace and governance network powered by on-chain reputation, job escrow, and indexed protocol data.
- **Key Technologies:** JavaScript, blockchain, on-chain reputation
- **Notable Features:** DAO governance, on-chain reputation system, job escrow, protocol-level data indexing

### 39. holyaustin/Tallent-Musica-Ripple
- **URL:** https://github.com/holyaustin/Tallent-Musica-Ripple
- **Stars/Forks:** 2 stars | 1 fork
- **Language:** Assembly (Solidity)
- **Last Activity:** Updated 1 year ago
- **Description:** Talent Musica is a web3 DApp that allows young music talents to upload their songs or performance as NFTs into the Talent Marketplace.
- **Key Technologies:** Ripple/XRP, NFTs, Solidity
- **Notable Features:** Music talent NFT marketplace, creative industry focus

### 40. Akshat0908/Skill-Exchange-Platform (Decentralized)
- **URL:** https://github.com/Akshat0908/Skill-Exchange-Platform
- **Stars/Forks:** 1 star | 1 fork
- **Language:** JavaScript
- **Last Activity:** Updated 4 months ago
- **Description:** The Skill Exchange platform is a decentralized application (dApp) built using React and Ethereum smart contracts. Users can connect wallets for trustless skill exchange.
- **Key Technologies:** React, Ethereum, Solidity, Web3.js
- **Notable Features:** Wallet-connected skill exchange, smart contract-based agreements

### 41. DEEPBRANDINGDOOH/DEEP-PULSE
- **URL:** https://github.com/DEEPBRANDINGDOOH/DEEP-PULSE
- **Stars/Forks:** 1 star
- **Language:** JavaScript
- **License:** MIT
- **Last Activity:** Updated 4 days ago
- **Description:** Web3 Brand Engagement Platform for Solana Mobile — Notification hubs, on-chain ad marketplace, Swipe-to-Earn, DAO Boost, Talent marketplace, DOOH worldwide. Powered by $SKR.
- **Key Technologies:** Solana, JavaScript, Mobile
- **Notable Features:** Solana-based, mobile-first, includes talent marketplace within broader Web3 platform

---

## Category E: Traditional Freelance & Talent Marketplaces

Human-to-human skill/talent marketplace platforms.

### 42. zer0-A1/Emineon
- **URL:** https://github.com/zer0-A1/Emineon
- **Stars/Forks:** 8 stars
- **Language:** TypeScript
- **Last Activity:** Updated 4 months ago
- **Description:** Emineon is a consulting OS that unifies firm workflows from lead to delivery. Uses AI agents for skill-matching, workflow management, and document generation. Also operates a talent marketplace.
- **Key Technologies:** TypeScript, AI agents
- **Notable Features:** AI-augmented consulting workflow, skill-matching automation, claims 40% less admin time and 60% more client time

### 43. felipevcc/holbie-talent-hub
- **URL:** https://github.com/felipevcc/holbie-talent-hub
- **Stars/Forks:** 6 stars | 1 fork
- **Language:** TypeScript
- **Last Activity:** Updated 1 year ago
- **Description:** Backend project at Coderise for a Web application focused on a Talent Marketplace called Holbie Talent Hub.
- **Key Technologies:** TypeScript (backend)
- **Notable Features:** Talent Hub backend, Coderise project

### 44. samuelemb/Tibeb-skill-marketplace
- **URL:** https://github.com/samuelemb/Tibeb-skill-marketplace
- **Stars/Forks:** 1 fork
- **Language:** TypeScript
- **Last Activity:** Updated 17 days ago
- **Description:** A full-stack skill marketplace platform for clients and freelancers, built using Next.js, Node.js, PostgreSQL, and real-time communication with Socket.IO.
- **Key Technologies:** Next.js, Node.js, PostgreSQL, Socket.IO
- **Notable Features:** Full-stack reference implementation, real-time communication, client-freelancer matching

### 45. zepzincirli/skillbridge
- **URL:** https://github.com/zepzincirli/skillbridge
- **Language:** C#
- **Last Activity:** Updated 9 months ago
- **Description:** Freelance skill marketplace project with .NET Core and React.
- **Key Technologies:** .NET Core, React, C#
- **Notable Features:** Enterprise .NET stack (unusual for this space), React frontend

### 46. shre4ya/Saathi
- **URL:** https://github.com/shre4ya/Saathi
- **Last Activity:** Updated 16 days ago
- **Description:** A global opportunity aggregator and peer-to-peer skill marketplace platform connecting people to internships, competitions, events, and skill-based services.
- **Notable Features:** Opportunity aggregation beyond just freelancing — internships, competitions, events

### 47. GajananDhangude/WorkOS
- **URL:** https://github.com/GajananDhangude/WorkOS
- **Stars/Forks:** 1 star
- **Language:** JavaScript
- **Last Activity:** Updated 1 month ago
- **Description:** WorkOS is an AI-native talent marketplace where jobs are defined as outcomes, not roles, and candidates are matched through real skill proof, micro-tasks, and performance signals instead of resumes.
- **Key Technologies:** JavaScript, AI matching
- **Notable Features:** Outcome-based job definitions (not role-based), skill proof via micro-tasks, performance signals over resumes — very innovative model

### 48. Conyx01/aukier
- **URL:** https://github.com/Conyx01/aukier
- **Stars/Forks:** 1 star
- **Language:** TypeScript
- **Last Activity:** Updated 4 days ago
- **Description:** African talent marketplace platform — connecting skilled workers with opportunities across Africa.
- **Key Technologies:** TypeScript
- **Notable Features:** Africa-focused, regional talent marketplace

### 49. 0-x-joseph/freelanceros
- **URL:** https://github.com/0-x-joseph/freelanceros
- **Last Activity:** Active
- **Description:** FreelancerOS revolutionizes how freelancers manage their business by providing a unified platform for proposal generation, project management, and client communication. Built with Bolt.new.
- **Key Technologies:** Bolt.new
- **Notable Features:** Freelancer business management OS, proposal generation, project management, built in hackathon

### 50. tahsinhasib/TARF
- **URL:** https://github.com/tahsinhasib/TARF-A-Global-Marketplace-for-Freelancing-Services
- **Last Activity:** Active
- **Description:** TARF (a global marketplace for freelancing services), a platform for freelancers and clients to effectively connect.
- **Notable Features:** Global freelancing marketplace

### 51. rhmti01/Frilino-Freelance-App
- **URL:** https://github.com/rhmti01/Frilino-Freelance-App
- **Last Activity:** Active
- **Description:** Frilino is a dynamic marketplace designed to connect skilled freelancers with clients seeking top-notch services.
- **Notable Features:** Developer, designer, and multi-service freelance marketplace

### 52. Emmanuel-Mukumbwa/campus_talent_front_end
- **URL:** https://github.com/Emmanuel-Mukumbwa/campus_talent_front_end
- **Stars/Forks:** 1 star
- **Language:** JavaScript
- **Last Activity:** Updated 2 days ago
- **Description:** A React-based frontend and Node.js/Express backend for a student talent marketplace connecting students, freelancers, and recruiters.
- **Key Technologies:** React, Node.js, Express
- **Notable Features:** Student/campus-focused talent marketplace

### 53. toushka/crewcallpro-mvp
- **URL:** https://github.com/toushka/crewcallpro-mvp
- **Stars/Forks:** 1 star
- **License:** MIT
- **Last Activity:** Updated 6 months ago
- **Description:** No-code MVP for Crew Call Pro — a talent marketplace connecting freelance event professionals with hiring companies in the GCC.
- **Notable Features:** Event industry vertical, GCC region focus, no-code MVP approach

### 54. a-pavithraa/springboot-skills-marketplace
- **URL:** https://github.com/a-pavithraa/springboot-skills-marketplace
- **Stars/Forks:** 16 stars | 2 forks
- **Language:** Java
- **License:** MIT
- **Last Activity:** Updated 3 days ago
- **Description:** Spring Boot skills marketplace.
- **Key Technologies:** Java, Spring Boot
- **Notable Features:** Java/Spring Boot stack (enterprise backend), relatively high stars for a traditional marketplace

### 55. gitswapnadeep/jaro (SkillShareHub)
- **URL:** https://github.com/gitswapnadeep/jaro
- **Language:** TypeScript
- **Last Activity:** Updated 9 months ago
- **Description:** SkillShareHub — A Skill Marketplace Platform.
- **Key Technologies:** TypeScript
- **Notable Features:** Named "SkillShareHub" — skill sharing/marketplace concept

### 56. Abhilash-commits-web/eduhunt
- **URL:** https://github.com/Abhilash-commits-web/eduhunt
- **Language:** TypeScript
- **Last Activity:** Updated 4 months ago
- **Description:** EduHunt — A comprehensive skill marketplace platform.
- **Key Technologies:** TypeScript
- **Notable Features:** Education-focused skill marketplace

---

## Category F: Peer-to-Peer Skill Exchange / Swap Platforms

Barter-style platforms where users exchange skills with each other (no money changes hands).

### 57. Kontukunal/Skill-Swap-App
- **URL:** https://github.com/Kontukunal/Skill-Swap-App
- **Stars/Forks:** 8 stars
- **Language:** JavaScript
- **Last Activity:** Updated 2 months ago
- **Description:** Peer-to-Peer Skill Exchange Platform: SkillSwap connects individuals looking to learn and share skills through mutual exchanges.
- **Notable Features:** P2P skill matching, mutual exchange model

### 58. 3cgbdg/SkillSwapAI
- **URL:** https://github.com/3cgbdg/SkillSwapAI
- **Stars/Forks:** 7 stars
- **Language:** TypeScript
- **License:** GPL-3.0
- **Last Activity:** Updated 30 days ago
- **Description:** SkillSwap AI is a skills exchange platform.
- **Key Technologies:** TypeScript, AI matching
- **Notable Features:** AI-powered skill matching for exchanges

### 59. irahrapunzel/expair
- **URL:** https://github.com/irahrapunzel/expair
- **Last Activity:** Active
- **Description:** A Skill Exchange Platform with AI-Powered Skill Matching and Fair Trade System. EXPAIR is built with Next.js (frontend) and Django (backend), featuring real-time messaging, skill-based trading, and user verification systems.
- **Key Technologies:** Next.js, Django, AI matching
- **Notable Features:** AI-powered matching, fair trade system, real-time messaging, user verification

### 60. juanscr24/skill_swap
- **URL:** https://github.com/juanscr24/skill_swap
- **Last Activity:** Active
- **Description:** A professional skill-exchange platform that connects people to teach and learn new skills through smart matching, real-time chat, and a reputation system.
- **Key Technologies:** Open source
- **Notable Features:** Smart matching algorithm, real-time chat, reputation system

### 61. AdItYa-1900/Maven
- **URL:** https://github.com/AdItYa-1900/Maven
- **Last Activity:** Active
- **Description:** Maven — A modern peer-to-peer skill exchange platform powered by AI matching, real-time collaboration, and WebRTC.
- **Key Technologies:** Node.js, React, WebRTC, AI
- **Notable Features:** WebRTC for real-time video collaboration, AI matching, P2P architecture

### 62. kirangautham-82899/SkillSwap
- **URL:** https://github.com/kirangautham-82899/SkillSwap
- **Stars/Forks:** 3 stars
- **Language:** JavaScript
- **Last Activity:** Updated 7 months ago
- **Description:** Full-stack skill-exchange platform where users match based on complementary skills and connect through real-time chat — built with React, Node.js, and MySQL.
- **Key Technologies:** React, Node.js, MySQL (MERN variant)
- **Notable Features:** Complementary skill matching, real-time chat

### 63. abhi-yo/skillpact
- **URL:** https://github.com/abhi-yo/skillpact
- **Stars/Forks:** 2 stars
- **Language:** TypeScript
- **License:** MIT
- **Last Activity:** Updated 3 months ago
- **Description:** Skillpact is a unique credit-based skill exchange platform designed to connect neighbors and foster community collaboration.
- **Key Technologies:** TypeScript
- **Notable Features:** Credit-based exchange (not pure barter), hyperlocal/neighbor focus

### 64. Vinit-Sahare-Dev/SKILLFUSION
- **URL:** https://github.com/Vinit-Sahare-Dev/SKILLFUSION
- **Stars/Forks:** 2 stars
- **Language:** Java
- **Last Activity:** Updated 1 month ago
- **Description:** Skill Fusion is a community-driven skill exchange platform that enables professionals, learners, and educators to share expertise through a barter-based system. Key features include user profiles with skill validation/verification, real-time communication, and project tracking tools.
- **Key Technologies:** Java
- **Notable Features:** Skill validation/verification, project tracking, barter-based

### 65. rakhaafd/barterkita
- **URL:** https://github.com/rakhaafd/barterkita
- **Stars/Forks:** 2 stars
- **Language:** JavaScript
- **Last Activity:** Updated 4 months ago
- **Description:** KidiHackathon — A modern skill exchange platform connecting individuals and businesses to trade services without money.
- **Notable Features:** B2B + B2C skill bartering, money-free model

### 66. OmPrakash-X/Konnekt
- **URL:** https://github.com/OmPrakash-X/Konnekt
- **Last Activity:** Active
- **Description:** Konnekt — Skill Exchange Platform. A full-stack web application that connects people to exchange skills, book sessions, and build a community of learners and experts. Built for hackathon submission.
- **Notable Features:** Session booking, community building features

### 67. harshmemane/skill-exchange-platform
- **URL:** https://github.com/harshmemane/skill-exchange-platform
- **Stars/Forks:** 1 star
- **Language:** HTML
- **Last Activity:** Updated 4 months ago
- **Description:** AI-powered peer-to-peer skill exchange platform — M.Tech Research Project.
- **Notable Features:** Academic research project, AI-powered matching

---

## Emerging Trends

### 1. AI Agent Skills as the "New App Store"
The most active and highest-starred repositories are all about AI agent skill marketplaces (Claude Code, Codex, Cursor). This is the 2025-2026 equivalent of the App Store model — skills are the new apps, and agents are the new phones.

### 2. Security Concerns in Agent Skill Marketplaces
`tech-leads-club/agent-skills` highlights that **over 13% of marketplace skills contain security issues**. This creates an opportunity for security-audited, trusted skill registries.

### 3. Enterprise Adoption
Major companies (Anthropic, Microsoft, Block, Binance, Supabase, Gate.io, Callstack) are all publishing official agent skills repos. This signals enterprise-level investment in the agent skills ecosystem.

### 4. Two-Sided Agent Marketplaces
`democra-ai/candy-shop` (240+ skills, web + desktop) and `0xmythril/clawdtm` (1,600+ skills with ratings) are building full two-sided marketplaces with discovery, matching, ratings, and trade.

### 5. Crypto/Web3 Agent Economies
`squidbay/squidbay` (Bitcoin Lightning for agent-to-agent payments) and `mktrades29/neuromarket-dapp` (Bitcoin OP_NET tokens) represent a new frontier where AI agents have their own economic systems.

### 6. Outcome-Based Talent Matching
`GajananDhangude/WorkOS` represents an innovative model: jobs defined as outcomes (not roles), candidates matched by skill proof and micro-tasks rather than resumes.

### 7. Regional/Vertical Talent Marketplaces
Several projects focus on specific regions (Africa: `Conyx01/aukier`, GCC: `toushka/crewcallpro-mvp`) or verticals (music: `holyaustin/Tallent-Musica-Ripple`, events: `toushka/crewcallpro-mvp`).

### 8. Skill Exchange (Barter) Model Persists
Despite being mostly student/hackathon projects, the barter-style skill exchange model keeps reappearing. Key innovations: AI matching (`SkillSwapAI`, `expair`), credit systems (`skillpact`), and WebRTC collaboration (`Maven`).

---

## Technology Stack Summary

| Technology | Count (approx.) | Usage Context |
|---|---|---|
| **TypeScript** | ~40% | Dominant across all categories |
| **JavaScript** | ~25% | Traditional marketplaces, MERN stack |
| **Python** | ~15% | Claude Code skills, AI tools |
| **Next.js** | ~20% | Modern web frontends |
| **React** | ~25% | Frontend across categories |
| **Node.js** | ~20% | Backend APIs |
| **Solidity/Web3** | ~10% | Decentralized platforms |
| **Java/Spring Boot** | ~5% | Enterprise backends |
| **C#/.NET** | ~2% | Enterprise (rare) |

---

*Document generated from automated GitHub API + DuckDuckGo searches across 7 search terms and 100+ repository results.*
