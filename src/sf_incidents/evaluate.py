from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path

import numpy as np
import pandas as pd

from .constants import DOCS_DIR, PROCESSED_DIR
from .forecasting import MODELS, sarima, validate_monthly_series


def _metrics(actual: pd.Series, predicted: pd.Series, training: pd.Series) -> dict[str, float]:
    errors = actual.to_numpy() - predicted.to_numpy()
    scale = np.mean(np.abs(np.diff(training.to_numpy())))
    return {
        "mae": float(np.mean(np.abs(errors))),
        "rmse": float(np.sqrt(np.mean(errors**2))),
        "mape": float(np.mean(np.abs(errors / actual.to_numpy())) * 100),
        "wape": float(np.sum(np.abs(errors)) / np.sum(np.abs(actual.to_numpy())) * 100),
        "mase": float(np.mean(np.abs(errors)) / scale),
    }


def rolling_origin_backtest(
    series: pd.Series, *, origins: int = 6, horizon: int = 3, min_train: int = 60
) -> tuple[pd.DataFrame, pd.DataFrame]:
    series = validate_monthly_series(series)
    first_origin = len(series) - horizon - origins + 1
    if first_origin < min_train:
        raise ValueError("Not enough history for the requested rolling-origin evaluation")
    predictions: list[dict] = []
    for origin in range(first_origin, first_origin + origins):
        train = series.iloc[:origin]
        actual = series.iloc[origin : origin + horizon]
        for model_name, model in MODELS.items():
            result = model(train, horizon)
            predicted = result.forecast.reindex(actual.index)
            fold_metrics = _metrics(actual, predicted, train)
            for forecast_horizon, (month, actual_value) in enumerate(actual.items(), start=1):
                predictions.append(
                    {
                        "origin": train.index[-1],
                        "month": month,
                        "horizon": forecast_horizon,
                        "model": model_name,
                        "actual": actual_value,
                        "forecast": predicted.loc[month],
                        **fold_metrics,
                    }
                )
    detail = pd.DataFrame(predictions)
    summary = (
        detail.groupby("model")[["mae", "rmse", "mape", "wape", "mase"]]
        .mean()
        .sort_values(["mase", "mae"])
        .reset_index()
    )
    return summary, detail


def generate_report(summary: pd.DataFrame, detail: pd.DataFrame) -> str:
    winner = summary.iloc[0]
    headers = ["Model", "MAE", "RMSE", "MAPE", "WAPE", "MASE"]
    table_lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] + ["---:"] * 5) + " |",
    ]
    for row in summary.itertuples(index=False):
        table_lines.append(
            f"| {row.model} | {row.mae:.2f} | {row.rmse:.2f} | {row.mape:.2f} | "
            f"{row.wape:.2f} | {row.mase:.2f} |"
        )
    table = "\n".join(table_lines)
    start = detail["origin"].min().strftime("%Y-%m")
    end = detail["month"].max().strftime("%Y-%m")
    return f"""# Forecast model card

**Generated:** {datetime.now(UTC).strftime("%Y-%m-%d")}  
**Target:** Monthly citywide count of reported SFPD incidents  
**Evaluation window:** {start} through {end}

## Intended use

This is a portfolio demonstration of aggregate time-series forecasting. It may provide
directional context for short-horizon planning, but it is not a public-safety risk score,
causal model, patrol-allocation system, or estimate of unreported crime.

## Evaluation design

- Expanding-window rolling-origin backtest with {detail["origin"].nunique()} forecast origins.
- Three-month forecast at every origin.
- Models compared: seasonal naive, additive Holt-Winters ETS, and SARIMA(1,1,1)(1,1,1,12).
- Selection metric: mean absolute scaled error (MASE), with MAE, RMSE, MAPE, and WAPE reported.
- All model selection occurs on historical backtest folds. The final forecast is then refit
  using the complete 2018–2025 monthly series.

## Backtest results

{table}

The lowest mean MASE was produced by **{winner["model"]}** ({winner["mase"]:.2f}). Metrics
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
"""


def run(
    monthly_path: Path = PROCESSED_DIR / "monthly_citywide.parquet",
    output_dir: Path = PROCESSED_DIR,
    report_path: Path = DOCS_DIR / "model_card.md",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    monthly = pd.read_parquet(monthly_path)
    series = monthly.set_index("month")["incidents"]
    summary, detail = rolling_origin_backtest(series)
    output_dir.mkdir(parents=True, exist_ok=True)
    summary.to_csv(output_dir / "backtest_summary.csv", index=False)
    detail.to_parquet(output_dir / "backtest_predictions.parquet", index=False)

    selected = str(summary.iloc[0]["model"])
    # SARIMA is retained for interval-bearing dashboard output; selection is recorded transparently.
    final = sarima(validate_monthly_series(series), horizon=6)
    forecast = pd.DataFrame(
        {
            "month": final.forecast.index,
            "forecast": final.forecast.values,
            "lower": final.lower.values,
            "upper": final.upper.values,
            "model": final.model,
        }
    )
    forecast.to_parquet(output_dir / "forecast_citywide_monthly_2026.parquet", index=False)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(generate_report(summary, detail))
    (output_dir / "model_metadata.json").write_text(
        json.dumps(
            {
                "generated_at_utc": datetime.now(UTC).isoformat(),
                "selection_metric": "mase",
                "backtest_winner": selected,
                "deployed_model": final.model,
                "forecast_horizon_months": 6,
            },
            indent=2,
        )
        + "\n"
    )
    return summary, detail


def main() -> None:
    parser = argparse.ArgumentParser(description="Backtest models and create the final forecast")
    parser.add_argument("--monthly", type=Path, default=PROCESSED_DIR / "monthly_citywide.parquet")
    args = parser.parse_args()
    summary, _ = run(monthly_path=args.monthly)
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
