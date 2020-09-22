from fastapi import HTTPException, status
from sqlalchemy.orm import Session
# import typing as t

from db import models
from app.db.experiencia import schemas


def get_experiencia_by_id(
    db: Session, experiencia_id: int
) -> schemas.ExperienciaAcad:
    experiencia = (
        db.query(models.ExperienciaAcad)
        .filter(models.ExperienciaAcad.id == experiencia_id)
        .first()
    )
    if not experiencia:
        raise HTTPException(
            status_code=404, detail="Experiencia Academica não encontrada"
        )
    return experiencia


def get_experiencias_from_pessoa(
    db: Session, pessoa_id: int
) -> schemas.ExperienciaAcad:
    experiencias = (
        db.query(models.ExperienciaAcad)
        .filter(models.ExperienciaAcad.pessoa_id == pessoa_id)
        .all()
    )
    if not experiencias:
        raise HTTPException(
            status_code=404,
            detail="Pessoa não possui experiências Academicas",
        )
    return experiencias


def create_experiencia(
    db: Session, experiencia: schemas.ExperienciaAcad, pessoa_id: int
):
    try:
        db_experiencia_prof = models.ExperienciaAcad(
            escolaridade=experiencia.escolaridade,
            data_fim=experiencia.data_fim,
            data_inicio=experiencia.data_inicio,
            descricao=experiencia.descricao,
            instituicao=experiencia.instituicao,
            pessoa_id=pessoa_id,
        )
    except Exception as e:
        print('CORRIGIR FUTURAMENTE. Exceção encontrada:', e)
    db.add(db_experiencia_prof)
    db.commit()
    db.refresh(db_experiencia_prof)
    return db_experiencia_prof


def delete_experiencia(db: Session, experiencia_id: int):
    experiencia = get_experiencia_by_id(db, experiencia_id)
    if not experiencia:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="experiencia academica não encontrada",
        )
    db.delete(experiencia)
    db.commit()
    return experiencia


def edit_experiencia(
    db: Session, experiencia_id, experiencia: schemas.ExperienciaAcadEdit
) -> schemas.ExperienciaAcad:
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
    db_experiencia = get_experiencia_by_id(db, experiencia_id)
    if not db_experiencia:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="experiencia academica não encontrada",
        )
    update_data = experiencia.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_experiencia, key, value)

    db.add(db_experiencia)
    db.commit()
    db.refresh(db_experiencia)
    return db_experiencia
