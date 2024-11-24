import streamlit as st
import pandas as pd
from pathlib import Path
from keplergl import KeplerGl

# Função para carregar os dados
def carregar_dados(file_path):
    if not file_path.exists():
        st.error(f"O arquivo não foi encontrado no caminho: {file_path}")
        return None
    data = pd.read_csv(file_path)
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
    data = data.dropna(subset=['Start_Latitude', 'Start_Longitude', 'Magnitude', 'Property_Loss', 'Crop_Loss'])
    data['Magnitude'] = pd.to_numeric(data['Magnitude'], errors='coerce')
    data['Property_Loss'] = pd.to_numeric(data['Property_Loss'], errors='coerce')
    data['Crop_Loss'] = pd.to_numeric(data['Crop_Loss'], errors='coerce')
    return data

# Função para exibir as métricas principais
def exibir_metricas_principais(filtered_data):
    st.subheader("Métricas Principais")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Perdas de Propriedades", f"${filtered_data['Property_Loss'].sum():,.2f}")
    col2.metric("Perdas de Colheitas", f"${filtered_data['Crop_Loss'].sum():,.2f}")
    col3.metric("Fatalidades", int(filtered_data['Fatalities'].sum()))
    col4.metric("Feridos", int(filtered_data['Injuries'].sum()))

# Função para gerar a série temporal
def gerar_serie_temporal(filtered_data, metrica):
    serie_metrica = (
        "Property_Loss" if metrica == "Perdas de Propriedades" else
        "Crop_Loss" if metrica == "Perdas de Colheitas" else
        "Fatalities" if metrica == "Fatalidades" else
        "Injuries"
    )
    serie_temporal = filtered_data[['Date', serie_metrica]].set_index('Date').resample('M').sum()
    st.line_chart(serie_temporal, y=serie_metrica)

# Função para gerar a distribuição por estado
def gerar_distribuicao_estado(filtered_data, serie_metrica):
    st.subheader("Distribuição por Estado")
    barras_por_estado = filtered_data.groupby('State')[serie_metrica].sum()
    st.bar_chart(barras_por_estado)

# Função para gerar o mapa interativo
def gerar_mapa_interativo(filtered_data):
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

# Função para aplicar os filtros de dados
def aplicar_filtros(data):
    """
    Filtro de intervalo de datas
    """
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
    """
    estado_default = data['State'].unique()[:10]
    estado = st.sidebar.multiselect(
        "Estado(s) - Pesquisar ou Selecionar",
        options=data['State'].unique(),
        default=estado_default,
        help="Pesquise ou selecione os estados desejados",
    )
    filtered_data = filtered_data[filtered_data['State'].isin(estado)]

    return filtered_data

# Função principal para orquestrar a aplicação
def main():
    st.title("Análise de Perdas e Prejuízos de Tornados")
    st.sidebar.header("Filtros")

    # Define o caminho do arquivo usando Pathlib
    file_path = Path("data") / "processed" / "tornado_processed_data.csv"

    # Carregar os dados
    data = carregar_dados(file_path)

    if data is not None:
        # Aplicar filtros
        filtered_data = aplicar_filtros(data)

        # Seleção de métrica
        metrica = st.sidebar.selectbox(
            "Métrica a ser exibida",
            ["Perdas de Propriedades", "Perdas de Colheitas", "Fatalidades", "Feridos"]
        )

        # Exibir as métricas principais
        exibir_metricas_principais(filtered_data)

        # Gerar a série temporal
        gerar_serie_temporal(filtered_data, metrica)

        # Gerar a distribuição por estado
        gerar_distribuicao_estado(filtered_data, metrica)

        # Gerar o mapa interativo
        gerar_mapa_interativo(filtered_data)

if __name__ == "__main__":
    main()
