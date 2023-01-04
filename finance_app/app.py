import streamlit as st
from frontend import frontend

if __name__ == "__main__":
    st.set_page_config(
        layout="wide"
    )
    frontend()
