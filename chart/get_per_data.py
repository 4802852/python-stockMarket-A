import requests
import json
import pandas as pd
import datetime

from common_tools import *


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
    "referer": "https://seekingalpha.com/",
}


def get_per_array(ticker):
    url = (
        "https://seekingalpha.com/api/v3/symbols/"
        + ticker
        + "/metrics?filter[fields][]=pe_nongaap&filter[fields][]=pe_nongaap_fy1&filter[fields][]=pe_ratio&filter[fields][]=pe_gaap_fy1&filter[fields][]=peg_gaap&filter[fields][]=peg_nongaap_fy1&filter[fields][]=ev_12m_sales_ratio&filter[fields][]=ev_sales_fy1&filter[fields][]=ev_ebitda&filter[fields][]=ev_ebitda_fy1&filter[fields][]=ev_ebit&filter[fields][]=ev_ebit_fy1&filter[fields][]=ps_ratio&filter[fields][]=ps_ratio_fy1&filter[fields][]=pb_ratio&filter[fields][]=pb_fy1_ratio&filter[fields][]=price_cf_ratio&filter[fields][]=price_cf_ratio_fy1&filter[fields][]=dividend_yield"
    )
    req = requests.get(url, headers=headers).content
    dataj = json.loads(req.decode("utf-8"))
    per = round(dataj["data"][1]["attributes"]["value"], 2)
    per_base = round(per, -1)
    per_array = [per] + [per_base * i / 5 for i in range(1, 8)]
    return per_array


def get_eps_df(ticker):
    url = (
        "https://seekingalpha.com/symbol/"
        + ticker
        + "/financials-data?period_type=annual&statement_type=income-statement&order_type=latest_right&is_pro=true"
    )
    req = requests.get(url, headers=headers).content
    dataj = json.loads(req.decode("utf-8"))
    eps_df = dataj["data"][4][1]
    eps_df = pd.DataFrame(eps_df).drop(0)[::-1].reset_index().drop(0).drop(["index"], axis=1)
    eps_df = eps_df[["name", "value"]][:5]
    month_dict = {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12,
    }
    for i in range(len(eps_df)):
        month, year = eps_df.loc[i + 1, "name"].split(" ")
        time_tmp = datetime.datetime(int(year), month_dict[month], 1)
        eps_df.loc[i + 1, "name"] = time_tmp
        eps_temp = get_number(eps_df.loc[i + 1, "value"])
        eps_df.loc[i + 1, "value"] = eps_temp if eps_temp > 0 else 0

    url = (
        "https://seekingalpha.com/symbol/"
        + ticker
        + "/earnings/estimates_data?data_type=eps&unit=earning_estimates"
    )
    req = requests.get(url, headers=headers)
    dataj = json.loads(req.content.decode("utf-8"))
    eps_data = pd.DataFrame(dataj["annual"]).transpose()
    eps_data.sort_values("fiscalYear", inplace=True)
    eps_data.set_index("fiscalYear", inplace=True)
    year = int(datetime.datetime.now().strftime("%Y"))
    for i in range(3):
        time_tmp = datetime.datetime(year, month_dict[month], 1)
        eps_df.loc[6 + i] = [time_tmp, round(eps_data.loc[year, "estimate"], 2)]
        year += 1
    eps_df = eps_df.sort_values(by="name")
    eps_df["zero"] = 0
    return eps_df.reset_index().drop("index", axis=1)


def get_per_band(ticker):
    per_array = get_per_array(ticker)
    eps_df = get_eps_df(ticker)
    for per_value in per_array:
        eps_df[f"{per_value}"] = eps_df["value"] * per_value
    return eps_df
