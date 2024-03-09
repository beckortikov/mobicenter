import pickle
from pathlib import Path

import streamlit_authenticator as stauth

names = [
    "Амонов Асадбек",
    "Суванов Исломбек",
    "Сирожиддинова Садокат",
    "Абдуллоев Сохиб",
    "Бердикулов Машхурбек",
    "Абдусамадов Ботир",
    "Юлдашов Мехрож",
    "Абдужабборова Мавлуда",
    "Исобоев Алижон",
    "Шаропов Шехроз",
]
usernames = [
    "asadbek", "islombek", "sadoqat",
    "soxib", "mashxurbek", "botir",
    "mexroj", "mavluda", "alijon",
    "shexroz",
]
passwords = [
    "asadbek123", "islombek123", "sadoqat123",
    "soxib123", "mashxurbek123", "botir123",
    "mexroj123", "mavluda123", "alijon123",
    "shexroz123",
]

hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)
