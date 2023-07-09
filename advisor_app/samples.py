from pathlib import Path

import pandas as pd

from position_tracking import get_tracked_positions
from app_authentication import generate_hashed_passwords

PARENT = Path(__file__).parent


class Samples:
    @staticmethod
    def run_tracking() -> None:
        posns = get_tracked_positions()
        savefile = PARENT / "data" / "tracked_positions.csv"
        posns.to_csv(savefile, index=False)

    @staticmethod
    def generate_keys() -> None:
        savefile = "hashed_passwords.pkl"
        generate_hashed_passwords(savefile)


if __name__ == "__main__":
    Samples().run_tracking()
