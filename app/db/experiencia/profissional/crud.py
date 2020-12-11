from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t

from db import models
from db.experiencia import schemas
from db.utils.extract_areas import append_areas


def get_experiencia_by_id(
    db: Session, experiencia_id: int
) -> schemas.ExperienciaProf:
    experiencia = (
        db.query(models.ExperienciaProf)
        .filter(models.ExperienciaProf.id == experiencia_id)
        .first()
    )
    if not experiencia:
        raise HTTPException(
            status_code=404, detail="Experiencia profissional não encontrada"
        )
    return experiencia


def get_experiencias(
    db: Session, skip: int = 0, limit: int = 100
) -> t.List[schemas.ExperienciaProf]:
    return db.query(models.ExperienciaProf).offset(skip).limit(limit).all()


def get_experiencias_from_pessoa(
    db: Session, pessoa_id: int
) -> schemas.ExperienciaProf:
    experiencias = (
        db.query(models.ExperienciaProf)
        .filter(models.ExperienciaProf.pessoa_id == pessoa_id)
        .all()
    )
    if not experiencias:
        raise HTTPException(
            status_code=404,
            detail="Pessoa não possui experiências profissionais",
        )
    return experiencias


async def create_experiencia(
    db: Session, experiencia: schemas.ExperienciaProf, pessoa_id: int
):
    db_experiencia_prof = models.ExperienciaProf(
            cargo=experiencia.cargo,
            data_fim=experiencia.data_fim,
            data_inicio=experiencia.data_inicio,
            descricao=experiencia.descricao,
            organizacao=experiencia.organizacao,
            pessoa_id=pessoa_id,
    )

    db_exp = experiencia.dict(exclude_unset=True)
    await append_areas(db_exp, db)

    for key, value in db_exp.items():
        setattr(db_experiencia_prof, key, value)
    
    db.add(db_experiencia_prof)
    db.commit()
    db.refresh(db_experiencia_prof)
    return db_experiencia_prof


def delete_experiencia(db: Session, experiencia_id: int):
    experiencia = get_experiencia_by_id(db, experiencia_id)
    if not experiencia:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="experiencia profissional não encontrada",
        )
    db.delete(experiencia)
    db.commit()
    return experiencia


async def edit_experiencia(
    db: Session, experiencia_id, experiencia: schemas.ExperienciaProfEdit
) -> schemas.ExperienciaProf:
    """
    Edits experiencia on database.

    Tries to find the experience in the database, if it finds, updates each field
    that was send with new information to the database.

    Args:
        db: Database Local Session. sqlalchemy.orm.sessionmaker instance.
        experiencia_id: Integer representing the experiencia id. Integer.
        experiencia: New data to use on update of experienciaProf. Schema from ExperienciaProfEdit.

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
            detail="experiencia profissional não encontrada",
        )
    update_data = experiencia.dict(exclude_unset=True)

    await append_areas(update_data, db)

    for key, value in update_data.items():
        setattr(db_experiencia, key, value)

    db.add(db_experiencia)
    db.commit()
    db.refresh(db_experiencia)
    return db_experiencia
