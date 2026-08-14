import csv
import os
import sqlite3

def carregar_dados(pasta_csv, caminho_db):
    """
    Carrega todos os arquivos CSV brutos para um banco de dados relacional (SQLite local),
    preservando os dados sem remoção de nulos ou tratamentos indevidos.
    """
    # Garante que a pasta 'data' existe
    os.makedirs(os.path.dirname(caminho_db), exist_ok=True)
    
    conn = sqlite3.connect(caminho_db)
    cursor = conn.cursor()
    
    arquivos_csv = sorted([f for f in os.listdir(pasta_csv) if f.endswith('.csv')])
    
    print(f"Iniciando a carga de {len(arquivos_csv)} tabelas...\n")
    
    for arquivo in arquivos_csv:
        nome_tabela = os.path.splitext(arquivo)[0]
        caminho_arquivo = os.path.join(pasta_csv, arquivo)
        
        with open(caminho_arquivo, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            try:
                header = next(reader)
            except StopIteration:
                continue  # Arquivo vazio
            
            # Recria a tabela
            cursor.execute(f'DROP TABLE IF EXISTS "{nome_tabela}";')
            cols_def = ", ".join([f'"{col}" TEXT' for col in header])
            cursor.execute(f'CREATE TABLE "{nome_tabela}" ({cols_def});')
            
            # Inserção em lote (bulk insert) para máxima performance
            placeholders = ", ".join(["?"] * len(header))
            query_insert = f'INSERT INTO "{nome_tabela}" VALUES ({placeholders})'
            cursor.executemany(query_insert, reader)
            
        print(f"✔ Tabela '{nome_tabela}' carregada com sucesso.")
        
    conn.commit()
    
    # Validação da Questão 3.2: Contagem de linhas das tabelas solicitadas
    tabelas_alvo = ['customers', 'orders', 'order_items', 'payments']
    total_linhas_acumulado = 0
    
    print("\n" + "="*50)
    print("VALIDAÇÃO DE LINHAS (QUESTÃO 3.2)")
    print("="*50)
    
    for tab in tabelas_alvo:
        cursor.execute(f'SELECT COUNT(*) FROM "{tab}";')
        qtd = cursor.fetchone()[0]
        total_linhas_acumulado += qtd
        print(f"- Linhas em '{tab}': {qtd}")
        
    print("-" * 50)
    print(f"TOTAL DE LINHAS SOMADAS: {total_linhas_acumulado}")
    print("="*50 + "\n")
    
    conn.close()
    return total_linhas_acumulado

if __name__ == "__main__":
    pasta_origem = os.path.join('lh_nautical_csv')
    caminho_banco = os.path.join('data', 'lh_nautical.db')
    carregar_dados(pasta_origem, caminho_banco)