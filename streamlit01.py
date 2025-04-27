# -*- coding: utf-8 -*-
## Aula_26.04.2025_Atividade-01_001.ipynb

#**Faculdade Senac Pernambuco**
###MBA em Ciência de Dados e Inteligência Artificial - Turma: 2025
###Criação de um Data Storytelling com Streamlit
###Petrônio João da Silva

##Importação de Bibliotecas

# STREAMLIT - permite a publicação em um dashboard na rede mundial
import streamlit as st

# NUMPY - funções essencias para álgebra linear, manipulação de imagens e cálculos de arrays
import numpy as np

# PANDAS - possibilita preparação e operação de dados em alta performance. Trabalha com duas estruturas principais: Series (Array unidimensional) e Dataframes (bidimensional)
import pandas as pd

# MATPLOTLIB - fornece visualização de dados
import matplotlib.pyplot as plt

# SEABORN - melhora a aparência dos gráficos do matplotlib
import seaborn as sb

# SCIKIT-LEARN - utilização de Machine Learning, contendo uma variedade de algoritmos eficientes para inteligência artificial e modelagem estatística
import sklearn as skl

st.title("Dashboard - Eficiência de Manutenções em um Conjunto de Máquinas")

##Importação dos Dados a Serem Analisados

# A variável "url" guarda do endereço do local ou o nome do arquivo onde os dados são disponibilizados
url = 'machinery_data.csv'

# Criação do DataFrame a partir da leitura (importação) dos dados
df = pd.read_csv(url, sep=',')

st.markdown('# Exibição Inicial dos Dados')
st.dataframe(df.head())

st.markdown('### Os dados exibem a quantidade de horas de utilização de um determinado conjunto de máquinas juntamente com a informação da temperatura de funcionamento, a quantidade de falhas e as datas de manutenção.')

colunas = {'Machine_Type': 'Tipo_de_Maquina', 'Usage_Hours':	'Horas_de_Uso', 'Temperature':	'Temperatura', 'Failures':	'Numero_de_Falhas', 'Maintenance_Date': 'Data_de_Manutencao'}
df2 = df.copy()
df2.drop('Machine_ID', axis = 1, inplace = True)
df2.rename(columns= colunas, inplace = True)

st.dataframe(df2.head())
st.write(df2.info())
st.dataframe(df2['Tipo_de_Maquina'].value_counts())

st.markdown('### Há um número total de 200 registros e é possível perceber que uma mesma máquina aparece tantas vezes quantas forem as datas de manutenção, logo entende-se que o número de registros de uma máquina reflete a quantidade de manutenções que é feita nela.')

plt.figure(figsize=(6,4))
plt.bar(df2['Tipo_de_Maquina'].value_counts().index, df2['Tipo_de_Maquina'].value_counts())
plt.title('Quantidade de Manutenções por Máquinas')
plt.xlabel('Máquina')
plt.ylabel('N° de Manutenções')
plt.show()

st.markdown('### O gráfico mostra que a máquina com maior número de manutenções é a *Milling* enquanto que a que tem menor número de manutenções é a *Drill*')

# Conversão da coluna "Date" para formato de data
df2.Data_de_Manutencao = pd.to_datetime(df2.Data_de_Manutencao)

df2.describe()

Manutencao = df2.groupby(['Tipo_de_Maquina']).agg(Media_de_Horas_de_Uso = ('Horas_de_Uso','mean'), Temperatura_Media = ('Temperatura','mean'), Total_de_Falhas = ('Numero_de_Falhas', 'sum'))
st.dataframe(Manutencao.head())

st.markdown('### A tabela acima mostra que a máquina *Milling*, apesar de ter o segundo maior número de falhas, é a que possui maior tempo de utilização. Lembrando que ela é também a que mais recebe manutenções. Por outro lado, a máquina *CNC* apesar de quase emparelhar com a *Milling* em número de manutenções, e possuir o menor tempo de uso, é a que mais registra falhas.')

st.markdown('### Além disso, é possível perceber que a temperatura não é um fator preponderante nesta análise, uma vez que todas as máquinas, quando em funcionamento, registram praticamente a mesma temperatura.')

st.markdown('### Vejamos isso nos gráficos a seguir.')

#Gráfico referente à Temperatura Média de Funcionamento das Máquinas
plt.figure(figsize=(6, 4))
#plt.bar(Manutencao.index, Manutencao.Temperatura_Media, color='red')
st.bar_chart(Manutencao.index, Manutencao.Temperatura_Media, color='red')
plt.title('Temperatura Média das Máquinas')
plt.xlabel('Máquina')
plt.ylabel('Temperatura')
plt.show()

#Dataframe para os valores e colunas relacionado à Média de Horas de Uso
categorias = Manutencao.index
valores_MHU = Manutencao.Media_de_Horas_de_Uso.values

#Dataframe para os valores e colunas relacionado ao Total de Falhas
valores_QTF = Manutencao.Total_de_Falhas.values

#Construindo um subplots para que gere dois gráficos lado a lado
fig, axs = plt.subplots(1, 2, figsize=(16, 6), sharey=True)

#Gráfico referente à Média de Horas de Uso
axs[0].bar(categorias, valores_MHU, color='lightblue', edgecolor='black')
axs[0].set_title('Horas de Uso Médio por Máquina')
axs[0].set_xlabel('Máquina')
axs[0].set_ylabel('Tempo Médio de Uso (h)')
axs[0].tick_params(axis='x', rotation=45)
axs[0].grid(axis='y', linestyle='--', alpha=0.7)

#Gráfico referente ao Total de Falhas
axs[1].bar(categorias, valores_QTF, color='lightgreen', edgecolor='black')
axs[1].set_title('Quantidade de Falhas por Máquina')
axs[1].set_xlabel('Máquina')
axs[1].set_ylabel('N° de Falhas')
axs[1].tick_params(axis='x', rotation=45)
axs[1].grid(axis='y', linestyle='--', alpha=0.7)

#Ajuste no Layout dos gráficos
plt.suptitle('Comparação: Tempo de Funcionamento vs Número de Falhas', fontsize=16)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()

st.markdown('# Conclusão')

st.markdown('## Podemos concluir que as manutenções na máquina *CNC* necessitam de um cuidado maior, umas vez que essa máquina não apresenta a mesma proporcionalidade de tempo de uso vesus quantidade de manutenção vesus quantidade de falha que as demais, pois apesar de ser a segunda maior em número de manutenções e a que menos é utilizada, ela registra a maior quantidade de falhas.')