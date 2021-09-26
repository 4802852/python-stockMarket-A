import matplotlib.pyplot as plt
import datetime

from get_price_data import *
from get_per_data import *
from get_krx_code import *


def chart(ticker, df, eps_df, type):
    fig, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw={"height_ratios": [3, 1]}, figsize=(10, 7))
    df.plot(kind="line", x="Date", y=["Close", "52High"], ax=ax1)
    df.plot(kind="line", x="Date", y="MDD", ax=ax2)
    if type == 2:
        columns = list(eps_df.columns)[3:]
        colors = [
            "#FF0000",
            "#BDFF95",
            "#95FFE2",
            "#95CFFF",
            "#959BFF",
            "#CD95FF",
            "#FF95E7",
            "#95FFBD",
        ]
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
    if type == 2:
        plt.savefig(f"{now}-{ticker}-PERband.png", bbox_inches="tight")
    else:
        plt.savefig(f"{now}-{ticker}.png", bbox_inches="tight")
    plt.show()


def chart_k(stock_name, df):
    fig, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw={"height_ratios": [3, 1]}, figsize=(10, 7))
    df.plot(kind="line", x="Date", y=["Close", "52High"], ax=ax1)
    df.plot(kind="line", x="Date", y="MDD", ax=ax2)
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
    plt.savefig(f"{now}-{stock_name}.png", bbox_inches="tight")
    plt.show()


def main():
    # ticker = "AAPL"
    # target = 5
    country = input("Country(1 for America, 2 for Korea): ").strip()
    if country == "":
        country = 1
    else:
        country = int(country)
    if country == 1:
        ticker = input("Ticker: ").strip()
        ticker = ticker.upper()
        target = input("Target Year: ").strip()
        type = input("Type (1 for normal, 2 for PER band): ").strip()
    elif country == 2:
        stock_name = input("종목명: ").strip()
        ticker = get_code(stock_name)
        if ticker == -1:
            return
        target = input("Target Year: ").strip()
        type = 1
    if type == "":
        type = 1
    else:
        type = int(type)
    if target == "":
        target = 5
    else:
        target = int(target)
    df = get_base_data(ticker, target)
    if type == 2:
        eps_df = get_per_band(ticker)
    else:
        eps_df = None
    if country == 1:
        chart(ticker, df, eps_df, type)
    elif country == 2:
        chart_k(stock_name, df)


if __name__ == "__main__":
    main()
