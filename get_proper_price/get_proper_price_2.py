import pandas as pd
import requests
import json
import datetime
import time

from get_proper_price import get_sector_name, get_price


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
    "referer": "http://www.naver.com",
}


def get_proper_price_revenue(ticker):
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
        print(f"Sales Growth {year + i}: {round(yoy, 2)}")
    ps_fwd = eps_data.loc[year, "fwd"]
    print(f"P/S(fwd): {ps_fwd}")


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


def get_sector_psg(ticker):
    url = (
        "https://seekingalpha.com/api/v3/symbols/"
        + ticker
        + "/sector_metrics?filter[fields][]=revenue_growth&filter[fields][]=revenue_change_display&filter[fields][]=ebitda_yoy&filter[fields][]=ebitda_change_display&filter[fields][]=operating_income_ebit_yoy&filter[fields][]=ebit_change_display&filter[fields][]=diluted_eps_growth&filter[fields][]=eps_change_display&filter[fields][]=eps_ltg&filter[fields][]=levered_free_cash_flow_yoy&filter[fields][]=fcf_per_share_change_display&filter[fields][]=op_cf_yoy&filter[fields][]=cf_op_change_display&filter[fields][]=roe_yoy&filter[fields][]=roe_change_display&filter[fields][]=working_cap_change&filter[fields][]=capex_change&filter[fields][]=dividend_per_share_change_dislpay&filter[fields][]=dps_yoy"
    )
    req = requests.get(url, headers=headers).content
    dataj = json.loads(req.decode("utf-8"))
    data_fwd = pd.DataFrame(dataj["data"][14])
    secter_median_revenue_growth = data_fwd.loc["value", "attributes"]
    print(f"Secter Median Growth: {round(secter_median_revenue_growth, 2)}")
    time.sleep(0.5)
    url = (
        "https://seekingalpha.com/api/v3/symbols/"
        + ticker
        + "/sector_metrics?filter[fields][]=pe_nongaap&filter[fields][]=pe_nongaap_fy1&filter[fields][]=pe_ratio&filter[fields][]=pe_gaap_fy1&filter[fields][]=peg_gaap&filter[fields][]=peg_nongaap_fy1&filter[fields][]=ev_12m_sales_ratio&filter[fields][]=ev_sales_fy1&filter[fields][]=ev_ebitda&filter[fields][]=ev_ebitda_fy1&filter[fields][]=ev_ebit&filter[fields][]=ev_ebit_fy1&filter[fields][]=ps_ratio&filter[fields][]=ps_ratio_fy1&filter[fields][]=pb_ratio&filter[fields][]=pb_fy1_ratio&filter[fields][]=price_cf_ratio&filter[fields][]=price_cf_ratio_fy1&filter[fields][]=dividend_yield"
    )
    req = requests.get(url, headers=headers).content
    dataj = json.loads(req.decode("utf-8"))
    data_ttm = pd.DataFrame(dataj["data"][17])
    data_fwd = pd.DataFrame(dataj["data"][18])
    secter_median_psg_ttm = data_ttm.loc["value", "attributes"]
    secter_median_psg_fwd = data_fwd.loc["value", "attributes"]
    print(f"Secter Median PSG TTM: {round(secter_median_psg_ttm, 2)}")
    print(f"Secter Median PSG FWD: {round(secter_median_psg_fwd, 2)}")
    time.sleep(0.5)
    url = (
        "https://seekingalpha.com/api/v3/symbols/"
        + ticker
        + "/sector_metrics?filter[fields][]=gross_margin&filter[fields][]=ebit_margin&filter[fields][]=ebitda_margin&filter[fields][]=net_margin&filter[fields][]=levered_fcf_margin&filter[fields][]=rtn_on_common_equity&filter[fields][]=return_on_total_capital&filter[fields][]=return_on_avg_tot_assets&filter[fields][]=capex_to_sales&filter[fields][]=assets_turnover&filter[fields][]=cash_from_operations_as_reported&filter[fields][]=net_inc_per_employee"
    )
    req = requests.get(url, headers=headers).content
    dataj = json.loads(req.decode("utf-8"))
    data = pd.DataFrame(dataj["data"][4])
    secter_median_operating_margin = data.loc["value", "attributes"]
    print(f"Secter Median Operating Margin: {round(secter_median_operating_margin, 2)}")


if __name__ == "__main__":
    ticker = "amd"
    ticker = ticker.upper()
    # get_sector_name(ticker)
    # get_proper_price_revenue(ticker)
    # get_margin(ticker)
    get_sector_psg(ticker)
    # get_price(ticker)
