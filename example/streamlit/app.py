import datetime

import pandas as pd
import streamlit as st
from pandas import DataFrame

st.title("Crypto Terminal")

SYMBOL_COLUMN = "symbol"
DATA_URL = "http://127.0.0.1:8888/api/coins/"
TRANSACTION_URL = "http://127.0.0.1:8888/api/coins/search-transaction/"
BEST_TRANSACTION_URL = "http://127.0.0.1:8888/api/coins/best-transaction/"


@st.cache_data
def load_coins_data():
    data = pd.read_json(DATA_URL)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    return data


def load_transaction_data(symbol, date):
    data = pd.read_json(TRANSACTION_URL + symbol + "/" + str(date))
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    return data


def load_best_transactions(start_date, end_date):
    data = pd.read_json(BEST_TRANSACTION_URL + str(start_date) + "/" + str(end_date))
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    return data


data_load_state = st.text("Loading Coins List")
data = load_coins_data()
data_load_state.text("")

if st.checkbox("Available coins"):
    st.subheader("Available Coins")
    st.write(data)

if st.checkbox("Close Price"):
    option = st.selectbox("Coin", list(data.symbol))
    selected_date = st.date_input("Date", datetime.date(2020, 10, 6))

    if st.button("Search Close Price"):
        transaction_data = load_transaction_data(option, selected_date)
        close_data = DataFrame(transaction_data["close"])

        st.metric(
            "Close Price", str(close_data.close[0]), delta=None, delta_color="normal"
        )

if st.checkbox("Maximize Profit"):
    start_date = st.date_input("Start Date", datetime.date(2020, 10, 6))
    end_date = st.date_input("End Date", datetime.date(2020, 11, 6))

    if st.button("Search Best Opportunity"):
        transactions_data = load_best_transactions(start_date, end_date)

        st.title("Best Transaction")

        st.metric(
            "Coin", str(transactions_data.coin[0]), delta=None, delta_color="normal"
        )
        st.metric(
            "Buy Date",
            str(transactions_data.date[0].date()),
            delta=None,
            delta_color="normal",
        )
        st.metric(
            "Buy Price", transactions_data.low[0], delta=None, delta_color="normal"
        )
        st.metric(
            "Sell Date",
            str(transactions_data.date[1].date()),
            delta=None,
            delta_color="normal",
        )
        st.metric(
            "Sell Price", transactions_data.high[1], delta=None, delta_color="normal"
        )
