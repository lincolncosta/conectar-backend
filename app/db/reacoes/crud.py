from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from db.notificacao.crud import notificacao_interesse, notificacao_favorito

from db import models
from . import schemas


def checa_existe_reacao(
    db: Session,
    reacao: schemas.ReacoesCreate
) -> bool:

    db_reacao = (
        db.query(models.Reacoes)
        .filter(models.Reacoes.pessoa_id == reacao.pessoa_id,
                models.Reacoes.projeto_id == reacao.projeto_id,
                models.Reacoes.reacao == reacao.reacao,)
        .first()
    )

    if db_reacao:
        return True
    else:
        return False


def create_reacao(
    db: Session, reacao: schemas.ReacoesCreate
) -> schemas.Reacoes:

    if not checa_existe_reacao(db, reacao):
        db_reacao = models.Reacoes(
            projeto_id=reacao.projeto_id,
            pessoa_id=reacao.pessoa_id,
            reacao=reacao.reacao,
        )

        db.add(db_reacao)
        db.commit()
        db.refresh(db_reacao)

        if db_reacao.reacao == 'FAVORITO':
            notificacao_favorito(db, db_reacao.pessoa_id, db_reacao.projeto_id)

        if db_reacao.reacao == 'INTERESSE':
            notificacao_interesse(db, db_reacao.pessoa_id,
                                  db_reacao.projeto_id)


def get_reacao(
    db: Session,
    pessoa_id: int,
    projeto_id: int
):
    try:
        db_reacao = (
            db.query(models.Reacoes)
            .filter(models.Reacoes.pessoa_id == pessoa_id,
                    models.Reacoes.projeto_id == projeto_id)
            .all()
        )
        if not db_reacao:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, detail="reação não encontrada"
            )
        return db_reacao
    except Exception as e:
        raise e


def edit_reacao(
    db: Session,
    pessoa_id: int,
    projeto_id: int,
    reacao: schemas.ReacoesEdit
):
    try:
        db_reacao = get_reacao(db, pessoa_id, projeto_id)

        if not db_reacao:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, detail="reação não encontrada"
            )

        update_data = reacao.dict(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_reacao, key, value)

        db.add(db_reacao)
        db.commit()
        db.refresh(db_reacao)

        return db_reacao

    except Exception as e:
        raise e


def delete_reacao(
    db: Session,
    pessoa_id: int,
    projeto_id: int,
    reacao: str,
):

    db_reacao = db.query(models.Reacoes)\
        .filter(models.Reacoes.pessoa_id == pessoa_id)\
        .filter(models.Reacoes.projeto_id == projeto_id)\
        .filter(models.Reacoes.reacao == reacao)\
        .first()

    if not db_reacao:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="reação não encontrada"
        )
    db.delete(db_reacao)
    db.commit()
    return db_reacao
