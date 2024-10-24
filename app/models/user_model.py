import datetime
import hashlib
from app.database import execute_query
from app.models.utils import encrypt_password, compare_encrypted_passwords
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os
load_dotenv()
SECRET = os.getenv("SECRET")

cipher_suite = Fernet(b'Ywk56SAgd4vrpeWiFPKIZ__e9jYsTg0c6di9N3OYr5Q=')

def create_user(nome: str, email: str, senha: str, telefone: str) -> dict:
    check_query = """
    SELECT COUNT(*) FROM usuarios WHERE email = %s OR telefone = %s
    """
    check_params = (email, telefone)
    result = execute_query(check_query, check_params)
    
    if result[0][0] > 0:
        return {"msg": "Usuário já existe", "funcionou": False} 
   
    # Encrypt the password
    encrypted_password = encrypt_password(senha)
    
    # Insert the new user
    query = """
    INSERT INTO usuarios (nome, email, telefone, senha, tipo_usuario, cadastro)
    VALUES (%s, %s, %s, %s, 'externo', CURRENT_DATE)
    """
    params = (nome, email, telefone, encrypted_password)
    
    try:
        execute_query(query, params)
        return {"msg": "Usuário criado com sucesso", "funcionou": True}
    except Exception as e:
        print(f"Erro: {e}")
        return {"msg": "Erro ao criar usuário", "funcionou": False}
    
def generate_session_token(email: str) -> str:
    encrypted_email = cipher_suite.encrypt(email.encode())
    return encrypted_email.decode()

def decrypt_session_token(encrypted_email: str) -> str:
    decrypted_email = cipher_suite.decrypt(encrypted_email.encode())
    return decrypted_email.decode()

def authenticate_user(email: str, senha: str) -> dict:
    query = """
    SELECT nome, email, telefone, senha FROM usuarios WHERE email = %s
    """
    result = execute_query(query, (email,))
    
    if not result or not compare_encrypted_passwords(result[0][3],senha):  # Verifica a senha criptografada
        return None
    
    session_token = generate_session_token(email)
    
    return {
        "nome": result[0][0],
        "email": result[0][1],
        "telefone": result[0][2],
        "session_token": session_token
    }

def get_user_by_session_token(session_token: str):
    print(f"Received session_token: {session_token}")  # Debugging line
    email = decrypt_session_token(session_token)
    print(f"Decrypted email: {email}")  # Debugging line
    query = """
    SELECT nome, email, telefone FROM usuarios WHERE email = %s
    """
    result = execute_query(query, (email,))  # Updated to pass email as a tuple
    
    if not result:
        return None
    
    response = {
        "nome": result[0][0],
        "email": result[0][1],
        "telefone": result[0][2]
    }
    
    print(response)
    
    return response
    
def getUserType(email: str) -> str:
    query = """
    SELECT tipo_usuario FROM usuarios WHERE email = %s
    """
    result = execute_query(query, (email,))
    
    if not result:
        return None
    
    return result[0][0]
