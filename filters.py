import streamlit as st

def inicializar_filtros():
    """Garante que os filtros estejam inicializados no session_state."""
    session_keys = ["data_inicio", "data_fim", "origem_combustivel", "fonte_combustivel", "estados", "selecionar_todos"]
    for key in session_keys:
        if key not in st.session_state:
            st.session_state[key] = [] if key in ["origem_combustivel", "fonte_combustivel", "estados"] else None

def aplicar_filtros(df):
    """Aplica os filtros ao DataFrame."""
    return df[
        (df["DatInicioVigencia"].dt.year >= st.session_state.data_inicio) &
        (df["DatInicioVigencia"].dt.year <= st.session_state.data_fim) &
        (df["DscOrigemCombustivel"].isin(st.session_state.origem_combustivel)) &
        (df["NomFonteCombustivel"].isin(st.session_state.fonte_combustivel)) &
        (df["SigUFPrincipal"].isin(st.session_state.estados))
    ]
