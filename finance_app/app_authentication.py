import pickle
from typing import Tuple
from pathlib import Path

import pandas as pd
import streamlit_authenticator as stauth

PARENT = Path(__file__).parent


def get_authentication_data(passwords=True) -> Tuple[list, ...]:
    auth_file = PARENT / "data" / "authentication.csv"
    df = pd.read_csv(auth_file)
    names, usernames = df["names"].to_list(), df["usernames"].to_list()
    if passwords:
        return names, usernames, df["passwords"].to_list()
    else:
        return names, usernames


def generate_hashed_passwords(savefile: str):
    names, usernames, passwords = get_authentication_data()
    hashed_passwords = stauth.Hasher(passwords).generate()
    file_path = PARENT / savefile  # eg. "hashed_passwords.pkl"

    with file_path.open("wb") as file:
        pickle.dump(hashed_passwords, file)


def load_hashed_passowrds(file: str):
    file_path = PARENT / file
    with file_path.open("rb") as f:
        hashed_passwords = pickle.load(f)
    return hashed_passwords


def generate_credentials(usernames, names, passwords):
    credentials = {"usernames": {}}

    for un, name, pw in zip(usernames, names, passwords):
        user_dict = {"name": name, "password": pw}
        credentials["usernames"].update({un: user_dict})
    return credentials


def get_authentication():
    names, usernames = get_authentication_data(False)
    hashed_passwords = load_hashed_passowrds("hashed_passwords.pkl")
    credentials = generate_credentials(usernames, names, hashed_passwords)

    authenticator = stauth.Authenticate(
        credentials,
        "finance_app",
        "auth",
        cookie_expiry_days=30,
    )
    return authenticator
