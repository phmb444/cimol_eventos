from datetime import date, time
from fastapi import APIRouter, Depends, HTTPException, Response, Form, Cookie, UploadFile, File
from fastapi.responses import RedirectResponse
from app.models import evento_model
from app.models import user_model
from app.models.user_model import decrypt_session_token
from pydantic import BaseModel
import os
import shutil

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
    banner: UploadFile = File(...),
    icon: UploadFile = File(...),
    session_token: str = Cookie(None)
):
    if session_token is None:
        raise HTTPException(status_code=403, detail="Não autenticado")
    
    email = decrypt_session_token(session_token)
    organizador = evento_model.get_user_id_by_email(email)
    if not organizador:
        raise HTTPException(status_code=404, detail="Organizador não encontrado")

    # Processar e salvar as imagens
    banner_path = f"app/static/banners/{banner.filename}"
    icon_path = f"app/static/icons/{icon.filename}"
    
    banner_path_save = f"../../static/banners/{banner.filename}"
    icon_path_save = f"../../static/icons/{icon.filename}"

    with open(banner_path, "wb") as buffer:
        shutil.copyfileobj(banner.file, buffer)

    with open(icon_path, "wb") as buffer:
        shutil.copyfileobj(icon.file, buffer)

    result = evento_model.create_evento(
        nome_evento, descricao, data_inicio, tempo_inicio,
        data_fim, tempo_fim, local, vagas, aberto,
        organizador, banner_path_save, icon_path_save
    )
    return RedirectResponse(url="/eventos", status_code=303)

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

@router.post("/eventos/{id}/editar", tags=["Eventos"])
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
    banner: UploadFile = File(None),
    icon: UploadFile = File(None),
    session_token: str = Cookie(None)
):
    if session_token is None:
        raise HTTPException(status_code=403, detail="Não autenticado")
    
    email = decrypt_session_token(session_token)
    organizador = evento_model.get_user_id_by_email(email)
    if not organizador:
        raise HTTPException(status_code=404, detail="Organizador não encontrado")
    
    if banner:
        banner_path = f"app/static/banners/{banner.filename}"
        banner_path_save = f"../../static/banners/{banner.filename}"
        with open(banner_path, "wb") as buffer:
            shutil.copyfileobj(banner.file, buffer)
    if icon:
        icon_path = f"app/static/icons/{icon.filename}"
        icon_path_save = f"../../static/icons/{icon.filename}"
        with open(icon_path, "wb") as buffer:
            shutil.copyfileobj(icon.file, buffer)

    result = evento_model.update_evento(
        id, nome_evento, descricao, data_inicio, tempo_inicio,
        data_fim, tempo_fim, local, vagas, aberto,
        organizador, banner_path_save, icon_path_save
    )
    return RedirectResponse(url=f"/eventos/{id}", status_code=302)

@router.get("/eventos/{id}/deletar", tags=["Eventos"])
async def delete_evento(id: int):
    result = evento_model.delete_evento(id)
    if result == "ok":
        return RedirectResponse(url="/eventos", status_code=303)
    else:
        raise HTTPException(status_code=404, detail="Evento não encontrado")


@router.post("/eventos/{id}/inscricao", tags=["Eventos"])
async def inscrever_evento(id: int, session_token: str = Cookie(None)):
    if session_token is None:
        raise HTTPException(status_code=403, detail="Não autenticado")
    result = evento_model.inscrever_evento(id, session_token)
    return RedirectResponse(url=f"/eventos/{id}", status_code=303)
