# Interview Talking Points - SF Crime Analytics Project

**Author:** Sileshi Hirpa  
**Project:** San Francisco Crime Analytics (2018-2025)  
**Model:** SARIMA Time-Series Forecasting

---

## Executive Summary

This project analyzes 1M+ SFPD incident reports from 2018-2025 using time-series forecasting, geospatial analysis, and interactive dashboards. The SARIMA model achieves 3.78% MAPE on a 6-month holdout set, reducing forecast error by 78.9% compared to a seasonal naive baseline.

**Key Achievement:** Rigorous model validation with train/test split and baseline comparison, demonstrating measurable improvement in forecast accuracy.

---

## Business Problem

**Question:** "What problem were you trying to solve?"

**Answer:**

"I wanted to build a forecasting system that could help understand crime patterns in San Francisco and provide short-term projections for operational planning. The goal was to identify which neighborhoods and time periods see the most incidents, and to create a validated forecasting model that outperforms simple baselines."

**Key Points:**
- Understand spatial and temporal crime patterns
- Build validated forecasting model for 3-6 month planning
- Create interactive tools for exploring the data
- Demonstrate measurable improvement over naive approaches

---

## Dataset Scale

**Question:** "Tell me about the data you worked with."

**Answer:**

"I worked with over 1 million SFPD incident reports from 2018 to 2025, sourced from the DataSF Open Data Portal. The data covers 41 official analysis neighborhoods and includes 30+ incident categories. I processed this into monthly aggregates for citywide forecasting and built hourly-weekday patterns for temporal analysis."

**Key Points:**
- 1M+ records from DataSF API
- 8-year time span (2018-2025)
- 41 neighborhoods (official SFPD zones)
- 30+ incident categories
- Multiple aggregation levels (monthly, hourly, neighborhood)

---

## Why SARIMA Was Selected

**Question:** "Why did you choose SARIMA for this problem?"

**Answer:**

"San Francisco crime data exhibits strong 12-month seasonality. You see consistent patterns like higher incidents in summer and lower in winter. SARIMA is designed to handle both trend and seasonal components, making it well-suited for this type of data. It's also interpretable and widely used in operational forecasting, which makes it easier to explain to stakeholders."

**Key Points:**
- Strong 12-month seasonality in the data
- SARIMA handles trend + seasonal components
- Interpretable model (not a black box)
- Standard approach for time-series forecasting
- Balances accuracy with explainability

**Technical Detail:**
- SARIMA(1,1,1)(1,1,1,12)
- Non-seasonal: AR(1), I(1), MA(1)
- Seasonal: SAR(1), SI(1), SMA(1) with 12-month cycle

---

## Validation Methodology

**Question:** "How did you validate your model?"

**Answer:**

"I used a train/test split with a 6-month holdout set. I trained the model on 90 months of data (2018-01 to 2025-06) and tested on the final 6 months (2025-07 to 2025-12). I also compared against a seasonal naive baseline, which just uses the value from the same month last year. This is standard practice for time-series validation."

**Key Points:**
- Train/test split (90 months train, 6 months test)
- Held-out test set (not used during training)
- Baseline comparison (seasonal naive)
- Standard metrics: MAE, RMSE, MAPE
- No data leakage

**Why 6 months?**
- Sufficient for validation
- Aligns with operational planning horizon (3-6 months)
- Preserves enough training data

---

## Interpretation of 3.78% MAPE

**Question:** "What does 3.78% MAPE mean in practical terms?"

**Answer:**

"MAPE stands for Mean Absolute Percentage Error. A MAPE of 3.78% means that on average, my forecasts are within 3.78% of the actual values. In forecasting, anything under 10% is considered excellent. So 3.78% indicates the model is highly accurate and suitable for operational planning."

**Key Points:**
- MAPE < 10% = excellent forecast
- MAPE < 20% = good forecast
- 3.78% is well below the excellent threshold
- Predictions typically within 4% of actual values

**Example:**
- If actual incidents = 7,000
- 3.78% error = ±265 incidents
- Forecast range: 6,735 - 7,265

---

## Interpretation of 255.7 MAE

**Question:** "What does MAE of 255.7 incidents/month mean?"

**Answer:**

"MAE is Mean Absolute Error. It means that on average, my forecast is off by about 256 incidents per month. Given that San Francisco sees around 6,000-7,500 incidents per month in recent years, this represents about 3-4% error, which aligns with the MAPE. It's a concrete measure of forecast accuracy in the original units."

**Key Points:**
- MAE = average absolute error
- 256 incidents/month average error
- Context: ~6,000-7,500 incidents/month citywide
- Represents ~3-4% of monthly volume
- Easy to interpret (same units as data)

---

## Interpretation of 78.9% MAE Improvement

**Question:** "You mention 78.9% improvement over baseline. What does that mean?"

**Answer:**

"I compared my SARIMA model against a seasonal naive baseline, which just uses the value from the same month last year. The baseline had an MAE of 1,211 incidents/month, while SARIMA achieved 256 incidents/month. That's a 78.9% reduction in forecast error. It shows the model adds real value compared to a simple approach."

**Key Points:**
- Baseline MAE: 1,211 incidents/month
- SARIMA MAE: 256 incidents/month
- Improvement: (1211 - 256) / 1211 = 78.9%
- Demonstrates model adds measurable value
- Not just better than random, better than a reasonable baseline

**Why this matters:**
- Proves the model isn't just overfitting
- Shows improvement over "do nothing" approach
- Validates the complexity is justified

---

## Model Strengths

**Question:** "What are the strengths of your approach?"

**Answer:**

"First, the model is rigorously validated with a held-out test set and baseline comparison. Second, it achieves excellent accuracy with MAPE under 4%. Third, it's interpretable, so stakeholders can understand how it works. Fourth, I built dual dashboards for both technical and non-technical users. And fifth, all the code is reproducible with clear documentation."

**Key Strengths:**
1. **Rigorous validation:** Train/test split, baseline comparison
2. **Excellent accuracy:** 3.78% MAPE, well below 10% threshold
3. **Interpretable:** SARIMA is explainable, not a black box
4. **Dual dashboards:** API-powered + artifact-based
5. **Reproducible:** Clear documentation, validation script
6. **Scalable:** Handles 1M+ records efficiently

---

## Model Limitations

**Question:** "What are the limitations of your model?"

**Answer:**

"The main limitation is the 2020 structural break from the pandemic. Crime patterns changed significantly, so the model may not generalize well to future structural shifts. Also, I only tested one SARIMA configuration. Grid search could potentially improve performance. The model also doesn't account for external factors like policy changes or economic conditions. And the 6-month test window is relatively short for long-term validation."

**Key Limitations:**
1. **Structural breaks:** 2020 pandemic caused regime shift
2. **Single configuration:** Only tested (1,1,1)(1,1,1,12)
3. **No external regressors:** Doesn't use policy, economic data
4. **Short test window:** 6 months is limited for long-term validation
5. **Linear assumptions:** SARIMA assumes linear relationships

**Mitigation:**
- Recommend quarterly retraining
- Monitor forecast accuracy over time
- Present forecasts with confidence intervals
- Continue baseline comparison

---

## What I Would Improve Next

**Question:** "If you had more time, what would you improve?"

**Answer:**

"First, I'd implement grid search to optimize the SARIMA hyperparameters. Second, I'd add longer-term backtesting with multiple test windows. Third, I'd explore ensemble methods, maybe combining SARIMA with Prophet or exponential smoothing. Fourth, I'd add external regressors like weather or economic indicators. And fifth, I'd build automated retraining and monitoring pipelines."

**Improvement Priorities:**

1. **Grid search:** Optimize (p,d,q) and (P,D,Q,s) parameters
2. **Longer backtesting:** Multiple test windows, cross-validation
3. **Ensemble methods:** Combine SARIMA + Prophet + ETS
4. **External regressors:** Weather, events, economic data
5. **Automated pipeline:** Retraining, monitoring, alerting
6. **Anomaly detection:** Flag unusual patterns
7. **Neighborhood-level forecasts:** Not just citywide

---

## Common Hiring Manager Questions

### "Walk me through your project."

**Answer:**

"I built an end-to-end crime analytics system for San Francisco using 1M+ SFPD incident reports. I started with data cleaning and exploratory analysis to understand patterns. Then I built a SARIMA forecasting model that achieves 3.78% MAPE, which is 78.9% better than a seasonal naive baseline. I validated this with a 6-month holdout set. Finally, I created dual dashboards for interactive exploration. The whole project is reproducible with clear documentation."

---

### "What was the biggest challenge?"

**Answer:**

"The biggest challenge was handling the 2020 structural break. Crime patterns changed dramatically during the pandemic and haven't returned to pre-2020 levels. This makes long-term forecasting difficult because the model is trained on data that includes this regime shift. I addressed this by focusing on short-term forecasts (3-6 months) and recommending quarterly retraining to adapt to evolving patterns."

---

### "How would you deploy this in production?"

**Answer:**

"I'd set up an automated pipeline that retrains the model monthly using the latest data. I'd implement monitoring to track forecast accuracy and alert if performance degrades. I'd also add A/B testing to compare new model versions against the current production model. For serving, I'd precompute forecasts and store them in a database, then expose them via an API. And I'd build dashboards for both technical monitoring and business stakeholders."

**Production Components:**
- Automated retraining pipeline (monthly)
- Performance monitoring and alerting
- A/B testing framework
- Forecast storage (database)
- API for serving predictions
- Monitoring dashboards

---

### "How do you know your model is working?"

**Answer:**

"I validate the model in three ways. First, I use a held-out test set that the model never sees during training. Second, I compare against a seasonal naive baseline to ensure I'm adding value. Third, I track standard metrics like MAE, RMSE, and MAPE. The model achieves 3.78% MAPE and 78.9% improvement over baseline, which demonstrates it's working well. In production, I'd continue monitoring these metrics as new data arrives."

---

### "What would you do differently?"

**Answer:**

"I'd spend more time on hyperparameter tuning with grid search. I only tested one SARIMA configuration, and there's likely room for improvement. I'd also implement longer backtesting with multiple test windows to better understand model stability. And I'd explore ensemble methods to combine SARIMA with other approaches like Prophet or exponential smoothing."

---

### "How does this relate to business value?"

**Answer:**

"The forecast enables operational planning with high confidence. With MAPE under 4%, stakeholders can use these projections for resource allocation decisions. For example, if the model predicts higher incident volume in certain neighborhoods or time periods, that information can inform staffing and deployment. The key is that the model is validated and measurably better than simple baselines."

---

## Technical Deep Dives

### SARIMA Specification

**SARIMA(1,1,1)(1,1,1,12)**

**Non-seasonal components:**
- AR(1): Autoregressive order 1
- I(1): First-order differencing
- MA(1): Moving average order 1

**Seasonal components (12-month cycle):**
- SAR(1): Seasonal autoregressive order 1
- SI(1): Seasonal differencing order 1
- SMA(1): Seasonal moving average order 1

**Why this configuration?**
- Balances model complexity with interpretability
- 12-month cycle captures annual seasonality
- (1,1,1) is a common starting point for ARIMA

---

### Baseline Comparison

**Why seasonal naive?**
- Standard baseline for seasonal data
- Represents "do nothing" approach
- Easy to implement and interpret
- Provides meaningful comparison point

**Baseline performance:**
- MAE: 1,210.8 incidents/month
- RMSE: 1,260.6 incidents/month
- MAPE: 17.07%

**SARIMA performance:**
- MAE: 255.7 incidents/month (78.9% better)
- RMSE: 333.7 incidents/month (73.5% better)
- MAPE: 3.78% (77.8% better)

---

### Data Engineering

**Pipeline components:**
1. API integration (DataSF)
2. Data cleaning and validation
3. Feature engineering (month, hour, weekday)
4. Aggregation (monthly, hourly, neighborhood)
5. Parquet artifact generation
6. Dashboard deployment

**Performance optimizations:**
- Chunked API calls (50k records per chunk)
- 24-hour caching
- Precomputed parquet artifacts
- Dual dashboard architecture

---

## Closing Thoughts

**What makes this project strong:**

1. **Validated metrics:** All claims backed by actual test set performance
2. **Baseline comparison:** Demonstrates measurable improvement
3. **Reproducible:** Clear documentation, validation script
4. **Professional quality:** Portfolio-ready code and documentation
5. **Practical focus:** Addresses real operational planning needs

**What to emphasize in interviews:**

- 3.78% MAPE (excellent accuracy)
- 78.9% improvement over baseline (measurable value)
- Rigorous validation (train/test split)
- End-to-end pipeline (data → model → dashboard)
- Reproducible and well-documented

---

*All metrics are computed from actual model validation and can be reproduced by running `python src/validate_forecast.py`.*
