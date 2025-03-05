import os

UPLOAD_DIR = "uploaded_files"

def listar_arquivos():
    """Lista os arquivos CSV disponíveis para análise."""
    return [f for f in os.listdir(UPLOAD_DIR) if f.endswith(".csv")]

def salvar_arquivo(uploaded_file):
    """Salva um arquivo enviado pelo usuário."""
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
