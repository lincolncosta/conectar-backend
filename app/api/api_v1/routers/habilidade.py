from fastapi import APIRouter, Request, Depends, Response
import typing as t

from db.session import get_db
from db.habilidade.crud import (
    get_habilidades,
    create_habilidades,
    get_habilidades_by_id,
    edit_habilidades,
    delete_habilidades,
    get_habilidade_by_name
)
from db.habilidade.schemas import (
    HabilidadesCreate,
    Habilidades,
    HabilidadesEdit
)
from core.auth import (
    get_current_active_pessoa,
    get_current_active_superuser,
)

habilidades_router = r = APIRouter()


@r.get(
    "/habilidades",
    response_model=t.List[Habilidades],
    response_model_exclude_none=True,
)
async def habilidades_list(
    response: Response,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Get all habilidades
    """
    habilidades = get_habilidades(db)
    # This is necessary for react-admin to work
    response.headers["Content-Range"] = f"0-9/{len(habilidades)}"
    return habilidades


@r.get(
    "/habilidades/name/{habilidades_name}",
    response_model=t.List[Habilidades],
    response_model_exclude_none=True,
)
async def habilidades_details_name(
    request: Request,
    habilidades_name: str,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Get any habilidades details by its name
    """

    habilidades = get_habilidade_by_name(db, habilidades_name)

    return habilidades


@r.post(
    "/habilidades",

    response_model=Habilidades,
    response_model_exclude_none=True,
)
async def habilidades_create(
    request: Request,
    habilidades: HabilidadesCreate,
    db=Depends(get_db),
):
    """
    Create a new habilidades
    """
    return create_habilidades(db, habilidades)

@r.put(
    "/habilidades/{habilidade_id}",
    response_model=Habilidades,
    response_model_exclude_none=True,
)
async def habilidade_edit(
    request: Request,
    habilidade_id: int,
    habilidades: HabilidadesEdit,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Update existing habilidades
    """
    return edit_habilidades(db, habilidade_id, habilidades)


@r.delete(
    "/habilidade/{habilidade_id}",
    response_model=Habilidades,
    response_model_exclude_none=True,
)
async def habilidade_pessoa_delete(
    request: Request,
    habilidade_id: int,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
        Delete existing habilidades
    """
    return delete_habilidades(db, habilidade_id)
