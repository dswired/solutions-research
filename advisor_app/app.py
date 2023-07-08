import streamlit as st

import app_components as acs
import apps
import utils


def run():
    if "selected_choice" not in st.session_state:
        st.session_state["selected_choice"] = "Monitor"
    acs.app_config()
    acs.app_hamburger()
    with st.sidebar:
        acs.app_option_menu()
        acs.horizontal_rule()
    choice = utils.convert_selected_choice(st.session_state["selected_choice"])
    section = getattr(apps, choice)
    section.run()


if __name__ == "__main__":
    run()
