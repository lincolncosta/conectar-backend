from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t

from db import models
from db.habilidade import schemas


def get_habilidade_by_id( 
    db: Session,
    habilidades_id: int
    ) -> schemas.Habilidades:

    '''
        Busca habilidade pelo ID

        Entrada: ID

        Saída: Esquema da Habilidade referente

        Exceções: Não existe Habilidade correspondente ao ID inserido
    '''

    habilidades = db.query(models.Habilidades)\
        .filter(models.Habilidades.id == habilidades_id)\
        .first()

    if not habilidades:
        raise HTTPException(status_code=404, detail="Habilidade não encontrada")

    return habilidades


def get_habilidade_by_name(
    db: Session,
    habilidades_name: str
    ) -> schemas.Habilidades:

    '''
        Busca habilidade com nome exatamente igual à string buscada

        Entrada: string

        Saída: Lista de Esquemas da Habilidade correspondente

        Exceções: Não existe Habilidade correspondente à string inserida
    '''

    habilidades = db.query(models.Habilidades)\
            .filter(models.Habilidades.nome == habilidades_name)\
            .first()
    
    if not habilidades:
        raise HTTPException(status_code=404, detail="habilidades não encontrada")

    return habilidades


def get_habilidades(
    db: Session,
    skip: int = 0,
    limit: int = 100
    ) -> t.List[schemas.Habilidades]:

    '''
        Busca todas as Habilidades

        Entrada: 

        Saída: Lista com todas as Habilidades cadastradas

        Exceções: 
    '''

    habilidades = db.query(models.Habilidades)\
        .offset(skip)\
        .limit(limit)\
        .all()

    return habilidades


def create_habilidades(
    db: Session,
    habilidades: schemas.Habilidades
    ):

    '''
        Cria uma nova Habilidade

        Entrada: Esquema de Habilidade

        Saída: Esquema da Habilidade Criada

        Exceções: Habilidade já cadastrada
    '''

    filtro = db.query(models.Habilidades)\
        .filter(models.Habilidades.nome == habilidades.nome)\
        .first()
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


def delete_habilidades(
    db: Session,
    habilidades_id: int
    ):

    '''
        Apaga uma habilidade existente

        Entrada: ID

        Saída: Esquema da habilidade Deletada

        Exceções: Habilidade não encontrada
    '''

    habilidades = get_habilidade_by_id(db, habilidades_id)

    db.delete(habilidades)
    db.commit()

    return habilidades


def edit_habilidades(
    db: Session,
    habilidades_id: int,
    habilidades: schemas.HabilidadesEdit
    ) -> schemas.Habilidades:
    
    '''
        Edita uma habilidade existente

        Entrada: ID, esquema de habilidade a ser editada

        Saída: Esquema da habilidade editada

        Exceções: Habilidade não encontrada
                : Habilidade já cadastrada
    '''

    db_habilidades = get_habilidade_by_id(db, habilidades_id)
    
    update_data = habilidades.dict(exclude_unset=True)

    filtro = db.query(models.Habilidades)\
        .filter(models.Habilidades.nome == update_data["nome"])\
        .first()

    if filtro:
        raise HTTPException(status_code=409, detail="Habilidade já cadastrada")

    for key, value in update_data.items():
        setattr(db_habilidades, key, value)

    db.add(db_habilidades)
    db.commit()
    db.refresh(db_habilidades)

    return db_habilidades
