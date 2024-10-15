from datetime import date, datetime, time
from psycopg2 import Timestamp
from pydantic import BaseModel
from enum import Enum

class TipoUsuario(str, Enum):
    ORGANIZADOR = "organizador"
    EXTERNO = "externo"
    INTERNO = "interno"
    PROFESSOR = "professor"

class Status (str, Enum):
    INSCRITO = "inscrito"
    CANCELADO = "cancelado"
    
class StatusRecuperacao (str, Enum):
    PENDENTE = "pendente"
    VALIDADO = "concluido"

class User(BaseModel):
    id: int
    nome: str
    email: str
    senha: str
    telefone: str
    tipo_usuario: TipoUsuario
    cadastro: date
    
class Evento(BaseModel):
    id_evento: int
    nome_evento: str
    descricao: str
    data_inicio: date
    tempo_inicio: time
    data_fim: date
    tempo_fim: time
    local: str
    vagas: int
    aberto: bool
    data_cadastro: Timestamp
    organizador: int
    id_icon: int
    id_banner: int
    
class Foto(BaseModel):
    id_foto: int
    file_name: str
    
class Incricoes(BaseModel):
    id_inscricao: int
    id_evento: int
    id_usuario: int
    data_inscricao: Timestamp
    status: Status
    
class Recuperacao_senha(BaseModel):
    id: int
    id_usuario: int
    codigo_verificacao: str
    data_solicitacao: Timestamp
    data_validacao: Timestamp
    status: StatusRecuperacao
    