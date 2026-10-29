# Leitura, limpeza e preparação dos dados usados pelo dashboard.

import os
import pandas as pd


PASTA = os.path.dirname(os.path.abspath(__file__))

df = pd.read_csv(os.path.join(PASTA, "Country_Medals.csv"), sep=None, engine="python")
df.columns = df.columns.str.strip()

df = df.rename(columns={
    "Year": "Ano",
    "Host_country": "Pais_sede",
    "Host_city": "Cidade_sede",
    "Country_Name": "Pais",
    "Country_Code": "Sigla",
    "Gold": "Ouro",
    "Silver": "Prata",
    "Bronze": "Bronze",
})

df["Pais"] = df["Pais"].replace({
    "United States": "United States of America",
    "ROC": "Russia",
})

for coluna in ["Ouro", "Prata", "Bronze"]:
    df[coluna] = pd.to_numeric(df[coluna], errors="coerce").fillna(0).astype(int)

df = df[(df["Ano"] >= 1992) & (df["Ano"] <= 2020)].copy()
df["Total"] = df["Ouro"] + df["Prata"] + df["Bronze"]


OPCOES_MEDALHA = [
    {"label": "Todos", "value": "Total"},
    {"label": "Ouro", "value": "Ouro"},
    {"label": "Prata", "value": "Prata"},
    {"label": "Bronze", "value": "Bronze"},
]

sedes = df.groupby("Ano", as_index=False)[["Cidade_sede", "Pais_sede"]].first()

opcoes_ano = [{"label": "Todos os anos (1992–2020)", "value": "todos"}]
for linha in sedes.itertuples():
    opcoes_ano.append({
        "label": f"{linha.Ano} – {linha.Cidade_sede} ({linha.Pais_sede})",
        "value": int(linha.Ano),
    })

paises = sorted(df["Pais"].dropna().unique())
pais_inicial = "Brazil"
