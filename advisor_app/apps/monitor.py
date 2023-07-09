import streamlit as st
from top_summary import top_summary
import data_processing as dp
import graphs as gph
from components import horizontal_rule
import pandas as pd

# div.css-1offfwp.e16nr0p34

theme_plotly = None


def set_state():
    ...


def run(name, username):
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}<style>", unsafe_allow_html=True)

    clients, positions = dp.get_advisor_data(username)
    advisor_clients = dp.get_advisor_client_list(positions)
    trxs = dp.get_transactions(clients)

    st.write(st.session_state)
    with st.container():
        (
            aggregated_positions_upto_selected_date,
            aggregated_positions_on_selected_date,
            analytics_time_series,
            updated_positions,
        ) = top_summary(clients=advisor_clients, positions=positions)
    horizontal_rule()

    st.subheader("Overview")
    ts_line = gph.get_time_series_plot(
        aggregated_positions_upto_selected_date,
        xaxis_value_name="date",
        yaxis_value_names={x: x for x in ["Market Value"]},
        title="Market Value Over Time.",
    )
    st.plotly_chart(ts_line, use_container_width=True, theme=theme_plotly)

    st.subheader("Exposure")
    col3, col4, col5 = st.columns([1, 1, 1])
    with col3:
        pie1 = gph.get_pie_chart(
            aggregated_positions_on_selected_date,
            label_col=st.session_state["aggregation_level"],
            values_col="Market Value",
            title=f"By {dp.NAME_MAP[st.session_state['aggregation_level']]}",
        )
        st.plotly_chart(pie1, use_container_width=True)

    with col4:
        industry_counts = pd.DataFrame(
            updated_positions.industry.value_counts().reset_index()
        )
        industry_counts.columns = ["industry", "percentage"]
        pie2 = gph.get_pie_chart(
            industry_counts,
            label_col="industry",
            values_col="percentage",
            title="By Industry",
        )
        st.plotly_chart(pie2, use_container_width=True)

    with col5:
        sector_counts = pd.DataFrame(
            updated_positions.sector.value_counts().reset_index()
        )
        sector_counts.columns = ["sector", "percentage"]
        pie2 = gph.get_pie_chart(
            sector_counts,
            label_col="sector",
            values_col="percentage",
            title="By Sector",
        )
        st.plotly_chart(pie2, use_container_width=True)

    st.subheader("Transactions")
    filtered_transactions = dp.filter_transactions(
        trxs, st.session_state.selected_client, st.session_state.selected_account
    )
    st.dataframe(filtered_transactions)
