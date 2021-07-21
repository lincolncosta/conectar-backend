from fastapi import APIRouter, Request, Depends
from app.db.pessoa_projeto.crud import get_pessoa_projeto
import typing as t

from app.db.session import get_db
from app.db.notificacao.crud import (
    notificacao_pendente_idealizador,
    notificacao_pendente_colaborador,
    notificacao_aceito_recusado,
    notificacao_finalizado,
    notificacao_checagem,
    notificacao_checagem_projeto,
    get_notificacao_by_destinatario,
    get_notificacao_lida_by_destinatario,
    get_notificacao_by_id,
    edit_notificacao,
    delete_notificacao,
    ler_todas_notificacao
)
from app.db.notificacao.schemas import (
    Notificacao,
    NotificacaoCreate,
    NotificacaoEdit,
)
from app.core.auth import (
    get_current_active_pessoa
)

notificacao_router = r = APIRouter()


@r.get(
    "/notificacao/pendente_idealizador",
    status_code=200
)
async def pendente_idealizador_notificacao(
    db=Depends(get_db)
):
    """
    Create notificacao to pendente idealizador
    """

    notificacao_pendente_idealizador(db)


@r.post(
    "/notificacao/pendente_colaborador",
    response_model=NotificacaoCreate,
    response_model_exclude_none=True,
)
async def pendente_colaborador_notificacao(
    request: Request,
    pessoa_projeto_id: int,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Create notificacao to pendente colaborador
    """

    pessoaProjeto = get_pessoa_projeto(db, pessoa_projeto_id)

    notificacao = notificacao_pendente_colaborador(
        db, current_pessoa.id, pessoaProjeto)

    return notificacao


@r.post(
    "/notificacao/aceito_recusado",
    response_model=NotificacaoCreate,
    response_model_exclude_none=True,
)
async def aceito_recusado_notificacao(
    request: Request,
    pessoa_projeto_id: int,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Create notificacao to pendente colaborador
    """

    pessoaProjeto = get_pessoa_projeto(db, pessoa_projeto_id)

    notificacao = notificacao_aceito_recusado(
        db, current_pessoa.id, pessoaProjeto)

    return notificacao


@r.get(
    "/notificacao/checagem",
    status_code=200
)
async def checagem_notificacao(
    db=Depends(get_db)
):
    """
    Create notificacao
    """

    notificacao_checagem(db)


@r.get(
    "/notificacao/checagem/projeto",
    status_code=200
)
async def checagem_notificacao_projeto(
    db=Depends(get_db)
):
    """
    Create notificacao
    """

    notificacao_checagem_projeto(db)


@r.get(
    "/notificacao/id",
    response_model=Notificacao,
    response_model_exclude_none=True,
)
async def get_notificacao_id(
    request: Request,
    notificacao_id: int,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Get any notificacao details by id
    """

    notificacao = get_notificacao_by_id(db, notificacao_id)

    return notificacao


@r.get(
    "/notificacao/destinatario",
    response_model=t.List[Notificacao],
    response_model_exclude_none=True,
)
async def get_notificacao_destinatario(
    request: Request,
    destinatario_id: int,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Get any notificacao details by destinatario
    """

    notificacao = get_notificacao_by_destinatario(db, destinatario_id)

    return notificacao


@r.get(
    "/notificacao/destinatario/lidas",
    response_model=t.List[Notificacao],
    response_model_exclude_none=True,
)
async def get_notificacao_lida_destinatario(
    request: Request,
    destinatario_id: int,
    lido: bool,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Get any notificacao lida details by destinatario
    """

    notificacao = get_notificacao_lida_by_destinatario(
        db, destinatario_id, lido)

    return notificacao


@r.put("/notificacao",
       response_model=Notificacao,
       response_model_exclude_none=True,
       )
async def notificacao_edit(
    request: Request,
    notificacao_id: int,
    notificacao: NotificacaoEdit,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Edit Notificacao
    """

    return edit_notificacao(db, notificacao_id, notificacao)


@r.delete(
    "/notificacao",
    response_model=Notificacao,
    response_model_exclude_none=True,
)
async def notificacao_delete(
    request: Request,
    notificacao_id: int,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Delete notificacao
    """

    return delete_notificacao(db, notificacao_id)


@r.post(
    "/notificacao/ler-todas",
    status_code=200
)
async def notificacao_ler_todas(
    request: Request,
    destinatario_id: int,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Create notificacao
    """

    ler_todas_notificacao(db, destinatario_id)

    return {}
