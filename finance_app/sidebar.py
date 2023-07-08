import streamlit as st
from utils import time_greeting

APP_TITLE = "Portfolio Management App"
APP_SIDEBAR_OPTIONS = [
    "🕴️Manage Client Portfolios",
    "Reports",

]


def sidebar(**opts):
    greeting = f"{time_greeting()} {opts['name']}!"
    st.sidebar.title(greeting)
    st.sidebar.title(APP_TITLE)

    st.sidebar.radio(
        'Manage Clients',
        APP_SIDEBAR_OPTIONS,
        index=0,
        label_visibility="hidden",
        key="selected_sidebar_option"
    )
