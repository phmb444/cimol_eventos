from datetime import date, time
import hashlib

from fastapi.responses import RedirectResponse
from app.database import execute_query
from app.models.user_model import decrypt_session_token
from app.models.utils import encrypt_password, compare_encrypted_passwords
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os
import json

load_dotenv()
SECRET = os.getenv("SECRET")

cipher_suite = Fernet(b'Ywk56SAgd4vrpeWiFPKIZ__e9jYsTg0c6di9N3OYr5Q=')

def get_user_id_by_email(email: str):
    query = "SELECT id FROM usuarios WHERE email = %s"
    params = (email,)
    result = execute_query(query, params)
    if not result:
        return None
    return result[0][0]

def get_eventos():
    query = """
    SELECT e.*, COUNT(i.id_inscricao) as inscritos FROM eventos e
    LEFT JOIN inscricoes i ON e.id_evento = i.id_evento GROUP BY e.id_evento ORDER BY e.data_inicio DESC 
    """
    RESULT = execute_query(query)
    if not RESULT:
        return {"msg": "Nenhum evento encontrado"}
    
    eventos = []
    for row in RESULT:
        evento = {
            "id_evento": row[0],
            "nome_evento": row[1],
            "descricao": row[2],
            "data_inicio": row[3],
            "tempo_inicio": row[4],
            "data_fim": row[5],
            "tempo_fim": row[6],
            "local": row[7],
            "vagas": row[8],
            "aberto": row[9],
            "data_cadastro": row[10],
            "organizador": row[11],
            "id_icon": row[12],
            "id_banner": row[13],
            "inscritos": row[14]
        }
        eventos.append(evento)
    
    return eventos

def get_evento(id_evento: int):
    query = """
    SELECT e.*, COUNT(i.id_inscricao) as inscritos FROM eventos e
    LEFT JOIN inscricoes i ON e.id_evento = i.id_evento WHERE e.id_evento = %s GROUP BY e.id_evento
    """
    params = (id_evento,)
    RESULT = execute_query(query, params)
    if not RESULT:
        return {"msg": "Nenhum evento encontrado"}
    
    row = RESULT[0]
    evento = {
        "id_evento": row[0],
        "nome_evento": row[1],
        "descricao": row[2],
        "data_inicio": row[3],
        "tempo_inicio": row[4],
        "data_fim": row[5],
        "tempo_fim": row[6],
        "local": row[7],
        "vagas": row[8],
        "aberto": row[9],
        "data_cadastro": row[10],
        "organizador": row[11],
        "id_icon": row[12],
        "id_banner": row[13],
        "inscritos": row[14]
    }
    
    return evento

def create_evento(nome_evento: str, descricao: str, data_inicio: date, tempo_inicio:time, data_fim:date, tempo_fim:time, local: str, vagas: int, aberto: bool, organizador: int, banner_path: str, icon_path: str):
    query = """
    INSERT INTO eventos (nome_evento, descricao, data_inicio, tempo_inicio, data_fim, tempo_fim, local, vagas, aberto, data_cadastro, organizador, id_icon, id_banner)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, %s, %s, %s)
    """
    params = (nome_evento, descricao, data_inicio, tempo_inicio, data_fim, tempo_fim, local, vagas, aberto, organizador, icon_path, banner_path)
    try:
        execute_query(query, params)
        return None
    except Exception as e:
        print(f"Erro: {e}")
        return {"msg": "Erro ao criar evento"}
    
def delete_evento(id_evento: int):
    try:
        # Delete all inscriptions related to the event
        query_inscricoes = "DELETE FROM inscricoes WHERE id_evento = %s"
        params_inscricoes = (id_evento,)
        execute_query(query_inscricoes, params_inscricoes)
        
        # Delete the event
        query_evento = "DELETE FROM eventos WHERE id_evento = %s"
        params_evento = (id_evento,)
        execute_query(query_evento, params_evento)
        
        return "ok"
    except Exception as e:
        print(f"Erro: {e}")
        return "not ok"
    
def update_evento(id_evento, nome_evento, descricao, data_inicio, tempo_inicio, data_fim, tempo_fim, local, vagas, aberto, organizador, banner_path, icon_path):
    query = """
    UPDATE eventos SET nome_evento=%s, descricao=%s, data_inicio=%s, tempo_inicio=%s,
    data_fim=%s, tempo_fim=%s, local=%s, vagas=%s, aberto=%s, organizador=%s,
    id_icon=%s, id_banner=%s WHERE id_evento=%s
    """
    params = (nome_evento, descricao, data_inicio, tempo_inicio, data_fim, tempo_fim, local, vagas, aberto, organizador, icon_path, banner_path, id_evento)
    execute_query(query, params)

def inscrever_evento(id_evento: int, session_token: str):
    email = decrypt_session_token(session_token)
    query = "select id from usuarios where email = %s"
    params = (email,)
    result = execute_query(query, params)
    if not result:
        return {"msg": "Usuário não encontrado"}
    id_usuario = result[0][0]
    query = "select count(*) from inscricoes where id_evento = %s and id_usuario = %s"
    params = (id_evento, id_usuario)
    result = execute_query(query, params)
    if result[0][0] > 0:
        query = "DELETE FROM inscricoes WHERE id_evento = %s AND id_usuario = %s"
        params = (id_evento, id_usuario)
        execute_query(query, params)
        return "ok"    
    query = "insert into inscricoes (id_evento, id_usuario, data_inscricao, status) values (%s, %s, CURRENT_TIMESTAMP, 'inscrito')"
    params = (id_evento, id_usuario)
    result = execute_query(query, params)
    return "ok"

def ja_inscrito(id_evento: int, session_token: str):
    email = decrypt_session_token(session_token)
    query = "select id from usuarios where email = %s"
    params = (email,)
    result = execute_query(query, params)
    if not result:
        return {"msg": "Usuário não encontrado"}
    id_usuario = result[0][0]
    query = "select count(*) from inscricoes where id_evento = %s and id_usuario = %s"
    params = (id_evento, id_usuario)
    result = execute_query(query, params)
    if result[0][0] > 0:
        return True
    return False

def get_eventos_inscritos(session_token: str):
    email = decrypt_session_token(session_token)
    query = "SELECT id FROM usuarios WHERE email = %s"
    params = (email,)
    result = execute_query(query, params)
    if not result:
        return {"msg": "Usuário não encontrado"}
    id_usuario = result[0][0]
    
    query = """
    SELECT e.*, COUNT(i.id_inscricao) as inscritos FROM eventos e
    LEFT JOIN inscricoes i ON e.id_evento = i.id_evento WHERE i.id_usuario = %s GROUP BY e.id_evento ORDER BY e.data_inicio DESC 
    """
    params = (id_usuario,)
    RESULT = execute_query(query, params)
    if not RESULT:
        return {"msg": "Nenhum evento encontrado"}
    
    eventos = []
    for row in RESULT:
        evento = {
            "id_evento": row[0],
            "nome_evento": row[1],
            "descricao": row[2],
            "data_inicio": row[3],
            "tempo_inicio": row[4],
            "data_fim": row[5],
            "tempo_fim": row[6],
            "local": row[7],
            "vagas": row[8],
            "aberto": row[9],
            "data_cadastro": row[10],
            "organizador": row[11],
            "id_icon": row[12],
            "id_banner": row[13],
            "inscritos": row[14]
        }
        eventos.append(evento)
    
    return eventos


def get_gallery():
    query = "SELECT id_banner, id_icon FROM eventos"
    RESULT = execute_query(query)
    if not RESULT:
        return {"msg": "Nenhum evento encontrado"}
        
    gallery = []
    for row in RESULT:
        item = {
            "id_banner": row[0],
            "id_icon": row[1]
        }
        gallery.append(item)
        
    return gallery

def get_gallery_four():
    query = "SELECT id_banner, id_icon FROM eventos"
    RESULT = execute_query(query)
    if not RESULT:
        return {"msg": "Nenhum evento encontrado"}
        
    gallery = []
    for row in RESULT:
        item = {
            "id_banner": row[0],
            "id_icon": row[1]
        }
        gallery.append(item)
        
    return gallery[:4]