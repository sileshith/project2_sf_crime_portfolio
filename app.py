from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "processed"
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

st.set_page_config(page_title="SF Reported-Incident Intelligence", page_icon="🌉", layout="wide")


@st.cache_data(show_spinner="Loading verified project artifacts…")
def load_data() -> dict[str, pd.DataFrame | dict]:
    paths = {
        "monthly": DATA / "monthly_citywide.parquet",
        "breakdown": DATA / "monthly_neighborhood_category.parquet",
        "hourly": DATA / "hourly_weekday_counts.parquet",
        "forecast": DATA / "forecast_citywide_monthly_2026.parquet",
        "backtest": DATA / "backtest_summary.csv",
        "metadata": DATA / "metadata.json",
        "model_metadata": DATA / "model_metadata.json",
    }
    missing = [path.name for path in paths.values() if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Missing project artifacts: {', '.join(missing)}")
    result: dict[str, pd.DataFrame | dict] = {
        "monthly": pd.read_parquet(paths["monthly"]),
        "breakdown": pd.read_parquet(paths["breakdown"]),
        "hourly": pd.read_parquet(paths["hourly"]),
        "forecast": pd.read_parquet(paths["forecast"]),
        "backtest": pd.read_csv(paths["backtest"]),
        "metadata": json.loads(paths["metadata"].read_text()),
        "model_metadata": json.loads(paths["model_metadata"].read_text()),
    }
    return result


try:
    data = load_data()
except Exception as exc:
    st.error(f"The dashboard could not load its verified artifacts: {exc}")
    st.stop()

monthly = data["monthly"].copy()
breakdown = data["breakdown"].copy()
hourly = data["hourly"].copy()
forecast = data["forecast"].copy()
backtest = data["backtest"].copy()
metadata = data["metadata"]
model_metadata = data["model_metadata"]

monthly["month"] = pd.to_datetime(monthly["month"])
breakdown["year_month"] = pd.to_datetime(breakdown["year_month"])
forecast["month"] = pd.to_datetime(forecast["month"])

st.title("San Francisco Reported-Incident Intelligence")
st.markdown(
    "A reproducible view of recorded SFPD incidents from **2018–2025**, with transparent "
    "model backtesting and an uncertainty-aware six-month outlook."
)
st.caption(
    f"Data artifact generated {metadata['generated_at_utc'][:10]} · "
    f"{metadata['source_rows']:,} canonical records · DataSF dataset wg3w-h783"
)

with st.sidebar:
    st.header("Explore")
    years = sorted(breakdown["year"].unique())
    year_range = st.slider(
        "Year range", int(min(years)), int(max(years)), (int(min(years)), int(max(years)))
    )
    neighborhoods = sorted(breakdown["neighborhood"].dropna().unique())
    selected_neighborhoods = st.multiselect("Neighborhoods", neighborhoods, default=neighborhoods)
    category_totals = (
        breakdown.groupby("incident_category")["incidents"].sum().sort_values(ascending=False)
    )
    categories = category_totals.index.tolist()
    selected_categories = st.multiselect("Incident categories", categories, default=categories)
    st.divider()
    st.markdown(
        "[Data source](https://data.sfgov.org/d/wg3w-h783) · "
        "[Methodology](https://github.com/sileshith/sf-incident-forecasting/blob/main/docs/model_card.md)"
    )

if not selected_neighborhoods or not selected_categories:
    st.warning("Select at least one neighborhood and incident category.")
    st.stop()

filtered = breakdown[
    breakdown["year"].between(*year_range)
    & breakdown["neighborhood"].isin(selected_neighborhoods)
    & breakdown["incident_category"].isin(selected_categories)
].copy()

total = int(filtered["incidents"].sum())
months_in_view = max(filtered["year_month"].nunique(), 1)
top_neighborhood = (
    filtered.groupby("neighborhood")["incidents"].sum().idxmax() if not filtered.empty else "—"
)
top_category = (
    filtered.groupby("incident_category")["incidents"].sum().idxmax() if not filtered.empty else "—"
)

k1, k2, k3, k4 = st.columns(4)
k1.metric("Reported incidents", f"{total:,}")
k2.metric("Monthly average", f"{total / months_in_view:,.0f}")
k3.metric("Leading neighborhood", top_neighborhood)
k4.metric("Leading category", top_category)

overview, patterns, outlook, methodology = st.tabs(
    ["Overview", "Time patterns", "Forecast & validation", "Methods & limitations"]
)

with overview:
    trend = filtered.groupby("year_month", as_index=False)["incidents"].sum()
    fig = px.line(
        trend, x="year_month", y="incidents", markers=True, title="Monthly reported incidents"
    )
    fig.update_layout(xaxis_title=None, yaxis_title="Incident records", hovermode="x unified")
    st.plotly_chart(fig, width="stretch")

    left, right = st.columns(2)
    with left:
        neighborhoods_chart = (
            filtered.groupby("neighborhood", as_index=False)["incidents"]
            .sum()
            .nlargest(12, "incidents")
            .sort_values("incidents")
        )
        fig = px.bar(
            neighborhoods_chart,
            x="incidents",
            y="neighborhood",
            orientation="h",
            title="Highest-volume neighborhoods",
        )
        fig.update_layout(xaxis_title="Incident records", yaxis_title=None)
        st.plotly_chart(fig, width="stretch")
    with right:
        categories_chart = (
            filtered.groupby("incident_category", as_index=False)["incidents"]
            .sum()
            .nlargest(12, "incidents")
            .sort_values("incidents")
        )
        fig = px.bar(
            categories_chart,
            x="incidents",
            y="incident_category",
            orientation="h",
            title="Highest-volume incident categories",
        )
        fig.update_layout(xaxis_title="Incident records", yaxis_title=None)
        st.plotly_chart(fig, width="stretch")

    st.download_button(
        "Download filtered monthly data",
        filtered.to_csv(index=False),
        "sf_reported_incidents_filtered.csv",
        "text/csv",
    )

with patterns:
    pattern = hourly[hourly["incident_category"].isin(selected_categories)].copy()
    pattern = pattern.groupby(["weekday_label", "hour"], as_index=False)["incidents"].sum()
    matrix = pattern.pivot(index="weekday_label", columns="hour", values="incidents").reindex(
        WEEKDAYS
    )
    fig = px.imshow(
        matrix,
        aspect="auto",
        labels={"x": "Hour of day", "y": "Weekday", "color": "Incident records"},
        title="Reported incidents by weekday and hour",
        color_continuous_scale="Blues",
    )
    st.plotly_chart(fig, width="stretch")
    st.info(
        "The time-pattern artifact supports category filtering but not neighborhood "
        "or year filtering. "
        "Those controls therefore do not alter this panel."
    )

with outlook:
    st.subheader("Six-month citywide outlook")
    fig = go.Figure()
    historical_window = monthly.tail(36)
    fig.add_trace(
        go.Scatter(
            x=historical_window["month"],
            y=historical_window["incidents"],
            name="Historical",
            mode="lines+markers",
        )
    )
    fig.add_trace(
        go.Scatter(x=forecast["month"], y=forecast["lower"], line={"width": 0}, showlegend=False)
    )
    fig.add_trace(
        go.Scatter(
            x=forecast["month"],
            y=forecast["upper"],
            line={"width": 0},
            fill="tonexty",
            fillcolor="rgba(37,99,235,.16)",
            name="95% model interval",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=forecast["month"],
            y=forecast["forecast"],
            name="SARIMA forecast",
            mode="lines+markers",
            line={"dash": "dash"},
        )
    )
    fig.update_layout(yaxis_title="Reported incidents", xaxis_title=None, hovermode="x unified")
    st.plotly_chart(fig, width="stretch")
    st.caption(
        "The forecast is aggregate and descriptive. It is not an individual risk "
        "score, causal estimate, "
        "or patrol-allocation recommendation."
    )

    st.subheader("Rolling-origin backtest")
    display = backtest.rename(
        columns={
            "model": "Model",
            "mae": "MAE",
            "rmse": "RMSE",
            "mape": "MAPE (%)",
            "wape": "WAPE (%)",
            "mase": "MASE",
        }
    )
    st.dataframe(
        display.style.format({c: "{:.2f}" for c in display.columns if c != "Model"}),
        hide_index=True,
        width="stretch",
    )
    st.caption(
        f"Selection metric: MASE · Backtest winner: {model_metadata['backtest_winner']} · "
        f"Deployed interval-bearing model: {model_metadata['deployed_model']}"
    )

with methodology:
    st.subheader("What the project measures")
    st.markdown(
        "The unit is a **recorded SFPD incident**, not an estimate of all crime or "
        "personal safety. Counts may change with reporting behavior, enforcement "
        "practice, classification, and source revisions."
    )
    st.subheader("Forecast design")
    st.markdown(
        "Models are evaluated across multiple expanding-window forecast origins. "
        "Seasonal naive, additive Holt-Winters ETS, and SARIMA are compared using "
        "MAE, RMSE, MAPE, WAPE, and MASE."
    )
    st.subheader("Known limitations")
    st.markdown(
        "- The 2020 pandemic is a structural break.\n"
        "- Raw neighborhood counts are not population- or exposure-adjusted rates.\n"
        "- The model excludes policy, weather, economic, event, and reporting-delay variables.\n"
        "- Citywide forecasts must not be interpreted as neighborhood-level risk."
    )
