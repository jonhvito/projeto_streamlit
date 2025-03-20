import streamlit as st
import datetime
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

        # 📅 Seleção principal de intervalo de meses e anos (usando selectbox)
        st.sidebar.subheader("📅 Intervalo de Data de Início de Vigência (Mês e Ano)")
        ano_minimo = df["DatInicioVigencia"].dropna().dt.year.min() if "DatInicioVigencia" in df.columns else 2000
        ano_maximo = df["DatInicioVigencia"].dropna().dt.year.max() if "DatInicioVigencia" in df.columns else 2025
        anos_disponiveis = list(range(ano_minimo, ano_maximo + 1))
        meses = list(range(1, 13))  # 1 a 12 para os meses

        # Valores padrão (1970 a 2002, ajustado ao intervalo disponível)
        default_inicio_ano = st.session_state.get("inicio_ano", min(1970, ano_minimo)) if st.session_state.get("inicio_ano") else min(1970, ano_minimo)
        default_inicio_mes = st.session_state.get("inicio_mes", 1) if st.session_state.get("inicio_mes") else 1
        default_fim_ano = st.session_state.get("fim_ano", min(2002, ano_maximo)) if st.session_state.get("fim_ano") else min(2002, ano_maximo)
        default_fim_mes = st.session_state.get("fim_mes", 12) if st.session_state.get("fim_mes") else 12

        # Garantir que os valores padrão estejam dentro do intervalo disponível
        default_inicio_ano = max(ano_minimo, min(default_inicio_ano, ano_maximo))
        default_fim_ano = max(ano_minimo, min(default_fim_ano, ano_maximo))

        # Seleção de início
        st.sidebar.subheader("Início")
        inicio_ano = st.sidebar.selectbox("Ano de Início", anos_disponiveis, index=anos_disponiveis.index(default_inicio_ano), key="inicio_ano_select")
        inicio_mes = st.sidebar.selectbox("Mês de Início", meses, index=meses.index(default_inicio_mes), key="inicio_mes_select")

        # Seleção de fim
        st.sidebar.subheader("Fim")
        fim_ano = st.sidebar.selectbox("Ano de Fim", anos_disponiveis, index=anos_disponiveis.index(default_fim_ano), key="fim_ano_select")
        fim_mes = st.sidebar.selectbox("Mês de Fim", meses, index=meses.index(default_fim_mes), key="fim_mes_select")

        # Armazenar no session_state
        st.session_state.inicio_ano = inicio_ano
        st.session_state.inicio_mes = inicio_mes
        st.session_state.fim_ano = fim_ano
        st.session_state.fim_mes = fim_mes

        # 📅 Slider secundário sincronizado com os anos selecionados (1970 a 2002 como padrão)
        ano_inicio_slider, ano_fim_slider = st.sidebar.slider(
            "Ajuste fino com o slider (anos)",
            ano_minimo,
            ano_maximo,
            (inicio_ano, fim_ano),
            key="slider_secundario"
        )

        # Sincronizar os selectbox com o slider (atualiza apenas o ano)
        if ano_inicio_slider != inicio_ano or ano_fim_slider != fim_ano:
            st.session_state.inicio_ano = ano_inicio_slider
            st.session_state.fim_ano = ano_fim_slider

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
                df_exibicao = df_filtrado 
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