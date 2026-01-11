# dashboard/app.py
# San Francisco Crime Analytics (2018–2025) + 2026 Outlook
# Streamlit dashboard reading precomputed parquet artifacts from data/processed/

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

MONTHLY_NBH_CAT_FILE = DATA_DIR / "monthly_neighborhood_category.parquet"
HOURLY_WEEKDAY_FILE = DATA_DIR / "hourly_weekday_counts.parquet"
MONTHLY_CITYWIDE_FILE = DATA_DIR / "monthly_citywide.parquet"
FORECAST_FILE = DATA_DIR / "forecast_citywide_monthly_2026.parquet"


# ============================================================
# Page config
# ============================================================
st.set_page_config(
    page_title="SF Crime Analytics (2018–2025) + 2026 Outlook",
    layout="wide",
)
st.title("San Francisco Crime Analytics (2018–2025) + 2026 Outlook")
st.caption("Portfolio dashboard built from precomputed SFPD aggregates (parquet).")


# ============================================================
# Load artifacts
# ============================================================
@st.cache_data(show_spinner="Loading dashboard artifacts...")
def load_artifacts():
    required_files = [
        MONTHLY_NBH_CAT_FILE,
        HOURLY_WEEKDAY_FILE,
        MONTHLY_CITYWIDE_FILE,
        FORECAST_FILE,
    ]

    missing = [str(p) for p in required_files if not p.exists()]
    if missing:
        raise FileNotFoundError("Missing required artifact(s):\n" + "\n".join(missing))

    mnc = pd.read_parquet(MONTHLY_NBH_CAT_FILE)
    hw = pd.read_parquet(HOURLY_WEEKDAY_FILE)
    mc = pd.read_parquet(MONTHLY_CITYWIDE_FILE)
    fc = pd.read_parquet(FORECAST_FILE)

    # ----------------------------
    # Validate monthly_neighborhood_category
    # ----------------------------
    need_mnc = {"year_month", "year", "neighborhood", "incident_category", "incidents"}
    miss_mnc = sorted(list(need_mnc - set(mnc.columns)))
    if miss_mnc:
        raise ValueError(f"monthly_neighborhood_category missing columns: {miss_mnc}")

    mnc = mnc.copy()
    mnc["year_month"] = pd.to_datetime(mnc["year_month"], errors="coerce")
    mnc["year"] = pd.to_numeric(mnc["year"], errors="coerce").astype("Int64")
    mnc["incidents"] = pd.to_numeric(mnc["incidents"], errors="coerce").fillna(0)

    mnc = mnc.dropna(subset=["year_month", "year", "neighborhood", "incident_category"])
    mnc["year"] = mnc["year"].astype(int)

    # ----------------------------
    # Validate hourly_weekday_counts
    # ----------------------------
    need_hw = {"weekday_label", "hour", "incident_category", "incidents"}
    miss_hw = sorted(list(need_hw - set(hw.columns)))
    if miss_hw:
        raise ValueError(f"hourly_weekday_counts missing columns: {miss_hw}")

    hw = hw.copy()
    hw["hour"] = pd.to_numeric(hw["hour"], errors="coerce").fillna(0).astype(int)
    hw = hw[(hw["hour"] >= 0) & (hw["hour"] <= 23)].copy()
    hw["weekday_label"] = hw["weekday_label"].astype(str)
    hw["incident_category"] = hw["incident_category"].astype(str)
    hw["incidents"] = pd.to_numeric(hw["incidents"], errors="coerce").fillna(0)

    # ----------------------------
    # Validate monthly_citywide
    # ----------------------------
    need_mc = {"month", "incidents"}
    miss_mc = sorted(list(need_mc - set(mc.columns)))
    if miss_mc:
        raise ValueError(f"monthly_citywide missing columns: {miss_mc}")

    mc = mc.copy()
    mc["month"] = pd.to_datetime(mc["month"], errors="coerce")
    mc["incidents"] = pd.to_numeric(mc["incidents"], errors="coerce").fillna(0)
    mc = mc.dropna(subset=["month"]).sort_values("month")

    # ----------------------------
    # Validate forecast_citywide_monthly_2026
    # ----------------------------
    need_fc = {"month", "forecast", "lower", "upper"}
    miss_fc = sorted(list(need_fc - set(fc.columns)))
    if miss_fc:
        raise ValueError(f"forecast_citywide_monthly_2026 missing columns: {miss_fc}")

    fc = fc.copy()
    fc["month"] = pd.to_datetime(fc["month"], errors="coerce")
    fc["forecast"] = pd.to_numeric(fc["forecast"], errors="coerce")
    fc["lower"] = pd.to_numeric(fc["lower"], errors="coerce")
    fc["upper"] = pd.to_numeric(fc["upper"], errors="coerce")
    fc = fc.dropna(subset=["month", "forecast", "lower", "upper"]).sort_values("month")

    return mnc, hw, mc, fc


try:
    mnc, hw, mc, fc = load_artifacts()
except Exception as e:
    st.error(f"Failed to load dashboard artifacts. Details: {e}")
    st.stop()


# ============================================================
# Sidebar filters (based on mnc)
# ============================================================
st.sidebar.header("Filters")

years = sorted(mnc["year"].unique())
year_min, year_max = int(min(years)), int(max(years))

year_range = st.sidebar.slider(
    "Year range",
    min_value=year_min,
    max_value=year_max,
    value=(year_min, year_max),
    step=1,
)

neighborhoods = sorted(mnc["neighborhood"].unique())
selected_nbhds = st.sidebar.multiselect(
    "Neighborhoods",
    options=neighborhoods,
    default=neighborhoods,   # portfolio-friendly: show full city by default
)

categories = (
    mnc.groupby("incident_category", observed=True)["incidents"]
       .sum()
       .sort_values(ascending=False)
       .index
       .tolist()
)
default_categories = categories[:10] if len(categories) > 10 else categories

selected_categories = st.sidebar.multiselect(
    "Incident categories",
    options=categories,
    default=default_categories,
)

if len(selected_nbhds) == 0 or len(selected_categories) == 0:
    st.warning("Please select at least one neighborhood and one category in the sidebar.")
    st.stop()

mask_mnc = (
    (mnc["year"] >= year_range[0]) &
    (mnc["year"] <= year_range[1]) &
    (mnc["neighborhood"].isin(selected_nbhds)) &
    (mnc["incident_category"].isin(selected_categories))
)
mnc_filt = mnc.loc[mask_mnc].copy()

st.sidebar.markdown("---")
st.sidebar.download_button(
    "Download filtered monthly table (CSV)",
    data=mnc_filt.to_csv(index=False).encode("utf-8"),
    file_name="sf_crime_monthly_filtered.csv",
    mime="text/csv",
)


# ============================================================
# Summary metrics
# ============================================================
total_incidents = int(mnc_filt["incidents"].sum()) if len(mnc_filt) else 0
months_in_view = int(mnc_filt["year_month"].dt.to_period("M").nunique()) if len(mnc_filt) else 0
nbhds_in_view = int(mnc_filt["neighborhood"].nunique()) if len(mnc_filt) else 0

st.write(f"Filtered incidents (from monthly aggregates): **{total_incidents:,}**")

m1, m2, m3 = st.columns(3)
m1.metric("Total incidents", f"{total_incidents:,}")
m2.metric("Months in view", months_in_view)
m3.metric("Neighborhoods in view", nbhds_in_view)


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
    st.subheader("Monthly Trend (from filtered aggregates)")

    if len(mnc_filt) == 0:
        st.info("No data under current filters.")
    else:
        monthly = (
            mnc_filt.groupby("year_month", observed=True)["incidents"]
                    .sum()
                    .reset_index()
                    .sort_values("year_month")
        )

        fig_ts = px.line(monthly, x="year_month", y="incidents", markers=True)
        st.plotly_chart(fig_ts, use_container_width=True)

        c1, c2 = st.columns(2)

        with c1:
            st.subheader("Top Neighborhoods")
            top_n = (
                mnc_filt.groupby("neighborhood", observed=True)["incidents"]
                        .sum()
                        .sort_values(ascending=False)
                        .head(10)
                        .reset_index()
            )
            fig_n = px.bar(top_n, x="incidents", y="neighborhood", orientation="h")
            fig_n.update_layout(yaxis={"categoryorder": "total ascending"})
            st.plotly_chart(fig_n, use_container_width=True)

        with c2:
            st.subheader("Top Categories")
            top_c = (
                mnc_filt.groupby("incident_category", observed=True)["incidents"]
                        .sum()
                        .sort_values(ascending=False)
                        .head(10)
                        .reset_index()
            )
            fig_c = px.bar(top_c, x="incident_category", y="incidents")
            st.plotly_chart(fig_c, use_container_width=True)


# ============================================================
# TAB 2 — Hour and Weekday Patterns
# ============================================================
with tab2:
    st.subheader("Hour × Weekday Heatmap (category-filtered)")

    hw_filt = hw[hw["incident_category"].isin(selected_categories)].copy()

    if len(hw_filt) == 0:
        st.info("No hourly-weekday data for the selected categories.")
    else:
        weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        weekday_values = sorted(hw_filt["weekday_label"].unique())
        weekday_options = [d for d in weekday_order if d in weekday_values] + [
            d for d in weekday_values if d not in weekday_order
        ]

        hw_filt["weekday_label"] = pd.Categorical(
            hw_filt["weekday_label"], categories=weekday_options, ordered=True
        )
        hw_filt = hw_filt.sort_values(["weekday_label", "hour"])

        fig_h = px.density_heatmap(
            hw_filt,
            x="hour",
            y="weekday_label",
            z="incidents",
            nbinsx=24,
            labels={"weekday_label": "Weekday", "hour": "Hour", "incidents": "Incidents"},
        )
        st.plotly_chart(fig_h, use_container_width=True)

        c1, c2 = st.columns(2)

        with c1:
            st.subheader("Hourly pattern")
            hourly = hw_filt.groupby("hour", observed=True)["incidents"].sum().reset_index()
            fig_hour = px.line(hourly, x="hour", y="incidents", markers=True)
            st.plotly_chart(fig_hour, use_container_width=True)

        with c2:
            st.subheader("Weekday pattern")
            wk = hw_filt.groupby("weekday_label", observed=True)["incidents"].sum().reset_index()
            wk["weekday_label"] = pd.Categorical(wk["weekday_label"], categories=weekday_options, ordered=True)
            wk = wk.sort_values("weekday_label")
            fig_wk = px.bar(wk, x="weekday_label", y="incidents")
            st.plotly_chart(fig_wk, use_container_width=True)


# ============================================================
# TAB 3 — Forecast (2026 Outlook)
# ============================================================
with tab3:
    st.subheader("Citywide Monthly Forecast (precomputed)")

    fig_fc = go.Figure()

    fig_fc.add_trace(go.Scatter(
        x=mc["month"], y=mc["incidents"],
        mode="lines+markers", name="Historical"
    ))

    fig_fc.add_trace(go.Scatter(
        x=fc["month"], y=fc["forecast"],
        mode="lines+markers", name="Forecast"
    ))

    fig_fc.add_trace(go.Scatter(
        x=fc["month"], y=fc["lower"],
        mode="lines", line=dict(width=0), showlegend=False
    ))

    fig_fc.add_trace(go.Scatter(
        x=fc["month"], y=fc["upper"],
        mode="lines", line=dict(width=0),
        fill="tonexty", name="Confidence Interval"
    ))

    fig_fc.update_layout(height=520)
    st.plotly_chart(fig_fc, use_container_width=True)

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
- The dashboard reads only precomputed parquet artifacts under `data/processed/`.
- Filters apply to the monthly neighborhood-category aggregates.
- Hour × Weekday patterns come from a separate hourly-weekday aggregate and are filtered by category.
- The forecast panel reads a precomputed citywide model output.
""")

    st.subheader("Neighborhood naming")
    st.markdown("""
This project uses the official DataSF **Analysis Neighborhoods** system for consistency with city reporting.
""")
