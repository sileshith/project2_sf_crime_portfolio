# SARIMA Forecast Validation Report

**Generated:** 2026-06-08 23:44:35  
**Model:** SARIMA(1,1,1)(1,1,1,12)  
**Dataset:** SF Crime Monthly Citywide Totals (2018-2025)

---

## Executive Summary

This report validates the SARIMA time-series forecasting model used in the SF Crime Analytics dashboard. The model was trained on historical data and evaluated on a held-out test set using standard forecasting metrics.

**Key Finding:** SARIMA outperforms the seasonal naive baseline by **78.9%** (MAE improvement).

---

## Validation Methodology

### Train/Test Split
- **Training Period:** 2018-01 to 2025-06 (90 months)
- **Test Period:** 2025-07 to 2025-12 (6 months)
- **Approach:** Walk-forward validation with fixed test window

### Baseline Model
**Seasonal Naive Forecast:** Uses the value from the same month in the previous year as the prediction. This is a standard baseline for seasonal data and represents the "do nothing" approach.

---

## Performance Metrics

### SARIMA Model Performance

| Metric | Value | Interpretation |
|--------|-------|----------------|
| **MAE** | 255.7 incidents/month | Average absolute error |
| **RMSE** | 333.7 incidents/month | Root mean squared error |
| **MAPE** | 3.78% | Mean absolute percentage error |
| **AIC** | 981.9 | Akaike Information Criterion |
| **BIC** | 992.6 | Bayesian Information Criterion |

### Baseline (Seasonal Naive) Performance

| Metric | Value |
|--------|-------|
| **MAE** | 1210.8 incidents/month |
| **RMSE** | 1260.6 incidents/month |
| **MAPE** | 17.07% |

### Improvement Over Baseline

| Metric | Improvement |
|--------|-------------|
| **MAE Improvement** | 78.9% |
| **RMSE Improvement** | 73.5% |
| **MAPE Improvement** | 77.8% |

---

## Forecast vs. Actual (Test Set)

| Month | Actual | SARIMA Forecast | Baseline Forecast | SARIMA Error | Baseline Error |
|-------|--------|-----------------|-------------------|--------------|----------------|
| 2025-07 | 7453 | 7634 | 9008 | -181 | -1555 |
| 2025-08 | 7573 | 7547 | 8813 | +26 | -1240 |
| 2025-09 | 7265 | 7232 | 8628 | +33 | -1363 |
| 2025-10 | 7602 | 7391 | 8681 | +211 | -1079 |
| 2025-11 | 7043 | 6534 | 7557 | +509 | -514 |
| 2025-12 | 6069 | 6644 | 7583 | -575 | -1514 |

---

## Model Specification

**SARIMA(1,1,1)(1,1,1,12)**

- **Non-seasonal components:**
  - AR(1): Autoregressive order 1
  - I(1): First-order differencing
  - MA(1): Moving average order 1

- **Seasonal components (12-month cycle):**
  - SAR(1): Seasonal autoregressive order 1
  - SI(1): Seasonal differencing order 1
  - SMA(1): Seasonal moving average order 1

- **Constraints:**
  - `enforce_stationarity=False`
  - `enforce_invertibility=False`

---

## Interpretation

### What These Metrics Mean

1. **MAE (255.7):** On average, the SARIMA forecast is off by about 256 incidents per month.

2. **MAPE (3.78%):** The forecast has an average percentage error of 3.8%, meaning predictions are typically within 3.8% of actual values.

3. **Improvement (78.9%):** SARIMA reduces forecast error by 78.9% compared to simply using last year's values.

### Model Quality Assessment

**Excellent** - MAPE < 10% indicates highly accurate forecasts

---

## Limitations

1. **Short Test Window:** 6-month test set provides limited validation. Longer-term backtesting would strengthen confidence.

2. **Single Model:** Only SARIMA(1,1,1)(1,1,1,12) was evaluated. Grid search over hyperparameters could potentially improve performance.

3. **Structural Breaks:** The 2020 pandemic caused a significant regime shift. Model trained on pre-2020 data may not generalize well.

4. **External Factors:** The model does not account for policy changes, economic conditions, or other external drivers of crime.

---

## Recommendations

1. **Deployment:** Model performance is sufficient for short-term (3-6 month) operational planning.

2. **Monitoring:** Retrain model quarterly and monitor forecast accuracy as new data arrives.

3. **Uncertainty:** Always present forecasts with confidence intervals to communicate uncertainty.

4. **Baseline Comparison:** Continue comparing against seasonal naive to ensure model adds value.

---

## Conclusion

The SARIMA model demonstrates **measurable improvement** over the seasonal naive baseline, with {metrics['mae_improvement_pct']:.1f}% lower MAE. This validates the model's utility for short-term crime forecasting in San Francisco.

**Bottom Line:** The model is suitable for inclusion in the dashboard and can support operational planning decisions.
