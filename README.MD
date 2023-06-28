# Crypto Terminal

# Data
All necessary data is in `example/data/archive`.

## Create an interactive tool to answer the following questions
1) What coins are available in our dataset?
2) What was the Close price of X coin at date yyyy-mm-dd (eg: BTC in 2020-01-02)
3) Given a start date and end date, what are the best possible buy and sell times to maximise profit?

You can use any language and GUI (command line interface, streamlit, etc.).

## Bonus
These are not necessary for evaluation, but the candidate can use them to showcase his/her skills.
- Load the data into SQLite
- Create a REST API backend to serve the data to the tool
- Create a dashboard with useful metrics and graphs

## Installation

Install the requirements in the environment `poetry install`

## Configuration

### Execute if the database was deleted

First create the database `python manage.py migrate`

To load the data into de sqlite database run `python manage.py load_into_db`

To create a superuser run `python manage.py createsuperuser`

## Run application

To run the backend `python manage.py runserver 8888`

To run the interactive tool `streamlit run example/streamlit/app.py`

To run the dashboard `streamlit run example/streamlit/dashboard.py`

To access to the backend admin enter in `http://127.0.0.1:8888/admin` with the credentials created for the
superuser (`admin/admin` if the database is not deleted)