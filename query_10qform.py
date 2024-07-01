import requests as req
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np

print('Initializing SEC query data program')

def main():

    
    stocks_watch = ['AAPL', 'MSFT', 'NVDA', 'AMZN', 'META','ADBE', 'GOOG', 'INTC']
    #stocks_watch = ['XOM', 'CVX', 'COP', 'EOG', 'SLB']

    dic_stockswatch = {}

    for stock in stocks_watch:
        dic_stockswatch[stock] = {
            'label': stock,
            'df_data': treat_data_from_10q(get_data_from_sec(stock), stock)['df_data'],
            'df_kpi': treat_data_from_10q(get_data_from_sec(stock), stock)['df_kpi']
        }
        print(dic_stockswatch[stock]['df_data'])
        print(dic_stockswatch[stock]['df_kpi'])
        # plt.figure(stock)
        # plt.plot(dic_stockswatch[stock]['df_kpi'])
        # plt.legend(dic_stockswatch[stock]['df_kpi'].columns)
        # plt.grid(True)
        
        #save to .csv
        #dic_stockswatch[stock]['df_data'].to_csv(stock, sep=';')
    
    plt.show()



def get_data_from_sec(ticker):
    #request header
    headers = {'User-Agent': "eng.gabrielcoutinho@outlook.com.br"}
    
    #company tickers
    df_tickers = pd.DataFrame.from_dict(req.get("https://www.sec.gov/files/company_tickers.json", headers=headers).json(), orient='index')
    #add leading zeros to the cik_str. In that way, CIK will match sec.gov api
    df_tickers['cik_str'] = df_tickers['cik_str'].astype(str).str.zfill(10)

    cik_tryout = df_tickers[df_tickers['ticker'] == ticker]
    cik = cik_tryout.cik_str[0]

    return req.get(f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json', headers=headers).json()['facts']['us-gaap']

def treat_data_from_10q(fillings_us_gaap, ticker):
    nonUSDkeys = []
    for element in fillings_us_gaap.values():
        try:
            element['units']['USD'] = [reg for reg in element['units']['USD'] if reg['form'] == '10-Q']        
            element['units']['shares'] = [reg for reg in element['units']['shares'] if reg['form'] == '10-Q']
            element['units']['USD/shares'] = [reg for reg in element['units']['USD/shares'] if reg['form'] == '10-Q']
        except:
            nonUSDkeys.append(element['label'])        

    ## Fundamental indicators calculation
    #necessary data from 10-Q

    fields2find = ['AssetsCurrent', 
                'LiabilitiesCurrent',
                'Liabilities',
                'InventoryNet', 
                'SalesRevenueNet',
                'Revenues', 
                'CostOfGoodsAndServicesSold',
                'CostOfRevenue',
                'CostsAndExpenses',
                'OperatingIncomeLoss',
                'NetIncomeLoss',
                'StockholdersEquity',
                'InterestExpense',
                'Assets',
                'AccountsReceivableNetCurrent',
                'CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents',
                'EarningsPerShareBasic'
                ]

    dic_10q_inputs = {}

    for field in fields2find:
        dic_10q_inputs[field] = {
            'label': 'blank description',
            'rawdata':{
                'value': [],
                'timestamp': []
            },
            'df': pd.DataFrame({})
            }
        try:
            dic_10q_inputs[field]['label'] = fillings_us_gaap[field]['label']
            if field == 'EarningsPerShareBasic':
                dic_10q_inputs[field]['rawdata']['value'] = [reg['val'] for reg in fillings_us_gaap[field]['units']['USD/shares'] if reg['form'] == '10-Q']
                dic_10q_inputs[field]['rawdata']['timestamp'] = [reg['end'] for reg in fillings_us_gaap[field]['units']['USD/shares'] if reg['form'] == '10-Q']
            else:    
                dic_10q_inputs[field]['rawdata']['value'] = [reg['val'] for reg in fillings_us_gaap[field]['units']['USD'] if reg['form'] == '10-Q']
                dic_10q_inputs[field]['rawdata']['timestamp'] = [reg['end'] for reg in fillings_us_gaap[field]['units']['USD'] if reg['form'] == '10-Q']
            dic_10q_inputs[field]['df'] = pd.DataFrame({field: dic_10q_inputs[field]['rawdata']['value'], 'timestamp': dic_10q_inputs[field]['rawdata']['timestamp']})
            dic_10q_inputs[field]['df'] = dic_10q_inputs[field]['df'].drop_duplicates(subset=['timestamp'])
            dic_10q_inputs[field]['df'] = dic_10q_inputs[field]['df'].set_index('timestamp')
        except:
            dic_10q_inputs[field]['label'] = 'data unavailable'

    timestamp_10q_df = []
    for input in dic_10q_inputs.keys():
        if len(timestamp_10q_df) < dic_10q_inputs[input]['df'].shape[0]:
            timestamp_10q_df = dic_10q_inputs[input]['df'].index
        

    df_10q_data = pd.DataFrame(index=timestamp_10q_df)

    for input in dic_10q_inputs.keys():
        df_10q_data = df_10q_data.merge(dic_10q_inputs[input]['df'], left_index=True, right_index= True, how='left')
        
    

    stock_prices = []
    prices_historical_data = yf.Ticker(ticker).history(start=datetime.strptime(list(df_10q_data.index)[0], "%Y-%m-%d")-timedelta(days=10), end=datetime.strptime(list(df_10q_data.index)[-1], "%Y-%m-%d"))['Close']
    for i in df_10q_data.index:
            
        #print(i, ' - ', prices_historical_data.loc[datetime.strptime(i, "%Y-%m-%d")-timedelta(days=5):datetime.strptime(i, "%Y-%m-%d")][-1])
        try:
            stock_prices.append(prices_historical_data.loc[datetime.strptime(i, "%Y-%m-%d")-timedelta(days=5):datetime.strptime(i, "%Y-%m-%d")][-1])
        except:
            stock_prices.append(np.nan)


    df_10q_data['stock_price'] = stock_prices

    df_10q_data = df_10q_data.sort_index()
    df_10q_data = df_10q_data.interpolate(method='linear', axis=0)



    for input in df_10q_data.columns:
        df_10q_data[input] = df_10q_data[input].fillna(df_10q_data[input].rolling(window=9, min_periods=1).mean())
    

    


    df_10q_kpi = pd.DataFrame(index=df_10q_data.index)

    try:
        df_10q_kpi['current_ratio'] = df_10q_data['AssetsCurrent']/df_10q_data['LiabilitiesCurrent']
    except:
        df_10q_kpi['current_ratio'] = 0
    try:
        df_10q_kpi['quick_ratio'] = (df_10q_data['AssetsCurrent'] - df_10q_data['InventoryNet'])/df_10q_data['LiabilitiesCurrent']
    except:
        df_10q_kpi['quick_ratio'] = 0

    try:
        try:
            df_10q_kpi['GrossMargin'] = (df_10q_data['SalesRevenueNet'] - df_10q_data['CostOfGoodsAndServicesSold'])/df_10q_data['SalesRevenueNet']
        except:
            df_10q_kpi['GrossMargin'] = (df_10q_data['Revenues'] - df_10q_data['CostOfRevenue'])/df_10q_data['Revenues']
    except:
        df_10q_kpi['GrossMargin'] = 0
    
    try:
        try:
            df_10q_kpi['OperatingMargin'] = df_10q_data['OperatingIncomeLoss']/df_10q_data['SalesRevenueNet']
        except:
            df_10q_kpi['OperatingMargin'] = df_10q_data['OperatingIncomeLoss']/df_10q_data['Revenues']
    except:
        df_10q_kpi['OperatingMargin'] = 0
        

    try:
        df_10q_kpi['roa'] = df_10q_data['NetIncomeLoss']/df_10q_data['AssetsCurrent']
    except:
        df_10q_kpi['roa'] = 0
    try:
        df_10q_kpi['roe'] = df_10q_data['NetIncomeLoss']/df_10q_data['StockholdersEquity']
    except:
        df_10q_kpi['roe'] = 0

    try:
        df_10q_kpi['debt_equity'] = df_10q_data['Liabilities']/df_10q_data['StockholdersEquity']
    except:
        df_10q_kpi['debt_equity'] = 0

    try:
        df_10q_kpi['interest_coverage'] = df_10q_data['OperatingIncomeLoss']/df_10q_data['InterestExpense']
    except:
        df_10q_kpi['interest_coverage'] = 0


    try:
        df_10q_kpi['assets_turnover'] = df_10q_data['Revenues']/df_10q_data['Assets']
    except:
        df_10q_kpi['assets_turnover'] = 0
    try:
        df_10q_kpi['receivable_turnover'] = df_10q_data['Revenues']/df_10q_data['AccountsReceivableNetCurrent']
    except:
        df_10q_kpi['receivable_turnover'] = 0
    try:
        df_10q_kpi['cash_netincome'] = df_10q_data['CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents']/df_10q_data['NetIncomeLoss']
    except:
        df_10q_kpi['cash_netincome'] = 0

    try:
        df_10q_kpi['eps'] = df_10q_data['EarningsPerShareBasic']
    except:
        df_10q_kpi['eps'] = 0

    try:
        df_10q_kpi['pe'] = df_10q_data['stock_price']/df_10q_kpi['eps']
    except:
        df_10q_kpi['pe'] = 0

    return {'df_data': df_10q_data,
            'df_kpi': df_10q_kpi.dropna()
            }


if __name__ == "__main__":
    main()