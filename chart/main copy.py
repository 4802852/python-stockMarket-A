import pandas_datareader as pdr
import matplotlib.pyplot as plt
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


def chart(df, ticker):
    fig, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw={"height_ratios": [2, 1]}, figsize=(10, 7))
    df.plot(kind="line", x="Date", y=["Close", "52High"], ax=ax1)
    df.plot(kind="line", x="Date", y="MDD", ax=ax2)
    ax1.grid(True, axis="y")
    ax1.set_xlabel("")
    ax1.set_ylabel("Price ($)")
    ax2.grid(True, axis="y")
    ax2.set_ylabel("MDD (%)")
    now = datetime.datetime.now().strftime("%Y-%m-%d")
    plt.savefig(f"{now}-{ticker}.png", bbox_inches="tight")
    plt.show()


def main():
    ticker = "AAPL"
    target = 5
    # ticker = input("Ticker: ").strip()
    # ticker = ticker.upper()
    # target = input("Target Year: ").strip()
    # if target == "":
    #     target = 5
    # else:
    #     target = int(target)
    df = get_base_data(ticker, target)
    print(df.head(10))
    # chart(df, ticker)


if __name__ == "__main__":
    main()
