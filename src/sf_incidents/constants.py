from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
PROCESSED_DIR = DATA_DIR / "processed"
DOCS_DIR = ROOT / "docs"

DATASET_ID = "wg3w-h783"
API_URL = f"https://data.sfgov.org/resource/{DATASET_ID}.json"
START_DATE = "2018-01-01T00:00:00.000"
END_DATE = "2025-12-31T23:59:59.999"

WEEKDAY_ORDER = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]
