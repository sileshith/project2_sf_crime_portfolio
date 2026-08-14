import numpy as np
import pandas as pd
import pytest

from sf_incidents.forecasting import seasonal_naive, validate_monthly_series


def test_seasonal_naive_repeats_last_year():
    index = pd.date_range("2023-01-01", periods=24, freq="MS")
    series = pd.Series(np.arange(24), index=index)
    forecast = seasonal_naive(series, 3).forecast
    assert forecast.tolist() == [12.0, 13.0, 14.0]


def test_monthly_validation_rejects_gaps():
    series = pd.Series([10, 11], index=pd.to_datetime(["2024-01-01", "2024-03-01"]))
    with pytest.raises(ValueError, match="missing periods"):
        validate_monthly_series(series)
