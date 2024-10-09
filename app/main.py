from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.views import views
from app.controllers import user_controller


# Inicializa o app FastAPI
app = FastAPI()

# Conecta arquivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Inclui rotas
app.include_router(views.router)
app.include_router(user_controller.router)


@app.get("/")
async def root():
    return HTMLResponse(content="<h1>Bem-vindo à aplicação gerenciadora de eventos do cimol</h1>", status_code=200)
