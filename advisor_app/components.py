import datetime

import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image

MAIN_MENU_MAP = {  # icons from https://icons.getbootstrap.com/
    "Monitor": "house-door-fill",
    "Reports": "book-half",
    "Compare Portfolios": "list-task",
}


def app_option_menu():
    app_menu = option_menu(
        None,
        list(MAIN_MENU_MAP.keys()),
        icons=list(MAIN_MENU_MAP.values()),
        menu_icon="magic",
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#f0f2f6"},
            "icon": {"color": "black", "font-size": "25px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#61ACD1",
            },
            "nav-link-selected": {"background-color": "#0A5A81"},
        },
        key="selected_choice",
    )
    return app_menu


def time_greeting():
    now = datetime.datetime.now()
    if now.hour < 12:
        return "Good morning"
    elif 12 <= now.hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"


def get_greeting(name: str):
    greeting = f"{time_greeting()} {name}!"
    st.sidebar.title(greeting)


def app_logo():
    im = Image.open("images/app_logo.jpg")  # save this first
    st.image(im)


def app_config(layout="wide"):
    # im = Image.open('images/app_logo.jpg')
    st.set_page_config(
        layout=layout,
        page_title="finance app",
        # page_icon=im,  # https://docs.streamlit.io/library/api-reference/utilities/st.set_page_config
    )


def horizontal_rule():
    return st.markdown("---")


def display_dataframe(df: pd.DataFrame, interactive=True):
    if interactive:
        return st.dataframe(df)


def sidebar_options(options: list):
    option = st.sidebar.selectbox("Select an option:", options)
    return option


def app_hamburger():
    hamburger_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            footer:after {
                    content:'Powered by <Your Company Name here>';
                    visibility: visible;
                    display: block;
                    position: relative;
                    #background-color: red;
                    padding: 5px;
                    top: 2px;
                    }
            </style>
            """

    st.markdown(hamburger_style, unsafe_allow_html=True)
