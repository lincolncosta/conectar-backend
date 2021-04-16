from fastapi import APIRouter, Request, Depends, Response
from app.db.pessoa_projeto.crud import get_pessoa_projeto
import typing as t

from app.db.session import get_db
from app.db.notificacao.crud import (
    create_notificacao_vaga,
    check_notificacao_vaga,
    get_notificacao_by_destinatario,
    get_notificacao_by_id,
    edit_notificacao,
    delete_notificacao,
    finaliza_notificacao_vaga,
)
from app.db.notificacao.schemas import (
    Notificacao,
    NotificacaoBase,
    NotificacaoCreate,
    NotificacaoEdit,
)
from app.core.auth import (
    get_current_active_pessoa,
    get_current_active_superuser,
)

notificacao_router = r = APIRouter()


@r.post(
    "/notificacao",
    response_model=NotificacaoCreate,
    response_model_exclude_none=True,
)
async def notificacao_create_vaga(
    request: Request,
    pessoa_projeto_id: int,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Create notificacao
    """

    notificacao = create_notificacao_vaga(
        db, current_pessoa.id, pessoa_projeto_id)

    return notificacao


@r.post(
    "/notificacao/finaliza",
    response_model=t.List[Notificacao],
    response_model_exclude_none=True,
)
async def notificacao_finaliza_vaga(
    request: Request,
    pessoa_projeto_id: int,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Create notificacao to pessoa_projeto that are "FINALIZADO"
    """

    pessoa_projeto = get_pessoa_projeto(db, pessoa_projeto_id)

    notificacao = finaliza_notificacao_vaga(db, pessoa_projeto_id, pessoa_projeto)

    return notificacao


@r.post(
    "/notificacao/check",
    response_model=t.List[Notificacao],
    response_model_exclude_none=True,
)
async def notificacao_checagem(
    request: Request,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Create notificacao
    """

    notificacao = check_notificacao_vaga(db)

    return notificacao


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
