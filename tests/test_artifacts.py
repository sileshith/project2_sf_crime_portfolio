import hashlib
import json
from pathlib import Path

import pandas as pd

from sf_incidents.artifacts import build_aggregates


def sample_incidents() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "incident_datetime": pd.to_datetime(
                ["2024-01-01 01:00", "2024-01-02 13:00", "2024-02-01 01:00"]
            ),
            "incident_category": ["A", "A", "B"],
            "neighborhood": ["North", "South", "North"],
            "weekday": ["Monday", "Tuesday", "Thursday"],
            "latitude": [37.7, 37.8, 37.7],
            "longitude": [-122.4, -122.5, -122.4],
        }
    )


def test_aggregate_totals_are_conserved():
    artifacts = build_aggregates(sample_incidents())
    assert artifacts["monthly_citywide"]["incidents"].sum() == 3
    assert artifacts["monthly_neighborhood_category"]["incidents"].sum() == 3
    assert artifacts["hourly_weekday_counts"]["incidents"].sum() == 3


def test_monthly_schema():
    monthly = build_aggregates(sample_incidents())["monthly_citywide"]
    assert monthly.columns.tolist() == ["month", "incidents"]
    assert monthly["month"].tolist() == [pd.Timestamp("2024-01-01"), pd.Timestamp("2024-02-01")]


def test_committed_artifact_hashes_match_metadata():
    processed = Path("data/processed")
    metadata = json.loads((processed / "metadata.json").read_text())
    for filename, details in metadata["files"].items():
        digest = hashlib.sha256((processed / filename).read_bytes()).hexdigest()
        assert digest == details["sha256"]
