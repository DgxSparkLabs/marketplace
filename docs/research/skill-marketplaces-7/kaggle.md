# Kaggle Datasets, Competitions & Notebooks for Skill Marketplaces

> Research compiled July 2025 via DuckDuckGo site-searches on kaggle.com
> Focus areas: trust/reputation systems, pricing optimization, quality scoring, demand forecasting

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Freelancer & Skill Marketplace Datasets](#1-freelancer--skill-marketplace-datasets)
3. [Trust, Reputation & Fraud Detection](#2-trust-reputation--fraud-detection)
4. [Pricing Optimization & Dynamic Pricing](#3-pricing-optimization--dynamic-pricing)
5. [Skill Demand Forecasting & Job Trends](#4-skill-demand-forecasting--job-trends)
6. [Quality Scoring & Benchmarking](#5-quality-scoring--benchmarking)
7. [Skill Matching & Recommendation Systems](#6-skill-matching--recommendation-systems)
8. [Applicable ML Techniques](#7-applicable-ml-techniques)
9. [Recommended Priority Datasets](#8-recommended-priority-datasets)

---

## Executive Summary

This research identifies **30+ Kaggle datasets, competitions, and notebooks** directly relevant to building ML-powered skill marketplace systems. The findings are organized around four core marketplace capabilities: trust/reputation, pricing optimization, quality scoring, and demand forecasting. While no single Kaggle dataset perfectly mirrors a skill marketplace, several can be combined or adapted to train and benchmark marketplace ML models.

**Key finding:** The freelancer marketplace space now has dedicated Kaggle datasets (Upwork, Fiverr, Freelancer.com data) with real platform features like ratings, hourly rates, skills, client satisfaction, and job completion metrics. Combined with fraud detection and dynamic pricing datasets, these provide a strong foundation for ML experimentation.

---

## 1. Freelancer & Skill Marketplace Datasets

### 1.1 Freelancer Earnings & Job Trends
- **URL:** https://www.kaggle.com/datasets/shohinurpervezshohan/freelancer-earnings-and-job-trends
- **Description:** Comprehensive dataset tracking freelancer earnings and job trends across multiple platforms (Fiverr, Upwork, Toptal, Freelancer, PeoplePerHour), experience levels, and job categories.
- **Key Features:** Platform, Experience_Level, Job_Category, Hourly_Rate, Client_Satisfaction, Job_Completion metrics
- **Relevance:** **HIGH** - Directly models marketplace dynamics, pricing patterns, and quality signals across competing platforms
- **ML Applications:** Earnings prediction, platform comparison, client satisfaction modeling, skill-to-earnings mapping
- **Associated Notebooks:**
  - [Freelancer Earnings Analysis and Prediction](https://www.kaggle.com/code/muhammedaliyilmazz/freelancer-earnings-analysis-and-prediction)
  - [Freelancer Earnings Job Trends Analysis](https://www.kaggle.com/code/devraai/freelancer-earnings-job-trends-analysis)
  - [Freelancer Earning & Job Trends Analysis](https://www.kaggle.com/code/sarthakmishra12/freelancer-earning-job-trends-analysis)

### 1.2 Upwork Job Postings Dataset 2024 (50K Records)
- **URL:** https://www.kaggle.com/datasets/asaniczka/upwork-job-postings-dataset-2024-50k-records
- **Description:** Real-time data collected over 2 weeks from Upwork, the largest freelance marketplace.
- **Key Features:** Job title, skills required, budget, experience level, client history, job type
- **Relevance:** **HIGH** - Real marketplace data with skill requirements and pricing signals
- **Associated Notebook:** [upwork_job_posting_dataset_analysis](https://www.kaggle.com/code/srilalithagarapati/upwork-job-posting-dataset-analysis)

### 1.3 All Upwork Job Postings - Monthly Tracker (200K+)
- **URL:** https://www.kaggle.com/datasets/asaniczka/all-jobs-on-upwork-200k-plus
- **Description:** Monthly tracker of Upwork job postings (200K+ records, from Feb 2024). Tracks job trends, salary ranges, and demand for various skills.
- **Relevance:** **HIGH** - Longitudinal marketplace data ideal for trend analysis and demand forecasting

### 1.4 Upwork Jobs (June 2025)
- **URL:** https://www.kaggle.com/datasets/hashiromer/upwork-jobs
- **Description:** Recent (June 2025) random sample of job listings on Upwork.com with preprocessing. Raw data also available.
- **Relevance:** **HIGH** - Most recent Upwork data available, good for current market analysis

### 1.5 Upwork Dataset of Freelancers and Agency Records
- **URL:** https://www.kaggle.com/datasets/riyaiitiansamanta/upwork-dataset-of-freelancers-and-agency-records
- **Description:** Supply-side marketplace data with freelancer profiles and agency records.
- **Relevance:** **HIGH** - Captures the provider/supply side of marketplace dynamics

### 1.6 Upwork Data Job Posting (12+ months)
- **URL:** https://www.kaggle.com/datasets/llathrop/upwork-data-job-posting
- **Description:** Upwork job postings over a 12-month period, enabling time-series analysis of marketplace dynamics.
- **Relevance:** **MEDIUM-HIGH** - Longer time horizon for seasonal and trend analysis

### 1.7 Global Freelancers (Raw) Dataset
- **URL:** https://www.kaggle.com/datasets/urvishahir/global-freelancers-raw-dataset
- **Published:** July 5, 2025
- **Description:** 1,000 fictional freelancer profiles with realistic variability including names, skills, ratings, hourly rates. Designed to reflect real-world data messiness.
- **Relevance:** **MEDIUM** - Good for testing data cleaning pipelines and rating analysis
- **Associated Notebook:** [Key Factors in Global Freelancer Ratings](https://www.kaggle.com/code/btsarmy17/key-factors-in-global-freelancer-ratings)

### 1.8 Freelancer Data Analysis Jobs Dataset
- **URL:** https://www.kaggle.com/datasets/isaacoresanya/freelancer
- **Description:** 9,193 data analysis job postings scraped from Freelancer.com with job titles, skills, rates, and client preferences.
- **Relevance:** **MEDIUM** - Narrower scope (data analysis only) but detailed feature set

### 1.9 Brazilian E-Commerce Public Dataset by Olist
- **URL:** https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
- **Description:** 100,000 orders with product, customer, and review information from a real Brazilian marketplace.
- **Relevance:** **MEDIUM** - General marketplace with review/reputation data, transferable patterns for trust systems

---

## 2. Trust, Reputation & Fraud Detection

### 2.1 Deceptive Patterns Dataset
- **URL:** https://www.kaggle.com/datasets/akashnath29/deceiptive-patterns
- **Description:** Dataset for detecting fake reviews and ratings. Designed for fraud detection, AI-driven browser extensions to warn users about suspicious reviews, e-commerce trust and safety monitoring.
- **Relevance:** **VERY HIGH** - Directly applicable to marketplace trust systems, fake review detection
- **ML Applications:**
  - Fake review classification
  - Suspicious rating pattern detection
  - Trust score computation
  - Manipulative behavior identification

### 2.2 Fraud Detection Transactions Dataset (Jan 2026)
- **URL:** https://www.kaggle.com/datasets/barkataliarbab/fraud-detection-transactions
- **Published:** January 8, 2026 (most recent)
- **Description:** High-quality synthetic transaction records for fraud detection. Suitable for XGBoost, Random Forest, and Logistic Regression models.
- **Relevance:** **HIGH** - Latest fraud detection benchmark, applicable to marketplace payment fraud

### 2.3 IEEE-CIS Fraud Detection Competition
- **URL:** https://www.kaggle.com/competitions/ieee-fraud-detection
- **Description:** Major Kaggle competition for transaction fraud detection (Jul 2019). Rich feature engineering benchmark.
- **Relevance:** **HIGH** - Gold-standard competition with extensive community solutions and notebooks
- **Associated Notebook:** [Fraud Detection with Machine Learning](https://www.kaggle.com/code/enesztrk/fraud-detection-with-machine-learning)

### 2.4 E-Commerce Fraud Detection Dataset (Nov 2025)
- **URL:** https://www.kaggle.com/datasets/umuttuygurr/e-commerce-fraud-detection-dataset
- **Published:** November 3, 2025
- **Description:** Synthetic dataset recreating realistic fraud behavior across countries, channels, and user profiles. Allows building and comparing fraud-detection models.
- **Relevance:** **HIGH** - Recent, diverse fraud patterns applicable to marketplace contexts

### 2.5 Fraudulent E-Commerce Transactions
- **URL:** https://www.kaggle.com/datasets/shriyashjagtap/fraudulent-e-commerce-transactions
- **Description:** For developing/testing ML models for fraud detection in e-commerce. Useful for feature engineering and benchmarking fraud detection algorithms.
- **Relevance:** **MEDIUM-HIGH** - E-commerce fraud patterns transferable to service marketplaces

### 2.6 Credit Card Fraud Detection
- **URL:** https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud
- **Description:** Classic anonymized credit card transactions labeled as fraudulent or genuine.
- **Relevance:** **MEDIUM** - Foundational fraud detection dataset, good for baseline models

### 2.7 Synthetic Financial Datasets for Fraud Detection (PaySim)
- **URL:** https://www.kaggle.com/datasets/ealaxi/paysim1
- **Description:** Synthetic datasets generated by the PaySim mobile money simulator.
- **Relevance:** **MEDIUM** - Mobile payment fraud patterns, applicable to marketplace payment systems

### 2.8 Real or Fake Job Postings
- **URL:** https://www.kaggle.com/code/szeyeung/real-or-fake-job-postings-ensemble-model
- **Description:** EMSCAD dataset - 17,800 job ads (2012-present) labeled as real or fake. Ensemble model approach.
- **Relevance:** **HIGH** - Directly applicable to detecting fraudulent listings in skill marketplaces

### 2.9 Trustpilot Reviews Sentiment Analysis
- **URL:** https://www.kaggle.com/code/nurudeenabdulsalaam/trustpilot-reviews-sentiment-analysis
- **Description:** Sentiment analysis on Trustpilot review data - a platform built around trust and reputation.
- **Relevance:** **MEDIUM** - Trust-focused review analysis techniques

### 2.10 Multi-Agent E-Commerce Shopping Decision Assistant
- **URL:** https://www.kaggle.com/competitions/agents-intensive-capstone-project/writeups/new-writeup-1763624946128
- **Description:** AI system that compares products, analyzes reviews, and filters suspicious patterns for buyers.
- **Relevance:** **MEDIUM** - Agent-based approach to trust assessment in marketplace decisions

---

## 3. Pricing Optimization & Dynamic Pricing

### 3.1 Dynamic Pricing Dataset
- **URL:** https://www.kaggle.com/datasets/arashnic/dynamic-pricing-dataset
- **Description:** Build a dynamic pricing model incorporating features to predict optimal fares for rides in real-time. Must consider demand, supply, and market conditions.
- **Relevance:** **VERY HIGH** - Core dynamic pricing dataset with demand/supply multipliers
- **ML Applications:**
  - Real-time price optimization
  - Demand-supply equilibrium modeling
  - Feature engineering for pricing models

### 3.2 Dynamic Programming: Price Optimization (Flight Revenue)
- **URL:** https://www.kaggle.com/code/bimimi/dynamic-programming-price-optimization
- **Description:** Dynamic programming approach to price optimization using Flight Revenue Simulator data.
- **Relevance:** **HIGH** - Advanced optimization techniques directly applicable to marketplace pricing
- **Techniques:** Dynamic programming, revenue management, yield optimization

### 3.3 The Art of Demand-Based Pricing Optimization (Hotel)
- **URL:** https://www.kaggle.com/code/juanjosemuozpanos/the-art-of-demand-based-pricing-optimization
- **Description:** Demand-based pricing optimization using hotel booking demand data.
- **Relevance:** **HIGH** - Demand elasticity and pricing strategy techniques transferable to skill marketplaces

### 3.4 Airline Price Optimization Solution
- **URL:** https://www.kaggle.com/code/dansbecker/airline-price-optimization-solution
- **Description:** Price optimization for airline tickets with Flight Revenue Simulator.
- **Relevance:** **MEDIUM-HIGH** - Revenue optimization techniques for perishable inventory (analogous to time-limited freelancer availability)

### 3.5 Building Dynamic Pricing Strategy Using Python
- **URL:** https://www.kaggle.com/code/surajkumarsahu112/building-dynamic-pricing-strategy-using-python
- **Description:** Flexible pricing strategy designed to maximize revenue and profitability by adapting to market demand, customer behavior, and competitor pricing.
- **Relevance:** **HIGH** - Practical Python implementation of dynamic pricing

### 3.6 Retail Price Optimization
- **URL:** https://www.kaggle.com/code/harshsingh2209/retail-price-optimization
- **Description:** Finding optimal price point to maximize profits, balancing price vs. sales volume.
- **Relevance:** **MEDIUM** - Price elasticity and optimization fundamentals

### 3.7 Retailer Price Optimization Model
- **URL:** https://www.kaggle.com/models/adeosunvictorayomide/retailer-price-optimization-model
- **Description:** Pre-trained model for retail price optimization.
- **Relevance:** **MEDIUM** - Reusable model architecture for price optimization

### 3.8 ReCell Project (Used Device Pricing)
- **URL:** https://www.kaggle.com/code/muzammilparacha/recell-project
- **Description:** ML-based dynamic pricing for used phones/tablets - predicting price based on features. Linear regression model.
- **Relevance:** **MEDIUM** - Pricing based on quality/feature attributes, analogous to skill-based pricing

### 3.9 Comprehensive Synthetic E-Commerce Dataset
- **URL:** https://www.kaggle.com/datasets/imranalishahh/comprehensive-synthetic-e-commerce-dataset
- **Published:** December 5, 2024
- **Description:** Synthetic e-commerce dataset with transaction, customer, product, and advertising data in a dynamic marketplace context.
- **Relevance:** **MEDIUM** - Multi-faceted marketplace data with pricing dimensions

### 3.10 AI and ML Jobs Analysis: Dynamic Pricing Models
- **URL:** https://www.kaggle.com/code/zain280/ai-and-ml-jobs-analysis-insights
- **Description:** Includes developing and implementing dynamic pricing models to optimize marketplace liquidity and profitability.
- **Relevance:** **MEDIUM-HIGH** - Directly references marketplace pricing optimization

---

## 4. Skill Demand Forecasting & Job Trends

### 4.1 AI Job Replacement & Skill Shift Dataset
- **URL:** https://www.kaggle.com/datasets/dmahajanbe23/ai-job-replacement-and-skill-shift-dataset
- **Description:** Models workforce dynamics using structured synthetic data (2020-2026). Features automation risk percentages, salary impact metrics, skill demand growth indicators, AI adoption levels, remote feasibility scores.
- **Relevance:** **VERY HIGH** - Directly models skill demand forecasting and workforce evolution
- **ML Applications:**
  - Automation risk prediction (regression)
  - Risk category classification
  - Wage volatility modeling
  - Workforce reskilling strategy research
  - Skill demand forecasting
  - Industry AI exposure scoring
- **Associated Notebooks:**
  - [AI Job Replacement Skill Shift Dataset Analysis](https://www.kaggle.com/code/ibrahimragabrashaad/ai-job-replacement-skill-shift-dataset-analysis)
  - [AI Changes Required Skill Mix](https://www.kaggle.com/code/sasakitetsuya/ai-changes-required-skill-mix) - Includes Skill Shift Index (SSI), Skill Archetypes via Clustering, Career Transition Simulation, Skill Portfolio Optimization
  - [AI Job Shift Analytics](https://www.kaggle.com/code/lalit7881/ai-job-shift-analytics)

### 4.2 Global AI Job Market & Salary Trends 2025
- **URL:** https://www.kaggle.com/datasets/bismasajjad/global-ai-job-market-and-salary-trends-2025
- **Description:** AI job market data for salary prediction, market trend analysis, and career planning.
- **Key Features:** Salary data, skill requirements, remote work patterns, job roles, locations
- **Relevance:** **HIGH** - Market intelligence for skill marketplace pricing and demand signals
- **ML Applications:**
  - Salary prediction models
  - Market trend analysis
  - Emerging role identification
  - Skill requirement analysis

### 4.3 Future Jobs and Skills Demand Analysis 2025
- **URL:** https://www.kaggle.com/code/devraai/future-jobs-and-skills-demand-analysis-2025
- **Description:** Analysis notebook on Future Jobs & Skills Demand 2025 dataset.
- **Relevance:** **HIGH** - Forward-looking skill demand analysis

### 4.4 Job Trend Forecasting Dataset
- **URL:** https://www.kaggle.com/datasets/illuminate123/job-trend-forecasting
- **Description:** Job market trend data designed for forecasting applications.
- **Relevance:** **HIGH** - Time-series job market data for trend prediction

### 4.5 Tech Layoffs & Hiring Trends 2025-2026
- **URL:** https://www.kaggle.com/datasets/ahsanneural/tech-layoffs-and-hiring-trends-2025-2026
- **Description:** Multi-level ML challenges including salary prediction, time series forecasting of layoff volumes, department prediction, NLP sentiment analysis, severance prediction.
- **Relevance:** **HIGH** - Rich feature set for workforce dynamics modeling

### 4.6 Demand Forecasting Dataset (Supply Chain)
- **URL:** https://www.kaggle.com/datasets/programmer3/demand-forecasting-dataset
- **Description:** Real-world sales data across products, categories, and retail locations with temporal/contextual variables (promotions, holidays, economic conditions).
- **Relevance:** **MEDIUM** - Demand forecasting techniques transferable to skill demand prediction

### 4.7 Job Skill Set Dataset
- **URL:** https://www.kaggle.com/datasets/batuhanmutlu/job-skill-set
- **Description:** Structured for ML projects related to job matching, skill extraction, and NLP tasks.
- **Relevance:** **MEDIUM-HIGH** - Skill taxonomy for matching

### 4.8 Resume / CV Skills Extraction Dataset
- **URL:** https://www.kaggle.com/datasets/muqaddasejaz/resume-cv-skills-extraction-dataset
- **Description:** Resume and CV text data categorized by professional domains for NLP and information extraction.
- **Relevance:** **MEDIUM** - Skill extraction from unstructured text

---

## 5. Quality Scoring & Benchmarking

### 5.1 Kaggle Benchmarks Platform
- **URL:** https://www.kaggle.com/benchmarks
- **Description:** New Kaggle platform for discovering open, rigorous benchmarks and leaderboards from top AI labs, researchers, and the Kaggle community. Includes Benchmarks SDK.
- **Relevance:** **HIGH** - Infrastructure for creating marketplace-specific quality benchmarks
- **Applications:** Can be used to benchmark agent/model quality in skill marketplace contexts

### 5.2 Skill & Career Recommendation Dataset
- **URL:** https://www.kaggle.com/datasets/tea340yashjoshi/skill-and-career-recommendation-dataset
- **Description:** Structured for predicting career paths based on students' skills and academic performance.
- **Relevance:** **MEDIUM-HIGH** - Skill-to-career quality matching

### 5.3 Yelp Review Sentiment Dataset
- **URL:** https://www.kaggle.com/datasets/ilhamfp31/yelp-review-dataset
- **Description:** 598,000 reviews from Yelp - a service marketplace with rich quality signals.
- **Relevance:** **MEDIUM** - Service quality scoring from review text

### 5.4 Reward Modeling Notebook
- **URL:** https://www.kaggle.com/code/lonnieqin/reward-modeling
- **Description:** Training and evaluating reward models for quality assessment.
- **Relevance:** **MEDIUM** - Reward modeling techniques applicable to quality scoring

---

## 6. Skill Matching & Recommendation Systems

### 6.1 Job Recommendations with Embeddings
- **URL:** https://www.kaggle.com/code/uycung/job-recommendations-with-embeddings
- **Description:** Embeddings-based approach to improve job matching effectiveness, addressing limitations of traditional keyword-based matching.
- **Relevance:** **VERY HIGH** - Core skill-to-job matching using modern embedding techniques
- **Techniques:** Sentence-BERT, semantic similarity, vector search

### 6.2 Job Recommender NLP (Sentence-BERT)
- **URL:** https://www.kaggle.com/code/muhammadaliasghar01/job-recommender-nlp
- **Description:** Job recommendation engine using Sentence-BERT embeddings. Supports both job seekers (resume-based) and employers (candidate matching).
- **Relevance:** **VERY HIGH** - Bi-directional marketplace matching system

### 6.3 Resume and Job Description Matching
- **URL:** https://www.kaggle.com/code/gemyai/resume-and-job-description-matching
- **Description:** ML-based matching between resumes and job descriptions.
- **Relevance:** **HIGH** - Direct skill matching implementation

### 6.4 Job & Resume Matchmaker Copilot
- **URL:** https://www.kaggle.com/competitions/agents-intensive-capstone-project/writeups/new-writeup-1763199945883
- **Description:** AI-powered copilot that analyses resumes, scrapes job postings, matches using intelligent scoring, and generates tailored recommendations.
- **Relevance:** **HIGH** - End-to-end matching pipeline with quality scoring

### 6.5 LightFM Hybrid Recommendation System (CareerVillage)
- **URL:** https://www.kaggle.com/code/niyamatalmass/lightfm-hybrid-recommendation-system
- **Description:** Hybrid recommendation system using LightFM on CareerVillage.org data.
- **Relevance:** **MEDIUM-HIGH** - Hybrid collaborative + content-based filtering for skill matching

### 6.6 Negotify: Autonomous AI Contract Negotiation Agent
- **URL:** https://www.kaggle.com/competitions/agents-intensive-capstone-project/writeups/negotify-autonomous-ai-contract-negotiation-agent
- **Description:** AI agent helping freelancers review contracts without expensive lawyers.
- **Relevance:** **MEDIUM** - Agent-based marketplace interaction pattern

---

## 7. Applicable ML Techniques

Based on the datasets and notebooks surveyed, the following ML techniques are most applicable to skill marketplace problems:

### Trust & Reputation Systems
| Technique | Application | Example Dataset |
|-----------|------------|-----------------|
| **Gradient Boosted Trees (XGBoost/LightGBM)** | Fraud detection, fake review classification | IEEE-CIS Fraud Detection, Deceptive Patterns |
| **Anomaly Detection (Isolation Forest, Autoencoders)** | Unusual rating patterns, suspicious activity | Fraud Detection Transactions (2026) |
| **NLP Sentiment Analysis (BERT, LSTM)** | Review quality assessment, trust scoring | Trustpilot Reviews, Yelp Reviews |
| **Graph Neural Networks** | Network-based fraud detection, reputation propagation | Multi-network analysis notebook |
| **Ensemble Methods (Random Forest + Logistic Regression)** | Fake job posting detection | Real or Fake Job Postings (EMSCAD) |

### Pricing Optimization
| Technique | Application | Example Dataset |
|-----------|------------|-----------------|
| **Dynamic Programming** | Optimal pricing under constraints | Flight Revenue Simulator |
| **Reinforcement Learning** | Adaptive pricing strategies | Dynamic Pricing Dataset |
| **Regression Models (Linear, Ridge, Lasso)** | Base price prediction from features | ReCell Project, Retail Price Optimization |
| **Time Series (SARIMA, Prophet)** | Seasonal pricing adjustments | Demand Forecasting Dataset |
| **Demand Elasticity Modeling** | Price sensitivity estimation | Hotel Booking Demand |

### Quality Scoring
| Technique | Application | Example Dataset |
|-----------|------------|-----------------|
| **Reward Modeling (RLHF-style)** | Quality score calibration | Reward Modeling notebook |
| **Multi-factor Scoring (Weighted aggregation)** | Composite quality scores | Freelancer Earnings dataset |
| **Bayesian Rating Systems** | Confidence-adjusted ratings | Global Freelancers dataset |
| **NLP Feature Extraction** | Skill verification from text | Resume/CV Skills Extraction |

### Demand Forecasting
| Technique | Application | Example Dataset |
|-----------|------------|-----------------|
| **SARIMA / Prophet** | Seasonal skill demand forecasting | Demand Forecasting Dataset |
| **Clustering (K-Means, DBSCAN)** | Skill archetype discovery | AI Job Replacement & Skill Shift |
| **Skill Shift Index (SSI)** | Tracking skill mix evolution | AI Changes Required Skill Mix notebook |
| **Career Transition Simulation** | Workforce mobility modeling | AI Job Replacement & Skill Shift |
| **Embedding-based Similarity** | Emerging skill detection | Job Recommendations with Embeddings |

### Skill Matching & Recommendation
| Technique | Application | Example Dataset |
|-----------|------------|-----------------|
| **Sentence-BERT Embeddings** | Semantic skill matching | Job Recommender NLP |
| **Hybrid Collaborative Filtering (LightFM)** | Personalized recommendations | CareerVillage Recommendation |
| **Content-Based Filtering (LDA + Cosine)** | Skill/expertise matching | Content Based Recommender |
| **NLP Named Entity Recognition** | Skill extraction from descriptions | Resume Parsing notebooks |

---

## 8. Recommended Priority Datasets

### Tier 1: Directly Applicable (Download Immediately)

| # | Dataset | Records | Key Value |
|---|---------|---------|-----------|
| 1 | [Freelancer Earnings & Job Trends](https://www.kaggle.com/datasets/shohinurpervezshohan/freelancer-earnings-and-job-trends) | Multi-platform | Cross-platform marketplace comparison with earnings, satisfaction, completion metrics |
| 2 | [Upwork Job Postings 2024 (50K)](https://www.kaggle.com/datasets/asaniczka/upwork-job-postings-dataset-2024-50k-records) | 50K | Real marketplace demand signals with skills, budgets, experience levels |
| 3 | [AI Job Replacement & Skill Shift](https://www.kaggle.com/datasets/dmahajanbe23/ai-job-replacement-and-skill-shift-dataset) | Large | Skill demand forecasting with automation risk, skill shift indices |
| 4 | [Dynamic Pricing Dataset](https://www.kaggle.com/datasets/arashnic/dynamic-pricing-dataset) | Varies | Core dynamic pricing with demand/supply features |
| 5 | [Deceptive Patterns](https://www.kaggle.com/datasets/akashnath29/deceiptive-patterns) | Varies | Fake review and deceptive rating detection |

### Tier 2: High Complementary Value

| # | Dataset | Key Value |
|---|---------|-----------|
| 6 | [All Upwork Jobs Monthly (200K+)](https://www.kaggle.com/datasets/asaniczka/all-jobs-on-upwork-200k-plus) | Longitudinal marketplace trends |
| 7 | [Fraud Detection Transactions (2026)](https://www.kaggle.com/datasets/barkataliarbab/fraud-detection-transactions) | Latest fraud detection benchmark |
| 8 | [Global AI Job Market & Salary Trends 2025](https://www.kaggle.com/datasets/bismasajjad/global-ai-job-market-and-salary-trends-2025) | Salary prediction & market intelligence |
| 9 | [Job Skill Set Dataset](https://www.kaggle.com/datasets/batuhanmutlu/job-skill-set) | Skill taxonomy for matching |
| 10 | [Brazilian E-Commerce (Olist)](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) | 100K orders with review/reputation data |

### Tier 3: Technique Transfer

| # | Resource | Technique Value |
|---|----------|----------------|
| 11 | [Job Recommendations with Embeddings](https://www.kaggle.com/code/uycung/job-recommendations-with-embeddings) | Embedding-based matching architecture |
| 12 | [AI Changes Required Skill Mix](https://www.kaggle.com/code/sasakitetsuya/ai-changes-required-skill-mix) | Skill Shift Index, clustering, portfolio optimization |
| 13 | [Dynamic Programming: Price Optimization](https://www.kaggle.com/code/bimimi/dynamic-programming-price-optimization) | DP-based pricing methodology |
| 14 | [Building Dynamic Pricing Strategy](https://www.kaggle.com/code/surajkumarsahu112/building-dynamic-pricing-strategy-using-python) | End-to-end Python pricing pipeline |
| 15 | [LightFM Hybrid Recommendation](https://www.kaggle.com/code/niyamatalmass/lightfm-hybrid-recommendation-system) | Hybrid recommendation for marketplace matching |

---

## Appendix: New Competitive Datasets & Benchmarks (2025-2026)

| Dataset | Date | Category | Novelty |
|---------|------|----------|---------|
| Fraud Detection Transactions | Jan 2026 | Fraud | Latest synthetic fraud benchmark |
| Upwork Jobs | Jun 2025 | Marketplace | Most recent freelance marketplace data |
| Global Freelancers (Raw) | Jul 2025 | Marketplace | Raw messy data for pipeline testing |
| E-Commerce Fraud Detection | Nov 2025 | Fraud | Cross-country fraud behavior patterns |
| Global AI Job Market & Salary 2025 | 2025 | Demand | Current AI job market intelligence |
| Tech Layoffs & Hiring 2025-2026 | 2025 | Demand | Multi-level ML challenges dataset |
| Kaggle Benchmarks Platform | 2025 | Benchmarking | New infrastructure for open benchmarks with SDK |

---

*Note: Kaggle pages are heavily JavaScript-rendered; dataset descriptions were compiled from DuckDuckGo search snippets, associated GitHub repos, and notebook metadata. Direct scraping was unsuccessful due to JS rendering. For full schema details, visit the dataset pages directly on Kaggle.*
