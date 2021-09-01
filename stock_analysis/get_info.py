import pandas as pd
import requests
import json
import datetime
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
    "referer": "http://www.naver.com",
}


def get_sector_name(ticker):
    url = (
        "https://seekingalpha.com/api/v3/symbol_data?fields[]=long_desc&fields[]=sectorname&fields[]=sectorgics&fields[]=primaryname&fields[]=primarygics&fields[]=numberOfEmployees&fields[]=yearfounded&fields[]=streetaddress&fields[]=streetaddress2&fields[]=streetaddress3&fields[]=streetaddress4&fields[]=city&fields[]=state&fields[]=zipcode&fields[]=country&fields[]=officephonevalue&fields[]=webpage&fields[]=company_name&fields[]=marketCap&fields[]=totalEnterprise&fields[]=totAnalystsRecommendations&slugs=TSLA%2CTM%2CDDAIF%2CGM%2CNIO%2CHMChttps://seekingalpha.com/api/v3/symbol_data?fields[]=long_desc&fields[]=sectorname&fields[]=sectorgics&fields[]=primaryname&fields[]=primarygics&fields[]=numberOfEmployees&fields[]=yearfounded&fields[]=streetaddress&fields[]=streetaddress2&fields[]=streetaddress3&fields[]=streetaddress4&fields[]=city&fields[]=state&fields[]=zipcode&fields[]=country&fields[]=officephonevalue&fields[]=webpage&fields[]=company_name&fields[]=marketCap&fields[]=totalEnterprise&fields[]=totAnalystsRecommendations&slugs="
        + ticker
    )
    req = requests.get(url, headers=headers).content
    dataj = json.loads(req.decode("utf-8"))
    data = pd.DataFrame(dataj["data"][0]["attributes"], index=[ticker]).transpose()
    name = data.loc["sectorname", ticker]
    print(f"sector name: {name}\n")


def get_per(ticker):
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
        print(f"EPS Growth {year + i}: {round(yoy, 2)}%")
    per_fwd = eps_data.loc[year, "fwd"]
    print(f"P/E(fwd): {per_fwd}%\n")


def get_psr(ticker):
    url = (
        "https://seekingalpha.com/symbol/"
        + ticker
        + "/earnings/estimates_data?data_type=revenue&unit=earning_estimates"
    )
    req = requests.get(url, headers=headers).content
    dataj = json.loads(req.decode("utf-8"))
    eps_data = pd.DataFrame(dataj["annual"]).transpose()
    eps_data.sort_values("fiscalYear", inplace=True)
    eps_data.set_index("fiscalYear", inplace=True)
    year = int(datetime.datetime.now().strftime("%Y"))
    for i in range(5):
        yoy = eps_data.loc[year + i, "yoy"]
        print(f"Sales Growth {year + i}: {round(yoy, 2)}%")
    ps_fwd = eps_data.loc[year, "fwd"]
    print(f"P/S(fwd): {ps_fwd}%\n")


def get_pbr_dividend(ticker):
    url = (
        "https://seekingalpha.com/api/v3/symbols/"
        + ticker
        + "/metrics?filter[fields][]=pe_nongaap&filter[fields][]=pe_nongaap_fy1&filter[fields][]=pe_ratio&filter[fields][]=pe_gaap_fy1&filter[fields][]=peg_gaap&filter[fields][]=peg_nongaap_fy1&filter[fields][]=ev_12m_sales_ratio&filter[fields][]=ev_sales_fy1&filter[fields][]=ev_ebitda&filter[fields][]=ev_ebitda_fy1&filter[fields][]=ev_ebit&filter[fields][]=ev_ebit_fy1&filter[fields][]=ps_ratio&filter[fields][]=ps_ratio_fy1&filter[fields][]=pb_ratio&filter[fields][]=pb_fy1_ratio&filter[fields][]=price_cf_ratio&filter[fields][]=price_cf_ratio_fy1&filter[fields][]=dividend_yield"
    )
    req = requests.get(url, headers=headers).content
    dataj = json.loads(req.decode("utf-8"))
    pbr = dataj["data"][15]["attributes"]["value"]
    dividend = dataj["data"][18]["attributes"]["value"]
    print(f"PBR(fwd): {round(pbr, 2)}")
    print(f"Dividend Yield: {round(dividend, 2)}")


def get_sector_per_psr(ticker):
    url = (
        "https://seekingalpha.com/api/v3/symbols/"
        + ticker
        + "/sector_metrics?filter[fields][]=pe_nongaap&filter[fields][]=pe_nongaap_fy1&filter[fields][]=pe_ratio&filter[fields][]=pe_gaap_fy1&filter[fields][]=peg_gaap&filter[fields][]=peg_nongaap_fy1&filter[fields][]=ev_12m_sales_ratio&filter[fields][]=ev_sales_fy1&filter[fields][]=ev_ebitda&filter[fields][]=ev_ebitda_fy1&filter[fields][]=ev_ebit&filter[fields][]=ev_ebit_fy1&filter[fields][]=ps_ratio&filter[fields][]=ps_ratio_fy1&filter[fields][]=pb_ratio&filter[fields][]=pb_fy1_ratio&filter[fields][]=price_cf_ratio&filter[fields][]=price_cf_ratio_fy1&filter[fields][]=dividend_yield"
    )
    req = requests.get(url, headers=headers).content
    dataj = json.loads(req.decode("utf-8"))
    sector_per = dataj["data"][13]["attributes"]["value"]
    sector_psr = dataj["data"][18]["attributes"]["value"]
    sector_pbr = dataj["data"][7]["attributes"]["value"]
    print(f"Sector P/E(fwd): {round(sector_per, 2)}")
    print(f"Sector P/S(fwd): {round(sector_psr, 2)}")
    print(f"Sector P/B(fwd): {round(sector_pbr, 2)}")
    time.sleep(0.5)
    url = (
        "https://seekingalpha.com/api/v3/symbols/"
        + ticker
        + "/sector_metrics?filter[fields][]=revenue_growth&filter[fields][]=revenue_change_display&filter[fields][]=ebitda_yoy&filter[fields][]=ebitda_change_display&filter[fields][]=operating_income_ebit_yoy&filter[fields][]=ebit_change_display&filter[fields][]=diluted_eps_growth&filter[fields][]=eps_change_display&filter[fields][]=eps_ltg&filter[fields][]=levered_free_cash_flow_yoy&filter[fields][]=fcf_per_share_change_display&filter[fields][]=op_cf_yoy&filter[fields][]=cf_op_change_display&filter[fields][]=roe_yoy&filter[fields][]=roe_change_display&filter[fields][]=working_cap_change&filter[fields][]=capex_change&filter[fields][]=dividend_per_share_change_dislpay&filter[fields][]=dps_yoy"
    )
    req = requests.get(url, headers=headers).content
    dataj = json.loads(req.decode("utf-8"))
    data_fwd = pd.DataFrame(dataj["data"][14])
    secter_median_revenue_growth = data_fwd.loc["value", "attributes"]
    print(f"Sector PSG(fwd): {round(sector_psr*secter_median_revenue_growth, 2)}\n")


def get_margin(ticker):
    url = (
        "https://seekingalpha.com/symbol/"
        + ticker
        + "/financials-data?period_type=annual&statement_type=income-statement&order_type=latest_right&is_pro=false"
    )
    req = requests.get(url, headers=headers).content
    dataj = json.loads(req.decode("utf-8"))
    data = pd.DataFrame(dataj["data"][1][-1]).transpose()
    columns = data.loc["name"]
    data.drop("name", inplace=True)
    data.columns = columns
    text = data.loc["value", "Operating Expenses & Income"]
    yoy = list(data.loc["revenue_percent"])
    for i in range(3):
        print(f"{text} {list(columns)[-1 - i]}: {yoy[-1 - i]}")


def get_sector_margin(ticker):
    url = (
        "https://seekingalpha.com/api/v3/symbols/"
        + ticker
        + "/sector_metrics?filter[fields][]=gross_margin&filter[fields][]=ebit_margin&filter[fields][]=ebitda_margin&filter[fields][]=net_margin&filter[fields][]=levered_fcf_margin&filter[fields][]=rtn_on_common_equity&filter[fields][]=return_on_total_capital&filter[fields][]=return_on_avg_tot_assets&filter[fields][]=capex_to_sales&filter[fields][]=assets_turnover&filter[fields][]=cash_from_operations_as_reported&filter[fields][]=net_inc_per_employee"
    )
    req = requests.get(url, headers=headers).content
    dataj = json.loads(req.decode("utf-8"))
    data = pd.DataFrame(dataj["data"][4])
    secter_median_operating_margin = data.loc["value", "attributes"]
    print(f"Secter Median Operating Margin: {round(secter_median_operating_margin, 2)}\n")


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
                    "Selling General & Admin Expenses",
                    "R&D Expenses",
                ]:
                    data_dict[data.iloc[i, j][0]["value"]] = data.iloc[i, j]
            except:
                pass
    order = ["Selling General & Admin Expenses", "R&D Expenses"]
    for item in order:
        if item in data_dict:
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
                    "Total Equity",
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
    equity = get_number(data_dict["Total Equity"][-2]["value"])
    debt_equity = liab / equity * 100
    current_ratio = asset / liab * 100
    quick_ratio = (cash + receive) / liab * 100
    print(f"부채비율: {round(debt_equity, 2)}%")
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
                    "Net Change in Cash",
                ]:
                    data_dict[data.iloc[i, j][0]["value"]] = data.iloc[i, j]
            except:
                pass
    order = [
        "Net Income",
        "Cash from Operations",
        "Cash from Investing",
        "Cash from Financing",
        "Net Change in Cash",
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
    ticker = "msft"
    ticker = ticker.upper()
    get_sector_per_psr(ticker)
    # get_financial_info(ticker)
    # get_balance_info(ticker)
    # get_cash_info(ticker)
