
import pandas as pd
import sqlite3

# Load cleaned data
campaigns = pd.read_csv("data/cleaned/campaigns_clean.csv")
ad_perf = pd.read_csv("data/cleaned/ad_performance_clean.csv")
leads = pd.read_csv("data/cleaned/leads_clean.csv")

# Create SQLite DB
conn = sqlite3.connect("marketing.db")

# Load into tables
campaigns.to_sql("campaigns", conn, if_exists="replace", index=False)
ad_perf.to_sql("ad_performance", conn, if_exists="replace", index=False)
leads.to_sql("leads", conn, if_exists="replace", index=False)

print("Database created successfully")