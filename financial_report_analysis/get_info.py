import pandas as pd
import requests
import json
import datetime

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
    "referer": "http://www.naver.com",
}

def get_financial_info(ticker):
    url = "https://seekingalpha.com/symbol/" + ticker + "/financials-data?period_type=annual&statement_type=income-statement&order_type=latest_right&is_pro=false"
    req = requests.get(url, headers=headers)
    dataj = json.loads(req.content.decode("utf-8"))
    data = pd.DataFrame(dataj['data'])
    for i in range(len(data.index)):
        for j in range(len(data.columns)):
            try:
                if 'Total Revenue' in data.iloc[i, j][0]['value']:
                    data2 = data.iloc[i, j]
                elif 'Selling' in data.iloc[i, j][0]['value']:
                    data3 = data.iloc[i, j]
                elif 'R&D Expenses' in data.iloc[i, j][0]['value']:
                    data4 = data.iloc[i, j]
            except:
                pass
    average_tmp = []
    for i in range(1, len(data2)):
        try:
            name = data2[i]['name']
            yoy = data2[i]['yoy_value']
            if '(' in yoy:
                yoy = -float(yoy[1:-2])
            else:
                yoy = float(yoy[:-1])
            print(f'{name} Revenue YoY: {yoy}')
            average_tmp.append(yoy)
        except:
            pass
    year_3_average = average_tmp[-2] + average_tmp[-3] + average_tmp[-4]
    year_3_average /= 3
    print(f'3 year average Revenue YoY: {round(year_3_average, 2)}\n')
    average_tmp = []
    for i in range(1, len(data3)):
        try:
            name = data3[i]['name']
            sgae = data3[i]['revenue_percent']
            if '(' in sgae:
                sgae = -float(sgae[1:-2])
            else:
                sgae = float(sgae[:-1])
            print(f'{name} Selling General & Admin Expense: {sgae}')
            average_tmp.append(sgae)
        except:
            pass
    year_3_average = average_tmp[-2] + average_tmp[-3] + average_tmp[-4]
    year_3_average /= 3
    print(f'3 year average Selling General & Admin Expense: {round(year_3_average, 2)}\n')
    average_tmp = []
    for i in range(1, len(data4)):
        try:
            name = data4[i]['name']
            rd = data4[i]['revenue_percent']
            if '(' in rd:
                rd = -float(rd[1:-2])
            else:
                rd = float(rd[:-1])
            print(f'{name} R&D Expense: {rd}')
            average_tmp.append(rd)
        except:
            pass
    year_3_average = average_tmp[-2] + average_tmp[-3] + average_tmp[-4]
    year_3_average /= 3
    print(f'3 year average R&D Expense: {round(year_3_average, 2)}\n')


def get_balance_info(ticker):
    url = 'https://seekingalpha.com/symbol/' + ticker + '/financials-data?period_type=annual&statement_type=balance-sheet&order_type=latest_right&is_pro=false'
    req = requests.get(url, headers=headers)
    dataj = json.loads(req.content.decode("utf-8"))
    data = pd.DataFrame(dataj['data'])
    for i in range(len(data.index)):
        for j in range(len(data.columns)):
            try:
                if 'Total Cash' in data.iloc[i, j][0]['value']:
                    data2 = data.iloc[i, j]
                elif 'Total Receivables' in data.iloc[i, j][0]['value']:
                    data3 = data.iloc[i, j]
                elif 'Total Current Assets' in data.iloc[i, j][0]['value']:
                    data4 = data.iloc[i, j]
                elif 'Total Current Liabilities' in data.iloc[i, j][0]['value']:
                    data5 = data.iloc[i, j]
                elif 'Accounts Receivable' in data.iloc[i, j][0]['value']:
                    data6 = data.iloc[i,j]
                elif 'Accounts Payable' in data.iloc[i, j][0]['value']:
                    data7 = data.iloc[i,j]
            except:
                pass
    cash = float(data2[-2]['value'])
    receive = float(data3[-2]['value'])
    asset = float(data4[-2]['value'])
    liab = float(data5[-2]['value'])
    current_ratio = asset / liab * 100
    quick_ratio = (cash + receive) / liab * 100
    print(f'유동비율: {current_ratio}%')
    print(f'당좌비율: {quick_ratio}%\n')
    for i in range(1, len(data6)):
        try:
            name = data6[i]['name']
            acre = data6[i]['asset_percent']
            if '(' in acre:
                acre = -float(acre[1:-2])
            else:
                acre = float(acre[:-1])
            print(f'{name} Accounts Receivable: {round(acre, 2)}')
        except:
            pass
    for i in range(1, len(data7)):
        try:
            name = data7[i]['name']
            acpay = data7[i]['liability_percent']
            if '(' in acpay:
                acpay = -float(acpay[1:-2])
            else:
                acpay = float(acpay[:-1])
            print(f'{name} Accounts Payable: {round(acpay, 2)}')
        except:
            pass
    

def get_cash_info(ticker):
    url = "https://seekingalpha.com/symbol/" + ticker + "/financials-data?period_type=annual&statement_type=cash-flow-statement&order_type=latest_right&is_pro=false"
    req = requests.get(url, headers=headers)
    dataj = json.loads(req.content.decode("utf-8"))
    data = pd.DataFrame(dataj['data'])
    for i in range(len(data.index)):
        for j in range(len(data.columns)):
            try:
                if 'Net Income' in data.iloc[i, j][0]['value']:
                    data2 = data.iloc[i, j]
                elif 'Cash from Operations' in data.iloc[i, j][0]['value']:
                    data3 = data.iloc[i, j]
                elif 'Free Cash Flow' in data.iloc[i, j][0]['value']:
                    data4 = data.iloc[i, j]
            except:
                pass
    for i in range(1, len(data2)):
        try:
            name = data2[i]['name']
            netin = data2[i]['value']
            if '(' in netin:
                netin = -float(netin[1:-2])
            else:
                netin = float(netin[:-1])
            print(f'{name} Net Income: {netin}')
        except:
            pass
    for i in range(1, len(data3)):
        try:
            name = data3[i]['name']
            cashop = data3[i]['value']
            if '(' in cashop:
                cashop = -float(cashop[1:-2])
            else:
                cashop = float(cashop[:-1])
            print(f'{name} Cash from Operationss: {cashop}')
        except:
            pass    
    print(data4)
    for i in range(1, len(data4)):
        try:
            name = data4[i]['name']
            freecash = data4[i]['value']
            if '(' in freecash:
                freecash = -float(freecash[2:-1])
            else:
                freecash = float(freecash[1:])
            print(f'{name} Free Cash Flow/Share: {freecash}')
        except:
            pass  


if __name__ == '__main__':
    ticker = 'chpt'
    ticker = ticker.upper()
    # get_financial_info(ticker)
    # get_balance_info(ticker)
    get_cash_info(ticker)