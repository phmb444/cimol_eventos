from fastapi import APIRouter, Cookie, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from app.models import evento_model
from app.models.evento_model import get_eventos, get_evento
from app.models.user_model import get_user_by_session_token  # Importing the correct functions

router = APIRouter()
templates = Jinja2Templates(directory="app/views/templates")

@router.get("/register" , tags=["Páginas"])
def register_page(request: Request) -> str:
    return templates.TemplateResponse("register.html", {"request": request})

@router.get("/login" , tags=["Páginas"])
def login_page(request: Request) -> str:
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/me", tags=["Usuários"])
def get_logged_user(request: Request, session_token: str = Cookie(None)):
    print(session_token)
    if session_token is None:
        raise HTTPException(status_code=403, detail="Não autenticado")
    user = get_user_by_session_token(session_token) 
    if not user:
        raise HTTPException(status_code=403, detail="Sessão inválida ou expirada")
    return templates.TemplateResponse("user.html", {"request": request, "user": user})


@router.get("/eventos", tags=["Eventos"])
async def eventos(request: Request):
    result = evento_model.get_eventos()
    return templates.TemplateResponse("all_events.html", {"request": request, "eventos": result})

@router.get("/eventos/{id}", tags=["Eventos"])
async def evento(request: Request, id: int):
    result = evento_model.get_evento(id)
    print(result)
    return templates.TemplateResponse("event_detail.html", {"request": request, "evento": result})
