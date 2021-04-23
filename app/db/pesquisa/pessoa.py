from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t

from app.db import models
from app.db.pessoa import schemas
from app.core.security.passwords import get_password_hash 

def get_pessoa_by_name(db: Session, pessoa_name: str) -> schemas.Pessoa:

    '''
        Search a user by name 
    '''

    pessoa = db.query(models.Pessoa)\
        .filter(models.Pessoa.nome.ilike(f'%{pessoa_name}%')).all()
    if not pessoa:
        raise HTTPException(status_code=404, detail="pessoa não encontrado")
    return pessoa

def get_pessoa_by_area(db: Session, pessoa_area: str) -> schemas.Pessoa:
    
    '''
        Search a user by areas  
    '''
    
    pessoa = db.query(models.Pessoa)\
        .join(models.Area, models.Pessoa.areas)\
            .filter(models.Area.descricao.ilike(f'%{pessoa_area}%')).all()
    
    if not pessoa:
        raise HTTPException(status_code=404, detail="pessoa não encontrado")
    return pessoa

def get_pessoa_by_habilidade(db: Session, pessoa_habilidade: str) -> schemas.Pessoa:

    '''
        Search a user by name 
    '''
    pessoa = db.query(models.Pessoa)\
        .join(models.Habilidades, models.Pessoa.habilidades)\
            .filter(models.Habilidades.nome.ilike(f'%{pessoa_habilidade}%')).all()
    
    if not pessoa:
        raise HTTPException(status_code=404, detail="pessoa não encontrado")
    return pessoa
