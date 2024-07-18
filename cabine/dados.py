#import pandas as pd
import sqlite3

def procurar_dados(codigo):
    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect('meu_banco_de_dados.db')
    cursor = conn.cursor()

    # Executar a consulta para obter os dados baseados no código
    cursor.execute('''
    SELECT codigo, nome, anos FROM minha_tabela WHERE codigo = ?
    ''', (codigo,))

    # Recuperar os resultados da consulta
    resultado = cursor.fetchone()

    # Fechar a conexão
    conn.close()
    
    return resultado
"""
# Ler os dados da planilha Excel
df = pd.read_excel('planilha.xlsx')  # Substitua 'dados.xlsx' pelo caminho para o seu arquivo

# Conectar ao banco de dados SQLite (ou criar um novo)
conn = sqlite3.connect('meu_banco_de_dados.db')
cursor = conn.cursor()

# Criar a tabela se não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS minha_tabela (
    codigo INTEGER PRIMARY KEY,
    nome TEXT,
    anos INTEGER
)
''')

# Inserir os dados da planilha no banco de dados
for index, row in df.iterrows():
    cursor.execute('''
    INSERT INTO minha_tabela (codigo, nome, anos) VALUES (?, ?, ?)
    ''', (row['codigo'], row['nome'], row['anos']))

# Commit e fechar a conexão
conn.commit()
conn.close()
"""