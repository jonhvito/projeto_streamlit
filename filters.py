import streamlit as st
import pandas as pd

def inicializar_filtros():
    """Garante que os filtros estejam inicializados no session_state."""
    session_keys = ["inicio_ano", "inicio_mes", "fim_ano", "fim_mes", "origem_combustivel", "fonte_combustivel", "estados", "selecionar_todos"]
    for key in session_keys:
        if key not in st.session_state:
            st.session_state[key] = [] if key in ["origem_combustivel", "fonte_combustivel", "estados"] else None

def aplicar_filtros(df):
    """Aplica os filtros ao DataFrame com base em mês e ano."""
    # Extrair ano e mês de DatInicioVigencia
    df_ano = df["DatInicioVigencia"].dt.year
    df_mes = df["DatInicioVigencia"].dt.month

    # Valores do session_state
    inicio_ano = st.session_state.inicio_ano
    inicio_mes = st.session_state.inicio_mes
    fim_ano = st.session_state.fim_ano
    fim_mes = st.session_state.fim_mes

    # Converter para um número comparável (ano * 12 + mês)
    df_data_num = df_ano * 12 + df_mes
    inicio_data_num = inicio_ano * 12 + inicio_mes
    fim_data_num = fim_ano * 12 + fim_mes

    return df[
        (df_data_num >= inicio_data_num) &
        (df_data_num <= fim_data_num) &
        (df["DscOrigemCombustivel"].isin(st.session_state.origem_combustivel)) &
        (df["NomFonteCombustivel"].isin(st.session_state.fonte_combustivel)) &
        (df["SigUFPrincipal"].isin(st.session_state.estados))
    ]