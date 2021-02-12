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

from app.db.session import get_db
from app.db.projeto.crud import get_projeto
from app.db.pessoa.crud import get_pessoa
from app.db.endpoints.connections import (
    pessoa_projeto_aceite,
    pessoa_projeto_recusa,
    pessoa_projeto_pendente_colaborador_time
)
from app.db.pessoa_projeto.schemas import (
    PessoaProjeto,
    PessoaProjetoBase,
    PessoaProjetoEdit,
    PessoaProjetoOut,
    PessoaProjetoCreate,
)

from core.auth import get_current_active_pessoa

endpoint_router = r = APIRouter()

@r.put(
    "/endpoint/aceite",
    response_model=PessoaProjeto,
    response_model_exclude_none=True,
)
async def aceite(
    request: Request,
    pessoa_projeto_id: int,
    db=Depends(get_db),
):

    '''
        Update situação from pessoa_projeto
    '''

    return pessoa_projeto_aceite(db, pessoa_projeto_id)

@r.put(
    "/endpoint/recusa",
    response_model=PessoaProjeto,
    response_model_exclude_none=True,
)
async def recusa(
    request: Request,
    pessoa_projeto_id: int,
    db=Depends(get_db),
):
    """
    Update situação from pessoa_projeto to PENDENTE_IDEALIZADOR if user refuse invitation
    """
    
    return pessoa_projeto_recusa(db, pessoa_projeto_id)


@r.put(
    "/endpoint/tempo_de_espera",
    response_model=PessoaProjeto,
    response_model_exclude_none=True,
)
async def tempo_de_espera(
    request: Request,
    pessoa_projeto_id: int,
    db=Depends(get_db),
):
    """
    Update situação from pessoa_projeto to PENDENTE_IDEALIZADOR based on time
    OR sends message showing how many days are left
    """

    return pessoa_projeto_pendente_colaborador_time(db, pessoa_projeto_id)