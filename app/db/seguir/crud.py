from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from db import models
from . import schemas


def create_seguir(
    db: Session, seguir: schemas.Seguir
) -> schemas.Seguir:

    db_seguir = models.Seguir(
        seguido_id=seguir.seguido_id,
        seguidor_id=seguir.seguidor_id,
        seguir=seguir.seguir,
    )

    db.add(db_seguir)
    db.commit()
    db.refresh(db_seguir)

    return db_seguir


def delete_seguir(
    db: Session,
    seguido_id: int,
    seguidor_id: int,
):

    db_seguir = db.query(models.Seguir)\
        .filter(models.Seguir.seguido_id == seguido_id)\
        .filter(models.Seguir.seguidor_id == seguidor_id)\
        .first()

    if not db_seguir:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="Relação não encontrada."
        )
    db.delete(db_seguir)
    db.commit()
    return db_seguir
