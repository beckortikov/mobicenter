import pickle
from pathlib import Path

import streamlit_authenticator as stauth
names = [
    "gagarin",
    "jomboy",
    "tayloq",
    "juma",
    "sogdiana",
    "kqorasuv",
    "kvokzal",
    "bulungur"
]

usernames = [
    "gagarin",
    "jomboy",
    "tayloq",
    "juma",
    "sogdiana",
    "kqorasuv",
    "kvokzal",
    "bulungur"
]
passwords = [
    "gagarin123",
    "jomboy123",
    "tayloq123",
    "juma123",
    "sogdiana123",
    "kqorasuv123",
    "kvokzal123",
    "bulungur123"
]

hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)
