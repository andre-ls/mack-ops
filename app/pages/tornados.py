import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import folium
import plotly.figure_factory as ff
from vega_datasets import data
from datetime import datetime

st.title('Dados de Tornados')

with st.sidebar:
    st.title('Filtros')
    data = st.session_state['data']
    date_min, date_max = st.select_slider('Data', options = data['Datetime'].sort_values(), value=[data['Datetime'].min(),data['Datetime'].max()])
    estado = st.sidebar.multiselect('Estado', options = data['State'].unique(), default = None)
    magnitude = st.selectbox('Magnitude', options = data['Magnitude'].sort_values().unique(), index = None)

def plotCards(data, states, magnitude, date_min, date_max):
    if states is not None:
        plot_data = data[data['State'].isin(states)]
        plot_data = plot_data[plot_data['Datetime'].between(date_min, date_max)]
        plot_data = plot_data[plot_data['Magnitude'] == magnitude] if magnitude != None else plot_data
        comprimentoMedia = np.round(plot_data[['Length']].sum() / len(plot_data[['Length']]),2)
        larguraMedia = np.round(plot_data[['Width']].sum() / len(plot_data[['Width']]),2)
    else:
        plot_data = data
        comprimentoMedia = 0
        larguraMedia = 0
        
    column_1, column_2, column_3 = st.columns([2.0, 2.0, 2.0])

    tornadoTotal = plot_data[['State']].count().astype(int)

    with column_1:
        st.metric('Número de Tornados', tornadoTotal)

    with column_2:
        st.metric('Média de Comprimento', comprimentoMedia)

    with column_3:
        st.metric('Média de Largura', larguraMedia)

def distTornados(data, states, magnitude, date_min, date_max):
    if states is not None:
        plot_data = data[data['State'].isin(states)]
        plot_data = plot_data[plot_data['Datetime'].between(date_min, date_max)]
        plot_data = plot_data[plot_data['Magnitude'] == magnitude] if magnitude != None else plot_data
        plot_data['Datetime'] = pd.to_datetime(plot_data['Datetime']).dt.date
    else:
        plot_data = data

    dfPorDia = plot_data.groupby(plot_data['Datetime']).size().reset_index(name='contagem')

    x = dfPorDia['Datetime']
    y = dfPorDia['contagem']
    z = x

    plt.plot(x, y)

    plt.title('Distribuição de Tornados por Dia', color='white')
    plt.xlabel('Data', color='white')
    plt.ylabel('Número de Tornados', color='white')

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

    st.pyplot(plt.gcf())

def hexPlot(data, states, magnitude, date_min, date_max):
    if states is not None:
        plot_data = data[data['State'].isin(states)]
        plot_data = plot_data[plot_data['Datetime'].between(date_min, date_max)]
        plot_data = plot_data[plot_data['Magnitude'] == magnitude] if magnitude != None else plot_data
    else:
        plot_data = data

    fig, ax = plt.subplots(figsize=(10, 8))

    # Plotar o Hexbin
    hb = ax.hexbin(plot_data['Start_Longitude'], plot_data['Start_Latitude'], gridsize=30, cmap='viridis')

    # Adicionar barra de cores
    cb = fig.colorbar(hb, ax=ax)
    cb.set_label('Densidade de Tornados')

    # Definir rótulos e título
    ax.set_title('Densidade de Tornados por Localização', fontsize=16)
    ax.set_xlabel('Longitude', fontsize=12)
    ax.set_ylabel('Latitude', fontsize=12)

    ax.set_facecolor('black')  # Cor de fundo do gráfico (cor preta)
    fig.patch.set_facecolor('none')  # Cor de fundo da figura (transparente)

    # Definir rótulos e título com texto branco
    ax.set_title('Densidade de Tornados por Localização', fontsize=16, color='white')  # Cor do título
    ax.set_xlabel('Longitude', fontsize=12, color='white')  # Cor do rótulo do eixo X
    ax.set_ylabel('Latitude', fontsize=12, color='white')  # Cor do rótulo do eixo Y


    # Alterar cor dos eixos (marcas e linhas)
    ax.spines['top'].set_color('white')      # Cor da borda superior
    ax.spines['right'].set_color('white')    # Cor da borda direita
    ax.spines['left'].set_color('white')     # Cor da borda esquerda
    ax.spines['bottom'].set_color('white')   # Cor da borda inferior

    ax.tick_params(axis='x', colors='white')  # Cor das marcas do eixo X
    ax.tick_params(axis='y', colors='white')  # Cor das marcas do eixo Y

    st.pyplot(plt.gcf())

def distDistancia(data, states, magnitude, date_min, date_max):
    if states is not None:
        plot_data = data[data['State'].isin(states)]
        plot_data = plot_data[plot_data['Datetime'].between(date_min, date_max)]
        plot_data = plot_data[plot_data['Magnitude'] == magnitude] if magnitude != None else plot_data
    else:
        plot_data = data

    plt.figure(figsize=(10, 6))

    sns.histplot(plot_data['Distance'], kde=True, bins=10)

    plt.title('Distribuição de Distância Percorrida por Ocorrência', fontsize=16, color='white')
    plt.xlabel('Distância Percorrida (km)', fontsize=12, color='white')
    plt.ylabel('Frequência', fontsize=12, color='white')

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

    st.pyplot(plt.gcf())

def barraMagnitude(data, states, magnitude, date_min, date_max):
    if states is not None:
        plot_data = data[data['State'].isin(states)]
        plot_data = plot_data[plot_data['Datetime'].between(date_min, date_max)]
        plot_data = plot_data[plot_data['Magnitude'] == magnitude] if magnitude != None else plot_data
    else:
        plot_data = data

    df = plot_data[['State', 'Magnitude']]
    st.bar_chart(df, x="State", y="Magnitude", color="Magnitude", stack=False)

st.write("#")
plotCards(data, estado, magnitude, date_min, date_max)
st.write("#")
distTornados(data, estado, magnitude, date_min, date_max)
st.write("#")
hexPlot(data, estado, magnitude, date_min, date_max)
st.write("#")
distDistancia(data, estado, magnitude, date_min, date_max)
st.write("#")
st.markdown("<h5 style='text-align: center; color: white;'> Magnitude dos Tornados </h5>", unsafe_allow_html=True)
st.write("#")
barraMagnitude(data, estado, magnitude, date_min, date_max)