from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t

from app.db import models
from app.db.papel import schemas


def get_papel_by_id(db: Session, papel_id: int) -> schemas.Papel:
    papel = db.query(models.Papel).filter(models.Papel.id == papel_id).first()

    if not papel:
        raise HTTPException(status_code=404, detail="papel não encontrado")
    return papel


def get_papel(
    db: Session, skip: int = 0, limit: int = 100
) -> t.List[schemas.Papel]:
    return db.query(models.Papel).offset(skip).limit(limit).all()


def create_papel(db: Session, papel: schemas.Papel):
    try:
        db_papel = models.Papel(
            descricao=papel.descricao,
        )
    except Exception as e:
        print("CORRIGIR FUTURAMENTE. Exceção encontrada:", e)
    db.add(db_papel)
    db.commit()
    db.refresh(db_papel)
    return db_papel


def delete_papel(db: Session, papel_id: int):
    papel = get_papel_by_id(db, papel_id)
    if not papel:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="papel não encontrado",
        )
    db.delete(papel)
    db.commit()
    return papel


def edit_papel(
    db: Session, papel_id, papel: schemas.PapelEdit
) -> schemas.Papel:
    """
    Edits experiencia on database.

    Tries to find the experience in the database, if it finds, updates each field
    that was send with new information to the database.

    Args:
        db: Database Local Session. sqlalchemy.orm.sessionmaker instance.
        experiencia_id: Integer representing the experiencia id. Integer.
        experiencia: New data to use on update of experienciaAcad. Schema from ExperienciaAcadEdit.

    Returns:
        A dict of experiencia with the updated values. For example:
        old_experiencia: {
            id: 1,
            descricao: "uma descrição"
        }
        db_experiencia: {
            id: 1,
            descricao: "Uma nova descrição"
        }

    Raises:
        HTTPException: No experience corresponds to experiencia_id in the database.
    """
    db_papel = get_papel_by_id(db, papel_id)
    if not db_papel:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="papel não encontrado",
        )
    update_data = papel.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_papel, key, value)

    db.add(db_papel)
    db.commit()
    db.refresh(db_papel)
    return db_papel
