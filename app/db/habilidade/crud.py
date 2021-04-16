from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t

from db import models
from db.habilidade import schemas


def get_habilidades_by_id( 

    db: Session, habilidades_id: int
) -> schemas.Habilidades:
    habilidades = (
        db.query(models.Habilidades)
        .filter(models.Habilidades.id == habilidades_id) 
        .first()
    )

    if not habilidades:
        raise HTTPException(
            status_code=404, detail="Habilidade não encontrada"
        )
    return habilidades

def get_habilidades(db: Session, skip: int = 0, limit: int = 100) -> t.List[schemas.Habilidades]:
    return db.query(models.Habilidades).offset(skip).limit(limit).all()

def get_habilidade_by_name(db: Session, habilidades_name: int) -> t.List[schemas.Habilidades]:
    '''
        Get a single instance of habilidades from its name

        Args:
        db: Database Local Session. sqlalchemy.orm.sessionmaker instance.
        habilidades_name: String representing the habilidades description.

        Returns:
        An habilidades object.

        Raises:
            HTTPException: No habilidades corresponds to the habilidades_id.
    '''
    habilidades = db.query(models.Habilidades)\
            .filter(models.Habilidades.nome.ilike(f'%{habilidades_name}%'))\
            .all()
    
    if not habilidades:
        raise HTTPException(status_code=404, detail="habilidades não encontrada")
    return habilidades

def create_habilidades(db: Session, habilidades: schemas.Habilidades):

    filtro = db.query(models.Habilidades)\
        .filter(models.Habilidades.nome == habilidades.nome).first()
    if filtro:
        raise HTTPException(status_code=409, detail="Habilidade já cadastrada")

    try:
        db_habilidades = models.Habilidades(
            nome=habilidades.nome,
        )
    except Exception as e:
        print('CORRIGIR FUTURAMENTE. Exceção encontrada:', e)
    db.add(db_habilidades)
    db.commit()
    db.refresh(db_habilidades)
    return db_habilidades

def delete_habilidades(db: Session, habilidades_id: int):
    habilidades = get_habilidades_by_id(db, habilidades_id)
    if not habilidades:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="experiencia academica não encontrada",
        )
    db.delete(habilidades)
    db.commit()
    return habilidades

def edit_habilidades(
    db: Session, habilidades_id, habilidades: schemas.HabilidadesEdit
) -> schemas.Habilidades:
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
    db_habilidades = get_habilidades_by_id(db, habilidades_id)
    if not db_habilidades:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="habilidades academica não encontrada",
        )
    update_data = habilidades.dict(exclude_unset=True)

    filtro = db.query(models.Habilidades)\
        .filter(models.Habilidades.nome == update_data["nome"]).first()

    if filtro:
        raise HTTPException(status_code=409, detail="Habilidade já cadastrada")

    for key, value in update_data.items():
        setattr(db_habilidades, key, value)

    db.add(db_habilidades)
    db.commit()
    db.refresh(db_habilidades)
    return db_habilidades
