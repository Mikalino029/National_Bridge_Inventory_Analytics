# 📊 National Bridge Inventory (NBI) - Structural Analytics & Capital Planning Pipeline

## 🏗️ Project Overview
This project bridges **Civil Engineering domain knowledge** with an advanced **Data Engineering stack** to solve a critical infrastructure challenge: prioritizing maintenance capital across a massive regional network. 

Using a dataset of **15,034 public bridge inspection records** from the National Bridge Inventory (NBI), I engineered an end-to-end automated data pipeline. The system ingests messy, unformatted public logs, executes advanced data cleansing and imputation, runs relational database benchmarking, and visualizes a simulated **€6.31 Billion structural rehabilitation backlog** for executive decision-making.

---

## 🛠️ Technical Stack & Architecture

1. **Data Automation Engine (Python / Pandas):** Handles raw ingestion, deduplication, string-to-numeric type enforcements, feature engineering, and contextual data imputation.
2. **Relational Database Warehouse (SQLite / SQL):** Enforces entity integrity and runs advanced analytical window functions to isolate high-risk structures.
3. **Business Intelligence Interface (Power BI):** Translates complex tabular data into an interactive, multi-dimensional executive control dashboard.

---

## 🐍 1. Python ETL & Feature Engineering Pipeline
The raw NBI dataset contains heavily corrupted records, missing values, and mixed-type columns. The `clean_bridge_pipeline.py` script automates the following steps:
* **Deduplication:** Sorts records chronologically by construction year to preserve the most recent inspection telemetry, dropping obsolete duplicate IDs.
* **Type Enforcement & Normalization:** Converts alphanumeric code cells into clean numerical formats while coercing corrupted text faults into standardized `NaN` blocks.
* **Contextual Group Imputation:** Replaces missing structural component ratings by dynamically calculating the average condition scores of bridges built within the **exact same decade**, preserving historical engineering standards.
* **Feature Engineering:** Computes a global `Average_Condition_Score` and categorizes assets into `Maintenance_Urgency` tiers.

---

## 🗄️ 2. SQL Relational Database & Benchmarking Queries
The polished output is loaded into an SQLite database instance. To enable granular data discovery, the `bridge_analysis_queries.sql` script utilizes **SQL Window Functions** to calculate network baselines right alongside individual rows:

```sql
SELECT 
    Bridge_ID,
    State_Code,
    Material_Type,
    Infrastructure_Generation,
    Average_Condition_Score,
    ROUND(AVG(Average_Condition_Score) OVER(PARTITION BY Material_Type), 2) AS Material_Network_Avg,
    ROUND(AVG(Average_Condition_Score) OVER(PARTITION BY Infrastructure_Generation), 2) AS Generation_Network_Avg
FROM bridge_inspections
ORDER BY Average_Condition_Score ASC;
```
* **Impact:** This query isolates individual critical assets (e.g., a failing Steel bridge scoring `0.0`) and contrasts them directly against the broader material group baseline (`6.65`), allowing project controls managers to catch anomalies instantly.

---

## 📊 3. Power BI Executive Dashboard Insights
The business intelligence dashboard converts these data streams into clear, interactive management decisions based on two core data insights discovered during analysis:

1. **🧱 Material Durability Analysis:** Slicing the network reveals that **Masonry** bridges suffer from severe structural bottlenecks, with a massive volume of structures trapped under "Routine Monitoring." Conversely, **Aluminum & Wrought Iron** assets maintain a 0.00 backlog, proving superior material lifespan and resilience.
2. **⏳ Chronological Decay Curves:** The 5-bar historical era chart validates real-world civil engineering physics—displaying a steady, predictable decline in average condition ratings from modern construction eras down to pre-1960 historic structures.

### Visual Control Board Elements:
* **Financial Backlog Gauge:** Tracks the calculated **€6.31B** total repair bill against a **€15.00B** state infrastructure budget ceiling.
* **Risk Scatter Plot:** Crosses Daily Traffic Count against Average Condition Scores to isolate high-volume, low-health hazard clusters.
* **Geographic Heatmap:** Aggregates and colors regional bubbles based on a composite `Traffic_Risk_Index`.

---

## 📂 Repository Structure
```text
├── Data/
│   └── clean_bridge_analytics.csv    # Cleaned, feature-engineered output dataset
├── Scripts/
│   ├── clean_bridge_pipeline.py      # Automated Python ETL script
│   └── bridge_analysis_queries.sql   # Advanced SQL Window Function queries
└── Dashboard/
    ├── Bridge_Health_Dashboard.pbix  # Interactive Power BI development file
    └── Bridge_Health_Dashboard.pdf   # High-resolution executive report export
```

---

## 🚀 How to Run the Pipeline
1. Clone this repository to your local system.
2. Place the raw NBI source file inside your `/Data` directory.
3. Run the Python ETL script via terminal: `python Scripts/clean_bridge_pipeline.py`.
4. Open the generated SQLite instance or import the clean CSV into DB Browser to execute the SQL benchmarking scripts.
5. Launch the Power BI file and click **Refresh** to populate the interactive visuals!
