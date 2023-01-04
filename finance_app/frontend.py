import streamlit as st

from sidebar import sidebar
from main_frontend import main_frontend
from app_authentication import get_authentication


def frontend():
    authenticator = get_authentication()
    name, auth_status, username = authenticator.login("Login", "main")

    if auth_status == False:
        st.error("Username or Password is incorrect!")

    if auth_status is None:
        st.warning("Please enter your username and password!")

    if auth_status:
        sidebar(name=name, username=username)
        main_frontend(name=name, username=username)
        authenticator.logout("Logout", "sidebar")
