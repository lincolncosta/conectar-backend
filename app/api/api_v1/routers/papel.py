from fastapi import APIRouter, Request, Depends, Response
import typing as t

from app.db.session import get_db
from app.db.papel.crud import (
    get_papel,
    get_papel_by_id,
    create_papel,
    edit_papel,
    delete_papel,
)
from app.db.papel.schemas import PapelCreate, Papel, PapelEdit
from app.core.auth import (
    get_current_active_pessoa,
    get_current_active_superuser,
)

papel_router = r = APIRouter()


@r.get(
    "/papel",
    response_model=t.List[Papel],
    response_model_exclude_none=True,
)
async def papel_list(
    response: Response,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Get all papel
    """
    papel = get_papel(db)
    # This is necessary for react-admin to work
    response.headers["Content-Range"] = f"0-9/{len(papel)}"
    return papel


@r.get(
    "/papel/{papel_id}",
    response_model=Papel,
    response_model_exclude_none=True,
)
async def papel_details(
    response: Response,
    papel_id: int,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Get papel by id
    """
    papel = get_papel_by_id(db, papel_id)
    return papel


@r.post(
    "/papel",
    response_model=Papel,
    response_model_exclude_none=True,
)
async def papel_create(
    request: Request,
    papel: PapelCreate,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Create a new papel
    """
    return create_papel(db, papel, current_pessoa.id)


@r.put(
    "/papel/{papel_id}",
    response_model=Papel,
    response_model_exclude_none=True,
)
async def papel_edit(
    request: Request,
    papel_id: int,
    papel: PapelEdit,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Update existing papel
    """
    return edit_papel(db, papel_id, papel)


@r.delete(
    "/papel/{papel_id}",
    response_model=Papel,
    response_model_exclude_none=True,
)
async def papel_delete(
    request: Request,
    papel_id: int,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Delete existing papel
    """
    return delete_papel(db, papel_id)
