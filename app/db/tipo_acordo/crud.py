from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t

from app.db import models
from . import schemas


def get_tipo_acordo(db: Session, tipo_acordo_id: int) -> schemas.TipoAcordo:

    tipo_acordo = (
        db.query(models.TipoAcordo)
        .filter(models.TipoAcordo.id == tipo_acordo_id)
        .first()
    )

    if not tipo_acordo:
        raise HTTPException(
            status_code=404, detail="tipo_acordo não encontrado"
        )
    return tipo_acordo


async def create_tipo_acordo(
    db: Session, tipo_acordo: schemas.TipoAcordoCreate
) -> schemas.TipoAcordo:

    filtro = db.query(models.Area)\
        .filter(models.TipoAcordo.descricao == tipo_acordo.descricao)\
        .first()
    if filtro:
        raise HTTPException(status_code=409, detail="TipoAcordo já cadastrado")


    try:
        db_tipo_acordo = models.TipoAcordo(
            descricao=tipo_acordo.descricao,
        )

        db.add(db_tipo_acordo)
        db.commit()
        db.refresh(db_tipo_acordo)
        
        return db_tipo_acordo
    except Exception as e:
        raise e


def edit_tipo_acordo(
    db: Session, tipo_acordo_id: int, tipo_acordo: schemas.TipoAcordoEdit
) -> schemas.TipoAcordoEdit:

    db_tipo_acordo = get_tipo_acordo(db, tipo_acordo_id)
    if not db_tipo_acordo:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="tipo_acordo não encontrado"
        )

    update_data = tipo_acordo.dict(exclude_unset=True)

    filtro = db.query(models.Area)\
        .filter(models.TipoAcordo.descricao == update_data["descricao"])\
        .first()
    if filtro:
        raise HTTPException(status_code=409, detail="TipoAcordo já cadastrado")


    for key, value in update_data.items():
        setattr(db_tipo_acordo, key, value)

    db.add(db_tipo_acordo)
    db.commit()
    db.refresh(db_tipo_acordo)
    return db_tipo_acordo


def delete_tipo_acordo(db: Session, tipo_acordo_id: int):

    tipo_acordo = get_tipo_acordo(db, tipo_acordo_id)
    if not tipo_acordo:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="tipo_acordo não encontrado"
        )

    db.delete(tipo_acordo)
    db.commit()
    return tipo_acordo