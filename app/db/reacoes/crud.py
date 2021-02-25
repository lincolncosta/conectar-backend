from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from sqlalchemy.exc import IntegrityError
import typing as t

from db import models
from . import schemas


def create_reacao(
    db: Session, reacao: schemas.ReacoesCreate
) -> schemas.Reacoes:
    try:
        db_reacao = models.Reacoes(
            projeto_id=reacao.projeto_id,
            pessoa_id=reacao.pessoa_id,
            reacao=reacao.reacao,
        )

        db.add(db_reacao)
        db.commit()
        db.refresh(db_reacao)

        return db_reacao
    except IntegrityError as e:
        # Rollback to perform delete with new transaction
        db.rollback()
        return delete_reacao(db, reacao.pessoa_id, reacao.projeto_id)


def get_reacao(db: Session, pessoa_id: int, projeto_id: int):
    try:
        db_reacao = (
            db.query(models.Reacoes)
            .filter(
                models.Reacoes.pessoa_id == pessoa_id,
                models.Reacoes.projeto_id == projeto_id,
            )
            .first()
        )
        if not db_reacao:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, detail="reação não encontrada"
            )
        return db_reacao
    except Exception as e:
        raise e


def edit_reacao(
    db: Session, pessoa_id: int, projeto_id: int, reacao: schemas.ReacoesEdit
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


def delete_reacao(db: Session, pessoa_id: int, projeto_id: int):
    db_reacao = get_reacao(db, pessoa_id, projeto_id)
    if not db_reacao:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="reação não encontrado"
        )
    db.delete(db_reacao)
    db.commit()
    return db_reacao