import streamlit as st
import pandas as pd
import numpy as np

st.title('Mapas')

with st.sidebar:
    st.title('Filtros')
    data = st.session_state['data']
    date_min, date_max = st.select_slider('Data', options=data['Date'].sort_values(), value=[data['Date'].min(),data['Date'].max()])
    states = st.multiselect('State', data['State'].unique(), default=None)
    magnitudes = st.select_slider('Magnitude',options=data['Magnitude'].sort_values().unique())

