
import pandas as pd
import numpy as np

# Define file paths
RAW_DATA_PATH = "data/raw/"
CLEAN_DATA_PATH = "data/cleaned/"

# Load raw data
campaigns = pd.read_csv(RAW_DATA_PATH + "campaigns.csv")
ad_perf = pd.read_csv(RAW_DATA_PATH + "ad_performance.csv")
leads = pd.read_csv(RAW_DATA_PATH + "leads.csv")



# CLEANING: campaigns.csv

# Fix date consistency (extra safety)
campaigns["start_date"] = pd.to_datetime(campaigns["start_date"])
campaigns["end_date"] = pd.to_datetime(campaigns["end_date"])

# Detection of Issue 1 — Inconsistent category labels (channel)
campaigns["channel"].value_counts()

# Correction of Issue 1 — Standardize channel labels
campaigns["channel"] = campaigns["channel"].str.title()


# Detection of Issue 2 — Impossible date (end_date < start_date)
invalid_dates = campaigns[
    campaigns["end_date"] < campaigns["start_date"]
]

# Correction of Issue 2 — Fix invalid date ranges
# Assumption: campaign duration minimum 30 days

campaigns.loc[
    campaigns["end_date"] < campaigns["start_date"],
    "end_date"
] = (
    campaigns["start_date"] + pd.Timedelta(days=30)
)



# CLEANING: ad_performance.csv

# Detection of Issue 3 — Wrong data type (ctr as string %)
ad_perf["ctr"].dtype
ad_perf[ad_perf["ctr"].astype(str).str.contains("%", na=False)]

# Correction of Issue 3 — Convert ctr from percentage string to float between 0 and 1
ad_perf["ctr"] = ad_perf["ctr"].astype(str).str.replace("%", "")
ad_perf["ctr"] = ad_perf["ctr"].astype(float) / 100


# Detection of Issue 4 — Duplicate rows
ad_perf.duplicated().sum()

# Correction of Issue 4 — Remove duplicate rows
ad_perf = ad_perf.drop_duplicates()


# Detection of Issue 5 — Non-random missing revenue (Email campaigns)
ad_perf[ad_perf["revenue_usd"].isna()]["campaign_id"].value_counts()

# Correction of Issue 5 — Impute missing revenue for Email campaigns using spend and ROAS (Assumption: Revenue = Spend * ROAS)
email_mask = campaigns.set_index("campaign_id").loc[
    ad_perf["campaign_id"]
]["channel"].values == "Email"

ad_perf.loc[
    ad_perf["revenue_usd"].isna(),
    "revenue_usd"
] = (
    ad_perf["spend_usd"] *
    ad_perf["roas"]
)



# CLEANING: leads.csv

# Fix date consistency (extra safety)
leads["lead_date"] = pd.to_datetime(leads["lead_date"])
leads["conversion_date"] = pd.to_datetime(leads["conversion_date"])


# Fix impossible conversions (if any)
leads.loc[
    leads["conversion_date"] < leads["lead_date"],
    "conversion_date"
] = np.nan


# Normalize categorical values
leads["status"] = leads["status"].str.title()
leads["lead_source"] = leads["lead_source"].str.title()
leads["industry"] = leads["industry"].str.title()

# Fix missing deal values consistency
leads.loc[
    leads["status"] != "Converted",
    "deal_value_usd"
] = np.nan



# Save Clean Files
campaigns.to_csv(CLEAN_DATA_PATH + "campaigns_clean.csv", index=False)
ad_perf.to_csv(CLEAN_DATA_PATH + "ad_performance_clean.csv", index=False)
leads.to_csv(CLEAN_DATA_PATH + "leads_clean.csv", index=False)