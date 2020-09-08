from fastapi import APIRouter, Request, Depends, Response, encoders
import typing as t

from app.db.session import get_db
from app.db.Projeto.crud import (
    create_projeto,
    get_projetos,
    get_projeto,
    delete_projeto,
)
from app.db.Projeto.schemas import ProjetoCreate, Projeto, ProjetoOut
from app.core.auth import get_current_active_pessoa, get_current_active_superuser

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
    current_pessoa=Depends(get_current_active_superuser),
):
    """
    Get any pessoa details
    """
    projeto = get_projeto(db, projeto_id)
    return projeto
    # return encoders.jsonable_encoder(
    #     pessoa, skip_defaults=True, exclude_none=True,
    # )



@r.post("/projeto", response_model=Projeto, response_model_exclude_none=True)
async def projeto_create(
    request: Request,
    projeto: ProjetoCreate,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_superuser),
):
    """
    Create a new projeto
    """
    return create_projeto(db, projeto)

@r.delete(
    "/projeto/{projeto_id}", response_model=Projeto, response_model_exclude_none=True
)
async def projeto_delete(
    request: Request,
    projeto_id: int,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_superuser),
):
    """
    Delete existing user
    """
    return delete_projeto(db, projeto_id)
