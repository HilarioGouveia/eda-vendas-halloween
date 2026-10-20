# Processamento, Auditoria de Vendas e Dashboard - Festa em Cena

<div align="center">

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://eda-vendas-halloween.streamlit.app/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/pandas-2.0+-150458.svg?style=flat&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.30+-FF4B4B.svg?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Status](https://img.shields.io/badge/status-concluído-brightgreen.svg?style=flat)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub last commit](https://img.shields.io/github/last-commit/HilarioGouveia/eda-vendas-halloween?style=flat&logo=github)](https://github.com/HilarioGouveia/eda-vendas-halloween)
[![Dataset](https://img.shields.io/badge/dataset-1.500_linhas-orange?style=flat&logo=database)](#)

</div>

> 🔗 **Acesse o Dashboard Online:** [eda-vendas-halloween.streamlit.app](https://eda-vendas-halloween.streamlit.app/)

---

Este repositório contém a solução desenvolvida para higienização, auditoria de integridade cadastral e análise exploratória dos dados transacionais sazonais da Festa em Cena. O projeto conta com execução via terminal (CLI) e um dashboard interativo construído em Streamlit.

---

## 1. Estrutura do Projeto

A arquitetura do repositório foi desenhada de forma modular para desacoplar as regras de negócio e higienização das camadas de apresentação (linha de comando e interface web):

```text
festa-em-cena-vendas/
├── .gitignore               # Ignora ambientes virtuais, caches e arquivos temporários
├── requirements.txt         # Dependências do projeto (pandas, streamlit)
├── halloween_vendas.csv     # Base de dados original (1.500 registros)
├── funcoes.py               # Módulo central com regras de negócio, regex e validações
├── main.py                  # Ponto de entrada CLI (execução e relatório no terminal)
├── app.py                   # Dashboard interativo com Streamlit
├── README.md                # Documentação técnica e guia de execução
└── report.md                # Relatório executivo de insights

```

---

## 2. Descrição do Projeto

### Contexto e Problema de Negócio

A equipe operacional da **Festa em Cena** identificou inconsistências cadastrais em sua base de vendas de Halloween. Entre os problemas reportados estavam categorias não preenchidas, pontuações indevidas em textos, grafias divergentes nos canais de venda, quantidades numéricas inválidas, preços ausentes e registros de datas corrompidos. A gestão solicitou uma auditoria completa e estruturada antes de comparar períodos históricos de vendas.

### Objetivo do Programa

Desenvolver um conjunto modular de scripts em Python utilizando a biblioteca padrão (`re`, `datetime`, `typing`) em conjunto com `pandas` e `streamlit` para:

1. Validar e tratar valores ausentes e inconsistências numéricas sem imputação de dados artificiais.
2. Padronizar textos com expressões regulares.
3. Testar e validar hipóteses de regras de negócio (entrega vs. cancelamento).
4. Normalizar dados cronológicos no padrão brasileiro.
5. Disponibilizar os resultados tanto via terminal quanto por meio de um painel interativo.

### Significado das Linhas e Colunas do Dataset

* **Significado de uma Linha:** Cada linha representa uma **ordem/pedido registrado** nos sistemas da loja (uma intenção de compra cadastrada em determinado momento e canal), não correspondendo necessariamente a uma venda concluída ou item faturado.

* **Quatro Colunas Selecionadas:**

1. `pedido_id`: Identificador numérico único de cada registro.

2. `data_venda`: Registro cronológico no formato original `AAAA-MM-DD HH:MM:SS`.

3. `categoria`: Classificação do item (ex.: Fantasia, Acessório).

4. `canal_venda`: Ponto de contato onde a transação foi originada (Web, Loja física, Mercado).

*Observação sobre custos e descontos:* As colunas `custo_unitario` e `desconto_pct` constam na base, mas seu uso é opcional, tendo sido priorizada a auditoria de consistência cadastral e a contagem volumétrica de pedidos.

### Regras Adotadas para Tratamento

* **Campos de Texto:**
* `categoria`: Registros ausentes (`NaN`) foram preenchidos com o valor sentinela `"sem categoria"`. Em valores preenchidos, aplicou-se `.strip()`, `.lower()` e a remoção de pontuações via expressão regular (`re.sub(r'[^a-zA-Z\s]', '', texto)`).

* `canal_venda`: Mapeado e padronizado estritamente para `"Mercado"`, `"Loja física"` e `"Web"`.

* **Valores Numéricos:**
* `quantidade`: Validado como número inteiro estritamente maior que zero (`> 0`).

* `preco_unitario`: Validado como preenchido (não nulo) e não negativo (`>= 0`).

* *Justificativa:* Registros que violaram essas regras foram sinalizados através da flag booleana `problema_numerico`. Não houve substituição por médias ou zeros para não comprometer a fidedignidade contábil e a rastreabilidade da auditoria.

* **Datas:**
* Convertidas estritamente com `datetime.strptime(valor, "%Y-%m-%d %H:%M:%S")`, preservando a string original e extraindo ano, mês, dia e hora, além do formato brasileiro (`%d/%m/%Y`).

* *Justificativa:* Registros corrompidos foram sinalizados com `data_venda_invalida` sem substituição pela data de hoje, evitando distorcer as janelas sazonais de 2024 e 2025.

---

## 3. Ambiente Virtual e Instalação

### Pré-requisitos

* **Python 3.10** ou superior (compatível com 3.9, 3.10, 3.11 e 3.12).

### 1. Criar e Ativar o Ambiente Virtual

Recomenda-se o uso de um ambiente virtual isolado para a execução do projeto:

```bash
# No Linux/macOS:
python3 -m venv venv
source venv/bin/activate

# No Windows (Prompt de Comando ou PowerShell):
python -m venv venv
venv\Scripts\activate

```

### 2. Instalar as Dependências (`requirements.txt`)

Com o ambiente ativado, instale as bibliotecas necessárias:

```bash
pip install -r requirements.txt

```

O arquivo `requirements.txt` contém:

```text
pandas>=2.0.0
streamlit>=1.30.0

```

*(As bibliotecas `re`, `datetime`, `typing` e `sys` são nativas do Python e não exigem instalação externa).*

---

## 4. Guia de Execução

### Opção A: Executar o Relatório no Terminal (`main.py`)

Para rodar o pipeline completo de auditoria e exibir o relatório consolidado no console:

```bash
python main.py

```

### Opção B: Executar o Dashboard Interativo (`app.py`)

Para inicializar o painel interativo no navegador web:

```bash
streamlit run app.py

```

O Streamlit abrirá automaticamente a interface em `http://localhost:8501`, disponibilizando:

* KPIs de integridade em tempo real (total de pedidos, problemas numéricos e cancelamentos).

* Painel de auditoria da regra de negócio com inspeção direta dos contraexemplos.

* Gráficos de barras por canal e séries temporais de pedidos por ano-mês.

* Tabela interativa com filtros dinâmicos por status e filtro rápido para pedidos com inconsistência.

---

## 5. Resumo dos Resultados Obtidos (Base Integral)

* **Total de linhas lidas:** 1.500 registros.

* **Categorias vazias preenchidas:** 18 registros preenchidos como `"sem categoria"`.

* **Categorias com pontuação indevida corrigidas:** 55 registros ajustados via Regex (exclamações).

* **Problemas numéricos identificados:** 19 pedidos afetados (sem sobreposição):

* 7 pedidos com quantidade inválida (`-1`).

* 12 pedidos com preço unitário ausente (`NaN`).

* **Datas de venda inválidas:** 4 registros corrompidos com o texto `"data_invalida"`.

* **Total de pedidos cancelados:** 109 pedidos.

### Conclusão sobre Entrega sem Data

A gestão operava sob a premissa de que *todos os pedidos sem data de entrega estariam cancelados*.

* **Veredito:** **Hipótese FALSA**.

* **Evidência:** Dos 143 pedidos sem data de entrega, 109 estão cancelados, mas **34 pedidos possuem status "Concluído"** (por exemplo, os pedidos IDs `1170`, `990` e `740`). Assumir cancelamento nesses casos excluiria indevidamente vendas concluídas pendentes apenas de sincronização no rastreio logístico.

---

## 6. Descobertas Analíticas

### Descoberta 1: Por Canal de Venda

* **Evidência Numérica:** O canal **Web** liderou o volume com **666 pedidos (44,4%)**, seguido pela **Loja física** com **551 pedidos (36,7%)** e pelo **Mercado** com **283 pedidos (18,9%)**. 100% dos registros foram reconhecidos após a padronização (0 exclusões).

* **Interpretação:** O canal digital demonstra forte preferência do consumidor por conveniência e antecedência nas compras sazonais, enquanto a loja física mantém papel expressivo para aquisições de conveniência imediata.

* **Limitação:** Os números representam exclusivamente o volume de ordens registradas, não mensurando faturamento financeiro (GMV), ticket médio ou margem líquida. Trata-se de uma base amostral e fictícia de exercício, não devendo ser confundida com o comportamento do varejo nacional.

### Descoberta 2: Por Período Temporal (Ano-Mês)

* **Evidência Numérica:** O mês de **outubro** concentrou o ápice das vendas nos dois anos: **393 pedidos em outubro/2024** e **410 pedidos em outubro/2025**, somando **803 pedidos (53,7% da base)**. O comportamento apresenta curva acentuada: início tímido em agosto (77 e 62 pedidos), aquecimento em setembro (104 e 94 pedidos), pico em outubro e arrefecimento em novembro (174 e 182 pedidos).

* **Interpretação:** Confirma-se uma sazonalidade estrita e previsível ("tiro curto"), com expansão orgânica de 4,3% nas ordens registradas no mês de pico entre 2024 e 2025.

* **Limitação:** As contagens consideram ordens registradas independentemente do status final (incluindo 109 cancelamentos), excluíram 4 registros com data corrompida e não avaliam a eficiência da entrega antes da data do evento (31 de outubro).
