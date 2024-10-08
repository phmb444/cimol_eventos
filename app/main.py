from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.views import user_view
from app.database import engine, Base

# Inicializa o app FastAPI
app = FastAPI()

# Conecta arquivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Inclui rotas
app.include_router(user_view.router)

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Bem-vindo à aplicação FastAPI MVC"}
