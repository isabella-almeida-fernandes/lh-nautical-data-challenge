WITH RECURSIVE limites_datas AS (
        SELECT 
            MIN(DATE(created_at)) AS data_inicio,
            MAX(DATE(created_at)) AS data_fim
        FROM orders
        WHERE channel = 'pos'
    ),
    calendario AS (
        SELECT data_inicio AS data_referencia
        FROM limites_datas
        UNION ALL
        SELECT DATE(data_referencia, '+1 day')
        FROM calendario, limites_datas
        WHERE data_referencia < limites_datas.data_fim
    ),
    vendas_diarias_pos AS (
        SELECT 
            DATE(created_at) AS data_venda,
            SUM(CAST(total AS REAL)) AS total_diario
        FROM orders
        WHERE channel = 'pos'
        GROUP BY DATE(created_at)
    ),
    calendario_com_vendas AS (
        SELECT 
            c.data_referencia,
            strftime('%w', c.data_referencia) AS dia_num, -- 0=Domingo, 1=Segunda, etc.
            COALESCE(v.total_diario, 0.0) AS faturamento_dia
        FROM calendario c
        LEFT JOIN vendas_diarias_pos v ON c.data_referencia = v.data_venda
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
        COUNT(*) AS total_dias_periodo,
        ROUND(SUM(faturamento_dia), 2) AS faturamento_total,
        ROUND(AVG(faturamento_dia), 2) AS media_vendas_diaria
    FROM calendario_com_vendas
    GROUP BY dia_num
    ORDER BY media_vendas_diaria ASC;