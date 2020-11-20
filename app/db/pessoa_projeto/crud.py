from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t

from db import models
from . import schemas
from db.pessoa.crud import get_pessoa
from db.projeto.crud import get_projeto

def get_pessoa_projeto(db: Session, pessoa_projeto_id: int) -> schemas.PessoaProjeto:
    
    pessoa_projeto = (
        db.query(models.PessoaProjeto)\
            .filter(models.PessoaProjeto.id == pessoa_projeto_id).first()
    )
    if not pessoa_projeto:
        raise HTTPException(status_code=404, detail="pessoa_projeto não encontrada")
    
    return pessoa_projeto


def get_pessoa_projeto_by_projeto(db: Session, id_projeto: int) -> schemas.PessoaProjeto:
    pessoa_projeto = db.query(models.PessoaProjeto)\
        .filter(models.Projeto.id == id_projeto).all()
    

    if not pessoa_projeto:
        raise HTTPException(status_code=404, detail="pessoa_projetos não encontradas")
    return pessoa_projeto


async def create_pessoa_projeto(
    db: Session,
    pessoa_projeto: schemas.PessoaProjetoCreate
    ) -> schemas.PessoaProjeto:

    try:
        projeto = get_projeto(db, pessoa_projeto.projeto)
        if pessoa_projeto.pessoa:
            pessoa = get_pessoa(db, pessoa_projeto.pessoa.id)

            db_pessoa_projeto = models.PessoaProjeto(
            pessoa=pessoa,
            projeto=projeto,
            descricao=pessoa_projeto.descricao,
            situacao=pessoa_projeto.situacao
    )
        else:
            db_pessoa_projeto = models.PessoaProjeto(
            projeto=projeto,
            descricao=pessoa_projeto.descricao,
            situacao=pessoa_projeto.situacao,
        )
    
    except HTTPException as e:
        raise e

    
    db.add(db_pessoa_projeto)
    db.commit()
    db.refresh(db_pessoa_projeto)

    db_vaga = db_pessoa_projeto.__dict__
    return {"id": db_vaga["id"]}


async def edit_pessoa_projeto(db: Session, pessoa_projeto_id: int,
    pessoa_projeto: schemas.PessoaProjetoEdit) -> schemas.PessoaProjeto:

    db_pessoa_projeto = get_pessoa_projeto(db, pessoa_projeto_id)
    if not db_pessoa_projeto:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="pessoa_projeto não encontrada"
        )
    update_data = pessoa_projeto.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_pessoa_projeto, key, value)

    db.add(db_pessoa_projeto)
    db.commit()
    db.refresh(db_pessoa_projeto)
    return db_pessoa_projeto
