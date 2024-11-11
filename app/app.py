import streamlit as st
import pandas as pd
import numpy as np

st.session_state['data'] = pd.read_csv("data/processed/tornado_processed_data.csv")

maps_page = st.Page("pages/maps.py", title="Mapas", icon="🗺️")
tornados_page = st.Page("pages/tornados.py", title="Tornados", icon="🌪️")
loss_page = st.Page("pages/loss.py", title="Perdas e Prejuízos", icon="💰")

pg = st.navigation([maps_page, tornados_page, loss_page])
st.set_page_config(page_title="Página Inicial", page_icon=":material/home:")
pg.run()
