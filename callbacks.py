# Interatividade: funções que atualizam os gráficos quando os filtros mudam.
# O decorador @callback (sem "app.") registra a função no app que importar este arquivo.

import pandas as pd
import plotly.express as px
from dash import callback, Input, Output

from dados import df, sedes, pais_inicial


CORES = {"Total": "#B8860B", "Ouro": "#D4AF37", "Prata": "#A8A9AD", "Bronze": "#CD7F32"}
ESCALAS_MAPA = {"Total": "YlOrRd", "Ouro": "YlOrBr", "Prata": "Greys", "Bronze": "Oranges"}

LAYOUT_GRAFICOS = dict(
    template="plotly_white",
    margin=dict(l=40, r=20, t=70, b=40),
    font=dict(family="Segoe UI, Arial, sans-serif", size=12),
)


@callback(
    Output("grafico-mapa", "figure"),
    Output("grafico-area", "figure"),
    Input("filtro-medalha", "value"),
)
def atualizar_mapa_e_area(medalha):
    medalhas_pais = df.groupby("Pais", as_index=False)[medalha].sum()
    medalhas_pais = medalhas_pais[medalhas_pais[medalha] > 0]

    fig_mapa = px.choropleth(
        medalhas_pais,
        locations="Pais",
        locationmode="country names",
        color=medalha,
        hover_name="Pais",
        color_continuous_scale=ESCALAS_MAPA[medalha],
        labels={medalha: "Medalhas"},
        title=f"Medalhas por país – {medalha} (1992–2020)",
    )
    fig_mapa.update_layout(**LAYOUT_GRAFICOS)
    fig_mapa.update_geos(
        showframe=False,
        projection_type="natural earth",
        projection_rotation=dict(lon=0, lat=0),
        center=dict(lon=0, lat=15),
        lataxis_range=[-58, 85],
        lonaxis_range=[-180, 180],
    )

    top10 = medalhas_pais.nlargest(10, medalha)["Pais"]
    dados_area = (
        df[df["Pais"].isin(top10)]
        .pivot_table(index="Ano", columns="Pais", values=medalha, aggfunc="sum", fill_value=0)
        .reset_index()
        .melt(id_vars="Ano", var_name="Pais", value_name=medalha)
    )

    fig_area = px.area(
        dados_area,
        x="Ano",
        y=medalha,
        color="Pais",
        category_orders={"Pais": list(top10)},
        labels={"Ano": "Ano", medalha: "Medalhas", "Pais": "País"},
        title=f"Top 10 países – {medalha} ao longo do tempo",
    )
    fig_area.update_layout(**LAYOUT_GRAFICOS)
    fig_area.update_xaxes(tickvals=sorted(df["Ano"].unique()))

    return fig_mapa, fig_area


@callback(
    Output("grafico-barras", "figure"),
    Input("filtro-medalha", "value"),
    Input("filtro-ano", "value"),
)
def atualizar_barras(medalha, ano):
    if ano == "todos":
        dados = df
        periodo = "1992–2020"
    else:
        dados = df[df["Ano"] == ano]
        sede = sedes[sedes["Ano"] == ano].iloc[0]
        periodo = f"{ano} – {sede.Cidade_sede} ({sede.Pais_sede})"

    ranking = dados.groupby("Pais", as_index=False)[medalha].sum().nlargest(10, medalha)

    fig_barras = px.bar(
        ranking,
        x="Pais",
        y=medalha,
        text=medalha,
        color_discrete_sequence=[CORES[medalha]],
        labels={"Pais": "País", medalha: "Medalhas"},
        title=f"Top 10 países – {medalha}<br><sup>{periodo}</sup>",
    )
    fig_barras.update_layout(**LAYOUT_GRAFICOS)
    fig_barras.update_traces(textposition="outside")
    fig_barras.update_xaxes(tickangle=-35)
    return fig_barras


@callback(
    Output("filtro-pais", "value"),
    Input("grafico-mapa", "clickData"),
    prevent_initial_call=True,
)
def selecionar_pais_no_mapa(clique):
    if clique and clique.get("points"):
        return clique["points"][0]["location"]
    return pais_inicial


@callback(
    Output("grafico-pizza", "figure"),
    Input("filtro-pais", "value"),
    Input("filtro-medalha", "value"),
)
def atualizar_pizza(pais, medalha):
    soma = df[df["Pais"] == pais][["Ouro", "Prata", "Bronze"]].sum()
    dados_pizza = pd.DataFrame({
        "Medalha": ["Ouro", "Prata", "Bronze"],
        "Quantidade": [soma["Ouro"], soma["Prata"], soma["Bronze"]],
    })
    total = int(dados_pizza["Quantidade"].sum())
    dados_pizza = dados_pizza[dados_pizza["Quantidade"] > 0]
    palavra = "medalha" if total == 1 else "medalhas"

    fig_pizza = px.pie(
        dados_pizza,
        names="Medalha",
        values="Quantidade",
        color="Medalha",
        color_discrete_map=CORES,
        hole=0.35,
        title=f"{pais}: {total} {palavra} (1992–2020)",
    )
    fig_pizza.update_traces(
        textinfo="label+value+percent",
        textposition="inside",
        insidetextorientation="horizontal",
        pull=[0.12 if fatia == medalha else 0 for fatia in dados_pizza["Medalha"]],
        sort=False,
    )
    fig_pizza.update_layout(**LAYOUT_GRAFICOS)
    fig_pizza.update_layout(showlegend=False)
    return fig_pizza
