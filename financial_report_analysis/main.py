from get_info import *
import time


def get_info(ticker):
    get_financial_info(ticker)
    time.sleep(1)
    get_balance_info(ticker)
    time.sleep(1)
    get_cash_info(ticker)


if __name__ == "__main__":
    ticker = input("Ticker: ")
    ticker = ticker.upper()
    try:
        get_info(ticker)
    except ValueError:
        print(ValueError)
        print(f"Ticker Name {ticker} is not available")
