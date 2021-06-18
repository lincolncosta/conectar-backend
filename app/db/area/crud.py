from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from db import models
from . import schemas

async def get_area_by_id(
    db: Session,
    area_id: int
    ) -> schemas.Area:

    '''
        Busca uma Área a partir do ID da mesma

        Entrada: ID

        Saída: Esquema da Área correspondente

        Exceções: Não existe Área correspondente ao ID inserido
    '''

    area = db.query(models.Area)\
        .filter(models.Area.id == area_id)\
        .first()
    if not area:
        raise HTTPException(status_code=404, detail="area não encontrada")
    return area


async def get_area_by_name(
    db: Session,
    area_name: str
    ) -> schemas.Area:

    '''
        Busca Área cujo nome seja exatamente igual à string inserida

        Entrada: string

        Saída: Lista de Esquemas da Área correspondente

        Exceções: Não existe Área correspondente à string inserida
    '''

    area = db.query(models.Area)\
        .filter(models.Area.descricao == area_name)\
        .first()
    
    if not area:
        raise HTTPException(status_code=404, detail="area não encontrada")
        
    return area


async def get_area_and_subareas(
    db: Session,
    area_id: int
    ):

    '''
        Busca uma Área e todas as suas subareas a partir do ID buscado

        Entrada: ID

        Saída: Dicionário contendo área pai e suas subareas

        Exceções: Não existe Área correspondente ao ID inserido
    '''
    
    area = await get_area_by_id(db, area_id)
    if not area:
        raise HTTPException(status_code=404, detail="area não encontrada")

    subareas = db.query(models.Area)\
        .filter(models.Area.area_pai_id == area_id)\
        .all()
    
    area_and_subareas = {"area": area, "subareas": subareas}

    return area_and_subareas

async def get_areas(
    db: Session
    ):

    '''
        Busca todas as Áreas e subareas

        Entrada: 

        Saída: Lista com todas as áreas e subáreas cadastradas

        Exceções:
    '''

    areas = db.query(models.Area)\
        .filter(models.Area.area_pai_id == None)\
        .all()
        
    areasAndSubareas = [await get_area_and_subareas(db, area.id) for area in areas]
                
    return areasAndSubareas


async def create_area(
    db: Session,
    area: schemas.AreaCreate
    ) -> schemas.Area:

    '''
        Cria uma nova área

        Entrada: Esquema de Area

        Saída: Esquema da Area Criada

        Exceções: Area já existe
                : Area pai não encontrada
    '''

    filtro = db.query(models.Area)\
        .filter(models.Area.descricao == area.descricao)\
        .first()
    if filtro:
        raise HTTPException(status_code=409, detail="Area já cadastrada")

    try:
        if area.area_pai_id:
            area_pai = await get_area_by_id(db, area.area_pai_id)
    except HTTPException:
        raise HTTPException(status_code=400, detail="area pai não encontrada")

    db_area = models.Area(
          descricao=area.descricao,
          area_pai_id=area.area_pai_id
    )

    db.add(db_area)
    db.commit()
    db.refresh(db_area)

    return db_area


async def delete_area(
    db: Session,
    area_id: int
    ):

    '''
        Apaga uma área existente

        Entrada: ID

        Saída: Esquema da Area Deletada

        Exceções: Area não encontrada
    '''

    area = await get_area_by_id(db, area_id)

    db.delete(area)
    db.commit()
    return area


async def edit_area(
    db: Session,
    area_id: int,
    area: schemas.AreaEdit
    ) -> schemas.Area:
    
    '''
        Edita uma área existente

        Entrada: ID, Esquema de area a ser editada

        Saída: Esquema da Area Editada

        Exceções: Area não encontrada
                : Area já Cadastrada
    '''

    db_area = await get_area_by_id(db, area_id)

    update_data = area.dict(exclude_unset=True)

    filtro = db.query(models.Area)\
        .filter(models.Area.descricao == update_data["descricao"])\
        .first()

    if filtro:
        raise HTTPException(status_code=409, detail="Area já cadastrada")

    for key, value in update_data.items():
        setattr(db_area, key, value)

    db.add(db_area)
    db.commit()
    db.refresh(db_area)

    return db_area
