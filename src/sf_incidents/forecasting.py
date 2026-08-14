from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.statespace.sarimax import SARIMAX


@dataclass(frozen=True)
class ForecastResult:
    model: str
    forecast: pd.Series
    lower: pd.Series | None = None
    upper: pd.Series | None = None


def seasonal_naive(train: pd.Series, horizon: int) -> ForecastResult:
    if len(train) < 12:
        raise ValueError("Seasonal naive requires at least 12 monthly observations")
    values = np.resize(train.iloc[-12:].to_numpy(), horizon)
    index = pd.date_range(train.index[-1] + pd.offsets.MonthBegin(), periods=horizon, freq="MS")
    return ForecastResult("seasonal_naive", pd.Series(values, index=index, dtype=float))


def ets(train: pd.Series, horizon: int) -> ForecastResult:
    fitted = ExponentialSmoothing(
        train, trend="add", seasonal="add", seasonal_periods=12, initialization_method="estimated"
    ).fit(optimized=True)
    index = pd.date_range(train.index[-1] + pd.offsets.MonthBegin(), periods=horizon, freq="MS")
    return ForecastResult("ets", pd.Series(fitted.forecast(horizon).to_numpy(), index=index))


def sarima(train: pd.Series, horizon: int) -> ForecastResult:
    fitted = SARIMAX(
        train,
        order=(1, 1, 1),
        seasonal_order=(1, 1, 1, 12),
        enforce_stationarity=False,
        enforce_invertibility=False,
    ).fit(disp=False)
    prediction = fitted.get_forecast(horizon)
    interval = prediction.conf_int(alpha=0.05)
    index = pd.date_range(train.index[-1] + pd.offsets.MonthBegin(), periods=horizon, freq="MS")
    return ForecastResult(
        "sarima",
        pd.Series(prediction.predicted_mean.to_numpy(), index=index),
        pd.Series(interval.iloc[:, 0].to_numpy(), index=index),
        pd.Series(interval.iloc[:, 1].to_numpy(), index=index),
    )


MODELS = {"seasonal_naive": seasonal_naive, "ets": ets, "sarima": sarima}


def validate_monthly_series(series: pd.Series) -> pd.Series:
    result = series.copy()
    result.index = pd.DatetimeIndex(result.index).to_period("M").to_timestamp()
    result = result.sort_index().astype(float)
    expected = pd.date_range(result.index.min(), result.index.max(), freq="MS")
    if not result.index.equals(expected):
        missing = expected.difference(result.index)
        raise ValueError(
            f"Monthly series has missing periods: {missing.strftime('%Y-%m').tolist()}"
        )
    if (result <= 0).any():
        raise ValueError("Monthly incident counts must be positive")
    return result
