import streamlit as st
import pandas as pd
import plotly.express as px

from models.polling import load_polls, calculate_average


# --------------------------------------------------
# PAGE SETUP
# --------------------------------------------------

st.set_page_config(
    page_title="Canada & Québec Election Tracker",
    page_icon="📊",
    layout="wide"
)


# --------------------------------------------------
# ELECTION CONFIGURATION
# --------------------------------------------------

ELECTIONS = {
    "Québec 2026": {
        "file": "data/quebec_polls.csv",
        "parties": ["pq", "plq", "caq", "pcq", "qs"],
        "labels": {
            "pq": "PQ",
            "plq": "PLQ",
            "caq": "CAQ",
            "pcq": "PCQ",
            "qs": "QS"
        }
    },

    "Canada Federal": {
        "file": "data/federal_polls.csv",
        "parties": ["lpc", "cpc", "ndp", "bq", "gpc"],
        "labels": {
            "lpc": "Liberal",
            "cpc": "Conservative",
            "ndp": "NDP",
            "bq": "Bloc Québécois",
            "gpc": "Green"
        }
    }
}


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🇨🇦 Canada & Québec Election Tracker")

st.caption(
    "V1.1 — Polling averages and polling trends"
)


# --------------------------------------------------
# ELECTION SELECTOR
# --------------------------------------------------

election = st.selectbox(
    "Election",
    list(ELECTIONS.keys())
)

config = ELECTIONS[election]


# --------------------------------------------------
# LOAD POLLS
# --------------------------------------------------

polls = load_polls(config["file"])


# --------------------------------------------------
# CALCULATE AVERAGES
# --------------------------------------------------

averages = calculate_average(
    polls,
    config["parties"]
)


# --------------------------------------------------
# POLLING AVERAGE
# --------------------------------------------------

st.subheader("Current Polling Average")

columns = st.columns(len(config["parties"]))

for column, party in zip(columns, config["parties"]):

    column.metric(
        config["labels"][party],
        f"{averages[party]:.1f}%"
    )


# --------------------------------------------------
# POLLING TREND
# --------------------------------------------------

st.subheader("Polling Trend")

trend_data = polls.copy()

trend_data = trend_data.sort_values("date")

for party in config["parties"]:

    trend_data[config["labels"][party]] = trend_data[party]


trend_long = trend_data[
    ["date"] +
    [config["labels"][party] for party in config["parties"]]
].melt(
    id_vars="date",
    var_name="Party",
    value_name="Support"
)


figure = px.line(
    trend_long,
    x="date",
    y="Support",
    color="Party",
    markers=True,
    title=f"{election} Polling Trend"
)

figure.update_layout(
    yaxis_title="Polling support (%)",
    xaxis_title="Date",
    legend_title="Party"
)

st.plotly_chart(
    figure,
    use_container_width=True
)


# --------------------------------------------------
# POLL DATABASE
# --------------------------------------------------

st.subheader("Poll Database")

display_data = polls.copy()

display_data["pollster"] = display_data["pollster"]

st.dataframe(
    display_data,
    use_container_width=True
)