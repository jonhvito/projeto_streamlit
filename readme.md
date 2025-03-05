
# 📊 Dashboard Interativo de Usinas de Geração de Energia

🔍 **Um dashboard interativo em Streamlit para análise de usinas de geração de energia no Brasil, permitindo upload, filtragem e visualização de dados com gráficos e mapas geoespaciais.**

---

## 📌 Índice
- [🎯 Objetivo do Projeto](#-objetivo-do-projeto)
- [📁 Fonte de Dados](#-fonte-de-dados)  <!-- NOVA SEÇÃO -->
- [📦 Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [🚀 Como Configurar o Projeto](#-como-configurar-o-projeto)
- [📂 Estrutura do Projeto](#-estrutura-do-projeto)
- [💡 Funcionalidades](#-funcionalidades)
- [📊 Visualizações Disponíveis](#-visualizações-disponíveis)
- [🛠️ Melhorias Futuras](#️-melhorias-futuras)
- [🤝 Contribuições](#-contribuições)
- [📞 Contato](#-contato)
- [📜 Licença](#-licença)

---

## 🎯 Objetivo do Projeto
Este projeto tem como objetivo **facilitar a análise de dados de usinas de geração de energia no Brasil**, oferecendo uma interface interativa para **gestores, investidores e pesquisadores** explorarem tendências e métricas de produção energética.

✅ **Principais Benefícios:**
- Visualização de dados em **gráficos dinâmicos e mapas geoespaciais**.
- Filtragem avançada por estado, tipo de combustível e período.
- Exportação de dados filtrados em CSV.
- Interface intuitiva e acessível para usuários não técnicos.

---

## 📁 Fonte de Dados  <!-- NOVA SEÇÃO -->
Os dados utilizados nesta análise são públicos e foram obtidos do portal de dados abertos da **ANEEL (Agência Nacional de Energia Elétrica)**.  
🔗 **Dataset utilizado**: [SIGA - Sistema de Informações de Geração da ANEEL](https://dadosabertos.aneel.gov.br/dataset/siga-sistema-de-informacoes-de-geracao-da-aneel)  
📄 **Arquivo**: `siga-empreendimentos-geracao.csv` *(dados atualizados até 01/03/2025)*  

---

## 📦 Tecnologias Utilizadas
| **Tecnologia**       | **Função**                                                                 |
|-----------------------|----------------------------------------------------------------------------|
| Python 3.9           | Linguagem principal do projeto                                            |
| Streamlit            | Framework para construção da interface web                                |
| Pandas               | Manipulação e limpeza de dados                                            |
| Altair & Matplotlib  | Geração de gráficos interativos e estáticos                               |
| Folium               | Criação de mapas geoespaciais                                             |
| PyCharm              | Ambiente de desenvolvimento integrado (IDE)                               |

---

## 🚀 Como Configurar o Projeto

### Pré-requisitos
- Python 3.9+
- Gerenciador de pacotes `pip`
- Git (opcional)

### Passo a Passo
1. **Clonar o repositório**:
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```

2. **Criar ambiente virtual (recomendado)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate    # Windows
   ```

3. **Instalar dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Executar a aplicação**:
   ```bash
   streamlit run main.py
   ```
   Acesse no navegador: [http://localhost:8501](http://localhost:8501).

---

## 📂 Estrutura do Projeto
```plaintext
.
├── main.py                  # Ponto de entrada da aplicação
├── requirements.txt         # Lista de dependências
├── README.md                # Documentação do projeto
├── data_loader.py           # Carrega e processa dados de CSV
├── filters.py               # Lógica de filtros (estado, combustível, data)
├── visualizations.py        # Gera gráficos e mapas
├── file_manager.py          # Gerencia uploads de arquivos
└── uploaded_files/          # Armazena arquivos enviados pelo usuário
```

---

## 💡 Funcionalidades
- **Upload de Dados**: Suporte a arquivos CSV com dados de usinas *(formato compatível com `siga-empreendimentos-geracao.csv`)*.
- **Filtros Dinâmicos**:
  - Seleção por estado, tipo de combustível e período.
  - Atualização automática das visualizações.
- **Visualizações**:
  - Tabelas interativas com dados filtrados.
  - Gráficos de linha (evolução temporal) e barras (comparação por estado).
  - Mapa de calor geoespacial das usinas.
- **Exportação**: Download dos dados filtrados em CSV.

---

## 📊 Visualizações Disponíveis
| **Tipo**               | **Descrição**                                                                 |
|------------------------|-------------------------------------------------------------------------------|
| 📋 Tabela de Dados     | Exibe dados brutos após aplicação dos filtros.                                |
| 📈 Gráfico de Linha    | Mostra a evolução da potência fiscalizada ao longo do tempo.                  |
| 📊 Gráfico de Barras   | Compara a potência total entre estados.                                       |
| 🗺️ Mapa Interativo    | Exibe a localização geográfica das usinas com marcadores e heatmap.           |

---

## 🛠️ Melhorias Futuras
- [ ] Adicionar autenticação de usuário.
- [ ] Integrar dados em tempo real via API da ANEEL.  <!-- REFERÊNCIA À FONTE -->
- [ ] Implementar análise preditiva (ex: previsão de produção).
- [ ] Suporte a outros formatos de arquivo (Excel, JSON).

---

## 🤝 Contribuições
1. **Faça um fork do projeto**.
2. **Crie uma branch**:
   ```bash
   git checkout -b feature/nome-da-sua-feature
   ```
3. **Faça commit das mudanças**:
   ```bash
   git commit -m "feat: adiciona nova funcionalidade"
   ```
4. **Envie para o repositório**:
   ```bash
   git push origin feature/nome-da-sua-feature
   ```
5. **Abra um Pull Request** e descreva suas alterações.

---

## 📞 Contato
- **Email**: [victorjoao8817@gmail.com](mailto:victorjoao8817@gmail.com)
- **GitHub**: [@jonhvito](https://github.com/jonhvito)
<!-- - **LinkedIn**: [Seu Nome](https://linkedin.com/in/seu-perfil)-->

---

## 📜 Licença
Este projeto está licenciado sob a [Licença MIT](LICENSE).
