
# San Francisco Crime Analytics (2018–2025) + 2026 Forecast

## Overview
This project analyzes San Francisco Police Department incident records from 2018–2025 and produces a short-term citywide forecast for 2026.  
It is designed as a portfolio-quality analytics project demonstrating an end-to-end workflow: validated data, engineered time features, reproducible aggregates, forecasting, and an interactive dashboard.

The emphasis is on reproducibility, structure, and clarity rather than ad-hoc exploration.

---

## Project Structure

```text
project2_sf_crime_portfolio/
│
├── dashboard/
│   └── app.py              # Main Streamlit dashboard code
│
├── data/
│   ├── raw/                # Original, immutable data (SFPD Open Data)
│   └── processed/          # Cleaned Parquet files & aggregated 'lite' datasets
│
├── notebooks/
│   ├── 01_data_validation_and_cleaning.ipynb
│   ├── 02_exploratory_analysis.ipynb
│   └── 03_forecasting_2026.ipynb   # Prophet modeling and 2026 predictions
│
├── models/                 # Saved Prophet model binaries (.json or .pkl)
│
├── reports/
│   └── sf_crime_analysis_report.pdf
│
├── scripts/                # Helper .py scripts for data processing
│
├── README.md               # Project overview and setup instructions
└── requirements.txt        # Python dependencies (Pandas, Prophet, Plotly)
```

---

## Data

### Source
- DataSF – Police Incident Reports
- Neighborhood definitions follow the official **Analysis Neighborhoods** system used by the City of San Francisco.

### Included Data (GitHub-friendly)
To keep the repository lightweight and reproducible, the dashboard reads from **precomputed parquet artifacts** rather than raw incident-level data.

Included processed files:
- `data/processed/daily_counts.parquet`
- `data/processed/neighborhood_counts.parquet`
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
