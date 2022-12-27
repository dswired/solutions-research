import streamlit as st

from sidebar import sidebar
from app_authentication import get_authentication


def frontend():
    authenticator = get_authentication()
    name, auth_status, username = authenticator.login("Login", "main")

    if auth_status == False:
        st.error("Username or Password is incorrect!")

    if auth_status is None:
        st.warning("Please enter your username and password!")

    if auth_status:
        selected_client = sidebar(name=name, username=username)
        main_frontend(name=name, username=username, client=selected_client)
        authenticator.logout("Logout", "sidebar")


def main_frontend(**opts):
    st.write('WELCOME TO FINANCE APP')
    st.write(opts["name"])
    st.write(opts["username"])
    st.write(opts["client"])
