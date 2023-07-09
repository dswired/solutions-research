from pathlib import Path
from typing import Optional
from datetime import datetime

import pandas as pd
from pandas import Series, DataFrame, concat

PARENT = Path(__file__).parent


class Transaction:
    class DNATable:  # TODO: Add Fees to the mix
        SECURITY = {
            "buy": 1,
            "sell": -1,
            "deposit": 0,
            "withdrawal": 0,
            "instrument-cashflow": 0,
        }

        CASH = {
            "buy": -1,
            "sell": 1,
            "deposit": 1,
            "withdrawal": -1,
            "instrument-cashflow": 1,
        }


class TrackingModel(Transaction):
    def __init__(self, end_date: Optional[str] = None) -> None:
        """
        attributes are a strict reference to column headers as they appear in the db
        see singleclient.models. Any change to model names should result in a change
        to the attributes here.
        """
        self.end_date = end_date
        self.dte = "trade_date"
        self.ttype = "trx_type"
        self.acct = "accountid"
        self.amt = "trx_amt"
        self.qty = "trx_qty"
        self.security = "securityid"

        # Model fields
        self.cash_ffect = "cash_effect"
        self.qty_ffect = "qty_effect"
        self.cash = "cash"
        self.order = "trx_id"
        self.trx_order = [self.acct, self.dte, self.order]
        self.position = [self.acct, self.security, self.dte]

    @property
    def tracking_end_date(self):
        return datetime.today() if not self.end_date else self.end_date

    def _order_trxs(self, trxs: DataFrame) -> DataFrame:
        """
        Relies on the following data types for the following params
        self.acct : str,
        self.dte : datetime,
        """
        return trxs.sort_values(by=self.trx_order)

    def _get_trx_direction(self, trxs: DataFrame, cash=True) -> Series:
        if cash:
            lookup = self.DNATable.CASH
        else:
            lookup = self.DNATable.SECURITY
        return trxs[self.ttype].map(lookup)

    def _get_trx_qty_ffect(self, trxs: DataFrame) -> Series:
        qty_direction = self._get_trx_direction(trxs, False)
        return qty_direction * trxs[self.qty].fillna(0)

    def _get_trx_cash_effect(self, trxs: DataFrame) -> Series:
        cash_direction = self._get_trx_direction(trxs)
        return cash_direction * trxs[self.amt].fillna(0)

    def get_position_qtys(self, df: DataFrame) -> DataFrame:
        _df = df[df[self.security] != "Cash"]
        grpd = _df.groupby(self.position)
        grp_sum = grpd[self.qty_ffect].sum()
        _res = grp_sum.groupby(level=0).cumsum()
        res = _res.reset_index()
        res.rename(columns={self.qty_ffect: "qty"}, inplace=True)
        return res

    def get_acct_cash(self, df: DataFrame) -> DataFrame:
        grpd = df.groupby([self.acct, self.dte])
        grp_sum = grpd[self.cash_ffect].sum()
        _res = grp_sum.groupby(level=0).cumsum()
        res = _res.reset_index()
        res.rename(columns={self.cash_ffect: "qty"}, inplace=True)
        return res

    def cleanup_positions(self, qty, cash):
        df = concat([qty, cash])
        df[self.security].fillna("Cash", inplace=True)
        df.rename(columns={self.dte: "date", self.security: "securityid"}, inplace=True)
        return df

    def _reindex_posn(self, df: DataFrame) -> DataFrame:
        """
        df is a single position timeseries
        """
        start, end = df.date.min(), self.tracking_end_date
        new_index = pd.date_range(start, end, freq="D")
        _df = df.sort_values(by="date").set_index("date")
        res = _df.reindex(new_index).fillna(method="ffill")
        return res.reset_index()

    def _reindex_acct_posns(self, df: DataFrame) -> DataFrame:
        """
        df is account positions
        """
        instrs = set(df.securityid)
        psns = []
        for instr in instrs:
            _df = df[df.securityid == instr]
            re_psn = self._reindex_posn(_df)
            psns.append(re_psn)
        res = concat(psns)
        return res

    def reindex_posns_daily(self, df: DataFrame) -> DataFrame:
        """
        df is cleaned up, tracked, positions
        """
        accts = set(df[self.acct])
        posns = []
        for acct in accts:
            _df = df[df[self.acct] == acct]
            re_psn = self._reindex_acct_posns(_df)
            posns.append(re_psn)
        res = concat(posns)
        return res

    def track(self, trxs: DataFrame) -> DataFrame:
        """Does a full tracking of all cash an non-cash positions.
        Most expensive calcs:
        1. trxs get ordered once
        2. loop is used to determine running balance per cash bucket
        3. tracked cash bkt frames are concatenated.
        4. transactions file is reordered naturally again.
        """
        trxs[self.cash_ffect] = self._get_trx_cash_effect(trxs)
        trxs[self.qty_ffect] = self._get_trx_qty_ffect(trxs)

        ord_trxs = self._order_trxs(trxs)
        qty = self.get_position_qtys(ord_trxs)
        cash = self.get_acct_cash(ord_trxs)
        _res = self.cleanup_positions(qty, cash)
        res = self.reindex_posns_daily(_res)
        return res.rename(columns={"index": "date"})


def get_account_data(path):
    account_file = path / "accounts.csv"

    date_cols = ["client_date_opened", "account_open_date", "account_inception_date"]
    accounts = pd.read_csv(account_file, parse_dates=date_cols)
    is_duplicated_account = accounts.accountid.duplicated(keep=False)
    if any(is_duplicated_account):
        msg = "Accounts file contains duplicate accounts!"
        raise ValueError(msg)
    return accounts


def reindex_prices(pxs: pd.DataFrame, end_date: Optional[str] = None):
    start, end = "2015-12-31", datetime.today() if not end_date else end_date
    new_index = pd.date_range(start, end, freq="D")
    px = pxs.drop_duplicates(subset=["date", "securityid"], keep="first")
    instruments = set(px.securityid)
    dfs = []
    for instrument in instruments:
        df = px[px.securityid == instrument].sort_values(by="date").set_index("date")
        df_re = df.reindex(new_index).fillna(method="ffill").fillna(method="bfill")
        dfs.append(df_re.reset_index())
    result = pd.concat(dfs)
    result.columns = ["date", "securityid", "price"]
    return result


def get_position_pxs(posns: pd.DataFrame, pxs: pd.DataFrame) -> pd.DataFrame:
    clean_pxs = reindex_prices(pxs)
    results = posns.merge(clean_pxs, how="left", on=["date", "securityid"])
    cash_posns = results.securityid == "Cash"
    results.loc[cash_posns, "price"] = 1
    results["mv"] = results["qty"] * results["price"]
    return results


def get_tracking_inputs():
    data_path = PARENT / "data"
    trx_file = data_path / "transactions.csv"
    pxs_file = data_path / "prices_2022-12-29.csv"
    sec_file = data_path / "security_master.csv"

    accounts = get_account_data(data_path)
    trxs = pd.read_csv(trx_file, parse_dates=["trade_date"])
    pxs = pd.read_csv(pxs_file, parse_dates=["date"])
    sec = pd.read_csv(sec_file, dtype=str)
    return accounts, trxs, pxs, sec


def get_position_properties():
    ...


def get_tracked_positions():
    accounts, trxs, pxs, sec = get_tracking_inputs()
    posns = TrackingModel().track(trxs)
    valued_posns = get_position_pxs(posns, pxs)
    tracked_positions = valued_posns.merge(accounts, how="left", on=["accountid"])
    posns_with_properties = tracked_positions.merge(
        sec, how="left", on=["securityid"], validate="m:1"
    )
    return posns_with_properties
