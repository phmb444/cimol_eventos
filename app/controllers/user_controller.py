from fastapi import APIRouter, Depends, HTTPException
from app.database import execute_query
from app.models.user_model import create_user
from fastapi import Form
from fastapi.responses import RedirectResponse

router = APIRouter()

@router.post("/user")
def create_new_user(
    nome: str = Form(...), 
    email: str = Form(...), 
    senha: str = Form(...), 
    telefone: str = Form(...)
):
    reponse = create_user(nome, email, senha, telefone)
    if reponse["funcionou"]:
        return RedirectResponse(url="/user/pedro", status_code=303)
        return reponse["msg"]
    else:
        raise HTTPException(status_code=400, detail=reponse["msg"])
