from fastapi import APIRouter, Depends, HTTPException, Response, Form, Cookie
from fastapi.responses import RedirectResponse
from app.database import execute_query
from app.models.user_model import create_user, authenticate_user, get_user_by_session_token, generate_session_token

router = APIRouter()

# Rota de criação de usuário (já existente)
@router.post("/user", tags=["Usuários"])
def create_new_user(
    nome: str = Form(...), 
    email: str = Form(...), 
    senha: str = Form(...), 
    telefone: str = Form(...)
):
    reponse = create_user(nome, email, senha, telefone)
    if reponse["funcionou"]:
        return RedirectResponse(url=f"/user/{nome}", status_code=303)
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
    response.set_cookie(key="session_token", value=session_token, expires=604800)  # O cookie expira em 1 hora
    
    return {"msg": "Login bem-sucedido"}

# Rota para verificar se o usuário está autenticado via cookie
@router.get("/me", tags=["Usuários"])
def get_logged_user(session_token: str = Cookie(None)):
    if session_token is None:
        raise HTTPException(status_code=403, detail="Não autenticado")
    
    # Função para verificar o token da sessão
    user = get_user_by_session_token(session_token)  # Função que busca o usuário pelo token
    
    if not user:
        raise HTTPException(status_code=403, detail="Sessão inválida ou expirada")
    
    return {"username": user["nome"], "email": user["email"], "telefone": user["telefone"]}

# Rota de logout para remover o cookie
@router.post("/logout", tags=["Usuários"])
def logout_user(response: Response):
    response.delete_cookie(key="session_token")
    return {"msg": "Logout bem-sucedido"}
