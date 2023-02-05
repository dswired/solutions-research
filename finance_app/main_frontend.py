from datetime import datetime

from utils import time_greeting
import pandas as pd
import streamlit as st
from top_summary import get_client_positions_from_top_summary

from data_processing import (
    get_advisor_data,
    get_advisor_client_list,
)
from graphs import get_time_series_plot, get_pie_chart


def main_frontend(**opts):
    if "selected_sidebar_option" not in st.session_state:
        st.session_state["selected_sidebar_option"] = "🕴️Manage Client Portfolios"

    clients, positions = get_advisor_data(opts["username"])
    advisor_clients = get_advisor_client_list(positions)

    greeting = f"{time_greeting()} {opts['name']}!"
    st.header(greeting)

    # Top summary
    st.markdown("""---""")
    agg_upto_df, agg_on_df = get_client_positions_from_top_summary(
        clients=advisor_clients, positions=positions
    )
    st.markdown("""---""")

    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        show_table = st.checkbox("Show as table!")
        if not show_table:
            ts_line = get_time_series_plot(
                agg_upto_df,
                xaxis_value_name="date",
                yaxis_value_names={x: x for x in ["Market Value"]},
            )
            st.plotly_chart(ts_line, use_container_width=True)
        else:
            st.dataframe(agg_upto_df)  # Use Agrid to style this in future!
            # https://towardsdatascience.com/make-dataframes-interactive-in-streamlit-c3d0c4f84ccb


    # with col2:
    #     pie = get_pie_chart(
    #         agg_on_df,
    #         label_col=st.session_state["aggregation_level"],
    #         values_col="Market Value",
    #     )
    #     st.plotly_chart(pie, use_container_width=True)

    col4, col5, col6 = st.columns([1, 3, 1])
    with col5:
        pie = get_pie_chart(
            agg_on_df,
            label_col=st.session_state["aggregation_level"],
            values_col="Market Value",
        )
        st.plotly_chart(pie, use_container_width=True)
