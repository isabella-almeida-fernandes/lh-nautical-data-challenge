import csv
import os
import re
from datetime import datetime

# Regex simples para identificação de tipos comuns
INT_REGEX = re.compile(r'^-?\d+$')
FLOAT_REGEX = re.compile(r'^-?\d+\.\d+$')
DATE_REGEX = re.compile(r'^\d{4}-\d{2}-\d{2}$')
TIMESTAMP_REGEX = re.compile(r'^\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}')
BOOL_VALUES = {'true', 'false', 't', 'f', '1', '0'}

def inferir_tipo_valor(val):
    """Infere o tipo de um único valor individual."""
    val = val.strip()
    if not val or val.lower() in ('null', 'none', ''):
        return None  # Valor ausente/nulo
    
    if val.lower() in BOOL_VALUES:
        return 'BOOLEAN'
    if INT_REGEX.match(val):
        return 'INTEGER'
    if FLOAT_REGEX.match(val):
        return 'NUMERIC'
    if TIMESTAMP_REGEX.match(val):
        return 'TIMESTAMP'
    if DATE_REGEX.match(val):
        return 'DATE'
    
    return 'TEXT'

def resolver_tipo_coluna(tipos_encontrados):
    """
    Resolve o tipo final da coluna do PostgreSQL combinando 
    todos os tipos válidos observados no arquivo.
    """
    # Se todos os valores foram nulos
    if not tipos_encontrados:
        return 'VARCHAR(255)'
    
    # Hierarquia de tipos: TEXT domina qualquer inconsistência
    if 'TEXT' in tipos_encontrados:
        return 'VARCHAR(255)'
    if 'NUMERIC' in tipos_encontrados:
        return 'NUMERIC(15, 2)'
    if 'INTEGER' in tipos_encontrados and 'NUMERIC' in tipos_encontrados:
        return 'NUMERIC(15, 2)'
    if 'INTEGER' in tipos_encontrados:
        return 'INTEGER'
    if 'TIMESTAMP' in tipos_encontrados:
        return 'TIMESTAMP'
    if 'DATE' in tipos_encontrados:
        return 'DATE'
    if 'BOOLEAN' in tipos_encontrados:
        return 'BOOLEAN'
        
    return 'VARCHAR(255)'

def gerar_ddl_tabela(caminho_csv):
    """Lê um CSV e gera a instrução CREATE TABLE correspondente para PostgreSQL."""
    nome_tabela = os.path.splitext(os.path.basename(caminho_csv))[0]
    
    with open(caminho_csv, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            return ""  # Arquivo vazio
        
        # Mapeamento de cada coluna para os tipos observados
        tipos_por_coluna = {col: set() for col in header}
        
        for row in reader:
            for col_name, val in zip(header, row):
                tipo = inferir_tipo_valor(val)
                if tipo:
                    tipos_por_coluna[col_name].add(tipo)
                    
    # Construção da cláusula CREATE TABLE
    colunas_ddl = []
    for col_name in header:
        tipo_final = resolver_tipo_coluna(tipos_por_coluna[col_name])
        # Sanitiza nome da coluna se tiver caracteres especiais
        col_sanitizada = col_name.strip().lower()
        colunas_ddl.append(f"    {col_sanitizada} {tipo_final}")
        
    sql_ddl = f"DROP TABLE IF EXISTS {nome_tabela} CASCADE;\n"
    sql_ddl += f"CREATE TABLE {nome_tabela} (\n"
    sql_ddl += ",\n".join(colunas_ddl)
    sql_ddl += "\n);\n\n"
    
    return sql_ddl

def gerar_schema_completo(diretorio_csv, arquivo_saida):
    """Varre a pasta com os CSVs e grava o schema.sql final."""
    if not os.path.exists(diretorio_csv):
        raise FileNotFoundError(f"Diretório {diretorio_csv} não foi encontrado.")
        
    arquivos_csv = sorted([f for f in os.listdir(diretorio_csv) if f.endswith('.csv')])
    
    ddl_total = "-- ==============================================\n"
    ddl_total += "-- DDL SCHEMA GERADO AUTOMATICAMENTE - POSTGRESQL\n"
    ddl_total += f"-- Data de Geracao: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    ddl_total += "-- ==============================================\n\n"
    
    for arquivo in arquivos_csv:
        caminho_completo = os.path.join(diretorio_csv, arquivo)
        ddl_total += gerar_ddl_tabela(caminho_completo)
        
    with open(arquivo_saida, mode='w', encoding='utf-8') as f:
        f.write(ddl_total)
        
    print(f"Schema gerado com sucesso em: {arquivo_saida}")
    print(f"Total de tabelas mapeadas: {len(arquivos_csv)}")

if __name__ == "__main__":
    pasta_csv = os.path.join('lh_nautical_csv')
    saida_sql = 'schema.sql'
    gerar_schema_completo(pasta_csv, saida_sql)