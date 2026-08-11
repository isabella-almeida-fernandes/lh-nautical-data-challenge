# Resoluções do Desafio Lighthouse - LH Nautical

## Questão 1 - EDA

### Parte 1 - Visão Geral da Tabela `orders`
- **Quantidade total de linhas:** 48.998
- **Quantidade total de colunas:** 13
- **Intervalo de datas analisado (`created_at`):** 2020-01-01 01:19:28 até 2026-12-31 23:43:09

### Parte 2 - Análise Numérica (`total`)
- **Valor Mínimo:** R$ 32,62
- **Valor Máximo:** R$ 127.262,02
- **Valor Médio:** R$ 28.704,99

### Parte 3 - Diagnóstico de Confiabilidade
> A tabela `orders` em seu estado bruto atual não é recomendada para tomadas de decisão estratégicas. Identificou-se forte presença de outliers no ticket de vendas (máximo de R$ 127.262,02 frente a uma média de R$ 28.704,99) e incompletude cadastral (24.131 valores nulos em `salesperson_id`), exigindo sanitização prévia.

---

## Questão 1.1 - SQL (PostgreSQL)

```sql
SELECT 
    COUNT(*) AS total_linhas,
    MIN(created_at::timestamp) AS data_minima,
    MAX(created_at::timestamp) AS data_maxima,
    MIN(total) AS valor_minimo,
    MAX(total) AS valor_maximo,
    ROUND(AVG(total)::numeric, 2) AS valor_medio
FROM orders;
