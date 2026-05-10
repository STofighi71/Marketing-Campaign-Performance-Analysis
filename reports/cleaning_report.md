# Cleaning Report — Marketing Campaign Analysis

## Dataset 1: campaigns.csv

### Issue 1: Inconsistent channel labels
- Detected using value_counts()
- Standardized using str.title()
- Ensures consistency for grouping in SQL & Power BI

---

### Issue 2: Impossible dates
- Found campaigns where end_date < start_date
- Fixed by enforcing minimum 30-day duration
- Assumption: campaigns must run at least 1 month

---

## Dataset 2: ad_performance.csv

### Issue 3: CTR stored as string (%)
- Detected presence of '%' in numeric column
- Converted to float decimal format
- Required for correct KPI calculations

---

### Issue 4: Duplicate rows
- Identified using pandas.duplicated()
- Removed exact duplicates
- Assumption: duplicates are ingestion errors

---

### Issue 5: Missing revenue (Email campaigns)
- Detected pattern-based missing values
- Filled using spend × ROAS
- Assumption: attribution loss but spend data reliable

---

## Dataset 3: leads.csv

### Issue 6: Status inconsistency handling
- Normalized casing for consistency

### Issue 7: Invalid conversion dates
- Removed conversion dates before lead dates

---

## Final Note
All cleaning decisions were made with a balance between data integrity and business realism. No raw data was overwritten.