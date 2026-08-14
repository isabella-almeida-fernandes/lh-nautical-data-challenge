import sqlite3
import os

def executar_analise_fidelidade(caminho_db):
    conn = sqlite3.connect(caminho_db)
    cursor = conn.cursor()

    # Query 1: Top 10 Clientes Fiéis (Questão 4.1)
    query_top_10 = """
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
    SELECT 
        customer_id,
        ticket_medio,
        faturamento_total,
        frequencia,
        diversidade_categorias
    FROM customer_metrics
    ORDER BY ticket_medio DESC, customer_id ASC
    LIMIT 10;
    """

    print("="*60)
    print("TOP 10 CLIENTES FIÉIS (QUESTÃO 4.1)")
    print("="*60)
    cursor.execute(query_top_10)
    top_10_rows = cursor.fetchall()
    
    for row in top_10_rows:
        print(f"Customer ID: {row[0]} | Ticket Médio: R$ {row[1]} | Fat. Total: R$ {row[2]} | Freq: {row[3]} | Cat. Distintas: {row[4]}")

    # Query 2: Categoria mais consumida por esses 10 clientes (Questão 4.2)
    query_top_categoria = """
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
        p.category_id,
        c.name AS nome_categoria,
        SUM(CAST(oi.quantity AS INTEGER)) AS total_itens_comprados
    FROM orders o
    INNER JOIN top_10_customers top ON o.customer_id = top.customer_id
    INNER JOIN order_items oi ON o.id = oi.order_id
    INNER JOIN product_variants pv ON oi.product_variant_id = pv.id
    INNER JOIN products p ON pv.product_id = p.id
    LEFT JOIN categories c ON p.category_id = c.id
    GROUP BY p.category_id, c.name
    ORDER BY total_itens_comprados DESC
    LIMIT 5;
    """

    print("\n" + "="*60)
    print("CATEGORIAS MAIS VENDIDAS PARA OS TOP 10 CLIENTES")
    print("="*60)
    cursor.execute(query_top_categoria)
    cat_rows = cursor.fetchall()
    
    for row in cat_rows:
        print(f"Categoria ID: {row[0]} | Nome: {row[1]} | Qtd Itens: {row[2]}")

    conn.close()

if __name__ == "__main__":
    caminho_db = os.path.join('data', 'lh_nautical.db')
    executar_analise_fidelidade(caminho_db)