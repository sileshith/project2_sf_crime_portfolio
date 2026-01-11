# src/build_dashboard_artifacts.py
from pathlib import Path
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data" / "processed"

INCIDENTS_FILE = DATA_DIR / "incidents_clean_2018_2025.parquet"
OUT_MONTHLY_NBH_CAT = DATA_DIR / "monthly_neighborhood_category.parquet"

def main():
    if not INCIDENTS_FILE.exists():
        raise FileNotFoundError(f"Missing: {INCIDENTS_FILE}")

    df = pd.read_parquet(INCIDENTS_FILE)

    required = ["neighborhood", "incident_category", "year"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"incidents_clean is missing required columns: {missing}")

    # Build a reliable monthly time axis
    if "year_month" in df.columns:
        ym = pd.to_datetime(df["year_month"], errors="coerce")
    elif "month" in df.columns:
        ym = pd.to_datetime(df["month"], errors="coerce")
    elif "incident_datetime" in df.columns:
        ym = pd.to_datetime(df["incident_datetime"], errors="coerce").dt.to_period("M").dt.to_timestamp()
    else:
        raise ValueError("Need one of: year_month, month, or incident_datetime to build monthly axis")

    df = df.copy()
    df["year_month"] = ym
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    df = df.dropna(subset=["year_month", "year", "neighborhood", "incident_category"])
    df["year"] = df["year"].astype(int)

    monthly_nbh_cat = (
        df.groupby(["year_month", "year", "neighborhood", "incident_category"], observed=True)
          .size()
          .reset_index(name="incidents")
          .sort_values(["year_month", "neighborhood", "incident_category"])
          .reset_index(drop=True)
    )

    OUT_MONTHLY_NBH_CAT.parent.mkdir(parents=True, exist_ok=True)
    monthly_nbh_cat.to_parquet(OUT_MONTHLY_NBH_CAT, index=False)

    print("Wrote:", OUT_MONTHLY_NBH_CAT)
    print("Shape:", monthly_nbh_cat.shape)
    print("Columns:", list(monthly_nbh_cat.columns))

if __name__ == "__main__":
    main()
