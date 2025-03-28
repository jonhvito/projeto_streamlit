
# ⚡ Dashboard Interativo de Usinas de Geração de Energia

🔍 **Dashboard em Streamlit para análise de usinas de geração de energia no Brasil. Permite upload, filtragem e visualização de dados com gráficos, indicadores e mapas geoespaciais — incluindo análise espacial estatística.**

---

## 📌 Índice
- [🎯 Objetivo do Projeto](#-objetivo-do-projeto)
- [📁 Fonte de Dados](#-fonte-de-dados)
- [📦 Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [🚀 Como Configurar o Projeto](#-como-configurar-o-projeto)
- [📂 Estrutura do Projeto](#-estrutura-do-projeto)
- [💡 Funcionalidades](#-funcionalidades)
- [📊 Visualizações Disponíveis](#-visualizações-disponíveis)
- [🧭 Análise Espacial (Moran’s I e LISA)](#-análise-espacial-morans-i-e-lisa)
- [🛠️ Melhorias Futuras](#️-melhorias-futuras)
- [🤝 Contribuições](#-contribuições)
- [📞 Contato](#-contato)
- [📜 Licença](#-licença)

---

## 🎯 Objetivo do Projeto

Este projeto visa **facilitar a análise e o monitoramento de usinas de geração distribuída no Brasil**, oferecendo uma interface interativa e acessível para que gestores, pesquisadores e investidores possam:

- Visualizar dados com **gráficos e mapas georreferenciados**
- Realizar análises por período, estado e fonte energética
- Exportar os dados filtrados para uso externo
- Aplicar **análise espacial estatística avançada** (ESDA)

---

## 📁 Fonte de Dados

- 🔗 [SIGA - Sistema de Informações de Geração da ANEEL](https://dadosabertos.aneel.gov.br/dataset/siga-sistema-de-informacoes-de-geracao-da-aneel)
- 📄 Arquivo: `siga-empreendimentos-geracao.csv`
- 📅 Atualização: 01/03/2025

---

## 📦 Tecnologias Utilizadas

| Ferramenta | Função |
|------------|--------|
| Python 3.9 | Linguagem principal |
| Streamlit | Interface interativa |
| Pandas | Manipulação de dados |
| Altair / Matplotlib | Gráficos interativos e estáticos |
| Folium | Mapas interativos |
| GeoPandas, PySAL | Análise espacial |
| Seaborn | Estética visual refinada |
| Anaconda / PyCharm | Ambiente de desenvolvimento |

---

## 🚀 Como Configurar o Projeto

### Pré-requisitos
- Python 3.9+
- pip
- Git (opcional)

### Instalação

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
python -m venv venv
venv\Scripts\activate       # Windows
# ou
source venv/bin/activate   # Linux/Mac
pip install -r requirements.txt
streamlit run main.py
```

> 🔗 Acesse: [http://localhost:8501](http://localhost:8501)

---

## 📂 Estrutura do Projeto

```plaintext
.
├── main.py                  # Interface principal (Streamlit)
├── data_loader.py           # Carregamento e processamento dos dados
├── filters.py               # Filtros interativos (estado, fonte, período)
├── visualizations.py        # Gráficos e mapas
├── esda_analysis.py         # Cálculo de Moran’s I e LISA
├── file_manager.py          # Upload e gerenciamento de arquivos
├── requirements.txt         # Dependências do projeto
└── uploaded_files/          # Arquivos CSV enviados pelo usuário
```

---

## 💡 Funcionalidades

- 📥 Upload de múltiplos arquivos CSV (estrutura ANEEL)
- 🎛️ Filtros dinâmicos por:
  - Estado (UF)
  - Fonte e origem de combustível
  - Intervalo de datas (mês/ano)
- 📊 Indicadores rápidos: total de usinas, potência média
- 📈 Gráficos:
  - Temporal (linha)
  - Comparativo por estado (barra)
  - Evolução com média histórica
- 🗺️ Mapa interativo com pontos e heatmap
- 🧭 Análise espacial (Moran’s I e LISA)
- 📤 Exportação de dados filtrados

---

## 📊 Visualizações Disponíveis

| Tipo                   | Descrição |
|------------------------|----------|
| 📋 Tabela de Dados     | Resultado filtrado em tabela interativa |
| 📈 Gráfico de Linha    | Evolução da potência fiscalizada ao longo do tempo |
| 📊 Gráfico de Barras   | Distribuição de potência por estado |
| 📊 Barra com Média     | Potência por ano + média de anos anteriores |
| 🗺️ Mapa Geoespacial    | Localização das usinas |
| 🌐 Mapa LISA Interativo| Clusters espaciais com Folium (Alta-Alta, Baixa-Baixa etc.) |

---

## 🧭 Análise Espacial (Moran’s I e LISA)

Utilizamos técnicas da **Análise Exploratória de Dados Espaciais (ESDA)** para identificar **padrões de autocorrelação geográfica** na potência das usinas.

### 📐 Moran’s I (Global)

- Mede se valores semelhantes estão próximos no espaço
- `I > 0`: agrupamento | `I ≈ 0`: aleatório | `I < 0`: disperso
- Usado para detectar **tendência espacial geral**

### 🧠 LISA (Local Indicators of Spatial Association)

- Detecta clusters locais:
  - 🔴 Alta–Alta (hotspot)
  - 🔵 Baixa–Baixa (coldspot)
  - 🟢 Alta–Baixa (outlier)
  - 🟠 Baixa–Alta (outlier)
- Exibido em mapa interativo com camadas ativáveis

---

## 🛠️ Melhorias Futuras

- [ ] Autenticação de usuários
- [ ] Integração via API da ANEEL
- [ ] Exportação de relatórios PDF/Excel
- [ ] Previsão de geração (modelos preditivos)
- [ ] Agrupamento por município ou região

---

## 🤝 Contribuições

```bash
# Fork → Branch → Commit → Pull Request
git checkout -b feature/nova-funcionalidade
git commit -m "feat: adiciona análise espacial"
git push origin feature/nova-funcionalidade
```

---

## 📞 Contato

- ✉️ victorjoao8817@gmail.com  
- 🧑‍💻 GitHub: [@jonhvito](https://github.com/jonhvito)

---

## 📜 Licença

Distribuído sob a Licença MIT. Veja o arquivo [`LICENSE`](LICENSE) para mais informações.
