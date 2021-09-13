import pandas_datareader as pdr
import matplotlib.pyplot as plt
import datetime
import requests
import json
import pandas as pd


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


def chart(ticker, df, eps_df, type):
    fig, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw={"height_ratios": [3, 1]}, figsize=(10, 7))
    columns = list(eps_df.columns)[3:]
    df.plot(kind="line", x="Date", y=["Close", "52High"], ax=ax1)
    df.plot(kind="line", x="Date", y="MDD", ax=ax2)
    if type == 2:
        colors = ["#BDFF95", "#95FFE2", "#95CFFF", "#959BFF", "#FF0000", "#CD95FF", "#FF95E7", "#95FFBD"]
        eps_df.plot(kind="line", x="name", y=columns, ax=ax1, color=colors, linewidth=1)
        eps_df.plot(kind="line", x="name", y=["zero"], ax=ax2, linewidth=0)
    ax1.grid(True, axis="y")
    ax1.set_xlabel("")
    ax1.set_ylabel("Price ($)")
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.spines["left"].set_visible(False)
    ax2.grid(True, axis="y")
    ax2.set_ylabel("MDD (%)")
    ax2.spines["top"].set_visible(False)
    ax2.spines["bottom"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.spines["left"].set_visible(False)
    ax2.get_xaxis().set_visible(False)
    ax2.get_legend().remove()
    now = datetime.datetime.now().strftime("%Y-%m-%d")
    plt.savefig(f"{now}-{ticker}.png", bbox_inches="tight")
    plt.show()


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
    per_array = [per_base * i / 5 for i in range(1, 8)] + [per]
    per_array = sorted(per_array)
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
        eps_df.loc[i + 1, "value"] = float(eps_df.loc[i + 1, "value"].replace("$", ""))

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


def main():
    # ticker = "AAPL"
    # target = 5
    ticker = input("Ticker: ").strip()
    ticker = ticker.upper()
    target = input("Target Year: ").strip()
    type = input("Type (1 for normal, 2 for PER band): ").strip()
    if type == '':
        type = 1
    else:
        type = int(type)
    if target == "":
        target = 5
    else:
        target = int(target)
    df = get_base_data(ticker, target)
    eps_df = get_per_band(ticker)
    chart(ticker, df, eps_df, type)


if __name__ == "__main__":
    main()
