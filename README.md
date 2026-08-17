# ⚓ LH Nautical — Plataforma de Inteligência de Dados & Modelagem Preditiva

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Database](https://img.shields.io/badge/database-PostgreSQL%20%7C%20SQLite-darkblue.svg)](https://www.postgresql.org/)
[![Framework](https://img.shields.io/badge/frontend-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/status-concluído-brightgreen.svg)]()

> Solução analítica *end-to-end* desenvolvida para a **LH Nautical**, integrando ingestão de dados relacionais brutos, modelagem dimensional em SQL, previsão de demanda de estoques via séries temporais, motor de recomendação por similaridade vetorial e um Data App executivo interativo.

---

## 🧭 Visão Geral da Arquitetura

O projeto foi desenhado sobre uma arquitetura modular que transforma eventos transacionais brutos em alavancas de decisão e produtos de dados:

1. **Ingestão & Carga:** Extração e normalização dos dados relacionais brutos em CSV para o banco relacional auditado.
2. **Modelagem SQL & Diagnósticos:**
   - Segmentação de clientes fiéis por diversidade de categorias ($\ge 13$) e ticket médio.
   - Correção de viés estatístico de vendas em lojas físicas via Dimensão Calendário.
3. **Modelagem Preditiva & Inteligência:**
   - Previsão de demanda mensal para itens críticos sem vazamento de dados (*Data Leakage*).
   - Motor de recomendação item-item via filtragem colaborativa e similaridade de cosseno.
4. **Camada de Entrega Executiva:**
   - Data App interativo em Python com visualizações dinâmicas no Streamlit.
   - Relatório executivo em PDF com métricas e recomendações de negócio.

---

## 🛠️ Tecnologias & Bibliotecas

* **Linguagem:** Python 3.10+
* **Engenharia & Análise de Dados:** `pandas`, `numpy`, `sqlite3`
* **Machine Learning & Vetorização:** `scikit-learn` (Cosine Similarity)
* **Visualização & Data App:** `streamlit`, `plotly`
* **Banco de Dados & Dialeto:** SQLite / PostgreSQL (DDL & Queries)
* **Controle de Versão:** Git & GitHub

---

## 📁 Estrutura do Repositório

```text
├── data/
│   ├── raw/                 # Datasets transacionais brutos em CSV
│   └── lh_nautical.db       # Banco relacional auditado e normalizado
├── docs/
│   └── LH_Nautical_Relatorio_Executivo.pdf # Apresentação executiva em alta resolução
├── sql/
│   ├── schema.sql                   # DDL de criação das tabelas relacionais
│   ├── codigo_sql.sql               # Query de validação e métricas gerais (Q1.1)
│   ├── analise_fidelidade_sql.sql   # Query de identificação do grupo de elite (Q4.1)
│   └── analise_calendario_sql.sql   # Query de agregação por dia da semana (Q5)
├── src/
│   ├── analise_calendario.py      # Tratamento temporal via dimensão de datas (Q5)
│   ├── analise_fidelidade.py      # Script analítico de clientes fiéis (Q4)
│   ├── app_dashboard.py           # Aplicação interativa em Streamlit
│   ├── eda.py                     # Análise exploratória inicial
│   ├── load_data.py               # Pipeline de ingestão dos arquivos CSV
│   ├── previsao_demanda.py        # Modelo preditivo de demanda e MAE (Q6)
│   ├── schema_generator.py        # Utilitário de automação do schema
│   ├── sistema_recomendacao.py    # Motor de recomendação item-item (Q7)
│   └── test_sql.py                # Testes de integridade das consultas SQL
├── requirements.txt         # Dependências do ecossistema Python
├── RESPOSTAS.md             # Documento oficial com as respostas conceituais e queries SQL
└── README.md                # Documentação técnica e guia de execução
```

---

## 🚀 Como Executar o Projeto Localmente

### 1. Clonar o Repositório e Preparar o Ambiente

```bash
# Clone o repositório
git clone [https://github.com/isabella-almeida-fernandes/lh-nautical-data-challenge.git](https://github.com/isabella-almeida-fernandes/lh-nautical-data-challenge.git)
cd lh-nautical-data-challenge

# Crie e ative o ambiente virtual
python -m venv venv

# No Windows:
.\venv\Scripts\activate

# No Linux/macOS:
source venv/bin/activate

# Instale todas as dependências
pip install -r requirements.txt
```

### 2. Executar os Módulos Analíticos e Modelos

```bash
# 1. Análise de Clientes Fiéis e Mix de Categorias (Questão 4)
python src/analise_fidelidade.py

# 2. Análise Operacional e Dimensão Calendário (Questão 5)
python src/analise_calendario.py

# 3. Modelo Preditivo de Demanda (Questão 6)
python src/previsao_demanda.py

# 4. Sistema de Recomendação por Similaridade de Cosseno (Questão 7)
python src/sistema_recomendacao.py
```

### 3. Iniciar o Painel Executivo Interativo (Streamlit)

```bash
streamlit run src/app_dashboard.py
```
*O dashboard abrirá automaticamente no navegador no endereço* `http://localhost:8501`.

---

## 📊 Principais Módulos da Solução

- **Segmentação de Clientes Fiéis**: Identificação do grupo de clientes de alto valor com base na diversidade de categorias ($\ge 13$) e ticket médio ponderado. O diagnóstico destacou a categoria Hélices como o principal vetor de consumo deste grupo.
- **Otimização Operacional de Lojas Físicas**: Implementação de uma Dimensão de Calendário contínua para eliminar o viés de agregação estatística, imputando R$ 0,00 nos dias sem faturamento e revelando a real média de vendas diárias.
- **Previsão de Demanda & Gestão de Estoques**: Construção de um modelo baseline com Média Móvel de 3 Meses (Rolling Window) estritamente sem vazamento de dados (*Data Leakage*), avaliado através do MAE (*Mean Absolute Error*) para o 1º trimestre de 2026.
- **Motor de Recomendação por Filtragem Colaborativa**: Geração de matriz esparsa binária Usuário $\times$ Produto e cálculo vetorial de Similaridade de Cosseno para criação de vitrines inteligentes de *cross-selling*.

---

## 📑 Respostas Oficiais e Documentação de Apoio

Para conferir as consultas SQL completas, validações numéricas e as justificativas conceituais de cada questão do teste, consulte o arquivo `RESPOSTAS.md`.

Para visualizar a apresentação executiva e os insights voltados à tomada de decisão da diretoria, acesse o documento `docs/LH_Nautical_Relatorio_Executivo.pdf`.

---

## 👩‍💻 Autoria 

Desenvolvido por **Isabella Almeida Fernandes** como parte do Desafio Técnico de *Inteligência de Dados e Analytics*.
