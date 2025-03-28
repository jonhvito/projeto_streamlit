import geopandas as gpd
from shapely.geometry import Point
from esda.moran import Moran, Moran_Local
from libpysal.weights import DistanceBand
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from streamlit_folium import folium_static
import folium
from folium.plugins import MiniMap, MeasureControl


# =============================
# 🌐 Função: Moran Global
# =============================
def calcular_moran_global(df, coluna_valor="MdaPotenciaFiscalizadaKw", distancia_km=300):
    """Calcula o Moran's I Global com base nas coordenadas das usinas."""

    st.subheader("🧭 Análise Espacial - Moran's I Global")

    if df.empty or "NumCoordNEmpreendimento" not in df.columns or "NumCoordEEmpreendimento" not in df.columns:
        st.warning("⚠️ Dados geoespaciais ausentes. Não é possível calcular o índice de Moran.")
        return

    # 🧹 Corrigir coordenadas
    try:
        df["NumCoordNEmpreendimento"] = df["NumCoordNEmpreendimento"].astype(str).str.replace(",", ".").astype(float)
        df["NumCoordEEmpreendimento"] = df["NumCoordEEmpreendimento"].astype(str).str.replace(",", ".").astype(float)
    except Exception as e:
        st.error(f"Erro ao converter coordenadas: {e}")
        return

    # 🔍 Remover inválidos
    df = df.dropna(subset=["NumCoordEEmpreendimento", "NumCoordNEmpreendimento"])
    if df.empty:
        st.warning("⚠️ Não há dados válidos de coordenadas após limpeza.")
        return

    # 📍 Criar geometria
    try:
        df["geometry"] = df.apply(lambda row: Point(row["NumCoordEEmpreendimento"], row["NumCoordNEmpreendimento"]), axis=1)
        gdf = gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:4326")
    except Exception as e:
        st.error(f"Erro ao criar GeoDataFrame: {e}")
        return

    # 🌐 Matriz de vizinhança
    try:
        threshold_degraus = distancia_km / 111
        coords = [(geom.x, geom.y) for geom in gdf.geometry]
        w = DistanceBand(coords, threshold=threshold_degraus, binary=True, silence_warnings=True)
    except Exception as e:
        st.error(f"Erro ao criar matriz de vizinhança: {e}")
        return

    # 📈 Calcular Moran Global
    try:
        y = gdf[coluna_valor].fillna(0)
        moran = Moran(y, w)
    except Exception as e:
        st.error(f"Erro ao calcular Moran's I: {e}")
        return

    # 📊 Exibir resultados
    st.markdown(f"""
    ### 📊 Resultados do Índice de Moran (Global)

    - **Índice de Moran (I)**: `{moran.I:.4f}`
    - **p-valor (simulado)**: `{moran.p_sim:.4f}`

    **Como interpretar:**
    - Valores de `I` positivos indicam autocorrelação espacial (valores semelhantes estão próximos).
    - Valores de `I` próximos de 0 indicam aleatoriedade.
    - `p-valor < 0.05` indica que a autocorrelação é estatisticamente significativa.
    """)

# =============================
# 🔍 Função: LISA Local
# =============================
def calcular_lisa_local(df, coluna_valor="MdaPotenciaFiscalizadaKw", distancia_km=300):
    """Calcula o índice LISA (Moran Local) e mostra um mapa de clusters com visual refinado."""

    st.subheader("🧭 Análise Espacial - LISA (Clusters Locais)")

    # 🔁 Correção e validação de coordenadas
    try:
        df["NumCoordNEmpreendimento"] = df["NumCoordNEmpreendimento"].astype(str).str.replace(",", ".").astype(float)
        df["NumCoordEEmpreendimento"] = df["NumCoordEEmpreendimento"].astype(str).str.replace(",", ".").astype(float)
        df = df.dropna(subset=["NumCoordNEmpreendimento", "NumCoordEEmpreendimento"])
        df["geometry"] = df.apply(lambda row: Point(row["NumCoordEEmpreendimento"], row["NumCoordNEmpreendimento"]), axis=1)
        gdf = gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:4326")
    except Exception as e:
        st.error(f"Erro ao preparar dados geográficos: {e}")
        return

    # 🌐 Matriz de vizinhança
    try:
        threshold_degraus = distancia_km / 111
        coords = [(geom.x, geom.y) for geom in gdf.geometry]
        w = DistanceBand(coords, threshold=threshold_degraus, binary=True, silence_warnings=True)
    except Exception as e:
        st.error(f"Erro ao gerar vizinhança espacial: {e}")
        return

    # 📈 Calcular LISA
    try:
        y = gdf[coluna_valor].fillna(0)
        lisa = Moran_Local(y, w)
    except Exception as e:
        st.error(f"Erro ao calcular LISA: {e}")
        return

    # 📊 Classificação dos clusters
    cluster_labels = np.full(len(gdf), "Não Significativo")
    sig = lisa.p_sim < 0.05
    HH = (sig) & (lisa.q == 1)
    LL = (sig) & (lisa.q == 3)
    LH = (sig) & (lisa.q == 2)
    HL = (sig) & (lisa.q == 4)

    cluster_labels[HH] = "Alta-Alta 🔥"
    cluster_labels[LL] = "Baixa-Baixa ❄️"
    cluster_labels[LH] = "Baixa-Alta"
    cluster_labels[HL] = "Alta-Baixa"
    gdf["Cluster"] = cluster_labels

    # 🎨 Visual refinado
    st.markdown("### 🗺️ Mapa de Clusters Locais (LISA)")
    st.markdown("Cada ponto é colorido de acordo com o tipo de associação espacial que apresenta.")

    try:
        import seaborn as sns
        palette = {
            "Alta-Alta 🔥": sns.color_palette("Reds", n_colors=3)[-1],
            "Baixa-Baixa ❄️": sns.color_palette("Blues", n_colors=3)[-1],
            "Alta-Baixa": sns.color_palette("Greens", n_colors=3)[-1],
            "Baixa-Alta": sns.color_palette("Oranges", n_colors=3)[-1],
            "Não Significativo": "lightgray"
        }

        plt.style.use("dark_background")
        fig, ax = plt.subplots(figsize=(10, 6))

        for cluster, color in palette.items():
            gdf[gdf["Cluster"] == cluster].plot(
                ax=ax,
                color=color,
                label=cluster,
                markersize=60,
                edgecolor='black',
                linewidth=0.5,
                alpha=0.85
            )

        ax.set_title("Clusters Locais - LISA", fontsize=14, fontweight='bold')
        ax.set_xlabel("Longitude", fontsize=10)
        ax.set_ylabel("Latitude", fontsize=10)

        ax.legend(
            title="Tipo de Cluster",
            loc="center left",
            bbox_to_anchor=(1.05, 0.5),
            fontsize=9,
            title_fontsize=10,
            frameon=True
        )

        ax.set_aspect("auto")
        ax.set_facecolor("#1c1c1c")
        fig.patch.set_facecolor("#1c1c1c")
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Erro ao gerar mapa estilizado: {e}")




def mapa_interativo_lisa(df, coluna_valor="MdaPotenciaFiscalizadaKw", distancia_km=300):
    st.subheader("🌐 Mapa Interativo - Clusters LISA com Folium")

    # 🎛️ Seleção de tiles
    tile_option = st.selectbox("🗺️ Estilo do Mapa:", [
        "OpenStreetMap", "CartoDB positron", "CartoDB dark_matter", "Stamen Terrain"
    ])

    try:
        # 🔁 Coordenadas
        df["NumCoordNEmpreendimento"] = df["NumCoordNEmpreendimento"].astype(str).str.replace(",", ".").astype(float)
        df["NumCoordEEmpreendimento"] = df["NumCoordEEmpreendimento"].astype(str).str.replace(",", ".").astype(float)
        df = df.dropna(subset=["NumCoordNEmpreendimento", "NumCoordEEmpreendimento"])
        df["geometry"] = df.apply(lambda row: Point(row["NumCoordEEmpreendimento"], row["NumCoordNEmpreendimento"]), axis=1)
        gdf = gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:4326")

        # 🧠 LISA
        threshold_degraus = distancia_km / 111
        coords = [(geom.x, geom.y) for geom in gdf.geometry]
        w = DistanceBand(coords, threshold=threshold_degraus, binary=True, silence_warnings=True)
        y = gdf[coluna_valor].fillna(0)
        lisa = Moran_Local(y, w)

        cluster_labels = np.full(len(gdf), "Não Significativo")
        sig = lisa.p_sim < 0.05
        HH = (sig) & (lisa.q == 1)
        LL = (sig) & (lisa.q == 3)
        LH = (sig) & (lisa.q == 2)
        HL = (sig) & (lisa.q == 4)

        cluster_labels[HH] = "Alta-Alta 🔥"
        cluster_labels[LL] = "Baixa-Baixa ❄️"
        cluster_labels[LH] = "Baixa-Alta"
        cluster_labels[HL] = "Alta-Baixa"
        gdf["Cluster"] = cluster_labels

        # 🎨 Cores
        cor_cluster = {
            "Alta-Alta 🔥": "red",
            "Baixa-Baixa ❄️": "blue",
            "Baixa-Alta": "orange",
            "Alta-Baixa": "green",
            "Não Significativo": "gray"
        }

        # 🗺️ Mapa base
        centro = [gdf.geometry.y.mean(), gdf.geometry.x.mean()]
        mapa = folium.Map(location=centro, zoom_start=5, tiles=tile_option)

        # 🧭 MiniMapa
        MiniMap(toggle_display=True).add_to(mapa)

        # 📐 Escala de medida
        mapa.add_child(MeasureControl(primary_length_unit='kilometers'))

        # 🗂️ FeatureGroups por cluster
        grupos = {}
        for cluster in gdf["Cluster"].unique():
            grupos[cluster] = folium.FeatureGroup(name=cluster, show=True)
            mapa.add_child(grupos[cluster])

        # 📍 Adicionar pontos aos grupos
        for _, row in gdf.iterrows():
            cor = cor_cluster[row["Cluster"]]
            folium.CircleMarker(
                location=[row.geometry.y, row.geometry.x],
                radius=6,
                popup=folium.Popup(f"""
                    <b>{row['NomEmpreendimento']}</b><br>
                    Cluster: {row['Cluster']}<br>
                    Potência: {row[coluna_valor]:,.2f} kW
                """, max_width=250),
                color=cor,
                fill=True,
                fill_opacity=0.85
            ).add_to(grupos[row["Cluster"]])

        # ✅ Camada de controle
        folium.LayerControl(collapsed=False).add_to(mapa)

        # 🔁 Fit bounds
        bounds = gdf.geometry.bounds
        sw = [bounds.miny.min(), bounds.minx.min()]
        ne = [bounds.maxy.max(), bounds.maxx.max()]
        mapa.fit_bounds([sw, ne])

        # Renderizar
        folium_static(mapa, width=1000, height=600)

    except Exception as e:
        st.error(f"Erro ao gerar o mapa interativo: {e}")
