from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd


def build_aggregates(incidents: pd.DataFrame) -> dict[str, pd.DataFrame]:
    frame = incidents.copy()
    frame["month"] = frame["incident_datetime"].dt.to_period("M").dt.to_timestamp()
    frame["year"] = frame["incident_datetime"].dt.year
    frame["hour"] = frame["incident_datetime"].dt.hour

    monthly_citywide = frame.groupby("month").size().rename("incidents").reset_index()
    monthly_neighborhood_category = (
        frame.groupby(["month", "year", "neighborhood", "incident_category"], observed=True)
        .size()
        .rename("incidents")
        .reset_index()
        .rename(columns={"month": "year_month"})
    )
    hourly_weekday = (
        frame.groupby(["weekday", "hour", "incident_category"], observed=True)
        .size()
        .rename("incidents")
        .reset_index()
        .rename(columns={"weekday": "weekday_label"})
    )
    return {
        "monthly_citywide": monthly_citywide,
        "monthly_neighborhood_category": monthly_neighborhood_category,
        "hourly_weekday_counts": hourly_weekday,
    }


def write_aggregates(
    artifacts: dict[str, pd.DataFrame],
    output_dir: str | Path,
    *,
    source: str,
    source_rows: int,
) -> dict:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    files: dict[str, dict] = {}
    for name, frame in artifacts.items():
        path = output_dir / f"{name}.parquet"
        frame.to_parquet(path, index=False)
        files[path.name] = {
            "rows": len(frame),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        }
    metadata = {
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "source": source,
        "source_rows": source_rows,
        "study_window": ["2018-01-01", "2025-12-31"],
        "files": files,
    }
    (output_dir / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    return metadata
