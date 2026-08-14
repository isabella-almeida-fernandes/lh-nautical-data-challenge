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
