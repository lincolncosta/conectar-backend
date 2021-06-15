from app.db.models import Projeto
from fastapi import APIRouter, Request, Depends, Response
import typing as t

from db.session import get_db
from db.projeto.crud import get_projetos_destaque
from db.pessoa.crud import (
    get_rand_pessoas,
    get_pessoas,
    get_pessoa_by_username,
    get_pessoa_by_id,
    create_pessoa,
    delete_pessoa,
    edit_pessoa,
)
from db.pessoa.schemas import PessoaCreate, PessoaEdit, Pessoa, PessoaOut
from core.auth import (
    get_current_active_pessoa,
    get_current_active_superuser,
)

pessoas_router = r = APIRouter()


@r.get(
    "/pessoas",
    response_model=t.List[Pessoa],
    response_model_exclude_none=True,
)
async def pessoas_list(
    response: Response,
    db=Depends(get_db)
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
    "/pessoas/{identificador}",
    response_model=PessoaOut,
    response_model_exclude_none=True,
)
async def pessoa_details(
    request: Request,
    identificador: str,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Get any pessoa details
    """
    if identificador.isnumeric():
        pessoa = get_pessoa_by_id(db, identificador)
    else:
        pessoa = get_pessoa_by_username(db, identificador)
    return pessoa
    # return encoders.jsonable_encoder(
    #     pessoa, skip_defaults=True, exclude_none=True,
    # )


@r.get(
    "/projeto/destaque/{qtd_projetos}",
    response_model=t.List[Pessoa],
    response_model_exclude_none=True,
)
async def projetos_destaque(
    request: Request,
    qtd_pessoas: int,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Get N pessoas destaque
    """
    projetos: Projeto = get_projetos_destaque(db, qtd_pessoas)
    pessoas = []

    for projeto in projetos:
        pessoa_id = projeto.pessoa_id
        pessoa = get_pessoa_by_id(pessoa_id)
        pessoas.append(pessoa)

    return pessoas


@r.post("/pessoas/random", response_model=t.List[Pessoa], response_model_exclude_none=True)
async def random_pessoas(
    request: Request,
    qtde: dict,
    db=Depends(get_db)
):

    """
    Get random pessoas
    """

    pessoas = get_rand_pessoas(db, qtde)

    return pessoas


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
    "/pessoas",
    response_model=Pessoa,
    response_model_exclude_none=True,
)
async def pessoa_edit(
    request: Request,
    pessoa: PessoaEdit,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Update current logged in pessoa
    """
    try:
        pessoa_id = current_pessoa.id
    except Exception as e:
        print(e)
    return await edit_pessoa(db, pessoa_id, pessoa)


@r.delete(
    "/pessoas",
    response_model=Pessoa,
    response_model_exclude_none=True,
)
async def pessoa_delete(
    request: Request,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Delete current logged pessoa
    """
    try:
        pessoa_id = current_pessoa.id
    except Exception as e:
        print(e)

    return delete_pessoa(db, pessoa_id)


@r.put(
    "/admin/pessoas/{pessoa_id}",
    response_model=Pessoa,
    response_model_exclude_none=True,
    tags=["admin"],
)
async def pessoa_edit_admin(
    request: Request,
    pessoa: PessoaEdit,
    pessoa_id: int,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_superuser),
):
    """
    Update data in pessoa performed by admin user
    """
    return await edit_pessoa(db, pessoa_id, pessoa)


@r.delete(
    "/admin/pessoas/{pessoa_id}",
    response_model=Pessoa,
    response_model_exclude_none=True,
    tags=["admin"],
)
async def pessoa_delete_admin(
    request: Request,
    pessoa_id: int,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_superuser),
):
    """
    Delete pessoa performed by admin user
    """

    return delete_pessoa(db, pessoa_id)
