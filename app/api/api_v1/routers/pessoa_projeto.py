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
from app.db.habilidade.schemas import PessoaHabilidadeCreate
from app.db.area.schemas import ProjetoAreaCreate

from app.db.session import get_db
from app.db.projeto.crud import get_projeto
from app.db.pessoa.crud import get_pessoa
from app.db.pessoa_projeto.crud import (
    create_pessoa_projeto,
    get_pessoa_projeto,
    get_pessoa_projeto_by_projeto,
    edit_pessoa_projeto,
)
from app.db.pessoa_projeto.schemas import (
    PessoaProjeto,
    PessoaProjetoBase,
    PessoaProjetoEdit,
    PessoaProjetoOut,
    PessoaProjetoCreate,
)

pessoa_projeto_router = r = APIRouter()


@r.post("/pessoa_projeto", response_model_exclude_none=True)
async def pessoa_projeto_create(
    request: Request,
    pessoa_projeto: PessoaProjetoCreate,
    db=Depends(get_db),
):

    """
    Create a new pessoa_projeto
    """

    pessoa_projeto = await create_pessoa_projeto(db, pessoa_projeto)
    return pessoa_projeto


@r.get(
    "/pessoa_projeto/projeto/{projeto_id}",
    response_model=PessoaProjeto,
    response_model_exclude_none=True,
)
async def get_all_pessoa_projeto_by_projeto(
    request: Request,
    projeto_id: int,
    db=Depends(get_db),
):
    """
    Get all pessoa_projeto on projeto
    """
    pessoa_projeto = get_pessoa_projeto_by_projeto(db, projeto_id)
    return pessoa_projeto


@r.get(
    "/pessoa_projeto/{pessoa_projeto_id}",
    response_model=PessoaProjeto,
    response_model_exclude_none=True,
)
async def pessoa_projeto_get(
    request: Request,
    pessoa_projeto_id: int,
    db=Depends(get_db),
):
    """
    Get pessoa_projeto by id
    """
    pessoa_projeto = get_pessoa_projeto(db, pessoa_projeto_id)
    return pessoa_projeto


@r.put(
    "/pessoa_projeto",
    response_model=PessoaProjetoEdit,
    response_model_exclude_none=True,
)
async def pessoa_projeto_edit(
    pessoa_projeto_id: int,
    pessoa_projeto: PessoaProjetoEdit,
    db=Depends(get_db),
):
    """
    Update pessoa_projeto
    """

    return await edit_pessoa_projeto(db, pessoa_projeto_id, pessoa_projeto)


@r.delete(
    "/pessoa_projeto/{pessoa_projeto}",
    response_model=Projeto,
    response_model_exclude_none=True,
)
async def pessoa_projeto_delete(
    request: Request,
    pessoa_projeto: int,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Delete existing pessoa_projeto
    """
    return delete_pessoa_projeto(db, pessoa_projeto)
