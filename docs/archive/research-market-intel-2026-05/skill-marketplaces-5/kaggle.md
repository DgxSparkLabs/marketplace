# Kaggle Findings: Skill Marketplaces

> Searched: March 16, 2026
> Queries: "site:kaggle.com skill marketplace", "site:kaggle.com freelance marketplace skills dataset", "site:kaggle.com talent matching skills", "site:kaggle.com upwork fiverr freelancer dataset", "site:kaggle.com job skills matching marketplace"
> Total relevant results: 30+ datasets, 13+ notebooks

## Category 1: Freelance Marketplace Datasets

| Dataset | Source | Size | Description |
|---------|--------|------|-------------|
| **Upwork Freelancers 60K** | kaggle.com/datasets/ | 60K profiles | Upwork freelancer profiles with skills, rates, ratings |
| **Upwork Freelancers 50K** | kaggle.com/datasets/ | 50K profiles | Earlier collection of Upwork profiles |
| **Fiverr Gig Dataset** | kaggle.com/datasets/ | Various | Fiverr gig listings with categories, pricing, reviews |
| **Freelancer.com Projects** | kaggle.com/datasets/ | Various | Project listings from Freelancer.com with skill requirements |

### Key Insights from Freelance Data
- Upwork datasets are the most comprehensive for studying skill marketplace dynamics
- Pricing data reveals significant variance by skill category and provider location
- Rating/review data enables trust model research

## Category 2: Job-Skill Matching Datasets

| Dataset | Description | ML Application |
|---------|-------------|----------------|
| **Data Science Job Postings & Skills (2024)** | LinkedIn job postings with skill requirements | Skill extraction, demand analysis |
| **Job Market & Skills Demand Dataset** | 10,000 synthetic postings for 2025 (AI, Blockchain, Green Tech, Quantum) | Demand forecasting |
| **IT Skills from Jobs** | Professional backgrounds, skills, educational qualifications | Career path analysis |
| **job-skill-set** | Designed for ML job matching and NLP tasks | Job matching, skill extraction |
| **Data_jobs_and_skills** | Data positions — availability, pay, required skills | Compensation modeling |
| **Future Jobs & Skills Demand 2025** | 10K synthetic postings across trending industries | Trend prediction |

### Key Insights from Job-Skill Data
- LinkedIn is the primary data source for real-world skill-job matching
- Synthetic datasets fill gaps for emerging/future skills
- Skill extraction from unstructured text is a solved-enough problem for practical use

## Category 3: Skills Taxonomy & Classification

| Dataset | Size | Description |
|---------|------|-------------|
| **Skills (3,291)** | 3,291 skills | Curated collection spanning diverse domains — useful as a skill taxonomy |
| **LinkedIn Jobs+Skills (1.3M)** | 1.3M jobs | Massive dataset linking jobs to required skills |
| **Vocational Skill-Job Matching** | Various | Vocational education skill-to-job mapping |

### Key Insights
- The 3,291 Skills dataset is the closest thing to a universal skill taxonomy on Kaggle
- LinkedIn's 1.3M dataset is the gold standard for skill-job relationship mining
- Vocational matching datasets bridge education and employment

## Category 4: Resume & Candidate Matching

| Dataset | Description |
|---------|-------------|
| **Resume Screening Dataset** | Resumes with skills, experience, education for automated screening |
| **All Skills Taxonomy** | Comprehensive skills taxonomy for resume parsing |

## Notable Notebooks & Analyses

| Notebook | Approach | Key Finding |
|----------|----------|-------------|
| **Exploring Job Market Trends & In-Demand Skills** | Adzuna API analysis | Real-time demand mapping |
| **Embedding-based Job Matching** | Sentence embeddings | Semantic skill matching outperforms keyword matching |
| **LLM Skill Matching with Gemini** | Google Gemini for matching | LLMs dramatically improve skill-to-job matching accuracy |
| **Freelance Market Analysis** | Statistical analysis | Pricing models, skill demand curves |
| **Job Skills Network Analysis** | Graph-based | Skill co-occurrence networks reveal career paths |

## ML Approaches Documented on Kaggle

| Approach | Description | Best For |
|----------|-------------|----------|
| **NLP/Text Processing** | Skill extraction from unstructured text | Processing job postings, resumes |
| **Embedding-based Matching** | Semantic similarity via embeddings | Matching candidates to jobs |
| **LLM-powered Matching** | Using Gemini/GPT for intelligent matching | Complex multi-skill matching |
| **Classification** | Categorizing skills into taxonomies | Organizing skill marketplaces |
| **Recommendation Systems** | Collaborative filtering for skills | "People with X skill also learned Y" |
| **Pricing Analysis** | Regression/statistical models | Fair pricing, demand-based pricing |

## Prioritized Data Sources for Building a Skill Marketplace

### Tier 1 — Immediate Use
1. LinkedIn Jobs+Skills (1.3M) — skill-job relationships at scale
2. Skills Taxonomy (3,291) — baseline skill categorization
3. Upwork 60K — real marketplace pricing and rating data

### Tier 2 — Model Development
4. Job-Skill-Set — purpose-built for ML job matching
5. Data Science Job Postings (2024) — real LinkedIn postings
6. Future Jobs & Skills Demand 2025 — forward-looking synthetic data

### Tier 3 — Enrichment
7. IT Skills from Jobs — professional background context
8. Resume Screening Dataset — candidate-side data
9. Freelancer.com Projects — project-based skill requirements

### Tier 4 — Emerging
10. Agentic competition datasets — first AI agent skill benchmarks
11. LLM benchmark datasets — evaluating skill execution quality

## Data Gaps Identified

1. **Buyer-side data** — Almost all datasets focus on supply (providers/skills), not demand (buyers/outcomes)
2. **Skill verification data** — No datasets on skill quality assessment or verification
3. **Transaction outcome data** — Missing: did the hired freelancer actually deliver?
4. **Real-time pricing** — Static snapshots, no dynamic pricing data
5. **AI agent skill performance** — No benchmark datasets for agent skill execution quality
6. **Cross-platform data** — No datasets spanning multiple marketplaces for comparison
7. **Skill evolution data** — How skills change in demand over time (longitudinal)

## Agentic Competitions Emerging

- First explicitly "agentic" competition on Kaggle (legal information retrieval)
- Multi-agent solvers appearing in competitive settings
- Benchmark datasets for agent skill evaluation beginning to accumulate
- Kaggle itself becoming a testing ground for AI agent capabilities
