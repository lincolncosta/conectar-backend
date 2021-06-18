from fastapi import HTTPException
from sqlalchemy.orm import Session
import typing as t

from app.db import models
from app.db.area import schemas as schemas_areas
from app.db.habilidade import schemas as schemas_habilidades

def search_area_by_name(
    db: Session,
    area_nome: str,
    ) -> t.List[schemas_areas.Area]:

    '''
        Busca Áreas que contenham a string inserida

        Entrada: string

        Saída: Lista de Esquemas da Área correspondente

        Exceções: Não existe Área correspondente à string inserida
    '''

    area = db.query(models.Area)\
        .filter(models.Area.descricao.ilike(f'%{area_nome}%'))\
        .all()
    
    if not area:
        raise HTTPException(status_code=404, detail="area não encontrada")
        
    return area


def search_habilidade_by_name(
    db: Session,
    habilidade_nome: str,
    ) -> t.List[schemas_habilidades.Habilidades]:

    '''
        Busca Habilidades que contenham a string inserida

        Entrada: string

        Saída: Lista de Esquemas da Habilidades correspondente

        Exceções: Não existe Habilidades correspondente à string inserida
    '''

    habilidade = db.query(models.Habilidades)\
        .filter(models.Habilidades.nome.ilike(f'%{habilidade_nome}%'))\
        .all()
    
    if not habilidade:
        raise HTTPException(status_code=404, detail="habilidade não encontrada")
        
    return habilidade