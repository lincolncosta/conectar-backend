from app.db.seguir.schemas import SeguirCreate
from fastapi import APIRouter, Request, Depends
from db.session import get_db
from db.notificacao.crud import notificacao_seguindo
from db.seguir.crud import (
    create_seguir,
    delete_seguir,
    get_seguidores,
    get_seguindo
)
from db.seguir.schemas import SeguirCreate
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


@r.get("/qtd_seguidores", response_model=int, response_model_exclude_none=True)
def get_num_seguidores(
    pessoa_id: int,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Get quantidade de seguidores que um usuário possui
    """
    seguidores = len(get_seguidores(db, pessoa_id))
    return seguidores


@r.get("/seguindo", response_model=t.List[Pessoa], response_model_exclude_none=True)
def get_lista_seguindo(
    pessoa_id: int,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Get lista de usuários que um usuário segue
    """
    seguindo = get_seguindo(db, pessoa_id)
    return seguindo


@r.get("/qtd_seguindo", response_model=int, response_model_exclude_none=True)
def get_num_seguindo(
    pessoa_id: int,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Get quantidade de usuários que um usuário segue
    """
    qtd_seguindo = len(get_seguindo(db, pessoa_id))
    return qtd_seguindo


@r.post("/seguir", status_code=202)
async def seguir_create(
    request: Request,
    seguir: SeguirCreate,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Cria uma nova relação de seguir
    """
    create_seguir(db, seguir)
    notificacao_seguindo(db, seguir.seguido_id, seguir.seguidor_id)


@r.delete("/seguir", status_code=202)
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
    delete_seguir(db, seguido_id, seguidor_id)
