from fastapi import APIRouter, Request, Depends
from db.session import get_db

from db.seguir.crud import (
    create_seguir,
    delete_seguir,
)
from db.seguir.schemas import Seguir

from core.auth import get_current_active_pessoa

seguir_router = r = APIRouter()


@r.post("/seguir", response_model=Seguir, response_model_exclude_none=True)
async def reacao_create(
    request: Request,
    seguir: Seguir,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Cria uma nova relação de seguir
    """
    return create_seguir(db, seguir)


@r.delete(
    "/seguir",
    response_model=Seguir,
    response_model_exclude_none=True,
)
async def seguir_delete(
    request: Request,
    seguido_id: int,
    seguidor_id: int,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Deleta relação existente de seguir
    """
    return delete_seguir(db, seguido_id, seguidor_id)
