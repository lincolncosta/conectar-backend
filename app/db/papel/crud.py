from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t

from app.db import models
from app.db.papel import schemas


def get_papel_by_id(
    db: Session,
    papel_id: int
    ) -> schemas.Papel:

    '''
        Busca um papel a partir do ID da mesma

        Entrada: ID

        Saída: Esquema do papel correspondente

        Exceções: Não existe papel correspondente ao ID inserido
    '''

    papel = db.query(models.Papel)\
        .filter(models.Papel.id == papel_id)\
        .first()

    if not papel:
        raise HTTPException(status_code=404, detail="papel não encontrado")

    return papel


def get_papel(
    db: Session,
    skip: int = 0,
    limit: int = 100
    ) -> t.List[schemas.Papel]:

    '''
        Busca todos os papeis

        Entrada:

        Saída: Lista de Esquemas de Papeis

        Exceções:
    '''

    return db.query(models.Papel).offset(skip).limit(limit).all()


def create_papel(
    db: Session,
    papel: schemas.Papel
    ):

    '''
        Cria um papel

        Entrada: Esquema de papel

        Saída: Esquema do papel criado

        Exceções: 
    '''

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


def delete_papel(
    db: Session,
    papel_id: int
    ):

    '''
        Apaga um papel existente

        Entrada: ID

        Saída: Esquema do papel Deletado

        Exceções: Papel não encontrado
    '''

    papel = get_papel_by_id(db, papel_id)
    
    db.delete(papel)
    db.commit()

    return papel


def edit_papel(
    db: Session,
    papel_id,
    papel: schemas.PapelEdit
    ) -> schemas.Papel:

    '''
        Edita um papel existente

        Entrada: ID, Esquema de papel a ser editado

        Saída: Esquema do papel Editado

        Exceções: Papel não encontrado
    '''

    db_papel = get_papel_by_id(db, papel_id)
    
    update_data = papel.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_papel, key, value)

    db.add(db_papel)
    db.commit()
    db.refresh(db_papel)
    return db_papel
