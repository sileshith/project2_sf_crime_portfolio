# dashboard/app.py
# San Francisco Crime Analytics (2018–2025) + 2026 Outlook
# Streamlit dashboard reading cleaned parquet outputs from data/processed/

from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ============================================================
# Paths (robust no matter where you run from)
# ============================================================
APP_DIR = Path(__file__).resolve().parent      # .../dashboard
ROOT_DIR = APP_DIR.parent                      # project root
DATA_DIR = ROOT_DIR / "data" / "processed"

INCIDENTS_FILE = DATA_DIR / "incidents_clean_2018_2025.parquet"
FORECAST_FILE = DATA_DIR / "forecast_citywide_monthly_2026.parquet"
MONTHLY_FILE = DATA_DIR / "monthly_citywide.parquet"


# ============================================================
# Page config
# ============================================================
st.set_page_config(page_title="SF Crime Analytics (2018–2025) + 2026 Outlook", layout="wide")
st.title("San Francisco Crime Analytics (2018–2025) + 2026 Outlook")
st.caption("Portfolio dashboard built from cleaned SFPD incident data (parquet).")


# ============================================================
# Load data
# ============================================================
@st.cache_data(show_spinner="Loading incident data...")
def load_incidents(path: Path) -> pd.DataFrame:
    df = pd.read_parquet(path)

    # Required columns for dashboard
    required = ["neighborhood", "incident_category", "hour", "year"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # Ensure types
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    df = df.dropna(subset=["year"])
    df["year"] = df["year"].astype(int)

    # Monthly axis
    if "year_month" in df.columns:
        df["year_month"] = pd.to_datetime(df["year_month"], errors="coerce")
    elif "month" in df.columns:
        df["year_month"] = pd.to_datetime(df["month"], errors="coerce")
    else:
        raise ValueError("Missing 'year_month' or 'month' for monthly trend plots.")

    # Weekday label
    if "weekday_name" in df.columns:
        df["weekday_label"] = df["weekday_name"].astype(str)
    elif "weekday" in df.columns:
        df["weekday_label"] = df["weekday"].astype(str)
    else:
        df["weekday_label"] = "Unknown"

    # Hour
    df["hour"] = pd.to_numeric(df["hour"], errors="coerce").fillna(0).astype(int)
    df = df[(df["hour"] >= 0) & (df["hour"] <= 23)].copy()

    # Drop unusable rows for dashboard
    df = df.dropna(subset=["year_month", "neighborhood", "incident_category"])

    return df


if not INCIDENTS_FILE.exists():
    st.error(f"Missing file: {INCIDENTS_FILE}")
    st.info("Fix: put the cleaned parquet at data/processed/incidents_clean_2018_2025.parquet")
    st.stop()

try:
    df = load_incidents(INCIDENTS_FILE)
except Exception as e:
    st.error(f"Failed to load incident data. Details: {e}")
    st.stop()


# ============================================================
# Sidebar filters
# ============================================================
st.sidebar.header("Filters")

years = sorted(df["year"].unique())
year_min, year_max = int(min(years)), int(max(years))

year_range = st.sidebar.slider(
    "Year range",
    min_value=year_min,
    max_value=year_max,
    value=(year_min, year_max),
    step=1,
)

neighborhoods = sorted(df["neighborhood"].unique())
selected_nbhds = st.sidebar.multiselect(
    "Neighborhoods",
    options=neighborhoods,
    default=neighborhoods,
)

categories = sorted(df["incident_category"].unique())
default_cats = categories[:10] if len(categories) >= 10 else categories
selected_categories = st.sidebar.multiselect(
    "Incident categories",
    options=categories,
    default=default_cats,
)

weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
weekday_values = sorted(df["weekday_label"].unique())
weekday_options = [d for d in weekday_order if d in weekday_values] + [
    d for d in weekday_values if d not in weekday_order
]

selected_weekdays = st.sidebar.multiselect(
    "Weekdays",
    options=weekday_options,
    default=weekday_options,
)

hour_range = st.sidebar.slider(
    "Hour range",
    min_value=0,
    max_value=23,
    value=(0, 23),
    step=1,
)

mask = (
    (df["year"] >= year_range[0]) &
    (df["year"] <= year_range[1]) &
    (df["neighborhood"].isin(selected_nbhds)) &
    (df["incident_category"].isin(selected_categories)) &
    (df["weekday_label"].isin(selected_weekdays)) &
    (df["hour"].between(hour_range[0], hour_range[1], inclusive="both"))
)

df_filt = df.loc[mask].copy()

st.sidebar.markdown("---")
st.sidebar.download_button(
    "Download filtered CSV",
    data=df_filt.to_csv(index=False).encode("utf-8"),
    file_name="sf_crime_filtered.csv",
    mime="text/csv",
)

st.write(f"Filtered incidents: **{len(df_filt):,}**")


# ============================================================
# Summary metrics
# ============================================================
m1, m2, m3 = st.columns(3)

with m1:
    st.metric("Total incidents", f"{len(df_filt):,}")

with m2:
    if len(df_filt) > 0:
        months_in_view = df_filt["year_month"].dt.to_period("M").nunique()
        st.metric("Months in view", int(months_in_view))
    else:
        st.metric("Months in view", 0)

with m3:
    st.metric("Neighborhoods in view", int(df_filt["neighborhood"].nunique()))


# ============================================================
# Tabs
# ============================================================
tab1, tab2, tab3, tab4 = st.tabs(
    ["Trends and Rankings", "Hour and Weekday Patterns", "Forecast (2026 Outlook)", "About"]
)

# ============================================================
# TAB 1 — Trends and Rankings
# ============================================================
with tab1:
    st.subheader("Monthly Trend (from filtered incidents)")

    if len(df_filt) == 0:
        st.info("No data under current filters.")
    else:
        monthly = (
            df_filt.groupby(df_filt["year_month"].dt.to_period("M"), observed=True)
            .size()
            .reset_index(name="incidents")
        )
        monthly["year_month"] = monthly["year_month"].dt.to_timestamp()

        fig_ts = px.line(monthly, x="year_month", y="incidents", markers=True)
        st.plotly_chart(fig_ts, width="stretch")

        c1, c2 = st.columns(2)

        with c1:
            st.subheader("Top Neighborhoods")
            top_n = df_filt["neighborhood"].value_counts().head(10).reset_index()
            top_n.columns = ["neighborhood", "incidents"]
            fig_n = px.bar(top_n, x="incidents", y="neighborhood", orientation="h")
            fig_n.update_layout(yaxis={"categoryorder": "total ascending"})
            st.plotly_chart(fig_n, width="stretch")

        with c2:
            st.subheader("Top Categories")
            top_c = df_filt["incident_category"].value_counts().head(10).reset_index()
            top_c.columns = ["incident_category", "incidents"]
            fig_c = px.bar(top_c, x="incident_category", y="incidents")
            st.plotly_chart(fig_c, width="stretch")


# ============================================================
# TAB 2 — Hour and Weekday Patterns
# ============================================================
with tab2:
    st.subheader("Hour × Weekday Heatmap (from filtered incidents)")

    if len(df_filt) == 0:
        st.info("No data under current filters.")
    else:
        heat = (
            df_filt.groupby(["weekday_label", "hour"], observed=True)
            .size()
            .reset_index(name="incidents")
        )

        # Enforce weekday order using the exact options available
        heat["weekday_label"] = pd.Categorical(
            heat["weekday_label"], categories=weekday_options, ordered=True
        )
        heat = heat.sort_values(["weekday_label", "hour"])

        fig_h = px.density_heatmap(
            heat,
            x="hour",
            y="weekday_label",
            z="incidents",
            nbinsx=24,
            labels={"weekday_label": "Weekday", "hour": "Hour", "incidents": "Incidents"},
        )
        st.plotly_chart(fig_h, width="stretch")

        c1, c2 = st.columns(2)

        with c1:
            st.subheader("Hourly pattern")
            hourly = df_filt.groupby("hour", observed=True).size().reset_index(name="incidents")
            fig_hour = px.line(hourly, x="hour", y="incidents", markers=True)
            st.plotly_chart(fig_hour, width="stretch")

        with c2:
            st.subheader("Weekday pattern")
            wk = df_filt.groupby("weekday_label", observed=True).size().reset_index(name="incidents")
            wk["weekday_label"] = pd.Categorical(
                wk["weekday_label"], categories=weekday_options, ordered=True
            )
            wk = wk.sort_values("weekday_label")
            fig_wk = px.bar(wk, x="weekday_label", y="incidents")
            st.plotly_chart(fig_wk, width="stretch")


# ============================================================
# TAB 3 — Forecast (2026 Outlook)
# ============================================================
with tab3:
    st.subheader("Citywide Monthly Forecast (precomputed)")

    if not FORECAST_FILE.exists():
        st.error(f"Forecast file not found: {FORECAST_FILE}")
        st.info(
            "Fix:\n"
            "1) Make sure `forecast_citywide_monthly_2026.parquet` exists in your old project.\n"
            "2) Copy it into this project at `data/processed/`.\n"
            "3) Restart Streamlit."
        )
    else:
        fc = pd.read_parquet(FORECAST_FILE).copy()

        expected_cols = {"month", "forecast", "lower", "upper"}
        missing_cols = expected_cols - set(fc.columns)
        if missing_cols:
            st.error(f"Forecast file is missing columns: {sorted(missing_cols)}")
            st.write("Found columns:", list(fc.columns))
        else:
            fc["month"] = pd.to_datetime(fc["month"], errors="coerce")
            fc = fc.dropna(subset=["month"]).sort_values("month")

            hist = None
            if MONTHLY_FILE.exists():
                hist = pd.read_parquet(MONTHLY_FILE).copy()
                if "month" in hist.columns and "incidents" in hist.columns:
                    hist["month"] = pd.to_datetime(hist["month"], errors="coerce")
                    hist = hist.dropna(subset=["month"]).sort_values("month")
                else:
                    hist = None

            fig_fc = go.Figure()

            if hist is not None:
                fig_fc.add_trace(
                    go.Scatter(
                        x=hist["month"], y=hist["incidents"],
                        mode="lines+markers", name="Historical"
                    )
                )

            fig_fc.add_trace(
                go.Scatter(
                    x=fc["month"], y=fc["forecast"],
                    mode="lines+markers", name="Forecast"
                )
            )

            fig_fc.add_trace(
                go.Scatter(
                    x=fc["month"], y=fc["lower"],
                    mode="lines", line=dict(width=0), showlegend=False
                )
            )

            fig_fc.add_trace(
                go.Scatter(
                    x=fc["month"], y=fc["upper"],
                    mode="lines", line=dict(width=0),
                    fill="tonexty", name="Confidence Interval"
                )
            )

            fig_fc.update_layout(height=520)
            st.plotly_chart(fig_fc, width="stretch")

            st.caption(
                "Baseline forecast using a seasonal time-series model on monthly citywide totals. "
                "This is an operational planning signal, not a causal claim."
            )


# ============================================================
# TAB 4 — About
# ============================================================
with tab4:
    st.subheader("What this dashboard shows")
    st.markdown("""
- Filters update every view (years, neighborhoods, categories, weekdays, hours).
- The forecast panel reads a precomputed citywide model output from `data/processed/`.
- This dashboard is intentionally lightweight for portfolio deployment.
""")

    st.subheader("Neighborhood naming")
    st.markdown("""
This project uses the official DataSF **Analysis Neighborhoods** system for consistency with city reporting.
""")