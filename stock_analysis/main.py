from get_info import *
import time


def stock_analysis(ticker):
    get_sector_name(ticker)
    sector = input(
        "0: Sector median 1: Basic Materials, 2: Communication Services, 3: Consumer Cyclical, 4: Consumer Defensive, 5: Energy, 6: Financial, 7: Healthcare, 8: Industials, 9: Real Estate, 10: Technology, 11: Utilities\nSector number: "
    )
    print()
    time.sleep(0.5)
    get_per(ticker)
    time.sleep(0.2)
    get_psr(ticker)
    time.sleep(0.5)
    get_pbr_dividend(ticker)
    time.sleep(0.4)
    get_sector_per_psr(ticker)
    time.sleep(0.5)
    get_sector_peg(sector)
    time.sleep(1)
    get_margin(ticker)
    time.sleep(0.3)
    get_sector_margin(ticker)
    time.sleep(0.4)
    get_financial_info(ticker)
    time.sleep(0.7)
    get_balance_info(ticker)
    time.sleep(0.4)
    get_cash_info(ticker)
    time.sleep(0.3)
    get_price(ticker)


if __name__ == "__main__":
    ticker = input("Ticker: ")
    ticker = ticker.upper()
    stock_analysis(ticker)
