from get_proper_price import *
from get_proper_price_2 import *
import time


def get_by_EPS(ticker):
    get_sector_name(ticker)
    time.sleep(0.5)
    get_proper_price(ticker)
    time.sleep(0.5)
    get_price(ticker)
    print()
    time.sleep(0.5)
    get_sector_peg()


def get_by_revenue(ticker):
    get_sector_name(ticker)
    time.sleep(0.5)
    get_proper_price_revenue(ticker)
    time.sleep(0.5)
    get_margin(ticker)
    time.sleep(0.5)
    get_sector_psg(ticker)
    time.sleep(0.5)
    get_price(ticker)


if __name__ == "__main__":
    ticker = input("Ticker: ")
    ticker = ticker.upper()
    get_type = input("Get Type(1 by EPS, 2 by Revenue): ").strip()
    if get_type == "1":
        try:
            get_by_EPS(ticker)
        except ValueError:
            print(ValueError)
            print(f"Ticker Name {ticker} is not available")
    elif get_type == "2":
        try:
            get_by_revenue(ticker)
        except ValueError:
            print(ValueError)
            print(f"Ticker Name {ticker} is not available")
