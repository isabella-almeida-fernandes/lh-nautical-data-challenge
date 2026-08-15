import os
import sqlite3
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def recomendar_produtos(caminho_db, produto_referencia="Motor de Popa 1949"):
    # 1. Conectar ao banco local e extrair os pares (customer_id, product_id, product_name)
    conn = sqlite3.connect(caminho_db)
    
    query = """
    SELECT DISTINCT
        o.customer_id,
        p.id AS product_id,
        p.name AS product_name
    FROM orders o
    INNER JOIN order_items oi ON o.id = oi.order_id
    INNER JOIN product_variants pv ON oi.product_variant_id = pv.id
    INNER JOIN products p ON pv.product_id = p.id;
    """
    
    df_interacoes = pd.read_sql_query(query, conn)
    conn.close()

    print(f"Total de interações distintas carregadas: {len(df_interacoes)}")

    # 2. Criar a Matriz Usuário x Produto (Linhas: customer_id, Colunas: product_id)
    # Valor 1 se comprou pelo menos uma vez, 0 caso contrário
    df_interacoes['comprou'] = 1
    matriz_usuario_produto = df_interacoes.pivot_table(
        index='customer_id',
        columns='product_id',
        values='comprou',
        fill_value=0
    )

    print(f"Dimensões da Matriz Usuário x Produto: {matriz_usuario_produto.shape}")

    # 3. Transpor para obter a matriz Produto x Usuário e calcular Similaridade de Cosseno Produto x Produto
    matriz_produto_usuario = matriz_usuario_produto.T
    matriz_similaridade = cosine_similarity(matriz_produto_usuario)
    
    df_similaridade = pd.DataFrame(
        matriz_similaridade,
        index=matriz_produto_usuario.index,
        columns=matriz_produto_usuario.index
    )

    # 4. Mapear id do produto para o nome
    mapa_nomes = df_interacoes[['product_id', 'product_name']].drop_duplicates().set_index('product_id')['product_name'].to_dict()

    # 5. Localizar o ID do produto de referência
    id_referencia = None
    for p_id, nome in mapa_nomes.items():
        if produto_referencia.lower() in nome.lower():
            id_referencia = p_id
            nome_exato_ref = nome
            break

    if not id_referencia:
        print(f"Erro: Produto '{produto_referencia}' não encontrado no catálogo.")
        return

    print(f"\nProduto de Referência: {nome_exato_ref} (ID: {id_referencia})")

    # 6. Extrair e ordenar os produtos mais similares (excluindo ele mesmo)
    similaridades_item = df_similaridade[id_referencia].drop(index=id_referencia)
    top_5_similares = similaridades_item.sort_values(ascending=False).head(5)

    print("\n" + "="*70)
    print(f"RANKING: TOP 5 PRODUTOS MAIS SIMILARES A '{nome_exato_ref}'")
    print("="*70)
    
    for rank, (prod_id, score) in enumerate(top_5_similares.items(), start=1):
        nome_prod = mapa_nomes.get(prod_id, "Desconhecido")
        print(f"{rank}º Lugar: {nome_prod:<40} | Similaridade Cosseno: {score:.4f}")
        
    print("="*70 + "\n")

    produto_top_1 = mapa_nomes.get(top_5_similares.index[0])
    return produto_top_1

if __name__ == "__main__":
    caminho_db = os.path.join('data', 'lh_nautical.db')
    recomendar_produtos(caminho_db, "Motor de Popa 1949")