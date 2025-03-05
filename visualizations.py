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
