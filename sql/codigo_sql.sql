SELECT 
    COUNT(*) AS total_linhas,
    MIN(created_at) AS data_minima,
    MAX(created_at) AS data_maxima,
    ROUND(MIN(total::numeric), 2) AS valor_minimo,
    ROUND(MAX(total::numeric), 2) AS valor_maximo,
    ROUND(AVG(total::numeric), 2) AS valor_medio
FROM orders;
