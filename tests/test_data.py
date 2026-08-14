import pandas as pd

from sf_incidents.data import _canonicalize


def test_canonicalize_local_aliases():
    raw = pd.DataFrame(
        {
            "incident_datetime": ["2025-01-01 12:00"],
            "category": ["Assault"],
            "neighborhood": ["Mission"],
            "weekday_name": ["Wednesday"],
            "latitude": ["37.7"],
            "longitude": ["-122.4"],
        }
    )
    result = _canonicalize(raw)
    assert result.columns.tolist() == [
        "incident_datetime",
        "incident_category",
        "neighborhood",
        "weekday",
        "latitude",
        "longitude",
    ]
    assert result.loc[0, "incident_category"] == "Assault"


def test_source_timestamp_wins_over_derived_copy():
    raw = pd.DataFrame(
        {
            "Incident Datetime": ["2025/12/31 11:30:00 PM"],
            "incident_datetime": ["2025-11-01"],
            "category": ["Assault"],
            "neighborhood": ["Mission"],
            "weekday": ["Wednesday"],
        }
    )
    result = _canonicalize(raw)
    assert result.loc[0, "incident_datetime"] == pd.Timestamp("2025-12-31 23:30")
