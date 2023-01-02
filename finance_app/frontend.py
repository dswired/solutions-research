from datetime import datetime

import pandas as pd
import streamlit as st

from sidebar import sidebar
from app_authentication import get_authentication
from data_processing import (
    get_advisor_data,
    get_advisor_client_list,
    aggregate_positions_upto_date,
    aggregate_positions_on_date,
    get_aggregation_level,
    get_client_account_positions
)
from graphs import (
    get_time_series_plot,
    get_pie_chart
)

TODAY = datetime.today()
LAYOUT = "wide"


def frontend():
    st.set_page_config(
            layout=LAYOUT
        )
    authenticator = get_authentication()
    name, auth_status, username = authenticator.login("Login", "main")

    if auth_status == False:
        st.error("Username or Password is incorrect!")

    if auth_status is None:
        st.warning("Please enter your username and password!")

    if auth_status:
        accounts, positions = get_advisor_data(username)
        advisor_clients = get_advisor_client_list(accounts)
        selected_client = sidebar(name=name, username=username, clients=advisor_clients)

        if selected_client != "All Clients":
            posns = positions[positions.client_name == selected_client]
        else:
            posns = positions.copy()

        main_frontend(
            name=name, username=username, client=selected_client, positions=posns, account=None
        )
        authenticator.logout("Logout", "sidebar")


def main_frontend(**opts):
    positions = get_client_account_positions(opts["positions"], opts["client"], opts["account"])

    col1, col2 = st.columns([6, 2])
    if "asof_date" not in st.session_state:
        st.session_state["asof_date"] = TODAY

    with col2:
        asof_date = st.date_input(
            "AsOf date", value=st.session_state["asof_date"], max_value=TODAY
        )
        st.session_state["asof_date"] = asof_date

    filter_date = st.session_state["asof_date"].strftime("%Y-%m-%d")
    agg_upto_df: pd.DataFrame = aggregate_positions_upto_date(positions, upto_date=filter_date)
    aggregation_level: str = get_aggregation_level(client=opts["client"], account=opts["account"])
    agg_on_df: pd.DataFrame = aggregate_positions_on_date(positions, on_date=filter_date, level=aggregation_level)

    with col1:
        show_table = st.checkbox("Show as table!")
        if not show_table:
            ts_line = get_time_series_plot(
                agg_upto_df,
                xaxis_value_name="date",
                yaxis_value_names={x: x for x in ["Market Value"]}
            )
            st.plotly_chart(ts_line, use_container_width=True)
        else:
            st.dataframe(agg_upto_df)  # Use Agrid to style this in future!
            # https://towardsdatascience.com/make-dataframes-interactive-in-streamlit-c3d0c4f84ccb

    col3, col4 = st.columns([1, 1])
    with col3:
        pie = get_pie_chart(agg_on_df, label_col=aggregation_level, values_col="Market Value")
        st.plotly_chart(pie, use_container_width=True)
