import pandas as pd
import requests
import json
import datetime

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
    "referer": "http://www.naver.com",
}


def get_number(number):
    negative = False
    if "(" in number:
        number = number.replace("(", "").replace(")", "")
        negative = True
    number = number.replace(",", "").replace("%", "").replace("$", "")
    if negative:
        return -float(number)
    else:
        return float(number)


def get_financial_info(ticker):
    url = (
        "https://seekingalpha.com/symbol/"
        + ticker
        + "/financials-data?period_type=annual&statement_type=income-statement&order_type=latest_right&is_pro=false"
    )
    req = requests.get(url, headers=headers)
    dataj = json.loads(req.content.decode("utf-8"))
    data = pd.DataFrame(dataj["data"])
    data_dict = {}
    for i in range(len(data.index)):
        for j in range(len(data.columns)):
            try:
                if data.iloc[i, j][0]["value"] in [
                    "Total Revenues",
                    "Selling General & Admin Expenses",
                    "R&D Expenses",
                    "Net Income",
                ]:
                    data_dict[data.iloc[i, j][0]["value"]] = data.iloc[i, j]
            except:
                pass
    order = ["Total Revenues", "Net Income", "Selling General & Admin Expenses", "R&D Expenses"]
    for item in order:
        if item in data_dict:
            if item == "Total Revenues":
                getter = "yoy_value"
            else:
                getter = "revenue_percent"
            data = data_dict[item]
            average_tmp = []
            for i in range(1, len(data)):
                try:
                    name = data[i]["name"]
                    yoy = data[i][getter]
                    yoy = get_number(yoy)
                    print(f"{item} {getter} {name}: {yoy}")
                    average_tmp.append(yoy)
                except:
                    pass
            year_3_average = average_tmp[-2] + average_tmp[-3] + average_tmp[-4]
            year_3_average /= 3
            print(f"{item} 3 year average {getter}: {round(year_3_average, 2)}\n")
        else:
            print(f"There is no {item} in data\n")


def get_balance_info(ticker):
    url = (
        "https://seekingalpha.com/symbol/"
        + ticker
        + "/financials-data?period_type=annual&statement_type=balance-sheet&order_type=latest_right&is_pro=false"
    )
    req = requests.get(url, headers=headers)
    dataj = json.loads(req.content.decode("utf-8"))
    data = pd.DataFrame(dataj["data"])
    data_dict = {}
    for i in range(len(data.index)):
        for j in range(len(data.columns)):
            try:
                if data.iloc[i, j][0]["value"] in [
                    "Total Cash & ST Investments",
                    "Total Receivables",
                    "Total Current Assets",
                    "Total Current Liabilities",
                    "Accounts Receivable",
                    "Accounts Payable",
                ]:
                    data_dict[data.iloc[i, j][0]["value"]] = data.iloc[i, j]
            except:
                pass
    cash = get_number(data_dict["Total Cash & ST Investments"][-2]["value"])
    receive = get_number(data_dict["Total Receivables"][-2]["value"])
    asset = get_number(data_dict["Total Current Assets"][-2]["value"])
    liab = get_number(data_dict["Total Current Liabilities"][-2]["value"])
    current_ratio = asset / liab * 100
    quick_ratio = (cash + receive) / liab * 100
    print(f"유동비율: {round(current_ratio, 2)}%")
    print(f"당좌비율: {round(quick_ratio, 2)}%\n")
    for i in range(1, len(data_dict["Accounts Receivable"])):
        try:
            name = data_dict["Accounts Receivable"][i]["name"]
            acre = data_dict["Accounts Receivable"][i]["asset_percent"]
            acre = get_number(acre)
            print(f"{name} Accounts Receivable: {round(acre, 2)}")
        except:
            pass
    print()
    for i in range(1, len(data_dict["Accounts Payable"])):
        try:
            name = data_dict["Accounts Payable"][i]["name"]
            acpay = data_dict["Accounts Payable"][i]["liability_percent"]
            acpay = get_number(acpay)
            print(f"{name} Accounts Payable: {round(acpay, 2)}")
        except:
            pass
    print()


def get_cash_info(ticker):
    url = (
        "https://seekingalpha.com/symbol/"
        + ticker
        + "/financials-data?period_type=annual&statement_type=cash-flow-statement&order_type=latest_right&is_pro=false"
    )
    req = requests.get(url, headers=headers)
    dataj = json.loads(req.content.decode("utf-8"))
    data = pd.DataFrame(dataj["data"])
    data_dict = {}
    for i in range(len(data.index)):
        for j in range(len(data.columns)):
            try:
                if data.iloc[i, j][0]["value"] in [
                    "Net Income",
                    "Cash from Operations",
                    "Cash from Investing",
                    "Cash from Financing",
                ]:
                    data_dict[data.iloc[i, j][0]["value"]] = data.iloc[i, j]
            except:
                pass
    order = [
        "Net Income",
        "Cash from Operations",
        "Cash from Investing",
        "Cash from Financing",
    ]
    for item in order:
        if item in data_dict:
            data = data_dict[item]
            average_tmp = []
            for i in range(1, len(data)):
                try:
                    name = data[i]["name"]
                    yoy = data[i]["value"]
                    yoy = get_number(yoy)
                    print(f"{item} {name}: {yoy}")
                    average_tmp.append(yoy)
                except:
                    pass
            year_3_average = average_tmp[-2] + average_tmp[-3] + average_tmp[-4]
            year_3_average /= 3
            print(f"{item} 3 year average: {round(year_3_average, 2)}\n")
        else:
            print(f"There is no {item} in data\n")


if __name__ == "__main__":
    ticker = "AMZN"
    ticker = ticker.upper()
    get_financial_info(ticker)
    get_balance_info(ticker)
    get_cash_info(ticker)
