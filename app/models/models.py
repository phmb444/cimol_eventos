from sqlalchemy import Column, BigInteger, String, Boolean, Date, Time, Integer, Text, ForeignKey, CheckConstraint, TIMESTAMP
from app.database import Base
from sqlalchemy.orm import relationship

# Tabela "incricoes"
class Incricao(Base):
    __tablename__ = "incricoes"

    id_inscricao = Column(BigInteger, primary_key=True)
    id_evento = Column(BigInteger, ForeignKey("eventos.id_evento"), nullable=False)
    id_usuario = Column(BigInteger, ForeignKey("usuarios.id"), nullable=False)
    data_inscricao = Column(TIMESTAMP, nullable=False)
    status = Column(String(255), nullable=False, default="inscrito")
    __table_args__ = (
        CheckConstraint("status IN ('inscrito', 'cancelado')"),
    )

# Tabela "recuperacao_senha"
class RecuperacaoSenha(Base):
    __tablename__ = "recuperacao_senha"

    id = Column(BigInteger, primary_key=True)
    id_usuario = Column(BigInteger, ForeignKey("usuarios.id"), nullable=False)
    codigo_verificacao = Column(String(255), nullable=False)
    data_solicitacao = Column(TIMESTAMP, nullable=False)
    data_validacao = Column(TIMESTAMP, nullable=False)
    status = Column(String(255), nullable=False, default="pendente")
    __table_args__ = (
        CheckConstraint("status IN ('pendente', 'concluido')"),
    )

# Tabela "eventos"
class Evento(Base):
    __tablename__ = "eventos"

    id_evento = Column(BigInteger, primary_key=True)
    nome_evento = Column(String(255), nullable=False)
    descricao = Column(Text, nullable=False)
    data_inicio = Column(Date, nullable=False)
    tempo_inicio = Column(Time, nullable=False)
    data_fim = Column(Date, nullable=False)
    tempo_fim = Column(Time, nullable=False)
    local = Column(String(255), nullable=False)
    vagas = Column(Integer, nullable=False)
    aberto = Column(Boolean, nullable=False, default=False)
    data_cadastro = Column(TIMESTAMP, nullable=False)
    organizador = Column(BigInteger, ForeignKey("usuarios.id"), nullable=False)
    id_icon = Column(BigInteger, ForeignKey("foto.id_foto"), nullable=False)
    id_banner = Column(BigInteger, ForeignKey("foto.id_foto"), nullable=False)

# Tabela "foto"
class Foto(Base):
    __tablename__ = "foto"

    id_foto = Column(BigInteger, primary_key=True)
    file_name = Column(String(255), nullable=False)

# Tabela "palestrante"
class Palestrante(Base):
    __tablename__ = "palestrante"

    id_palestrante = Column(BigInteger, primary_key=True)
    id_usuario = Column(BigInteger, ForeignKey("usuarios.id"), nullable=False)
    id_evento = Column(BigInteger, ForeignKey("eventos.id_evento"), nullable=False)
    perfil = Column(Text, nullable=False)
    tema_apresentacao = Column(String(255), nullable=False)
    id_foto = Column(BigInteger, ForeignKey("foto.id_foto"), nullable=False)

# Tabela "usuarios"
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(BigInteger, primary_key=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    senha = Column(String(255), nullable=False)
    telefone = Column(String(255), nullable=False, unique=True)
    tipo_usuario = Column(String(255), nullable=False)
    __table_args__ = (
        CheckConstraint("tipo_usuario IN ('organizador', 'palestrante', 'interno', 'externo', 'professor')"),
    )
    cadastro = Column(Date, nullable=False)
