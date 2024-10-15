from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/views/templates")

@router.get("/user/{nome}", tags=["Páginas"])
def show_user(request: Request, nome: str):
    return templates.TemplateResponse("user.html", {"nome": nome})

@router.get("/register" , tags=["Páginas"])
def register_page(request: Request) -> str:
    
    return templates.TemplateResponse("register.html")

@router.get("/login" , tags=["Páginas"])
def login_page(request: Request) -> str:
    return templates.TemplateResponse("login.html")