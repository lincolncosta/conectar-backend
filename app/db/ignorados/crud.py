from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t

from app.db import models
from app.db.ignorados import schemas


def get_pessoa_ignorada_by_id(
    db: Session,
    pessoa_ignorada_id: int
    ) -> schemas.PessoaIgnoradaVaga:

    '''
        Busca um pessoa_ignorada a partir do ID da mesma

        Entrada: ID

        Saída: Esquema do pessoa_ignorada correspondente

        Exceções: Não existe pessoa_ignorada correspondente ao ID inserido
    '''

    pessoa_ignorada = db.query(models.PessoaIgnoradaVaga)\
        .filter(models.PessoaIgnoradaVaga.id == pessoa_ignorada_id)\
        .first()

    if not pessoa_ignorada:
        raise HTTPException(status_code=404, detail="pessoa_ignorada não encontrado")

    return pessoa_ignorada


def get_ids_pessoa_ignorada_by_vaga(
    db: Session,
    pessoa_projeto_id: int
    ) -> t.List[int]:

    pessoas_ignoradas_ids = db.query(models.PessoaIgnoradaVaga.pessoa_id)\
        .filter(models.PessoaIgnoradaVaga.pessoa_projeto_id == pessoa_projeto_id)\
        .all()

    return pessoas_ignoradas_ids

def get_ids_pessoa_ignorada_by_vagas(
    db: Session,
    pessoa_projeto_ids: t.List[int]
    ) -> t.List[int]:

    pessoas_ignoradas_ids = db.query(models.PessoaIgnoradaVaga.pessoa_id)\
        .filter(models.PessoaIgnoradaVaga.pessoa_projeto_id.in_(pessoa_projeto_ids))\
        .all()

    return pessoas_ignoradas_ids
    

def get_pessoas_ignoradas_by_vaga(
    db: Session,
    pessoa_projeto_id: int
    ) -> t.List[schemas.PessoaIgnoradaVaga]:

    pessoas_ignoradas = db.query(models.PessoaIgnoradaVaga)\
        .filter(models.PessoaIgnoradaVaga.pessoa_projeto_id == pessoa_projeto_id)\
        .all()

    return pessoas_ignoradas


def add_pessoa_ignorada(
    db: Session,
    pessoa_id: int,
    pessoa_projeto_id: int
    ):

    '''
        Adiciona uma pessoa_ignorada ao banco

        Entrada: pessoa_id, pessoa_projeto_id

        Saída: Esquema da pessoa_ignorada criada

        Exceções: 
    '''

    db_pessoa_ignorada = db.query(models.PessoaIgnoradaVaga)\
        .filter(models.PessoaIgnoradaVaga.pessoa_id == pessoa_id)\
        .filter(models.PessoaIgnoradaVaga.pessoa_projeto_id == pessoa_projeto_id)\
        .first()

    if not db_pessoa_ignorada:
        db_pessoa_ignorada = models.PessoaIgnoradaVaga(
            pessoa_id = pessoa_id,
            pessoa_projeto_id = pessoa_projeto_id
        )
    
        db.add(db_pessoa_ignorada)
        db.commit()
        db.refresh(db_pessoa_ignorada)

    return db_pessoa_ignorada


def delete_pessoas_ignoradas_by_vaga(
    db: Session,
    pessoa_projeto_id: int
    ):

    '''
        Apaga uma pessoa_ignorada

        Entrada: ID

        Saída: Esquema da pessoa_ignorada deletada

        Exceções: pessoa_ignorada não encontrada
    '''

    pessoas_ignoradas = get_pessoas_ignoradas_by_vaga(db, pessoa_projeto_id)
    
    for pessoa_ignorada in pessoas_ignoradas:
        db.delete(pessoa_ignorada)
        db.commit()

    return pessoas_ignoradas
