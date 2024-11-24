import streamlit as st
import pandas as pd
from pathlib import Path
from keplergl import KeplerGl

# Define o caminho do arquivo usando Pathlib
file_path = Path("data") / "processed" / "tornado_processed_data.csv"

# Verifica se o arquivo existe
if not file_path.exists():
    st.error(f"O arquivo não foi encontrado no caminho: {file_path}")
else:
    """
    Carrega, processa e exibe os dados dos tornados.
    - Carrega os dados de um arquivo CSV.
    - Converte as colunas relevantes para os tipos de dados corretos.
    - Remove registros com valores ausentes nas colunas críticas.
    - Exibe as métricas de perdas e fatalidades.
    """
    
    # Carrega e processa os dados
    data = pd.read_csv(file_path)
    data['Date'] = pd.to_datetime(data['Date'])
    data = data.dropna(subset=['Start_Latitude', 'Start_Longitude', 'Magnitude', 'Property_Loss', 'Crop_Loss'])
    data['Magnitude'] = pd.to_numeric(data['Magnitude'], errors='coerce')
    data['Property_Loss'] = pd.to_numeric(data['Property_Loss'], errors='coerce')
    data['Crop_Loss'] = pd.to_numeric(data['Crop_Loss'], errors='coerce')

    # Configurações da interface
    st.title("Análise de Perdas e Prejuízos de Tornados")
    st.sidebar.header("Filtros")

    """
    Filtro de intervalo de datas
    - Permite selecionar um intervalo de datas para filtrar os dados.
    - O intervalo é determinado pelos valores mínimo e máximo encontrados no conjunto de dados.
    """
    
    # Filtro de intervalo de datas
    min_date = data['Date'].min()
    max_date = data['Date'].max()
    start_date, end_date = st.sidebar.date_input(
        "Intervalo de Datas",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )
    filtered_data = data[(data['Date'] >= pd.Timestamp(start_date)) & (data['Date'] <= pd.Timestamp(end_date))]

    """
    Filtro de estados
    - Permite selecionar múltiplos estados para filtrar os dados.
    - O usuário pode pesquisar ou selecionar os estados desejados.
    """
    
    # Filtro de estados
    estado_default = data['State'].unique()[:10]
    estado = st.sidebar.multiselect(
        "Estado(s) - Pesquisar ou Selecionar",
        options=data['State'].unique(),
        default=estado_default,
        help="Pesquise ou selecione os estados desejados",
    )
    filtered_data = filtered_data[filtered_data['State'].isin(estado)]

    """
    Seleção de métrica
    - Permite ao usuário selecionar a métrica a ser exibida: perdas de propriedades, perdas de colheitas, fatalidades ou feridos.
    """
    
    # Seleção de métrica
    metrica = st.sidebar.selectbox(
        "Métrica a ser exibida",
        ["Perdas de Propriedades", "Perdas de Colheitas", "Fatalidades", "Feridos"]
    )

    """
    Exibição de métricas principais
    - Exibe os totais de perdas de propriedades, perdas de colheitas, fatalidades e feridos.
    - Cada métrica é exibida em uma coluna separada.
    """
    
    # Exibição de métricas principais
    st.subheader("Métricas Principais")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Perdas de Propriedades", f"${filtered_data['Property_Loss'].sum():,.2f}")
    col2.metric("Perdas de Colheitas", f"${filtered_data['Crop_Loss'].sum():,.2f}")
    col3.metric("Fatalidades", int(filtered_data['Fatalities'].sum()))
    col4.metric("Feridos", int(filtered_data['Injuries'].sum()))

    """
    Série temporal das métricas
    - Exibe um gráfico de linha representando a série temporal das métricas selecionadas (perdas de propriedades, perdas de colheitas, fatalidades ou feridos).
    """
    
    # Série temporal das métricas
    st.subheader("Série Temporal das Métricas")
    serie_metrica = (
        "Property_Loss" if metrica == "Perdas de Propriedades" else
        "Crop_Loss" if metrica == "Perdas de Colheitas" else
        "Fatalities" if metrica == "Fatalidades" else
        "Injuries"
    )
    serie_temporal = filtered_data[['Date', serie_metrica]].set_index('Date').resample('M').sum()
    st.line_chart(serie_temporal, y=serie_metrica)

    """
    Distribuição por estado
    - Exibe um gráfico de barras mostrando a distribuição das perdas ou fatalidades por estado.
    """
    
    # Distribuição por estado
    st.subheader("Distribuição por Estado")
    barras_por_estado = filtered_data.groupby('State')[serie_metrica].sum()
    st.bar_chart(barras_por_estado)

    """
    Mapa interativo
    - Exibe um mapa interativo mostrando a localização dos tornados, com informações como magnitude, perdas e colheitas.
    """
    
    # Mapa interativo
    st.subheader("Mapa Interativo dos Tornados")
    map_data = filtered_data[['Start_Latitude', 'Start_Longitude', 'Date', 'Magnitude', 'Property_Loss', 'Crop_Loss']]
    map_data['Date'] = map_data['Date'].dt.strftime('%Y-%m-%d')
    map_data['Property_Loss'] = map_data['Property_Loss'].fillna(0).astype(int)
    map_data['Crop_Loss'] = map_data['Crop_Loss'].fillna(0).astype(int)
    map_data = map_data.rename(columns={"Start_Latitude": "latitude", "Start_Longitude": "longitude"})

    kepler_map = KeplerGl(height=600)
    kepler_map.add_data(data=map_data, name="Tornados")
    map_file = "kepler_map.html"
    kepler_map.save_to_html(file_name=map_file)

    with open(map_file, "r", encoding="utf-8") as f:
        map_html = f.read()
    st.components.v1.html(map_html, height=600)
