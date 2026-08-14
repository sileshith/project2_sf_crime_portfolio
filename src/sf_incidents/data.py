from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd
import requests

from .constants import API_URL, END_DATE, START_DATE

LOGGER = logging.getLogger(__name__)

CANONICAL_COLUMNS = [
    "incident_datetime",
    "incident_category",
    "neighborhood",
    "weekday",
    "latitude",
    "longitude",
]


def _canonicalize(frame: pd.DataFrame) -> pd.DataFrame:
    # Prefer the source-system timestamp when a cleaned export also contains a derived copy.
    if "Incident Datetime" in frame.columns:
        frame = frame.copy()
        frame["incident_datetime"] = frame["Incident Datetime"]
    aliases = {
        "category": "incident_category",
        "analysis_neighborhood": "neighborhood",
        "weekday_name": "weekday",
        "incident_day_of_week": "weekday",
    }
    frame = frame.rename(columns={k: v for k, v in aliases.items() if k in frame.columns})
    duplicated = frame.columns[frame.columns.duplicated()].tolist()
    if duplicated:
        frame = frame.loc[:, ~frame.columns.duplicated(keep="last")]
    missing = sorted(set(CANONICAL_COLUMNS[:4]) - set(frame.columns))
    if missing:
        raise ValueError(f"Source data is missing required columns: {missing}")

    result = frame.copy()
    result["incident_datetime"] = pd.to_datetime(
        result["incident_datetime"], errors="coerce", format="mixed"
    )
    for column in ("latitude", "longitude"):
        if column not in result:
            result[column] = pd.NA
        result[column] = pd.to_numeric(result[column], errors="coerce")
    result = result.dropna(
        subset=["incident_datetime", "incident_category", "neighborhood", "weekday"]
    )
    result = result[
        result["incident_datetime"].between(
            pd.Timestamp("2018-01-01"), pd.Timestamp("2025-12-31 23:59:59")
        )
    ]
    result["incident_category"] = result["incident_category"].astype("string").str.strip()
    result["neighborhood"] = result["neighborhood"].astype("string").str.strip()
    result["weekday"] = result["weekday"].astype("string").str.strip()
    return result[CANONICAL_COLUMNS].sort_values("incident_datetime").reset_index(drop=True)


def load_local(path: str | Path) -> pd.DataFrame:
    """Load a CSV or Parquet source and return the canonical incident schema."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)
    LOGGER.info("Loading local source %s", path)
    if path.suffix.lower() == ".parquet":
        frame = pd.read_parquet(path)
    elif path.suffix.lower() == ".csv":
        frame = pd.read_csv(path, low_memory=False)
    else:
        raise ValueError("Source must be a .csv or .parquet file")
    return _canonicalize(frame)


def fetch_datasf(page_size: int = 50_000, session: requests.Session | None = None) -> pd.DataFrame:
    """Download the complete study window with deterministic Socrata pagination."""
    client = session or requests.Session()
    select = ",".join(
        [
            "incident_datetime",
            "incident_category",
            "analysis_neighborhood",
            "incident_day_of_week",
            "latitude",
            "longitude",
            ":id",
        ]
    )
    where = f"incident_datetime between '{START_DATE}' and '{END_DATE}'"
    chunks: list[pd.DataFrame] = []
    offset = 0
    while True:
        params = {
            "$select": select,
            "$where": where,
            "$order": "incident_datetime, :id",
            "$limit": page_size,
            "$offset": offset,
        }
        response = client.get(API_URL, params=params, timeout=120)
        response.raise_for_status()
        chunk = pd.DataFrame(response.json())
        if chunk.empty:
            break
        chunks.append(chunk)
        downloaded = sum(len(item) for item in chunks)
        LOGGER.info("Downloaded %s rows", f"{downloaded:,}")
        if len(chunk) < page_size:
            break
        offset += page_size
    if not chunks:
        raise RuntimeError("DataSF returned no records for the configured study window")
    return _canonicalize(pd.concat(chunks, ignore_index=True))
