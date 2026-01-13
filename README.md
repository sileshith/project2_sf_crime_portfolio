# San Francisco Crime Analytics (2018–2025) + 2026 Outlook

## Overview

This project analyzes San Francisco Police Department (SFPD) incident records from 2018–2025 and produces a short-term citywide forecast for 2026.

It is designed as a **portfolio-quality analytics project** demonstrating an end-to-end workflow: data validation, feature engineering, reproducible aggregation pipelines, forecasting, and deployment of an interactive dashboard.

The emphasis is on **structure, reproducibility, and clarity**, mirroring real-world analytics systems rather than ad-hoc exploration.

## Reports

- **Executive Presentation Deck:**  
  `reports/SF_CrimeTrendAnalysis_2026Forecast.pdf`  
  Concise, slide-based summary highlighting key findings, MSI framework, hotspot analysis, and the 2026 outlook.

- **Full Technical Report:**  
  `reports/SF Crime Trend Analysis and Forecasting (2018-2025).pdf`  
  Comprehensive documentation covering data validation, feature engineering, exploratory analysis, modeling decisions, and analytical limitations.

## Live Dashboard

**Public Streamlit App:**  
 https://project2sfcrimeportfolio-g6jhgqizljzqexcb3ss7wd.streamlit.app/

The deployed dashboard reads exclusively from **precomputed parquet artifacts** and does not rely on raw incident-level data at runtime.

This design mirrors production analytics environments where dashboards are decoupled from raw data storage.


---

## Project Structure

```text
project2_sf_crime_portfolio/
│
├── dashboard/
│   └── app.py              # Streamlit dashboard (reads precomputed artifacts)
│
├── data/
│   ├── raw/                # Original SFPD data (not tracked)
│   └── processed/          # Cleaned & aggregated parquet artifacts
│
├── notebooks/
│   ├── 01_data_validation_and_cleaning.ipynb
│   ├── 02_exploratory_analysis.ipynb
│   └── 03_forecasting_2026.ipynb
│
├── models/                 # Saved forecasting model artifacts (optional)
│
├── reports/
│   └── sf_crime_analysis_report.pdf
│
├── scripts/
│   └── build_dashboard_artifacts.py   # Reproducible aggregation pipeline
│
├── .streamlit/
│   └── config.toml         # Dashboard theme configuration
│
├── README.md
└── requirements.txt
```

---

## Data

### Source
- DataSF - Police Incident Reports
- Neighborhood definitions follow the official **Analysis Neighborhoods** system used by the City of San Francisco.

### Included Data (GitHub-friendly)
To keep the repository lightweight and reproducible, the dashboard reads from **precomputed parquet artifacts** rather than raw incident-level data.

Included processed files:
- `data/processed/monthly_neighborhood_category.parquet`
- `data/processed/hourly_weekday_counts.parquet`
- `data/processed/monthly_citywide.parquet`
- `data/processed/forecast_citywide_monthly_2026.parquet`

### Omitted Data
The full cleaned incident-level dataset  
`incidents_clean_2018_2025.parquet` (~1M rows) is not included due to size constraints.

All dashboard views and forecasts rely exclusively on the aggregated artifacts listed above.  
This mirrors real-world analytics systems where dashboards are decoupled from raw data storage.

---

## Dashboard

The interactive dashboard is built using **Streamlit** and **Plotly**.

Features:
- Citywide and neighborhood-level trends
- Hour × weekday pattern analysis
- Interactive filtering (years, neighborhoods, categories, weekdays, hours)
- Precomputed 2026 citywide forecast
- Downloadable filtered CSV

### Run Locally

1. Activate environment:
```bash
   conda activate py313
```

2. Install dependencies:
```
    pip install -r requirements.txt
```

3. Launch the dashboard:
```
streamlit run dashboard/app.py
```

### Notes on Interpretation

The 2026 forecast is intended as a planning and trend-monitoring signal, not a causal claim.

Results reflect reported incidents and may be influenced by reporting practices, policy changes, and external events.

This project prioritizes analytical rigor and reproducibility over visual embellishment.

#### Author

Sileshi Hirpa  
Data Science & Business Analytics  
Arizona State University
