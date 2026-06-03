# Kaggle Findings: Skill Marketplace Related Datasets, Competitions & Notebooks

> **Research Date:** July 2025
> **Search Method:** DuckDuckGo site-scoped searches (7 queries) + Kaggle API (datasets endpoint) + web scraping attempts (3 URLs)
> **Queries Used:**
> 1. `site:kaggle.com skill marketplace`
> 2. `site:kaggle.com talent marketplace`
> 3. `site:kaggle.com freelance marketplace dataset`
> 4. `site:kaggle.com skills matching`
> 5. `site:kaggle.com gig economy dataset`
> 6. `site:kaggle.com freelancer skills`
> 7. `site:kaggle.com job skills matching dataset`
>
> **Note:** Kaggle is a JavaScript SPA protected by reCAPTCHA; direct web scraping returned no extractable content. Data was gathered from DuckDuckGo search snippets, supplemental detail searches, and the Kaggle public datasets API.

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Tier 1 - Directly Relevant: Freelance Marketplace Datasets](#tier-1---directly-relevant-freelance-marketplace-datasets)
3. [Tier 2 - Highly Relevant: Skills Matching & Task Assignment](#tier-2---highly-relevant-skills-matching--task-assignment)
4. [Tier 3 - Relevant: Job Market & Skills Demand](#tier-3---relevant-job-market--skills-demand)
5. [Tier 4 - Supporting: Skills Taxonomies & Extraction](#tier-4---supporting-skills-taxonomies--extraction)
6. [Competitions](#competitions)
7. [Notebooks & Code](#notebooks--code)
8. [Cross-Reference Matrix](#cross-reference-matrix)
9. [Recommendations](#recommendations)

---

## Executive Summary

Across 7 DuckDuckGo searches scoped to kaggle.com plus Kaggle API queries, we identified **60+ unique Kaggle resources** relevant to skill marketplaces. There is **no single "skill marketplace" dataset** on Kaggle, but there is a rich ecosystem of related datasets spanning:

- **Freelance platform data** (Upwork, Fiverr, Freelancer.com, PeoplePerHour) - actual marketplace data
- **Skills matching datasets** - for job-candidate matching algorithms
- **Skill-based task assignment** - matching skills to project tasks
- **Job market & skills demand** - understanding what skills are in demand
- **Skills taxonomies** - comprehensive skill lists for NLP/classification
- **Talent management & HR analytics** - workforce and talent pipeline data

The most valuable resources for building a skill marketplace are the freelance platform datasets (real marketplace dynamics) combined with skills matching datasets (algorithmic matching).

---

## Tier 1 - Directly Relevant: Freelance Marketplace Datasets

These datasets contain actual freelance marketplace data - the closest analogs to skill marketplace platforms.

### 1. Freelance Contracts Dataset (1.3 Million Entries)
- **URL:** https://www.kaggle.com/datasets/asaniczka/freelance-contracts-dataset-1-3-million-entries
- **Type:** Dataset
- **Description:** A robust collection of 1.3 million contracts extracted from a leading freelancing platform, offering significant insights into freelance work dynamics.
- **Key Features:**
  - Job Details: Job ID, title, start and end dates
  - Freelancer Information: Unique freelancer IDs
  - Contract metadata across the platform
- **Size:** 1.3 million entries (largest freelance dataset found)
- **Potential Use Cases:**
  - Marketplace transaction modeling
  - Freelancer behavior analysis
  - Contract duration prediction
  - Supply/demand dynamics
- **Relevance:** ★★★★★ - Largest real-world freelance marketplace dataset; ideal for understanding contract patterns, pricing, and marketplace dynamics.

---

### 2. Upwork Job Postings Dataset 2024 (50K Records)
- **URL:** https://www.kaggle.com/datasets/asaniczka/upwork-job-postings-dataset-2024-50k-records
- **Type:** Dataset
- **Description:** 50,000 job postings from Upwork spanning various categories and countries. Real-time data collected over 2 weeks.
- **Key Features:**
  - Job titles, descriptions, categories
  - Pricing information (hourly/fixed)
  - Country/location data
  - Skill requirements
- **Size:** 50,000 records
- **Downloads/Votes:** 47 upvotes
- **Potential Use Cases:**
  - Job trend analysis and pricing strategies
  - Skills demand analysis
  - Geographic distribution of freelance work
  - Category-based marketplace segmentation
- **Relevance:** ★★★★★ - Real Upwork marketplace data with pricing and skills; directly applicable to skill marketplace design.

---

### 3. All Upwork Job Postings - Monthly Tracker (200K+)
- **URL:** https://www.kaggle.com/datasets/asaniczka/all-jobs-on-upwork-200k-plus
- **Type:** Dataset
- **Description:** Extensive dataset tracking monthly job postings on Upwork. Includes job title, link, posting date, payment type, budget details, and location information.
- **Size:** 200,000+ records (updated monthly)
- **Key Features:**
  - Job title, posting link
  - Published date
  - Hourly rates and budgets
  - Country/location
  - Payment type
- **Potential Use Cases:**
  - Longitudinal marketplace trend analysis
  - Seasonal demand patterns
  - Budget/pricing optimization
  - Geographic opportunity mapping
- **Relevance:** ★★★★★ - Longitudinal tracking enables trend analysis; critical for understanding marketplace evolution.

---

### 4. Fiverr Data Gigs
- **URL:** https://www.kaggle.com/datasets/muhammadadiltalay/fiverr-data-gigs
- **Type:** Dataset
- **Description:** Data collected from the freelance marketplace Fiverr, from three sections: data processing, data engineering, and data science.
- **Key Features:**
  - Gig details and descriptions
  - Average Rating (split from combined ratings column)
  - Number of Reviewers
  - Pricing information
- **Potential Use Cases:**
  - Gig pricing strategy analysis
  - Rating/review system modeling
  - Service category taxonomy
  - Marketplace quality signals
- **Relevance:** ★★★★ - Real Fiverr marketplace data; useful for understanding gig-based skill marketplace pricing and quality signals.

---

### 5. Data Science Freelancer Listings: Upwork Dataset
- **URL:** https://www.kaggle.com/datasets/kanchana1990/data-science-freelancer-listingsupwork-dataset
- **Type:** Dataset
- **Description:** Provides a unique window into the freelance market on Upwork, showcasing a diverse array of expertise, pricing strategies, and geographic distribution.
- **Size:** 0.10 MB | Downloads: 424 | Views: 2,569 | Votes: 47
- **Key Features:**
  - Freelancer profiles and expertise
  - Pricing strategies
  - Geographic distribution
  - Skills and specializations
- **Potential Use Cases:**
  - Skill Analysis: Identify most in-demand data science skills in freelance marketplace
  - Pricing strategy benchmarking
  - Freelancer profile optimization
  - Geographic talent distribution mapping
- **Relevance:** ★★★★ - Specifically designed for skill analysis in a freelance marketplace context.

---

### 6. Freelancer Data Analysis Jobs Dataset
- **URL:** https://www.kaggle.com/datasets/isaacoresanya/freelancer
- **Type:** Dataset
- **Description:** Over 9,193 data analysis job postings scraped from Freelancer.com. Provides valuable insights including job titles, skills, rates, and client preferences.
- **Size:** 9,193 records (CSV format)
- **Key Features:**
  - Job titles and descriptions
  - Required skills
  - Rates and pricing
  - Client preferences
- **Potential Use Cases:**
  - Skill-rate correlation analysis
  - Client preference modeling
  - Job description NLP analysis
  - Market segmentation
- **Relevance:** ★★★★ - Real Freelancer.com data with skills and rates; good for understanding marketplace pricing dynamics.

---

### 7. Upwork Jobs (Devastator)
- **URL:** https://www.kaggle.com/datasets/thedevastator/upwork-jobs-a-dataset-for-researchers
- **Type:** Dataset
- **Description:** Sample of Upwork freelance jobs posted in January 2022. Includes job title, posted date, job description, employment type, skills required, client location, estimated hours per week, project duration, fixed price, experience level, job type, project type, total jobs posted by client, total spent by client, and unique ID.
- **Key Features:**
  - Job title, description, type
  - Skills required
  - Client location and spending history
  - Experience level, project duration
  - Fixed price / hourly rate
- **Potential Use Cases:**
  - Client behavior analysis
  - Skills-to-price mapping
  - Experience-level segmentation
  - Project type classification
- **Relevance:** ★★★★ - Rich feature set with both supply and demand side data.

---

### 8. Upwork Dataset of Freelancers and Agency Records
- **URL:** https://www.kaggle.com/datasets/riyaiitiansamanta/upwork-dataset-of-freelancers-and-agency-records
- **Type:** Dataset
- **Description:** Freelancer and agency records from Upwork.
- **Potential Use Cases:**
  - Individual vs. agency comparison
  - Freelancer profile analysis
  - Agency marketplace dynamics
- **Relevance:** ★★★ - Unique angle with agency data alongside individual freelancers.

---

### 9. Freelance Platform Projects (PeoplePerHour)
- **URL:** https://www.kaggle.com/datasets/prtpljdj/freeelance-platform-projects
- **Type:** Dataset
- **Description:** Projects listed by clients on PeoplePerHour. Data collection started January 20, 2023, with ~40 new projects added regularly.
- **Key Features:**
  - Project listings from clients
  - Ongoing data collection (living dataset)
  - Project descriptions and requirements
- **Potential Use Cases:**
  - Real-time project demand tracking
  - Client requirement analysis
  - Project categorization and taxonomy
- **Relevance:** ★★★ - Living dataset from another major freelance platform.

---

### 10. Freelancer Earnings & Job Trends
- **URL:** https://www.kaggle.com/datasets/shohinurpervezshohan/freelancer-earnings-and-job-trends
- **Type:** Dataset
- **Description:** Comprehensive dataset tracking freelancer earnings and job trends across multiple platforms, experience levels, and job categories. Helps understand compensation patterns and demand in the gig economy.
- **Key Features:**
  - Earnings data across platforms
  - Experience level segmentation
  - Job categories and industries
  - Skill categories
- **Potential Use Cases:**
  - Compensation benchmarking for marketplaces
  - Experience-based pricing tiers
  - Cross-platform comparison
  - Demand forecasting by skill category
- **Relevance:** ★★★★★ - Multi-platform earnings data; critical for marketplace pricing strategy.

---

### 11. Freelancer_Income Vs Skills
- **URL:** https://www.kaggle.com/datasets/shaistashahid/freelancer-income-vs-skills
- **Type:** Dataset
- **Description:** Insights into freelancer earnings and their skill sets. Includes information on freelancers' primary skills, years of experience, and income data. Useful for analyzing trends in the gig economy, understanding how skills influence income, and identifying high-demand skill sets.
- **Key Features:**
  - Primary skills
  - Years of experience
  - Income data
  - Skill-income correlations
- **Potential Use Cases:**
  - Skill valuation models
  - Income prediction by skill
  - Experience-earnings curves
  - High-demand skill identification
- **Relevance:** ★★★★★ - Directly maps skills to income; foundational for skill marketplace pricing.

---

### 12. Freelancer Work Patterns Income Prediction Dataset
- **URL:** https://www.kaggle.com/datasets/bavatharanivethamani/freelancer-work-patterns-income-prediction-dataset
- **Type:** Dataset
- **Description:** Synthetic but realistic data about freelancer demographics, skills, experience, platform usage, work patterns, and income levels.
- **Key Features:**
  - Demographics
  - Skills and experience
  - Platform usage patterns
  - Work patterns
  - Income levels
- **Potential Use Cases:**
  - Income prediction models
  - Work pattern optimization
  - Platform usage analysis
  - Freelancer segmentation
- **Relevance:** ★★★★ - Comprehensive freelancer profile data including platform usage.

---

### 13. Synthetic Freelance Job Platform Dataset
- **URL:** https://www.kaggle.com/datasets/emirhanakku/synthetic-freelance-job-platform-dataset
- **Type:** Dataset
- **Description:** Simulates a freelance job platform with 1,000 synthetic job postings. Rich textual descriptions and structured numeric data.
- **Size:** 1,000 records
- **Potential Use Cases:**
  - Prototype testing for marketplace algorithms
  - NLP model training for job matching
  - Marketplace simulation
- **Relevance:** ★★★ - Synthetic but well-structured for prototyping.

---

### 14. AI/ML Freelance Economy Dataset (2025)
- **URL:** https://www.kaggle.com/datasets/noctscraperdataset/aiml-freelance-economy-dataset-2025
- **Type:** Dataset
- **Description:** 50-row sample from 134K AI/ML freelance jobs (Apr-Nov 2025).
- **Size:** 50 rows (sample of 134K)
- **Relevance:** ★★ - Small sample but covers emerging AI/ML freelance economy.

---

### 15. Global Freelancers (Raw) Dataset
- **URL:** https://www.kaggle.com/datasets/urvishahir/global-freelancers-raw-dataset
- **Type:** Dataset
- **Description:** 1,000 fictional freelancer profiles from around the world. Includes name, gender, age, country, primary skill, years of experience, and hourly rate (with mixed formatting).
- **Size:** 1,000 profiles
- **Potential Use Cases:**
  - Data cleaning practice
  - Freelancer profile modeling
  - Global talent distribution
- **Relevance:** ★★ - Synthetic but useful for prototyping profile-based features.

---

### 16. Gig Workers Data for Performance Analysis
- **URL:** https://www.kaggle.com/datasets/jayshnavs/gig-workers-data-for-performance-analysis
- **Type:** Dataset
- **Description:** Gig workers performance analysis data.
- **Size:** 12.66 kB (gig_workers_data1.csv)
- **Potential Use Cases:**
  - Gig worker performance metrics
  - Quality measurement systems
- **Relevance:** ★★★ - Performance analytics for gig marketplace quality management.

---

### 17. Freelancer_Income_Vs_Skills-AFM
- **URL:** https://www.kaggle.com/datasets/mdferozahmedafm/freelancer-income-vs-skills-afm
- **Type:** Dataset
- **Description:** Variant of the Freelancer Income vs Skills dataset.
- **Relevance:** ★★ - Augmented version of #11.

---

## Tier 2 - Highly Relevant: Skills Matching & Task Assignment

These datasets focus on matching skills to jobs/tasks - the core algorithm behind any skill marketplace.

### 18. Skill-Based Task Assignment
- **URL:** https://www.kaggle.com/datasets/umerfarooq09/skill-based-task-assignment
- **Type:** Dataset
- **Description:** Comprehensive collection of project management tasks, designed for AI-driven task assignment and skill matching.
- **Key Features:**
  - Skills required for each task
  - Example employee profiles with skill levels
  - Structured format for ML integration
- **Notebooks:** 4 associated notebooks (including "Task Categorization: 99.94% Accuracy")
- **Potential Use Cases:**
  - AI-driven task-skill matching algorithms
  - Skill level assessment
  - Task categorization
  - Marketplace matching engine development
- **Relevance:** ★★★★★ - Most directly applicable to skill marketplace matching engines.

---

### 19. Extended Skill-Based Task Assignment Dataset
- **URL:** https://www.kaggle.com/datasets/eustaceameliat/extended-skill-task-assignment
- **Type:** Dataset
- **Description:** Extension of the Kaggle skill-based task assignment dataset by Eustace Meliat.
- **Size:** 45,776 records
- **Key Columns:**
  - Category: Top-level task categorization
  - Skill: The user's skill
  - Additional extended features
- **Potential Use Cases:**
  - Large-scale skill-task matching
  - Category-based task routing
  - Skill taxonomy development
- **Relevance:** ★★★★★ - Larger version of skill-task assignment; ideal for training matching algorithms.

---

### 20. Vocational Skill-Job Matching Dataset
- **URL:** https://www.kaggle.com/datasets/ziya07/vocational-skill-job-matching-dataset
- **Type:** Dataset
- **Description:** Comprehensive view of student profiles, skill attributes, certifications, academic performance, and corresponding job requirements.
- **Size:** 2,809 rows (each row = student-job pair)
- **Key Features:**
  - Student Profile Data: Age, gender, vocational program, academic performance
  - Skill attributes and certifications
  - Job requirements
- **Potential Use Cases:**
  - Skill-job matching algorithm development
  - Certification impact on matching
  - Profile-based recommendation systems
- **Relevance:** ★★★★ - Structured for skill-to-job matching; directly applicable.

---

### 21. Industry-Education Skills Matching Dataset
- **URL:** https://www.kaggle.com/datasets/programmer3/industry-education-skills-matching-dataset
- **Type:** Dataset
- **Description:** Dynamic Skills & Course Alignment Data. Matches industry skill requirements with educational offerings.
- **Potential Use Cases:**
  - Skills gap analysis
  - Training/upskilling recommendations
  - Curriculum-to-marketplace alignment
- **Relevance:** ★★★ - Useful for marketplace upskilling features.

---

### 22. Recruitment Dataset
- **URL:** https://www.kaggle.com/datasets/surendra365/recruitement-dataset
- **Type:** Dataset
- **Description:** Contains applicant details, resumes, job descriptions, and matching labels to assess candidate-job fit.
- **Potential Use Cases:**
  - Candidate-job fit scoring
  - Resume screening automation
  - Matching label training data
- **Relevance:** ★★★ - Contains explicit matching labels; valuable for training matching models.

---

### 23. AI-Powered Job Recommendations
- **URL:** https://www.kaggle.com/datasets/samayashar/ai-powered-job-recommendations
- **Type:** Dataset
- **Size:** 50,000 records
- **Description:** Job postings spanning multiple industries, locations, experience levels, and salary brackets.
- **Potential Use Cases:**
  - Job recommendation engine training
  - Multi-factor matching
- **Relevance:** ★★★ - Large dataset for recommendation systems.

---

### 24. Human Resource Allocation Dataset
- **URL:** https://www.kaggle.com/datasets/zara2099/human-resource-allocation-dataset
- **Type:** Dataset
- **Size:** 5,000 records, 23 columns
- **Description:** Enterprise human resource allocation and workforce management data.
- **Potential Use Cases:**
  - Resource allocation optimization
  - Skill-based team composition
- **Relevance:** ★★★ - Skill-based resource allocation; applicable to project staffing.

---

### 25. Talent Management Dataset
- **URL:** https://www.kaggle.com/datasets/ashutoshsingh1093/talent-management-dataset
- **Type:** Dataset
- **Size:** Downloads: 280 | Views: 1,682
- **Description:** Talent management focused dataset.
- **Relevance:** ★★ - General talent management data.

---

### 26. Leadership and Talent Management in HR
- **URL:** https://www.kaggle.com/datasets/razasiddique/leadership-and-talent-management-in-hr
- **Type:** Dataset
- **Size:** Downloads: 54 | Views: 303
- **Relevance:** ★★ - HR talent management perspective.

---

## Tier 3 - Relevant: Job Market & Skills Demand

### 27. 1.3M LinkedIn Jobs & Skills (2024)
- **URL:** https://www.kaggle.com/datasets/asaniczka/1-3m-linkedin-jobs-and-skills-2024
- **Type:** Dataset
- **Description:** 1.3 million job listings scraped from LinkedIn in 2024. Augmented with job skills data.
- **Size:** 1.3 million records
- **Votes:** 278 upvotes (highly popular)
- **Key Features:**
  - Job postings with full details
  - Skills data augmented per job
  - Multiple CSV files (linkedin_job_postings.csv + more)
- **Potential Use Cases:**
  - Skills demand analysis at scale
  - Salary-skill correlation
  - Marketplace category/taxonomy design
- **Relevance:** ★★★★★ - Massive skills-augmented dataset; essential for understanding skills demand.

---

### 28. LinkedIn Job Postings (2023-2024)
- **URL:** https://www.kaggle.com/datasets/arshkon/linkedin-job-postings
- **Type:** Dataset
- **Size:** 124,000+ records
- **Description:** Nearly comprehensive record of job postings from LinkedIn.
- **Relevance:** ★★★ - Large LinkedIn dataset for talent marketplace demand analysis.

---

### 29. Job Market & Skills Demand Dataset
- **URL:** https://www.kaggle.com/datasets/muqaddasejaz/job-market-and-skills-demand-dataset
- **Type:** Dataset
- **Size:** 10,000 records
- **Description:** Synthetically generated job postings reflecting 2025 skills demand trends. Focus on AI, Blockchain, Green Technology, Quantum Computing.
- **Relevance:** ★★★ - Forward-looking skills demand; useful for marketplace planning.

---

### 30. job_market_skills_dataset
- **URL:** https://www.kaggle.com/datasets/sharmagayatri/job-market-skills-dataset
- **Type:** Dataset
- **Description:** Real job postings collected via the Adzuna Job Search API. Skills, contract types, locations, posting trends, salary info.
- **Relevance:** ★★★ - Real API-sourced data for validating skills demand.

---

### 31. AI & Data Science Job Market Dataset (2020-2026)
- **URL:** https://www.kaggle.com/datasets/shree0910/ai-and-data-science-job-market-dataset-20202026
- **Type:** Dataset
- **Description:** AI/DS job market trends with skills and salary data. Job roles, company characteristics, technical skills, education, experience, salary ranges.
- **Relevance:** ★★★ - Comprehensive tech job market data.

---

### 32. Data Science Job Postings & Skills (2024)
- **URL:** https://www.kaggle.com/datasets/asaniczka/data-science-job-postings-and-skills
- **Type:** Dataset
- **Description:** Raw dump of data science job postings from LinkedIn with skill requirements.
- **Relevance:** ★★ - Niche but useful for DS marketplace verticals.

---

### 33. AI Job Replacement & Skill Shift Dataset
- **URL:** https://www.kaggle.com/datasets/dmahajanbe23/ai-job-replacement-and-skill-shift-dataset
- **Type:** Dataset
- **Description:** Simulation (2020-2026) of global workforce transformation driven by AI. Job role evolution, skill shifts, wage adjustments.
- **Relevance:** ★★★ - Strategic insights for marketplace evolution.

---

### 34. Global AI Job Market & Salary Trends 2025
- **URL:** https://www.kaggle.com/datasets/bismasajjad/global-ai-job-market-and-salary-trends-2025
- **Type:** Dataset
- **Description:** AI/ML positions, salaries, and market trends across countries.
- **Relevance:** ★★ - Global perspective for international marketplace pricing.

---

### 35. Job Market Dataset (Global)
- **URL:** https://www.kaggle.com/datasets/kundanbedmutha/job-market-dataset-global
- **Type:** Dataset
- **Size:** 500,000 records
- **Description:** High-quality synthetic dataset reflecting realistic global job market patterns.
- **Relevance:** ★★ - Large synthetic dataset for testing algorithms at scale.

---

### 36. Job Postings Dataset
- **URL:** https://www.kaggle.com/datasets/moyukhbiswas/job-postings-dataset
- **Type:** Dataset
- **Description:** Extensive job postings for job market patterns, NLP, and ML. Potential: workforce planning, talent acquisition, NLP resume parsing, salary prediction, regional job market analysis.
- **Relevance:** ★★★ - Good for marketplace demand-side modeling.

---

### 37. AI Job Market Global 2026
- **URL:** https://www.kaggle.com/datasets/atharvasoundankar/ai-job-market-global-2026
- **Type:** Dataset
- **Description:** 5,773 live job postings from verified public APIs across 5 countries and 9 AI/ML categories. Updated weekly.
- **Relevance:** ★★ - Niche AI market but regularly updated.

---

### 38. Jobinja Job Listings 26K
- **URL:** https://www.kaggle.com/datasets/maminkheneifar/jobinja-job-listings-26k
- **Type:** Dataset
- **Size:** 10.21 MB | Downloads: 208 | Views: 1,346
- **Description:** 26,000 job listings from Jobinja.
- **Relevance:** ★★ - Regional job marketplace data.

---

## Tier 4 - Supporting: Skills Taxonomies & Extraction

### 39. List of All Skills (World's Largest)
- **URL:** https://www.kaggle.com/datasets/arbazkhan971/allskillandnonskill
- **Type:** Dataset
- **Description:** All skills from LinkedIn, GitHub, StackOverflow and job descriptions across Naukri, Indeed, Monster.com. Claims "World's Largest Collection of Dataset for skills."
- **Potential Use Cases:**
  - Skills taxonomy for marketplace categories
  - Skill extraction NLP training
  - Skill normalization/deduplication
  - Marketplace search and filter design
- **Relevance:** ★★★★★ - Essential for building a marketplace skills taxonomy.

---

### 40. job-skill-set
- **URL:** https://www.kaggle.com/datasets/batuhanmutlu/job-skill-set
- **Type:** Dataset
- **Description:** Designed for ML projects: job matching, skill extraction, NLP tasks.
- **Relevance:** ★★★ - Training data for skill extraction.

---

### 41. Related Job Skills
- **URL:** https://www.kaggle.com/datasets/ulrikthygepedersen/related-job-skills
- **Type:** Dataset
- **Description:** Correlation between different job skills: technical, soft, and industry-specific.
- **Potential Use Cases:**
  - Skills relationship graph
  - "Similar skills" recommendations
  - Skill adjacency for marketplace search
  - Skill cluster identification
- **Relevance:** ★★★★★ - Skill correlation data essential for marketplace "related skills" features.

---

### 42. Skills (3,291 Skills Dataset)
- **URL:** https://www.kaggle.com/datasets/zamamahmed211/skills
- **Type:** Dataset
- **Size:** 3,291 skills
- **Description:** Curated collection of skill-related data spanning diverse domains.
- **Relevance:** ★★★ - Curated taxonomy; starting point for marketplace categories.

---

### 43. IT Job Roles Skills Dataset
- **URL:** https://www.kaggle.com/datasets/dhivyadharunaba/it-job-roles-skills-dataset
- **Type:** Dataset
- **Size:** 493 IT job roles
- **Description:** IT roles with descriptions, required skills, and certifications.
- **Relevance:** ★★★ - Well-structured IT role-skill mapping.

---

### 44. Employment Skills
- **URL:** https://www.kaggle.com/datasets/maneeshdisodia/employment-skills
- **Type:** Dataset
- **Description:** Skills lookup identifying various skills related to job type and associated values.
- **Relevance:** ★★ - Skills lookup table for reference data.

---

### 45. Google Job Skills
- **URL:** https://www.kaggle.com/datasets/niyamatalmass/google-job-skills
- **Type:** Dataset
- **Description:** Skills needed to get a job at Google.
- **Relevance:** ★★ - Premium skill requirements benchmark.

---

### 46. Resume / CV Skills Extraction Dataset
- **URL:** https://www.kaggle.com/datasets/muqaddasejaz/resume-cv-skills-extraction-dataset
- **Type:** Dataset
- **Size:** 962 rows, 2 columns
- **Description:** Resumes mapped to job categories for skills extraction.
- **Relevance:** ★★★ - Training data for marketplace profile auto-fill from resumes.

---

### 47. Jobs and Skills Mapping for Career Analysis
- **URL:** https://www.kaggle.com/datasets/emaadakhter/jobs-and-skills-mapping-for-career-analysis
- **Type:** Dataset
- **Size:** ~41 KB, 166 downloads
- **Description:** Job Titles, Descriptions, Key Skills, Industry Categories, Pay Grades. "Structured Job Market Data for AI, NLP, and Career Recommendation Systems."
- **Relevance:** ★★★ - Clean structured job-skill mapping for taxonomy and pricing.

---

### 48. Skill & Career Recommendation Dataset
- **URL:** https://www.kaggle.com/datasets/tea340yashjoshi/skill-and-career-recommendation-dataset
- **Type:** Dataset
- **Key Columns:** Sr.No., Course, plus skill/career fields
- **Relevance:** ★★ - Career recommendation; applicable to user guidance.

---

### 49. AI-based Career Recommendation System
- **URL:** https://www.kaggle.com/datasets/adilshamim8/ai-based-career-recommendation-system
- **Type:** Dataset
- **Description:** Skills, interests, and career paths.
- **Relevance:** ★★ - Career pathing features.

---

### 50. candidate_job_role_dataset
- **URL:** https://www.kaggle.com/datasets/ckshetty/candidate-job-role-dataset
- **Type:** Dataset
- **Description:** Resume-extracted data for job role classification.
- **Relevance:** ★★ - Resume-to-role classification for profile processing.

---

### 51. AI Resume Screening & Job Market Dataset (2026)
- **URL:** https://www.kaggle.com/datasets/aminasalamt/ai-resume-screening-and-job-market-dataset-2026
- **Type:** Dataset
- **Description:** Synthetic AI recruitment data with skill match scores, salary expectations, screening decisions.
- **Relevance:** ★★★ - Contains skill match scores for training matching algorithms.

---

### 52. Employee Upskilling and Hiring Success Dataset
- **URL:** https://www.kaggle.com/datasets/sumittr26/employee-upskilling-and-hiring-success-dataset
- **Type:** Dataset
- **Description:** Impact of education, experience, and AI upskilling on hiring success.
- **Relevance:** ★★ - Upskilling focus for marketplace learning features.

---

### 53. Automating Talent
- **URL:** https://www.kaggle.com/datasets/willianoliveiragibin/automating-talent
- **Type:** Dataset
- **Description:** Addresses resume screening at scale for labor-intensive businesses.
- **Relevance:** ★★ - Talent automation for supply-side management.

---

### 54. Resume Dataset (Neuralframe AI)
- **URL:** https://www.kaggle.com/datasets/saugataroyarghya/resume-dataset
- **Type:** Dataset
- **Description:** Comprehensive resource for resume parsing, candidate profiling, and job matching. Includes career objectives, skills, education, experience, certifications.
- **Relevance:** ★★★ - Resume parsing for marketplace profile creation.

---

### 55. Resume Screening Dataset for NLP and ML
- **URL:** https://www.kaggle.com/datasets/arunsaini0906/resume-screening-dataset-for-nlp-and-ml
- **Type:** Dataset
- **Description:** For resume screening/shortlisting, classification by role, skill extraction, candidate-job matching, NER on resume data, ranking models.
- **Relevance:** ★★★ - Comprehensive resume processing training data.

---

### 56. HR Analytics Case Study
- **URL:** https://www.kaggle.com/datasets/vjchoudhary7/hr-analytics-case-study
- **Type:** Dataset
- **Size:** Downloads: 31,433 | Views: 208,528 | Votes: 343
- **Description:** Major HR analytics dataset, highly popular.
- **Relevance:** ★★ - General HR analytics; applicable to marketplace workforce insights.

---

### 57. Career Recommender Dataset
- **URL:** https://www.kaggle.com/datasets/siddardhashayini3/career-recommender-dataset
- **Type:** Dataset
- **Description:** Professions, required skills, educational backgrounds, industry trends.
- **Relevance:** ★★ - Career recommendations for marketplace guidance.

---

### 58. Job Dataset (Roles, Skills, Salaries)
- **URL:** https://www.kaggle.com/datasets/prit198/job-dataset
- **Type:** Dataset
- **Description:** Job roles, skills, salaries, and locations for employment trends.
- **Relevance:** ★★ - Basic job-skill-salary mapping.

---

## Competitions

### 59. Mercor Cheating Detection ★★★★★
- **URL:** https://www.kaggle.com/competitions/mercor-cheating-detection
- **Type:** Competition (with prizes)
- **Description:** Predict whether a candidate in an **online talent marketplace** (Mercor) is engaging in cheating behavior during an interview, using behavioral signals and social graph structure.
- **Key Features:**
  - Behavioral signals during interviews
  - Social graph structure
  - Binary cheating prediction
- **Potential Use Cases:**
  - Marketplace trust and safety systems
  - Interview fraud detection
  - Platform integrity
- **Relevance:** ★★★★★ - **The ONLY Kaggle competition directly from a talent marketplace (Mercor)**. Essential for marketplace trust systems.

---

### 60. Skills Detection from Text
- **URL:** https://www.kaggle.com/competitions/detect-skills-from-text
- **Type:** Competition
- **Description:** Improve education system by detecting skills from texts about specific industries.
- **Potential Use Cases:**
  - Automatic skill extraction from profiles/descriptions
  - NLP-based skill tagging
  - Education-industry alignment
- **Relevance:** ★★★★ - Skill detection is core marketplace functionality.

---

### 61. Predict Potential Spammers on Fiverr
- **URL:** https://www.kaggle.com/competitions/predict-potential-spammers-on-fiverr
- **Type:** Competition
- **Description:** Predict which new Fiverr users will become spammers based on initial actions.
- **Potential Use Cases:**
  - Marketplace anti-spam systems
  - New user risk scoring
  - Platform quality
- **Relevance:** ★★★★ - Marketplace trust & safety from a major freelance platform.

---

## Notebooks & Code

### 62. Skills Matching with Gemini
- **URL:** https://www.kaggle.com/code/poxman100/skills-matching-with-gemini
- **Description:** Gemini Pro evaluates 3 resumes against a job description for best candidate match. Uses LLM for skills-based matching.
- **Relevance:** ★★★★★ - AI-based skills matching; directly applicable to marketplace matching engines.

### 63. Skill Match - AI Resume Analyzer
- **URL:** https://www.kaggle.com/code/akhileshyadav1/skill-match-ai-resume-analyzer
- **Description:** Compares parsed resumes with job descriptions. Calculates match percentage, identifies skill gaps, provides market insights.
- **Relevance:** ★★★★★ - Complete skill matching pipeline with gap analysis.

### 64. Freelancer Earnings Analysis and Prediction
- **URL:** https://www.kaggle.com/code/muhammedaliyilmazz/freelancer-earnings-analysis-and-prediction
- **Description:** Analysis and prediction of freelancer earnings across industries and skill categories.
- **Relevance:** ★★★★ - Earnings prediction for marketplace pricing.

### 65. Freelance Trends: Budget, Demand & Success Drivers
- **URL:** https://www.kaggle.com/code/hammadrehmani/freelance-trends-budget-demand-success-drivers
- **Description:** EDA of Synthetic Freelance Jobs dataset examining gig economy factors.
- **Relevance:** ★★★ - Budget/demand analysis for marketplace design.

### 66. Freelance Jobs Analysis (Upwork)
- **URL:** https://www.kaggle.com/code/ahmedmyalo/freelance-jobs-analysis-upwork
- **Description:** Upwork as gig economy ecosystem. Prime job hunting times, key freelancer skills, actionable insights for HR companies.
- **Relevance:** ★★★★ - Marketplace dynamics with actionable insights.

### 67. Freelancer Income and Skills Analysis
- **URL:** https://www.kaggle.com/code/devraai/freelancer-income-and-skills-analysis
- **Description:** Using Freelancer_Income Vs Skills dataset.
- **Relevance:** ★★★ - Skill-income relationship analysis.

### 68. Fiverr Gigs Strategic Pricing
- **URL:** https://www.kaggle.com/code/sangsan/fiverr-gigs-strategic-pricing
- **Description:** Pricing tier analysis for Fiverr subcategories in data analytics.
- **Relevance:** ★★★★ - Marketplace pricing strategy; directly applicable.

### 69. Freelance Jobs Market Analysis & Future Demand
- **URL:** https://www.kaggle.com/code/hammadfarooq470/freelance-jobs-market-analysis-future-demand
- **Description:** Dataset with high-demand freelance jobs 2025, hourly rates, future demand projections.
- **Relevance:** ★★★ - Forward-looking freelance market data.

### 70. Exploring Job Market Trends & In-Demand Skills
- **URL:** https://www.kaggle.com/code/sharmagayatri/exploring-job-market-trends-in-demand-skills
- **Description:** Real-world Adzuna API analysis of demand, salary transparency, in-demand skills.
- **Relevance:** ★★★ - Market trends for skills demand.

### 71. Global Talent Migration Case Study
- **URL:** https://www.kaggle.com/code/arshaprasad/global-talent-migration-case-study
- **Description:** Skill Migration data from Middle East & North Africa.
- **Relevance:** ★★ - Talent migration for global marketplace planning.

### 72. Talent Analytics
- **URL:** https://www.kaggle.com/code/robin26091991/talent-analytics
- **Description:** ML code using HR Analytics Case Study data.
- **Relevance:** ★★ - HR analytics methodologies.

### 73. Analyzing Skills Required for Google
- **URL:** https://www.kaggle.com/code/aryandec25/analyzing-skills-required-for-google
- **Description:** Skills analysis for Google positions.
- **Relevance:** ★★ - Skills analysis methodology.

### 74. 1.3M LinkedIn Jobs and Skills Dataset (2024) Analysis
- **URL:** https://www.kaggle.com/code/mahmoudredagamail/1-3m-linkedin-jobs-and-skills-dataset-2024
- **Description:** Analysis notebook for the 1.3M LinkedIn dataset.
- **Relevance:** ★★★ - Analysis methodology for large skills dataset.

---

## Cross-Reference Matrix

| Use Case | Best Datasets | Competitions | Notebooks |
|----------|--------------|-------------|-----------|
| **Marketplace pricing** | #1, #2, #3, #4, #5, #10, #11 | - | #64, #65, #68 |
| **Skills matching/recommendation** | #18, #19, #20, #21, #23 | #60 | #62, #63 |
| **Trust & safety** | - | #59, #61 | - |
| **Skills taxonomy** | #39, #40, #41, #42, #43 | #60 | - |
| **Demand forecasting** | #27, #29, #30, #33, #36 | - | #65, #69, #70 |
| **User profiling** | #12, #15, #46, #50, #54 | - | #67 |
| **Platform dynamics** | #1, #2, #3, #9, #10 | - | #66 |
| **Income prediction** | #10, #11, #12 | - | #64, #67 |
| **Resume/skill extraction** | #46, #54, #55 | #60 | #63 |
| **Talent management** | #25, #26, #53, #56 | #59 | #72 |

---

## Recommendations

### Top 10 Datasets to Download First

| Priority | Dataset | Why |
|----------|---------|-----|
| 1 | **Freelance Contracts Dataset (1.3M)** (#1) | Largest real marketplace transaction data |
| 2 | **1.3M LinkedIn Jobs & Skills (2024)** (#27) | Massive skills-augmented job data |
| 3 | **Extended Skill-Based Task Assignment (45K)** (#19) | Best skill-task matching training data |
| 4 | **Upwork Job Postings 2024 (50K)** (#2) | Real marketplace with pricing & skills |
| 5 | **Freelancer_Income Vs Skills** (#11) | Direct skill-to-income mapping |
| 6 | **Related Job Skills** (#41) | Skill correlation graph data |
| 7 | **List of All Skills** (#39) | Comprehensive skills taxonomy |
| 8 | **Freelancer Earnings & Job Trends** (#10) | Multi-platform earnings benchmarks |
| 9 | **Skill-Based Task Assignment** (#18) | Core matching dataset with 4 notebooks |
| 10 | **Upwork Freelancer Listings** (#5) | Skill analysis in marketplace context |

### Key Competition to Study

- **Mercor Cheating Detection** (#59) - The ONLY Kaggle competition from an actual talent marketplace; invaluable data on marketplace trust and safety.

### Key Notebooks to Study

- **Skills Matching with Gemini** (#62) - LLM-based skills matching approach
- **Skill Match - AI Resume Analyzer** (#63) - Complete matching pipeline with gap analysis
- **Fiverr Gigs Strategic Pricing** (#68) - Marketplace pricing strategy analysis

### Gaps Identified

1. **No complete skill marketplace dataset** - No dataset models a complete marketplace with buyers, sellers, skills, pricing, and transactions together.
2. **Limited review/rating data** - Most datasets lack quality signals (reviews, ratings, completion rates).
3. **No matching outcome data** - Few datasets track whether a skill match resulted in a successful engagement.
4. **Sparse real-time data** - Most datasets are snapshots rather than longitudinal.
5. **No multi-sided marketplace data** - Missing the buyer/client side of marketplace interactions.
6. **No pricing negotiation data** - No datasets capture offer/counter-offer dynamics.

### Suggested Composite Dataset Strategy

To build a comprehensive skill marketplace model, combine:

| Layer | Sources |
|-------|---------|
| **Supply side** (freelancer profiles) | #5, #11, #12, #15 |
| **Demand side** (job postings) | #2, #3, #27, #30 |
| **Skills taxonomy** | #39, #41, #42 |
| **Matching algorithms** | #18, #19, #20 |
| **Pricing models** | #10, #11, #4, #6 |
| **Trust & safety** | Mercor competition (#59), Fiverr spammers (#61) |
| **Resume processing** | #46, #54, #55 |

### Kaggle API Access Note

Some resources require Kaggle API authentication to access:
- **Competitions data** (Mercor, Skills Detection, Fiverr Spammers)
- **Notebook source code and outputs**
- **Full dataset metadata**

To set up: Create an API token at https://www.kaggle.com/settings and set `KAGGLE_USERNAME` and `KAGGLE_KEY` environment variables.

---

## Appendix: Search Results Summary

| Search Query | Results Found | Unique Kaggle Resources |
|-------------|--------------|------------------------|
| `site:kaggle.com skill marketplace` | 18 | 15 datasets, 1 notebook |
| `site:kaggle.com talent marketplace` | 10 | 7 datasets, 1 competition |
| `site:kaggle.com freelance marketplace dataset` | 10 | 9 datasets |
| `site:kaggle.com skills matching` | 10 | 8 datasets, 1 notebook, 1 competition |
| `site:kaggle.com gig economy dataset` | 16 | 6 datasets, 3 notebooks |
| `site:kaggle.com freelancer skills` | 20 | 11 datasets, 3 notebooks |
| `site:kaggle.com job skills matching dataset` | 14 | 12 datasets |
| Kaggle API: "skill marketplace" | 9 | 1 relevant dataset |
| Kaggle API: "talent marketplace" | 2 | 1 relevant dataset |
| Kaggle API: "marketplace" (broad) | 20 | 3 relevant datasets |
| **Total unique resources** | | **~74 (after deduplication)** |

---

*This document was compiled from 7 DuckDuckGo site-scoped searches, 5 supplemental detail searches, and Kaggle API queries, covering 74 unique Kaggle resources across datasets, competitions, and notebooks.*
