QUADRO DE MEDALHAS OLÍMPICAS (1992–2020)
______________________________________________

Dashboard interativo com o desempenho dos países nos Jogos
Olímpicos de Verão de 1992 a 2020, feito em Python com Dash e
Plotly Express.

>> ACESSAR O DASHBOARD ONLINE:
   https://quadro-medalhas.onrender.com

>> REPOSITÓRIO NO GITHUB:
   https://github.com/karlapardocimo/quadro_medalhas


SOBRE O PROJETO
----------------------------------------------------------------
Trabalho da disciplina de Visualização de Dados do curso de
Gestão da Tecnologia da Informação do IF Sudeste MG – Campus
Muriaé.

Foi utilizado o tutorial "Dashboard Quadro de Medalhas
Olímpicas", que monta um mapa, um gráfico de área empilhada e um
gráfico de barras. O projeto expande esse painel com novos
gráficos, filtros interativos e organização do código em módulos.


FUNCIONALIDADES
----------------------------------------------------------------
Mapa coroplético ........ Países coloridos pela quantidade de
                          medalhas. Clique em um país para
                          vê-lo na pizza.
Gráfico de pizza ........ Ouro, Prata e Bronze do país
                          selecionado.
Área empilhada .......... Evolução dos 10 maiores países ao
                          longo das edições.
Barras .................. Ranking dos 10 países com mais
                          medalhas.
Filtro de medalha ....... Todos, Ouro, Prata ou Bronze,
                          aplicado a todos os gráficos.
Filtro de ano olímpico .. Escolhe a edição (ex.: 2016 – Rio de
                          Janeiro) no gráfico de barras.

Tratamento dos dados:
  - "United States" -> "United States of America", para o mapa
    reconhecer o país
  - "ROC" (Tóquio 2020) -> "Russia", para somar com as outras
    edições
  - Colunas traduzidas para português e recorte do período
    1992–2020


----------------------------------------------------------------
COMO RODAR LOCALMENTE
----------------------------------------------------------------
  git clone https://github.com/karlapardocimo/quadro_medalhas.git
  cd quadro_medalhas
  pip install -r requirements.txt
  python app.py

Depois, abra http://127.0.0.1:8050 no navegador.

DEPLOY
----------------------------------------------------------------
Publicado no Render (https://render.com) como Web Service:

  Build Command:  pip install -r requirements.txt
  Start Command:  gunicorn app:server


