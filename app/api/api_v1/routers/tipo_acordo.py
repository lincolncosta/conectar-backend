from fastapi import (
    APIRouter,
    Request,
    Depends,
    Response,
    encoders,
    UploadFile,
    File,
    Form,
)
import typing as t

from db.session import get_db
from db.tipo_acordo.crud import (
    get_tipo_acordo,
    create_tipo_acordo,
    delete_tipo_acordo,
    edit_tipo_acordo,
)

from db.tipo_acordo.schemas import (
    TipoAcordo,
    TipoAcordoBase,
    TipoAcordoCreate,
    TipoAcordoEdit,
    TipoAcordoOut,
)

tipo_acordo_router = r = APIRouter()


@r.get(
    "/tipoAcordo",
    response_model=TipoAcordo,
    response_model_exclude_none=True,
)
async def tipo_acordo_get(
    request: Request,
    tipo_acordo_id: int,
    db=Depends(get_db),
):
    tipo_acordo = get_tipo_acordo(db, tipo_acordo_id)
    return tipo_acordo


@r.post(
    "/tipo_acordo", response_model_exclude_none=True, response_model=TipoAcordo
)
async def tipo_acordo_create(
    request: Request, tipo_acordo: TipoAcordoCreate, db=Depends(get_db)
):
    """
    Create a new tipoAcordo
    """
    try:
        db_tipo_acordo = await create_tipo_acordo(db, tipo_acordo)
        return db_tipo_acordo

    except Exception as e:
        raise e


@r.put(
    "/tipo_acordo/{tipo_acordo_id}",
    response_model=TipoAcordo,
    response_model_exclude_none=True,
)
async def tipo_acordo_edit(
    request: Request,
    tipo_acordo: TipoAcordoEdit,
    tipo_acordo_id: int,
    db=Depends(get_db),
):
    return edit_tipo_acordo(db, tipo_acordo_id, tipo_acordo)


@r.delete(
    "/tipo_acordo/{tipo_acordo_id}",
    response_model=TipoAcordo,
    response_model_exclude_none=True,
)
async def tipo_acordo_delete(
    request: Request,
    tipo_acordo_id: int,
    db=Depends(get_db),
):

    return delete_tipo_acordo(db, tipo_acordo_id)
