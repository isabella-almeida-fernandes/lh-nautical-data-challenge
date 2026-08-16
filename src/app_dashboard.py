import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Configuração da página
st.set_page_config(
    page_title="LH Nautical | Executive Dashboard",
    page_icon="⚓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Conexão com o banco local
@st.cache_data
def carregar_dados():
    caminho_db = os.path.join('data', 'lh_nautical.db')
    conn = sqlite3.connect(caminho_db)
    
    # 1. Dados Clientes Fiéis (Questão 4)
    q_top10 = """
    WITH customer_metrics AS (
        SELECT 
            o.customer_id,
            ROUND(SUM(CAST(o.total AS REAL)), 2) AS faturamento_total,
            COUNT(DISTINCT o.id) AS frequencia,
            ROUND(SUM(CAST(o.total AS REAL)) / COUNT(DISTINCT o.id), 2) AS ticket_medio,
            COUNT(DISTINCT p.category_id) AS diversidade_categorias
        FROM orders o
        INNER JOIN order_items oi ON o.id = oi.order_id
        INNER JOIN product_variants pv ON oi.product_variant_id = pv.id
        INNER JOIN products p ON pv.product_id = p.id
        GROUP BY o.customer_id
        HAVING COUNT(DISTINCT p.category_id) >= 13
    )
    SELECT * FROM customer_metrics ORDER BY ticket_medio DESC, customer_id ASC LIMIT 10;
    """
    df_top10 = pd.read_sql_query(q_top10, conn)

    # Categorias mais vendidas para o Top 10
    q_top_cat = """
    WITH top_10_customers AS (
        SELECT 
            o.customer_id,
            SUM(CAST(o.total AS REAL)) / COUNT(DISTINCT o.id) AS ticket_medio
        FROM orders o
        INNER JOIN order_items oi ON o.id = oi.order_id
        INNER JOIN product_variants pv ON oi.product_variant_id = pv.id
        INNER JOIN products p ON pv.product_id = p.id
        GROUP BY o.customer_id
        HAVING COUNT(DISTINCT p.category_id) >= 13
        ORDER BY ticket_medio DESC, o.customer_id ASC
        LIMIT 10
    )
    SELECT 
        c.name AS nome_categoria,
        SUM(CAST(oi.quantity AS INTEGER)) AS total_itens_comprados
    FROM orders o
    INNER JOIN top_10_customers top ON o.customer_id = top.customer_id
    INNER JOIN order_items oi ON o.id = oi.order_id
    INNER JOIN product_variants pv ON oi.product_variant_id = pv.id
    INNER JOIN products p ON pv.product_id = p.id
    LEFT JOIN categories c ON p.category_id = c.id
    GROUP BY c.name
    ORDER BY total_itens_comprados DESC
    LIMIT 8;
    """
    df_top_cat = pd.read_sql_query(q_top_cat, conn)

    # 2. Dados Dias da Semana com Dimensão Calendário (Questão 5)
    q_calendario = """
    WITH RECURSIVE limites_datas AS (
        SELECT MIN(DATE(created_at)) AS data_inicio, MAX(DATE(created_at)) AS data_fim
        FROM orders WHERE channel = 'pos'
    ),
    calendario AS (
        SELECT data_inicio AS data_referencia FROM limites_datas
        UNION ALL
        SELECT DATE(data_referencia, '+1 day') FROM calendario, limites_datas WHERE data_referencia < limites_datas.data_fim
    ),
    vendas_diarias AS (
        SELECT DATE(created_at) AS data_venda, SUM(CAST(total AS REAL)) AS total_diario
        FROM orders WHERE channel = 'pos' GROUP BY DATE(created_at)
    ),
    calendario_vendas AS (
        SELECT 
            c.data_referencia,
            strftime('%w', c.data_referencia) AS dia_num,
            COALESCE(v.total_diario, 0.0) AS faturamento_dia
        FROM calendario c
        LEFT JOIN vendas_diarias v ON c.data_referencia = v.data_venda
    )
    SELECT 
        CASE dia_num
            WHEN '0' THEN 'Domingo'
            WHEN '1' THEN 'Segunda-feira'
            WHEN '2' THEN 'Terça-feira'
            WHEN '3' THEN 'Quarta-feira'
            WHEN '4' THEN 'Quinta-feira'
            WHEN '5' THEN 'Sexta-feira'
            WHEN '6' THEN 'Sábado'
        END AS dia_semana,
        dia_num,
        COUNT(*) AS total_dias,
        SUM(faturamento_dia) AS faturamento_total,
        AVG(faturamento_dia) AS media_vendas_diaria
    FROM calendario_vendas
    GROUP BY dia_num
    ORDER BY media_vendas_diaria ASC;
    """
    df_dias = pd.read_sql_query(q_calendario, conn)

    # 3. Séries Temporais Bússola (Questão 6)
    q_bussola = """
    SELECT 
        strftime('%Y-%m', o.created_at) AS mes_ano,
        SUM(CAST(oi.quantity AS INTEGER)) AS quantidade_real
    FROM orders o
    INNER JOIN order_items oi ON o.id = oi.order_id
    INNER JOIN product_variants pv ON oi.product_variant_id = pv.id
    INNER JOIN products p ON pv.product_id = p.id
    WHERE p.name LIKE '%Bússola de Bordo 702%'
    GROUP BY strftime('%Y-%m', o.created_at)
    ORDER BY mes_ano ASC;
    """
    df_bussola = pd.read_sql_query(q_bussola, conn)
    
    conn.close()
    return df_top10, df_top_cat, df_dias, df_bussola

df_top10, df_top_cat, df_dias, df_bussola = carregar_dados()

# Header Executivo
st.title("⚓ LH Nautical — Painel Executivo de Decisão & Insights")
st.markdown("### Monitoramento Estratégico de Clientes Fiéis, Eficiência Operacional e Previsão de Demanda")
st.markdown("---")

# Sidebar Informativa
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=500&q=80", caption="LH Nautical Analytics")
    st.header("Filtros & Navegação")
    visao = st.radio("Selecione a Visão:", [
        "1. Segmentação & Clientes Fiéis",
        "2. Análise Operacional (Lojas Físicas)",
        "3. Previsão de Demanda & Estoque",
        "4. Sistema de Recomendação"
    ])
    st.markdown("---")
    st.markdown("**Status do Pipeline:** ✔ Dados brutos integrados (`251.864` registros)")

# VISÃO 1: Clientes Fiéis (Questão 4)
if visao == "1. Segmentação & Clientes Fiéis":
    st.subheader("🎯 Perfil de Consumo dos Clientes Fiéis (Diversidade ≥ 13 Categorias)")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Maior Ticket Médio", f"R$ {df_top10['ticket_medio'].max():,.2f}")
    col2.metric("Média de Categorias Navegadas", f"{df_top10['diversidade_categorias'].mean():.1f} categorias")
    col3.metric("Faturamento do Top 10", f"R$ {df_top10['faturamento_total'].sum():,.2f}")

    col_g1, col_g2 = st.columns([1.2, 1])

    with col_g1:
        fig_bar = px.bar(
            df_top10, 
            x="customer_id", 
            y="ticket_medio",
            text="ticket_medio",
            title="Top 10 Clientes por Ticket Médio",
            labels={"customer_id": "ID do Cliente", "ticket_medio": "Ticket Médio (R$)"},
            color="ticket_medio",
            color_continuous_scale="Viridis"
        )
        fig_bar.update_traces(texttemplate='R$ %{text:,.2f}', textposition='outside')
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_g2:
        fig_cat = px.pie(
            df_top_cat,
            names="nome_categoria",
            values="total_itens_comprados",
            title="Categorias Mais Vendidas para o Grupo de Elite",
            hole=0.45,
            color_discrete_sequence=px.colors.sequential.Tealgrn
        )
        st.plotly_chart(fig_cat, use_container_width=True)

# VISÃO 2: Dias da Semana (Questão 5)
elif visao == "2. Análise Operacional (Lojas Físicas)":
    st.subheader("🗓️ Média Real de Vendas por Dia da Semana (Correção com Dimensão Calendário)")
    st.info("A dimensão de datas incorporou todos os dias em que as lojas físicas estiveram abertas com faturamento R$ 0,00, eliminando o viés de agregação.")

    pior_dia = df_dias.iloc[0]
    melhor_dia = df_dias.iloc[-1]

    col1, col2 = st.columns(2)
    col1.error(f"⚠️ **Pior Desempenho:** {pior_dia['dia_semana']} — Média Diária: R$ {pior_dia['media_vendas_diaria']:,.2f}")
    col2.success(f"🚀 **Melhor Desempenho:** {melhor_dia['dia_semana']} — Média Diária: R$ {melhor_dia['media_vendas_diaria']:,.2f}")

    fig_dias = px.bar(
        df_dias,
        x="dia_semana",
        y="media_vendas_diaria",
        text="media_vendas_diaria",
        title="Média Real de Vendas Diárias por Dia da Semana (Lojas Físicas - POS)",
        labels={"dia_semana": "Dia da Semana", "media_vendas_diaria": "Média de Vendas (R$)"},
        color="media_vendas_diaria",
        color_continuous_scale="RdYlBu"
    )
    fig_dias.update_traces(texttemplate='R$ %{text:,.2f}', textposition='outside')
    st.plotly_chart(fig_dias, use_container_width=True)

# VISÃO 3: Previsão de Demanda (Questão 6)
elif visao == "3. Previsão de Demanda & Estoque":
    st.subheader("📈 Previsão de Demanda: Bússola de Bordo 702 (1º Tri 2026)")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Previsão Total (1º Tri 2026)", "293 unidades")
    col2.metric("Erro Médio Absoluto (MAE)", "29.22 un/mês")
    col3.metric("Mecanismo", "Média Móvel (3 meses)")

    # Simulação dos dados de previsão para o gráfico
    df_grafico = df_bussola.copy()
    # Adicionar previsões do 1T 2026
    df_grafico['Tipo'] = 'Histórico Real'
    
    # Criar DataFrame com as previsões
    df_prev = pd.DataFrame([
        {'mes_ano': '2026-01', 'quantidade_real': 92.00, 'Tipo': 'Previsão (Baseline 3M)'},
        {'mes_ano': '2026-02', 'quantidade_real': 99.00, 'Tipo': 'Previsão (Baseline 3M)'},
        {'mes_ano': '2026-03', 'quantidade_real': 101.67, 'Tipo': 'Previsão (Baseline 3M)'}
    ])
    
    fig_ts = go.Figure()
    fig_ts.add_trace(go.Scatter(
        x=df_bussola['mes_ano'], 
        y=df_bussola['quantidade_real'], 
        mode='lines+markers', 
        name='Demanda Real',
        line=dict(color='#1f77b4', width=3)
    ))
    fig_ts.add_trace(go.Scatter(
        x=df_prev['mes_ano'], 
        y=df_prev['quantidade_real'], 
        mode='lines+markers', 
        name='Previsão Baseline',
        line=dict(color='#ff7f0e', dash='dash', width=3)
    ))
    
    fig_ts.update_layout(
        title="Evolução Mensal de Vendas e Projeção Preditiva",
        xaxis_title="Mês",
        yaxis_title="Quantidade Vendida (Unidades)",
        hovermode="x unified"
    )
    st.plotly_chart(fig_ts, use_container_width=True)

# VISÃO 4: Recomendação (Questão 7)
elif visao == "4. Sistema de Recomendação":
    st.subheader("🤝 Sistema de Cross-Selling por Similaridade de Cosseno")
    st.markdown("Recomendações geradas com base no item de referência **Motor de Popa 1949**.")

    df_recs = pd.DataFrame([
        {"Produto": "Motor de Popa 5331", "Similaridade Cosseno": 0.2566, "Posição": "1º Recomendação"},
        {"Produto": "Cabo Náutico 2105", "Similaridade Cosseno": 0.2562, "Posição": "2º Recomendação"},
        {"Produto": "Vela Mestra 1913", "Similaridade Cosseno": 0.2558, "Posição": "3º Recomendação"},
        {"Produto": "Cabo Náutico 9048", "Similaridade Cosseno": 0.2393, "Posição": "4º Recomendação"},
        {"Produto": "GPS Plotter 6249", "Similaridade Cosseno": 0.2377, "Posição": "5º Recomendação"}
    ])

    fig_rec = px.bar(
        df_recs,
        x="Similaridade Cosseno",
        y="Produto",
        orientation="h",
        text="Similaridade Cosseno",
        title="Top 5 Produtos Recomendados para Compradores do 'Motor de Popa 1949'",
        color="Similaridade Cosseno",
        color_continuous_scale="Blues"
    )
    fig_rec.update_layout(yaxis=dict(autorange="reversed"))
    fig_rec.update_traces(texttemplate='%{text:.4f}', textposition='outside')
    st.plotly_chart(fig_rec, use_container_width=True)