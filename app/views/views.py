from fastapi import APIRouter, Cookie, HTTPException
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from app.models import evento_model
from app.models import user_model
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
    print(user)
    eventos = evento_model.get_eventos_inscritos(session_token)
    if not user:
        raise HTTPException(status_code=403, detail="Sessão inválida ou expirada")
    return templates.TemplateResponse("user.html", {"request": request, "user": user, "eventos": eventos})


@router.get("/eventos", tags=["Eventos"])
async def eventos(request: Request, session_token: str = Cookie(None)):
    result = evento_model.get_eventos()
    gallery = evento_model.get_gallery_four()
    isAdmin = user_model.getUserType(session_token) == "organizador"
    return templates.TemplateResponse("all_events.html", {"request": request, "eventos": result, "isAdmin": isAdmin, "gallery": gallery})

@router.get("/eventos/{id}", tags=["Eventos"])
async def evento(request: Request, id: int, session_token: str = Cookie(None)):
    ja_inscrito = evento_model.ja_inscrito(id, session_token)
    result = evento_model.get_evento(id)
    isAdmin = user_model.getUserType(session_token) == "organizador"
    return templates.TemplateResponse("event_detail.html", {"request": request, "evento": result, "ja_inscrito": ja_inscrito, "isAdmin": isAdmin})

@router.get("/eventos/{id}/editar", tags=["Eventos"])
async def editar_evento(request: Request, id: int, session_token: str = Cookie(None)):
    if user_model.getUserType(session_token) != "organizador":
        raise HTTPException(status_code=403, detail="Acesso negado")
    evento = evento_model.get_evento(id)
    return templates.TemplateResponse("event_edit.html", {"request": request, "evento": evento})

@router.get("/home", tags=["Páginas"])
def home_page(request: Request) -> str:
    result = evento_model.get_eventos()
    for i in range(len(result)-1, 3, -1):
        result.pop(i)
    print(result)
    return templates.TemplateResponse("home.html", {"request": request, "eventos": result})

@router.get("/criar_evento", tags=["Eventos"])
async def eventos(request: Request, session_token: str = Cookie(None)):
    return templates.TemplateResponse("event_create.html", {"request": request})

@router.get("/galeria", tags=["Eventos"])
async def galeria(request: Request, session_token: str = Cookie(None)):
    gallery = evento_model.get_gallery()
    print(gallery)
    return templates.TemplateResponse("gallery.html", {"request": request, "gallery": gallery})