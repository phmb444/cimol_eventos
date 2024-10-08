import datetime
from app.database import execute_query


def create_user(nome: str, email: str, senha: str, telefone: str) -> dict:
    check_query = """
    SELECT COUNT(*) FROM usuarios WHERE email = %s OR telefone = %s
    """
    check_params = (email, telefone)
    result = execute_query(check_query, check_params)
    
    if result[0][0] > 0:
        raise ValueError("Já existe um usuário com este e-mail ou telefone")
    
    # Insert the new user
    query = """
    INSERT INTO usuarios (nome, email, telefone, senha, tipo_usuario, cadastro)
    VALUES (%s, %s, %s, %s, 'externo', CURRENT_DATE)
    """
    params = (nome, email, telefone, senha)
    
    try:
        execute_query(query, params)
        return {"msg": "Usuário criado com sucesso", "funcionou": True}
    except Exception as e:
        print(f"Erro: {e}")
        return {"msg": "Erro ao criar usuário", "funcionou": False}
    