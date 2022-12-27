from pathlib import Path

import pandas as pd
import streamlit as st

DATA_LOC = Path(__file__).parent / "data"


@st.cache
def get_advisor_clientele_data(advisor: str) -> pd.DataFrame:
    client_file = DATA_LOC / "clients.csv"
    df = pd.read_csv(client_file, parse_dates=["date_opened"])
    res = df[df.advisorid == advisor]
    return res


def get_advisor_client_list(advisor: str) -> list:
    df = get_advisor_clientele_data(advisor)
    return ["All Clients"] + df.name.to_list()


def get_inception_date():
    ...


def get_prices():
    ...


def get_transactions():
    ...
