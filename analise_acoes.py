import pandas as pd 
import plotly.express as px


df_principal = pd.read_excel('acoes.xlsx', sheet_name='Principal')
df_total_de_acoes = pd.read_excel('acoes.xlsx', sheet_name='Total_de_acoes')
df_ticker = pd.read_excel('acoes.xlsx', sheet_name='Ticker')
df_chat_gpt = pd.read_excel('acoes.xlsx', sheet_name='Chat_Gpt')


#mostra apenas as colunas que vc quer
df_principal = df_principal[['Ativo', 'Data', 'Último (R$)', 'Var. Dia (%)']].copy() 

#renomear as colunas
df_principal = df_principal.rename(columns={'Último (R$)':'valor_final', 'Var. Dia (%)':'var_dia_pct'}).copy() 

#adicionar novas colunas
df_principal['var_pct'] = df_principal['var_dia_pct']/100 

#adicionar novas colunas
df_principal['valor_incial'] = df_principal['valor_final'] / (df_principal['var_pct'] + 1) 

#similar ao procv ou vlook no excel, vamos mergir as celulas (código abaixo)
df_principal = df_principal.merge(df_total_de_acoes, left_on='Ativo', right_on='Código', how='left') 

#excluímos a coluna 'codigo' pois era igual a coluna 'ativo'
df_principal = df_principal.drop(columns=['Código']) 

#calculamos a variaçao em reais (código abaixo)
df_principal['variacao_rs'] = (df_principal['valor_final'] - df_principal['valor_incial']) * df_principal['Qtde. Teórica']

#formataçao de valores
pd.options.display.float_format = '{:.2f}'.format

#convertemos a coluna qntd teorica para inteiro
df_principal['Qtde. Teórica'] = df_principal['Qtde. Teórica'].astype(int)

#renomear as colunas
df_principal = df_principal.rename(columns={'Qtde. Teórica':'qntd_teorica'}).copy()

#criar a coluna resultado (código abaixo)
df_principal['resultado'] = df_principal['variacao_rs'].apply(lambda x: 'Subiu' if x > 0 else ('Desceu' if x < 0 else 'Estável'))

#similar ao procv ou vlook no excel, vamos mergir as celulas (código abaixo)
df_principal = df_principal.merge(df_ticker, left_on='Ativo', right_on='Ticker', how='left')

#excluímos a coluna 'ticker' pois era igual a coluna 'ativo'
df_principal = df_principal.drop(columns=['Ticker']) 

#similar ao procv ou vlook no excel, vamos mergir as celulas (código abaixo)
df_principal = df_principal.merge(df_chat_gpt, left_on='Nome', right_on='Empresa', how='left')

#excluímos a coluna 'empresa' pois era igual a coluna 'nome'
df_principal = df_principal.drop(columns=['Empresa']) 

#criar a coluna 'cat_idade' (código abaixo)
df_principal['cat_idade'] = df_principal['Idade (anos)'].apply(lambda x: 'Mais de 100 anos' if x > 100 else ('Menos de 50 anos' if x < 50 else 'Entre 50 e 100 anos')) 
#print(df_principal)

# Calculando o maior valor
maior = df_principal['variacao_rs'].max()

# Calculando o menor valor
menor = df_principal['variacao_rs'].min()

# Calculando a média
media = df_principal['variacao_rs'].mean()

# Calculando a média de quem subiu
media_subiu = df_principal[df_principal['resultado'] == 'Subiu']['variacao_rs'].mean()

# Calculando a média de quem desceu
media_desceu = df_principal[df_principal['resultado'] == 'Desceu']['variacao_rs'].mean()

# print(f'Maior:\tR$ {maior:,.2f}')
# print(f'Menor:\tR$ {menor:,.2f}')
# print(f'Média:\tR$ {media:,.2f}')
# print(f'Média de quem subiu:\tR$ {media_subiu:,.2f}')
# print(f'Média de quem desceu:\tR$ {media_desceu:,.2f}')

df_principal_subiu = df_principal[df_principal['resultado'] == 'Subiu']
#print(df_principal_subiu)

df_analise_segmento = df_principal_subiu.groupby('Segmento')['variacao_rs'].sum().reset_index()
#print(df_analise_segmento)

df_analise_saldo = df_principal.groupby('resultado')['variacao_rs'].sum().reset_index()
#print(df_analise_saldo)

df_analise_cat_idade = df_principal.groupby('cat_idade')['variacao_rs'].sum().reset_index()
#print(df_analise_cat_idade)

fig_1 = px.bar(df_analise_saldo, x='resultado', y='variacao_rs', text='variacao_rs', title='Variação em R$ por Resultado')
print(fig_1.show())

fig_2 = px.pie(df_analise_segmento, names='Segmento', values='variacao_rs', title='Variação Reais por Segmento')
print(fig_2.show())

fig_3 = px.bar(df_analise_cat_idade, x='cat_idade', y='variacao_rs', text='variacao_rs', title='Variação Reais por Categoria de Idade')
print(fig_3.show())
