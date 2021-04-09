from fastapi import (APIRouter, Request, Depends, Response,
                     encoders, UploadFile, File, Form)
import typing as t

from app.db.session import get_db
from app.db.pesquisa.projeto import (
    get_projeto_by_area,
    get_projeto_by_habilidade,
    get_projeto_by_name,
    get_projeto_by_objective,
)
from app.db.projeto.schemas import ProjetoCreate, Projeto, ProjetoOut, ProjetoEdit

pesquisa_projeto_router = r = APIRouter()

@r.get(
    "/projeto/nome/{projeto_name}", response_model=t.List[Projeto], response_model_exclude_none=True,
)
async def projeto_by_name(
    request: Request,
    projeto_name: str,
    db=Depends(get_db)
):
    """
    Search project by name
    """
    projetos = get_projeto_by_name(db, projeto_name)
    return projetos

@r.get(
    "/projeto/objetivo/{projeto_objective}", response_model=t.List[Projeto], response_model_exclude_none=True,
)
async def projeto_by_objective(
    request: Request,
    projeto_objective: str,
    db=Depends(get_db)
):
    """
    Search project by objective
    """
    projetos = get_projeto_by_objective(db, projeto_objective)
    return projetos

@r.get(
    "/projeto/area/{projeto_area}", response_model=t.List[Projeto], response_model_exclude_none=True,
)
async def projeto_by_area(
    request: Request,
    projeto_area: str,
    db=Depends(get_db)
):
    """
    Search project by area
    """
    projetos = get_projeto_by_area(db, projeto_area)
    return projetos

@r.get(
    "/projeto/habilidade/{projeto_habilidade}", response_model=t.List[Projeto], response_model_exclude_none=True,
)
async def projeto_by_habilidades(
    request: Request,
    projeto_habilidade: str,
    db=Depends(get_db)
):
    """
    Search project by habilidade
    """
    projetos = get_projeto_by_habilidade(db, projeto_habilidade)
    return projetos