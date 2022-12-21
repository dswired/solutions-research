import streamlit as st
from utils import time_greeting

APP_TITLE = "Portfolio Management App"


def sidebar(**options):
    if "name" in options:
        greeting = f"{time_greeting()} {options['name']}!"
        st.sidebar.title(greeting)
    st.sidebar.title(APP_TITLE)
    st.sidebar.subheader("Manage your Portfolio")
