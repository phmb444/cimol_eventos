from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from app.views import views
from app.controllers import user_controller, evento_controller


# Inicializa o app FastAPI
app = FastAPI()

# Conecta arquivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Inclui rotas
app.include_router(views.router)
app.include_router(user_controller.router)
app.include_router(evento_controller.router)


@app.get("/")
async def root():
    return RedirectResponse(url="/login")
