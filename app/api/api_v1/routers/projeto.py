from fastapi import APIRouter, Request, Depends, Response, encoders
import typing as t

from app.db.session import get_db
from app.db.projeto.crud import (
    create_projeto,
    get_projetos,
    get_projeto,
    delete_projeto,
    edit_projeto
)
from app.db.projeto.schemas import ProjetoCreate, Projeto, ProjetoOut, ProjetoEdit
from app.core.auth import get_current_active_pessoa

projeto_router = r = APIRouter()


@r.get(
    "/projetos", response_model=t.List[Projeto], response_model_exclude_none=True,
)
async def projetos_list(
    response: Response,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Get all projetos
    """
    projetos = get_projetos(db)
    # This is necessary for react-admin to work
    response.headers["Content-Range"] = f"0-9/{len(projetos)}"
    return projetos

@r.get(
    "/projeto/{projeto_id}", response_model=Projeto, response_model_exclude_none=True,
)
async def projeto_details(
    request: Request,
    projeto_id: int,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Get any pessoa details
    """
    projeto = get_projeto(db, projeto_id)
    return projeto



@r.post("/projeto", response_model=Projeto, response_model_exclude_none=True)
async def projeto_create(
    request: Request,
    projeto: ProjetoCreate,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Create a new projeto
    """
    return await create_projeto(db, projeto)


@r.put(
    "/projeto",
    response_model=ProjetoEdit,
    response_model_exclude_none=True,
)
async def projeto_edit(
    request: Request,
    projeto: ProjetoEdit,
    projeto_id: int,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):

    return await edit_projeto(db, projeto_id, projeto, current_pessoa.id)


@r.delete(
    "/projeto/{projeto_id}", response_model=Projeto, response_model_exclude_none=True
)
async def projeto_delete(
    request: Request,
    projeto_id: int,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Delete existing user
    """
    return delete_projeto(db, projeto_id)
