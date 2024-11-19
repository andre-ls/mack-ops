import os
import streamlit as st

app_directory = st.session_state['app_directory']

st.title('🔎Análise de Dados de Tornados')

st.image('https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEggMzfrIJ4_RGzPEqaBxtuwHYpGbtxUNzXc9n00Jv3YLmL90GCBzrJZuAQW9WMcm4Rt15JweSuwB8Mcbtaq89e5itCHlbYHuz8rzfazVB2mpaw2xT7IBPg5KxeA7Cdk0WJT1HBiUMeCqfQ/s640/Mike-Hollingshead_Tornado_1.gif')

st.write('Tornados consistem em um fenômeno metereológico extremo que causam uma quantidade exorbitante de danos por onde passam, desde casas e carros destruídos até vidas perdidas. Com o objetivo de contribuir para um maior entendimento destes acontecimentos, esta aplicação explora algunas dados sobre tornados ocorridos principalmente em territórios dos Estados Unidos, observando a sua trajetória, algumas de suas características fisicas e os danos causados em termos econômicos. A partir da análise destes dados, esperamos que decisões possam ser tomadas, contribuindo para a mitigação de danos futuros e a preservação de mais vidas.')

st.header('Dados')

st.image('https://www.fema.gov/profiles/femad8_gov/themes/fema_uswds/images/fema-logo-blue.svg',width=800)

st.write('Os dados utilizados neste projeto são fornecidos abertamente pelo FEMA, a Agência Federal de Gestão de Emergências dos Estados Unidos, e englobam dados de tornados que ocorreram entre 1950 e 2022 nos territórios dos Estados Unidos, Porto Rico e Ilhas Virgens Americanas.')

st.write('Dentre as variáveis fornecidas, estão as coordenadas de início e fim da trajetória dos tornados, sua magnitude, tamanho físico e danos causados à propriedades e plantações estimados em dólares.')

st.markdown('Os dados podem ser acessados [aqui](https://gis-fema.hub.arcgis.com/datasets/fedmaps::tornado-tracks-1/about).')

st.header('Sobre o Projeto')

st.image('https://logodownload.org/wp-content/uploads/2017/09/mackenzie-logo.png',width=500)

st.write('Este projeto foi desenvolvido como trabalho final da disciplina de DevOps e DataOps, componente do curso de Pós-Graduação em Engenharia de Dados oferecido pela Universidade Presbiteriana Mackenzie e lecionada pelo Prof. Gustavo Calixto.')

st.write('O objetivo proposto foi o de aplicar os conhecimentos adquiridos ao longo das aulas para construir uma solução de Análise de Dados utilizando como base principal de ferramentas o Streamlit e códigos de processamento de dados em Python, mas principalmente aplicando durante o processo de construção as melhores práticas de organização e colaboração para a consrução de uma solução em software, como a gestão do projeto via repositório, organização em Sprints e a utilização das funcionalidade de CI/CD do Streamlit para uma rápida testagem e produtização do código.')

st.markdown("""
Membros do Grupo:
- André Luis Andrade Machado
- Eduardo Tedeschi
- Murilo Garcia Ortega
""")
