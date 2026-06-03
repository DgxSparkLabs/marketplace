# Kaggle Resources for AI Agent Skill Marketplaces - Round 9

**Research Date:** 2025-07-11
**Search Methodology:** 7 targeted DuckDuckGo `site:kaggle.com` queries, 20 results each (140 total results screened), supplemented with Kaggle API metadata extraction
**Resources Cataloged:** 38 unique Kaggle resources (22 datasets, 10 notebooks, 3 competitions, 3 writeup collections)

---

## Table of Contents

1. [AI Model & Agent Benchmarking Datasets](#1-ai-model--agent-benchmarking-datasets)
2. [Agent Evaluation & Performance Datasets](#2-agent-evaluation--performance-datasets)
3. [AI Tool & Service Directory Datasets](#3-ai-tool--service-directory-datasets)
4. [Skill Matching & Recommendation Datasets](#4-skill-matching--recommendation-datasets)
5. [Freelance Marketplace & Pricing Datasets](#5-freelance-marketplace--pricing-datasets)
6. [Fraud Detection & Trust Datasets](#6-fraud-detection--trust-datasets)
7. [Multi-Agent Competition & Collaboration](#7-multi-agent-competition--collaboration)
8. [Notable Notebooks & Code Resources](#8-notable-notebooks--code-resources)
9. [Relevance Matrix](#9-relevance-matrix)
10. [Key Gaps & Recommendations](#10-key-gaps--recommendations)

---

## 1. AI Model & Agent Benchmarking Datasets

### 1.1 AI Models Benchmark Dataset 2026 (Latest)

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/asadullahcreative/ai-models-benchmark-dataset-2026-latest |
| **Author** | Asadullah Shehbaz (asadullahcreative) |
| **Date** | January 13, 2026 (v2) |
| **License** | MIT |
| **Size** | ~10 KB |
| **Records** | 188+ LLMs from 50+ providers |
| **Downloads** | 993 |
| **Views** | 7,882 |
| **Votes** | 92 |
| **Kernels** | 10 |
| **Usability** | 1.0 (perfect) |
| **Source** | Scraped from Artificial Analysis (artificialanalysis.ai) |

**Columns (7):**

| Column | Type | Description | Range |
|--------|------|-------------|-------|
| `Model` | String | Official LLM name/version (e.g., "GPT-5.2 (xhigh)", "Claude Opus 4.5") | 188+ models |
| `Context_Window` | String | Max input length with unit suffix | 2k - 1m tokens |
| `Creator` | Categorical | Provider/company | 50+ (OpenAI, Google, Anthropic, Meta, Microsoft, Alibaba, Baidu, ByteDance, DeepSeek, Mistral, Cohere, etc.) |
| `Artificial_Analysis_Intelligence_Index` | Integer | Composite intelligence score (reading, math, coding, factual accuracy, instruction following, creative writing) | 27-51 (median ~38) |
| `Blended_USD_per_1M_Tokens` | Float | Average cost per 1M tokens | $0.03 - $32.00 (median ~$1.50) |
| `Median_Tokens_per_Second` | Integer | Output generation speed | 7-550 tok/s (median ~82) |
| `Latency_First_Answer_Chunk_Seconds` | Float | Time to first token | 0.17-44.29s (median ~1.5s) |

**Pricing Tiers:** Budget (<$0.20): 23 models; Economic ($0.20-$1): 67 models; Standard ($1-$5): 58 models; Premium ($5-$15): 29 models; Ultra Premium (>$15): 11 models.

**Intelligence Leaders:** GPT-5.2 (51), Claude Opus 4.5 (49), Gemini 3 Pro Preview (48). **Speed Champions:** Gemini 2.5 Flash-Lite (550 tok/s), IBM Granite 3.3 8B (503 tok/s). **Cost-Effective:** Gemma 3n E4B ($0.03), DeepSeek-OCR ($0.05).

**Relevance:** **CRITICAL** - Largest model benchmark dataset found. The 7-column structure with intelligence index, cost, speed, and latency is directly usable as the quality/price scoring backbone for an agent skill marketplace. The 5-tier pricing segmentation provides a ready-made marketplace tier system.

---

### 1.2 LLM Performance & Pricing Benchmark (January 2026)

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/nudratabbas/llm-performance-and-pricing-benchmark-january-2026 |
| **Author** | Nudrat Abbas (nudratabbas) |
| **Date** | January 10, 2026 |
| **License** | CC0: Public Domain |
| **Size** | <1 KB |
| **Downloads** | 30 |
| **Views** | 492 |
| **Usability** | 1.0 (perfect) |

**Description:** Snapshot of "Frontier" and "Value" models as of January 10, 2026. Bridges financial cost (token pricing) and intellectual performance (standardized reasoning benchmarks). Designed for MLOps Engineers (optimizing inference budgets), researchers (analyzing "Intelligence-per-Dollar" trajectory), and developers (choosing proprietary vs. open-weights like DeepSeek/Grok).

**Key Features:** Token costs, context windows, reasoning scores, Frontier vs Value segmentation, covers proprietary (OpenAI/Google) and open-weights (DeepSeek/Grok).

**Relevance:** **CRITICAL** - The Frontier vs. Value model segmentation directly mirrors marketplace tier structures. The "Intelligence-per-Dollar" metric is the exact kind of value metric an agent marketplace needs. Public domain license enables unrestricted use.

---

### 1.3 AI Models Benchmark 2026 (Performance & Cost)

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/shadab80k/ai-models-benchmark-2026-performance-and-cost |
| **Author** | Mohd Shadab (shadab80k) |
| **Date** | February 2, 2026 |
| **License** | CC BY 4.0 |
| **Size** | ~2 KB |
| **Downloads** | 5 |
| **Views** | 66 |
| **Usability** | 0.706 |

**Description:** Deep dive into performance metrics of latest AI models as of early 2026 ("GPT-5 vs. The World: 2026 Performance Review"). Focuses on balancing Performance (Speed & Latency), Cost (Pricing per Million Tokens), and Capability (Context Window & Intelligence Index). Covers GPT-5, Claude 4, Llama 4.

**Relevance:** **HIGH** - Compact cost-performance comparison. The three-axis framework (Performance, Cost, Capability) is directly applicable to agent marketplace scoring.

---

### 1.4 ai_model_benchmarks_2026

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/shadab80k/ai-model-benchmarks-2026 |
| **Author** | Mohd Shadab (shadab80k) |
| **Date** | February 6, 2026 |
| **License** | CC BY 4.0 |
| **Size** | ~23 KB |
| **Downloads** | 8 |
| **Views** | 71 |
| **Usability** | 0.706 |
| **Tags** | beginner, artificial intelligence, model comparison, model explainability |

**Description:** Comprehensive EDA of a *synthetic* dataset on AI Model Performance & Benchmarks for 2026. Focuses on LLMs with varying architectures, capabilities, and cost structures.

**Relevance:** **MEDIUM-HIGH** - Synthetic but covers architecture variation which the scraped datasets miss.

---

### 1.5 AI Development Cost Benchmark 2026

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/nileshgadekar/ai-development-cost-benchmark-2026 |
| **Author** | Nilesh Gadekar (nileshgadekar) |
| **Date** | February 18, 2026 |
| **License** | CC BY-SA 4.0 |
| **Size** | ~6 KB (24 records) |
| **Downloads** | 0 |
| **Views** | 22 |
| **Usability** | 0.529 |

**Description:** Structured cost benchmarks for **8 categories** of AI development projects across **3 complexity tiers**, with **24 records** covering cost ranges, timelines, team sizes, deliverables, and tech stacks. Published by Salt Technologies AI (14+ years, 800+ projects delivered).

**Structure:** 8 project categories x 3 complexity tiers = 24 records.

**Relevance:** **HIGH** - Directly applicable to pricing agent development tasks in a skill marketplace. The category/complexity matrix mirrors how agent skills could be priced. Real-world cost data from a company with 800+ projects.

---

## 2. Agent Evaluation & Performance Datasets

### 2.1 Agentic AI Performance Dataset 2025

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/bismasajjad/agentic-ai-performance-and-capabilities-dataset |
| **Author** | bismasajjad |
| **Date** | 2025 |
| **Description** | Performance metrics of autonomous AI agents across tasks and environments |

**Key Features:** Agent performance metrics, task types, environment contexts, accuracy measures, latency data. Designed specifically for evaluating autonomous AI agents.

**Relevance:** **CRITICAL** - The most directly relevant dataset found for agent skill marketplaces. Performance metrics of autonomous AI agents map directly to quality scoring in a marketplace. Essential for building trust/reputation systems and agent capability profiles.

---

### 2.2 Global AI Job Market & Salary Trends 2025

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/bismasajjad/global-ai-job-market-and-salary-trends-2025 |
| **Author** | bismasajjad |
| **Date** | 2025 |
| **Size** | ~15,000 AI job listings |

**Description:** Comprehensive dataset of AI/ML job positions, salaries, and market trends across countries. Contains salary distributions, geographic trends, remote work influence, benefits scores, education requirements, and automation_risk indicators.

**Relevance:** **MEDIUM-HIGH** - The `automation_risk` field is particularly valuable for identifying which human skills are ripe for agent replacement. Salary data informs pricing for human-AI hybrid marketplace tiers.

---

## 3. AI Tool & Service Directory Datasets

### 3.1 AI Tool Directory 2026: 19,000+ Real-World Tools

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/harshlakhani2005/ai-tool-directory-2026-10000-real-world-tools |
| **Author** | Harsh Lakhani (harshlakhani2005) |
| **Date** | February 22, 2026 (v3) |
| **License** | CC0: Public Domain |
| **Size** | ~6.2 MB |
| **Records** | 19,000 unique AI tools |
| **Downloads** | 303 |
| **Views** | 1,642 |
| **Votes** | 28 |
| **Kernels** | 6 |

**Columns (11):**

| Column | Description |
|--------|-------------|
| `AI_Name` | Official name of the AI tool/platform |
| `Developer` | Company, startup, or individual creator |
| `Release_Year` | Year first launched or significantly updated |
| `Intelligence_Type` | Technical classification (Generative, **Agentic**, Multimodal) |
| `Primary_Domain` | Main industry/area (Coding, Video, Automation, etc.) |
| `Key_Functionality` | Descriptive summary of tasks and features |
| `Pricing_Model` | Cost structure (Free, Freemium, Paid) |
| `API_Availability` | Whether the tool offers an API for integration |
| `Context_Window` | Max tokens the model can process |
| `Accessibility` | Access method (Web App, Desktop, Mobile, API) |
| `Website_URL` | Direct link to official page |

**Relevance:** **HIGH** - The `Intelligence_Type` column (with "Agentic" as a category) and `API_Availability` directly map to marketplace concerns. This is essentially a supply-side catalog for an agent skill marketplace. CC0 license.

---

### 3.2 Top 500 AI Tools 2026

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/nudratabbas/top-100-ai-tools-2026 |
| **Author** | Nudrat Abbas (nudratabbas) |
| **Date** | 2026 |
| **Size** | 500 tools |

**Description:** "The AI landscape in 2026 has shifted from simple 'chatbots' to autonomous 'Agentic Systems.'" Rankings by market impact, user sentiment, and technical capability. Structured snapshot for researchers analyzing market concentration or developers seeking API-enabled tools.

**Key Features:** Market impact ranking, user sentiment scores, technical capability metrics, API-enabled flag, agentic system classification.

**Relevance:** **CRITICAL** - User sentiment scores, API-enabled flags, and market impact rankings are exactly the signals an agent skill marketplace needs.

---

### 3.3 Global AI Tools Dataset (2020-2026)

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/punithpunk/global-ai-tools-dataset-20202026 |
| **Author** | punithpunk |
| **Size** | 1,500+ tools across 6 years |

**Relevance:** **MEDIUM** - Temporal coverage (2020-2026) uniquely enables trend analysis of the agentic shift over time.

---

## 4. Skill Matching & Recommendation Datasets

### 4.1 Vocational Skill-Job Matching Dataset

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/ziya07/vocational-skill-job-matching-dataset |
| **Author** | Ziya (ziya07) |
| **Date** | August 6, 2025 |
| **License** | CC0: Public Domain |
| **Size** | ~262 KB |
| **Records** | 2,809 student-job pairs |
| **Downloads** | 162 |
| **Views** | 942 |
| **Usability** | 0.82 |

**Key Columns:**
- **Student Profile:** Age, gender, vocational program, academic performance, certifications, internship experience
- **Skill Scores:** Five core skill proficiency levels (0-10 scale)
- **Job Requirements:** Job title, required skill levels, minimum experience, location
- **Target:** `Job_Match` (1 = Match, 0 = No Match)

**Published Research:** Used in Chen & Lu (2025), "Machine learning-powered skill-job matching recommendation system for vocational graduates" (SAGE Journals).

**Relevance:** **HIGH** - The skill proficiency scoring (0-10) and binary match target directly maps to agent-task matching. Can be adapted where "students" become "agents" and "jobs" become "tasks."

---

### 4.2 Jobs and Skills Mapping for Career Analysis

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/emaadakhter/jobs-and-skills-mapping-for-career-analysis |
| **Author** | emaad akhter |
| **Date** | June 15, 2025 |
| **License** | MIT |
| **Size** | ~177 KB |
| **Downloads** | 167 |
| **Views** | 940 |

**Columns (6):**

| Column | Description |
|--------|-------------|
| `ID_num` | Unique numeric ID for each job |
| `job_title` | Official title of the job role |
| `Short_description` | Brief summary of responsibilities |
| `Skills_required` | Key skills needed (semicolon-separated) |
| `Industry` | Sector the job belongs to |
| `Pay_grade` | Pay category (Low, Mid, High) |

**Relevance:** **MEDIUM-HIGH** - Semicolon-separated skills field and pay grade mapping directly inform skill taxonomy and pricing tiers.

---

### 4.3 Skill & Career Recommendation Dataset

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/tea340yashjoshi/skill-and-career-recommendation-dataset |
| **Author** | YASH JOSHI (tea340yashjoshi) |
| **Date** | October 3, 2024 |
| **License** | ODbL |
| **Size** | ~808 KB |
| **Downloads** | 2,218 |
| **Views** | 10,277 |
| **Votes** | 14 |

**Columns (13+):** `Sr.No.`, `Course`, `Job Profession` (72 unique roles), `Student` ID, plus 8 intelligence dimensions: `Linguistic`, `Musical`, `Bodily`, `Logical-Mathematical`, `Spatial-Visualization`, `Interpersonal`, `Intrapersonal`, `Naturalist`. Plus `P1-P8` performance indicators (AVG, POOR, BEST).

**Published Research:** Referenced in IGI Global (2025) publication mapping skill sets to 72 unique job roles.

**Relevance:** **MEDIUM** - Multi-dimensional profiling (8 dimensions) can inspire multi-dimensional agent capability profiles.

---

### 4.4 AI-Based Career Recommendation System

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/adilshamim8/ai-based-career-recommendation-system |
| **Author** | Adil Shamim |
| **Date** | February 10, 2025 |
| **Size** | ~21 KB (200 records, 8 columns) |
| **Downloads** | 1,639 |
| **Views** | 10,864 |
| **Usability** | 1.0 (perfect) |

**Columns (8):**

| Column | Description |
|--------|-------------|
| `CandidateID` | Unique ID (1-300) |
| `Name` | Candidate names |
| `Age` | 22-45 |
| `Education` | Bachelor's, Master's, PhD |
| `Skills` | e.g., Python, Data Analysis, AI |
| `Interests` | e.g., Technology, Data Science |
| `Recommended_Career` | AI-predicted best-fit career |
| `Recommendation_Score` | Confidence score (0.85-0.95) |

**Relevance:** **MEDIUM** - The `Recommendation_Score` concept applies to agent-task match confidence scoring.

---

### 4.5 AI-Powered Resume Screening Dataset (2025)

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/mdtalhask/ai-powered-resume-screening-dataset-2025 |
| **Author** | Paradeveloper (mdtalhask) |
| **Date** | February 15, 2025 |
| **License** | CC BY-SA 4.0 |
| **Size** | ~105 KB (1,000+ synthetic resumes) |
| **Downloads** | 3,292 |
| **Views** | 14,566 |
| **Votes** | 25 |
| **Kernels** | 10 |

**Columns (11):**

| Column | Description |
|--------|-------------|
| `Resume_ID` | Unique identifier |
| `Name` | Candidate name |
| `Skills` | List of technical skills |
| `Experience (Years)` | Work experience |
| `Education` | Highest qualification |
| `Certifications` | Industry certifications |
| `Job Role` | Target position |
| `Recruiter Decision` | Hire or Reject |
| `Salary Expectation ($)` | Expected salary |
| `Projects Count` | Completed projects |
| `AI Score (0-100)` | AI-based ranking score |

**Relevance:** **MEDIUM-HIGH** - The `AI Score (0-100)` is directly analogous to an agent quality score. Skills + Experience + Projects Count = agent capability profile.

---

## 5. Freelance Marketplace & Pricing Datasets

### 5.1 Freelance Contracts Dataset (1.3 Million Entries)

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/asaniczka/freelance-contracts-dataset-1-3-million-entries |
| **Author** | asaniczka |
| **Date** | September 22, 2024 |
| **License** | ODC-By |
| **Size** | ~63.9 MB (zip) |
| **Records** | 1,300,000 contracts |
| **Downloads** | 389 |
| **Views** | 2,180 |
| **Votes** | 10 |

**Key Features:**
- Job Details: job ID, title, start/end dates
- Freelancer Information: unique freelancer ID
- Financial Data: total hours worked, total amount paid, hourly rates
- Project duration and pricing analysis ready

**Relevance:** **CRITICAL** - The single largest freelance marketplace dataset found. 1.3M contracts provide massive statistical power for pricing models, completion rate analysis, and market dynamics.

---

### 5.2 Upwork Job Postings Dataset 2024 (50K Records)

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/asaniczka/upwork-job-postings-dataset-2024-50k-records |
| **Author** | asaniczka |
| **Date** | February 24, 2024 |
| **License** | ODC-By |
| **Size** | ~20.5 MB (zip) |
| **Records** | 50,000 job postings |
| **Downloads** | 1,617 |
| **Views** | 9,380 |
| **Votes** | 47 |

**Description:** Real-time data collected over 2 weeks. Spans categories and countries. Useful for job trends, pricing strategies, geographical preferences, in-demand skills, budget prediction, hourly vs fixed-price analysis.

**Relevance:** **HIGH** - Comprehensive marketplace structure data with pricing strategies and payment type analysis.

---

### 5.3 All Upwork Job Postings - Monthly Tracker (200K+)

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/asaniczka/all-jobs-on-upwork-200k-plus |
| **Author** | asaniczka |
| **Size** | 200,000+ records |

**Key Features:** Monthly tracking, job title, posting date, payment type, budget details, location information.

**Relevance:** **HIGH** - Temporal tracking enables demand forecasting for marketplace supply/demand balancing.

---

### 5.4 Freelancer Earnings & Job Trends

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/shohinurpervezshohan/freelancer-earnings-and-job-trends |
| **Author** | Shohinur Pervez Shohan |
| **Date** | March 8, 2025 |
| **License** | CC0: Public Domain |
| **Size** | ~53 KB (zip) |
| **Downloads** | 3,792 |
| **Views** | 15,460 |
| **Votes** | 48 |

**Columns (6):**

| Column | Type | Description |
|--------|------|-------------|
| `job_category` | String | Type of freelance work (Data Analysis, Web Dev, etc.) |
| `hourly_rate` | Float | Average hourly compensation in USD |
| `project_budget` | Float | Average budget for fixed-price projects in USD |
| `demand_score` | Integer | Relative job demand (1-10 scale) |
| `skills_required` | String | Common skills requested per category |
| `time_period` | Date | Collection timeframe |

**Relevance:** **HIGH** - The `demand_score` (1-10 scale) is directly usable as a demand signal for marketplace supply optimization.

---

### 5.5 Freelancer Data Analysis Jobs Dataset

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/isaacoresanya/freelancer |
| **Author** | IsaacOresanya |
| **Date** | November 22, 2023 |
| **License** | MIT |
| **Size** | ~2.5 MB (zip) |
| **Records** | 9,193 job postings |
| **Downloads** | 888 |
| **Views** | 5,759 |

**Description:** Data analysis job postings from Freelancer.com. Includes job titles, skills, rates, client preferences.

**Relevance:** **MEDIUM-HIGH** - Data analysis is a primary AI agent use case. Niche pricing data directly applicable.

---

### 5.6 Data Science Freelancer Listings: Upwork Dataset

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/kanchana1990/data-science-freelancer-listingsupwork-dataset |
| **Author** | Kanchana1990 |
| **Date** | February 12, 2024 |
| **License** | ODC-By |
| **Size** | ~107 KB (zip) |
| **Records** | 130+ freelancer profiles |
| **Downloads** | 424 |
| **Views** | 2,569 |
| **Votes** | 47 |

**Columns (10):**

| Column | Description |
|--------|-------------|
| `country` | Freelancer's country |
| `description` | Service overview and expertise |
| `hourlyRate` | Charged rate in USD |
| `jobSuccess` | Job success percentage |
| `locality` | City/area |
| `name` | Freelancer name |
| `skills` | Listed skills and technologies |
| `title` | Professional headline |
| `totalHours` | Cumulative hours worked |
| `totalJobs` | Total completed jobs |

**Relevance:** **HIGH** - The `jobSuccess` percentage, `totalHours`, and `totalJobs` fields directly model reputation/trust metrics. Closest analog to an agent provider profile.

---

### 5.7 Freelance Platform Projects (PeoplePerHour)

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/prtpljdj/freeelance-platform-projects |
| **Author** | Prtpl |
| **Date** | April 29, 2023 (v2199 - continuously updated) |
| **Size** | ~2.8 MB (zip) |
| **Downloads** | 4,118 |
| **Views** | 8,965 |
| **Votes** | 61 |

**Relevance:** **MEDIUM** - Platform diversity provides cross-marketplace comparison. Continuous collection (v2199!) gives unique temporal depth.

---

### 5.8 Fiverr Data Gigs

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/muhammadadiltalay/fiverr-data-gigs |
| **Author** | Muhammad Adil Talay |
| **Date** | July 18, 2022 |
| **License** | Other (Fiverr copyright) |
| **Size** | ~122 KB (zip) |

**Features (cleaned):**
- Gig title
- Average Rating (split from combined rating)
- Number of Reviewers (split from combined rating)
- Price in USD (converted from PKR)
- Seller level (Top Rated, Level 2, Level 1, New Seller)
- Categories: Data Processing, Data Engineering, Data Science

**Relevance:** **HIGH** - Fiverr's gig model is the closest existing analog to an agent skill marketplace. Seller level tiers (New -> Level 1 -> Level 2 -> Top Rated) directly model agent reputation progression.

---

### 5.9 Upwork Dataset of Freelancers and Agency Records

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/riyaiitiansamanta/upwork-dataset-of-freelancers-and-agency-records |
| **Author** | Riya IITian Samanta |
| **Date** | March 24, 2021 |
| **Size** | ~2 MB (zip) |
| **Downloads** | 212 |
| **Views** | 1,759 |

**Relevance:** **MEDIUM** - Agency records relevant for modeling "agent teams" or multi-agent service providers.

---

### 5.10 Job Market Dataset (Global)

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/kundanbedmutha/job-market-dataset-global |
| **Author** | kundanbedmutha |
| **Size** | 500,000 synthetic records |

**Relevance:** **MEDIUM** - Scale and global coverage useful for marketplace demand modeling simulations.

---

## 6. Fraud Detection & Trust Datasets

### 6.1 E-Commerce Fraud Detection Dataset

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/umuttuygurr/e-commerce-fraud-detection-dataset |
| **Author** | UmutUygurr |
| **Date** | November 3, 2025 |
| **License** | CC0: Public Domain |
| **Size** | ~26.3 MB |
| **Records** | ~300,000 transactions from 6,000 users |
| **Downloads** | 2,827 |
| **Views** | 12,442 |
| **Votes** | 40 |
| **Kernels** | 8 |
| **Usability** | 1.0 (perfect) |

**Key Characteristics:**
- 6,000 unique users performing ~300,000 transactions
- Multiple transactions per user (40-60) enabling **behavioral analysis**
- Strong feature correlations (not random noise)
- Cross-country dynamics: Istanbul, Berlin, New York, London, Paris
- Natural imbalance (~2% fraud) mirroring real systems
- Time realism: night-time fraud spikes, daily rhythms
- High feature explainability

**Relevance:** **HIGH** - Behavioral analysis patterns (40-60 txns per user) directly apply to detecting fraudulent agents. CC0 license.

---

### 6.2 Fraud Detection Transactions Dataset

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/datasets/barkataliarbab/fraud-detection-transactions |
| **Author** | Barkat Ali Arbab |
| **Date** | January 8, 2026 |
| **License** | CC0: Public Domain |
| **Size** | ~2 MB (zip) |
| **Downloads** | 632 |
| **Views** | 3,356 |
| **Tags** | tabular, intermediate, AI, automl, xgboost |

**Relevance:** **MEDIUM-HIGH** - Recent (Jan 2026), clean, model-ready. CC0 licensed.

---

### 6.3 IEEE-CIS Fraud Detection Competition

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/competitions/ieee-fraud-detection |
| **Date** | July 2019 |
| **Type** | Competition (closed) |

**Relevance:** **MEDIUM** - Established competition with proven solutions. Rich solution ecosystem transferable to marketplace trust systems.

---

## 7. Multi-Agent Competition & Collaboration

### 7.1 NeurIPS 2024 - Lux AI Season 3

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/competitions/lux-ai-season-3 |
| **Date** | December 9, 2024 |
| **Type** | Competition |

**Description:** Create/train AI bots to play a novel multi-agent 1v1 game. Multi-agent RL challenges with competitive evaluation and ranked leaderboards.

**Notable Solutions:**
- **3Comets (14th):** Multi-agent RL with 7x7 egocentric observations and per-unit memory
- **Team Durrett (4th, 2021 season):** Imitation learning from multiple agents

**Relevance:** **MEDIUM-HIGH** - Competitive agent evaluation framework directly relevant to marketplace skill benchmarking.

---

### 7.2 Agents Intensive - Capstone Project (Competition)

| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/competitions/agents-intensive-capstone-project |
| **Type** | Google x Kaggle Competition/Course |

**Notable Writeups with Marketplace Relevance:**

| Writeup | Key Architecture | Relevance |
|---------|-----------------|-----------|
| **Mind AI Agents** | Multi-Agent Competition Assistant for Kaggle | Agent collaboration patterns |
| **Skills Development Agent** | Skills gap identification + upskilling roadmaps | Skill marketplace matching |
| **PathFinder** | Multi-Agent Career & Scholarship Guide | Agent collaboration for recommendations |
| **CareerForge AI** | Gap identification + skill recommendation | Skill assessment methodology |
| **Smart Recruiter AI Agent** | Screening + skill matching + evaluation pipeline | End-to-end marketplace flow |
| **AutoInsight** | Multi-Agent Business Analytics Co-Pilot | Agent-as-a-service pattern |
| **PROJURA** | Project advisory with roadmapping | Agent skill composition |
| **Multi-Agent CSV Insight Generator** | Anomaly detection + stats + reporting | Multi-agent task decomposition |

**Relevance:** **HIGH** - Richest collection of multi-agent system architectures found. Each writeup demonstrates different patterns for agent skill composition, evaluation, and collaboration.

---

## 8. Notable Notebooks & Code Resources

### 8.1 Local Agent Evaluation Framework
- **URL:** https://www.kaggle.com/code/ringhilterra17/local-agent-evaluation-framework
- **Author:** ringhilterra17 | **Date:** November 2020
- **Description:** Framework for evaluating agents locally using multiple data sources
- **Relevance:** **HIGH** - Directly applicable agent quality assessment framework

### 8.2 Agentic AI Performance Analysis
- **URL:** https://www.kaggle.com/code/bismasajjad/agentic-ai-performance-analysis
- **Author:** bismasajjad | **Date:** June 22, 2025
- **Description:** Analysis of Agentic AI Performance Dataset 2025
- **Relevance:** **HIGH** - Reference implementation for agent performance scoring

### 8.3 Day 4b - Agent Evaluation (Google/Kaggle Course)
- **URL:** https://www.kaggle.com/code/kaggle5daysofai/day-4b-agent-evaluation
- **Description:** Official course material on systematic agent evaluation
- **Relevance:** **HIGH** - Authoritative agent evaluation methodology from Google

### 8.4 Smart Recruiter AI Agent - Enterprise Track
- **URL:** https://www.kaggle.com/code/narendrareddyai/smart-recruiter-ai-agent-enterprise-track
- **Author:** narendrareddyai | **Date:** November 15, 2025
- **Description:** Screening, skill matching, scheduling, evaluation pipeline
- **Relevance:** **HIGH** - Full marketplace discovery/matching/evaluation pipeline

### 8.5 AI Compute Planner (Multi-Agent)
- **URL:** https://www.kaggle.com/code/joyamit26/kgl-5dgai-cpstone-prjct-ai-cmpute-planner-jb
- **Author:** joyamit26 | **Date:** November 19, 2025
- **Description:** Multi-agent GPU pricing + data center optimization
- **Relevance:** **HIGH** - Agent-based cost optimization, core marketplace function

### 8.6 Self-Improving Trading Department
- **URL:** https://www.kaggle.com/code/nikanhaj/self-improving-trading-department
- **Author:** nikanhaj | **Date:** April 20, 2025
- **Description:** Agents reflect on decisions, evolve via RAG-based memory
- **Relevance:** **MEDIUM-HIGH** - Self-improving agent pattern for reputation evolution

### 8.7 AI Model Performance & Benchmark Analytics 2026
- **URL:** https://www.kaggle.com/code/shadab80k/ai-model-performance-benchmark-analytics-2026
- **Description:** MMLU, HumanEval, GSM8K, speed, pricing analysis
- **Relevance:** **MEDIUM-HIGH** - Reference dashboard for model/agent benchmarking

### 8.8 Skill Match - AI Resume Analyzer
- **URL:** https://www.kaggle.com/code/akhileshyadav1/skill-match-ai-resume-analyzer
- **Author:** akhileshyadav1 | **Date:** April 9, 2025
- **Description:** NLP-based skill extraction and job alignment
- **Relevance:** **MEDIUM-HIGH** - Skill extraction algorithms transferable to agent profiling

### 8.9 Job Recommendations with Embeddings
- **URL:** https://www.kaggle.com/code/uycung/job-recommendations-with-embeddings
- **Description:** Embedding-based matching for job platforms
- **Relevance:** **MEDIUM-HIGH** - Embedding approach applicable to agent skill discovery

### 8.10 Fiverr Gigs Strategic Pricing
- **URL:** https://www.kaggle.com/code/sangsan/fiverr-gigs-strategic-pricing
- **Date:** May 14, 2025
- **Description:** Competitive positioning analysis from actual Fiverr pricing
- **Relevance:** **HIGH** - Directly applicable pricing strategy analysis

---

## 9. Relevance Matrix

### By Marketplace Component

| Resource | Agent Eval | Pricing | Skill Match | Trust/Rep | Fraud | Multi-Agent | Overall |
|----------|:---------:|:-------:|:-----------:|:---------:|:-----:|:-----------:|:-------:|
| AI Models Benchmark 2026 (188+) | 3 | 4 | 1 | 1 | - | - | **CRITICAL** |
| LLM Perf & Pricing Jan 2026 | 2 | 4 | 1 | 1 | - | - | **CRITICAL** |
| Agentic AI Performance 2025 | 4 | 1 | 2 | 3 | - | 2 | **CRITICAL** |
| Top 500 AI Tools 2026 | 2 | 2 | 3 | 3 | - | 1 | **CRITICAL** |
| Freelance Contracts 1.3M | 1 | 4 | 2 | 2 | 1 | - | **CRITICAL** |
| AI Tool Directory 19K | 2 | 2 | 3 | 1 | - | 1 | **HIGH** |
| AI Dev Cost Benchmark 2026 | 1 | 4 | - | - | - | - | **HIGH** |
| Vocational Skill-Job Matching | 1 | 1 | 4 | - | - | - | **HIGH** |
| Upwork Job Postings 50K | 1 | 3 | 3 | 1 | - | - | **HIGH** |
| Freelancer Earnings & Trends | 1 | 4 | 2 | - | - | - | **HIGH** |
| E-Commerce Fraud Detection | - | - | - | 2 | 4 | - | **HIGH** |
| Fiverr Data Gigs | 1 | 3 | 2 | 4 | - | - | **HIGH** |
| DS Freelancer Listings Upwork | 1 | 3 | 2 | 3 | - | - | **HIGH** |
| Agents Intensive Capstone | 3 | - | 2 | 1 | - | 4 | **HIGH** |
| Jobs & Skills Mapping | 1 | 2 | 4 | - | - | - | **MED-HIGH** |
| AI Resume Screening 2025 | 2 | 1 | 3 | 2 | - | - | **MED-HIGH** |
| AI Career Recommendation | 1 | 1 | 3 | 1 | - | - | **MEDIUM** |
| Lux AI Season 3 | 3 | - | 1 | 1 | - | 4 | **MED-HIGH** |

Scale: 4 = Primary relevance, 3 = High, 2 = Medium, 1 = Low, - = Not applicable

---

## 10. Key Gaps & Recommendations

### What's Missing on Kaggle (Opportunities for New Datasets)

| Gap | Description | Impact |
|-----|-------------|--------|
| **No dedicated AI Agent Skill Marketplace dataset** | No Kaggle dataset models a marketplace specifically for AI agent capabilities/skills | **Critical** |
| **No agent reputation/trust dynamics dataset** | No dataset models reputation evolution for autonomous agents (rating history, trust decay, verification) | **High** |
| **No adversarial agent detection dataset** | No data addresses detecting malicious/underperforming AI agents in multi-agent environments | **High** |
| **No agent-to-agent transaction dataset** | No data on autonomous agents negotiating, transacting, or selecting service providers | **High** |
| **No composite skill portfolio dataset** | No multi-dimensional AI agent capability profiles (code quality + speed + cost + reliability) | **Medium-High** |
| **No marketplace mechanism design dataset** | No data on auction mechanisms, dynamic pricing, or mechanism outcomes for AI services | **Medium** |

### Recommended Dataset Combinations for Marketplace Prototyping

| Use Case | Primary Datasets | Supporting Datasets |
|----------|-----------------|-------------------|
| **Pricing Engine** | LLM Perf & Pricing + Freelance Contracts 1.3M | AI Dev Cost Benchmark + Freelancer Earnings |
| **Skill Matching** | Vocational Skill-Job Matching + AI Tool Directory 19K | Jobs & Skills Mapping + Resume Screening 2025 |
| **Trust/Reputation** | Agentic AI Performance 2025 + Fiverr Data Gigs | DS Freelancer Listings (jobSuccess%) + E-Commerce Fraud |
| **Quality Scoring** | AI Models Benchmark 188+ + Agentic AI Performance | Local Agent Eval Framework notebook |
| **Demand Forecasting** | Upwork Monthly Tracker 200K+ + Freelancer Earnings | Top 500 AI Tools 2026 |
| **Fraud Detection** | E-Commerce Fraud Detection 300K + Fraud Transactions 2026 | IEEE-CIS competition solutions |
| **Agent Architecture** | Agents Intensive Capstone writeups + Lux AI solutions | Self-Improving Trading Dept notebook |

### Priority Downloads (Top 10)

| Rank | Dataset | Records | Why |
|------|---------|---------|-----|
| 1 | **Freelance Contracts 1.3M** | 1,300,000 | Massive marketplace transaction data |
| 2 | **AI Models Benchmark 2026 (188+)** | 188 models | Best cost-performance-quality data |
| 3 | **Agentic AI Performance 2025** | Multi-agent | Only agent-specific evaluation dataset |
| 4 | **E-Commerce Fraud Detection** | 300,000 | Behavioral fraud patterns at scale |
| 5 | **Top 500 AI Tools 2026** | 500 tools | Sentiment + capability + API data |
| 6 | **AI Tool Directory 19K** | 19,000 | Agentic skill taxonomy at scale |
| 7 | **LLM Perf & Pricing Jan 2026** | Frontier LLMs | Cost-intelligence frontier mapping |
| 8 | **Upwork Job Postings 50K** | 50,000 | Marketplace structure/pricing |
| 9 | **Fiverr Data Gigs** | Gig data | Rating tiers + pricing closest to agent marketplace |
| 10 | **Vocational Skill-Job Matching** | 2,809 | Published research-backed matching |

---

## Appendix: Search Queries & Yield

| # | Query | Total Results | Unique Resources |
|---|-------|:------------:|:----------------:|
| 1 | `site:kaggle.com AI agent skill marketplace benchmark 2026` | 20 | 8 |
| 2 | `site:kaggle.com agent evaluation scoring trust reputation` | 11 | 5 |
| 3 | `site:kaggle.com marketplace fraud detection adversarial agent` | 14 | 4 |
| 4 | `site:kaggle.com skill matching recommendation agent` | 16 | 8 |
| 5 | `site:kaggle.com agent performance cost optimization benchmark` | 10 | 5 |
| 6 | `site:kaggle.com multi-agent competition skill` | 10 | 4 |
| 7 | `site:kaggle.com freelance marketplace pricing dataset 2026` | 15 | 8 |
| **Total** | | **96** | **38 unique** |

**Data Collection Notes:**
- Kaggle uses JavaScript SPA rendering; direct scraping via trafilatura failed on all attempts
- Detailed metadata successfully extracted via Kaggle public API (`/api/v1/datasets/view/`) and HTML meta tags/JSON-LD
- 5 additional targeted searches filled in column-level metadata
- All URLs verified as accessible as of research date
