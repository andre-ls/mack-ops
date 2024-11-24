import os
import streamlit as st
import pandas as pd
import altair as alt


def criar_filtros(data):
    """
    Função responsável por configurar os filtros presentes na página de visualização de perdas.
    """
    date_min, date_max = st.select_slider('Data', options=data['Date'].sort_values(), value=[data['Date'].min(),data['Date'].max()])
    states = st.multiselect('Estado', data['State'].unique(), default=None, placeholder='Todos')
    measure = st.selectbox('Medida a ser exibida', options=['Perdas de Propriedades','Perdas de Colheitas','Fatalidades','Feridos'])

    return date_min, date_max, states, measure

def aplicar_filtros(data, date_min, date_max, states):
    """
    Função responsável por aplicar os filtros aos dados a serem exibidos na página de visualização de perdas.
    """
    plot_data = data[(data['Date'] >= date_min) & (data['Date'] <= date_max)]

    if len(states):
        plot_data = plot_data[data['State'].isin(states)]

    return plot_data

def exibir_metricas_principais(data,app_directory):
    col1, col2, col3, col4 = st.columns(4)
    space_left,\
    column_image_1, column_1,\
    column_image_2, column_2,\
    column_image_3, column_3,\
    column_image_4, column_4,\
    space_right = st.columns([1.0, 0.7, 2.0, 0.7, 2.0, 0.7, 2.0, 0.7, 2.0, 0.2])

    column_1.metric("Perdas de Propriedades", f"${data['Property_Loss'].sum()/1000000:,.2f} M")
    column_2.metric("Perdas de Colheitas", f"${data['Crop_Loss'].sum()/1000000:,.2f} M")
    column_3.metric("Fatalidades", int(data['Fatalities'].sum()))
    column_4.metric("Feridos", int(data['Injuries'].sum()))

    column_image_1.image(os.path.join(app_directory,"images/perda-de-dinheiro.png"),width=70)
    column_image_2.image(os.path.join(app_directory,"images/plantacoes.png"),width=70)
    column_image_3.image(os.path.join(app_directory,"images/paciente.png"),width=70)
    column_image_4.image(os.path.join(app_directory,"images/farmacia.png"),width=70)

def gerar_serie_temporal(data, metrica):
    st.subheader("Série Temporal de Perdas")
    serie_metrica = (
        "Property_Loss" if metrica == "Perdas de Propriedades" else
        "Crop_Loss" if metrica == "Perdas de Colheitas" else
        "Fatalities" if metrica == "Fatalidades" else
        "Injuries"
    )
    serie_temporal = data[['Date', serie_metrica]]
    serie_temporal['Date'] = pd.to_datetime(serie_temporal['Date'], errors='coerce')
    serie_temporal = serie_temporal.set_index('Date').resample('M').sum()
    st.line_chart(serie_temporal, y=serie_metrica, y_label=metrica, height=450)

def gerar_distribuicao_estado(data, metrica):
    serie_metrica = (
        "Property_Loss" if metrica == "Perdas de Propriedades" else
        "Crop_Loss" if metrica == "Perdas de Colheitas" else
        "Fatalities" if metrica == "Fatalidades" else
        "Injuries"
    )
    st.subheader("Estados com Maiores Perdas")
    barras_por_estado = data.groupby('State')[serie_metrica].sum().reset_index()
    barras_por_estado = barras_por_estado.sort_values(by=serie_metrica, ascending=False)[:20]
    c = alt.Chart(barras_por_estado).mark_bar().encode(y=alt.Y("State", sort=None,title='Estados'), x=alt.X(serie_metrica,title=metrica))
    st.altair_chart(c)

st.title("💰Perdas e Prejuízos")
with st.sidebar:
    st.title('Filtros')
    data = st.session_state['data']
    app_directory = st.session_state['app_directory']
    date_min, date_max, states, measure = criar_filtros(data)
    data = aplicar_filtros(data, date_min, date_max, states)

exibir_metricas_principais(data, app_directory)

time_series, bar_chart = st.columns([0.7,0.3])

with time_series:
    gerar_serie_temporal(data, measure)

with bar_chart:
    gerar_distribuicao_estado(data, measure)
