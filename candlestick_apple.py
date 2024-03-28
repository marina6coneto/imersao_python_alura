import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mplfinance as mpf 
import yfinance as yf 
import plotly.graph_objects as go 
from plotly.subplots import make_subplots

#dados da petrobrás em um ano
dados = yf.download('AAPL', start='2023-09-29', end='2024-03-27')

#traduzi os nomes das colunas para português
dados.columns = ['abertura', 'maximo', 'minimo', 'fechamento', 'fech_ajust', 'volume']

#renomear o índice de 'date' para 'data'
dados = dados.rename_axis('data')
#print(dados)

#desenvolvimento do primeiro gráfico
dados['fechamento'].plot(figsize=(10,6))
plt.title('Variação do Preço por Data - APPLE', fontsize=16)
plt.legend(['Fechamento'])
#plt.show()

df = dados.head(181).copy()

#convertendo o índice em uma coluna de data
df['data'] = df.index

#convertendo as datas para o formato númerico de matplotlib
#isso é necessário para que o matplotlib possa plotar as data corretamente no gráfico
df['data'] = df['data'].apply(mdates.date2num)
#print(df)

#desenvolvimento do segundo gráfico (candlestick)
fig, ax = plt.subplots(figsize=(15,8))

#definir a largura dos candles no gráfico
width = 0.7

#determinar a cor dos candles 
#(verde = preço do fechamento maior que o de abertura)
#(vermelho = preço do fechamento menor que o de abertura)
for i in range(len(df)):
    if df['fechamento'].iloc[i] > df['abertura'].iloc[i]:
        color = 'green'
    else:
        color = 'red'

    #desenhando a linha vertical do candle (mecha)
    #essa linha mostra os preços máximo (topo da linha) e mínimo (base da linha) do dia
    #usamos 'ax.plot' para desenhar uma linha vertical
    #[df['Data'].iloc[i], df['Data'].iloc[i]] define o ponto x da linha (a data)
    #[df['Mínimo'].iloc[i], df['Máximo'].iloc[i]] define a altura da linha.
    ax.plot([df['data'].iloc[i], df['data'].iloc[i]],
            [df['minimo'].iloc[i], df['maximo'].iloc[i]],
            color = color,
            linewidth = 1)
    
    ax.add_patch(plt.Rectangle((df['data'].iloc[i] - width/2, min(df['abertura'].iloc[i], df['fechamento'].iloc[i])),
                               width,
                               abs(df['fechamento'].iloc[i] - df['abertura'].iloc[i]),
                               facecolor = color))

#fazendo a curva da média móvel    
df['MA7'] = df['fechamento'].rolling(window=7).mean()    
df['MA14'] = df['fechamento'].rolling(window=14).mean()    

#plotando as médias móveis
ax.plot(df['data'], df['MA7'], color='orange', label='Média Móvel de 7 dias') #média de 7 dias
ax.plot(df['data'], df['MA14'], color='yellow', label='Média Móvel de 14 dias') #média de 14 dias

#adicionando legendas para as médias móveis
ax.legend()
    
# formando o eixo x para mostrar as datas
# configurei o formato da data e a rotação para melhor legibilidade
ax.xaxis_date() #o método ax.xaxis_date() é usado para dizer ao Matplotlib que as datas estao no eixo x
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.xticks(rotation=0)
    
#adicionei títulos e rótulos para os eixos x e y
plt.title('Candlestick - AAPL com Matplotlib')
plt.xlabel('Data')
plt.ylabel('Preço')
    
#adicionei uma grade para facilitar a visualização dos valores
plt.grid(True)

#exibe gráfico 1 e 2   
plt.show()

#criar subplots
'''
"Primeiro, criamos uma figura que conterá nossos gráficos usando make_subplots.
Isso nos permite ter múltiplos gráficos em uma única visualização.
Aqui, teremos dois subplots: um para o gráfico de candlestick e outro para o volume de transações."
'''
fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                    vertical_spacing=0.1,
                    subplot_titles=('Candlesticks - APPLE', 'Volume Transacionado - APPLE'),
                    row_width=[0.2,0.7])
'''
"No gráfico de candlestick, cada candle representa um dia de negociação,
mostrando o preço de abertura, fechamento, máximo e mínimo. Vamos adicionar este gráfico à nossa figura."
'''
#adicionei o gráfico de candlestick
fig.add_trace(go.Candlestick(x = df.index,
                             open = df['abertura'],
                             high = df['maximo'],
                             low = df['minimo'],
                             close = df['fechamento'],
                             name = 'Candlestick'),
                             row = 1, col = 1)

#adicionei as médias móveis ao msm subplot para análise de tendências
fig.add_trace(go.Scatter(x=df.index,
                         y=df['MA7'],
                         mode = 'lines',
                         name='MA7 - Média Móvel de 7 dias'),
                         row = 1, col = 1
                         )
fig.add_trace(go.Scatter(x = df.index,
                         y = df['MA14'],
                         mode = 'lines',
                         name ='MA14 - Média Móvel de 14 dias'),
                         row = 1, col = 1
                         )
                            
#adicionei o gráfico de barras para o volume
#em seguida, criei o gráfico de barras para o volume de transações
#que nos da uma ideia de atividades de negociações naquele dia
fig.add_trace(go.Bar(x = df.index,
                     y = df['volume'],
                     name = 'Volume'),
                     row = 2, col = 1)

#atualizando o layout, ajuste título, formato de eixo..etc
fig.update_layout(yaxis_title = 'Preço',
                  xaxis_rangeslider_visible= False,
                  width=1100, height=600)
fig.show()
