import pandas as pd
import sqlite3 as sql3

import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import lag_plot
from pandas import datetime
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
from fastai.tabular.all import *



def filter_deal_id(data: pd.DataFrame):
    ids = set()
    for i, d_id in enumerate(data["deal_id"]):
        if d_id not in ids:
            ids.add(i)

    data = data.iloc[list(ids)]
    return data


def read_data():
    con = sql3.connect("../data/trade_info.sqlite3")
    data = pd.read_sql(""
                       "SELECT s.id, s.date, c.time, deal_id, c.price "
                       "FROM Trading_session s "
                       "INNER JOIN Chart_data c ON s.id = c.session_id "
                       "WHERE trading_type='monthly' AND platform_id=1 "
                       "ORDER BY date, time",
                       con)

    data = filter_deal_id(data)
    data.price += 10

    return data


def preproc_boosting(df):
    add_datepart(df, 'date', drop=False)
    df.drop(['Elapsed', "date", "time"], axis=1, inplace=True)


if __name__ == "__main__":
    df = read_data()




    print("Done!")
