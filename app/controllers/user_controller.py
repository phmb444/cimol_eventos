from fastapi import APIRouter, Depends, HTTPException, Response, Form, Cookie
from fastapi.responses import RedirectResponse
from app.database import execute_query
from app.models.user_model import create_user, authenticate_user, get_user_by_session_token, generate_session_token

router = APIRouter()

# Rota de criação de usuário (já existente)
@router.post("/user", tags=["Usuários"])
def create_new_user(
    response: Response,
    nome: str = Form(...), 
    email: str = Form(...), 
    senha: str = Form(...), 
    telefone: str = Form(...)
):
    reponse = create_user(nome, email, senha, telefone)
    if reponse["funcionou"]:
        user = authenticate_user(email, senha)
        session_token = user["session_token"]
        redirect = RedirectResponse(url=f"/home", status_code=303)
        redirect.set_cookie(key="session_token", value=session_token)
        return redirect
    else:
        raise HTTPException(status_code=400, detail=reponse["msg"])

# Adicionando o login com cookies
@router.post("/login", tags=["Usuários"])
def login_user(response: Response, email: str = Form(...), senha: str = Form(...)):
    user = authenticate_user(email, senha)  # Função para verificar as credenciais
    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    # Criar um cookie de sessão para o usuário
    session_token = user["session_token"]  # Supomos que a função retorne um token único
    redirect_response = RedirectResponse(url="/home", status_code=303)
    redirect_response.set_cookie(
        key="session_token",
        value=session_token,
        samesite="Lax"
    )
    print(session_token)
    return redirect_response

# Rota de logout para remover o cookie
@router.get("/logout", tags=["Usuários"])
def logout_user(response: Response):
    redirecter = RedirectResponse(url="/", status_code=303)
    redirecter.delete_cookie(key="session_token")
    return redirecter
