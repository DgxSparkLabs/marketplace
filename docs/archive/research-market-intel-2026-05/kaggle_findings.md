# Kaggle Datasets & Competitions for Skill Marketplace Research

> **Research Date:** July 2025  
> **Search Queries:** 5 DuckDuckGo searches across Kaggle for skill marketplaces, freelance platforms, talent matching, and job-skill datasets  
> **Total Unique Results Analyzed:** 60+ results across all searches, 21 datasets scraped in detail

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Freelance Marketplace Datasets](#1-freelance-marketplace-datasets)
3. [Job-Skill Matching & Recommendation Datasets](#2-job-skill-matching--recommendation-datasets)
4. [Skills Taxonomy & Extraction Datasets](#3-skills-taxonomy--extraction-datasets)
5. [Resume Screening & Talent Acquisition Datasets](#4-resume-screening--talent-acquisition-datasets)
6. [Large-Scale Job Market Datasets](#5-large-scale-job-market-datasets)
7. [Notable Notebooks & Analyses](#6-notable-notebooks--analyses)
8. [Data Science Approaches to Skill Matching](#7-data-science-approaches-to-skill-matching)
9. [Competition Insights](#8-competition-insights)
10. [Potential Data Sources for Building a Skill Marketplace](#9-potential-data-sources-for-building-a-skill-marketplace)
11. [Recommendations](#10-recommendations)

---

## Executive Summary

There is a **rich ecosystem of Kaggle datasets** directly relevant to building a skill marketplace. The research uncovered **30+ relevant datasets** spanning freelance marketplace data (Upwork, Fiverr, Freelancer.com), job-skill matching systems, skills taxonomies, resume screening, and large-scale job market data. While no Kaggle competition directly targets "skill marketplaces," several competitions and notebooks address the core ML problems: **skill extraction, talent matching, job recommendation, and pricing optimization**.

### Key Takeaways
- **Upwork is the most data-rich platform** with 5+ scraped datasets (up to 60K+ job postings)
- **Fiverr has 3+ datasets** covering gig pricing, ratings, and freelancer profiles
- **LinkedIn provides the largest scale** with a 1.3M job+skills dataset
- **Skill-job matching** is an active research area with purpose-built ML datasets
- **NLP/embeddings approaches** are the dominant method for skill matching
- **No direct "skill marketplace" competition exists**, but related challenges in job recommendation and resume screening provide transferable insights

---

## 1. Freelance Marketplace Datasets

### 1.1 Upwork Datasets

| Dataset | URL | Size | Description |
|---------|-----|------|-------------|
| **Upwork Job Postings 2024 (50K)** | [Link](https://www.kaggle.com/datasets/asaniczka/upwork-job-postings-dataset-2024-50k-records) | 50,000 jobs | Real-time data collected over 2 weeks. Includes job titles, descriptions, categories, countries, budget info (hourly/fixed), and skills. Ideal for demand analysis, pricing prediction, and recommendation systems. |
| **Upwork Freelance Jobs (+60K)** | [Link](https://www.kaggle.com/datasets/ahmedmyalo/upwork-freelance-jobs-60k) | 60,000+ jobs | Scraped Feb-Mar 2023 covering 3D/Art, programming, and marketing sectors. Cleaned and organized with rich metadata. Created by a Top-Rated Upwork freelancer. |
| **Upwork Jobs (Researchers)** | [Link](https://www.kaggle.com/datasets/thedevastator/upwork-jobs-a-dataset-for-researchers) | Sample | January 2022 postings. Includes job title, description, employment type, skills required, client location, hours/week, duration, fixed price, experience level, project type, client history (jobs posted, total spent). |
| **Upwork Jobs (hashiromer)** | [Link](https://www.kaggle.com/datasets/hashiromer/upwork-jobs) | Varies | Unbiased random sample of Upwork.com listings. Raw data available. Includes skills, budgets, client information. |
| **Upwork Freelancers & Agency Records** | [Link](https://www.kaggle.com/datasets/riyaiitiansamanta/upwork-dataset-of-freelancers-and-agency-records) | Varies | Freelancer and agency profile data from Upwork. |
| **Data Science Freelancer Listings: Upwork** | [Link](https://www.kaggle.com/datasets/kanchana1990/data-science-freelancer-listingsupwork-dataset) | 130+ profiles | Curated data science professionals on Upwork. Includes expertise, pricing strategies, hourly rates, job success rates, geographic diversity. Great for market trend and skill analysis. |

### 1.2 Fiverr Datasets

| Dataset | URL | Size | Description |
|---------|-----|------|-------------|
| **Fiverr Gig Details** | [Link](https://www.kaggle.com/datasets/aniketanilmali/fiverr-gig-details) | Varies | Logo designer gigs with ratings, review counts, pricing tiers (Basic/Standard/Premium), delivery times, revisions, star ratings, seller country, response time, and member duration. |
| **Fiverr Freelancers Web Scraping Dataset** | [Link](https://www.kaggle.com/datasets/asarli/fiverr-freelancers-web-scraping-dataset) | Varies | Web scraping gigs with titles, seller levels, ratings, pricing, delivery time, descriptions. Useful for pricing analysis, market research, and ML experiments. |
| **Fiverr Data Gigs** | [Link](https://www.kaggle.com/datasets/muhammadadiltalay/fiverr-data-gigs) | Varies | Data science freelance gigs from Fiverr across data processing, engineering, and data science categories. Includes gig titles, ratings, prices (converted to USD), and seller levels. |

### 1.3 Freelancer.com Dataset

| Dataset | URL | Size | Description |
|---------|-----|------|-------------|
| **Freelancer Data Analysis Jobs** | [Link](https://www.kaggle.com/datasets/isaacoresanya/freelancer) | 9,193 jobs | Data analysis job postings from Freelancer.com with titles, skills, rates, and client preferences. |

### 1.4 General Freelancer Datasets

| Dataset | URL | Size | Description |
|---------|-----|------|-------------|
| **Freelancer Earnings & Job Trends** | [Link](https://www.kaggle.com/datasets/shohinurpervezshohan/freelancer-earnings-and-job-trends) | Varies | Comprehensive earnings data across industries/skill categories. Columns: job_category, hourly_rate, project_budget, demand_score, skills_required, time_period. Ideal for pricing and demand analysis. |
| **Global Freelancers (Raw) Dataset** | [Link](https://www.kaggle.com/datasets/urvishahir/global-freelancers-raw-dataset) | 1,000 profiles | Fictional but realistic freelancer profiles with demographics, skills, experience, hourly rates, ratings, satisfaction scores, and languages. Good for practicing data cleaning. |

---

## 2. Job-Skill Matching & Recommendation Datasets

These datasets are **directly applicable** to building skill marketplace matching algorithms:

| Dataset | URL | Size | Description | Key Application |
|---------|-----|------|-------------|-----------------|
| **Vocational Skill-Job Matching Dataset** | [Link](https://www.kaggle.com/datasets/ziya07/vocational-skill-job-matching-dataset) | 2,809 rows | Student-job pairs with skill scores (0-10), certifications, experience, and binary Job_Match target. | **Classification: does skill profile match job?** |
| **Job Skill Set** | [Link](https://www.kaggle.com/datasets/batuhanmutlu/job-skill-set) | Varies | Job roles, descriptions, and extracted skill sets (from LinkedIn postings via RecAI API). Categories: IT, Business Dev, Finance, Sales, HR. | **Skill extraction, job matching, NLP** |
| **AI-Powered Job Recommendations** | [Link](https://www.kaggle.com/datasets/samayashar/ai-powered-job-recommendations) | 50,000 jobs | Job postings with titles, companies, locations, experience levels, salary ranges, and required skills. | **Job recommendation systems, salary prediction** |
| **Industry-Education Skills Matching** | [Link](https://www.kaggle.com/datasets/programmer3/industry-education-skills-matching-dataset) | 5,000 rows | Technical/non-technical skills mapped to job categories and course types. 20+ skill attributes including programming, ML, cloud, cybersecurity, communication. | **Skill gap analysis, course recommendation** |
| **Skill & Career Recommendation Dataset** | [Link](https://www.kaggle.com/datasets/tea340yashjoshi/skill-and-career-recommendation-dataset) | Varies | Student skill profiles (linguistic, musical, logical-mathematical, spatial, interpersonal) mapped to career paths. | **Career recommendation systems** |
| **Jobs and Skills Mapping for Career Analysis** | [Link](https://www.kaggle.com/datasets/emaadakhter/jobs-and-skills-mapping-for-career-analysis) | Varies | Structured data: job titles, descriptions, key skills, industry categories, pay grades. | **AI/NLP career recommendation** |
| **AI-based Career Recommendation System** | [Link](https://www.kaggle.com/datasets/adilshamim8/ai-based-career-recommendation-system) | Varies | Skills, interests, and career paths for suggesting best careers. | **Career matching ML models** |

---

## 3. Skills Taxonomy & Extraction Datasets

| Dataset | URL | Size | Description |
|---------|-----|------|-------------|
| **List of All Skills (World's Largest)** | [Link](https://www.kaggle.com/datasets/arbazkhan971/allskillandnonskill) | 3,291+ skills | Comprehensive skill collection from LinkedIn, GitHub, Stack Overflow, Naukri, Indeed, Monster.com. Claims to be world's largest skills dataset. **Critical for building a skills taxonomy.** |
| **3291 Skills Dataset** | [Link](https://www.kaggle.com/datasets/zamamahmed211/skills) | 3,291 skills | Meticulously curated skills data spanning diverse domains. |
| **Resume/CV Skills Extraction Dataset** | [Link](https://www.kaggle.com/datasets/muqaddasejaz/resume-cv-skills-extraction-dataset) | 962 rows | Resume text mapped to job categories. Designed for skills extraction, resume classification, and talent matching via NLP. |
| **Employment Skills** | [Link](https://www.kaggle.com/datasets/maneeshdisodia/employment-skills) | Varies | Skill lookup data identifying various skills related to job types with associated values. |

---

## 4. Resume Screening & Talent Acquisition Datasets

| Dataset | URL | Size | Description |
|---------|-----|------|-------------|
| **Automating Talent** | [Link](https://www.kaggle.com/datasets/willianoliveiragibin/automating-talent) | Varies | Focused on ML for resume screening. Addresses matching skills with projects in service organizations. Discusses transitioning from manual to ML-automated screening. |
| **AI Resume Screening & Job Market (2026)** | [Link](https://www.kaggle.com/datasets/aminasalamt/ai-resume-screening-and-job-market-dataset-2026) | Varies | Synthetic dataset with candidate profiles, AI-generated resume/skill match scores, salary expectations, screening decisions. Supports bias analysis in automated recruitment. |
| **Resume Screening Dataset for NLP/ML** | [Link](https://www.kaggle.com/datasets/arunsaini0906/resume-screening-dataset-for-nlp-and-ml) | Varies | Structured resume text with skills, experience, education. Cleaned for semantic analysis. |
| **Updated Resume Dataset** | [Link](https://www.kaggle.com/datasets/jillanisofttech/updated-resume-dataset/) | Varies | For resume screening — selecting best talent among many applicants. |

---

## 5. Large-Scale Job Market Datasets

These provide massive training data for skill marketplace models:

| Dataset | URL | Scale | Description |
|---------|-----|-------|-------------|
| **1.3M LinkedIn Jobs & Skills (2024)** | [Link](https://www.kaggle.com/datasets/asaniczka/1-3m-linkedin-jobs-and-skills-2024) | **1.3 million** | The flagship dataset. Powers [SkillExplorer](https://skillexplorer.asaniczka.com/). Includes job listings with augmented skill data. Ideal for skills mapping, job recommendation, and market analysis. |
| **LinkedIn Job Postings (2023-2024)** | [Link](https://www.kaggle.com/datasets/arshkon/linkedin-job-postings) | Large | Snapshot of current job market from LinkedIn. |
| **Data Science Job Postings & Skills (2024)** | [Link](https://www.kaggle.com/datasets/asaniczka/data-science-job-postings-and-skills) | Varies | LinkedIn data science job postings with skills, titles, companies, locations. |
| **Job Market & Skills Demand Dataset** | [Link](https://www.kaggle.com/datasets/muqaddasejaz/job-market-and-skills-demand-dataset) | 10,000 | Synthetic 2025 projections across AI, Blockchain, Green Tech, Quantum Computing. |
| **Future Jobs & Skills Demand 2025** | [Link](https://www.kaggle.com/datasets/ahsanneural/future-jobs-and-skills-demand-2025) | 10,000 | Synthetic job postings across trending industries. |
| **Job Market Dataset (Global)** | [Link](https://www.kaggle.com/datasets/kundanbedmutha/job-market-dataset-global) | **500,000** | Large-scale synthetic global job market data. |

---

## 6. Notable Notebooks & Analyses

### Directly Relevant to Skill Marketplaces

| Notebook | URL | Approach |
|----------|-----|----------|
| **Job Recommendations with Embeddings** | [Link](https://www.kaggle.com/code/uycung/job-recommendations-with-embeddings) | Uses **vector embeddings** to improve job matching. Addresses limitations of traditional keyword-based matching. Directly applicable to skill marketplace matching engines. |
| **Skills Matching with Gemini** | [Link](https://www.kaggle.com/code/poxman100/skills-matching-with-gemini/notebook) | Uses **Google Gemini** LLM to match resumes to job descriptions. Feeds 3 resumes + 1 job description, asks which candidate is most suitable. |
| **Predicting Resume-Job Match Score Using Skills** | [Link](https://www.kaggle.com/code/vedikagupta0/predicting-resume-job-match-score-using-skills) | Develops custom matching models for resume-job pairs with pre-calculated match scores. |
| **Freelance Jobs Market Analysis & Future Demand** | [Link](https://www.kaggle.com/code/hammadfarooq470/freelance-jobs-market-analysis-future-demand/input) | Market analysis of high-demand freelance jobs in 2025 with hourly rate ranges. |
| **Freelance Jobs Analysis (Upwork)** | [Link](https://www.kaggle.com/code/ahmedmyalo/freelance-jobs-analysis-upwork) | Comprehensive analysis described as "a compass for freelancers" and "a guide for HR companies optimizing talent search." |
| **Data Cleaning and EDA of Freelancer Dataset** | [Link](https://www.kaggle.com/code/oyekanmiolamilekan/data-cleaning-and-eda-of-freelancer-dataset) | EDA of freelance data analysis market including skills, rates, and client preferences. |

### Talent Matching & HR Automation

| Notebook | URL | Approach |
|----------|-----|----------|
| **SYRA - Revolutionize Your Hiring Process** | [Link](https://www.kaggle.com/code/ramzybakir/syra-revolutionize-your-hiring-process) | AI hiring system evaluating marketing/data analytics experience, data visualization skills. |
| **HR Agent - Resume Screening Automation** | [Link](https://www.kaggle.com/code/farhanatiq/hr-agent-resume-screening-automation) | Automated screening with weighted scoring: Skills Match (50%), Years of Experience (20%), Education Match (remaining). |
| **Smart Resume Analyser** | [Link](https://www.kaggle.com/code/harshadajaveri/smart-resume-analyser) | GenAI-powered resume parsing generating structured candidate profiles. |
| **Resume and Job Description Matching** | [Link](https://www.kaggle.com/code/gemyai/resume-and-job-description-matching) | Direct resume-to-job matching system. |
| **Skills Landscape Analysis in Job Market** | [Link](https://www.kaggle.com/code/jijagallery/skills-landscape-analysis-in-job-market) | Comprehensive analysis of relationship between skills and job positions. |
| **Job Market Analysis Using NLP** | [Link](https://www.kaggle.com/code/krishnakumaria/job-market-analysis-using-nlp) | NLP techniques to extract in-demand skills from Canadian job postings. |
| **Exploring Job Market Trends & In-Demand Skills** | [Link](https://www.kaggle.com/code/sharmagayatri/exploring-job-market-trends-in-demand-skills) | Real-world job postings via Adzuna API analyzing demand, salary, and skills. |

### Write-ups & Articles

| Title | URL | Summary |
|-------|-----|---------|
| **Building AI-Powered Talent Matching from Zero** | [Link](https://www.kaggle.com/writeups/arjunfrancis/building-ai-powered-talent-matching-from-zero-our) | Non-technical founder building an AI co-founder matching platform. Documents 7 days of research, mistakes, and honest conversations. Directly relevant to skill marketplace building. |
| **Head Hunter (Agents Intensive Capstone)** | [Link](https://www.kaggle.com/competitions/agents-intensive-capstone-project/writeups/new-writeup-1764573904913) | Agentic AI system for recruitment, onboarding, and employee growth with minimal manual effort. |

---

## 7. Data Science Approaches to Skill Matching

Based on the notebooks and datasets analyzed, these are the **dominant ML/DS approaches** used for skill marketplace problems:

### 7.1 NLP & Text Processing
- **Skill Extraction from Text**: Using NER (Named Entity Recognition) to extract skills from resumes and job descriptions
- **TF-IDF + Cosine Similarity**: Traditional approach for matching job descriptions to candidate profiles
- **Topic Modeling (LDA)**: Discovering latent skill clusters in job postings

### 7.2 Embedding-Based Matching
- **Word2Vec / FastText embeddings** for skill and job title similarity
- **Sentence-BERT / Transformer embeddings** for semantic matching of job descriptions to candidate profiles
- **Vector similarity search** for real-time job-candidate matching (as demonstrated in the Job Recommendations with Embeddings notebook)

### 7.3 LLM-Powered Matching
- **Google Gemini** for multi-candidate evaluation against job descriptions
- **GenAI for structured profile generation** from unstructured resume text
- **LLM scoring** with weighted criteria (skills 50%, experience 20%, education 30%)

### 7.4 Classification Models
- **Binary classification**: Does a candidate match a job? (Job_Match target in Vocational dataset)
- **Multi-class classification**: Which job category best fits a skill profile?
- **Gradient Boosting / Random Forest** for feature importance in skill-based employability

### 7.5 Recommendation Systems
- **Collaborative filtering**: Based on similar freelancer-job interactions
- **Content-based filtering**: Matching skill vectors to job requirement vectors
- **Hybrid systems**: Combining collaborative + content-based approaches

### 7.6 Pricing & Market Analysis
- **Regression models** for predicting freelancer rates based on skills and experience
- **Time series analysis** for demand forecasting of specific skills
- **Clustering** to identify freelancer segments and pricing tiers

---

## 8. Competition Insights

### Direct Competitions
No Kaggle competition directly targets "skill marketplace" building. However, relevant adjacent competitions include:

- **Agents Intensive Capstone Project**: Featured an HR/hiring agent write-up demonstrating agentic AI for talent acquisition
- Various **job recommendation challenges** on Kaggle (typically community-organized)

### Transferable Competition Approaches
From related NLP and recommendation system competitions:

1. **Feature Engineering**: Creating skill overlap scores, experience-weighted skill vectors, and domain similarity features
2. **Ensemble Methods**: Combining multiple matching approaches (text similarity + structured features + collaborative signals)
3. **Cross-validation strategies**: Handling the cold-start problem for new skills or new marketplace participants
4. **Evaluation Metrics**: NDCG for ranking, MAP for recommendation quality, F1 for matching accuracy

---

## 9. Potential Data Sources for Building a Skill Marketplace

### Tier 1: Directly Usable (Freelance Marketplace Data)
| Priority | Dataset | Why It's Valuable |
|----------|---------|-------------------|
| **#1** | [1.3M LinkedIn Jobs & Skills](https://www.kaggle.com/datasets/asaniczka/1-3m-linkedin-jobs-and-skills-2024) | Massive scale, real data, pre-extracted skills, powers SkillExplorer |
| **#2** | [Upwork Job Postings 2024 (50K)](https://www.kaggle.com/datasets/asaniczka/upwork-job-postings-dataset-2024-50k-records) | Real marketplace data with pricing, skills, categories |
| **#3** | [Upwork Freelance Jobs (+60K)](https://www.kaggle.com/datasets/ahmedmyalo/upwork-freelance-jobs-60k) | Large, cleaned, multi-sector freelance data |
| **#4** | [Freelancer Earnings & Job Trends](https://www.kaggle.com/datasets/shohinurpervezshohan/freelancer-earnings-and-job-trends) | Earnings + demand scores across skill categories |
| **#5** | [Freelancer.com 9K Jobs](https://www.kaggle.com/datasets/isaacoresanya/freelancer) | Skills, rates, client preferences from another major platform |

### Tier 2: Skill Matching & Taxonomy Building
| Priority | Dataset | Why It's Valuable |
|----------|---------|-------------------|
| **#6** | [All Skills (World's Largest)](https://www.kaggle.com/datasets/arbazkhan971/allskillandnonskill) | Build a comprehensive skill taxonomy from LinkedIn, GitHub, StackOverflow |
| **#7** | [Vocational Skill-Job Matching](https://www.kaggle.com/datasets/ziya07/vocational-skill-job-matching-dataset) | Pre-labeled match/no-match pairs for training matching models |
| **#8** | [Job Skill Set](https://www.kaggle.com/datasets/batuhanmutlu/job-skill-set) | Skills extracted via API from LinkedIn job postings |
| **#9** | [Industry-Education Skills Matching](https://www.kaggle.com/datasets/programmer3/industry-education-skills-matching-dataset) | 20+ skill attributes mapped to job categories |

### Tier 3: Pricing & Market Intelligence
| Priority | Dataset | Why It's Valuable |
|----------|---------|-------------------|
| **#10** | [Fiverr Gig Details](https://www.kaggle.com/datasets/aniketanilmali/fiverr-gig-details) | Multi-tier pricing (Basic/Standard/Premium), ratings, delivery data |
| **#11** | [Fiverr Freelancers Web Scraping](https://www.kaggle.com/datasets/asarli/fiverr-freelancers-web-scraping-dataset) | Pricing, ratings, seller levels, market trends |
| **#12** | [DS Freelancer Listings: Upwork](https://www.kaggle.com/datasets/kanchana1990/data-science-freelancer-listingsupwork-dataset) | Freelancer profiles with success rates, pricing strategies |

### Tier 4: Resume/Profile Processing
| Priority | Dataset | Why It's Valuable |
|----------|---------|-------------------|
| **#13** | [Resume/CV Skills Extraction](https://www.kaggle.com/datasets/muqaddasejaz/resume-cv-skills-extraction-dataset) | Train skill extraction models from resume text |
| **#14** | [AI Resume Screening (2026)](https://www.kaggle.com/datasets/aminasalamt/ai-resume-screening-and-job-market-dataset-2026) | Simulated AI screening with match scores and hiring decisions |
| **#15** | [Automating Talent](https://www.kaggle.com/datasets/willianoliveiragibin/automating-talent) | ML approaches for talent-project matching in service orgs |

---

## 10. Recommendations

### For Immediate Use
1. **Start with the 1.3M LinkedIn dataset** as your primary training source for skill extraction and job-skill mapping
2. **Use Upwork 50K/60K datasets** to understand freelance marketplace dynamics, pricing models, and skill demand
3. **Build your skills taxonomy** using the All Skills dataset (3,291+ skills from multiple platforms)

### For Model Development
1. **Train a skill matching model** using the Vocational Skill-Job Matching dataset (has labeled match/no-match pairs)
2. **Implement embedding-based matching** following the Job Recommendations with Embeddings notebook approach
3. **Build pricing prediction models** using Fiverr multi-tier pricing data and Upwork hourly rate data
4. **Use LLM-based matching** (Gemini approach) for high-quality but lower-volume matching

### For Market Intelligence
1. **Analyze skill demand trends** using the Freelancer Earnings dataset (includes demand scores)
2. **Study pricing strategies** across Upwork, Fiverr, and Freelancer.com datasets
3. **Map geographic skill distribution** using the multiple datasets with location data

### Missing Data Gaps to Fill
- **Buyer-side data**: Most datasets focus on job postings/supply; buyer satisfaction and repeat hiring data is sparse
- **Skill assessment/verification data**: No dataset covers actual skill verification or testing results
- **Marketplace transaction outcomes**: Completion rates, disputes, and long-term engagement data not available
- **Real-time pricing signals**: Static snapshots only; no streaming marketplace data

---

*Report compiled from 5 DuckDuckGo searches across Kaggle, analyzing 60+ search results and scraping 21 dataset pages for detailed metadata.*
