import pandas as pd
from pandas.io.pytables import IndexCol
from get_div_info import *
import os
import time


def open_csv(filename):
    path = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_csv(path + "/" + filename)
    return df


def data_process(df):
    df[
        [
            "price_last",
            "price_52high",
            "price_fall",
            "div_yield",
            "div_rate",
            "div_growth",
            "div_growth_year",
        ]
    ] = "-"
    # price_info = [price_last, price_52high, price_fall]
    # div_info = [div_yield, div_rate, div_growth, div_growth_year]
    for i in range(len(df)):
        ticker = df.loc[i, "Symbol"]
        price_info, div_info = get_div_info(ticker)
        time.sleep(0.5)
        if price_info:
            (
                df.loc[i, "price_last"],
                df.loc[i, "price_52high"],
                df.loc[i, "price_fall"],
            ) = price_info
        if div_info:
            (
                df.loc[i, "div_yield"],
                df.loc[i, "div_rate"],
                df.loc[i, "div_growth"],
                df.loc[i, "div_growth_year"],
            ) = div_info
    return df


def write_csv(df, filename):
    path = os.path.dirname(os.path.abspath(__file__))
    df.to_csv(path + "/" + filename, header=True, index=False)


if __name__ == "__main__":
    filename = "dividend.csv"
    df = open_csv(filename)
    # print(df)
    data_df = data_process(df)
    # print(data_df)
    new_filename = "data_" + filename
    write_csv(df, new_filename)
