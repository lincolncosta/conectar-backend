from fastapi import APIRouter, Request, Depends, Response
import typing as t
from db.session import get_db

from db.reacoes.crud import (
    create_reacao,
    edit_reacao,
    get_reacao,
    delete_reacao,
)
from db.reacoes.schemas import Reacoes, ReacoesCreate, ReacoesEdit

from core.auth import get_current_active_pessoa

reacoes_router = r = APIRouter()


@r.get("/reacoes", response_model=Reacoes, response_model_exclude_none=True)
def reacao_details(
    pessoa_id: int,
    projeto_id: int,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Get all reacoes
    """
    reacoes = get_reacao(db, pessoa_id, projeto_id)
    return reacoes


@r.post("/reacoes", response_model=Reacoes, response_model_exclude_none=True)
async def reacao_create(
    request: Request,
    reacao: ReacoesCreate,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Create a new reacao
    """
    return create_reacao(db, reacao)


@r.put(
    "/reacoes",
    response_model=Reacoes,
    response_model_exclude_none=True,
)
async def reacoes_edit(
    request: Request,
    reacao: ReacoesEdit,
    pessoa_id: int,
    projeto_id: int,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):

    return edit_reacao(db, projeto_id, pessoa_id, reacao)


@r.delete(
    "/reacoes",
    response_model=Reacoes,
    response_model_exclude_none=True,
)
async def projeto_delete(
    request: Request,
    pessoa_id: int,
    projeto_id: int,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Delete existing reacao
    """
    return delete_reacao(db, pessoa_id, projeto_id)
