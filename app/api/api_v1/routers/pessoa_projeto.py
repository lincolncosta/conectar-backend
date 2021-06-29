from fastapi import (
    APIRouter,
    Request,
    Depends,
    HTTPException
)
import typing as t

from app.db.session import get_db
from app.db.pessoa_projeto.crud import (
    create_pessoa_projeto,
    get_pessoa_projeto,
    get_all_pessoas_projeto,
    get_pessoa_projeto_by_projeto,
    get_similaridade_projeto,
    get_similaridade_vaga,
    edit_pessoa_projeto,
    delete_pessoa_projeto,
)
from app.db.pessoa_projeto.schemas import (
    PessoaProjeto,
    PessoaProjetoEdit,
    PessoaProjetoCreate,
    PessoaProjetoPessoaOut,
)
from app.db.pessoa.schemas import Pessoa

from core.auth import get_current_active_pessoa

pessoa_projeto_router = r = APIRouter()


@r.post(
    "/pessoa_projeto",
    response_model=PessoaProjeto,
    response_model_exclude_none=True,
)
async def pessoa_projeto_create(
    request: Request,
    pessoa_projeto: PessoaProjetoCreate,
    db=Depends(get_db),
    pessoa=Depends(get_current_active_pessoa),
):

    """
    Create a new pessoa_projeto
    """

    vagas = await get_pessoa_projeto_by_projeto(db, pessoa_projeto.projeto_id)
    qtd_vagas = len(vagas)

    if (qtd_vagas) < 5:
        pessoa_projeto = await create_pessoa_projeto(db, pessoa_projeto)
    else:
        raise HTTPException(
            status_code=417, detail="Este projeto atingiu o limite de 5 vagas cadastradas.")
    return pessoa_projeto


@r.get(
    "/pessoa_projeto",
    response_model=t.List[PessoaProjeto],
    response_model_exclude_none=True,
)
async def get_pessoas_projeto(
    request: Request,
    db=Depends(get_db),
    pessoa=Depends(get_current_active_pessoa),
):

    """
    Get all pessoa_projeto
    """

    pessoas_projeto = await get_all_pessoas_projeto(db)
    return pessoas_projeto


@r.get(
    "/pessoa_projeto/similaridade_projeto/{projeto_id}",
    response_model=t.Dict[int, Pessoa],
    response_model_exclude_none=True
)
async def similaridade_projeto(
    request: Request,
    projeto_id: int,
    db=Depends(get_db),
    pessoa_logada=Depends(get_current_active_pessoa),
):

    """
    Get pessoas mais similares dado um projeto específico
    """

    pessoas = await get_similaridade_projeto(db, pessoa_logada, projeto_id)

    return pessoas


@r.get(
    "/pessoa_projeto/similaridade_vaga/{pessoa_projeto_id}",
    response_model=Pessoa,
    response_model_exclude_none=True
)
async def similaridade_vaga(
    request: Request,
    pessoa_projeto_id: int,
    db=Depends(get_db),
    pessoa_logada=Depends(get_current_active_pessoa),
):

    """
    Get similaridade to only one vaga
    """

    pessoa = await get_similaridade_vaga(db, pessoa_logada, pessoa_projeto_id)

    return pessoa


@r.get(
    "/pessoa_projeto/projeto/{projeto_id}",
    response_model=t.List[PessoaProjetoPessoaOut],
    response_model_exclude_none=True,
)
async def get_all_pessoa_projeto_by_projeto(
    request: Request,
    projeto_id: int,
    db=Depends(get_db),
    pessoa=Depends(get_current_active_pessoa),
):
    """
    Get all pessoa_projeto on projeto
    """
    pessoa_projeto = await get_pessoa_projeto_by_projeto(db, projeto_id)
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
    pessoa=Depends(get_current_active_pessoa),
):
    """
    Get pessoa_projeto by id
    """
    pessoa_projeto = get_pessoa_projeto(db, pessoa_projeto_id)
    return pessoa_projeto


@r.put(
    "/pessoa_projeto/{pessoa_projeto_id}",
    response_model=PessoaProjeto,
    response_model_exclude_none=True,
)
async def pessoa_projeto_edit(
    request: Request,
    pessoa_projeto_id: int,
    pessoa_projeto: PessoaProjetoEdit,
    db=Depends(get_db),
    pessoa=Depends(get_current_active_pessoa),
):
    """
    Update pessoa_projeto
    """

    return await edit_pessoa_projeto(db, pessoa_projeto_id, pessoa_projeto, pessoa.id)


@r.delete(
    "/pessoa_projeto/{pessoa_projeto}",
    response_model=PessoaProjeto,
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
