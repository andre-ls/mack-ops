import streamlit as st
import pandas as pd
import numpy as np
from keplergl import KeplerGl
from streamlit_keplergl import keplergl_static

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

    return date_min, date_max, states, mag_min, mag_max, measure

def filterData(data, date_min, date_max, mag_min, mag_max, states):
    """
    Função para Filtrar os dados a serem exibidos na página de visualização de Mapas.
    """
    plot_data = data[(data['Date'] >= date_min) & (data['Date'] <= date_max)]
    plot_data = plot_data[(data['Magnitude'] >= mag_min) & (data['Magnitude'] <= mag_max)]

    if len(states):
        plot_data = plot_data[data['State'].isin(states)]

    return plot_data

st.title('Mapas')
with st.sidebar:
    st.title('Filtros')
    data = st.session_state['data']
    date_min, date_max, states, mag_min, mag_max, measure = setupFilters(data)

mapData = filterData(data, date_min, date_max, mag_min, mag_max, states)

map = KeplerGl(height=600)
map.add_data(data=mapData)
keplergl_static(map,width=1250)



