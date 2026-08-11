import sqlite3
import csv
import os

def testar_query_sql():
    # 1. Conecta a um banco de dados temporário na memória RAM
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    # 2. Localiza o CSV de orders
    csv_path = os.path.join('lh_nautical_csv', 'orders.csv')

    if not os.path.exists(csv_path):
        print(f"Erro: Arquivo não encontrado em {csv_path}")
        return

    # 3. Lê o CSV e cria a tabela automaticamente no banco SQL
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        
        # Cria a definição de colunas para o SQL
        cols_def = ", ".join([f'"{col}" TEXT' for col in header])
        cursor.execute(f"CREATE TABLE orders ({cols_def});")
        
        # Insere todas as linhas na tabela temporária
        placeholders = ", ".join(["?"] * len(header))
        cursor.executemany(f"INSERT INTO orders VALUES ({placeholders})", reader)

    conn.commit()

    # 4. A Consulta SQL da Questão 1.1
    query = """
    SELECT 
        COUNT(*) AS total_linhas,
        MIN(created_at) AS data_minima,
        MAX(created_at) AS data_maxima,
        MIN(CAST(total AS REAL)) AS valor_minimo,
        MAX(CAST(total AS REAL)) AS valor_maximo,
        ROUND(AVG(CAST(total AS REAL)), 2) AS valor_medio
    FROM orders;
    """

    # 5. Executa e exibe o resultado
    cursor.execute(query)
    resultado = cursor.fetchone()

    print("\n" + "="*45)
    print("RESULTADO DA CONSULTA SQL (QUESTÃO 1.1)")
    print("="*45)
    print(f"Total Linhas:  {resultado[0]}")
    print(f"Data Mínima:   {resultado[1]}")
    print(f"Data Máxima:   {resultado[2]}")
    print(f"Valor Mínimo:  R$ {resultado[3]}")
    print(f"Valor Máximo:  R$ {resultado[4]}")
    print(f"Valor Médio:   R$ {resultado[5]}")
    print("="*45 + "\n")

    conn.close()

if __name__ == "__main__":
    testar_query_sql()