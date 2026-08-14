# Resoluções do Desafio Lighthouse - LH Nautical

## Questão 1 - EDA

### 1.1 - SQL (PostgreSQL)

Código calculando:
- **Quantidade total de linhas**
- **Intervalo de datas analisado (data mínima e máxima)**
- **Valor mínimo**
- **Valor máximo**
- **Valor médio**

```sql
SELECT 
    COUNT(*) AS total_linhas,
    MIN(created_at::timestamp) AS data_minima,
    MAX(created_at::timestamp) AS data_maxima,
    MIN(total) AS valor_minimo,
    MAX(total) AS valor_maximo,
    ROUND(AVG(total)::numeric, 2) AS valor_medio
FROM orders;
```

Visão Geral da Tabela `orders`
- **Quantidade total de linhas:** 48.998
- **Quantidade total de colunas:** 13
- **Intervalo de datas analisado (`created_at`):** 2020-01-01 01:19:28 até 2026-12-31 23:43:09

---

### 1.2 - Validação

- **Qual é o valor médio registrado na coluna `total`?**: R$ 28.704,99

Análise Numérica (`total`)
- **Valor Mínimo:** R$ 32,62
- **Valor Máximo:** R$ 127.262,02

---

### 1.3 - Interpretação 

Com base na análise exploratória realizada, escreva um breve diagnóstico sobre a confiabilidade da tabela `orders` para análises futuras. Comente sobre:

- **Possíveis outliers em "total"**  
- **Qualidade dos dados (valores nulos ou inconsistentes)**
- Se você considera que a tabela `orders` está pronta para análises ou se exigiria tratamento prévio ou relacionamento com demais tabelas

#### Diagnóstico de Confiabilidade

> A tabela `orders` em seu estado bruto atual não é recomendada para tomadas de decisão estratégicas. Identificou-se forte presença de outliers no ticket de vendas (máximo de R$ 127.262,02 frente a uma média de R$ 28.704,99) e incompletude cadastral (24.131 valores nulos em `salesperson_id`), exigindo sanitização prévia.

---

## Questão 2 - Schema

### Questão 2.1 - Script Python (Gerador de Schema)
O script `src/schema_generator.py` inspeciona dinamicamente os 24 arquivos CSV e gera as instruções DDL compatíveis com PostgreSQL sem utilizar bibliotecas externas.

---

### Questão 2.2 - Arquivo DDL (`schema.sql`)
Arquivo SQL gerado automaticamente contendo o mapeamento de criação de todas as 24 tabelas do banco de dados relacional. O arquivo está disponível na raiz deste repositório (`/schema.sql`).

---

## Questão 3 - Carga de Dados (Data Ingestion)

### Questão 3.1 - Script de Carga em Python
O script `src/load_data.py` realiza a ingestão em lote (*bulk insert*) de todos os 24 arquivos CSV brutos da pasta `lh_nautical_csv/` para um banco relacional local (`data/lh_nautical.db`), preservando a integridade original dos dados (sem expurgo de nulos ou tratamentos indevidos) e respeitando o schema definido.

---

### Questão 3.2 - Validação de Linhas Carregadas
Total acumulado de registros somando as tabelas essenciais (`customers`, `orders`, `order_items` e `payments`):

* **Total de Linhas Somadas:** `251864`

---

## Questão 4 - Análise de Clientes Fiéis e Segmentação

### Questão 4.1 - Consulta SQL dos Clientes Fiéis (PostgreSQL)

```sql
WITH customer_metrics AS (
    SELECT 
        o.customer_id,
        ROUND(SUM(o.total::numeric), 2) AS faturamento_total,
        COUNT(DISTINCT o.id) AS frequencia,
        ROUND(SUM(o.total::numeric) / COUNT(DISTINCT o.id), 2) AS ticket_medio,
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
ORDER BY 
    ticket_medio DESC, 
    customer_id ASC
LIMIT 10;
```

---

### Questão 4.2 - Diagnóstico e Explicação Metodológica

- **Cadeia de Chaves:** `orders.id` -> `order_items.order_id` -> `order_items.product_variant_id` -> `product_variants.id` -> `product_variants.product_id` -> `products.id` -> `products.category_id` -> `categories.id`.

- **Categoria Campeã:** A categoria que mais concentrou itens comprados entre os Top 10 clientes fiéis foi Hélices (ID 8), com 561 unidades adquiridas.

- **Filtro de Diversidade:** Implementado via cláusula `HAVING COUNT(DISTINCT p.category_id) >= 13`.

- **Isolamento dos Top 10:** Garantido através de subconsulta/CTE filtrando exclusivamente os 10 clientes de maior ticket médio ordenados decrescentemente com desempate por `customer_id ASC`.

---
