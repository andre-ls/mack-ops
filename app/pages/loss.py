import streamlit as st
import pandas as pd


def criar_filtros(data):
    """
    Função responsável por configurar os filtros presentes na página de visualização de perdas.
    """
    date_min, date_max = st.select_slider('Data', options=data['Date'].sort_values(), value=[data['Date'].min(),data['Date'].max()])
    states = st.multiselect('Estado', data['State'].unique(), default=None)
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

def exibir_metricas_principais(data):
    st.subheader("Métricas Principais")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Perdas de Propriedades", f"${data['Property_Loss'].sum():,.2f}")
    col2.metric("Perdas de Colheitas", f"${data['Crop_Loss'].sum():,.2f}")
    col3.metric("Fatalidades", int(data['Fatalities'].sum()))
    col4.metric("Feridos", int(data['Injuries'].sum()))

def gerar_serie_temporal(data, metrica):
    serie_metrica = (
        "Property_Loss" if metrica == "Perdas de Propriedades" else
        "Crop_Loss" if metrica == "Perdas de Colheitas" else
        "Fatalities" if metrica == "Fatalidades" else
        "Injuries"
    )
    serie_temporal = data[['Date', serie_metrica]]
    serie_temporal['Date'] = pd.to_datetime(serie_temporal['Date'], errors='coerce')
    serie_temporal = serie_temporal.set_index('Date').resample('M').sum()
    st.line_chart(serie_temporal, y=serie_metrica)

def gerar_distribuicao_estado(data, metrica):
    serie_metrica = (
        "Property_Loss" if metrica == "Perdas de Propriedades" else
        "Crop_Loss" if metrica == "Perdas de Colheitas" else
        "Fatalities" if metrica == "Fatalidades" else
        "Injuries"
    )
    st.subheader("Distribuição por Estado")
    barras_por_estado = data.groupby('State')[serie_metrica].sum()
    st.bar_chart(barras_por_estado)

# Função principal para orquestrar a aplicação
st.title("Análise de Perdas e Prejuízos de Tornados")
with st.sidebar:
    st.title('Filtros')
    data = st.session_state['data']
    app_directory = st.session_state['app_directory']
    date_min, date_max, states, measure = criar_filtros(data)

exibir_metricas_principais(data)

# Gerar a série temporal
gerar_serie_temporal(data, measure)

# Gerar a distribuição por estado
gerar_distribuicao_estado(data, measure)
