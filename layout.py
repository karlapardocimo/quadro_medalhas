# Estrutura da página: o que aparece e em que ordem.
# A aparência (cores, espaços, sombras) fica em assets/estilo.css.

from dash import dcc, html

from dados import OPCOES_MEDALHA, opcoes_ano, paises, pais_inicial


CONFIG_GRAFICOS = {"displayModeBar": False}


def cartao(grafico_id, classe_extra=""):
    return html.Div(
        dcc.Graph(id=grafico_id, className=classe_extra, config=CONFIG_GRAFICOS),
        className="cartao",
    )


layout = html.Div(className="pagina", children=[

    html.H1("Quadro de Medalhas Olímpicas (1992–2020)", className="titulo"),
    html.P("Use os filtros abaixo ou clique em um país no mapa para ver as medalhas dele no gráfico de pizza.",
           className="subtitulo"),

    html.Div(className="cartao filtros", children=[
        html.Div([
            html.Label("Tipo de medalha (todos os gráficos)", className="rotulo"),
            dcc.RadioItems(id="filtro-medalha", options=OPCOES_MEDALHA, value="Total", inline=True),
        ]),
        html.Div(className="filtro-largo", children=[
            html.Label("Ano olímpico / País sede (gráfico de barras)", className="rotulo"),
            dcc.Dropdown(id="filtro-ano", options=opcoes_ano, value="todos", clearable=False),
        ]),
        html.Div(className="filtro-largo", children=[
            html.Label("País (gráfico de pizza)", className="rotulo"),
            dcc.Dropdown(id="filtro-pais", options=paises, value=pais_inicial, clearable=False),
        ]),
    ]),

    html.Div(className="linha linha-mapa", children=[
        cartao("grafico-mapa", "grafico-alto"),
        cartao("grafico-pizza", "grafico-alto"),
    ]),

    html.Div(className="linha linha-meio", children=[
        cartao("grafico-area"),
        cartao("grafico-barras"),
    ]),

    html.P("Fonte dos dados: Kaggle – Olympic Medals by Country (Country_Medals.csv)", className="rodape"),
])
