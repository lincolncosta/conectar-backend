from fastapi import APIRouter, Request, Depends
import typing as t

from app.db.session import get_db
from app.db.experiencia.profissional.crud import (
    create_experiencia,
    get_experiencia_by_id,
    get_experiencias_from_pessoa,
    edit_experiencia,
    delete_experiencia
)
from app.db.experiencia.schemas import (
    ExperienciaProfCreate,
    ExperienciaProf,
    ExperienciaProfEdit,
)
from app.core.auth import (
    get_current_active_pessoa,
    get_current_active_superuser,
)

experiencia_prof_router = r = APIRouter()


@r.get(
    "/experiencias/profissional/me",
    response_model=t.List[ExperienciaProf],
    response_model_exclude_none=True,
)
async def experiencia_profissional_me(
    current_pessoa=Depends(get_current_active_pessoa), db=Depends(get_db)
):
    """
    Get all experiencias from current logged pessoa
    """
    pessoa_id = current_pessoa.id
    experiencias = get_experiencias_from_pessoa(db, pessoa_id)
    return experiencias


@r.get(
    "/experiencias/profissional/{experiencia_id}",
    response_model=ExperienciaProf,
    response_model_exclude_none=True,
)
async def experiencia_details(
    request: Request,
    experiencia_id: int,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_superuser),
):
    """
    Get any experiencia profissional details
    """
    experiencia = get_experiencia_by_id(db, experiencia_id)
    return experiencia


@r.post(
    "/experiencias/profissional",
    response_model=ExperienciaProfCreate,
    response_model_exclude_none=True,
)
async def experiencia_create(
    request: Request,
    experiencia: ExperienciaProfCreate,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Create a new experiencia profissional
    """
    return create_experiencia(db, experiencia, current_pessoa.id)


@r.put(
    "/experiencias/profissional/{experiencia_id}",
    response_model=ExperienciaProf,
    response_model_exclude_none=True,
)
async def experiencia_edit(
    request: Request,
    experiencia_id: int,
    experiencia: ExperienciaProfEdit,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Update existing experiencia profissional
    """
    return edit_experiencia(db, experiencia_id, experiencia)


@r.delete(
    "/experiencias/profissional/{experiencia_id}",
    response_model=ExperienciaProf,
    response_model_exclude_none=True,
)
async def experiencia_profissional_delete(
    request: Request,
    experiencia_id: int,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
        Delete existing experiencia profissional
    """
    return delete_experiencia(db, experiencia_id)
