import requests as req
import pandas as pd
import json
from datetime import datetime
import matplotlib.pyplot as plt

print('Initializing SEC query data program')

def main():
    #stocks_watch = ['AAPL', 'MSFT', 'NVDA', 'AMZN', 'META','ADBE', 'GOOG', 'INTC', 'TSLA']
    stocks_watch = ['XOM', 'CVX', 'COP', 'EOG', 'SLB']

    dic_stockswatch = {}

    for stock in stocks_watch:
        dic_stockswatch[stock] = {
            'label': stock,
            'df_data': treat_data_from_10q(get_data_from_sec(stock))['df_data'],
            'df_kpi': treat_data_from_10q(get_data_from_sec(stock))['df_kpi']
        }
        print(dic_stockswatch[stock]['df_kpi'])
        plt.figure(stock)
        plt.plot(dic_stockswatch[stock]['df_kpi'])
        plt.legend(dic_stockswatch[stock]['df_kpi'].columns)
        plt.grid(True)
        dic_stockswatch[stock]['df_data'].to_csv(stock, sep=';')
    
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

def treat_data_from_10q(fillings_us_gaap):
    nonUSDkeys = []
    for element in fillings_us_gaap.values():
        try:
            element['units']['USD'] = [reg for reg in element['units']['USD'] if reg['form'] == '10-Q']        
            element['units']['shares'] = [reg for reg in element['units']['shares'] if reg['form'] == '10-Q']
            
        except:
            nonUSDkeys.append(element['label'])        

    ## Fundamental indicators calculation
    #necessary data from 10-Q

    fields2find = ['AssetsCurrent', 
                'LiabilitiesCurrent', 
                'InventoryNet', 
                'SalesRevenueNet',
                'Revenues', 
                'CostOfGoodsAndServicesSold',
                'CostOfRevenue',
                'CostsAndExpenses',
                'OperatingIncomeLoss',
                'NetIncomeLoss',
                'StockholdersEquity',
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
        

    df_10q_data = df_10q_data.sort_index()
    df_10q_data = df_10q_data.interpolate(method='linear', axis=0)

    for input in df_10q_data.columns:
        df_10q_data[input] = df_10q_data[input].fillna(df_10q_data[input].rolling(window=9, min_periods=1).mean())
    

    df_10q_kpi = pd.DataFrame(index=df_10q_data.index)

    try:
        df_10q_kpi['current_ratio'] = df_10q_data['AssetsCurrent']/df_10q_data['LiabilitiesCurrent']
    except:
        df_10q_kpi['current_ratio'] = False
    try:
        df_10q_kpi['quick_ratio'] = (df_10q_data['AssetsCurrent'] - df_10q_data['InventoryNet'])/df_10q_data['LiabilitiesCurrent']
    except:
        df_10q_kpi['quick_ratio'] = False

    try:
        try:
            df_10q_kpi['GrossMargin'] = (df_10q_data['SalesRevenueNet'] - df_10q_data['CostOfGoodsAndServicesSold'])/df_10q_data['SalesRevenueNet']
        except:
            df_10q_kpi['GrossMargin'] = (df_10q_data['Revenues'] - df_10q_data['CostOfRevenue'])/df_10q_data['Revenues']
    except:
        df_10q_kpi['GrossMargin'] = False
    
    try:
        try:
            df_10q_kpi['OperatingMargin'] = df_10q_data['OperatingIncomeLoss']/df_10q_data['SalesRevenueNet']
        except:
            df_10q_kpi['OperatingMargin'] = df_10q_data['OperatingIncomeLoss']/df_10q_data['Revenues']
    except:
        df_10q_kpi['OperatingMargin'] = False
        

    try:
        df_10q_kpi['roa'] = df_10q_data['NetIncomeLoss']/df_10q_data['AssetsCurrent']
    except:
        df_10q_kpi['roa'] = False
    try:
        df_10q_kpi['roe'] = df_10q_data['NetIncomeLoss']/df_10q_data['StockholdersEquity']
    except:
        df_10q_kpi['roe'] = False

    return {'df_data': df_10q_data,
            'df_kpi': df_10q_kpi
            }


if __name__ == "__main__":
    main()