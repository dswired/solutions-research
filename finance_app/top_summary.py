from datetime import datetime

import streamlit as st
import pandas as pd

from data_processing import (
    ALL_CLIENTS,
    ALL_ACCOUNTS,
    get_client_account_positions,
    get_client_account_list,
    aggregate_positions_on_date,
    aggregate_positions_upto_date,
    get_aggregation_level,
    get_date_market_value,
    get_inception_date,
)

from analytics import AnalyticsLib

TODAY = datetime.today()
GAIN_DELTA = -12
RETURN_DELTA = 0.2343432

ANL = AnalyticsLib()


def _top_summary_widths():
    return [1.5, 1.5] + [1] * 7


def get_top_summary_cols():
    return st.columns(_top_summary_widths())


def get_client_positions_from_top_summary(**opts):
    col1, col2, col3, col4, col5, col6, col7, col8, col9 = get_top_summary_cols()

    if "asof_date" not in st.session_state:
        st.session_state["asof_date"] = TODAY

    if "selected_client" not in st.session_state:
        st.session_state["selected_client"] = ALL_CLIENTS

    if "selected_account" not in st.session_state:
        st.session_state["selected_account"] = ALL_ACCOUNTS

    if "aggregation_level" not in st.session_state:
        st.session_state["aggregation_level"] = "client_name"

    with st.container():
        col1.selectbox("Clients", opts["clients"], key="selected_client")
        client_positions = opts["positions"].copy()

        if st.session_state["selected_client"] != ALL_CLIENTS:
            client_positions = get_client_account_positions(
                opts["positions"], st.session_state["selected_client"]
            )
            client_accounts = get_client_account_list(client_positions)
            col2.selectbox("Accounts", client_accounts, key="selected_account")

        updated_positions = get_client_account_positions(
            client_positions,
            st.session_state["selected_client"],
            st.session_state["selected_account"],
        )
        filter_date = st.session_state["asof_date"].strftime("%Y-%m-%d")

        aggregated_positions_upto_selected_date: pd.DataFrame = (
            aggregate_positions_upto_date(updated_positions, upto_date=filter_date)
        )

        st.session_state["aggregation_level"]: str = get_aggregation_level(
            client=st.session_state["selected_client"],
            account=st.session_state["selected_account"],
        )

        aggregated_positions_on_selected_date: pd.DataFrame = (
            aggregate_positions_on_date(
                updated_positions,
                on_date=filter_date,
                level=st.session_state["aggregation_level"],
            )
        )

        anl_ts = aggregated_positions_upto_selected_date[
            ["date", "Market Value"]
        ].set_index("date")

        st.session_state["input_date_min"] = anl_ts.index.min()

        # Summary analytics
        date_mv = get_date_market_value(updated_positions, dte=filter_date, cash=False)
        date_cash = get_date_market_value(updated_positions, dte=filter_date)
        inception_date = get_inception_date(updated_positions)
        ytd_gain = ANL.get_ytd_gains(anl_ts, filter_date, ytd_cashflows=0)
        ytd_return = ANL.get_ytd_return(anl_ts, filter_date, ytd_cashflows=0)

        col4.metric(label="Market Value (AsOf Date)", value=f"{date_mv:,.2f}")
        col5.metric(label="Cash Balance (AsOf Date)", value=f"{date_cash:,.2f}")
        col6.metric(
            label="Total Gain (YtD)", value=f"{ytd_gain:,.2f}", delta=GAIN_DELTA
        )
        col7.metric(
            label="Total Return (YtD)",
            value=f"{ytd_return:.2%}",
            delta=f"{RETURN_DELTA:.2%}",
        )
        col8.metric(label="Inception Date", value=inception_date)
        col9.date_input(
            "AsOf date",
            max_value=TODAY,
            min_value=st.session_state.input_date_min,
            key="asof_date",
        )
    return (
        aggregated_positions_upto_selected_date,
        aggregated_positions_on_selected_date,
    )
