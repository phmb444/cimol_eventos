import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# URL de conexão com o PostgreSQL
DATABASE_URL = os.getenv("DB_URL")

# Função para executar uma consulta SQL
def execute_query(query, params=None):
    try:
        # Conecta ao banco de dados
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        # Executa a consulta SQL
        cur.execute(query, params)

        # Se for uma consulta SELECT, fetchall() retorna os resultados
        if query.strip().lower().startswith("select"):
            result = cur.fetchall()
            cur.close()
            conn.close()
            return result

        # Commit para comandos como INSERT, UPDATE, DELETE
        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        print(f"Erro: {e}")
