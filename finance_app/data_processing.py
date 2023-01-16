from pathlib import Path
from typing import Tuple

import pandas as pd
import streamlit as st

from analytics import AnalyticsLib

DATA_LOC = Path(__file__).parent / "data"

ALL_CLIENTS = "All Clients"
ALL_ACCOUNTS = "All Accounts"


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
            "account_inception_date",
        ],
    )
    res = df[df.advisorid == advisor]
    return res


@st.cache
def get_advisor_data(advisor: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    positions = get_advisor_client_positions(advisor)
    accounts = get_advisor_clientele_data(advisor)
    return accounts, positions


def get_advisor_client_list(positions: pd.DataFrame) -> list:
    return [ALL_CLIENTS] + list(set(positions.client_name))


def get_client_account_list(client: pd.DataFrame) -> list:
    return [ALL_ACCOUNTS] + list(set(client.account_name))


def aggregate_positions_upto_date(df: pd.DataFrame, upto_date) -> pd.DataFrame:
    _df = df[df.date <= upto_date]
    agg = _df.groupby(["date"])["mv"].sum()
    results = agg.reset_index().sort_values(by=["date"])
    results.columns = ["date", "Market Value"]
    results["Change from previous day"] = results["Market Value"] - results[
        "Market Value"
    ].shift(1)
    return results


def aggregate_positions_on_date(df: pd.DataFrame, on_date, level: str) -> pd.DataFrame:
    df_on_date = df[df.date == on_date]
    agg_group = ["date", level]
    agg = df_on_date.groupby(agg_group)["mv"].sum().reset_index()
    agg.columns = agg_group + ["Market Value"]
    return agg


def get_aggregation_level(
    client: str = ALL_CLIENTS, account: str = ALL_ACCOUNTS
) -> str:
    if client == ALL_CLIENTS:
        return "client_name"
    else:
        if account == ALL_ACCOUNTS:
            return "account_name"
        else:
            return "securityid"


def get_object_count_at_aggregation_level(
    df: pd.DataFrame, aggregation_level: str
) -> int:
    """Gets the unique number of values at a specific aggregation level eg.
    If aggregation level is "client_name" then its the unique set of clients undr consideration.
    If the aggregation level is "securityid" then it the unique set of positions,...
    """
    return len(set(df[aggregation_level]))


def get_client_account_positions(
    df: pd.DataFrame, client: str = ALL_CLIENTS, account: str = ALL_ACCOUNTS
):
    if client == ALL_CLIENTS:
        return df.copy()
    else:
        client_df = df[(df.client_name == client)]
        if account == ALL_ACCOUNTS:
            return client_df.copy()
        else:
            return client_df[(client_df.account_name == account)]


def get_date_market_value(df: pd.DataFrame, dte, cash=True):
    if cash:
        date_df = df[(df.date == dte) & (df.securityid == "Cash")]
    else:
        date_df = df[(df.date == dte)]
    return sum(date_df.mv)


def get_inception_date(positions: pd.DataFrame):
    return positions.date.min().strftime("%Y-%m-%d")


def get_analytics_ts(df: pd.DataFrame) -> pd.DataFrame:
    return df[["date", "Market Value"]].set_index("date")


def get_positions_summary(df: pd.DataFrame, aggr_level: str) -> pd.DataFrame:
    anl_ts = get_analytics_ts(df)
    summary_anls = AnalyticsLib().series_summary(anl_ts)
    count_key_map = {
        "client_name": "Clients",
        "account_name": "Accounts",
        "securityid": "Positions",
    }
    count_prompt = f"Number of {count_key_map[aggr_level]}"
    summary_anls[count_prompt] = get_object_count_at_aggregation_level(df, aggr_level)
    return pd.DataFrame.from_dict(summary_anls, orient="index")


def get_prices():
    ...


def get_transactions():
    ...
