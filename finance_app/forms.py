import os
from datetime import datetime

import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from jinja2 import Environment, select_autoescape, FileSystemLoader
import pdfkit

from data_processing import (
    ALL_CLIENTS,
    ALL_ACCOUNTS,
    get_client_account_positions,
    get_client_account_list,
    aggregate_positions_on_date,
    aggregate_positions_upto_date,
    get_aggregation_level,
    get_analytics_time_series,
)

load_dotenv("finance_app.env")

TODAY = datetime.today()


def report_form(**opts):
    st.write(st.session_state)
    left, right = st.columns(2)

    if "report_asof_date" not in st.session_state:
        st.session_state["report_asof_date"] = TODAY

    if "report_client" not in st.session_state:
        st.session_state["report_client"] = ALL_CLIENTS

    if "report_account" not in st.session_state:
        st.session_state["report_account"] = ALL_ACCOUNTS

    if "report_aggregation_level" not in st.session_state:
        st.session_state["report_aggregation_level"] = "client_name"

    if "report_date_min" not in st.session_state:
        st.session_state["report_date_min"] = TODAY

    right.write("Here's the template we'll be using:")
    right.image("images/report_template.png", width=300)

    template_env = Environment(loader=FileSystemLoader("templates"), autoescape=select_autoescape())
    template = template_env.get_template("report.html")

    left.write("Fill in the data:")
    form = left.form("report_form")

    form.date_input(
        "AsOf date",
        max_value=TODAY,
        min_value=st.session_state.report_date_min,
        key="report_date",
    )

    form.selectbox("Clients", opts["clients"], key="report_client")
    client_positions = opts["positions"].copy()

    if st.session_state["report_client"] != ALL_CLIENTS:
        client_positions = get_client_account_positions(
            opts["positions"], st.session_state["report_client"]
        )
        client_accounts = get_client_account_list(client_positions)
        form.selectbox("Accounts", client_accounts, key="report_account")

    updated_positions = get_client_account_positions(
        client_positions,
        st.session_state["report_client"],
        st.session_state["report_account"],
    )
    filter_date = st.session_state["report_asof_date"].strftime("%Y-%m-%d")

    aggregated_positions_upto_selected_date: pd.DataFrame = (
        aggregate_positions_upto_date(updated_positions, upto_date=filter_date)
    )

    st.session_state["report_aggregation_level"]: str = get_aggregation_level(
        client=st.session_state["report_client"],
        account=st.session_state["report_account"],
    )

    aggregated_positions_on_selected_date: pd.DataFrame = (
        aggregate_positions_on_date(
            updated_positions,
            on_date=filter_date,
            level=st.session_state["report_aggregation_level"],
        )
    )

    anl_ts = get_analytics_time_series(aggregated_positions_upto_selected_date)

    st.session_state["report_date_min"] = anl_ts.index.min()

    submit = form.form_submit_button("Generate Client Report")
    if submit:
        html = template.render(
            student=st.session_state["report_aggregation_level"],
            course=st.session_state["report_client"],
            grade=st.session_state["report_account"],
            date=st.session_state["report_asof_date"],
        )

        config = pdfkit.configuration(
            wkhtmltopdf=os.getenv("WKTHMLTOPDF_PATH")
        )
        pdf = pdfkit.from_string(html, configuration=config, verbose=False)

        right.success("Your report was generated!")

        right.download_button(
            "⬇️ Download PDF",
            data=pdf,
            file_name="diploma.pdf",
            mime="application/octet-stream",
        )
