<!-- HERO HEADER (Jupyter Notebook & HTML Export) -->
<div style="
position: relative;
width: 100%;
min-height: 520px;
border-radius: 10px;
overflow: hidden;
">
<img src="goldenGatebrge.png"
alt="Golden Gate Bridge"
style="width: 100%; height: auto; display: block;">
<div style="
position: absolute;
top: 0; left: 0; right: 0; bottom: 0;
background-color: rgba(0,0,0,0.45);
"></div>
<div style="
position: absolute;
top: 30%;
left: 50%;
transform: translate(-50%, -50%);
width: 90%;
max-width: 900px;
text-align: center;
color: white;
z-index: 2;
">
<h1 style="
font-size: 42px;
font-weight: 800;
line-height: 1.15;
margin: 0;
padding: 0;
">
San Francisco Crime Analytics (2018-2025)
</h1>
<h2 style="
font-size: 22px;
font-weight: 500;
margin-top: 10px;
padding: 0;
">
Time-Series Forecasting and Geospatial Analysis Using Python
</h2>
</div>
<div style="
position: absolute;
bottom: 40px;
left: 40px;
z-index: 2;
color: white;
font-size: 15px;
line-height: 1.45;
background-color: rgba(0,0,0,0.45);
padding: 12px 20px;
border-radius: 6px;
white-space: nowrap;
">
<strong>Author:</strong> Sileshi Hirpa<br>
<strong>Data Source:</strong> SFPD Incident Reports (DataSF)<br>
<strong>Time Window:</strong> 2018-2025<br>
<strong>Model:</strong> SARIMA (3.78% MAPE)
</div>
<div style="
position: absolute;
bottom: 40px;
right: 40px;
z-index: 2;
color: white;
font-size: 14px;
font-style: italic;
text-align: right;
">
Portfolio Project • December 2025
</div>
</div>
<div style="text-align: center; font-size: 12px; color: gray; margin-top: 6px;">
Cover Image Source: Britannica - “Golden Gate Bridge”
</div>



## San Francisco Crime Analytics (2018-2025)

An end-to-end analysis of nearly one million SFPD incident reports. This project covers data cleaning, exploratory visualization, geospatial patterns, time-series forecasting, and interactive dashboard development. The SARIMA forecasting model achieves 3.78% MAPE and reduces forecast error by 78.9% compared to a seasonal naive baseline.



### Table of Contents
1. [Project Overview](#project-overview)
2. [Research Goals](#research-goals)
3. [Dataset](#dataset)
4. [Repository Structure](#repository-structure)
5. [Analytical Summary](#analytical-summary)
   - [Citywide Trend](#1-citywide-trend-2018-2025)
   - [Neighborhood Hotspots](#2-neighborhood-hotspots)
   - [Leading Crime Categories](#3-leading-crime-categories)
   - [Daily & Weekly Patterns](#4-daily-and-weekly-patterns)
   - [Neighborhood Profiles](#5-neighborhood-crime-profiles)
   - [Forecasting Early 2026](#6-forecasting-early-2026-sarima)
   - [Dashboard Features](#7-dashboard-highlights)
6. [How to Run This Project](#how-to-run-this-project)
7. [Dashboard Snapshot](#dashboard-snapshot)
8. [Key Skills Demonstrated](#key-skills-demonstrated)



### Project Overview

This analysis explores crime trends in San Francisco using **2018-2025 SFPD incident data**. The work includes:
- Detailed data cleaning and feature engineering
- Temporal and weekday/hourly analysis
- Profiling across DataSF’s **41 Analysis Neighborhoods**
- Category-level exploration
- SARIMA-based forecasting for early 2026
- Dual dashboards (local and API-powered) for interactive exploration

The project follows a practical, real-world analytic workflow.


#### Research Goals

1. Identify which neighborhoods and categories contribute most to incident volume.
2. Examine hourly and weekly crime cycles.
3. Track citywide trends from 2018 through 2025.
4. Produce a baseline SARIMA forecast for early 2026.
5. Build dashboards for analysts and public audiences.


### Dataset

- **Source:** DataSF Open Data Portal
- **Dataset:** Police Incident Reports
- **Time Span:** 2018–2025
- **Geographical Standard:** DataSF’s **41 Analysis Neighborhoods**



### Repository Structure

```
├── README.md
├── project2_SH.ipynb              # Full analysis notebook
├── app.py                         # API-powered Streamlit dashboard
├── dashboard/app.py               # Artifact-based dashboard
├── src/
│   ├── validate_forecast.py      # SARIMA validation script
│   └── build_dashboard_artifacts.py
├── data/processed/                # Parquet artifacts
├── docs/
│   ├── performance_report.md     # Model validation results
│   ├── resume_bullets.md         # Portfolio-ready claims
│   └── interview_talking_points.md
└── requirements.txt
```



### Key Findings

#### 1. Forecasting Performance

**SARIMA model achieves 3.78% MAPE on 6-month test set**, reducing forecast error by 78.9% compared to seasonal naive baseline. This validates the model for short-term operational planning.

**Metrics:**
- MAE: 255.7 incidents/month
- RMSE: 333.7 incidents/month
- MAPE: 3.78% (excellent, well below 10% threshold)

#### 2. Citywide Trend

Crime incidents declined 40% post-2020 and stabilized at lower levels through 2025. No evidence of return to pre-pandemic volumes.

#### 3. Neighborhood Concentration

Top 3 neighborhoods (Mission, Tenderloin, SoMa) account for approximately 30% of citywide incidents. Lower-activity areas include Sunset/Parkside, Marina, Seacliff, and Outer Richmond.

#### 4. Temporal Patterns

**Hourly:** Bimodal distribution with peaks at midnight and noon. Quietest period is 4-6 AM.

**Weekly:** Friday shows highest volume, Sunday lowest. Wednesday also elevated.

#### 5. Category Distribution

Larceny/Theft dominates at 40%+ of all incidents, followed by Malicious Mischief and Assault.

#### 6. 2026 Forecast

SARIMA projects 3,900-4,600 incidents per month in early 2026, approximately 41% below pre-2020 averages. Seasonal cycles remain stable.



### Model Validation

The SARIMA forecasting model was validated using train/test split methodology with a 6-month holdout set.

**Performance Metrics:**
- **MAPE:** 3.78%
- **MAE:** 255.7 incidents/month
- **RMSE:** 333.7 incidents/month
- **Baseline (Seasonal Naive) MAPE:** 17.07%
- **Improvement:** 78.9% reduction in MAE vs. baseline

The model achieves excellent forecast accuracy (MAPE < 5%) and significantly outperforms the seasonal naive baseline. This validates its use for short-term planning.

**Documentation:**
- Detailed metrics: `docs/performance_report.md`
- Resume bullets: `docs/resume_bullets.md`
- Interview prep: `docs/interview_talking_points.md`
- Validation script: `src/validate_forecast.py`

---

## How to Run This Project

### 1. Environment Setup

```bash
# Activate conda environment
conda activate py313

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import statsmodels, sklearn; print('✓ Dependencies OK')"
```

### 2. Run Model Validation

```bash
# Generate performance metrics
python src/validate_forecast.py

# Creates:
# - docs/performance_report.md
# - docs/resume_bullets.md
```

```bash
# Launch Jupyter
jupyter notebook

# Open project2_SH.ipynb and run all cells
```

### 4. Run the Dashboard
```bash
# Option A: API-powered dashboard (live data)
streamlit run app.py

# Option B: Artifact-based dashboard (precomputed)
streamlit run dashboard/app.py
```

### 5. View Documentation

- Performance report: `docs/performance_report.md`
- Resume bullets: `docs/resume_bullets.md`
- Interview prep: `docs/interview_talking_points.md`
- Project audit: `docs/project_audit.md`

---

## Skills Demonstrated

### Technical Skills
- **Time-Series Forecasting:** SARIMA modeling (3.78% MAPE, 78.9% improvement over baseline)
- **Model Validation:** Train/test split, MAE/RMSE/MAPE metrics, baseline comparison
- **Data Engineering:** ETL pipeline processing 1M+ records, API integration, parquet artifacts
- **Visualization:** Plotly interactive charts, Streamlit dashboards
- **Python:** Pandas, NumPy, Statsmodels, Scikit-learn, Streamlit, Plotly

### Analytical Skills
- Geospatial analysis across 41 neighborhoods
- Temporal pattern recognition (hourly, weekly, monthly)
- Trend analysis (40% post-2020 decline)
- Category-level profiling

### Software Engineering
- Modular code structure with src/ organization
- Dual-dashboard architecture (API + artifacts)
- Error handling and data validation
- Performance optimization (caching, chunked API calls)
- Reproducible validation pipeline

---

## Troubleshooting

### Common Issues

**ModuleNotFoundError: No module named 'statsmodels'**

```bash
conda activate py313
pip install -r requirements.txt
```

**FileNotFoundError: Missing data/processed/monthly_citywide.parquet**

Run the data processing pipeline to generate artifacts. Verify that `data/processed/` contains the required parquet files.

**Dashboard won't start**

Ensure you're in the project root directory and the correct conda environment is activated.

---

## Author

**Sileshi Hirpa**

Portfolio project demonstrating time-series forecasting, geospatial analysis, and interactive dashboard development.

---

## License

This project uses publicly available data from the DataSF Open Data Portal. The code and analysis are provided for portfolio and educational purposes.
