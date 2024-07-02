import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

import matplotlib.pyplot as plt

import seaborn as sns


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
print(df_MSFT_kpi)

data_correlation_matrix = df_MSFT_data.corr()
#data_relevant_features = data_correlation_matrix['stock_price'].sort_values(ascending=False).index[1:]
data_relevant_features = data_correlation_matrix.loc[(data_correlation_matrix['stock_price'] > 0.3) | (data_correlation_matrix['stock_price'] < -0.3)]['stock_price'].sort_values(ascending=False).index[1:]

kpi_correlation_matrix = df_MSFT_kpi.corr()
#kpi_relevant_features = kpi_correlation_matrix['stock_price'].sort_values(ascending=False).index[1:]
kpi_relevant_features = kpi_correlation_matrix.loc[(kpi_correlation_matrix['stock_price'] > 0.95) | (kpi_correlation_matrix['stock_price'] < -0.89)]['stock_price'].sort_values(ascending=False).index[1:]

print(data_correlation_matrix)
print(kpi_correlation_matrix)



X = df_MSFT_data[data_relevant_features]
y = df_MSFT_data['stock_price']


Xkpi = df_MSFT_kpi[kpi_relevant_features]
ykpi = df_MSFT_kpi['stock_price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)
Xkpi_train, Xkpi_test, ykpi_train, ykpi_test = train_test_split(Xkpi, ykpi, test_size=0.4, random_state=42)



model= LinearRegression()
model.fit(X_train, y_train)


modelkpi= LinearRegression()
modelkpi.fit(Xkpi_train, ykpi_train)

#avaliacao do modelo
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)

ykpi_pred = modelkpi.predict(Xkpi_test)
msekpi = mean_squared_error(ykpi_test, ykpi_pred)




print(f'Mean Squared Error: {mse}')
print(f'Mean Squared Error: {msekpi}')

plt.figure(figsize=(10, 6))
plt.plot(y_test.index, y_test, label='y_test', marker='o')  # Plotar y_test como pontos sólidos
plt.plot(y_test.index, y_pred, label='Prediction - 10_Q info', linestyle='--')  # Plotar y_pred como linha pontilhada
plt.title('Stock price prediction')
plt.xlabel('Índice')
plt.ylabel('Valores')
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.figure(figsize=(10, 6))
plt.plot(ykpi_test.index, ykpi_test, label='y_test', marker='o')  # Plotar y_test como pontos sólidos
plt.plot(ykpi_test.index, ykpi_pred, label='Prediction - 10_Q KPI', linestyle='--')  # Plotar y_pred como linha pontilhada
plt.title('Stock price prediction')
plt.xlabel('Índice')
plt.ylabel('Valores')
plt.legend()
plt.grid(True)
plt.tight_layout()

# Mostrar o plot
plt.show()

#print(data_correlation_matrix.loc[(data_correlation_matrix['stock_price'] > 0.47) | (data_correlation_matrix['stock_price'] < -0.51)]['stock_price'].sort_values(ascending=False).index[1:])
