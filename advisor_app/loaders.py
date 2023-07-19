from pathlib import Path
import pandas as pd

DATA_LOC = Path(__file__).parent / "data"


def save_data(df: pd.DataFrame, filetype: str) -> None:
    df.to_csv(DATA_LOC / f"{filetype}.csv", mode="a", index=False, header=False)


def load_benchmark_defns(file: str) -> None:
    read_cols = ["name", "firm_provided_key"]
    df = pd.read_csv(file, usecols=read_cols, dtype=str)
    df["portfolios"] = (df["name"]) + " (" + df["firm_provided_key"] + ")"
    res = df[["name", "firm_provided_key", "portfolios"]]
    save_data(res, "benchmarks")


def load_benchmark_values(file: str) -> None:
    read_cols = ["firm_provided_key", "date", "value"]
    df = pd.read_csv(file, parse_dates=["date"], usecols=read_cols)
    df = df.drop_duplicates(subset=["firm_provided_key", "date"], keep="first")
    save_data(df[read_cols], "benchmark_values")
