import pandas as pd



stocks_watch = ['AAPL', 'MSFT', 'NVDA', 'AMZN', 'META','ADBE', 'GOOG', 'INTC']

df_MSFT_data = pd.read_csv('MSFT-df_data.csv', sep=';', index_col='timestamp')
df_MSFT_kpi = pd.read_csv('MSFT-df_kpi.csv', sep=';', index_col='timestamp')

df_MSFT_data.sort_index(inplace=True)
df_MSFT_kpi.sort_index(inplace=True)


df_MSFT_data.fillna(df_MSFT_data.rolling(window=12, min_periods=3).mean(), inplace=True)
df_MSFT_kpi.fillna(df_MSFT_kpi.rolling(window=12, min_periods=3).mean(), inplace=True)
df_MSFT_data.fillna(df_MSFT_data.mean(), inplace=True)
df_MSFT_kpi.fillna(df_MSFT_kpi.mean(), inplace=True)


print(df_MSFT_data)

data_correlation_matrix = df_MSFT_data.corr()
data_relevant_features = data_correlation_matrix['stock_price'].sort_values(ascending=False).index[1:]
#data_relevant_features = data_correlation_matrix.loc[(data_correlation_matrix['stock_price'] > 0.3) | (data_correlation_matrix['stock_price'] < -0.3)]['stock_price'].sort_values(ascending=False).index[1:]

# kpi_correlation_matrix = df_MSFT_kpi.corr()
#kpi_relevant_features = kpi_correlation_matrix['stock_price'].sort_values(ascending=False).index[1:]
# kpi_relevant_features = kpi_correlation_matrix.loc[(kpi_correlation_matrix['stock_price'] > 0.44) | (kpi_correlation_matrix['stock_price'] < -0.44)]['stock_price'].sort_values(ascending=False).index[1:]

print(data_correlation_matrix)
# print(kpi_correlation_matrix)
