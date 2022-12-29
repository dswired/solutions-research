from pathlib import Path
from typing import Tuple

import pandas as pd
import streamlit as st

DATA_LOC = Path(__file__).parent / "data"


def get_advisor_client_positions(advisor: str) -> pd.DataFrame:
    positions_file = DATA_LOC / "tracked_positions.csv"
    df = pd.read_csv(positions_file, parse_dates=["date"])
    res = df[df.advisorid == advisor]
    return res


def get_advisor_clientele_data(advisor: str) -> pd.DataFrame:
    account_file = DATA_LOC / "accounts.csv"
    df = pd.read_csv(
        account_file,
        parse_dates=[
            "client_date_opened",
            "account_open_date",
            "account_inception_date"
        ]
    )
    res = df[df.advisorid == advisor]
    return res


@st.cache
def get_advisor_data(advisor: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    positions = get_advisor_client_positions(advisor)
    accounts = get_advisor_clientele_data(advisor)
    return accounts, positions


def get_advisor_client_list(accounts: pd.DataFrame) -> list:
    return ["All Clients"] + list(set(accounts.client_name))


def aggregate_positions(df: pd.DataFrame, upto):
    agg = df.groupby(["date"])["mv"].sum()
    results = agg.reset_index().sort_values(by=["date"])
    results.columns = ["date", "Market Value"]
    results["Change from previous day"] = results["Market Value"] - results["Market Value"].shift(1)
    return results[results.date <= upto]


def get_inception_date():
    ...


def get_prices():
    ...


def get_transactions():
    ...
