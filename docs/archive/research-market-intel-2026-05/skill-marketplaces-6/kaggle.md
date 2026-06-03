# Kaggle Datasets & Competitions for Skill Marketplace R&D

> **Research Date:** July 2025  
> **Scope:** Kaggle datasets, competitions, notebooks, and discussions relevant to skill marketplaces, talent matching, freelance platforms, and AI-powered career/job recommendation systems.

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Tier 1: Directly Relevant Datasets](#tier-1-directly-relevant-datasets)
3. [Tier 2: Freelance Platform & Gig Economy Data](#tier-2-freelance-platform--gig-economy-data)
4. [Tier 3: Skill Taxonomies & Knowledge Graphs](#tier-3-skill-taxonomies--knowledge-graphs)
5. [Tier 4: AI Job Market & Emerging Roles](#tier-4-ai-job-market--emerging-roles)
6. [Tier 5: Supporting Datasets](#tier-5-supporting-datasets)
7. [Relevant Kaggle Notebooks & Code](#relevant-kaggle-notebooks--code)
8. [Kaggle Discussions on Marketplace Matching](#kaggle-discussions-on-marketplace-matching)
9. [ML Approaches & Techniques Observed](#ml-approaches--techniques-observed)
10. [Evolution of the Data Landscape](#evolution-of-the-data-landscape)
11. [Potential Data Sources for Skill Marketplace R&D](#potential-data-sources-for-skill-marketplace-rd)
12. [Recommendations & Next Steps](#recommendations--next-steps)

---

## Executive Summary

The Kaggle ecosystem has matured significantly for skill marketplace research. As of mid-2025, there are **25+ directly relevant datasets** spanning skill-job matching, freelance platform analytics, career recommendation systems, and skill taxonomies. Key trends:

- **Explosion of skill-matching datasets:** Multiple new datasets specifically designed for ML-powered skill-to-job matching (e.g., Vocational Skill-Job Matching, Job Recommendation Dataset, JobFit notebooks)
- **Large-scale freelance data:** Real datasets with 1.3M+ freelance contracts and 50K+ Upwork job postings now available
- **Skill embeddings & taxonomies:** O*NET + ESCO combined skill embeddings datasets enable semantic skill matching
- **AI/LLM-era job market data:** New datasets capturing emerging roles (LLM Engineer, RAG Engineer, AI Agent Developer) that didn't exist in older datasets
- **Shift toward agentic AI:** Datasets tracking autonomous AI agent applications across industries, relevant for AI-agent skill marketplaces

---

## Tier 1: Directly Relevant Datasets

### 1.1 Vocational Skill-Job Matching Dataset (star)(star)(star)
- **URL:** https://www.kaggle.com/datasets/ziya07/vocational-skill-job-matching-dataset
- **Creator:** Ziya07
- **License:** CC0: Public Domain
- **Size:** 2,809 rows (student-job pairs)
- **Description:** Purpose-built for ML-powered skill-job matching recommendation systems. Contains student profiles, skill scores (5 core skills on 0-10 scale), certifications, academic performance, and corresponding job requirements with a binary match target.
- **Key Columns:**
  - Student Profile: Age, gender, vocational program, academic performance, certifications, internship experience
  - Skill Scores: Five core skill proficiency levels (0-10 scale)
  - Job Requirements: Job title, required skill levels, minimum experience, location
  - **Target: `Job_Match`** (1 = Match, 0 = No Match)
- **Relevance to Skill Marketplaces:** **VERY HIGH** -- This is essentially a ready-made training set for skill-based matching algorithms. The structured skill-score vs. job-requirement format mirrors what a skill marketplace would need.
- **Use Cases:** Classification experiments, feature importance analysis, recommendation system prototyping

### 1.2 Job Recommendation Dataset (star)(star)(star)
- **URL:** https://www.kaggle.com/datasets/lastman0800/job-recomendation-dataset
- **Creator:** lastman0800
- **Size:** User-job pairs with skill matching
- **Key Columns:**
  - `User_ID`, `Job_ID`
  - `User_Skills` -- comma-separated skill list
  - `Job_Requirements` -- comma-separated required skills
  - `Match_Score` -- continuous 0-1 score
  - `Recommended` -- binary recommendation label
- **Relevance:** **VERY HIGH** -- Direct two-sided marketplace matching data. The Match_Score provides ground truth for skill-to-job alignment quality.

### 1.3 Job Skill Set (LinkedIn-derived) (star)(star)(star)
- **URL:** https://www.kaggle.com/datasets/batuhanmutlu/job-skill-set
- **Creator:** Batuhan Mutlu
- **License:** CC BY-SA 4.0
- **Source:** Enhanced from LinkedIn Job Postings dataset using RecAI API for skill extraction
- **Key Columns:**
  - `job_id`, `category` (IT, Business Dev, Finance, Sales, HR)
  - `job_title`, `job_description`
  - `job_skill_set` -- extracted hard and soft skills via RecAI APIs
- **Relevance:** **VERY HIGH** -- Real LinkedIn data with AI-extracted skills. The RecAI API skill extraction approach is directly applicable to marketplace skill inference.

### 1.4 AI-Powered Job Recommendations (star)(star)
- **URL:** https://www.kaggle.com/datasets/samayashar/ai-powered-job-recommendations
- **Creator:** Samay Ashar
- **License:** CC0: Public Domain
- **Size:** 50,000 job postings
- **Key Columns:**
  - `job_title`, `company`, `location`, `experience_level`
  - `salary_range` ($40K-$150K), `industry`
  - `required_skills` -- 1,559 unique skills
- **Techniques Referenced:** XGBoost, LightGBM, Neural Networks, Recommender Systems
- **Relevance:** **HIGH** -- Large-scale structured job data suitable for training recommendation models. The 50K size makes it practical for deep learning approaches.

### 1.5 Jobs and Skills Mapping for Career Analysis (star)(star)
- **URL:** https://www.kaggle.com/datasets/emaadakhter/jobs-and-skills-mapping-for-career-analysis
- **Creator:** emaad akhter
- **License:** MIT
- **Key Columns:**
  - `job_title`, `Short_description`
  - `Skills_required` (semicolon-separated)
  - `Industry`, `Pay_grade` (Low, Mid, High)
- **Relevance:** **HIGH** -- Clean skill-to-job mapping data ideal for NLP fine-tuning, career recommendation, and labor market analysis.

### 1.6 AI-Based Career Recommendation System (star)(star)
- **URL:** https://www.kaggle.com/datasets/adilshamim8/ai-based-career-recommendation-system
- **Creator:** Adil Shamim
- **Size:** 200 records
- **Key Columns:**
  - `Skills`, `Interests`, `Education`, `Age`
  - `Recommended_Career` -- AI-predicted best-fit career
  - `Recommendation_Score` -- confidence score (0.85-0.95)
- **Relevance:** **MODERATE-HIGH** -- Small but well-structured. The recommendation score concept maps to marketplace match confidence.

### 1.7 Career Recommender Dataset (star)(star)
- **URL:** https://www.kaggle.com/datasets/siddardhashayini3/career-recommender-dataset
- **Creator:** Siddardha Shayini
- **License:** CC0: Public Domain
- **Description:** Maps skills, qualifications, and preferences to suitable job roles. Includes info on professions, required skills, educational backgrounds, and industry trends.

### 1.8 Skill & Career Recommendation Dataset (star)(star)
- **URL:** https://www.kaggle.com/datasets/tea340yashjoshi/skill-and-career-recommendation-dataset
- **Creator:** YASH JOSHI
- **License:** Open Database
- **Description:** Foundation for predicting career paths based on students' skills and academic performance. Uses Gardner's Multiple Intelligences framework (Linguistic, Musical, Bodily, Logical-Mathematical, Spatial, Interpersonal, Intrapersonal, Naturalist scores).
- **Unique Angle:** The Multiple Intelligences approach provides a different axis for skill assessment beyond technical skills -- relevant for soft-skill marketplaces.

### 1.9 Recruitment Dataset (star)(star)
- **URL:** https://www.kaggle.com/datasets/surendra365/recruitement-dataset
- **Creator:** Surendra Kumar Nellore
- **License:** Open Database
- **Key Columns:**
  - `Resume` -- full text resume content
  - `Job Roles`, `Job Description`
  - `Best Match` -- label/score for applicant-job fit
- **Relevance:** **HIGH** -- Resume-to-job matching with ground truth labels. Directly models the marketplace matching problem.

---

## Tier 2: Freelance Platform & Gig Economy Data

### 2.1 Freelance Contracts Dataset (1.3 Million Entries) (star)(star)(star)
- **URL:** https://www.kaggle.com/datasets/asaniczka/freelance-contracts-dataset-1-3-million-entries
- **Creator:** asaniczka
- **License:** ODC Attribution License (ODC-By)
- **Size:** 1.3 million contracts
- **Description:** Extracted from a leading freelancing platform. Includes job ID, title, start/end dates, freelancer ID, total hours worked, total amount paid, and hourly rates.
- **Relevance:** **VERY HIGH** -- The largest freelance marketplace dataset on Kaggle. Ideal for pricing models, market dynamics analysis, freelancer performance prediction, and understanding marketplace economics.
- **Key Applications:**
  - Freelance pricing strategy optimization
  - Project duration vs. earnings analysis
  - Freelancer performance modeling
  - Market trend analysis

### 2.2 Upwork Job Postings Dataset 2024 (50K Records) (star)(star)(star)
- **URL:** https://www.kaggle.com/datasets/asaniczka/upwork-job-postings-dataset-2024-50k-records
- **Creator:** asaniczka
- **License:** ODC Attribution License (ODC-By)
- **Size:** 50,000 job postings (real data from 2-week collection period)
- **Description:** Real-time data from Upwork spanning various categories and countries. Enables analysis of skills demand, pricing strategies, and geographical preferences.
- **Suggested Tasks:** In-demand skill analysis, budget prediction from descriptions, freelancer recommendation systems, NLP categorization of job descriptions
- **Relevance:** **VERY HIGH** -- Real marketplace data from one of the largest freelance platforms.

### 2.3 Synthetic Freelance Job Platform Dataset (star)(star)
- **URL:** https://www.kaggle.com/datasets/emirhanakku/synthetic-freelance-job-platform-dataset
- **Creator:** Emirhan Akkus
- **License:** CC BY 4.0
- **Size:** 1,000 synthetic job postings
- **Key Features:**
  - Rich `job_description` field (NLP-ready)
  - `budget_usd` (clipped normal ~$500), `duration_days` (exponential)
  - `num_applicants` (Poisson), `hired` status, `freelancer_rating`
  - `completion_time_days`, `success` flag
  - 7 categories: Design, Development, Writing, Marketing, Data Science, Translation, Video Editing
- **Relevance:** **HIGH** -- Realistic distributions, well-documented generation process. Excellent for prototyping marketplace ML pipelines (classification, regression, NLP).

### 2.4 Freelancer Data Analysis Jobs (Freelancer.com) (star)(star)
- **URL:** https://www.kaggle.com/datasets/isaacoresanya/freelancer
- **Creator:** IsaacOresanya
- **License:** MIT
- **Size:** 9,193 job postings scraped from Freelancer.com
- **Description:** Job titles, skills, rates, and client preferences from real freelance platform data.

### 2.5 Freelancer Earnings & Job Trends (star)(star)
- **URL:** https://www.kaggle.com/datasets/shohinurpervezshohan/freelancer-earnings-and-job-trends
- **Creator:** Shohinur Pervez Shohan
- **License:** CC0: Public Domain
- **Key Columns:**
  - `job_category`, `hourly_rate`, `project_budget`
  - `demand_score` (1-10), `skills_required`, `time_period`
- **Relevance:** **HIGH** -- The demand_score and skills_required columns directly support skill-demand forecasting.

### 2.6 Global Freelance Stats 2025 (star)
- **URL:** https://www.kaggle.com/datasets/abdullahbutt1234/globalfreelancestats2025
- **Creator:** M Abdullah Butt
- **License:** CC0: Public Domain
- **Description:** Aggregated from LinkedIn, Upwork, Freelancer, and Fiverr statistics. Provides macro-level view of freelancing trends.

---

## Tier 3: Skill Taxonomies & Knowledge Graphs

### 3.1 Skills Dataset with Embeddings (O*NET + ESCO) (star)(star)(star)
- **URL:** https://www.kaggle.com/datasets/paiky1995/skills-dataset-with-embeddings
- **Creator:** paiky1995
- **License:** CC0: Public Domain
- **Description:** Combined O*NET and ESCO skill datasets into an exhaustive skills dictionary with pre-computed embeddings using `sentence-transformers/all-mpnet-base-v2`.
- **Columns:** `skill` (name), `embedding` (vector representation)
- **Relevance:** **CRITICAL** -- This is a foundational resource for any skill marketplace. Pre-computed skill embeddings enable:
  - Semantic skill matching (cosine similarity between skill vectors)
  - Skill taxonomy navigation
  - Cross-framework skill mapping (O*NET <-> ESCO)
  - Zero-shot skill inference

### 3.2 O*NET Database (v29.0) (star)(star)(star)
- **URL:** https://www.kaggle.com/datasets/emarkhauser/onet-29-0-database
- **Creator:** emarkhauser
- **License:** CC BY 4.0
- **Description:** The authoritative U.S. occupational information system. Rich variables describing work and worker characteristics, including skill requirements for hundreds of occupations.
- **Relevance:** **CRITICAL** -- The gold standard for occupational skill taxonomies. Essential foundation for any skill marketplace's taxonomy layer.

### 3.3 Occupational Skills and Tasks (star)(star)(star)
- **URL:** https://www.kaggle.com/datasets/thedevastator/occupational-skills-and-tasks
- **Creator:** The Devastator (sourced from Zenodo)
- **License:** CC0: Public Domain
- **Description:** Maps occupational skills to tasks, reconciled with the JRC-Eurofound Task Taxonomy. Sourced from online job advertisements showing how skill and task requirements change over time.
- **Relevance:** **VERY HIGH** -- The skill-to-task mapping is essential for understanding what skills actually enable what work outputs -- critical for marketplace matching quality.

### 3.4 List of All Skills (LinkedIn + GitHub + StackOverflow) (star)(star)
- **URL:** https://www.kaggle.com/datasets/arbazkhan971/allskillandnonskill
- **Creator:** arbazkhan971
- **Description:** Comprehensive skill collection aggregated from LinkedIn, GitHub, StackOverflow, and job platforms (Naukri, Indeed, Monster.com). Claims to be the "World's Largest Collection of Skills."
- **Relevance:** **HIGH** -- Useful for building comprehensive skill dictionaries and NER training sets for skill extraction.

---

## Tier 4: AI Job Market & Emerging Roles

### 4.1 AI Jobs Market 2025-2026 | Salaries (star)(star)(star)
- **URL:** https://www.kaggle.com/datasets/alitaqishah/ai-jobs-market-2025-2026-salaries
- **Creator:** Syed Ali Taqi
- **License:** CC0: Public Domain
- **Size:** 1,500 job postings (2025-2026)
- **Coverage:** 25 AI/ML roles, 14 countries, 12 industries, 5 company sizes
- **Key Differentiator:** Covers **emerging roles** -- LLM Engineer, RAG Engineer, AI Agent Developer, Prompt Engineer -- that don't exist in older datasets.
- **Key Columns:**
  - `required_skills` (pipe-separated)
  - `ai_salary_premium_pct` -- salary premium vs non-AI equivalent
  - `demand_score` -- market demand 0-100
  - `remote_work`, `company_size`
- **Relevance:** **VERY HIGH** -- Captures the cutting edge of the AI job market. The demand_score and salary_premium columns are directly applicable to marketplace pricing and demand forecasting for AI skills.

### 4.2 AI-Powered Resume Screening Dataset (2025) (star)(star)
- **URL:** https://www.kaggle.com/datasets/mdtalhask/ai-powered-resume-screening-dataset-2025
- **Creator:** Paradeveloper
- **License:** CC BY-SA 4.0
- **Size:** 1,000+ synthetic resumes
- **Key Columns:**
  - `Skills`, `Experience`, `Education`, `Certifications`
  - `Job Role`, `AI Score (0-100)` -- AI-based ranking score
  - `Recruiter Decision` -- Hire/Reject
  - `Salary Expectation ($)`, `Projects Count`
- **Relevance:** **HIGH** -- Models the AI screening pipeline. The AI Score vs. Recruiter Decision gap is interesting for studying algorithmic bias in marketplace matching.

### 4.3 Agentic AI Applications 2025 (star)(star)
- **URL:** https://www.kaggle.com/datasets/hajraamir21/agentic-ai-applications-2025
- **Creator:** Hajra Amir
- **License:** CC0: Public Domain
- **Key Columns:**
  - `Industry`, `Application Area`, `AI Agent Name`
  - `Task Description`, `Technology Stack`
  - `Outcome Metrics`, `Deployment Year`, `Geographical Region`
- **Relevance:** **MODERATE** -- Tracks how autonomous AI agents are being deployed across industries. Relevant for understanding which tasks/skills are being automated vs. augmented.

### 4.4 AI Tool Directory 2026: 19,000+ Real-World Tools (star)(star)
- **URL:** https://www.kaggle.com/datasets/harshlakhani2005/ai-tool-directory-2026-10000-real-world-tools
- **Creator:** Harsh Lakhani
- **License:** CC0: Public Domain
- **Size:** 19,000 AI tools
- **Key Columns:**
  - `AI_Name`, `Developer`, `Release_Year`
  - `Intelligence_Type` (Generative, Agentic, Multimodal)
  - `Primary_Domain`, `Key_Functionality`
  - `Pricing_Model`, `API_Availability`
- **Relevance:** **MODERATE** -- Maps the AI tool ecosystem. Relevant for understanding what AI capabilities exist that could be offered as marketplace "skills."

---

## Tier 5: Supporting Datasets

### 5.1 Jobs Data for Recommender Systems (star)
- **URL:** https://www.kaggle.com/datasets/tondji/jobs-data-for-recommender-systems
- **License:** CC0: Public Domain
- Pre-crawled job data with description, title, type, skills, salary, sector. France-focused.

### 5.2 Personalized Recommendation Systems Dataset (star)
- **URL:** https://www.kaggle.com/datasets/alfarisbachmid/personalized-recommendation-systems-dataset
- Rich metadata for exploring personalized recommendation approaches.

---

## Relevant Kaggle Notebooks & Code

### JobFit: Tailored Recommendations Based on Skills (star)(star)(star)
- **URL:** https://www.kaggle.com/code/morpho23/jobfit-tailored-recommendations-based-on-skills
- **Data:** LinkedIn Job Postings (2023-2024)
- **Approach:** End-to-end job recommender using **hybrid techniques** -- text vectorization, skill embeddings, and semantic matching
- **Relevance:** Demonstrates modern multi-signal recommendation approach for skill-based matching

### Freelance Trends: Budget, Demand & Success Drivers (star)(star)
- **URL:** https://www.kaggle.com/code/hammadrehmani/freelance-trends-budget-demand-success-drivers
- **Data:** Synthetic Freelance Job Platform Dataset
- **Focus:** Understanding budget allocation, demand patterns, and success factors in freelance work

### Freelance Jobs Analysis (Upwork) (star)(star)
- **URL:** https://www.kaggle.com/code/ahmedmyalo/freelance-jobs-analysis-upwork
- **Data:** Upwork freelance jobs (60K+)
- **Description:** Comprehensive marketplace data analysis -- "ecosystems teeming with data waiting to be decoded"

### Skill Extractor (star)(star)
- **URL:** https://www.kaggle.com/code/arbazkhan971/skill-extractor
- **Data:** Job Description Skill dataset
- **Focus:** NLP-based skill extraction from job descriptions -- core technology for marketplace skill inference

### Recommending Employee Training Courses (star)(star)
- **URL:** https://www.kaggle.com/code/aryashah2k/recommending-employee-training-courses
- **Data:** HR Analytics datasets
- **Focus:** Using AI to analyze peer ratings and recommend training programs -- relevant for internal talent marketplace skill development

### Freelancer Earnings Analysis and Prediction (star)
- **URL:** https://www.kaggle.com/code/muhammedaliyilmazz/freelancer-earnings-analysis-and-prediction
- **Focus:** Predictive modeling of freelancer earnings across industries and skill categories

---

## Kaggle Discussions on Marketplace Matching

### Two-Sided Market Matching
- **URL:** https://www.kaggle.com/discussions/questions-and-answers/73011
- **Context:** "I work for a web platform 2 sided market which matches available consultants to short term contracts. We currently have a rules based algorithm which matches..."
- **Relevance:** Direct industry discussion about upgrading from rules-based to ML matching in a skill marketplace.

### Buyer-Seller Matching in Marketplace
- **URL:** https://www.kaggle.com/discussions/questions-and-answers/57666
- **Context:** "I am working on a problem to match buyers and sellers in a B2B marketplace. The main aim is to provide relevant recommendations to buyers about sellers."
- **Relevance:** Discusses collaborative filtering, content-based, and hybrid approaches for marketplace matching.

### A Marketplace for Algorithms
- **URL:** https://www.kaggle.com/discussions/general/110436
- **Relevance:** Meta-discussion about algorithm marketplaces -- models as tradeable skills.

### Matching: Classify Offers on Marketplace (Competition)
- **URL:** https://www.kaggle.com/competitions/matching-to-classify-the-offers-on-marketplace/data
- **Description:** Binary classification competition for product/offer matching on a marketplace platform.

---

## ML Approaches & Techniques Observed

### 1. Skill Embedding & Semantic Matching
- **Pre-trained embeddings:** `sentence-transformers/all-mpnet-base-v2` used for skill embeddings (Skills Dataset with Embeddings)
- **Approach:** Encode skills as dense vectors -> compute cosine similarity for matching
- **Advantage:** Handles synonyms, related skills, and cross-taxonomy mapping automatically

### 2. Hybrid Recommendation Systems
- **Text vectorization + Skill embeddings + Semantic matching** (JobFit notebook)
- Combines collaborative filtering with content-based approaches
- XGBoost, LightGBM, and neural networks for recommendation scoring

### 3. NLP-Based Skill Extraction
- **RecAI APIs** for automated skill parsing from job descriptions
- Named Entity Recognition (NER) for skill identification
- TF-IDF and transformer-based embeddings for skill classification

### 4. Classification for Match Prediction
- Binary classification (Match/No Match) on structured skill scores
- Feature importance analysis to understand which skills drive hiring decisions
- Random Forest, Gradient Boosting, and Neural Network classifiers

### 5. Regression for Marketplace Economics
- Budget/salary prediction from job features and descriptions
- Project completion time estimation
- Demand score forecasting for skill categories

### 6. Graph-Based Approaches
- Knowledge graphs linking skills -> tasks -> occupations (O*NET, ESCO, JRC taxonomy)
- Skill adjacency and transferability modeling

### 7. Multi-Intelligence Assessment
- Gardner's Multiple Intelligences framework for holistic skill profiling
- Beyond technical skills: linguistic, interpersonal, spatial-visualization scoring

---

## Evolution of the Data Landscape

### Pre-2023: Foundation Era
- O*NET database as the primary occupational taxonomy
- Basic job posting datasets (Indeed, Monster scrapes)
- Limited structured skill-to-job mapping data
- Focus on traditional job categories

### 2023-2024: Marketplace Data Explosion
- Real platform data becomes available: Upwork 50K records, Freelancer.com scrapes
- LinkedIn job postings enhanced with AI skill extraction (RecAI)
- First large-scale freelance contract datasets (1.3M entries)
- Emergence of purpose-built recommendation system datasets

### 2025-2026: AI-Native & Agentic Era
- **New job roles emerge in datasets:** LLM Engineer, RAG Engineer, AI Agent Developer, Prompt Engineer
- **Skill embeddings become commoditized:** O*NET + ESCO combined with sentence-transformer embeddings
- **Synthetic data gains acceptance:** Well-designed synthetic datasets (Synthetic Freelance Platform) with documented statistical distributions
- **AI screening enters mainstream:** Datasets capturing AI screening scores alongside recruiter decisions
- **Agentic AI tracking:** Datasets cataloging autonomous AI applications across industries
- **AI tool ecosystem mapped:** 19,000+ AI tools cataloged with capability classifications
- **Demand scoring matures:** Multiple datasets now include numerical demand scores for skills/roles

### Key Shift: From "Job Listings" to "Marketplace Intelligence"
The datasets have evolved from simple job listing scrapes to rich, multi-dimensional marketplace data that captures:
- Supply-demand dynamics (demand scores, applicant counts)
- Pricing intelligence (hourly rates, budgets, salary premiums)
- Quality signals (ratings, success flags, match scores)
- Temporal dynamics (trend data, time periods)
- Geographic distributions across 14+ countries

---

## Potential Data Sources for Skill Marketplace R&D

### Immediate Use (Download & Train)

| Dataset | Size | Best For |
|---------|------|----------|
| Vocational Skill-Job Matching | 2,809 pairs | Skill match classification |
| Freelance Contracts 1.3M | 1.3M records | Marketplace economics, pricing |
| Upwork Job Postings 2024 | 50K postings | Real marketplace demand analysis |
| Skills with Embeddings | Full O*NET+ESCO | Semantic skill matching foundation |
| AI Jobs Market 2025-2026 | 1,500 postings | AI skill demand forecasting |
| Job Skill Set (LinkedIn) | LinkedIn-scale | Skill extraction training |
| AI-Powered Job Recommendations | 50K postings | Recommendation model training |
| Job Recommendation Dataset | User-job pairs | Match score prediction |

### Combine for Maximum Value

1. **Skill Foundation:** O*NET Database + ESCO + Skills with Embeddings -> comprehensive skill taxonomy with vector representations
2. **Real Marketplace Data:** Upwork 50K + Freelance Contracts 1.3M + Freelancer.com 9K -> multi-platform marketplace dynamics
3. **Matching Training:** Vocational Skill-Job Matching + Job Recommendation Dataset + Recruitment Dataset -> supervised matching models
4. **Demand Intelligence:** AI Jobs 2025-2026 + Freelancer Earnings & Trends -> skill demand forecasting
5. **NLP Pipeline:** Job Skill Set + All Skills list + Skill Extractor notebook -> end-to-end skill extraction system

### Build Pipelines Around

1. **Skill Extraction Pipeline:** Job descriptions -> NER/extraction -> canonical skill mapping -> embedding
2. **Match Scoring Pipeline:** User skills + Job requirements -> feature engineering -> match prediction -> ranking
3. **Pricing Intelligence Pipeline:** Contract data -> rate prediction -> budget estimation -> demand forecasting
4. **Taxonomy Management Pipeline:** O*NET/ESCO -> embeddings -> clustering -> dynamic taxonomy updates

---

## Recommendations & Next Steps

### High Priority
1. **Download & explore** the Skills Dataset with Embeddings -- it provides the semantic foundation for any skill matching system
2. **Benchmark** matching algorithms on the Vocational Skill-Job Matching dataset and Job Recommendation Dataset
3. **Analyze** the 1.3M Freelance Contracts for marketplace economic modeling
4. **Adapt** the JobFit notebook's hybrid recommendation approach for skill marketplace contexts

### Medium Priority
5. **Build** a skill extraction pipeline using the Job Skill Set dataset and RecAI-style approach
6. **Map** emerging AI roles (from AI Jobs 2025-2026) to traditional skill frameworks
7. **Study** the Synthetic Freelance dataset's distribution modeling for marketplace simulation

### Exploratory
8. **Investigate** the Two-Sided Market Matching discussion thread for practical industry insights
9. **Consider** the Multiple Intelligences angle for soft-skill marketplace differentiation
10. **Monitor** Kaggle competitions related to marketplace matching (e.g., "Matching: Classify Offers")

### Gaps to Fill
- No large-scale **internal talent marketplace** datasets found on Kaggle (enterprise mobility data is proprietary)
- Limited **real-time skill demand** data (most datasets are snapshots, not streams)
- No **multi-modal skill assessment** datasets (e.g., combining portfolio artifacts + skill claims + endorsements)
- Absence of **skill depreciation/evolution** longitudinal data
- No **two-sided marketplace outcome** data (i.e., post-match satisfaction, repeat engagement)

---

*This research identified 25+ datasets, 6 notebooks, 3 discussion threads, and 1 competition directly relevant to skill marketplace R&D across the Kaggle ecosystem.*
