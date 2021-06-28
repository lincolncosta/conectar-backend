from fastapi import APIRouter, Request, Depends
from db.session import get_db

from db.seguir.crud import (
    create_seguir,
    delete_seguir,
    get_seguidores,
    get_qtd_seguidores,
    get_seguindo,
    get_qtd_seguindo
)
from db.seguir.schemas import Seguir
from db.pessoa.schemas import Pessoa
import typing as t
from core.auth import get_current_active_pessoa

seguir_router = r = APIRouter()


@r.get("/seguidores", response_model=t.List[Pessoa], response_model_exclude_none=True)
def get_lista_seguidores(
    pessoa_id: int,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Get lista de seguidores que um usuário possui
    """
    seguidores = get_seguidores(db, pessoa_id)
    return seguidores


# @r.get("/qtd_seguidores", response_model=t.List[Seguir], response_model_exclude_none=True)
# def get_num_seguidores(
#     pessoa_id: int,
#     db=Depends(get_db),
#     current_pessoa=Depends(get_current_active_pessoa),
# ):
#     """
#     Get quantidade de seguidores que um usuário possui
#     """
#     reacoes = get_qtd_seguidores(db, pessoa_id)
#     return reacoes


# @r.get("/seguindo", response_model=t.List[Seguir], response_model_exclude_none=True)
# def get_lista_seguindo(
#     pessoa_id: int,
#     projeto_id: int,
#     db=Depends(get_db),
#     current_pessoa=Depends(get_current_active_pessoa),
# ):
#     """
#     Get lista de usuários que um usuário segue
#     """
#     reacoes = get_seguindo(db, pessoa_id)
#     return reacoes


# @r.get("/qtd_seguindo", response_model=t.List[Seguir], response_model_exclude_none=True)
# def get_num_seguindo(
#     pessoa_id: int,
#     db=Depends(get_db),
#     current_pessoa=Depends(get_current_active_pessoa),
# ):
#     """
#     Get quantidade de usuários que um usuário segue
#     """
#     reacoes = get_qtd_seguindo(db, pessoa_id)
#     return reacoes


@r.post("/seguir", response_model=Seguir, response_model_exclude_none=True)
async def seguir_create(
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
