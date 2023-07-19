from pathlib import Path
from typing import Tuple

import pandas as pd
import streamlit as st

from samples import Samples
from analytics import AnalyticsLib

DATA_LOC = Path(__file__).parent / "data"

ALL_CLIENTS = "All Clients"
ALL_ACCOUNTS = "All Accounts"

NAME_MAP = {
    "client_name": "Client",
    "account_name": "Account",
    "securityid": "Position",
}


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


@st.cache(allow_output_mutation=True)
def get_advisor_data(advisor: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    positions = get_advisor_client_positions(advisor)
    clients = get_advisor_clientele_data(advisor)
    return clients, positions


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


def get_analytics_time_series(df: pd.DataFrame) -> pd.DataFrame:
    return df[["date", "Market Value"]].set_index("date")


def get_positions_summary(
    analytics_time_series: pd.DataFrame,
    aggregated_positions_on_selected_date: pd.DataFrame,
    aggr_level: str,
) -> pd.DataFrame:
    summary_anls = AnalyticsLib().series_summary(analytics_time_series)
    count_key_map = {
        "client_name": "Clients",
        "account_name": "Accounts",
        "securityid": "Positions",
    }
    count_prompt = f"Number of {count_key_map[aggr_level]}"
    summary_anls[count_prompt] = get_object_count_at_aggregation_level(
        aggregated_positions_on_selected_date, aggr_level
    )
    return pd.DataFrame.from_dict(summary_anls, orient="index")


def get_prices():
    ...


@st.cache
def get_transactions(clients: pd.DataFrame) -> pd.DataFrame:
    trxs_file = DATA_LOC / "transactions.csv"
    str_cols = ["accountid", "securityid"]
    trx = pd.read_csv(
        trxs_file, parse_dates=["trade_date"], dtype={_: str for _ in str_cols}
    )
    res = trx.merge(clients, how="left", on=["accountid"], validate="m:1")
    return res[res.advisorid.notnull()].set_index(
        "trade_date"
    )  # crude way of selecting trxs only for the advisor!


def filter_transactions(
    trxs: pd.DataFrame, selected_client: str, selected_account: str
) -> pd.DataFrame:
    all_clients = selected_client == ALL_CLIENTS
    all_accounts = selected_account == ALL_ACCOUNTS
    if all_clients:
        return trxs
    elif all_accounts:
        return trxs[trxs.client_name == selected_client]
    else:
        return trxs[
            (trxs.account_name == selected_account)
            & (trxs.client_name == selected_client)
        ]


def get_benchmarks():
    data_loc = DATA_LOC / "benchmark_values.csv"
    fpk_loc = DATA_LOC / "benchmarks.csv"

    fpks = pd.read_csv(fpk_loc, dtype=str)
    data = pd.read_csv(data_loc, parse_dates=["date"])

    return fpks, data


def aggregate_account_positions(df: pd.DataFrame):
    agg = df.groupby(["accountid", "date"])["mv"].sum()
    results = agg.reset_index().sort_values(by=["date"])
    return results


def get_all_portfolio_periodic_returns(
    portfolio_list: list, df: pd.DataFrame
) -> pd.DataFrame:
    returns_list = []
    anl = AnalyticsLib()
    for portfolio in portfolio_list:
        portfolio_df = df.loc[df.accountid == portfolio, ["date", "mv"]]
        ser = portfolio_df.set_index("date")
        periodic_returns = anl.calculate_periodic_returns(ser)
        ser_df = pd.DataFrame.from_dict(periodic_returns.items())
        ser_df.columns = ["period", portfolio]
        ser_df.set_index("period", inplace=True)
        returns_list.append(ser_df)
    returns_df = pd.concat(returns_list, axis=1)
    return returns_df


def get_compare_portfolios_returns_frame(
    account_list: list,
    benchmark_list: list,
    agg_positions: pd.DataFrame,
    benchmark_values: pd.DataFrame,
):
    if account_list:
        cl_returns = get_all_portfolio_periodic_returns(account_list, agg_positions)
    if benchmark_list:
        bench_returns = get_all_portfolio_periodic_returns(
            benchmark_list, benchmark_values
        )
    res = pd.concat([cl_returns, bench_returns], axis=1)
    return res.reset_index()

