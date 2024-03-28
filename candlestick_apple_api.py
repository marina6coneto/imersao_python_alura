import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mplfinance as mpf 
import yfinance as yf 
import plotly.graph_objects as go 
from plotly.subplots import make_subplots

dados = yf.download('AAPL', start='2023-09-29', end='2024-03-27')
mpf.plot(dados.head(181), type='candle', figsize = (16,8), volume=True, mav=(7,14))