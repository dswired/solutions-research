from pathlib import Path

import pandas as pd

from position_tracking import get_tracked_positions
from app_authentication import generate_hashed_passwords
from graphs import get_time_series_plot

PARENT = Path(__file__).parent


class Samples:

    @staticmethod
    def run_tracking() -> None:
        posns = get_tracked_positions()
        posns.to_csv("data/tracked_positions.csv", index=False)

    @staticmethod
    def generate_keys() -> None:
        savefile = "hashed_passwords.pkl"
        generate_hashed_passwords(savefile)

    @staticmethod
    def get_sample_data_plot():
        file = PARENT / "data" / "sample_time_series.csv"
        df = pd.read_csv(file, parse_dates=["DATE"])
        fig = get_time_series_plot(df, xaxis_value_name="DATE", yaxis_value_names={x: x for x in ["val1", "val2"]},
                                   title="Sample line plot")
        return fig  # Now ran with st.plotly_chart(fig, use_container_width=True)