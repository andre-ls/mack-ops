import os
import streamlit as st
import pandas as pd
import numpy as np
from keplergl import KeplerGl
from streamlit_keplergl import keplergl_static
from pages.map_config import *

def setupFilters(data):
    """
    Função responsável por configurar os filtros presentes na página de visualização de Mapas.
    """
    date_min, date_max = st.select_slider('Data', options=data['Date'].sort_values(), value=[data['Date'].min(),data['Date'].max()])
    states = st.multiselect('Estado', data['State'].unique(), default=None)
    mag_min, mag_max = st.select_slider('Magnitude',options=data['Magnitude'].sort_values().unique(),value=[data['Magnitude'].min(),data['Magnitude'].max()])
    map_view = st.radio('Tipo de Mapa',options=['Trajetórias','Colunas'])

    if map_view == 'Colunas':
        measure = st.selectbox('Medida a ser exibida', options=['Total de Tornados','Perdas Econômicas','Fatalidades','Feridos'])
    else:
        measure = None

    return date_min, date_max, states, mag_min, mag_max, map_view, measure

def filterData(data, date_min, date_max, mag_min, mag_max, states):
    """
    Função para Filtrar os dados a serem exibidos na página de visualização de Mapas.
    """
    plot_data = data[(data['Date'] >= date_min) & (data['Date'] <= date_max)]
    plot_data = plot_data[(data['Magnitude'] >= mag_min) & (data['Magnitude'] <= mag_max)]

    if len(states):
        plot_data = plot_data[data['State'].isin(states)]

    return plot_data

def calculateCards(data):
    totalTornados = len(data)
    totalLoss = np.round(data['Total_Loss'].sum()/1000000,2)
    totalFatalities = data['Fatalities'].sum()
    totalInjuries = data['Injuries'].sum()

    return totalTornados, totalLoss, totalFatalities, totalInjuries

def positionCards(app_directory, totalTornados, totalLoss, totalFatalities, totalInjuries):
    space_left,\
    column_image_1, column_1,\
    column_image_2, column_2,\
    column_image_3, column_3,\
    column_image_4, column_4,\
    space_right = st.columns([1.0, 0.7, 2.0, 0.7, 2.0, 0.7, 2.0, 0.7, 2.0, 0.2])

    with column_image_1:
        st.image(os.path.join(app_directory,"images/tornado.png"),width=70)

    with column_1:
        st.metric('Total de Tornados', totalTornados)
    
    with column_image_2:
        st.image(os.path.join(app_directory,"images/perda-de-dinheiro.png"),width=70)

    with column_2:
        st.metric('Perdas Totais ($)', str(totalLoss) + 'M')

    with column_image_3:
        st.image(os.path.join(app_directory,"images/paciente.png"),width=70)

    with column_3:
        st.metric('Feridos', totalInjuries)

    with column_image_4:
        st.image(os.path.join(app_directory,"images/farmacia.png"),width=70)

    with column_4:
        st.metric('Fatalidades', totalFatalities)


def getMapConfiguration(map_view, measure):
    if map_view == 'Trajetórias':
        return tracks_config
    elif map_view == 'Colunas':
        if measure == 'Total de Tornados':
            return count_hex
        if measure == 'Fatalidades':
            return fatalities_hex
        if measure == 'Feridos':
            return injuries_hex
        if measure == 'Perdas Econômicas':
            return loss_hex

def generateMap(data, map_config):
    map = KeplerGl(height=600, config=map_config)
    map.add_data(data=mapData,name='Tornados')
    keplergl_static(map,width=1250)

st.title('🗺️Mapas')
with st.sidebar:
    st.title('Filtros')
    data = st.session_state['data']
    app_directory = st.session_state['app_directory']
    date_min, date_max, states, mag_min, mag_max, map_view, measure = setupFilters(data)

mapData = filterData(data, date_min, date_max, mag_min, mag_max, states)
totalTornados, totalLoss, totalFatalities, totalInjuries = calculateCards(mapData)
positionCards(app_directory, totalTornados, totalLoss, totalFatalities, totalInjuries)
map_config = getMapConfiguration(map_view, measure)
generateMap(data, map_config)
