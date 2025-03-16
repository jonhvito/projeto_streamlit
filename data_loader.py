import pandas as pd
import os
import csv


def detectar_delimitador(file_path):
    """Detecta automaticamente o delimitador do arquivo CSV."""
    with open(file_path, 'r', encoding="latin1") as f:
        sniffer = csv.Sniffer()
        first_line = f.readline()
        return ";" if ";" in first_line else ","


def carregar_dados(file_paths):
    """Carrega e processa os arquivos CSV selecionados."""
    df_list = []
    for file_path in file_paths:
        delimitador = detectar_delimitador(os.path.join("uploaded_files", file_path))
        df = pd.read_csv(os.path.join("uploaded_files", file_path), delimiter=delimitador, encoding="latin1",
                         low_memory=False)

        # Conversão de tipos
        df["DatInicioVigencia"] = pd.to_datetime(df["DatInicioVigencia"], errors="coerce")
        df["DatFimVigencia"] = pd.to_datetime(df["DatFimVigencia"], errors="coerce")
        df["MdaPotenciaFiscalizadaKw"] = pd.to_numeric(df["MdaPotenciaFiscalizadaKw"], errors='coerce')

        # Classificação das usinas
        def classificar_geracao(potencia_kw):
            if potencia_kw <= 75:
                return "Microgeração"
            elif 75 < potencia_kw <= 5000:
                return "Minigeração"
            else:
                return "Geração"

        df["TipoGeracaoDistribuida"] = df["MdaPotenciaFiscalizadaKw"].apply(classificar_geracao)
        df_list.append(df)

    return pd.concat(df_list, ignore_index=True)
