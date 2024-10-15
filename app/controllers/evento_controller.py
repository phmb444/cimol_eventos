from datetime import date, time
from fastapi import APIRouter, Depends, HTTPException, Response, Form, Cookie
from fastapi.responses import RedirectResponse
from app.models import evento_model
from pydantic import BaseModel

router = APIRouter()
class Evento(BaseModel):
    nome_evento: str
    descricao: str
    data_inicio: date
    tempo_inicio: time
    data_fim: date
    tempo_fim: time
    local: str
    vagas: int
    aberto: bool
    organizador: int
    id_icon: int
    id_banner: int


@router.get("/eventos", tags=["Eventos"])
async def eventos():
    result = evento_model.get_eventos()
    return {"eventos": result}

@router.get("/eventos/{id}", tags=["Eventos"])
async def evento(id: int):
    result = evento_model.get_evento(id)
    return result

@router.post("/eventos", tags=["Eventos"])
async def create_evento(
    nome_evento: str = Form(...),
    descricao: str = Form(...),
    data_inicio: date = Form(...),
    tempo_inicio: time = Form(...),
    data_fim: date = Form(...),
    tempo_fim: time = Form(...),
    local: str = Form(...),
    vagas: int = Form(...),
    aberto: bool = Form(...),
    organizador: int = Form(...),
    id_icon: int = Form(...),
    id_banner: int = Form(...)
):
    result = evento_model.create_evento(
        nome_evento, descricao, data_inicio, tempo_inicio,
        data_fim, tempo_fim, local, vagas, aberto,
        organizador, id_icon, id_banner
    )
    return result


@router.put("/eventos/{id}", tags=["Eventos"])
async def update_evento(
    id: int,
    nome_evento: str = Form(...),
    descricao: str = Form(...),
    data_inicio: date = Form(...),
    tempo_inicio: time = Form(...),
    data_fim: date = Form(...),
    tempo_fim: time = Form(...),
    local: str = Form(...),
    vagas: int = Form(...),
    aberto: bool = Form(...),
    organizador: int = Form(...),
    id_icon: int = Form(...),
    id_banner: int = Form(...)
):
    result = evento_model.update_evento(
        id, nome_evento, descricao, data_inicio, tempo_inicio,
        data_fim, tempo_fim, local, vagas, aberto,
        organizador, id_icon, id_banner
    )
    return result

@router.delete("/eventos/{id}", tags=["Eventos"])
async def delete_evento(id: int):
    result = evento_model.delete_evento(id)
    return result
    result = evento_model.delete_evento(id)
    return result
