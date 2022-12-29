from datetime import datetime

import streamlit as st

from sidebar import sidebar
from app_authentication import get_authentication
from data_processing import (
    get_advisor_data,
    get_advisor_client_list,
    aggregate_positions
)
from graphs import get_time_series_plot

TODAY = datetime.today()


def frontend():
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
            positions = positions[positions.client_name == selected_client]

        main_frontend(name=name, username=username, client=selected_client, positions=positions)
        authenticator.logout("Logout", "sidebar")


def main_frontend(**opts):
    col1, col2 = st.columns([5, 1])

    positions = opts["positions"]

    if "asof_date" not in st.session_state:
        st.session_state["asof_date"] = TODAY

    with col2:
        asof_date = st.date_input(
            "AsOf date",
            value=st.session_state["asof_date"],
            max_value=TODAY
        )
        st.session_state["asof_date"] = asof_date

    filter_date = st.session_state["asof_date"].strftime("%Y-%m-%d")
    agg = aggregate_positions(positions, upto=filter_date)

    with col1:
        show_table = st.checkbox("Show as table!")
        if not show_table:
            fig = get_time_series_plot(agg, xaxis_value_name="date", yaxis_value_names={x: x for x in ["Market Value"]},
                                       title=None)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.dataframe(agg)  # Use Agrid to style this in future!
            # https://towardsdatascience.com/make-dataframes-interactive-in-streamlit-c3d0c4f84ccb
