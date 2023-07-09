import streamlit as st

from top_summary import get_client_positions_from_top_summary
from forms import report_form
import data_processing as dp
import graphs as gph


def main_frontend(**opts):
    # st.write(st.session_state)
    if "selected_sidebar_option" not in st.session_state:
        st.session_state["selected_sidebar_option"] = "🕴️Manage Client Portfolios"

    clients, positions = dp.get_advisor_data(opts["username"])
    advisor_clients = dp.get_advisor_client_list(positions)
    trxs = dp.get_transactions(clients)

    if st.session_state["selected_sidebar_option"] == "🕴️Manage Client Portfolios":

        # Top summary
        st.markdown("""---""")
        (
            aggregated_positions_upto_selected_date,
            aggregated_positions_on_selected_date,
            analytics_time_series,
        ) = get_client_positions_from_top_summary(
            clients=advisor_clients, positions=positions
        )
        st.markdown("""---""")

        # col1, col2 = st.columns([6, 2])
        ts_line = gph.get_time_series_plot(
            aggregated_positions_upto_selected_date,
            xaxis_value_name="date",
            yaxis_value_names={x: x for x in ["Market Value"]},
        )
        st.plotly_chart(ts_line, use_container_width=True)
        # st.dataframe(
            #     aggregated_positions_upto_selected_date
            # )  # Use Agrid to style this in future!
            # # https://towardsdatascience.com/make-dataframes-interactive-in-streamlit-c3d0c4f84ccb
        # with col2:
        #     summary = dp.get_positions_summary(
        #         analytics_time_series,
        #         aggregated_positions_on_selected_date,
        #         st.session_state.aggregation_level,
        #     )
        #     st.dataframe(summary)

        col3, col4 = st.columns([1, 1])
        with col3:
            pie = gph.get_pie_chart(
                aggregated_positions_on_selected_date,
                label_col=st.session_state["aggregation_level"],
                values_col="Market Value",
            )
            st.plotly_chart(pie, use_container_width=True)

        filtered_transactions = dp.filter_transactions(
            trxs, st.session_state.selected_client, st.session_state.selected_account
        )
        st.dataframe(filtered_transactions)

    elif st.session_state.selected_sidebar_option == "Reports":
        report_form(clients=advisor_clients, positions=positions)
