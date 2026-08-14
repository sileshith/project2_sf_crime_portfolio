# Forecast model card

**Generated:** 2026-08-14  
**Target:** Monthly citywide count of reported SFPD incidents  
**Evaluation window:** 2025-04 through 2025-12

## Intended use

This is a portfolio demonstration of aggregate time-series forecasting. It may provide
directional context for short-horizon planning, but it is not a public-safety risk score,
causal model, patrol-allocation system, or estimate of unreported crime.

## Evaluation design

- Expanding-window rolling-origin backtest with 6 forecast origins.
- Three-month forecast at every origin.
- Models compared: seasonal naive, additive Holt-Winters ETS, and SARIMA(1,1,1)(1,1,1,12).
- Selection metric: mean absolute scaled error (MASE), with MAE, RMSE, MAPE, and WAPE reported.
- All model selection occurs on historical backtest folds. The final forecast is then refit
  using the complete 2018–2025 monthly series.

## Backtest results

| Model | MAE | RMSE | MAPE | WAPE | MASE |
| --- | ---: | ---: | ---: | ---: | ---: |
| sarima | 432.24 | 482.39 | 5.78 | 5.76 | 0.80 |
| ets | 433.60 | 490.32 | 5.81 | 5.78 | 0.81 |
| seasonal_naive | 1062.50 | 1113.31 | 14.14 | 14.12 | 1.97 |

The lowest mean MASE was produced by **sarima** (0.80). Metrics
summarize several forecast origins and should not be interpreted as guaranteed future accuracy.

## Limitations

1. Recorded incidents reflect reporting, enforcement, classification, and source-system changes.
2. The pandemic period is a major structural break.
3. Aggregate citywide forecasts do not describe neighborhood-level or individual risk.
4. No weather, event, economic, policy, or reporting-delay variables are included.
5. Prediction intervals are model-based and require continued calibration monitoring.

## Monitoring recommendation

Re-run the backtest when new complete months arrive, compare against the seasonal-naive
baseline, track error by horizon, and investigate material data revisions before retraining.
