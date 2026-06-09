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
Forecasting, Neighborhood Patterns, and Patrol Optimization Using Python
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
<strong>Course:</strong> DAT 301 (Exploring Data in R & Python)<br>
<strong>Project:</strong> Project 2 (Python)<br>
<strong>Professor:</strong> Dr. Neha Joshi (PhD)<br>
<strong>Data Source:</strong> SFPD Incident Reports (DataSF)<br>
<strong>Time Window:</strong> 2018-2025
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
Arizona State University • December 2025
</div>
</div>
<div style="text-align: center; font-size: 12px; color: gray; margin-top: 6px;">
Cover Image Source: Britannica - “Golden Gate Bridge”
</div>



## San Francisco Crime Analytics (2018-2025)

A structured, end-to-end analysis of nearly one million SFPD incident reports, covering **data cleaning, exploratory visualization, geospatial patterns, time-series forecasting, and an interactive Streamlit dashboard.** This project demonstrates practical analytical workflow skills aligned with business analytics and data science roles.



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
│  
 ├── project2_SH.ipynb # Full analysis notebook   
 ├── project2_SH.html # HTML export   
 ├── app.py # Streamlit dashboar    
├── goldenGatebrge.png # Cover image    
├── dashboard_charts/ # Dashboard snapshot assets   
└── Police_Department_Incident_Reports__2018_to_20251121.csv   



### Analytical Summary

#### 1. Citywide Trend (2018-2025)

Incident volume declines significantly beginning in 2020 and stabilizes at lower levels through 2024–2025 due to:
- Hybrid and remote work
- Fewer commuters in downtown areas
- Changing tourism patterns
- Targeted safety initiatives

San Francisco appears to have settled into a **post-2020 baseline**.

#### 2. Neighborhood Hotspots

Consistently high-activity neighborhoods include:
1. Mission
2. Tenderloin
3. South of Market (SoMa)
4. Financial District / South Beach
5. Bayview-Hunters Point

Lower-activity residential regions include Sunset/Parkside, Marina, Seacliff, Outer Richmond.

#### 3. Leading Crime Categories

Top categories across years:
- **Larceny/Theft**
- **Malicious Mischief**
- **Assault**
- **Other Miscellaneous**
- **Motor Vehicle Theft**
- **Burglary**

These categories define the city's crime signature.

### 4. Daily and Weekly Patterns

##### Hourly
- Quietest: **4-6 AM**
- Midday peak: **12-3 PM**
- Evening plateau: **3-7 PM**
- Weekend nightlife spike: **12-3 AM**

##### Weekly
- Highest: **Wednesday & Friday**
- Lowest: **Sunday**

#### 5. Neighborhood Crime Profiles
- **Theft-heavy areas:** Financial District, South Beach, Union Square, SoMa
- **Vehicle-crime clusters:** Mission, Tenderloin, Bayview
- **Lower-risk residential:** Sunset, Richmond, Marina

#### 6. Forecasting Early 2026 (SARIMA)

SARIMA projections estimate:
- **3,900-4,600 incidents per month** early in 2026
- Levels remain **~41% below** pre-2020 averages
- Seasonal cycles remain stable
- No evidence of return to pre-pandemic highs

#### 7. Dashboard Highlights

**Full Local Dashboard**
Includes:
- Spatial heatmaps
- Hourly/weekday trends
- Category breakdowns
- Neighborhood comparisons
- Forecast visualization

**API-Based Dashboard**
Includes:
- Dynamic filters
- Real-time updated visuals
- CSV export
- Neighborhood & category exploration


### Key Findings

1. **Forecasting Performance:** SARIMA model achieves 3.78% MAPE on 6-month test set, reducing forecast error by 78.9% compared to seasonal naive baseline.

2. **Citywide Trend:** Crime incidents declined 40% post-2020 and stabilized at lower levels through 2025, with no evidence of return to pre-pandemic volumes.

3. **Neighborhood Concentration:** Top 3 neighborhoods (Mission, Tenderloin, SoMa) account for approximately 30% of citywide incidents.

4. **Temporal Patterns:** Bimodal hourly distribution with peaks at midnight and noon; Friday shows highest weekly volume, Sunday lowest.

5. **Category Distribution:** Larceny/Theft dominates at 40%+ of all incidents, followed by Malicious Mischief and Assault.

---

### Model Validation & Performance

The SARIMA forecasting model has been rigorously validated using train/test split methodology with a 6-month holdout set.

**Key Results:**
- **MAPE:** 3.78% (mean absolute percentage error)
- **MAE:** 255.7 incidents/month (mean absolute error)
- **RMSE:** 333.7 incidents/month (root mean squared error)
- **Improvement vs. Baseline:** 78.9% reduction in MAE compared to seasonal naive forecast

**Model Performance:**
The SARIMA model achieves excellent forecast accuracy with MAPE < 5%, significantly outperforming the seasonal naive baseline (17.07% MAPE). This validates the model's utility for short-term operational planning.

**Documentation:**
- **Detailed Metrics:** `docs/performance_report.md`
- **Resume Bullets:** `docs/resume_bullets.md`
- **Validation Script:** `src/validate_forecast.py`

---

## How to Run This Project

### 1. Run Model Validation (Generate Metrics)
```bash
# Validate SARIMA model and generate performance reports
python src/validate_forecast.py

# This creates:
# - docs/performance_report.md (detailed metrics)
# - docs/resume_bullets.md (resume-ready claims)
```

### 2. Run the Notebook
```bash
# Launch Jupyter Notebook or Lab
jupyter notebook
# or
jupyter lab

# Open project2_SH.ipynb and run all cells
```

### 3. Run the Dashboard
```bash
# Option A: API-powered dashboard (live data)
streamlit run app.py

# Option B: Artifact-based dashboard (precomputed)
streamlit run dashboard/app.py
```

### 4. View Documentation
- **Performance Report:** `docs/performance_report.md`
- **Resume Bullets:** `docs/resume_bullets.md`
- **Project Audit:** `docs/project_audit.md`

---

## Key Skills Demonstrated

### Technical Skills
- **Time-Series Forecasting:** SARIMA modeling achieving 3.78% MAPE with 78.9% improvement over baseline
- **Model Validation:** Train/test split methodology, MAE/RMSE/MAPE metrics, baseline comparison
- **Data Engineering:** ETL pipeline processing 1M+ records, API integration, parquet artifacts
- **Visualization:** Plotly interactive charts, Streamlit dashboards with dual architecture
- **Python Stack:** Pandas, NumPy, Statsmodels, Scikit-learn, Streamlit, Plotly

### Analytical Skills
- Geospatial analysis across 41 neighborhoods identifying top 3 hotspots (30% of incidents)
- Temporal pattern recognition revealing bimodal hourly distribution and weekly cycles
- Trend analysis detecting 40% post-2020 decline in citywide incidents
- Category-level profiling across 8 years of SFPD data

### Software Engineering
- Modular code structure with src/ organization and artifact-based architecture
- Dual-dashboard system (API-powered + precomputed) with 24-hour caching
- Robust error handling and data validation pipelines
- Performance optimization through chunked API calls and parquet storage
- Comprehensive documentation and reproducible validation pipeline

---

## Troubleshooting

### Environment Setup

**Recommended workflow:**
```bash
# 1. Activate the correct environment
conda activate py313

# 2. Navigate to project root
cd /Users/sileshihirpa/Desktop/ASU/projects/san-francisco-crime-forecasting

# 3. Verify dependencies
python -c "import statsmodels, sklearn; print('✓ Dependencies OK')"

# 4. Run validation
python src/validate_forecast.py
```

### Common Issues

**Problem:** `ModuleNotFoundError: No module named 'statsmodels'`

**Solution:**
```bash
conda activate py313
pip install -r requirements.txt
```

**Problem:** `FileNotFoundError: Missing: data/processed/monthly_citywide.parquet`

**Solution:** Ensure you've run the data processing pipeline to generate artifacts. Check that `data/processed/` contains the required parquet files.
