import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error

import matplotlib.pyplot as plt

stocks_watch = ['AAPL', 'MSFT', 'NVDA', 'AMZN', 'META','ADBE', 'GOOG', 'INTC']

df_MSFT_data = pd.read_csv('MSFT-df_data.csv', sep=';', index_col='timestamp')
df_MSFT_kpi = pd.read_csv('MSFT-df_kpi.csv', sep=';', index_col='timestamp')

df_MSFT_data.sort_index(inplace=True)
df_MSFT_kpi.sort_index(inplace=True)


df_MSFT_data.fillna(df_MSFT_data.rolling(window=12, min_periods=3).mean(), inplace=True)
df_MSFT_kpi.fillna(df_MSFT_kpi.rolling(window=12, min_periods=3).mean(), inplace=True)
df_MSFT_data.fillna(df_MSFT_data.mean(), inplace=True)
df_MSFT_kpi.fillna(df_MSFT_kpi.mean(), inplace=True)

data_correlation_matrix = df_MSFT_data.corr()
data_relevant_features = data_correlation_matrix['stock_price'].sort_values(ascending=False).index[1:]
#data_relevant_features = data_correlation_matrix.loc[(data_correlation_matrix['stock_price'] > 0.3) | (data_correlation_matrix['stock_price'] < -0.3)]['stock_price'].sort_values(ascending=False).index[1:]


X = df_MSFT_data[data_relevant_features]
y = df_MSFT_data['stock_price']

# Dividir os dados em conjunto de treinamento, validação e teste mantendo os índices
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)


# Padronizar os dados
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_val = scaler.transform(X_val)
X_test = scaler.transform(X_test)


# Treinar o MLPRegressor
mlp = MLPRegressor(hidden_layer_sizes=(64, 32), max_iter=505, random_state=42)
mlp.fit(X_train, y_train)

# Fazer previsões
y_train_pred = mlp.predict(X_train)
y_val_pred = mlp.predict(X_val)
y_test_pred = mlp.predict(X_test)

# Avaliar o modelo
train_mse = mean_squared_error(y_train, y_train_pred)
val_mse = mean_squared_error(y_val, y_val_pred)
test_mse = mean_squared_error(y_test, y_test_pred)

print(f'Train MSE: {train_mse}')
print(f'Validation MSE: {val_mse}')
print(f'Test MSE: {test_mse}')



# Plotar os resultados
plt.figure(figsize=(14, 7))
plt.plot(y_test.index, y_test, label='True Prices', color='blue')
plt.plot(y_test.index, y_test_pred, label='Predicted Prices', linestyle='dotted', color='red')
plt.xlabel('Time')
plt.ylabel('Stock Price')
plt.title('True vs Predicted Stock Prices')
plt.grid()
plt.legend()
plt.show()
