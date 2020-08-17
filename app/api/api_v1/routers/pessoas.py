from fastapi import APIRouter, Request, Depends, Response, encoders
import typing as t

from app.db.session import get_db
from app.db.crud import (
    get_pessoas,
    get_pessoa,
    create_pessoa,
    delete_pessoa,
    edit_pessoa,
)
from app.db.schemas import PessoaCreate, PessoaEdit, Pessoa, PessoaOut
from app.core.auth import get_current_active_pessoa, get_current_active_superuser

pessoas_router = r = APIRouter()


@r.get(
    "/pessoas", response_model=t.List[Pessoa], response_model_exclude_none=True,
)
async def pessoas_list(
    response: Response,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_superuser),
):
    """
    Get all pessoas
    """
    pessoas = get_pessoas(db)
    # This is necessary for react-admin to work
    response.headers["Content-Range"] = f"0-9/{len(pessoas)}"
    return pessoas


@r.get("/pessoas/me", response_model=Pessoa, response_model_exclude_none=True)
async def pessoa_me(current_pessoa=Depends(get_current_active_pessoa)):
    """
    Get own pessoa
    """
    return current_pessoa


@r.get(
    "/pessoas/{pessoa_id}", response_model=Pessoa, response_model_exclude_none=True,
)
async def pessoa_details(
    request: Request,
    pessoa_id: int,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_superuser),
):
    """
    Get any pessoa details
    """
    pessoa = get_pessoa(db, pessoa_id)
    return pessoa
    # return encoders.jsonable_encoder(
    #     pessoa, skip_defaults=True, exclude_none=True,
    # )


@r.post("/pessoas", response_model=Pessoa, response_model_exclude_none=True)
async def pessoa_create(
    request: Request,
    pessoa: PessoaCreate,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_superuser),
):
    """
    Create a new pessoa
    """
    return create_pessoa(db, pessoa)


@r.put(
    "/pessoas/{pessoa_id}", response_model=Pessoa, response_model_exclude_none=True
)
async def pessoa_edit(
    request: Request,
    pessoa_id: int,
    pessoa: PessoaEdit,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_superuser),
):
    """
    Update existing pessoa
    """
    return edit_pessoa(db, pessoa_id, pessoa)


@r.delete(
    "/pessoas/{pessoa_id}", response_model=Pessoa, response_model_exclude_none=True
)
async def pessoa_delete(
    request: Request,
    pessoa_id: int,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_superuser),
):
    """
    Delete existing user
    """
    return delete_pessoa(db, pessoa_id)
