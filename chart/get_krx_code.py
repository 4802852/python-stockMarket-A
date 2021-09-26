import pandas as pd
import os
import datetime
import time

stock_type = {"kospi": "stockMkt", "kosdaq": "kosdaqMkt"}


def get_code(name):
    df = check_krx_data()
    code = df.query("회사명=='{}'".format(name))["종목코드"].to_string(index=False)
    if code == "Series([], )":
        print("한국 종목명을 확인하세요.")
        time.sleep(3)
        return -1
    code = code.strip()
    return code


def get_download_stock(market_type=None):
    market_type = stock_type[market_type]
    download_link = (
        "http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&marketType=" + market_type
    )
    df = pd.read_html(download_link, header=0)[0]
    return df


def get_download_kospi():
    df = get_download_stock("kospi")
    df.종목코드 = df.종목코드.map("{:06d}.KS".format)
    return df


def get_download_kosdaq():
    df = get_download_stock("kosdaq")
    df.종목코드 = df.종목코드.map("{:06d}.KQ".format)
    return df


def get_krx():
    kospi_df = get_download_kospi()
    kosdaq_df = get_download_kosdaq()
    code_df = pd.concat([kospi_df, kosdaq_df])
    code_df = code_df[["회사명", "종목코드"]]
    return code_df


def save_krx(df):
    now = datetime.datetime.now().strftime("%Y%m%d")
    path = os.path.dirname(os.path.abspath(__file__))
    filename = f"krx_{now}.csv"
    df.to_csv(path + "/" + filename, index=False)


def check_krx_data():
    path = os.path.dirname(os.path.abspath(__file__))
    files = os.listdir(path)
    for file in files[::-1]:
        if file[0:4] == "krx_":
            temp_year = int(file[4:8])
            temp_month = int(file[8:10])
            temp_day = int(file[10:12])
            file_datetime = datetime.date(temp_year, temp_month, temp_day)
            now_datetime = datetime.date.today()
            if (now_datetime - file_datetime) < datetime.timedelta(days=30):
                df = pd.read_csv(path + "/" + file)
                return df
    df = get_krx()
    save_krx(df)
    return df


def main():
    # ticker = input("Ticker: ")
    ticker = "123"
    code = get_code(ticker)
    # print(code)


if __name__ == "__main__":
    main()
