import streamlit as st
from data_loader import carregar_dados
from filters import inicializar_filtros, aplicar_filtros
from visualizations import exibir_indicadores, grafico_temporal, grafico_barras, mapa_usinas
from file_manager import listar_arquivos, salvar_arquivo
    
# 🔄 Inicializar filtros no Streamlit
inicializar_filtros()

st.set_page_config(page_title="Dashboard de Usinas", layout="wide")

# 📥 Upload de arquivos CSV
uploaded_files = st.file_uploader("Escolha arquivos CSV", type=["csv"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        salvar_arquivo(uploaded_file)
    st.rerun()

# 📂 Listar arquivos disponíveis
arquivos_disponiveis = listar_arquivos()
arquivos_selecionados = st.multiselect("📂 Selecione os arquivos para análise:", arquivos_disponiveis)

# 📂 Criar Sidebar para os Filtros
st.sidebar.title("⚙️ Filtros")


# 📊 Se houver arquivos selecionados, carregar os dados
if arquivos_selecionados:
    df = carregar_dados(arquivos_selecionados)

    # 🚨 Verificar se o DataFrame está vazio ou tem colunas ausentes
    if df.empty:
        st.error("❌ O arquivo carregado não contém dados válidos. Verifique o delimitador ou a estrutura do CSV.")
        st.write("📌 **Colunas detectadas no arquivo:**", df.columns.tolist())
    else:
        # 🔍 Filtros dinâmicos (verifica se as colunas existem antes de usá-las)
        opcoes_origem = df["DscOrigemCombustivel"].dropna().unique().tolist() if "DscOrigemCombustivel" in df.columns else []
        opcoes_fonte_combustivel = df["NomFonteCombustivel"].dropna().unique().tolist() if "NomFonteCombustivel" in df.columns else []
        opcoes_estados = df["SigUFPrincipal"].dropna().unique().tolist() if "SigUFPrincipal" in df.columns else []

        # 🔍 Pré-seleção de "Biomassa" e "Bagaço de Cana" sem duplicação
        valores_padrao_origem = ["Biomassa"] if "Biomassa" in opcoes_origem else []
        valores_padrao_fonte = ["Bagaço de Cana de Açúcar"] if "Bagaço de Cana de Açúcar" in opcoes_fonte_combustivel else []

        if not st.session_state.origem_combustivel:
            st.session_state.origem_combustivel = valores_padrao_origem

        if not st.session_state.fonte_combustivel:
            st.session_state.fonte_combustivel = valores_padrao_fonte

        # 📅 Intervalo de Datas na Sidebar
        st.session_state.data_inicio, st.session_state.data_fim = st.sidebar.slider(
            "📅 Intervalo de Data de Início de Vigência",
            int(df["DatInicioVigencia"].dropna().dt.year.min()) if "DatInicioVigencia" in df.columns else 2000,
            int(df["DatInicioVigencia"].dropna().dt.year.max()) if "DatInicioVigencia" in df.columns else 2025,
            (st.session_state.data_inicio or 1970, st.session_state.data_fim or 2002)
        )

        # 🌱 Origem do Combustível na Sidebar
        st.session_state.origem_combustivel = st.sidebar.multiselect("🌱 Origem do Combustível", opcoes_origem,
                                                                     default=st.session_state.origem_combustivel)

        # 🔥 Fonte do Combustível na Sidebar
        st.session_state.fonte_combustivel = st.sidebar.multiselect("🔥 Fonte do Combustível", opcoes_fonte_combustivel,
                                                                    default=st.session_state.fonte_combustivel)

        # 🗺️ Estados na Sidebar
        selecionar_todos = st.sidebar.checkbox("Selecionar Todos os Estados", value=True)
        if selecionar_todos:
            st.session_state.estados = opcoes_estados
        else:
            st.session_state.estados = st.sidebar.multiselect("🗺️ Estados", opcoes_estados, default=st.session_state.estados)

        # 📌 Aplicar filtros
        df_filtrado = aplicar_filtros(df)

        # 📌 Definir colunas de interesse
        colunas_interesse = [
            "NomEmpreendimento", "SigUFPrincipal", "DscFaseUsina", "DscTipoOutorga", "DscPropriRegimePariticipacao",
            "MdaPotenciaFiscalizadaKw", "TipoGeracaoDistribuida", "DatInicioVigencia", "DatFimVigencia",
            "NumCoordNEmpreendimento", "NumCoordEEmpreendimento"
        ]

        # 📌 Verificar se todas as colunas de interesse existem no DataFrame
        colunas_existentes = [col for col in colunas_interesse if col in df_filtrado.columns]
        df_filtrado = df_filtrado[colunas_existentes]  # Filtrar apenas as colunas que existem

        # 📌 Ordenar os dados pela data de início de vigência
        if "DatInicioVigencia" in df_filtrado.columns:
            df_filtrado = df_filtrado.sort_values(by=["DatInicioVigencia"])

            # Criar abas para organizar as visualizações
            aba_tabela, aba_graficos, aba_mapa = st.tabs(["📋 Tabela de Dados", "📊 Gráficos", "🗺️ Mapa Geoespacial"])

            with aba_tabela:
                st.subheader("📌 Dados Filtrados")

                # Criar uma cópia do DataFrame com as colunas de coordenadas
                df_exibicao = df_filtrado 

                # Criar uma cópia do DataFrame com as colunas de coordenadas
                #df_exibicao = df_filtrado.drop(columns=["NumCoordNEmpreendimento", "NumCoordEEmpreendimento"],
                  #                             errors="ignore")

                st.dataframe(df_exibicao)

            with aba_graficos:
                if not df_filtrado.empty:
                    exibir_indicadores(df_filtrado)
                    grafico_temporal(df_filtrado)
                    grafico_barras(df_filtrado)

            with aba_mapa:
                if not df_filtrado.empty:
                    tipo_mapa = st.radio("📍 Selecione o tipo de mapa:", ["Mapa Normal", "Mapa de Calor"])
                    mapa_usinas(df_filtrado, tipo_mapa)

            # 📤 Exportar dados filtrados
            st.download_button("📥 Baixar CSV", df_filtrado.to_csv(index=False), "dados_filtrados.csv", "text/csv")
        else:
            st.warning("⚠️ Nenhum dado encontrado com os filtros selecionados. Tente ajustar os filtros para visualizar informações.")
else:
    st.info("🚀 Faça o upload e selecione os arquivos para análise.")
