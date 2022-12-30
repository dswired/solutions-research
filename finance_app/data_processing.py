from pathlib import Path
from typing import Tuple, Optional

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


def aggregate_positions_upto_date(df: pd.DataFrame, upto_date) -> pd.DataFrame:
    agg = df.groupby(["date"])["mv"].sum()
    results = agg.reset_index().sort_values(by=["date"])
    results.columns = ["date", "Market Value"]
    results["Change from previous day"] = results["Market Value"] - results["Market Value"].shift(1)
    return results[results.date <= upto_date]


def aggregate_positions_on_date(df: pd.DataFrame, on_date, level: str) -> pd.DataFrame:
    df_on_date = df[df.date == on_date]
    agg_group = ["date", level]
    agg = df_on_date.groupby(agg_group)["mv"].sum().reset_index()
    agg.columns = agg_group + ["Market Value"]
    return agg


def get_aggregation_level(client: str, account: Optional[str] = None) -> str:
    if client == "All Clients":
        return "client_name"
    else:
        if account:
            return "securityid"
        else:
            return "account_name"


def get_client_account_positions(df: pd.DataFrame, client: str, account: Optional[str] = None):
    if client == "All Clients":
        return df
    else:
        client_df = df[(df.client_name == client)]
        if account:
            return client_df[(client_df.account_name == account)]
        else:
            return client_df


def get_inception_date():
    ...


def get_prices():
    ...


def get_transactions():
    ...
