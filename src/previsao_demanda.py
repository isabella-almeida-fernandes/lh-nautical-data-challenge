import sqlite3
import os

def prever_demanda_bussola(caminho_db):
    conn = sqlite3.connect(caminho_db)
    cursor = conn.cursor()

    # 1. Agregação mensal de vendas para 'Bússola de Bordo 702'
    query = """
    SELECT 
        strftime('%Y-%m', o.created_at) AS mes_ano,
        SUM(CAST(oi.quantity AS INTEGER)) AS quantidade_real
    FROM orders o
    INNER JOIN order_items oi ON o.id = oi.order_id
    INNER JOIN product_variants pv ON oi.product_variant_id = pv.id
    INNER JOIN products p ON pv.product_id = p.id
    WHERE p.name LIKE '%Bússola de Bordo 702%'
    GROUP BY strftime('%Y-%m', o.created_at)
    ORDER BY mes_ano ASC;
    """

    cursor.execute(query)
    historico = cursor.fetchall()
    conn.close()

    if not historico:
        print("Erro: Nenhum registro encontrado para o produto 'Bússola de Bordo 702'.")
        return

    # Dicionário mapeando mes_ano -> quantidade_real
    vendas_por_mes = {row[0]: row[1] for row in historico}
    meses_ordenados = sorted(list(vendas_por_mes.keys()))

    print("="*60)
    print("HISTÓRICO RECENTE DE VENDAS MENSAIS (Bússola de Bordo 702)")
    print("="*60)
    for mes in meses_ordenados[-8:]:
        print(f"Mês: {mes} | Quantidade Vendida: {vendas_por_mes[mes]}")

    # Meses do teste: Primeiro Trimestre de 2026
    meses_teste = ['2026-01', '2026-02', '2026-03']
    
    previsoes = {}
    erros_absolutos = []
    
    # Previsão rolling/passo a passo para cada mês do teste
    # Garantindo ausência de data leakage usando estritamente os 3 meses anteriores
    for mes_alvo in meses_teste:
        idx = meses_ordenados.index(mes_alvo)
        ultimos_3_meses = meses_ordenados[idx-3:idx]
        valores_ultimos_3 = [vendas_por_mes[m] for m in ultimos_3_meses]
        
        media_movel = sum(valores_ultimos_3) / len(valores_ultimos_3)
        previsoes[mes_alvo] = media_movel
        
        real = vendas_por_mes.get(mes_alvo, 0)
        erro_abs = abs(real - media_movel)
        erros_absolutos.append(erro_abs)

    total_previsto = sum(previsoes.values())
    total_previsto_arredondado = round(total_previsto)
    mae = sum(erros_absolutos) / len(erros_absolutos)

    print("\n" + "="*60)
    print("AVALIAÇÃO NO PRIMEIRO TRIMESTRE DE 2026 (TESTE)")
    print("="*60)
    for mes in meses_teste:
        print(f"Mês: {mes} | Real: {vendas_por_mes.get(mes, 0)} | Previsto (Média Móvel): {previsoes[mes]:.2f} | Erro Absoluto: {abs(vendas_por_mes.get(mes, 0) - previsoes[mes]):.2f}")

    print("-" * 60)
    print(f"SOMA TOTAL PREVISTA (FLOAT):       {total_previsto:.2f}")
    print(f"SOMA TOTAL PREVISTA (ARREDONDADA): {total_previsto_arredondado}")
    print(f"MAE (MEAN ABSOLUTE ERROR):         {mae:.2f}")
    print("="*60 + "\n")

    return total_previsto_arredondado, mae

if __name__ == "__main__":
    caminho_db = os.path.join('data', 'lh_nautical.db')
    prever_demanda_bussola(caminho_db)