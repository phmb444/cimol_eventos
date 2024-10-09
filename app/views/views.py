from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/user/{nome}")
def show_user(request: Request, nome: str) -> str:
    return templates.TemplateResponse("user.html", {"request": request, "nome": nome})

@router.get("/register")
def register_page(request: Request) -> str:
    return templates.TemplateResponse("register.html", {"request": request})

@router.get("/login")
def login_page(request: Request) -> str:
    return templates.TemplateResponse("login.html", {"request": request})