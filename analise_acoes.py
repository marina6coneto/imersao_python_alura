import pandas as pd 

df_principal = pd.read_excel('acoes.xlsx', sheet_name='Principal')
print(df_principal)

df_total_de_acoes = pd.read_excel('acoes.xlsx', sheet_name='Total_de_acoes')
print(df_total_de_acoes)

df_ticker = pd.read_excel('acoes.xlsx', sheet_name='Ticker')
print(df_ticker)

df_chat_gpt = pd.read_excel('acoes.xlsx', sheet_name='Chat_Gpt')
print(df_chat_gpt)

