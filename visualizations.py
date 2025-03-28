import streamlit as st
import matplotlib.pyplot as plt
import altair as alt
import folium
import pandas as pd
from streamlit_folium import folium_static
from folium.plugins import HeatMap

def exibir_indicadores(df):
    """Mostra indicadores rápidos no Streamlit."""
    if df.empty:
        st.warning("⚠️ Nenhum dado disponível para os indicadores.")
        return

    st.metric("🔋 Total de Usinas", len(df))
    st.metric("⚡ Potência Média (kW)", df["MdaPotenciaFiscalizadaKw"].mean())

def grafico_temporal(df):
    """Gera gráfico de evolução da potência fiscalizada ao longo do tempo."""
    if df.empty:
        st.warning("⚠️ Nenhum dado disponível para o gráfico temporal.")
        return

    st.subheader("📈 Evolução da Potência Fiscalizada ao longo do tempo")
    chart = alt.Chart(df).mark_line().encode(
        x="DatInicioVigencia:T",
        y="MdaPotenciaFiscalizadaKw:Q",
        color="SigUFPrincipal:N"
    ).interactive()
    st.altair_chart(chart, use_container_width=True)

def grafico_barras(df):
    """Cria um gráfico de barras para distribuição de potência por estado."""
    if df.empty:
        st.warning("⚠️ Nenhum dado disponível para o gráfico de barras.")
        return

    st.subheader("📊 Distribuição de Potência Fiscalizada por Estado")
    fig, ax = plt.subplots(figsize=(12, 6))
    df.groupby("SigUFPrincipal")["MdaPotenciaFiscalizadaKw"].sum().plot(kind="bar", ax=ax)
    ax.set_ylabel("Potência Fiscalizada (kW)")
    ax.set_xlabel("Estado")
    ax.set_title("Distribuição de Potência por Estado")
    st.pyplot(fig)


def grafico_barra_com_media_anual(df):
    """Gera gráfico de barras com potência anual, média dos anos anteriores e média geral."""
    if df.empty or "DatInicioVigencia" not in df.columns:
        st.warning("⚠️ Dados insuficientes para gerar o gráfico por ano.")
        return

    st.subheader("📊 Potência Fiscalizada por Ano com Médias Comparativas")
    st.markdown("""
### ℹ️ Como interpretar este gráfico

- As **barras azuis** representam a **potência fiscalizada total** registrada em cada ano.
- A **linha laranja pontilhada** mostra a **média dos anos anteriores**, permitindo comparar cada barra com o histórico até aquele ponto.
- A **linha verde contínua** representa a **média geral** no período selecionado.

Esse gráfico ajuda a identificar anos com desempenho **acima ou abaixo da tendência histórica**.
""")

    # 🎯 Preparar dados
    df["Ano"] = df["DatInicioVigencia"].dt.year
    df_ano = df.groupby("Ano")["MdaPotenciaFiscalizadaKw"].sum().reset_index()
    df_ano = df_ano.sort_values("Ano")  # garantir ordenação cronológica

    # 📈 Média dos anos anteriores
    df_ano["MediaAnosAnteriores"] = df_ano["MdaPotenciaFiscalizadaKw"].expanding().mean().shift(1)

    # 📉 Média geral do período
    media_geral = df_ano["MdaPotenciaFiscalizadaKw"].mean()
    df_ano["MediaGeral"] = media_geral

    # 🧱 Construir gráfico Altair
    base = alt.Chart(df_ano).encode(x=alt.X("Ano:O", title="Ano"))

    barras = base.mark_bar(color="#1f77b4").encode(
        y=alt.Y("MdaPotenciaFiscalizadaKw:Q", title="Potência Fiscalizada (kW)"),
        tooltip=[
            alt.Tooltip("Ano:O"),
            alt.Tooltip("MdaPotenciaFiscalizadaKw:Q", title="Potência"),
            alt.Tooltip("MediaAnosAnteriores:Q", title="Média até o ano anterior"),
            alt.Tooltip("MediaGeral:Q", title="Média geral do período")
        ]
    )

    linha_media_acumulada = base.mark_line(color="orange", strokeDash=[4, 4], point=True).encode(
        y="MediaAnosAnteriores:Q"
    )

    linha_media_geral = base.mark_rule(color="green", size=5).encode(
        y="MediaGeral:Q"
    )

    chart_final = (barras + linha_media_acumulada + linha_media_geral).properties(
        width=750,
        height=400,
        title="Evolução Anual da Potência Fiscalizada"
    )

    st.altair_chart(chart_final, use_container_width=True)


def mapa_usinas(df, tipo_mapa="Mapa Normal"):
    """Cria um mapa interativo com a distribuição das usinas e opção de Heatmap."""
    if df.empty or "NumCoordNEmpreendimento" not in df.columns or "NumCoordEEmpreendimento" not in df.columns:
        st.warning("⚠️ Dados de latitude e longitude não disponíveis para criar o mapa.")
        return

    # 🔄 Converter latitude e longitude para float (corrige erro de string)
    df["NumCoordNEmpreendimento"] = pd.to_numeric(df["NumCoordNEmpreendimento"].astype(str).str.replace(",", "."), errors="coerce")
    df["NumCoordEEmpreendimento"] = pd.to_numeric(df["NumCoordEEmpreendimento"].astype(str).str.replace(",", "."), errors="coerce")

    # 🔍 Remover linhas com valores NaN após conversão
    df = df.dropna(subset=["NumCoordNEmpreendimento", "NumCoordEEmpreendimento"])

    # 🚨 Verificar se ainda há dados após limpeza
    if df.empty:
        st.warning("⚠️ Nenhum dado válido para exibir no mapa após conversão de coordenadas.")
        return

    # Criar mapa centralizado na média das coordenadas
    mapa = folium.Map(location=[df["NumCoordNEmpreendimento"].mean(), df["NumCoordEEmpreendimento"].mean()], zoom_start=5)

    # 🔥 Selecione entre mapa normal ou heatmap
    if tipo_mapa == "Mapa de Calor":
        heat_data = df[["NumCoordNEmpreendimento", "NumCoordEEmpreendimento"]].values.tolist()
        HeatMap(heat_data, radius=15, blur=10, max_zoom=10).add_to(mapa)
    else:
        for _, row in df.iterrows():
            folium.Marker(
                location=[row["NumCoordNEmpreendimento"], row["NumCoordEEmpreendimento"]],
                popup=f"{row['NomEmpreendimento']} - {row['SigUFPrincipal']}",
                tooltip=row['NomEmpreendimento']
            ).add_to(mapa)

    st.subheader("🗺️ Mapa Geoespacial - Distribuição das Usinas")
    folium_static(mapa)
