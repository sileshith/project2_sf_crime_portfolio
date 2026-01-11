# dashboard/app.py
# San Francisco Crime Analytics (2018–2025) + 2026 Outlook
# Streamlit dashboard reading aggregated parquet outputs from data/processed/
#
# Option A (Recommended): No raw incident parquet required for deployment.
# The app reads lightweight, precomputed artifacts that are safe to store on GitHub.

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

MONTHLY_FILE = DATA_DIR / "monthly_citywide.parquet"
HOURLY_WEEKDAY_FILE = DATA_DIR / "hourly_weekday_counts.parquet"
FORECAST_FILE = DATA_DIR / "forecast_citywide_monthly_2026.parquet"


# ============================================================
# Page config
# ============================================================
st.set_page_config(page_title="SF Crime Analytics (2018-2025) + 2026 Outlook", layout="wide")
st.title("San Francisco Crime Analytics (2018-2025) + 2026 Outlook")
st.caption("Portfolio dashboard built from precomputed SFPD aggregates (parquet).")


# ============================================================
# Load data (aggregates only)
# ============================================================
@st.cache_data(show_spinner="Loading monthly totals...")
def load_monthly(path: Path) -> pd.DataFrame:
    df = pd.read_parquet(path).copy()

    # Expect: month, neighborhood, incident_category, incidents
    required = {"month", "neighborhood", "incident_category", "incidents"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"monthly_citywide missing columns: {sorted(missing)}")

    df["month"] = pd.to_datetime(df["month"], errors="coerce")
    df = df.dropna(subset=["month"])
    df["incidents"] = pd.to_numeric(df["incidents"], errors="coerce").fillna(0).astype(int)

    # Add year + hour placeholders for unified filtering
    df["year"] = df["month"].dt.year.astype(int)
    return df


@st.cache_data(show_spinner="Loading hour × weekday counts...")
def load_hourly_weekday(path: Path) -> pd.DataFrame:
    df = pd.read_parquet(path).copy()

    # Expect: weekday_label, hour, incident_category, incidents
    required = {"weekday_label", "hour", "incident_category", "incidents"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"hourly_weekday_counts missing columns: {sorted(missing)}")

    df["hour"] = pd.to_numeric(df["hour"], errors="coerce").fillna(0).astype(int)
    df = df[(df["hour"] >= 0) & (df["hour"] <= 23)].copy()
    df["incidents"] = pd.to_numeric(df["incidents"], errors="coerce").fillna(0).astype(int)

    df["weekday_label"] = df["weekday_label"].astype(str)
    df["incident_category"] = df["incident_category"].astype(str)

    return df


@st.cache_data(show_spinner="Loading forecast...")
def load_forecast(path: Path) -> pd.DataFrame:
    df = pd.read_parquet(path).copy()

    required = {"month", "forecast", "lower", "upper"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"forecast_citywide_monthly_2026 missing columns: {sorted(missing)}")

    df["month"] = pd.to_datetime(df["month"], errors="coerce")
    df = df.dropna(subset=["month"]).sort_values("month")

    for c in ["forecast", "lower", "upper"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    return df


# ============================================================
# Existence checks
# ============================================================
missing_files = [p for p in [MONTHLY_FILE, HOURLY_WEEKDAY_FILE] if not p.exists()]
if missing_files:
    st.error("Missing required data artifacts in data/processed/:")
    for p in missing_files:
        st.write(f"- {p}")
    st.info(
        "Fix:\n"
        "1) Generate the artifacts in your notebook/script.\n"
        "2) Save them under `data/processed/`.\n"
        "3) Commit + push to GitHub so Streamlit Cloud can read them."
    )
    st.stop()

try:
    monthly_df = load_monthly(MONTHLY_FILE)
    hourly_df = load_hourly_weekday(HOURLY_WEEKDAY_FILE)
except Exception as e:
    st.error(f"Failed to load dashboard artifacts. Details: {e}")
    st.stop()


# ============================================================
# Sidebar filters (applied to aggregates)
# ============================================================
st.sidebar.header("Filters")

years = sorted(monthly_df["year"].unique())
year_min, year_max = int(min(years)), int(max(years))

year_range = st.sidebar.slider(
    "Year range",
    min_value=year_min,
    max_value=year_max,
    value=(year_min, year_max),
    step=1,
)

neighborhoods = sorted(monthly_df["neighborhood"].unique())
selected_nbhds = st.sidebar.multiselect(
    "Neighborhoods",
    options=neighborhoods,
    default=neighborhoods[:5] if len(neighborhoods) > 5 else neighborhoods,
)

categories_monthly = sorted(monthly_df["incident_category"].unique())
categories_hourly = sorted(hourly_df["incident_category"].unique())
all_categories = sorted(set(categories_monthly) | set(categories_hourly))

default_cats = all_categories[:10] if len(all_categories) >= 10 else all_categories
selected_categories = st.sidebar.multiselect(
    "Incident categories",
    options=all_categories,
    default=default_cats,
)

weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
weekday_values = sorted(hourly_df["weekday_label"].unique())
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


# ============================================================
# Apply filters to aggregates
# ============================================================
monthly_filt = monthly_df[
    (monthly_df["year"].between(year_range[0], year_range[1])) &
    (monthly_df["neighborhood"].isin(selected_nbhds)) &
    (monthly_df["incident_category"].isin(selected_categories))
].copy()

hourly_filt = hourly_df[
    (hourly_df["weekday_label"].isin(selected_weekdays)) &
    (hourly_df["hour"].between(hour_range[0], hour_range[1])) &
    (hourly_df["incident_category"].isin(selected_categories))
].copy()


# ============================================================
# Sidebar download (monthly filtered view)
# ============================================================
st.sidebar.markdown("---")
st.sidebar.download_button(
    "Download monthly filtered CSV",
    data=monthly_filt.to_csv(index=False).encode("utf-8"),
    file_name="sf_crime_monthly_filtered.csv",
    mime="text/csv",
)


# ============================================================
# Summary metrics (aggregate-aware)
# ============================================================
total_incidents = int(monthly_filt["incidents"].sum()) if len(monthly_filt) else 0
months_in_view = int(monthly_filt["month"].dt.to_period("M").nunique()) if len(monthly_filt) else 0
neighborhoods_in_view = int(monthly_filt["neighborhood"].nunique()) if len(monthly_filt) else 0

st.write(f"Filtered incidents (monthly aggregate sum): **{total_incidents:,}**")

m1, m2, m3 = st.columns(3)
with m1:
    st.metric("Total incidents", f"{total_incidents:,}")
with m2:
    st.metric("Months in view", months_in_view)
with m3:
    st.metric("Neighborhoods in view", neighborhoods_in_view)


# ============================================================
# Tabs
# ============================================================
tab1, tab2, tab3, tab4 = st.tabs(
    ["Trends and Rankings", "Hour and Weekday Patterns", "Forecast (2026 Outlook)", "About"]
)


# ============================================================
# TAB 1 — Trends and Rankings (monthly aggregates)
# ============================================================
with tab1:
    st.subheader("Monthly Trend (from filtered monthly aggregates)")

    if len(monthly_filt) == 0:
        st.info("No data under current filters.")
    else:
        city_monthly = (
            monthly_filt.groupby("month", as_index=False, observed=True)["incidents"]
            .sum()
            .sort_values("month")
        )

        fig_ts = px.line(city_monthly, x="month", y="incidents", markers=True)
        st.plotly_chart(fig_ts, width="stretch")

        c1, c2 = st.columns(2)

        with c1:
            st.subheader("Top Neighborhoods (by incidents)")
            top_n = (
                monthly_filt.groupby("neighborhood", as_index=False, observed=True)["incidents"]
                .sum()
                .sort_values("incidents", ascending=False)
                .head(10)
            )
            fig_n = px.bar(top_n, x="incidents", y="neighborhood", orientation="h")
            fig_n.update_layout(yaxis={"categoryorder": "total ascending"})
            st.plotly_chart(fig_n, width="stretch")

        with c2:
            st.subheader("Top Categories (by incidents)")
            top_c = (
                monthly_filt.groupby("incident_category", as_index=False, observed=True)["incidents"]
                .sum()
                .sort_values("incidents", ascending=False)
                .head(10)
            )
            fig_c = px.bar(top_c, x="incident_category", y="incidents")
            st.plotly_chart(fig_c, width="stretch")


# ============================================================
# TAB 2 — Hour and Weekday Patterns (hourly aggregates)
# ============================================================
with tab2:
    st.subheader("Hour × Weekday Heatmap (from hourly aggregates)")

    if len(hourly_filt) == 0:
        st.info("No data under current filters.")
    else:
        heat = hourly_filt.copy()
        heat["weekday_label"] = pd.Categorical(heat["weekday_label"], categories=weekday_options, ordered=True)
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
            hourly_line = (
                hourly_filt.groupby("hour", as_index=False, observed=True)["incidents"]
                .sum()
                .sort_values("hour")
            )
            fig_hour = px.line(hourly_line, x="hour", y="incidents", markers=True)
            st.plotly_chart(fig_hour, width="stretch")

        with c2:
            st.subheader("Weekday pattern")
            wk = (
                hourly_filt.groupby("weekday_label", as_index=False, observed=True)["incidents"]
                .sum()
            )
            wk["weekday_label"] = pd.Categorical(wk["weekday_label"], categories=weekday_options, ordered=True)
            wk = wk.sort_values("weekday_label")
            fig_wk = px.bar(wk, x="weekday_label", y="incidents")
            st.plotly_chart(fig_wk, width="stretch")


# ============================================================
# TAB 3 — Forecast (2026 Outlook)
# ============================================================
with tab3:
    st.subheader("Citywide Monthly Forecast (precomputed)")

    if not FORECAST_FILE.exists():
        st.warning(
            "Forecast file not found.\n\n"
            f"Expected: {FORECAST_FILE}\n\n"
            "Fix: generate it from your forecasting notebook and save to data/processed/, then commit + push."
        )
    else:
        try:
            fc = load_forecast(FORECAST_FILE)
        except Exception as e:
            st.error(f"Failed to load forecast file. Details: {e}")
            st.stop()

        # Historical citywide monthly from monthly_df (not filtered by neighborhood/category for forecast view)
        hist_citywide = (
            monthly_df.groupby("month", as_index=False, observed=True)["incidents"]
            .sum()
            .sort_values("month")
        )

        fig_fc = go.Figure()

        fig_fc.add_trace(
            go.Scatter(
                x=hist_citywide["month"], y=hist_citywide["incidents"],
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
    st.markdown(
        """
- The app reads **precomputed parquet artifacts** from `data/processed/` for fast, reliable deployment.
- Filters apply to **aggregated views**, not raw incidents (a deliberate design choice for Streamlit Cloud).
- The forecast panel reads a **precomputed citywide model output**.
        """
    )

    st.subheader("Neighborhood naming")
    st.markdown(
        """
This project uses the official DataSF **Analysis Neighborhoods** system for consistency with city reporting.
        """
    )
