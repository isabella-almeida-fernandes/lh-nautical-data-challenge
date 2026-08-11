import csv
from datetime import datetime
import os

def analisar_tabela_orders(caminho_csv):
    """
    Realiza a Análise Exploratória de Dados (EDA) na tabela 'orders'.
    """
    if not os.path.exists(caminho_csv):
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_csv}")

    total_linhas = 0
    total_colunas = 0
    
    datas_created_at = []
    valores_total = []
    nulos_por_coluna = {}
    
    with open(caminho_csv, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)  # Primeira linha: cabeçalho
        total_colunas = len(header)
        
        # Mapeamento dos índices das colunas relevantes
        idx_created_at = header.index('created_at') if 'created_at' in header else None
        idx_total = header.index('total') if 'total' in header else None
        
        # Inicializa contador de nulos por coluna
        for col in header:
            nulos_por_coluna[col] = 0

        for row in reader:
            total_linhas += 1
            
            # 1. Contagem de valores nulos ou vazios por coluna
            for i, val in enumerate(row):
                if val is None or val.strip() == '':
                    col_name = header[i]
                    nulos_por_coluna[col_name] += 1
            
            # 2. Coleta de datas (created_at)
            if idx_created_at is not None:
                val_date = row[idx_created_at].strip()
                if val_date:
                    try:
                        # Trata formatos com ou sem horário Z/offset
                        cleaned_date = val_date.replace('Z', '').split('+')[0]
                        dt = datetime.fromisoformat(cleaned_date)
                        datas_created_at.append(dt)
                    except ValueError:
                        pass
            
            # 3. Coleta de valores numéricos (total)
            if idx_total is not None:
                val_total = row[idx_total].strip()
                if val_total:
                    try:
                        num = float(val_total)
                        valores_total.append(num)
                    except ValueError:
                        pass

    # Processamento dos resultados da Parte 1
    data_minima = min(datas_created_at) if datas_created_at else None
    data_maxima = max(datas_created_at) if datas_created_at else None

    # Processamento dos resultados da Parte 2
    valor_minimo = min(valores_total) if valores_total else None
    valor_maximo = max(valores_total) if valores_total else None
    valor_medio = sum(valores_total) / len(valores_total) if valores_total else 0.0

    return {
        "total_linhas": total_linhas,
        "total_colunas": total_colunas,
        "data_minima": data_minima,
        "data_maxima": data_maxima,
        "valor_minimo": valor_minimo,
        "valor_maximo": valor_maximo,
        "valor_medio": valor_medio,
        "nulos_por_coluna": nulos_por_coluna
    }

if __name__ == "__main__":
    # Garante a busca do arquivo de forma relativa a partir da raiz do projeto
    caminho_arquivo = os.path.join('lh_nautical_csv', 'orders.csv')
    res = analisar_tabela_orders(caminho_arquivo)
    
    print("="*45)
    print("PARTE 1 - VISÃO GERAL DA TABELA ORDERS")
    print("="*45)
    print(f"Quantidade total de linhas: {res['total_linhas']}")
    print(f"Quantidade total de colunas: {res['total_colunas']}")
    print(f"Data Mínima (created_at): {res['data_minima']}")
    print(f"Data Máxima (created_at): {res['data_maxima']}")
    
    print("\n" + "="*45)
    print("PARTE 2 - ANÁLISE DA COLUNA 'TOTAL'")
    print("="*45)
    print(f"Valor Mínimo: {res['valor_minimo']}")
    print(f"Valor Máximo: {res['valor_maximo']}")
    print(f"Valor Médio:  {res['valor_medio']:.2f}")
    
    print("\n" + "="*45)
    print("MÉTRICAS DE QUALIDADE (Nulos por Coluna)")
    print("="*45)
    for col, count in res['nulos_por_coluna'].items():
        print(f"- {col}: {count} valores nulos/vazios")