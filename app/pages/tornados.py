import os
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from vega_datasets import data

def createFilters(data):
    """
    Função responsável por configurar os filtros presentes na página de visualização de dados de tornados.
    """
    date_min, date_max = st.select_slider('Data', options = data['Date'].sort_values(), value=[data['Date'].min(),data['Date'].max()])
    states = st.sidebar.multiselect('Estado', options = data['State'].unique(), default = None)
    mag_min, mag_max = st.select_slider('Magnitude',options=data['Magnitude'].sort_values().unique(),value=[data['Magnitude'].min(),data['Magnitude'].max()])
    return date_min, date_max, mag_min, mag_max, states

def filterData(data, date_min, date_max, mag_min, mag_max, states):
    """
    Função responsável por filtrar os dados utilizados na página de visualização de dados de tornados.
    """
    plot_data = data[(data['Date'] >= date_min) & (data['Date'] <= date_max)]
    plot_data = plot_data[(data['Magnitude'] >= mag_min) & (data['Magnitude'] <= mag_max)]

    if len(states):
        plot_data = plot_data[data['State'].isin(states)]

    return plot_data

def plotCards(plot_data, app_directory):
    """
    Função responsável por gerar as visualizações em cards na página de visualização de dados de tornados.
    """
    space_left,\
    column_image_1, column_1,\
    column_image_2, column_2,\
    column_image_3, column_3,\
    space_right = st.columns([1.0, 0.7, 2.0, 0.7, 2.0, 0.7, 2.0, 0.2])

    tornadoTotal = plot_data[['State']].count().astype(int)
    comprimentoMedia = np.round(plot_data['Length'].mean(),2)
    larguraMedia = np.round(plot_data['Width'].mean(),2)

    with column_1:
        st.metric('Número de Tornados', tornadoTotal)
    with column_2:
        st.metric('Média de Comprimento (metros)', comprimentoMedia)
    with column_3:
        st.metric('Média de Largura (metros)', larguraMedia)

    with column_image_1:
        st.image(os.path.join(app_directory,"images/tornado.png"),width=70)
    with column_image_2:
        st.image(os.path.join(app_directory,"images/comprimento.png"),width=70)
    with column_image_3:
        st.image(os.path.join(app_directory,"images/largura.png"),width=70)

def distTornados(plot_data):
    """
    Função responsável por gerar a visualização de série temporal de ocorrência de tornados na paǵina de visualização de dados de tornados.
    """
    st.subheader('Série Temporal de Tornados')
    dfPorDia = plot_data.groupby(plot_data['Date']).size().reset_index(name='Contagem')
    dfPorDia['Date'] = pd.to_datetime(dfPorDia['Date'], errors='coerce')
    dfPorDia = dfPorDia.set_index('Date').resample('M').sum()

    st.line_chart(dfPorDia, y='Contagem', y_label='Tornados')

def scatterPlot(plot_data):
    """
    Função responsável por gerar a visualização de Scatter Plot de Comprimento x Largura na paǵina de visualização de dados de tornados.
    """
    st.subheader('Largura e Comprimento')
    st.scatter_chart(plot_data,x='Width',y='Length',x_label='Largura (em metros)',y_label='Comprimento (em metros)')

def distDistancia(plot_data):
    """
    Função responsável por gerar a visualização de distribuição de Distâncias percorridas na paǵina de visualização de dados de tornados.
    """
    
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

def barraMagnitude(plot_data):
    """
    Função responsável por gerar a visualização de barras por Magnitude na página de visualização de dados de tornados.
    """
    st.subheader('Magnitude de Tornados')
    plot_data = plot_data.groupby(plot_data['Magnitude']).size().reset_index(name='Contagem')
    st.bar_chart(plot_data, x="Magnitude", y="Contagem")

st.title('🌪️Tornados')
with st.sidebar:
    st.title('Filtros')
    data = st.session_state['data']
    app_directory = st.session_state['app_directory']
    date_min, date_max, mag_min, mag_max, states = createFilters(data)
    filtered_data = filterData(data, date_min, date_max, mag_min, mag_max, states)

plotCards(filtered_data, app_directory)

col_1, col_2 = st.columns(2)
with col_1:
    distTornados(filtered_data)
    scatterPlot(filtered_data)

with col_2:
    distDistancia(filtered_data)
    barraMagnitude(filtered_data)
