from fastapi import (APIRouter, Request, Depends, Response,
                     encoders, UploadFile, File, Form)
import typing as t

from app.db.session import get_db
from app.db.pesquisa.pessoa import (
   get_pessoa_by_name,
   get_pessoa_by_area,
   get_pessoa_by_habilidade,
)
from app.db.pessoa.schemas import Pessoa

pesquisa_pessoa_router = r = APIRouter()

@r.get(
    "/pessoa/nome/{pessoa_name}", response_model=t.List[Pessoa], response_model_exclude_none=True,
)
async def pessoa_by_name(
    request: Request,
    pessoa_name: str,
    db=Depends(get_db)
):
    """
    Search pessoa by name
    """
    pessoa = get_pessoa_by_name(db, pessoa_name)
    return pessoa


@r.get(
    "/pessoa/area/{pessoa_area}", response_model=t.List[Pessoa], response_model_exclude_none=True,
)
async def pessoa_by_area(
    request: Request,
    pessoa_area: str,
    db=Depends(get_db)
):
    """
    Search pessoa by area
    """
    pessoa = get_pessoa_by_area(db, pessoa_area)
    return pessoa

@r.get(
    "/pessoa/habilidade/{pessoa_habilidade}", response_model=t.List[Pessoa], response_model_exclude_none=True,
)
async def pessoa_by_habilidade(
    request: Request,
    pessoa_habilidade: str,
    db=Depends(get_db)
):
    """
    Search pessoa by habilidade
    """
    pessoa = get_pessoa_by_habilidade(db, pessoa_habilidade)
    return pessoa
