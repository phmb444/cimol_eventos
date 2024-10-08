from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/user/{nome}")
def show_user(request: Request, nome: str) -> str:
    return templates.TemplateResponse("index.html", {"request": request, "nome": nome})