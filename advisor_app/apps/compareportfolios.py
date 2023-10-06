import streamlit as st
import data_processing as dp
from components import horizontal_rule, sidebar_options
from loaders import load_benchmark_defns, load_benchmark_values
from top_summary import TODAY
import pandas as pd
import graphs as gph


import plotly.express as px

benchmark_options = ["Benchmarking", "Load Data"]


def load_benchmarks():
    col1, col2 = st.columns(2)
    with col1:
        defns_file = st.file_uploader("Load benchmark definitions")
    with col2:
        data_file = st.file_uploader("Load bencmark values")
    horizontal_rule()
    if defns_file:
        try:
            load_benchmark_defns(defns_file)
            st.success("Successfully loaded benchmark definitions!")
        except Exception as err:
            st.error(
                f"Failed to load provided benchmarks definitions due to the following error: {err}"
            )
    if data_file:
        try:
            load_benchmark_values(data_file)
            st.success(
                "Successfully loaded benchmark values. Please refresh portfolios!"
            )
        except Exception as err:
            st.error(
                f"Failed to load provided benchmarks valujes due to the following error: {err}"
            )


def run(name, username):
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}<style>", unsafe_allow_html=True)
    option = sidebar_options(benchmark_options)
    if option == "Benchmarking":

        clients, positions = dp.get_advisor_data(username)
        agg_positions = dp.aggregate_account_positions(positions)
        accounts_list = list(set(positions["accountid"])) or []

        benchmark_info, benchmark_data = dp.get_benchmarks()
        benchmark_fpks = list(set(benchmark_data["accountid"])) or []

        col1, col2, col3, col4 = st.columns([2, 2, 1, 1])

        if "asof_date" not in st.session_state:
            st.session_state["compare_asof_date"] = TODAY

        with col1:
            selected_portfolios = st.multiselect(
                "Select a Client Portfolio", accounts_list, [accounts_list[0]]
            )
        with col2:
            if benchmark_fpks:
                selected_benchmarks = st.multiselect(
                    "Select a Benchmark", benchmark_fpks, benchmark_fpks[0]
                )
            else:
                st.warning("No benchmarks found in database!")
        col3.date_input(
            "AsOf date",
            max_value=TODAY,
            min_value=st.session_state.input_date_min,
            key="compare_asof_date",
        )
        with col4:
            update = st.button("Refresh portfolios!")
        horizontal_rule()
        col5, col6 = st.columns([4, 2])
        with col5:
            returns = dp.get_compare_portfolios_returns_frame(
                selected_portfolios, selected_benchmarks, agg_positions, benchmark_data
            )
            values = selected_benchmarks + selected_portfolios
            return_bars = gph.get_bar_chart(
                returns,
                label_col="period",
                values_cols=values,
                title="Periodic returns",
            )
            st.plotly_chart(return_bars, use_container_width=True)
        with col6:
            vol = pd.read_csv(
                r"G:\My Drive\Fin_Engineering\d1g1t-repo\solutions-research\advisor_app\data\risk_vol_data.csv"
            )
            fig = px.scatter(
                vol,
                x="Mean Return",
                y="Risk(Annual Volatility)",
                color="portfolio",
                title="Risk-Return Map",
            )
            st.plotly_chart(fig, use_container_width=True)
        risk_stats = pd.read_csv(
            r"G:\My Drive\Fin_Engineering\d1g1t-repo\solutions-research\advisor_app\data\risk_stats.csv"
        )
        st.dataframe(risk_stats.set_index("Portfolio"), use_container_width=True)
    elif option == "Load Data":
        load_benchmarks()
