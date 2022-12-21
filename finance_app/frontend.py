import streamlit as st

from sidebar import sidebar
from app_authentication import get_authentication


def frontend():
    authenticator = get_authentication()
    name, auth_status, username = authenticator.login("Login", "main")

    if auth_status == False:
        st.error("Username or Password is incorrect!")

    if not auth_status:
        st.warning("Please enter your username and password!")

    if auth_status:
        authenticator.logout("Logout", "sidebar")
        sidebar(name=name)
        main_frontend()


def main_frontend():
    st.write('WELCOME TO FINANCE APP')
