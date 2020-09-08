from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t

from app.db import models
from . import schemas
from app.core.security import get_password_hash


def get_projeto(db: Session, projeto_id: int):
    projeto = db.query(models.Projeto)\
        .filter(models.Projeto.id == projeto_id).first()
    if not projeto:
        raise HTTPException(status_code=404, detail="projeto não encontrada")
    return projeto

def get_projetos(
    db: Session, skip: int = 0, limit: int = 100
) -> t.List[schemas.ProjetoOut]:
    return db.query(models.Projeto).offset(skip).limit(limit).all()

def create_projeto(db: Session, projeto: schemas.ProjetoCreate):
    try:
        db_projeto = models.Projeto(
            nome=projeto.nome,
            descricao=projeto.descricao,
            visibilidade=projeto.visibilidade
        )
    except Exception as e:
        print(e)
    db.add(db_projeto)
    db.commit()
    db.refresh(db_projeto)
    return db_projeto    

def delete_projeto(db: Session, projeto_id: int):
    projeto = get_projeto(db, projeto_id)
    if not projeto:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="projeto não encontrada")
    db.delete(projeto)
    db.commit()
    return projeto