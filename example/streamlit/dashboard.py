import pandas as pd

import streamlit as st

st.title("Dashboard")

SYMBOL_COLUMN = "symbol"
DATA_URL = "http://127.0.0.1:8888/api/coins/"
COIN_URL = "http://127.0.0.1:8888/api/coins/detail/"


@st.cache_data
def load_coins_data():
    data = pd.read_json(DATA_URL)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    return data


def load_transactions_for_coin_data(symbol):
    data = pd.read_json(COIN_URL + symbol)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    return data


data_load_state = st.text("Loading Coins List")
data = load_coins_data()
data_load_state.text("")

st.subheader("Available Coins")
st.write(data)

option = st.selectbox("Coin", list(data.symbol))

if option:
    coins_data = load_transactions_for_coin_data(option)
    st.dataframe(coins_data)
