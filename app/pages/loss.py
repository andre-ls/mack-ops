import streamlit as st
import pandas as pd
import numpy as np
from keplergl import KeplerGl

data = st.session_state['data']

st.title("Análise de Perdas e Prejuízos de Tornados")

st.sidebar.header("Filtros")

ano = st.sidebar.multiselect("Ano", options=data['Ano'].unique(), default=data['Ano'].unique())

estado = st.sidebar.multiselect("Estado(s)", options=data['State'].unique(), default=data['State'].unique())

metrica = st.sidebar.selectbox("Métrica a ser exibida", ["Perdas de Propriedades", "Perdas de Colheitas", "Fatalidades", "Feridos"])

st.subheader("Métricas Principais")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Perdas de Propriedades", f"${filtered_data['Property_Loss'].sum():,.2f}")
col2.metric("Perdas de Colheitas", f"${filtered_data['Crop_Loss'].sum():,.2f}")
col3.metric("Fatalidades", filtered_data['Fatalities'].sum())
col4.metric("Feridos", filtered_data['Injuries'].sum())

st.subheader("Série Temporal das Métricas")
serie_metrica = "Property_Loss" if metrica == "Perdas de Propriedades" else (
    "Crop_Loss" if metrica == "Perdas de Colheitas" else (
    "Fatalities" if metrica == "Fatalidades" else "Injuries"))

serie_temporal = filtered_data[['Datetime', serie_metrica]].set_index('Datetime').resample('M').sum()
st.line_chart(serie_temporal, y=serie_metrica)

st.subheader("Distribuição por Estado")
barras_por_estado = filtered_data.groupby('State')[serie_metrica].sum()
st.bar_chart(barras_por_estado)

st.subheader("Mapa Interativo dos Tornados")
map_data = filtered_data[['Start_Latitude', 'Start_Longitude', 'Datetime', 'Magnitude', 'Property_Loss', 'Crop_Loss']]
map_data = map_data.rename(columns={"Start_Latitude": "latitude", "Start_Longitude": "longitude"})
kepler_map = KeplerGl(height=400)
kepler_map.add_data(data=map_data, name="Tornados")
st.pydeck_chart(kepler_map)
