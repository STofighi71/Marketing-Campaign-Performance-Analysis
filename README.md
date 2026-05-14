# Marketing Campaign Performance & Attribution Analysis

## Project Overview

This project simulates a real-world marketing analytics workflow for a fictional company called Pulsar.

The goal is to generate realistic multi-channel marketing data, clean and validate the datasets, perform SQL-based business analysis, and build an interactive Power BI dashboard for stakeholder reporting.

The project covers the complete analytics lifecycle:

- Synthetic data generation using Python
- Data quality issue simulation
- Data cleaning and validation
- SQL business analysis using SQLite
- Interactive dashboard development in Power BI
- Documentation and reproducibility

This project was designed as an end-to-end analytics assignment focused on marketing campaign performance and attribution analysis.

---

# Business Problem

Pulsar is expanding its digital marketing operations across multiple channels and global markets.

The marketing team needs a structured, data-driven view of:

- Campaign performance
- Customer acquisition trends
- Return on ad spend (ROAS)
- Lead conversion efficiency
- Budget allocation effectiveness

The objective of this project is to transform raw marketing data into actionable business insights.

---

# Project Objectives

The project includes four major stages:

1. Generate realistic marketing datasets using Python
2. Simulate and clean real-world data quality issues
3. Perform analytical SQL queries using SQLite
4. Build a professional Power BI dashboard for business stakeholders

---

# Tech Stack

## Programming & Data Processing
- Python
- Pandas
- NumPy
- Faker

## Database & SQL
- SQLite
- SQL Window Functions

## Data Visualization
- Power BI

## Version Control
- Git
- GitHub

---

# Project Structure

```text
marketing-campaign-performance-analysis/
│
├── assets/
│   ├── executive_summary.png
│   ├── campaign_performance.png
│   └── lead_analysis.png
│
├── data/
│   ├── raw/
│   │   ├── campaigns.csv
│   │   ├── ad_performance.csv
│   │   └── leads.csv
│   │
│   └── cleaned/
│       ├── campaigns_clean.csv
│       ├── ad_performance_clean.csv
│       └── leads_clean.csv
│
├── scripts/
│   ├── data_generation.py
│   ├── cleaning_pipeline.py
│   └── load_to_sqlite.py
│
├── sql/
│   └── queries.sql
│
├── dashboard/
│   └── dashboard.pbix
│
├── reports/
│   └── cleaning_report.md
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Dataset Description

The project contains three relational datasets.

---

## 1. campaigns.csv

Contains marketing campaign metadata.

### Columns
- campaign_id
- campaign_name
- channel
- platform
- target_market
- start_date
- end_date
- objective
- budget_usd
- campaign_manager

### Total Records
Approximately 150 rows

---

## 2. ad_performance.csv

Contains campaign performance metrics.

### Columns
- record_id
- campaign_id
- report_date
- impressions
- clicks
- conversions
- spend_usd
- revenue_usd
- ctr
- cpc
- roas

### Total Records
Approximately 500 rows

---

## 3. leads.csv

Contains simulated lead and conversion information.

### Columns
- lead_id
- campaign_id
- lead_date
- conversion_date
- country
- industry
- lead_source
- deal_value_usd
- status

### Total Records
Approximately 400 rows

---

# Simulated Data Quality Issues

The raw datasets intentionally contain five realistic data quality issues.

## Included Issues

1. Exact duplicate rows
2. Incorrect data types
3. Impossible dates
4. Inconsistent category labels
5. Non-random missing values

These issues were intentionally embedded to simulate real-world marketing data exports and were resolved during the cleaning phase.

---

# Data Cleaning Pipeline

The cleaning pipeline performs the following tasks:

- Detects all embedded data quality issues
- Cleans and standardizes datasets
- Validates corrected outputs
- Saves cleaned datasets separately
- Documents all cleaning decisions

The original raw files are preserved unchanged.

---

# Data Cleaning Decisions

Several assumptions were made during the cleaning process to preserve analytical consistency.

Examples include:

- Standardizing inconsistent categorical labels
- Reconstructing missing revenue values using ROAS and spend
- Correcting invalid campaign dates
- Removing exact duplicate records
- Preserving legitimate NULL values where business meaning existed

All cleaning decisions are documented in `cleaning_report.md`.

---

# SQLite Database

The cleaned CSV datasets are loaded into a SQLite database to support structured analytical querying.

Database tables:
- campaigns
- ad_performance
- leads

SQLite was selected because it is lightweight, portable, and suitable for analytics prototyping workflows.

---

# SQL Analysis

The cleaned datasets are analyzed using SQLite queries.

The SQL analysis includes:

1. Spend and revenue analysis by channel
2. Top-performing campaigns by ROAS
3. Month-over-month performance trends
4. Lead conversion analysis
5. Platform-level CTR and CPC analysis
6. Industry lead quality analysis
7. Campaign cohort analysis
8. Advanced trend anomaly detection using SQL window functions (`LAG`, `OVER`)

---

# Dashboard Features

The Power BI dashboard includes:

- Cross-page interactive slicers
- Dynamic KPI trend indicators
- Time-series performance analysis
- Campaign-level profitability analysis
- Lead funnel visualization
- Geographic lead distribution
- Industry-level revenue insights
- Interactive filtering and drill-down capabilities

---

# Power BI Dashboard

The final dashboard contains three interactive pages.

---

## Page 1 — Executive Summary

Includes:
- KPI indicators
- Spend vs Revenue trends
- ROAS by channel
- Lead conversion metrics



---

## Page 2 — Campaign Performance

Includes:
- Campaign performance table
- Budget vs Revenue scatter chart
- Top campaigns by revenue
- Spend distribution by objective

---

## Page 3 — Lead & Audience Analysis

Includes:
- Lead source analysis
- Geographic lead distribution
- Industry deal value analysis
- Funnel visualization
- Lead quality summary table

---

# Key Metrics

The project analyzes several important marketing KPIs.

## CTR (Click-Through Rate)

CTR = Clicks / Impressions

## CPC (Cost Per Click)

CPC = Spend / Clicks

## ROAS (Return on Ad Spend)

ROAS = Revenue / Spend

## Lead Conversion Rate

Conversion Rate = Converted Leads / Total Leads

---

# Data Model

The datasets are connected using the `campaign_id` field.

Relationships:

- campaigns → ad_performance
- campaigns → leads

This creates a relational marketing analytics model suitable for SQL analysis and Power BI reporting.

---

# Reproducibility

The project uses a fixed random seed during data generation to ensure reproducible outputs.

This guarantees that the same datasets can be regenerated consistently.

---

# How to Run the Project

## 1. Clone Repository

```bash
git clone git@github.com:STofighi71/Marketing-Campaign-Performance-Analysis.git
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

---

## 3. Activate Environment

### Windows

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
source venv/bin/activate
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 5. Generate Raw Data

```bash
python scripts/data_generation.py
```

---

## 6. Run Cleaning Pipeline

```bash
python scripts/cleaning_pipeline.py
```

---

## 7. Load Data into SQLite

```bash
python scripts/load_to_sqlite.py
```

---

# Dashboard Preview

## Executive Summary

(Add screenshot here)

![Executive Summary](assets/executive_summary.png)

---

## Campaign Performance

(Add screenshot here)

![Campaign Performance](assets/campaign_performance.png)

---

## Lead & Audience Analysis

(Add screenshot here)

![Lead Analysis](assets/lead_analysis.png)

---

# Key Learning Outcomes

This project demonstrates practical experience in:

- Data generation and simulation
- Data quality management
- ETL workflows
- SQL analytics
- SQL window functions
- Marketing KPI analysis
- Dashboard design
- Business-focused storytelling
- Interactive reporting development

---

# Future Improvements

Potential future enhancements:

- Multi-touch attribution modeling
- Customer lifetime value analysis
- Marketing mix modeling
- Forecasting campaign performance
- Automated reporting pipelines
- Cloud-based data warehousing integration

---

# Important Note

This project was intentionally designed to simulate realistic marketing analytics workflows and common data quality challenges encountered in production environments.

The embedded data issues were introduced deliberately and resolved through a documented cleaning pipeline to demonstrate practical analytical problem-solving skills.

