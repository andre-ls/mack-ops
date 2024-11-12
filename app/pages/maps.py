import streamlit as st
import pandas as pd
import numpy as np
from keplergl import KeplerGl
from streamlit_keplergl import keplergl_static

st.title('Mapas')

with st.sidebar:
    st.title('Filtros')
    data = st.session_state['data']
    date_min, date_max = st.select_slider('Data', options=data['Date'].sort_values(), value=[data['Date'].min(),data['Date'].max()])
    states = st.multiselect('State', data['State'].unique(), default=None)
    mag_min, mag_max = st.select_slider('Magnitude',options=data['Magnitude'].sort_values().unique(),value=[data['Magnitude'].min(),data['Magnitude'].max()])

def filterData(data, date_min, date_max, mag_min, mag_max, states):
    plot_data = data[(data['Date'] >= date_min) & (data['Date'] <= date_max)]
    plot_data = plot_data[(data['Magnitude'] >= mag_min) & (data['Magnitude'] <= mag_max)]

    if len(states):
        plot_data = plot_data[data['State'].isin(states)]

    return plot_data

mapData = filterData(data, date_min, date_max, mag_min, mag_max, states)

map = KeplerGl(height=600)
map.add_data(data=mapData)
keplergl_static(map,width=1250)



