import streamlit as st

import components as cs
from app_authentication import get_authentication
import apps
import utils


def run():
    cs.app_config()
    cs.app_hamburger()
    auth = get_authentication()
    name, status, username = auth.login("Login")

    if not status:
        st.warning("Please enter your username and password!")

    if status == False:
        st.error("Username or password is incorrect!")

    if status:
        if "selected_choice" not in st.session_state:
            st.session_state["selected_choice"] = "Monitor"
        cs.get_greeting(name=name)
        with st.sidebar:
            cs.app_option_menu()
            cs.horizontal_rule()
        choice = utils.convert_selected_choice(st.session_state["selected_choice"])
        section = getattr(apps, choice)
        section.run(name=name, username=username)
        auth.logout("Logout", "sidebar")


if __name__ == "__main__":
    run()
