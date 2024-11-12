import streamlit as st
import pandas as pd
import numpy as np

st.title('Mapas')

with st.sidebar:
    st.title('Filtros')
    data = st.session_state['data']
    date_min, date_max = st.select_slider('Data', options=data['Datetime'].sort_values(), value=[data['Datetime'].min(),data['Datetime'].max()])
    states = st.multiselect('State', data['State'].unique(), default=None)

