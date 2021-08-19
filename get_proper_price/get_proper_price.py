import pandas as pd
import requests
import json
import datetime


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
    "referer": "http://www.naver.com",
}


def get_proper_price(ticker):
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
        yoy = eps_data.loc[year + i, "yoy"]
        print(f"EPS Growth {year + i}: {round(yoy, 2)}")
    per_fwd = eps_data.loc[year, "fwd"]
    print(f"P/E(fwd): {per_fwd}")


def get_sector_name(ticker):
    url = (
        "https://seekingalpha.com/api/v3/symbol_data?fields[]=long_desc&fields[]=sectorname&fields[]=sectorgics&fields[]=primaryname&fields[]=primarygics&fields[]=numberOfEmployees&fields[]=yearfounded&fields[]=streetaddress&fields[]=streetaddress2&fields[]=streetaddress3&fields[]=streetaddress4&fields[]=city&fields[]=state&fields[]=zipcode&fields[]=country&fields[]=officephonevalue&fields[]=webpage&fields[]=company_name&fields[]=marketCap&fields[]=totalEnterprise&fields[]=totAnalystsRecommendations&slugs=TSLA%2CTM%2CDDAIF%2CGM%2CNIO%2CHMChttps://seekingalpha.com/api/v3/symbol_data?fields[]=long_desc&fields[]=sectorname&fields[]=sectorgics&fields[]=primaryname&fields[]=primarygics&fields[]=numberOfEmployees&fields[]=yearfounded&fields[]=streetaddress&fields[]=streetaddress2&fields[]=streetaddress3&fields[]=streetaddress4&fields[]=city&fields[]=state&fields[]=zipcode&fields[]=country&fields[]=officephonevalue&fields[]=webpage&fields[]=company_name&fields[]=marketCap&fields[]=totalEnterprise&fields[]=totAnalystsRecommendations&slugs="
        + ticker
    )
    req = requests.get(url, headers=headers).content
    dataj = json.loads(req.decode("utf-8"))
    data = pd.DataFrame(dataj["data"][0]["attributes"], index=[ticker]).transpose()
    name = data.loc["sectorname", ticker]
    print(f"sector name: {name}")


def get_price(ticker):
    url = "https://finance.api.seekingalpha.com/v2/real-time-prices?symbols%5B%5D=" + ticker
    req = requests.get(url, headers=headers).content
    dataj = json.loads(req.decode("utf-8"))
    data = pd.DataFrame(dataj["data"][0]["attributes"], index=[ticker]).transpose()
    high52Week = data.loc["high52Week", ticker]
    now_price = data.loc["last", ticker]
    print(f"high52Week: {high52Week}")
    print(f"now price: {now_price}")


def get_sector_peg():
    url = "https://finviz.com/groups.ashx?g=sector&v=120&o=name"
    req = requests.get(url, headers=headers)
    data = pd.read_html(req.text)[4]
    columns = data.loc[0]
    data.drop(0, inplace=True)
    data.columns = columns
    data.set_index("No.", inplace=True)
    for i in range(len(data)):
        print(
            "Average PEG {}: {}".format(data.loc[str(i + 1), "Name"], data.loc[str(i + 1), "PEG"])
        )


if __name__ == "__main__":
    ticker = "amd"
    ticker = ticker.upper()
    get_sector_name(ticker)
    get_proper_price(ticker)
    get_price(ticker)
    print()
    get_sector_peg()
