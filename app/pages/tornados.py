import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from vega_datasets import data

def createFilters(data):
    date_min, date_max = st.select_slider('Data', options = data['Date'].sort_values(), value=[data['Date'].min(),data['Date'].max()])
    states = st.sidebar.multiselect('Estado', options = data['State'].unique(), default = None)
    mag_min, mag_max = st.select_slider('Magnitude',options=data['Magnitude'].sort_values().unique(),value=[data['Magnitude'].min(),data['Magnitude'].max()])
    return date_min, date_max, mag_min, mag_max, states

def filterData(data, date_min, date_max, mag_min, mag_max, states):
    plot_data = data[(data['Date'] >= date_min) & (data['Date'] <= date_max)]
    plot_data = plot_data[(data['Magnitude'] >= mag_min) & (data['Magnitude'] <= mag_max)]

    if len(states):
        plot_data = plot_data[data['State'].isin(states)]

    return plot_data

# Cria uma visualizacao de cards com os numeros absolutos
def plotCards(plot_data):

    # definicao dos espacamentos das colunas
    column_1, column_2, column_3 = st.columns([2.0, 2.0, 2.0])

    tornadoTotal = plot_data[['State']].count().astype(int)
    comprimentoMedia = np.round(plot_data[['Length']].sum() / len(plot_data[['Length']]),2)
    larguraMedia = np.round(plot_data[['Width']].sum() / len(plot_data[['Width']]),2)

    # plot dos cards com os big numbers
    with column_1:
        st.metric('Número de Tornados', tornadoTotal)

    with column_2:
        st.metric('Média de Comprimento', 0 if len(states) == 0 else comprimentoMedia)

    with column_3:
        st.metric('Média de Largura', 0 if len(states) == 0 else larguraMedia)

# Cria uma visualizacao de um grafico de distribuicao de tornados por tempo
def distTornados(plot_data):
    st.subheader('Série Temporal de Tornados')
    dfPorDia = plot_data.groupby(plot_data['Date']).size().reset_index(name='Contagem')
    dfPorDia['Date'] = pd.to_datetime(dfPorDia['Date'], errors='coerce')
    dfPorDia = dfPorDia.set_index('Date').resample('M').sum()

    st.line_chart(dfPorDia, y='Contagem', y_label='Tornados')

# Cria a visualizacao de um hexplot com os dados de posicao dos tornados
def scatterPlot(plot_data):
    st.subheader('Largura e Comprimento')
    st.scatter_chart(plot_data,x='Width',y='Length',x_label='Largura (em metros)',y_label='Comprimento (em metros)')

# Cria uma visualizacao de um grafico de distribuição da Distância Percorrida em km pelos tornados
def distDistancia(plot_data):
    
    plt.figure(figsize=(8, 4.2))
    st.subheader('Distribuição por Distâncias Percorridas')

    sns.histplot(plot_data['Distance'], kde=True, bins=100)

    # definicao dos nomes dos eixos
    plt.xlabel('Distância Percorrida (km)', fontsize=12, color='white')
    plt.ylabel('Frequência', fontsize=12, color='white')

    # alteracoes visuais do grafico
    plt.xlim(0, 150)
    sns.despine()

    plt.gcf().set_facecolor('none')
    plt.gca().set_facecolor('none')

    # Mudar a cor dos eixos para branco
    plt.gca().spines['top'].set_color('white')      # Eixo superior
    plt.gca().spines['right'].set_color('white')    # Eixo direito
    plt.gca().spines['left'].set_color('white')     # Eixo esquerdo
    plt.gca().spines['bottom'].set_color('white')   # Eixo inferior

    # Mudar a cor das marcas (ticks) dos eixos
    plt.tick_params(axis='x', colors='white')  # Cor das marcas do eixo X
    plt.tick_params(axis='y', colors='white')  # Cor das marcas do eixo Y

    # mostrar o grafico
    st.pyplot(plt.gcf())

# Cria uma visualizacao de um grafico de barras apresetando os valores de magnitudes dos tornados
def barraMagnitude(plot_data):
    st.subheader('Magnitude de Tornados')
    plot_data = plot_data.groupby(plot_data['Magnitude']).size().reset_index(name='Contagem')
    st.bar_chart(plot_data, x="Magnitude", y="Contagem")

st.title('Dados de Tornados')
with st.sidebar:
    st.title('Filtros')
    data = st.session_state['data']
    date_min, date_max, mag_min, mag_max, states = createFilters(data)
    filtered_data = filterData(data, date_min, date_max, mag_min, mag_max, states)

plotCards(filtered_data)

col_1, col_2 = st.columns(2)
with col_1:
    distTornados(filtered_data)
    scatterPlot(filtered_data)

with col_2:
    distDistancia(filtered_data)
    barraMagnitude(filtered_data)
