import pandas_datareader as pdr
import datetime


def get_base_data(ticker, target=10):
    end = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    start = end.replace(year=end.year - target - 1)
    df = pdr.DataReader(ticker, "yahoo", start, end)
    df = df.reset_index()
    df[["52High", "MDD"]] = 0
    high_list = []
    len_high_list = 0
    for i in range(len(df)):
        if len_high_list <= 250:
            high_list.append(df.loc[i, "High"])
            len_high_list += 1
            df.loc[i, "52High"] = max(high_list)
        else:
            high_list.pop(0)
            high_list.append(df.loc[i, "High"])
            df.loc[i, "52High"] = max(high_list)
        df.loc[i, "MDD"] = (df.loc[i, "Close"] - df.loc[i, "52High"]) / df.loc[i, "52High"] * 100
    start = start.replace(year=end.year - target)
    for i in range(270):
        if df.loc[i, "Date"] < start:
            df = df.drop([i])
    return df
