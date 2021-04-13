from fastapi import HTTPException, status, UploadFile
from sqlalchemy.orm import Session
import typing as t

from app.db import models
from app.db.projeto import schemas

def get_projeto_by_name(db: Session, projeto_name: str) -> schemas.Projeto:
    projeto = db.query(models.Projeto)\
        .filter(models.Projeto.nome.ilike(f'%{projeto_name}%')).all()
    if not projeto:
        raise HTTPException(status_code=404, detail="projeto não encontrado")
    return projeto


def get_projeto_by_objective(db: Session, projeto_objective: str) -> schemas.Projeto:
    projeto = db.query(models.Projeto)\
        .filter(models.Projeto.objetivo.ilike(f'%{projeto_objective}%')).all()
    if not projeto:
        raise HTTPException(status_code=404, detail="projeto não encontrado")
    return projeto


def get_projeto_by_area(db: Session, projeto_area: str) -> schemas.Projeto:
    projeto = db.query(models.Projeto)\
        .join(models.Area, models.Projeto.areas)\
            .filter(models.Area.descricao.ilike(f'%{projeto_area}%')).all()
    
    if not projeto:
        raise HTTPException(status_code=404, detail="projeto não encontrado")
    return projeto

def get_projeto_by_habilidade(db: Session, projeto_habilidade: str) -> schemas.Projeto:
    projeto = db.query(models.Projeto)\
        .join(models.Habilidades, models.Projeto.habilidades)\
            .filter(models.Habilidades.nome.ilike(f'%{projeto_habilidade}%')).all()
    
    if not projeto:
        raise HTTPException(status_code=404, detail="projeto não encontrado")
    return projeto
