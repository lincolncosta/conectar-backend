from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql import select, func
import typing as t

from db import models
from db.utils.extract_areas import append_areas
from db.utils.extract_habilidade import append_habilidades
from . import schemas
from core.security.passwords import get_password_hash


def get_rand_pessoas(
    db: Session,
    qtde: dict
    ) -> t.List[schemas.Pessoa]:

    '''
        Busca Pessoas aleatoriamente baseado no tipo de papel

        Entrada: dict {papel: quantidade}

        Saída: Lista de Esquemas de Pessoas 

        Exceções: Papel não encontrado
                : Pessoas não Encontradas
    '''

    for key in qtde:
        if key == "aliado":
            pessoasAliado = db.query(models.Pessoa)\
                .filter(models.Pessoa.aliado == True)\
                .order_by(func.random())\
                .limit(qtde[key])\
                .all()
        elif key == "colaborador":
            pessoasColab = db.query(models.Pessoa)\
                .filter(models.Pessoa.colaborador == True)\
                .order_by(func.random())\
                .limit(qtde[key])\
                .all()
        else:
            raise HTTPException(status_code=404, detail="papel não encontrado")

    pessoas = pessoasAliado + pessoasColab

    if not pessoas:
        raise HTTPException(status_code=404, detail="pessoas não encontradas")

    return pessoas


def get_pessoa_by_id(
    db: Session,
    pessoa_id: int
    ) -> schemas.PessoaOut:

    '''
        Busca pessoa pelo ID

        Entrada: ID

        Saída: Esquema da Pessoa referente

        Exceções: Não existe Pessoa correspondente ao ID inserido
    '''

    pessoa = db.query(models.Pessoa)\
        .filter(models.Pessoa.id == pessoa_id)\
        .first()
    
    if not pessoa:
        raise HTTPException(status_code=404, detail="pessoa não encontrada")

    return pessoa


def get_pessoa_by_email(
    db: Session,
    email: str
    ) -> schemas.Pessoa:

    '''
        Busca pessoa pelo email exatamente como digitado

        Entrada: string

        Saída: Esquema da Pessoa referente

        Exceções: Não existe Pessoa correspondente ao email inserido
    '''

    pessoa = db.query(models.Pessoa)\
        .filter(models.Pessoa.email == email)\
        .first()

    return pessoa


def get_pessoa_by_username(
    db: Session,
    usuario: str
    ) -> schemas.Pessoa:
    
    '''
        Busca pessoa pelo usuário exatamente como digitado

        Entrada: string

        Saída: Esquema da Pessoa referente

        Exceções: Não existe Pessoa correspondente ao email inserido
    '''

    pessoa = db.query(models.Pessoa)\
        .filter(models.Pessoa.usuario == usuario)\
        .first()

    return pessoa


def get_pessoas(
    db: Session,
    skip: int = 0,
    limit: int = 100
    ) -> t.List[schemas.Pessoa]:

    '''
        Busca todas as pessoas

        Entrada:

        Saída: Lista de Esquemas de Pessoas

        Exceções: 
    '''

    pessoas = db.query(models.Pessoa)\
        .offset(skip)\
        .limit(limit)\
        .all()

    return pessoas


def get_pessoas_by_papel(
    db: Session,
    papel_id: int,
    pessoas_selecionadas_ids: t.List[int]
    ) -> t.List[schemas.Pessoa]:

    '''
        Busca pessoas pelo papel

        Entrada: ID 

        Saída: Lista de Esquemas da Pessoa referente

        Exceções:
    '''

    # Refatorar futuramente para não utilizarmos números fixos no código.
    if (papel_id == 36):
        return db.query(models.Pessoa)\
            .filter(models.Pessoa.aliado == True)\
            .filter(models.Pessoa.id.notin_(pessoas_selecionadas_ids))\
            .filter((models.Area != '') | (models.Habilidades != ''))\
            .join(models.Habilidades, models.Pessoa.habilidades, full=True, isouter=True)\
            .join(models.Area, models.Pessoa.areas, full=True, isouter=True)\
            .order_by(func.random())\
            .distinct()
    elif (papel_id == 37):
        return db.query(models.Pessoa)\
            .filter(models.Pessoa.colaborador == True)\
            .filter(models.Pessoa.id.notin_(pessoas_selecionadas_ids))\
            .filter((models.Area != '') | (models.Habilidades != ''))\
            .join(models.Habilidades, models.Pessoa.habilidades, full=True, isouter=True)\
            .join(models.Area, models.Pessoa.areas, full=True, isouter=True)\
            .order_by(func.random())\
            .distinct()
    elif (papel_id == 38):
        return db.query(models.Pessoa)\
            .filter(models.Pessoa.idealizador == True)\
            .filter(models.Pessoa.id.notin_(pessoas_selecionadas_ids))\
            .filter((models.Area != '') | (models.Habilidades != ''))\
            .join(models.Habilidades, models.Pessoa.habilidades, full=True, isouter=True)\
            .join(models.Area, models.Pessoa.areas, full=True, isouter=True)\
            .order_by(func.random())\
            .distinct()


def create_pessoa(
    db: Session,
    pessoa: schemas.PessoaCreate
    ) -> schemas.Pessoa:
    
    '''
        Cria pessoa

        Entrada: Esquema de Pessoa

        Saída: Esquema da Pessoa Criada

        Exceções:
    '''
    
    password = get_password_hash(pessoa.senha)

    db_pessoa = models.Pessoa(
        nome=pessoa.nome,
        email=pessoa.email,
        telefone=pessoa.telefone,
        usuario=pessoa.usuario,
        ativo=pessoa.ativo,
        superusuario=pessoa.superusuario,
        senha=password,
        data_nascimento=pessoa.data_nascimento,
        foto_perfil=pessoa.foto_perfil,
        colaborador=pessoa.colaborador,
        aliado=pessoa.aliado,
        idealizador=pessoa.idealizador,
    )

    db.add(db_pessoa)
    db.commit()
    db.refresh(db_pessoa)

    return db_pessoa


def delete_pessoa(
    db: Session,
    pessoa_id: int
    ):

    '''
        Apaga pessoa existente

        Entrada: ID

        Saída: Esquema da Pessoa deletada

        Exceções: Pessoa não encontrada
    '''

    pessoa = get_pessoa_by_id(db, pessoa_id)
    
    db.delete(pessoa)
    db.commit()

    return pessoa


async def edit_pessoa(
    db: Session,
    pessoa_id: int,
    pessoa: schemas.PessoaEdit
    ) -> schemas.Pessoa:

    '''
        Edita pessoa já existente

        Entrada: ID, esquema de pessoa

        Saída: Esquema da Pessoa Editada

        Exceções: Pessoa não encontrada
                : Email já cadastrado
    '''

    db_pessoa = get_pessoa_by_id(db, pessoa_id)
    
    update_data = pessoa.dict(exclude_unset=True)

    if "senha" in update_data.keys():
        update_data["senha"] = get_password_hash(pessoa.senha)
        del update_data["senha"]
    if "email" in update_data.keys():
        filtro = get_pessoa_by_email(db, update_data["email"])
        if filtro:
            raise HTTPException(status_code=409, detail="Email já cadastrado")

    await append_areas(update_data, db)
    await append_habilidades(update_data, db)

    for key, value in update_data.items():
        setattr(db_pessoa, key, value)

    db.add(db_pessoa)
    db.commit()
    db.refresh(db_pessoa)

    return db_pessoa
