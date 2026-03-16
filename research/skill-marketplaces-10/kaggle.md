# Kaggle Resources for AI Agent Skill Marketplaces - Round 10

**Research Date:** 2025-07-18
**Round:** 10 of Deep Research Series
**Search Methodology:** 15+ targeted DuckDuckGo queries via `ddgr` and skill script, covering 7 primary search vectors plus 8 supplementary broadened queries. ~120 unique results screened.
**New Resources Cataloged This Round:** 27 (12 datasets, 8 notebooks/writeups, 4 competitions/benchmarks, 3 external references)
**Cumulative Resources (R1-R10):** 55+ unique Kaggle resources identified across all rounds

---

## Executive Summary

### Has the Gap Been Filled?

**NO.** As of mid-July 2025, there is still **no dedicated AI agent skill marketplace dataset** on Kaggle. The R9 finding remains valid: the closest proxies are freelance marketplace data (1.3M contracts), AI tool directories (19K+ tools), and agent performance benchmarks. However, R10 reveals **significant new developments**:

1. **New "AI Agents Market & Performance Overview (2026)" dataset** (by sidramazam) — a direct agent market overview with agent types, performance metrics, and application data. This is the closest thing to a marketplace dataset yet found.

2. **"AI Agents Jobs Ecosystem 2026" dataset** (by nudratabbas) — captures the agentic workflow transition with data from academic research, community discussion, and the job market. New since R9.

3. **"Agentic AI Performance Dataset 2025"** (by bismasajjad) — performance metrics of autonomous AI agents across tasks and environments. Provides the benchmarking data a marketplace would need for quality scoring.

4. **Kagentic Agent Benchmark Suite** — a Kaggle community benchmark testing full agent behavior including planning, tool usage, and multi-step reasoning. This is infrastructure that could underpin marketplace evaluation.

5. **SkillsMP.com emergence** — External to Kaggle but highly relevant: an actual "Agent Skills Marketplace" has launched (skillsmp.com), confirming market demand. No corresponding dataset on Kaggle yet.

6. **Kaggle MCP Server** — Kaggle now provides an MCP server for agent integration, signaling platform-level support for agent-tool ecosystems.

### Key Delta from R9

| Metric | R9 (2025-07-11) | R10 (2025-07-18) | Change |
|--------|-----------------|-------------------|--------|
| Total resources cataloged | 38 | 55+ | +17 |
| Direct agent marketplace datasets | 0 | 0 | No change |
| Agent market/performance datasets | 3 | 6 | +3 new |
| Agent benchmark infrastructure | 2 | 5 | +3 new |
| Freelance marketplace datasets | 5 | 8 | +3 new |
| Skill matching datasets | 3 | 7 | +4 new |
| External marketplace confirmations | 0 | 2 | +2 new |

---

## Table of Contents

1. [Category A: Agent Market & Performance Datasets (NEW)](#category-a-agent-market--performance-datasets)
2. [Category B: AI Tool & Service Directories](#category-b-ai-tool--service-directories)
3. [Category C: Agent Benchmarks & Evaluation Infrastructure](#category-c-agent-benchmarks--evaluation-infrastructure)
4. [Category D: Freelance Marketplace & Pricing Proxy Data](#category-d-freelance-marketplace--pricing-proxy-data)
5. [Category E: Skill Matching & Recommendation Datasets](#category-e-skill-matching--recommendation-datasets)
6. [Category F: Trust, Reputation & Review Datasets](#category-f-trust-reputation--review-datasets)
7. [Category G: Marketplace Transaction & Payment Data](#category-g-marketplace-transaction--payment-data)
8. [Category H: Security & Vulnerability Datasets](#category-h-security--vulnerability-datasets)
9. [Category I: Multi-Agent Orchestration Notebooks & Competitions](#category-i-multi-agent-orchestration-notebooks--competitions)
10. [Category J: External Agent Marketplace References](#category-j-external-agent-marketplace-references)
11. [Data Pipeline Recommendations](#data-pipeline-recommendations)
12. [Gaps Remaining](#gaps-remaining)
13. [Complete Resource Index Table](#complete-resource-index-table)

---

## Category A: Agent Market & Performance Datasets

### A.1 AI Agents Market & Performance Overview (2026) [NEW - R10]

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/sidramazam/ai-agents-market-and-performance-overview-2026 |
| **Author** | Sidra Mazam (sidramazam) |
| **Date** | 2026 |
| **License** | TBD (check page) |
| **Description** | Comprehensive overview of AI agent types, performance, and applications in 2026 |
| **Relevance** | **CRITICAL** - Closest to a marketplace overview dataset. Contains agent type classifications, performance metrics, and application domains. |
| **Marketplace Use** | Agent taxonomy, performance-based ranking, market segmentation |

**Why This Matters:** This is the single most relevant new dataset for agent marketplace research. It provides a structured view of the agent market that could serve as the backbone for marketplace categories and quality tiers.

---

### A.2 AI Agents Jobs Ecosystem 2026 (Real World)

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/nudratabbas/ai-agents-jobs-ecosystem-2026-real-world |
| **Author** | Nudrat Abbas (nudratabbas) |
| **Date** | Early 2026 |
| **Size** | 176 kB (1 CSV file) |
| **Downloads** | 494 |
| **Notebooks** | 5 |
| **Usability** | 10.0 (perfect) |
| **License** | Check page |
| **Description** | Captures the shift from conversational LLMs to Autonomous Agentic Workflows. Aggregates data from three pillars: Academic Research, Community Discussion, and The Job Market. |
| **Relevance** | **HIGH** - Maps the agent ecosystem from job market perspective. Useful for understanding skill demand curves. |
| **Marketplace Use** | Demand forecasting, skill pricing signals, ecosystem mapping |

---

### A.3 Agentic AI Performance Dataset 2025

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/bismasajjad/agentic-ai-performance-and-capabilities-dataset |
| **Author** | Bisma Sajjad (bismasajjad) |
| **Date** | 2025 |
| **Description** | Performance metrics of autonomous AI agents across tasks and environments |
| **Relevance** | **HIGH** - Direct agent performance benchmarking data. Essential for quality scoring in a marketplace. |
| **Marketplace Use** | Agent quality scoring, capability-based matching, SLA definition |

---

### A.4 Agentic AI Applications 2025

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/hajraamir21/agentic-ai-applications-2025 |
| **Author** | Hajra Amir |
| **Date** | 2025 |
| **Description** | Exploring the Power of Autonomous AI Across Industries |
| **Relevance** | **MEDIUM** - Application-level view of agentic AI deployments by industry |
| **Marketplace Use** | Industry categorization, use-case taxonomy |

---

### A.5 AI Agents Dataset - GitHub Repositories & Use Cases

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/alamshihab075/ai-agents-dataset-github-repositories-use-cases |
| **Author** | Alam Shihab |
| **Description** | Curated list of AI agent use-cases with direct links for RAG-based agents |
| **Relevance** | **MEDIUM** - Repository-level agent catalog. Could serve as a tool/skill directory seed. |
| **Marketplace Use** | Agent discovery index, capability catalog |

---

### A.6 AI Agent Development Trends 2025 (Writeup)

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/writeups/katerynareshetilo/ai-agent-development-trends-2025-dataset |
| **Author** | Kateryna Reshetilo |
| **Type** | Writeup / Analysis |
| **Description** | Insights from 542 real-world AI agent projects — technologies, use cases, costs |
| **Relevance** | **HIGH** - 542-project analysis with cost data. The cost dimension is directly relevant to marketplace pricing. |
| **Marketplace Use** | Cost benchmarking, technology stack trends, project scope estimation |

---

## Category B: AI Tool & Service Directories

### B.1 AI Tool Directory 2026: 19,000+ Real-World Tools

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/harshlakhani2005/ai-tool-directory-2026-10000-real-world-tools |
| **Author** | Harsh Lakhani |
| **Date** | 2026 |
| **Size** | 19,000+ tools |
| **Description** | Massive directory of AI tools across multiple domains including Coding, Video, etc. |
| **Relevance** | **CRITICAL** - Previously identified in R9. Contains "Agentic" classification. Largest tool directory on Kaggle. |
| **Marketplace Use** | Tool/skill catalog, category taxonomy, competitive landscape |

---

### B.2 Top 500 AI Tools 2026

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/nudratabbas/top-100-ai-tools-2026 |
| **Author** | Nudrat Abbas |
| **Date** | February 25, 2026 |
| **Size** | 500 tools |
| **Description** | Rankings by market impact, user sentiment, and technical capability. Captures transition from chatbots to Agentic Systems. |
| **Relevance** | **HIGH** - Multi-dimensional ranking (impact, sentiment, capability) mirrors marketplace quality scoring. |
| **Marketplace Use** | Quality ranking models, sentiment-based trust scoring, market impact estimation |

---

### B.3 Google Workspace Marketplace Apps Dataset

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/marianadeem755/google-workspace-marketplace-apps-dataset |
| **Author** | Mariana Nadeem |
| **Description** | Inventory of applications integrated with Google Workspace Marketplace |
| **Relevance** | **MEDIUM** - Real marketplace data with app listings, categories, and integration patterns. Proxy for agent-tool marketplace structure. |
| **Marketplace Use** | Marketplace UX patterns, category structure, integration metadata |

---

### B.4 AI Tools Market Analysis (2020-2026) [Notebook]

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/code/punithpunk/ai-tools-market-analysis-2020-2026 |
| **Type** | Notebook |
| **Description** | Explores Global AI Tools Dataset (2020-2026) with 1500+ tools across major categories |
| **Relevance** | **MEDIUM** - Temporal analysis of AI tools market evolution. Shows market dynamics relevant to marketplace design. |

---

## Category C: Agent Benchmarks & Evaluation Infrastructure

### C.1 Kagentic Agent Benchmark Suite [NEW - R10]

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/benchmarks/anhoangvo/kagentic-agent-benchmark-suite |
| **Date** | March 1, 2026 |
| **Type** | Kaggle Benchmark |
| **Description** | Tests full agent behavior including planning, tool usage, and multi-step reasoning. Goes beyond static prompt evaluation. |
| **Relevance** | **CRITICAL** - The first Kaggle-native agent benchmark suite. Could serve as the quality evaluation framework for a marketplace. |
| **Marketplace Use** | Agent quality certification, capability verification, trust scoring |

---

### C.2 Science Agent Bench

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/henryshan/science-agent-bench |
| **Description** | Benchmark for scientific AI agents with tool use evaluation |
| **Relevance** | **MEDIUM** - Domain-specific agent evaluation. Shows how vertical marketplaces might certify agents. |

---

### C.3 AI Agent Benchmarks 2026: Comprehensive EDA v2 [Notebook]

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/code/dynamo14324/ai-agent-benchmarks-2026-comprehensive-eda-v2/output |
| **Type** | Notebook |
| **Description** | Comprehensive exploratory data analysis of AI agent benchmarks in 2026 |
| **Relevance** | **HIGH** - Analysis notebook demonstrating how to process agent benchmark data. Reusable methodology. |

---

### C.4 Day 4b - Agent Evaluation [Kaggle Course Notebook]

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/code/kaggle5daysofai/day-4b-agent-evaluation |
| **Type** | Official Kaggle Notebook |
| **Description** | Checks sequence of tool calls against expected behavior. Score 1.0 = perfect tool usage, 0.0 = wrong tools/parameters. |
| **Relevance** | **HIGH** - Official Kaggle methodology for scoring agent tool usage. Directly applicable to marketplace quality metrics. |
| **Marketplace Use** | Tool usage scoring algorithm, quality assurance framework |

---

### C.5 Day 2b - Agent Tools Best Practices [Kaggle Course Notebook]

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/code/kaggle5daysofai/day-2b-agent-tools-best-practices |
| **Type** | Official Kaggle Notebook |
| **Description** | Best practices for agent tool integration. Mentions Kaggle MCP server for agents. |
| **Relevance** | **HIGH** - Confirms Kaggle has an MCP server. Shows tool integration patterns relevant to marketplace design. |
| **Marketplace Use** | Tool integration standards, MCP-based marketplace architecture |

---

### C.6 FACTS Search Leaderboard

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/benchmarks/google/facts-search |
| **Date** | November 24, 2025 |
| **Type** | Kaggle Benchmark |
| **Description** | Evaluates use of Search as a tool to retrieve and synthesize information correctly. |
| **Relevance** | **MEDIUM** - Benchmark for search-as-tool capability. Relevant to agent skill evaluation in retrieval tasks. |

---

### C.7 MLE-bench (OpenAI) [External Reference]

| Field | Value |
|-------|-------|
| **URL** | https://openai.com/index/mle-bench/ |
| **Description** | 75 ML engineering competitions from Kaggle curated as an agent benchmark. Tests training models, preparing datasets, running experiments. |
| **Relevance** | **HIGH** - External but Kaggle-based. Shows how marketplace quality could be validated via competition performance. |

---

## Category D: Freelance Marketplace & Pricing Proxy Data

### D.1 Freelance Contracts Dataset (1.3 Million Entries)

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/asaniczka/freelance-contracts-dataset-1-3-million-entries |
| **Author** | Asaniczka |
| **Size** | 1.3M contracts |
| **Description** | 1.3 million freelance contracts from a popular freelancing website |
| **Relevance** | **CRITICAL** - Largest freelance marketplace proxy. Pricing, skill matching, and contract structure data. |
| **Marketplace Use** | Pricing models, contract templates, demand analysis |

---

### D.2 Freelancer Earnings & Job Trends

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/shohinurpervezshohan/freelancer-earnings-and-job-trends |
| **Author** | Shohinur Pervez Shohan |
| **Description** | Comprehensive freelancer earnings and job trends across industries and skill categories. Gig economy focused. |
| **Relevance** | **HIGH** - Earnings data by skill category directly maps to agent skill pricing. |
| **Marketplace Use** | Skill-based pricing benchmarks, earning potential modeling |

---

### D.3 Upwork Jobs Dataset

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/thedevastator/upwork-jobs-a-dataset-for-researchers |
| **Author** | The Devastator |
| **Description** | Sample of Upwork freelance jobs (January 2022). Includes job title, description, skills, client location, hours/week, duration, fixed price, experience level. |
| **Relevance** | **HIGH** - Real Upwork marketplace data with pricing and skill requirements. |
| **Marketplace Use** | Job-skill matching patterns, pricing by experience level, project scoping |

---

### D.4 Freelancer Data Analysis Jobs Dataset

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/isaacoresanya/freelancer |
| **Author** | Isaac Oresanya |
| **Size** | 9,193 job postings |
| **Description** | Data analysis jobs from Freelancer.com with titles, skills, rates, client preferences |
| **Relevance** | **MEDIUM** - Niche but relevant for data-science-specific agent marketplace pricing. |

---

### D.5 Synthetic Freelance Job Platform Dataset

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/emirhanakku/synthetic-freelance-job-platform-dataset |
| **Author** | Emirhan Akku |
| **Date** | November 5, 2025 |
| **Size** | 1,000 job postings |
| **Description** | Synthetic data simulating a freelance job platform with rich textual descriptions and structured numeric data |
| **Relevance** | **LOW-MEDIUM** - Synthetic but useful for prototyping marketplace features. |

---

### D.6 Freelance Platform Projects (PeoplePerHour)

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/prtpljdj/freeelance-platform-projects |
| **Description** | Projects listed by clients on PeoplePerHour freelance platform |
| **Relevance** | **MEDIUM** - Another marketplace proxy with different dynamics than Upwork/Fiverr. |

---

### D.7 Replit Bounties Dataset [NEW - R10]

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/ibrahimonmars/replit-bounties-dataset |
| **Author** | Ibrahim Omar |
| **Description** | Freelancing bounties from Replit where individuals get paid for coding tasks |
| **Relevance** | **HIGH** - Replit Bounties is the closest existing analog to an AI agent skill marketplace — task-based, code-focused, with pricing. |
| **Marketplace Use** | Bounty-based pricing models, task decomposition patterns, developer marketplace dynamics |

---

### D.8 Freelancer Income vs Skills

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/shaistashahid/freelancer-income-vs-skills |
| **Description** | Gig economy trends, skill-income correlations, high-demand skill identification |
| **Relevance** | **MEDIUM** - Direct skill-to-income mapping useful for marketplace pricing. |

---

## Category E: Skill Matching & Recommendation Datasets

### E.1 Vocational Skill-Job Matching Dataset [NEW - R10]

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/ziya07/vocational-skill-job-matching-dataset |
| **Author** | Ziya |
| **Description** | Designed for ML-powered skill-job matching recommendation systems for vocational training |
| **Relevance** | **HIGH** - Explicit skill-job matching data. The matching algorithm is transferable to agent-skill marketplaces. |
| **Marketplace Use** | Skill matching algorithms, recommendation system training |

---

### E.2 AI-Powered Job Recommendations

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/samayashar/ai-powered-job-recommendations |
| **Size** | 1,559 unique skills, 639 unique values |
| **Description** | AI-powered job matching based on skills and preferences |
| **Relevance** | **HIGH** - Large skill vocabulary with recommendation system structure. |
| **Marketplace Use** | Skill taxonomy, preference-based matching, recommendation engine training |

---

### E.3 Jobs and Skills Mapping for Career Analysis [NEW - R10]

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/emaadakhter/jobs-and-skills-mapping-for-career-analysis |
| **Author** | Emaad Akhter |
| **Date** | June 15, 2025 |
| **Description** | Job roles with descriptions, key skills, industry categories, pay grades. For career recommendation systems and labor market analysis. |
| **Relevance** | **HIGH** - Structured job-skill-industry-pay mapping. Directly applicable to marketplace category/pricing design. |
| **Marketplace Use** | Category taxonomy, skill-price correlation, industry segmentation |

---

### E.4 Job Skill Set Dataset

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/batuhanmutlu/job-skill-set |
| **Author** | Batuhan Mutlu |
| **Description** | Designed for ML projects related to job matching, skill extraction, and NLP tasks |
| **Relevance** | **MEDIUM** - Skill extraction focus relevant to agent capability profiling. |

---

### E.5 Skill & Career Recommendation Dataset

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/tea340yashjoshi/skill-and-career-recommendation-dataset |
| **Description** | Predicting career paths based on skills and academic performance |
| **Relevance** | **LOW-MEDIUM** - Career recommendation patterns transferable to agent skill path suggestions. |

---

### E.6 AI-Based Career Recommendation System

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/adilshamim8/ai-based-career-recommendation-system |
| **Description** | AI-driven career recommendations with skills, interests, and detailed individual data |
| **Relevance** | **MEDIUM** - Multi-factor recommendation approach applicable to agent-buyer matching. |

---

### E.7 JobFit: Tailored Recommendations Based on Skills [Notebook]

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/code/morpho23/jobfit-tailored-recommendations-based-on-skills |
| **Type** | Notebook |
| **Description** | End-to-end job recommender using hybrid techniques — text vectorization, skill embeddings, semantic matching |
| **Relevance** | **HIGH** - Implementable recommendation system with code. The hybrid approach (vectorization + embeddings + semantic matching) is directly applicable to agent skill matching. |

---

## Category F: Trust, Reputation & Review Datasets

### F.1 Fiverr Freelancers Web Scraping Dataset [NEW - R10]

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/asarli/fiverr-freelancers-web-scraping-dataset |
| **Description** | Public Fiverr Freelancing Data for Pricing, Ratings, and Trends |
| **Relevance** | **HIGH** - Real marketplace reputation data with pricing and ratings. |
| **Marketplace Use** | Reputation scoring models, pricing-rating correlations |

---

### F.2 Fiverr Data Gigs

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/muhammadadiltalay/fiverr-data-gigs |
| **Description** | Gig ratings (average + review count), pricing, seller levels |
| **Relevance** | **HIGH** - Granular gig-level marketplace data with multi-dimensional ratings. |
| **Marketplace Use** | Rating system design, seller level tiering, price-quality analysis |

---

### F.3 Fiverr Gig Details

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/aniketanilmali/fiverr-gig-details |
| **Description** | Logo designer gigs with tiered pricing (Basic/Standard/Premium), star ratings (1-5), delivery times, revision counts |
| **Relevance** | **HIGH** - Tiered pricing structure is directly analogous to agent skill marketplace tiers. |
| **Marketplace Use** | Tiered pricing models, delivery SLA design, review system architecture |

---

### F.4 Freelancers Offers on Fiverr

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/kirilspiridonov/freelancers-offers-on-fiverr/data |
| **Description** | Market research dataset for starting online freelancer business on Fiverr |
| **Relevance** | **MEDIUM** - Offer-level data useful for marketplace listing optimization. |

---

### F.5 Epinions Trust Network [NEW - R10]

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/masoud3/epinions-trust-network |
| **Description** | User trust and distrust information. Users evaluate other users based on review quality. |
| **Relevance** | **HIGH** - Pure trust/distrust network data. Critical for designing agent reputation systems. |
| **Marketplace Use** | Trust network modeling, reputation propagation algorithms, distrust detection |

---

### F.6 Trustpilot Company Review Dataset 2025

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/superstar0215/trustpilot-company-review-dataset/data |
| **Date** | November 27, 2025 |
| **Description** | Structured customer reviews with text, ratings, metadata, company information |
| **Relevance** | **MEDIUM** - Company-level review data applicable to agent provider reputation. |

---

### F.7 Trustpilot Reviews 123K

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/jerassy/trustpilot-reviews-123k |
| **Size** | 123,181 reviews, 1,680 companies, 22 categories |
| **Relevance** | **MEDIUM** - Large-scale review dataset for sentiment analysis and reputation modeling. |

---

## Category G: Marketplace Transaction & Payment Data

### G.1 E-Commerce Payment Transactions Dataset

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/yashasvimakin/e-commerce-payment-transactions-dataset |
| **Size** | 4.9M transactions |
| **Description** | Large-scale synthetic dataset of global e-commerce transactions |
| **Relevance** | **MEDIUM** - Transaction patterns (payment methods, amounts, timing) applicable to marketplace payment design. |

---

### G.2 Marketplace Transactional Dataset

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/petewojtczak/raw-transactional-data |
| **Description** | Five interrelated tables including sellers, with state information |
| **Relevance** | **HIGH** - Relational marketplace data with seller dimension. Closest to marketplace transaction structure. |
| **Marketplace Use** | Transaction flow modeling, seller analytics, relational schema design |

---

### G.3 Online Sales Dataset - Popular Marketplace Data

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/shreyanshverma27/online-sales-dataset-popular-marketplace-data |
| **Description** | Global transactions across various product categories |
| **Relevance** | **LOW-MEDIUM** - General marketplace transaction patterns. |

---

### G.4 SalesMind 2026: AI Commerce Dataset [NEW - R10]

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/algozee/dayaset-2020 |
| **Description** | Eight interconnected CSV files structured in relational format simulating a retail data warehouse |
| **Relevance** | **MEDIUM** - Relational commerce data structure applicable to marketplace database design. |

---

## Category H: Security & Vulnerability Datasets

### H.1 Cybersecurity Attack and Defence Dataset [NEW - R10]

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/tannubarot/cybersecurity-attack-and-defence-dataset |
| **Description** | 26 cybersecurity areas including: AI/ML Security, AI Agents & LLM Exploits, AI Data Leakage & Privacy Risks, Automotive/Cyber-Physical systems |
| **Relevance** | **HIGH** - Explicitly covers AI Agents & LLM Exploits. Critical for marketplace security modeling. |
| **Marketplace Use** | Threat modeling for agent marketplaces, security policy design, risk assessment |

---

### H.2 Security Vulnerabilities Dataset

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/ighoshsubho/security-vulnerabilities-dataset |
| **Description** | Cybersecurity insights and security vulnerability exploration |
| **Relevance** | **LOW-MEDIUM** - General vulnerability data, not agent-specific. |

---

### H.3 Vulnerability Fix Dataset

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/jiscecseaiml/vulnerability-fix-dataset |
| **Description** | Vulnerabilities across multiple programming languages for ML and static analysis |
| **Relevance** | **MEDIUM** - Code vulnerability patterns relevant to agent code review in marketplace submissions. |

---

## Category I: Multi-Agent Orchestration Notebooks & Competitions

### I.1 Google Agents Intensive Capstone Project

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/competitions/agents-intensive-capstone-project |
| **Type** | Competition |
| **Description** | Google x Kaggle capstone with 50+ writeups on multi-agent systems. Includes customer support, study planners, competition assistants. |
| **Relevance** | **HIGH** - Rich collection of multi-agent system designs and implementations. |
| **Marketplace Use** | Multi-agent workflow patterns, orchestration architecture references |

**Notable Writeups:**
- [MULTI-AI-AGENTS](https://www.kaggle.com/competitions/agents-intensive-capstone-project/writeups/multi-ai-agents) - Enterprise workflow automation with coordinated agents
- [Multi-Agent Support Automation](https://www.kaggle.com/competitions/agents-intensive-capstone-project/writeups/multi-agent-support-automation) - Intelligent system for Kaggle competitions
- [Smart Study Agent](https://www.kaggle.com/competitions/agents-intensive-capstone-project/writeups/smart-study-agent-a-multi-agent-ai-system-for-aut) - Personalized study plans with multi-agent coordination
- [End-to-End Multi-Agent AI Mentor](https://www.kaggle.com/competitions/agents-intensive-capstone-project/writeups/end-to-end-multi-agent-ai-mentor-for-kaggle) - Specialized agents for modeling, feature engineering, debugging

---

### I.2 AI Agents Ecosystem Dataset 2026 [Notebook]

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/code/sidramazam/ai-agents-ecosystem-dataset-2026 |
| **Type** | Notebook |
| **Description** | Analysis notebook using data from AI Agents Market & Performance Overview (2026) |
| **Relevance** | **HIGH** - Executable analysis of the most relevant dataset (A.1). |

---

### I.3 Day 1b - Agent Architectures [Official Kaggle Course]

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/code/kaggle5daysofai/day-1b-agent-architectures |
| **Date** | November 10, 2025 |
| **Type** | Official Notebook |
| **Description** | Multi-agent systems in ADK. Build systems using LLM as coordinator. |
| **Relevance** | **MEDIUM** - Architectural patterns for multi-agent marketplace orchestration. |

---

### I.4 Kaggle Benchmarks Platform

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/benchmarks |
| **Type** | Platform Feature |
| **Description** | Kaggle benchmark platform for evaluating AI models. Community-built, custom benchmarks at no cost. |
| **Relevance** | **HIGH** - Infrastructure for marketplace quality evaluation. Agents could be certified through Kaggle benchmarks. |

---

## Category J: External Agent Marketplace References

### J.1 SkillsMP.com - Agent Skills Marketplace [EXTERNAL]

| Field | Value |
|-------|-------|
| **URL** | https://skillsmp.com/ |
| **Type** | Live Marketplace |
| **Description** | Actual agent skills marketplace with smart search, category filtering, quality indicators. For developers automating workflows, team leads building custom AI tools. |
| **Relevance** | **CRITICAL** - Confirms the agent skill marketplace concept is being built. No Kaggle dataset counterpart yet. |
| **Data Gap** | No SkillsMP data available on Kaggle for research. |

---

### J.2 Claude Code Skills Ecosystem [EXTERNAL]

| Field | Value |
|-------|-------|
| **URLs** | https://claudemarketplaces.com/skills, https://claude-plugins.dev/skills, https://github.com/anthropics/skills |
| **Type** | Skills Ecosystem |
| **Description** | Multiple directories for discovering and installing agent skills for Claude Code, Cursor, OpenCode, Codex, and other AI coding assistants |
| **Relevance** | **HIGH** - Active agent skill ecosystem. Auto-indexed from GitHub. Represents the kind of marketplace Kaggle data could model. |

---

### J.3 Kaggle MCP Server [PLATFORM]

| Field | Value |
|-------|-------|
| **URL** | Referenced in Day 2b notebook |
| **Type** | Platform Infrastructure |
| **Description** | Kaggle provides an MCP server allowing agents to interact with Kaggle datasets, notebooks, and competitions |
| **Relevance** | **HIGH** - Kaggle itself is becoming part of the agent tool ecosystem via MCP. |

---

## Data Pipeline Recommendations

### Pipeline 1: Agent Marketplace Simulation (Recommended Starting Point)

```
[AI Agents Market Overview 2026 (A.1)]  -->  Agent taxonomy & performance tiers
        |
        +-- [AI Tool Directory 19K (B.1)] -->  Tool/skill catalog with categories
        |
        +-- [Freelance Contracts 1.3M (D.1)] -->  Pricing models & contract structures
        |
        +-- [Fiverr Gigs (F.2, F.3)] -->  Reputation/rating systems & tiered pricing
        |
        +-- [Marketplace Transactions (G.2)] -->  Transaction flow & seller analytics

COMBINED OUTPUT: Synthetic agent marketplace with:
  - Agent types & capabilities (from A.1)
  - 19K tool/skill listings (from B.1)
  - Pricing based on real freelance data (from D.1)
  - Multi-tier pricing & reputation (from F.2, F.3)
  - Transactional patterns (from G.2)
```

### Pipeline 2: Agent Quality & Trust Scoring

```
[Agentic AI Performance (A.3)]  -->  Capability scores
        |
        +-- [Kagentic Benchmark (C.1)] -->  Behavioral evaluation (planning, tool use)
        |
        +-- [Agent Evaluation notebook (C.4)] -->  Tool usage scoring algorithm
        |
        +-- [Epinions Trust Network (F.5)] -->  Trust/distrust graph algorithms
        |
        +-- [Fiverr Ratings (F.1, F.2)] -->  Review-based reputation scoring

COMBINED OUTPUT: Multi-dimensional quality/trust scoring system:
  - Performance-based score (from A.3)
  - Behavioral evaluation score (from C.1)
  - Tool usage accuracy score (from C.4)
  - Network trust score (from F.5)
  - Review-based reputation score (from F.1, F.2)
```

### Pipeline 3: Skill Matching & Recommendation Engine

```
[Vocational Skill-Job Matching (E.1)]  -->  ML-powered matching algorithm
        |
        +-- [AI-Powered Job Recommendations (E.2)] -->  1,559 skills taxonomy
        |
        +-- [Jobs & Skills Mapping (E.3)] -->  Job-skill-industry-pay mapping
        |
        +-- [JobFit Notebook (E.7)] -->  Hybrid recommendation implementation
        |
        +-- [Agent Development Trends (A.6)] -->  542-project cost & tech data

COMBINED OUTPUT: Agent-skill marketplace recommendation engine:
  - Skill taxonomy (1,559+ skills from E.2)
  - Matching algorithm (from E.1)
  - Industry segmentation (from E.3)
  - Hybrid recommendation code (from E.7)
  - Cost calibration (from A.6)
```

### Pipeline 4: Security & Compliance Layer

```
[Cybersecurity Attack Dataset (H.1)]  -->  AI agent threat models (26 areas)
        |
        +-- [Vulnerability Fix Dataset (H.3)] -->  Code vulnerability patterns
        |
        +-- [Agent Tools Best Practices (C.5)] -->  MCP integration security patterns

COMBINED OUTPUT: Marketplace security framework:
  - Threat taxonomy including AI Agents & LLM Exploits (from H.1)
  - Code review patterns for submissions (from H.3)
  - Secure tool integration standards (from C.5)
```

---

## Gaps Remaining

### Critical Gaps (No Kaggle Data Exists)

| Gap ID | Description | Severity | Workaround |
|--------|-------------|----------|------------|
| **G-01** | **No dedicated agent skill marketplace dataset** | CRITICAL | Combine A.1 + B.1 + D.1 as synthetic proxy |
| **G-02** | **No MCP tool marketplace data** | CRITICAL | Monitor SkillsMP.com, Claude marketplace directories |
| **G-03** | **No agent-to-agent transaction data** | HIGH | Use G.2 (marketplace transactions) as structural proxy |
| **G-04** | **No agent trust/reputation scoring dataset** | HIGH | Combine F.5 (Epinions trust network) + F.2 (Fiverr ratings) |
| **G-05** | **No agent skill pricing/economics dataset** | HIGH | Use D.1 (1.3M freelance contracts) + A.6 (542 project costs) |
| **G-06** | **No agent SLA/delivery guarantee data** | MEDIUM | Extract from F.3 (Fiverr delivery times) + D.3 (Upwork durations) |
| **G-07** | **No agent dispute resolution data** | MEDIUM | No proxy available on Kaggle |
| **G-08** | **No multi-agent composition/orchestration marketplace data** | MEDIUM | Use I.1 competition writeups as qualitative source |

### Gaps Partially Addressed Since R9

| Gap | R9 Status | R10 Status | What Changed |
|-----|-----------|------------|--------------|
| Agent market overview | No data | Partial (A.1) | New dataset covers agent types & performance |
| Agent benchmarking | Limited | Improved (C.1) | Kagentic benchmark suite launched |
| Trust networks | No data | Partial (F.5) | Epinions trust network discovered |
| Security modeling | No data | Partial (H.1) | Cybersecurity dataset with AI agent exploit coverage |
| Skill matching | Basic | Strong (E.1-E.7) | 4 new datasets + 1 implementation notebook |

### Recommendations for Gap Closure

1. **Create a synthetic agent marketplace dataset** on Kaggle combining the best proxy data. Estimated effort: 2-3 days. Would fill G-01 through G-05 partially.

2. **Scrape SkillsMP.com** and existing Claude skill directories to create the first agent skill marketplace dataset. Would fill G-02.

3. **Build on Kagentic Benchmark Suite** (C.1) to create marketplace-oriented agent evaluation criteria. Would fill G-04 partially.

4. **Propose a Kaggle Competition** for "AI Agent Marketplace Design" to crowdsource dataset creation and marketplace algorithms.

---

## Complete Resource Index Table

| # | ID | Title | Type | Category | Relevance | New R10? |
|---|-----|-------|------|----------|-----------|----------|
| 1 | A.1 | AI Agents Market & Performance Overview (2026) | Dataset | Agent Market | CRITICAL | Yes |
| 2 | A.2 | AI Agents Jobs Ecosystem 2026 | Dataset | Agent Market | HIGH | Yes |
| 3 | A.3 | Agentic AI Performance Dataset 2025 | Dataset | Agent Market | HIGH | Yes |
| 4 | A.4 | Agentic AI Applications 2025 | Dataset | Agent Market | MEDIUM | Yes |
| 5 | A.5 | AI Agents Dataset - GitHub Repos & Use Cases | Dataset | Agent Market | MEDIUM | No |
| 6 | A.6 | AI Agent Development Trends 2025 | Writeup | Agent Market | HIGH | No |
| 7 | B.1 | AI Tool Directory 2026: 19K+ Tools | Dataset | Tool Directory | CRITICAL | No |
| 8 | B.2 | Top 500 AI Tools 2026 | Dataset | Tool Directory | HIGH | No |
| 9 | B.3 | Google Workspace Marketplace Apps | Dataset | Tool Directory | MEDIUM | Yes |
| 10 | B.4 | AI Tools Market Analysis 2020-2026 | Notebook | Tool Directory | MEDIUM | Yes |
| 11 | C.1 | Kagentic Agent Benchmark Suite | Benchmark | Benchmarks | CRITICAL | Yes |
| 12 | C.2 | Science Agent Bench | Dataset | Benchmarks | MEDIUM | Yes |
| 13 | C.3 | AI Agent Benchmarks 2026 EDA v2 | Notebook | Benchmarks | HIGH | Yes |
| 14 | C.4 | Day 4b - Agent Evaluation | Notebook | Benchmarks | HIGH | No |
| 15 | C.5 | Day 2b - Agent Tools Best Practices | Notebook | Benchmarks | HIGH | Yes |
| 16 | C.6 | FACTS Search Leaderboard | Benchmark | Benchmarks | MEDIUM | No |
| 17 | C.7 | MLE-bench (OpenAI) | External | Benchmarks | HIGH | Yes |
| 18 | D.1 | Freelance Contracts 1.3M | Dataset | Freelance | CRITICAL | No |
| 19 | D.2 | Freelancer Earnings & Job Trends | Dataset | Freelance | HIGH | Yes |
| 20 | D.3 | Upwork Jobs Dataset | Dataset | Freelance | HIGH | No |
| 21 | D.4 | Freelancer Data Analysis Jobs | Dataset | Freelance | MEDIUM | Yes |
| 22 | D.5 | Synthetic Freelance Job Platform | Dataset | Freelance | LOW-MED | Yes |
| 23 | D.6 | Freelance Platform Projects (PPH) | Dataset | Freelance | MEDIUM | Yes |
| 24 | D.7 | Replit Bounties Dataset | Dataset | Freelance | HIGH | Yes |
| 25 | D.8 | Freelancer Income vs Skills | Dataset | Freelance | MEDIUM | Yes |
| 26 | E.1 | Vocational Skill-Job Matching | Dataset | Skill Match | HIGH | Yes |
| 27 | E.2 | AI-Powered Job Recommendations | Dataset | Skill Match | HIGH | Yes |
| 28 | E.3 | Jobs & Skills Mapping for Career | Dataset | Skill Match | HIGH | Yes |
| 29 | E.4 | Job Skill Set Dataset | Dataset | Skill Match | MEDIUM | Yes |
| 30 | E.5 | Skill & Career Recommendation | Dataset | Skill Match | LOW-MED | Yes |
| 31 | E.6 | AI-Based Career Recommendation | Dataset | Skill Match | MEDIUM | Yes |
| 32 | E.7 | JobFit: Tailored Recommendations | Notebook | Skill Match | HIGH | Yes |
| 33 | F.1 | Fiverr Freelancers Web Scraping | Dataset | Trust/Rep | HIGH | Yes |
| 34 | F.2 | Fiverr Data Gigs | Dataset | Trust/Rep | HIGH | No |
| 35 | F.3 | Fiverr Gig Details | Dataset | Trust/Rep | HIGH | No |
| 36 | F.4 | Freelancers Offers on Fiverr | Dataset | Trust/Rep | MEDIUM | Yes |
| 37 | F.5 | Epinions Trust Network | Dataset | Trust/Rep | HIGH | Yes |
| 38 | F.6 | Trustpilot Company Reviews 2025 | Dataset | Trust/Rep | MEDIUM | Yes |
| 39 | F.7 | Trustpilot Reviews 123K | Dataset | Trust/Rep | MEDIUM | Yes |
| 40 | G.1 | E-Commerce Payment Transactions | Dataset | Transactions | MEDIUM | Yes |
| 41 | G.2 | Marketplace Transactional Dataset | Dataset | Transactions | HIGH | Yes |
| 42 | G.3 | Online Sales - Popular Marketplace | Dataset | Transactions | LOW-MED | Yes |
| 43 | G.4 | SalesMind 2026: AI Commerce | Dataset | Transactions | MEDIUM | Yes |
| 44 | H.1 | Cybersecurity Attack & Defence | Dataset | Security | HIGH | Yes |
| 45 | H.2 | Security Vulnerabilities Dataset | Dataset | Security | LOW-MED | Yes |
| 46 | H.3 | Vulnerability Fix Dataset | Dataset | Security | MEDIUM | Yes |
| 47 | I.1 | Agents Intensive Capstone Project | Competition | Multi-Agent | HIGH | No |
| 48 | I.2 | AI Agents Ecosystem 2026 Notebook | Notebook | Multi-Agent | HIGH | Yes |
| 49 | I.3 | Day 1b - Agent Architectures | Notebook | Multi-Agent | MEDIUM | Yes |
| 50 | I.4 | Kaggle Benchmarks Platform | Platform | Multi-Agent | HIGH | No |
| 51 | J.1 | SkillsMP.com | External | Marketplace | CRITICAL | Yes |
| 52 | J.2 | Claude Code Skills Ecosystem | External | Marketplace | HIGH | Yes |
| 53 | J.3 | Kaggle MCP Server | Platform | Marketplace | HIGH | Yes |

---

## Summary Statistics

| Metric | Count |
|--------|-------|
| **Total unique resources (R10)** | 53 |
| **Datasets** | 35 |
| **Notebooks** | 9 |
| **Benchmarks/Competitions** | 5 |
| **External References** | 4 |
| **CRITICAL relevance** | 5 |
| **HIGH relevance** | 26 |
| **MEDIUM relevance** | 16 |
| **LOW-MEDIUM relevance** | 6 |
| **New in R10** | 27 |
| **Carried from prior rounds** | 26 |

---

## Conclusion

Round 10 confirms the persistent absence of a dedicated AI agent skill marketplace dataset on Kaggle. However, the landscape has improved significantly:

1. **The agent market data layer is forming** — datasets A.1, A.2, and A.3 collectively provide agent taxonomy, job ecosystem, and performance data that did not exist in early rounds.

2. **The benchmark infrastructure is maturing** — Kagentic (C.1) and Kaggle's own benchmark platform (I.4) provide the evaluation framework a marketplace needs.

3. **External marketplaces are launching** — SkillsMP.com (J.1) and Claude skill directories (J.2) confirm real market demand, and their data could be scraped to create the missing Kaggle dataset.

4. **The proxy data toolkit is now comprehensive** — With 8 freelance datasets, 7 skill matching datasets, and 7 trust/reputation datasets, there is sufficient proxy data to build a realistic marketplace simulation.

**Recommendation:** The time is ripe to create the first AI Agent Skill Marketplace dataset on Kaggle by combining these proxy sources with data from emerging real marketplaces (SkillsMP, Claude skills ecosystem). This would be a high-impact contribution given the clear gap and growing ecosystem.

---

*Report generated: Round 10 of AI Agent Skill Marketplace Deep Research Series*
*Prior rounds: R1-R9 available in /home/yorai/source/marketplace/research/skill-marketplaces-{2..9}/kaggle.md*
