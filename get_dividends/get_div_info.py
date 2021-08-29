import requests
import json


def get_div_info(ticker):
    print(f"Getting {ticker} information...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
        "referer": "https://seekingalpha.com/symbol/" + ticker + "/dividends/scorecard",
    }
    # price info
    url = "https://finance.api.seekingalpha.com/v2/real-time-prices?symbols=" + ticker
    req = requests.get(url, headers=headers)
    try:
        dataj = json.loads(req.content.decode("utf-8"))
        data = dataj["data"][0]["attributes"]
        price_last = data["last"]
        price_52high = data["high52Week"]
        price_fall = str(round((price_last - price_52high) / price_52high, 2)) + "%"
        price_info = [price_last, price_52high, price_fall]
    except:
        price_info = None
    # dividend info
    url = (
        "https://seekingalpha.com/api/v3/symbol_data?fields[]=divYieldFwd&fields[]=divRate&fields[]=payoutRatio&fields[]=divGrowRate5&fields[]=dividendGrowth&fields[]=divYieldTtm&fields[]=divDistribution&fields[]=dividends&slugs="
        + ticker
    )
    # url = (
    #     "https://seekingalpha.com/api/v3/symbol_data?fields[]=divYield&fields[]=divYieldFwd&fields[]=divRate&fields[]=payoutRatio&fields[]=divGrowRate5&fields[]=dividendGrowth&fields[]=divYieldTtm&fields[]=divDistribution&fields[]=dividends&slugs="
    #     + ticker
    # )
    req = requests.get(url, headers=headers)
    print(req)
    try:
        dataj = json.loads(req.content.decode("utf-8"))
        print(dataj)
        data = dataj["data"][0]["attributes"]
        div_yield = round(data["divYieldFwd"], 2)
        div_rate = data["divRate"]
        div_growth = round(data["divGrowRate5"], 2)
        div_growth_year = data["dividendGrowth"]
        div_info = [div_yield, div_rate, div_growth, div_growth_year]
    except:
        div_info = None
    return price_info, div_info


if __name__ == "__main__":
    ticker = "aapl"
    ticker = ticker.upper()
    try:
        result = get_div_info(ticker)
        print(result)
    except:
        print(f"No ticker {ticker} available")
