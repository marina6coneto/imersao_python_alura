import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from prophet import Prophet 

#baixando dados dos ultimos 4 anos de uma açao 
dados = yf.download('JNJ', start='2020-01-01', end='2023-12-31', progress=False)
dados = dados.reset_index()
#print(dados)

#dividir dados em treino (até julho 2023) e teste (seg semestre de 2023)
dados_treino = dados[dados['Date'] < '2023-07-31']
dados_teste = dados[dados['Date'] >= '2023-07-31']

#preparando os dados para o FBProphet 
dados_prophet_treino = dados_treino[['Date', 'Close']].rename(columns={'Date': 'ds', 'Close': 'y'})
#print(dados_prophet_treino)

#criar e treinar modelo
modelo = Prophet(weekly_seasonality=True,
                 yearly_seasonality=True,
                 daily_seasonality=False)

modelo.add_country_holidays(country_name='US')
modelo.fit(dados_prophet_treino)

#ciar datas futuras para a previsao ate final de 2023
futuro = modelo.make_future_dataframe(periods=150)
previsao = modelo.predict(futuro)
#print(previsao)

#plotar os dados de treino, teste e previsoes
plt.figure(figsize=(14, 8))
plt.plot(dados_treino['Date'], dados_treino['Close'], label='Dados de treino', color='blue')
plt.plot(dados_teste['Date'], dados_teste['Close'], label='Dados Reais (teste)', color='green')
plt.plot(previsao['ds'], previsao['yhat'], label='Previsão', color='orange', linestyle='--')

plt.axvline(dados_treino['Date'].max(), color='red', linestyle='--', label='Início da Previsão')
plt.xlabel('Data')
plt.ylabel('Preço de Fechamento')
plt.title('Previsão de Preço de Fechamento vs Dados Reais')
plt.legend()
plt.show()