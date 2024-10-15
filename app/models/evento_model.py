from datetime import date, time
import hashlib
from app.database import execute_query
from app.models.utils import encrypt_password, compare_encrypted_passwords
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os
import json

load_dotenv()
SECRET = os.getenv("SECRET")

cipher_suite = Fernet(b'Ywk56SAgd4vrpeWiFPKIZ__e9jYsTg0c6di9N3OYr5Q=')

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

def create_evento(nome_evento: str, descricao: str, data_inicio: date, tempo_inicio:time, data_fim:date, tempo_fim:time, local: str, vagas: int, aberto: bool, organizador: int, id_icon: int, id_banner: int):
    query = """
    INSERT INTO eventos (nome_evento, descricao, data_inicio, tempo_inicio, data_fim, tempo_fim, local, vagas, aberto, data_cadastro, organizador, id_icon, id_banner)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, %s, %s, %s)
    """
    params = (nome_evento, descricao, data_inicio, tempo_inicio, data_fim, tempo_fim, local, vagas, aberto, organizador, id_icon, id_banner)
    try:
        execute_query(query, params)
        return {"msg": "Evento criado com sucesso"}
    except Exception as e:
        print(f"Erro: {e}")
        return {"msg": "Erro ao criar evento"}
    
def delete_evento(id_evento: int):
    query = """
    DELETE FROM eventos WHERE id_evento = %s
    """
    params = (id_evento,)
    try:
        execute_query(query, params)
        return {"msg": "Evento deletado com sucesso"}
    except Exception as e:
        print(f"Erro: {e}")
        return {"msg": "Erro ao deletar evento"}
    
def update_evento(id_evento: int, nome_evento: str, descricao: str, data_inicio: date, tempo_inicio: time, data_fim: date, tempo_fim: time, local: str, vagas: int, aberto: bool, organizador: int, id_icon: int, id_banner: int):
    query = """
    UPDATE eventos SET nome_evento = %s, descricao = %s, data_inicio = %s, tempo_inicio = %s, data_fim = %s, tempo_fim = %s, local = %s, vagas = %s, aberto = %s, organizador = %s, id_icon = %s, id_banner = %s
    WHERE id_evento = %s
    """
    params = (nome_evento, descricao, data_inicio, tempo_inicio, data_fim, tempo_fim, local, vagas, aberto, organizador, id_icon, id_banner, id_evento)
    try:
        execute_query(query, params)
        return json.dumps({"msg": "Evento atualizado com sucesso"})
    except Exception as e:
        print(f"Erro: {e}")
        return json.dumps({"msg": "Erro ao atualizar evento"})