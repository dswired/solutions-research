from pathlib import Path

from position_tracking import get_tracked_positions
from app_authentication import generate_hashed_passwords

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
