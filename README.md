# 🔎Análise de Dados de Tornados

![Tornado](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEggMzfrIJ4_RGzPEqaBxtuwHYpGbtxUNzXc9n00Jv3YLmL90GCBzrJZuAQW9WMcm4Rt15JweSuwB8Mcbtaq89e5itCHlbYHuz8rzfazVB2mpaw2xT7IBPg5KxeA7Cdk0WJT1HBiUMeCqfQ/s640/Mike-Hollingshead_Tornado_1.gif)

Tornados consistem em um fenômeno metereológico extremo que causam uma quantidade exorbitante de danos por onde passam, desde casas e carros destruídos até vidas perdidas. Em 2024, ano em que este projeto foi desenvolvido, o Furacão Milton, estimado como um dos mais caros da história, causou sozinho um prejuízo estimado de 34 bilhões de dólares e 35 mortes.

Com o objetivo de contribuir para um maior entendimento destes fenômenos, este projeto propõe como ideia principal a construção de um dashboard capaz de permitir a análise e exploração de dados públicos sobre a ocorrência de Tornados em territórios dos Estados Unidos, país com a maior ocorrência deste fenômeno no mundo. As visualizações e análises geradas permitem a extração sobre trajetórias, características fisicas e prejuízos econômicos causados por tornados em um histórico de mais de 50 anos de registros. 

A partir destas análises, esperamos que informações relevantes possam ser extraídas e decisões possam ser tomadas, contribuindo para a mitigação de danos futuros e a preservação de mais vidas.

## Dados

<img src="https://www.fema.gov/profiles/femad8_gov/themes/fema_uswds/images/fema-logo-blue.svg" alt="Fema" width="600"/>

Os dados utilizados neste projeto são fornecidos abertamente pelo FEMA, a Agência Federal de Gestão de Emergências dos Estados Unidos, e englobam dados de tornados que ocorreram entre 1950 e 2022 nos territórios dos Estados Unidos, Porto Rico e Ilhas Virgens Americanas.

As variáveis fornecidas incluem:
- Data de Ocorrência
- Estado
- Magnitude do Tornado
- Quantidade de Feridos
- Quantidade de Fatalidades
- Perdas de Propriedades (Estimada em Dólares)
- Perdas de Plantações (Estimada em Dólares)
- Coordenadas de Início e Fim da Trajetória do Tornado
- Comprimento e Largura do Tornado

Os dados podem ser acessados [aqui](https://gis-fema.hub.arcgis.com/datasets/fedmaps::tornado-tracks-1/about).

## Ferramentas Utilizadas

Para a composição deste projeto, uma estrutura simples foi montada utilizando as seguintes ferramentas:
- Linguagem Python, para limpeza e processamento dos dados.
- Streamlit, para construção do dashboard e grande parte de suas visualizações.
- Kepler.gl, para construção de visualizações de mapas.

## Resultados

Como resultado, construiu-se uma aplicação no Streamlit compondo um dashboard com 3 páginas principais:

- Visualização de Mapas: Página contendo gráficos em mapas para exploração da trajetória dos tornados, e algumas métricas agregadas por Estado.
- Visualização de Dados Físicos: Página contendo visualizações focadas na exploração de características físicas dos tornados, como suas dimensões, distâncias percorridas e data de ocorrência.
- Visualização de Perdas: Página contendo visualizações focadas nos danos e perdas econômicas causadas pelos tornados.

## Sobre o Projeto

<img src="https://logodownload.org/wp-content/uploads/2017/09/mackenzie-logo.png" alt="Mackenzie" width="500"/>

Este projeto foi desenvolvido como trabalho final da disciplina de DevOps e DataOps, componente do curso de Pós-Graduação em Engenharia de Dados oferecido pela Universidade Presbiteriana Mackenzie e lecionada pelo Prof. Gustavo Calixto.

O objetivo proposto foi o de aplicar os conhecimentos adquiridos ao longo das aulas para construir uma solução de Análise de Dados utilizando como base principal de ferramentas o Streamlit e códigos de processamento de dados em Python, mas principalmente aplicando durante o processo de construção as melhores práticas de organização e colaboração para a consrução de uma solução em software, como a gestão do projeto via repositório, organização em Sprints e a utilização das funcionalidade de CI/CD do Streamlit para uma rápida testagem e produtização do código.

Membros do Grupo:
- André Luis Andrade Machado
- Eduardo Tedeschi
- Murilo Garcia Ortega
