
-- QUERY 1 — Total spend and total revenue by channel

SELECT
    c.channel,
    SUM(a.spend_usd) AS total_spend,
    SUM(a.revenue_usd) AS total_revenue
FROM ad_performance a
JOIN campaigns c
    ON a.campaign_id = c.campaign_id
GROUP BY c.channel;



-- QUERY 2 — Top 10 campaigns by ROAS

SELECT
    campaign_id,
    SUM(revenue_usd) * 1.0 / NULLIF(SUM(spend_usd), 0) AS roas
FROM ad_performance
GROUP BY campaign_id
ORDER BY roas DESC
LIMIT 10;



-- QUERY 3 — Month-over-month spend vs revenue trend

SELECT
    STRFTIME('%Y-%m', report_date) AS month,
    SUM(spend_usd) AS total_spend,
    SUM(revenue_usd) AS total_revenue
FROM ad_performance
GROUP BY month
ORDER BY month;



-- QUERY 4 — Lead conversion rate by channel and campaign objective

SELECT
    c.channel,
    c.objective,
    COUNT(l.lead_id) AS total_leads,
    SUM(CASE WHEN l.status = 'Converted' THEN 1 ELSE 0 END) * 1.0 / COUNT(l.lead_id) AS conversion_rate
FROM leads l
JOIN campaigns c
    ON l.campaign_id = c.campaign_id
GROUP BY c.channel, c.objective;


-- QUERY 5 — Average CTR and CPC by platform

SELECT
    c.platform,
    AVG(a.ctr) AS avg_ctr,
    AVG(a.cpc) AS avg_cpc
FROM ad_performance a
JOIN campaigns c
    ON a.campaign_id = c.campaign_id
GROUP BY c.platform;



-- QUERY 6 — Monthly lead volume and average deal value by industry
-- Note: AVG excludes NULL values. The NULL values represent non-converted leads. 
-- Since deal_value_usd is only assigned for converted leads, industries with low conversion
-- rates or no conversions will naturally show NULL averages. This is expected and reflects 
-- real-world funnel drop-off.

SELECT
    industry,
    STRFTIME('%Y-%m', lead_date) AS month,
    COUNT(*) AS lead_volume,
    AVG(deal_value_usd) AS avg_deal_value
FROM leads
GROUP BY industry, month;


-- QUERY 7 — Campaign cohort analysis: revenue at 30, 60, 90 days after launch

WITH campaign_launch AS (
    SELECT
        campaign_id,
        MIN(start_date) AS launch_date
    FROM campaigns
    GROUP BY campaign_id
),

revenue_by_days AS (
    SELECT
        a.campaign_id,
        c.launch_date,
        JULIANDAY(a.report_date) - JULIANDAY(c.launch_date) AS days_since_launch,
        a.revenue_usd
    FROM ad_performance a
    JOIN campaign_launch c
        ON a.campaign_id = c.campaign_id
)
SELECT
    campaign_id,

    SUM(CASE WHEN days_since_launch <= 30 THEN revenue_usd ELSE 0 END) AS revenue_30d,
    SUM(CASE WHEN days_since_launch <= 60 THEN revenue_usd ELSE 0 END) AS revenue_60d,
    SUM(CASE WHEN days_since_launch <= 90 THEN revenue_usd ELSE 0 END) AS revenue_90d

FROM revenue_by_days
GROUP BY campaign_id;



-- QUERY 8 — Campaigns where spend increased for 3 months but ROAS declined

WITH monthly AS (
    SELECT
        campaign_id,
        STRFTIME('%Y-%m', report_date) AS month,
        SUM(spend_usd) AS spend,
        SUM(revenue_usd) * 1.0 / NULLIF(SUM(spend_usd), 0) AS roas
    FROM ad_performance
    GROUP BY campaign_id, month
),

windowed AS (
    SELECT
        *,
        LAG(spend, 1) OVER (PARTITION BY campaign_id ORDER BY month) AS spend_lag1,
        LAG(spend, 2) OVER (PARTITION BY campaign_id ORDER BY month) AS spend_lag2,

        LAG(roas, 1) OVER (PARTITION BY campaign_id ORDER BY month) AS roas_lag1,
        LAG(roas, 2) OVER (PARTITION BY campaign_id ORDER BY month) AS roas_lag2

    FROM monthly
)
SELECT
    campaign_id,
    month,
    spend,
    roas
FROM windowed
WHERE
    spend > spend_lag1
    AND spend_lag1 > spend_lag2
    AND roas < roas_lag1
    AND roas_lag1 < roas_lag2;