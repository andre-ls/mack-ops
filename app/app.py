import os
import streamlit as st
import pandas as pd
import numpy as np

st.session_state['app_directory'] = os.path.dirname(__file__)
st.session_state['data'] = pd.read_csv("data/processed/tornado_processed_data.csv")

home_page = st.Page("pages/home.py", title="Início", icon="🔎")
maps_page = st.Page("pages/maps.py", title="Mapas", icon="🗺️")
tornados_page = st.Page("pages/tornados.py", title="Tornados", icon="🌪️")
loss_page = st.Page("pages/loss.py", title="Perdas e Prejuízos", icon="💰")

st.logo('https://www.fema.gov/profiles/femad8_gov/themes/fema_uswds/images/fema-logo-blue.svg',
        size='large',
        link='https://gis-fema.hub.arcgis.com/datasets/fedmaps::tornado-tracks-1/about')

pg = st.navigation([home_page, maps_page, tornados_page, loss_page])
st.set_page_config(page_title="Página Inicial", page_icon=":material/home:",layout="wide")
pg.run()
