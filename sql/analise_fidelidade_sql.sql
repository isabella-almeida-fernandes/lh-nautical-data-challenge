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