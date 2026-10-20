"""
app.py - Dashboard Interativo Streamlit para Festa em Cena
Com Sidebar de Auditoria e Filtros de Governança
"""

import pandas as pd
import streamlit as st
from funcoes import executar_pipeline_completo

st.set_page_config(
    page_title="Festa em Cena | Auditoria & Vendas",
    page_icon="🎃",
    layout="wide",
)


# --- CUSTOMIZAÇÃO VISUAL: REDUÇÃO DO TOPO E FONTE DO HEADER ---
st.markdown(
    """
    <style>
        /* Ajusta o espaçamento do topo para não ser cortado pela barra superior */
        .block-container {
            padding-top: 3.5rem !important;
            padding-bottom: 2rem !important;
        }

        /* Título Principal (Header) */
        h1 {
            font-size: 1.8rem !important;
            font-weight: 700 !important;
            margin-top: 0rem !important;
            margin-bottom: 0.25rem !important;
            padding-top: 0.2rem !important;
            line-height: 1.25 !important;
        }

        /* Título da Sidebar: tamanho reduzido para evitar quebra de linha indesejada */
        [data-testid="stSidebar"] h1 {
            font-size: 1.35rem !important;
            line-height: 1.2 !important;
            margin-bottom: 0.2rem !important;
        }

        /* Subtítulo logo abaixo do cabeçalho */
        .stMarkdown p {
            font-size: 0.95rem;
        }

        /* Valor dos KPIs ligeiramente mais compacto */
        [data-testid="stMetricValue"] {
            font-size: 1.75rem !important;
        }
    </style>
""",
    unsafe_allow_html=True,
)


@st.cache_data
def carregar_e_processar():
    return executar_pipeline_completo("halloween_vendas.csv")


try:
    df, metricas = carregar_e_processar()
except Exception as e:
    st.error(f"Erro ao carregar e processar a base de dados: {e}")
    st.stop()

# ==========================================
# SIDEBAR: AUDITORIA E GOVERNANÇA DE DADOS
# ==========================================
st.sidebar.title("🎃 Painel de Auditoria")
st.sidebar.caption("Validação de integridade e regras de negócio")

# 1. Seção: Validação da Regra de Negócio (Data de Entrega)
st.sidebar.subheader("🚚 Regra: Data de Entrega")
met_entrega = metricas["entrega"]

if not met_entrega["hipotese_confirmada"]:
    st.sidebar.warning(
        "**Hipótese Falsa:** Falta de data de entrega **não** significa cancelamento."
    )
    st.sidebar.write(
        f"• Sem entrega & Cancelados: **{met_entrega['sem_entrega_e_cancelados']}**"
    )
    st.sidebar.write(
        f"• Sem entrega & Concluídos: **{met_entrega['sem_entrega_outros_status']}**"
    )

    with st.sidebar.expander("Ver contraexemplos na base"):
        df_contra = pd.DataFrame(met_entrega["exemplos_contraexemplos"])
        st.dataframe(df_contra, hide_index=True)
else:
    st.sidebar.success("Hipótese confirmada na base.")

st.sidebar.markdown("---")

# 2. Seção: Filtros Globais para a Visualização
st.sidebar.subheader("⚙️ Filtros de Visualização")
filtro_status = st.sidebar.multiselect(
    "Filtrar por Status do Pedido:",
    options=sorted(df["status_pedido"].unique()),
    default=sorted(df["status_pedido"].unique()),
)

somente_problemas = st.sidebar.checkbox(
    "Exibir apenas registros com inconsistências",
    help="Filtra pedidos com problemas numéricos (qtd/preço) ou data inválida.",
)

# [RODAPÉ] Assinatura do desenvolvedor
st.sidebar.markdown("---")
st.sidebar.caption("Desenvolvido por **Hilário Gouveia**")
st.sidebar.markdown(
    "[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/hilário-gouveia-30a09b26b) "
    "[![GitHub](https://img.shields.io/badge/GitHub-100000?style=flat&logo=github&logoColor=white)](https://github.com/HilarioGouveia)"
)

# ==========================================
# PAINEL PRINCIPAL: KPIS E ANÁLISE EXPLORATÓRIA
# ==========================================
st.title("🎃 Festa em Cena - Inteligência e Auditoria de Vendas")
st.markdown(
    "Visão executiva da volumetria transacional e integridade cadastral da base."
)

# KPIs em Destaque
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Total de Pedidos", f"{metricas['total_linhas']:,}".replace(",", "."))
kpi2.metric(
    "Problemas Numéricos",
    metricas["ausentes"]["total_pedidos_com_problema_numerico"],
)
kpi3.metric(
    "Categorias Tratadas",
    metricas["ausentes"]["categorias_vazias_preenchidas"]
    + metricas["regex"]["categorias_com_pontuacao_alteradas"],
)
kpi4.metric("Total Cancelados", metricas["total_cancelados"])

st.markdown("---")

# Abas Analíticas
tab1, tab2, tab3 = st.tabs(
    ["📊 Pedidos por Canal", "📅 Evolução Temporal (Ano-Mês)", "📋 Base de Dados Auditada"]
)

# --- Aba 1: Análise por Canal ---
with tab1:
    st.subheader("Distribuição de Pedidos por Canal de Venda")
    df_canal = df[df["canal_venda_padrao"] != "Desconhecido"]
    contagem_canal = (
        df_canal["canal_venda_padrao"]
        .value_counts()
        .reset_index(name="Quantidade")
    )
    contagem_canal.columns = ["Canal", "Quantidade"]
    contagem_canal["Participação (%)"] = (
        contagem_canal["Quantidade"] / contagem_canal["Quantidade"].sum()
    ) * 100

    col_chart, col_tbl = st.columns([2, 1])
    with col_chart:
        st.bar_chart(data=contagem_canal.set_index("Canal")["Quantidade"])
    with col_tbl:
        st.dataframe(
            contagem_canal.style.format({"Participação (%)": "{:.1f}%"}),
            hide_index=True,
            width="stretch",
        )

# --- Aba 2: Análise Temporal ---
with tab2:
    st.subheader("Sazonalidade de Pedidos Registrados por Ano-Mês")
    df_tempo = df[~df["data_venda_invalida"]]
    contagem_tempo = (
        df_tempo["ano_mes"]
        .value_counts()
        .sort_index()
        .reset_index(name="Quantidade")
    )
    contagem_tempo.columns = ["Ano-Mês", "Quantidade"]

    st.line_chart(data=contagem_tempo.set_index("Ano-Mês"))
    st.info(
        f"ℹ️ Exclusões temporais: {metricas['tempo']['datas_invalidas_ou_vazias']} pedidos "
        "desconsiderados por apresentarem texto de data corrompido ('data_invalida')."
    )

# --- Aba 3: Tabela com Filtros ---
with tab3:
    st.subheader("Exploração da Base Filtrada")
    df_view = df[df["status_pedido"].isin(filtro_status)]

    if somente_problemas:
        df_view = df_view[
            df_view["problema_numerico"] | df_view["data_venda_invalida"]
        ]

    st.caption(f"Exibindo **{len(df_view)}** de **{len(df)}** registros.")

    colunas_exibicao = [
        "pedido_id",
        "data_venda_br",
        "produto",
        "categoria_limpa",
        "canal_venda_padrao",
        "quantidade",
        "preco_unitario",
        "status_pedido",
        "problema_numerico",
        "data_entrega",
    ]
    st.dataframe(df_view[colunas_exibicao], width="stretch")