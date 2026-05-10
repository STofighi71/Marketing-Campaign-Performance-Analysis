
import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import timedelta


# Set random seed for reproducibility
RANDOM_SEED = 42

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

fake = Faker()
Faker.seed(RANDOM_SEED)

# Define constants and parameters for data generation
RAW_DATA_PATH = "data/raw/"

CHANNELS = [
    "Paid Search",
    "Paid Social",
    "Display",
    "Email",
    "Influencer",
    "Affiliate"
]


PLATFORM_MAPPING = {
    "Paid Search": ["Google Ads"],
    "Paid Social": ["Meta", "TikTok", "LinkedIn"],
    "Display": ["Google Ads"],
    "Email": ["Mailchimp"],
    "Influencer": ["YouTube", "TikTok"],
    "Affiliate": ["LinkedIn"]
}


MARKETS = [
    "EMEA",
    "North America",
    "APAC",
    "LATAM"
]


OBJECTIVES = [
    "Awareness",
    "Lead Generation",
    "Conversion",
    "Retention"
]


COUNTRIES = [
    "Germany",
    "France",
    "United Kingdom",
    "United States",
    "Canada",
    "Brazil",
    "Mexico",
    "India",
    "Japan",
    "Australia",
    "Spain",
    "Italy"
]


INDUSTRIES = [
    "Retail",
    "Finance",
    "Healthcare",
    "SaaS",
    "Travel",
    "Education",
    "Real Estate",
    "Automotive"
]

LEAD_SOURCES = [
    "Organic",
    "Paid",
    "Referral",
    "Direct"
]

CAMPAIGN_MANAGERS = [
    fake.name() for _ in range(15)
]



START_DATE = pd.Timestamp("2024-01-01")
END_DATE = pd.Timestamp("2025-06-30")


CHANNEL_PERFORMANCE = {
    "Paid Search": {
        "ctr_range": (0.03, 0.08),
        "conversion_rate": (0.05, 0.12),
        "cpc_range": (1.5, 4.0),
        "roas_range": (2.0, 5.0)
    },

    "Paid Social": {
        "ctr_range": (0.01, 0.05),
        "conversion_rate": (0.03, 0.08),
        "cpc_range": (0.8, 2.5),
        "roas_range": (1.5, 4.0)
    },

    "Display": {
        "ctr_range": (0.002, 0.015),
        "conversion_rate": (0.01, 0.04),
        "cpc_range": (0.3, 1.2),
        "roas_range": (0.8, 2.0)
    },

    "Email": {
        "ctr_range": (0.04, 0.12),
        "conversion_rate": (0.08, 0.20),
        "cpc_range": (0.1, 0.5),
        "roas_range": (4.0, 10.0)
    },

    "Influencer": {
        "ctr_range": (0.01, 0.04),
        "conversion_rate": (0.02, 0.06),
        "cpc_range": (1.0, 3.5),
        "roas_range": (1.0, 3.0)
    },

    "Affiliate": {
        "ctr_range": (0.02, 0.06),
        "conversion_rate": (0.04, 0.10),
        "cpc_range": (0.5, 2.0),
        "roas_range": (3.0, 7.0)
    }
}



# Function to generate synthetic campaign data
def generate_campaigns(num_campaigns=150):

    campaigns = []

    for i in range(1, num_campaigns + 1):

        channel = random.choice(CHANNELS)

        platform = random.choice(
            PLATFORM_MAPPING[channel]
        )

        start_date = START_DATE + timedelta(
            days=random.randint(0, 500)
        )

        duration_days = random.randint(30, 120)

        end_date = start_date + timedelta(
            days=duration_days
        )

        campaign = {
            "campaign_id": f"CAMP_{i:03}",
            "campaign_name": f"{channel} Campaign {i}",
            "channel": channel,
            "platform": platform,
            "target_market": random.choice(MARKETS),
            "start_date": start_date.date(),
            "end_date": end_date.date(),
            "objective": random.choice(OBJECTIVES),
            "budget_usd": round(
                random.uniform(5000, 150000),
                2
            ),
            "campaign_manager": random.choice(
                CAMPAIGN_MANAGERS
            )
        }

        campaigns.append(campaign)

    campaigns_df = pd.DataFrame(campaigns)

    return campaigns_df


# Generate campaigns dataframe
campaigns_df = generate_campaigns()



# DATA QUALITY ISSUE #1:
# Inconsistent category labels in channel column

campaigns_df.loc[5, "channel"] = "paid social"
campaigns_df.loc[12, "channel"] = "PAID SOCIAL"



# DATA QUALITY ISSUE #2:
# Impossible date where end_date occurs before start_date

campaigns_df.loc[20, "end_date"] = (
    campaigns_df.loc[20, "start_date"]
    - timedelta(days=10)
)


# Save campaigns data to CSV
campaigns_df.to_csv(
    RAW_DATA_PATH + "campaigns.csv",
    index=False
)



# Function to generate synthetic ad performance data based on campaigns
def generate_ad_performance(campaigns_df):

    performance_records = []

    record_id = 1

    for _, campaign in campaigns_df.iterrows():

        campaign_id = campaign["campaign_id"]
        channel = campaign["channel"]

        # Use normalized channel name
        normalized_channel = str(channel).title()

        if normalized_channel == "Paid Social":
            normalized_channel = "Paid Social"

        profile = CHANNEL_PERFORMANCE.get(
            normalized_channel,
            CHANNEL_PERFORMANCE["Paid Social"]
        )

        start_date = pd.to_datetime(
            campaign["start_date"]
        )

        end_date = pd.to_datetime(
            campaign["end_date"]
        )

        # Skip invalid date ranges temporarily
        if end_date <= start_date:
            continue

        # Generate 2 to 5 performance records per campaign
        num_records = random.randint(2, 5)

        for _ in range(num_records):

            report_date = start_date + timedelta(
                days=random.randint(
                    0,
                    (end_date - start_date).days
                )
            )

            impressions = random.randint(
                1000,
                100000
            )

            ctr = round(
                random.uniform(
                    profile["ctr_range"][0],
                    profile["ctr_range"][1]
                ),
                4
            )

            clicks = int(impressions * ctr)

            conversion_rate = random.uniform(
                profile["conversion_rate"][0],
                profile["conversion_rate"][1]
            )

            conversions = int(
                clicks * conversion_rate
            )

            cpc = round(
                random.uniform(
                    profile["cpc_range"][0],
                    profile["cpc_range"][1]
                ),
                2
            )

            spend = round(
                clicks * cpc,
                2
            )

            roas = round(
                random.uniform(
                    profile["roas_range"][0],
                    profile["roas_range"][1]
                ),
                2
            )

            revenue = round(
                spend * roas,
                2
            )

            performance_record = {
                "record_id": record_id,
                "campaign_id": campaign_id,
                "report_date": report_date.date(),
                "impressions": impressions,
                "clicks": clicks,
                "conversions": conversions,
                "spend_usd": spend,
                "revenue_usd": revenue,
                "ctr": ctr,
                "cpc": cpc,
                "roas": roas
            }

            performance_records.append(
                performance_record
            )

            record_id += 1

    performance_df = pd.DataFrame(
        performance_records
    )

    return performance_df


# Generate ad performance dataframe
ad_performance_df = generate_ad_performance(
    campaigns_df
)



# DATA QUALITY ISSUE #3:
# Wrong data type in ctr column stored as percentage string

# Convert ctr column to object type
# so mixed data types can exist intentionally
ad_performance_df["ctr"] = (
    ad_performance_df["ctr"].astype(object)
)

ad_performance_df.loc[3, "ctr"] = "4.2%"
ad_performance_df.loc[17, "ctr"] = "7.5%"
ad_performance_df.loc[42, "ctr"] = "2.1%"



# DATA QUALITY ISSUE #4:
# Exact duplicate rows added intentionally

duplicate_rows = ad_performance_df.sample(
    3,
    random_state=RANDOM_SEED
)

ad_performance_df = pd.concat(
    [ad_performance_df, duplicate_rows],
    ignore_index=True
)



# DATA QUALITY ISSUE #5:
# Non-random missing values for revenue in Email campaigns

email_campaign_ids = campaigns_df[
    campaigns_df["channel"].str.lower() == "email"
]["campaign_id"]

ad_performance_df.loc[
    ad_performance_df["campaign_id"].isin(
        email_campaign_ids
    ),
    "revenue_usd"
] = np.nan

# Save ad performance data to CSV
ad_performance_df.to_csv(
    RAW_DATA_PATH + "ad_performance.csv",
    index=False
)


# Function to generate synthetic leads data based on campaigns
def generate_leads(campaigns_df, num_leads=400):

    leads = []

    for i in range(1, num_leads + 1):

        campaign = campaigns_df.sample(
            1,
            random_state=RANDOM_SEED + i
        ).iloc[0]

        campaign_id = campaign["campaign_id"]

        start_date = pd.to_datetime(
            campaign["start_date"]
        )

        end_date = pd.to_datetime(
            campaign["end_date"]
        )

        # Handle invalid campaign dates
        if end_date <= start_date:
            lead_date = start_date
        else:
            lead_date = start_date + timedelta(
                days=random.randint(
                    0,
                    max(
                        1,
                        (end_date - start_date).days
                    )
                )
            )

        status = random.choices(
            ["New", "Qualified", "Converted", "Lost"],
            weights=[0.25, 0.30, 0.30, 0.15],
            k=1
        )[0]

        conversion_date = None
        deal_value = None

        if status == "Converted":

            conversion_date = lead_date + timedelta(
                days=random.randint(7, 60)
            )

            deal_value = round(
                random.uniform(1000, 50000),
                2
            )

        lead = {
            "lead_id": f"LEAD_{i:04}",
            "campaign_id": campaign_id,
            "lead_date": lead_date.date(),
            "conversion_date": (
                conversion_date.date()
                if conversion_date
                else None
            ),
            "country": random.choice(COUNTRIES),
            "industry": random.choice(INDUSTRIES),
            "lead_source": random.choice(
                LEAD_SOURCES
            ),
            "deal_value_usd": deal_value,
            "status": status
        }

        leads.append(lead)

    leads_df = pd.DataFrame(leads)

    return leads_df

# Generate leads dataframe
leads_df = generate_leads(campaigns_df)


# Save leads data to CSV
leads_df.to_csv(
    RAW_DATA_PATH + "leads.csv",
    index=False
)




print("\n==============================")
print("FINAL DATA VALIDATION")
print("==============================")

print("\nCampaigns Dataset:")
print(campaigns_df.shape)

print("\nAd Performance Dataset:")
print(ad_performance_df.shape)

print("\nLeads Dataset:")
print(leads_df.shape)

print("\nLead Status Distribution:")
print(
    leads_df["status"]
    .value_counts()
)

print("\nUnique Campaign IDs:")
print(campaigns_df["campaign_id"].nunique())

print("\nAd Performance Campaign Match:")
print(
    ad_performance_df["campaign_id"]
    .isin(campaigns_df["campaign_id"])
    .all()
)

print("\nLeads Campaign Match:")
print(
    leads_df["campaign_id"]
    .isin(campaigns_df["campaign_id"])
    .all()
)

print("\nDuplicate Rows in Ad Performance:")
print(
    ad_performance_df
    .duplicated()
    .sum()
)

print("\nMissing Revenue Values:")
print(
    ad_performance_df["revenue_usd"]
    .isna()
    .sum()
)

print("\nData Generation Completed Successfully.")