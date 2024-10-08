import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# URL de conexão com o banco de dados PostgreSQL
DATABASE_URL = os.getenv("DB_URL")

# Cria o engine para conectar com o PostgreSQL
engine = create_engine(DATABASE_URL)

# Cria uma fábrica de sessões para interagir com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base para definir os modelos ORM
Base = declarative_base()

# Função para obter a sessão do banco de dados em cada requisição
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
