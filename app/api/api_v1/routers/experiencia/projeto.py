from fastapi import APIRouter, Request, Depends
import typing as t

from app.db.session import get_db
from app.db.experiencia.projeto.crud import (
    create_experiencia,
    get_experiencia_by_id,
    get_experiencias_from_pessoa,
    edit_experiencia,
    delete_experiencia
)
from app.db.experiencia.schemas import (
    ExperienciaProjCreate,
    ExperienciaProj,
    ExperienciaProjEdit,
)
from app.core.auth import (
    get_current_active_pessoa,
    get_current_active_superuser,
)

experiencia_proj_router = r = APIRouter()


@r.get(
    "/experiencias/projeto/me",
    response_model=t.List[ExperienciaProj],
    response_model_exclude_none=True,
)
async def experiencia_projeto_me(
    current_pessoa=Depends(get_current_active_pessoa), db=Depends(get_db)
):
    """
    Get all experiencias from current logged pessoa
    """
    pessoa_id = current_pessoa.id
    experiencias = get_experiencias_from_pessoa(db, pessoa_id)
    return experiencias


@r.get(
    "/experiencias/projeto/{experiencia_id}",
    response_model=ExperienciaProj,
    response_model_exclude_none=True,
)
async def experiencia_details(
    request: Request,
    experiencia_id: int,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_superuser),
):
    """
    Get any experiencia projeto details
    """
    experiencia = get_experiencia_by_id(db, experiencia_id)
    return experiencia


@r.post(
    "/experiencias/projeto",
    response_model=ExperienciaProjCreate,
    response_model_exclude_none=True,
)
async def experiencia_create(
    request: Request,
    experiencia: ExperienciaProjCreate,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Create a new experiencia projeto
    """
    return create_experiencia(db, experiencia, current_pessoa.id)


@r.put(
    "/experiencias/projeto/{experiencia_id}",
    response_model=ExperienciaProj,
    response_model_exclude_none=True,
)
async def experiencia_edit(
    request: Request,
    experiencia_id: int,
    experiencia: ExperienciaProjEdit,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Update existing experiencia projeto
    """
    return edit_experiencia(db, experiencia_id, experiencia)


@r.delete(
    "/experiencias/projeto/{experiencia_id}",
    response_model=ExperienciaProj,
    response_model_exclude_none=True,
)
async def experiencia_projeto_delete(
    request: Request,
    experiencia_id: int,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
        Delete existing experiencia projeto
    """
    return delete_experiencia(db, experiencia_id)
