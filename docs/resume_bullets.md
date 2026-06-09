# Resume Bullets - SF Crime Analytics Project

**Generated:** 2026-06-08 23:44:35  
**Source:** Validated metrics from SARIMA forecast evaluation

---

## ✅ Quantitatively Supported Bullets

### Forecasting & Modeling

1. **"Developed SARIMA time-series forecasting model achieving 3.8% MAPE on 6-month test set, outperforming seasonal naive baseline by 78.9%"**
   - Skills: Time-series analysis, SARIMA, model validation
   - Metrics: MAPE, MAE improvement
   - Evidence: docs/performance_report.md

2. **"Validated predictive model using train/test split methodology, achieving MAE of 256 incidents/month (RMSE: 334) on held-out data"**
   - Skills: Model validation, statistical testing
   - Metrics: MAE, RMSE
   - Evidence: docs/performance_report.md

3. **"Implemented seasonal ARIMA model with 12-month periodicity, generating 6-month crime forecasts with confidence intervals for operational planning"**
   - Skills: Seasonal decomposition, uncertainty quantification
   - Technical: SARIMA(1,1,1)(1,1,1,12)
   - Evidence: app.py, dashboard/app.py

### Data Engineering & Pipeline

4. **"Engineered end-to-end crime analytics pipeline processing 1M+ SFPD incidents (2018-2025) using Python, Pandas, and Plotly, deployed via Streamlit dashboard with real-time API integration"**
   - Skills: Python, Pandas, Plotly, Streamlit, API integration
   - Scale: 1M+ records
   - Evidence: app.py, src/build_dashboard_artifacts.py

5. **"Built dual-dashboard architecture (API-powered + artifact-based) with 24-hour caching, dynamic filtering, and CSV export functionality"**
   - Skills: System design, caching, performance optimization
   - Technical: Parquet artifacts, API chunking
   - Evidence: app.py, dashboard/app.py

### Analysis & Insights

6. **"Conducted geospatial and temporal analysis across 41 SF neighborhoods, identifying top 3 hotspots (Mission, Tenderloin, SoMa) representing 30% of citywide incidents"**
   - Skills: Geospatial analysis, data aggregation
   - Insight: Actionable hotspot identification
   - Evidence: README.md, project2_SH.ipynb

7. **"Analyzed 8-year crime dataset revealing 40% post-2020 decline and bimodal hourly pattern (midnight/noon peaks) across all neighborhoods"**
   - Skills: Trend analysis, pattern recognition
   - Insight: Temporal crime dynamics
   - Evidence: README.md, app.py

8. **"Designed interactive dashboard with hour×weekday heatmaps and neighborhood drill-down, enabling stakeholders to explore crime patterns across 41 analysis zones"**
   - Skills: Dashboard design, data visualization, UX
   - Impact: Stakeholder enablement
   - Evidence: app.py, dashboard/app.py

---

## 📊 Key Metrics Summary

| Category | Metric | Value |
|----------|--------|-------|
| **Forecast Accuracy** | MAPE | 3.78% |
| **Forecast Accuracy** | MAE | 256 incidents/month |
| **Forecast Accuracy** | RMSE | 334 incidents/month |
| **Model Improvement** | vs. Baseline (MAE) | 78.9% better |
| **Model Improvement** | vs. Baseline (MAPE) | 77.8% better |
| **Data Scale** | Total Incidents | 1M+ (2018-2025) |
| **Data Scale** | Neighborhoods | 41 analysis zones |
| **Data Scale** | Time Span | 8 years |

---

## 🎯 Recommended Resume Formats

### For Data Scientist Roles

**San Francisco Crime Analytics & Forecasting**  
*Python, SARIMA, Streamlit, Pandas, Plotly*

- Developed SARIMA time-series model achieving 3.8% MAPE, outperforming seasonal naive baseline by 78.9%
- Engineered end-to-end pipeline processing 1M+ SFPD incidents with dual-dashboard architecture (API + artifacts)
- Identified top 3 crime hotspots accounting for 30% of citywide incidents through geospatial analysis

### For Data Analyst Roles

**SF Crime Analytics Dashboard (2018-2025)**  
*Streamlit, Python, Plotly, API Integration*

- Built interactive dashboard analyzing 1M+ crime incidents across 41 neighborhoods with real-time API integration
- Discovered 40% post-2020 crime decline and bimodal hourly patterns through temporal analysis
- Designed hour×weekday heatmaps and neighborhood drill-down enabling data-driven resource allocation

### For ML Engineer Roles

**Time-Series Forecasting Pipeline**  
*SARIMA, Python, Statsmodels, Model Validation*

- Implemented SARIMA forecasting model with train/test validation achieving MAE of 256 incidents/month
- Designed dual-dashboard system with 24-hour caching and precomputed parquet artifacts for performance
- Validated model against seasonal naive baseline, demonstrating 78.9% improvement in forecast accuracy

---

## ❌ Do NOT Claim (Unsupported)

1. ❌ "Reduced crime by X%" - Descriptive analysis, not causal intervention
2. ❌ "Optimized patrol allocation" - No optimization algorithm implemented
3. ❌ "Saved $X in costs" - No cost-benefit analysis performed
4. ❌ "Achieved 95% accuracy" - Classification accuracy not applicable to time-series forecasting
5. ❌ "Deployed to production" - Portfolio project, not production system
6. ❌ "Real-time predictions" - Dashboard uses precomputed forecasts, not real-time model inference
7. ❌ "Prevented X incidents" - No causal impact evaluation performed

**What you CAN claim:**
- ✅ 3.78% MAPE on test set
- ✅ 78.9% improvement over baseline
- ✅ Processed 1M+ incidents
- ✅ Built dual-dashboard architecture
- ✅ Validated with train/test split
- ✅ Identified top 3 hotspots (30% of incidents)

---

## 📝 LinkedIn Summary Snippet

"Developed a time-series forecasting system for San Francisco crime data, achieving 3.8% MAPE and 78.9% improvement over baseline. Built dual-dashboard architecture processing 1M+ incidents with interactive visualizations across 41 neighborhoods. Technologies: Python, SARIMA, Streamlit, Plotly, Pandas."

---

## 🎤 Interview Talking Points

1. **Model Selection:** "I chose SARIMA because SF crime data exhibits strong 12-month seasonality. The model captures both trend and seasonal components."

2. **Validation Approach:** "I used a 6-month held-out test set and compared against a seasonal naive baseline to ensure the model adds value."

3. **Performance:** "The model achieved 3.8% MAPE, which is 78.9% better than simply using last year's values."

4. **Business Impact:** "The forecast enables SFPD to anticipate resource needs 3-6 months ahead, supporting data-driven staffing decisions."

5. **Limitations:** "The 2020 structural break limits long-term forecasting. I recommend quarterly retraining to adapt to evolving patterns."

---

## 📚 Technical Deep-Dive Points

- **Why SARIMA?** Handles both trend and seasonality; interpretable; standard in time-series forecasting
- **Why (1,1,1)(1,1,1,12)?** Balances model complexity with interpretability; 12-month seasonal cycle
- **Why 6-month test?** Sufficient for validation while preserving training data; aligns with operational planning horizon
- **Why seasonal naive baseline?** Industry-standard baseline for seasonal data; represents "do nothing" approach
- **Model limitations:** Assumes linear relationships; sensitive to structural breaks; no external regressors

---

*All metrics in this document are computed from actual model validation and can be reproduced by running `python src/validate_forecast.py`.*
