import streamlit as st
from utils import time_greeting
from data_processing import get_advisor_client_list

APP_TITLE = "Portfolio Management App"


def sidebar(**opts):
    greeting = f"{time_greeting()} {opts['name']}!"
    st.sidebar.title(greeting)
    st.sidebar.title(APP_TITLE)
    st.sidebar.subheader("Manage your Portfolio")

    selected_client = st.sidebar.selectbox(
        'Manage your clients', opts["clients"], index=0, help="Your client list"
    )
    return selected_client
