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
    db: Session, qtde: dict
) -> schemas.Pessoa:

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


def get_pessoa(db: Session, pessoa_id: int) -> schemas.PessoaOut:
    pessoa = (
        db.query(models.Pessoa).filter(models.Pessoa.id == pessoa_id).first()
    )
    if not pessoa:
        raise HTTPException(status_code=404, detail="pessoa não encontrada")
    return pessoa


def get_pessoa_by_email(db: Session, email: str) -> schemas.Pessoa:
    return db.query(models.Pessoa).filter(models.Pessoa.email == email).first()


def get_pessoa_by_username(db: Session, usuario: str) -> schemas.Pessoa:
    return (
        db.query(models.Pessoa).filter(
            models.Pessoa.usuario == usuario).first()
    )


def get_pessoa_by_name(db: Session, pessoa_name: str) -> schemas.Pessoa:
    pessoa = (
        db.query(models.Pessoa)
        .filter(models.Pessoa.nome.ilike(f"{pessoa_name}%"))
        .all()
    )
    if not pessoa:
        raise HTTPException(status_code=404, detail="pessoa não encontrado")
    return pessoa


def get_pessoa_by_area(db: Session, pessoa_area: str) -> schemas.Pessoa:
    pessoa = (
        db.query(models.Pessoa)
        .join(models.Area, models.Pessoa.areas)
        .filter(models.Area.descricao.ilike(f"{pessoa_area}%"))
        .all()
    )

    if not pessoa:
        raise HTTPException(status_code=404, detail="pessoa não encontrado")
    return pessoa


def get_pessoa_by_habilidade(
    db: Session, pessoa_habilidade: str
) -> schemas.Pessoa:
    pessoa = (
        db.query(models.Pessoa)
        .join(models.Habilidades, models.Pessoa.habilidades)
        .filter(models.habilidades.descricao.ilike(f"{pessoa_habilidade}%"))
        .all()
    )

    if not pessoa:
        raise HTTPException(status_code=404, detail="pessoa não encontrado")
    return pessoa


def get_pessoas(
    db: Session, skip: int = 0, limit: int = 100
) -> t.List[schemas.Pessoa]:
    return db.query(models.Pessoa).offset(skip).limit(limit).all()


def get_pessoas_by_papel(db: Session, papel: int, pessoas_selecionadas: t.List[schemas.Pessoa]) -> t.List[schemas.Pessoa]:

    # Refatorar futuramente para não utilizarmos números fixos no código.
    if (papel == 1):
        return db.query(models.Pessoa).filter(models.Pessoa.aliado == True).filter(models.Pessoa.id.notin_(pessoas_selecionadas)).all()
    elif (papel == 2):
        return db.query(models.Pessoa).filter(models.Pessoa.colaborador == True).filter(models.Pessoa.id.notin_(pessoas_selecionadas)).all()
    elif (papel == 3):
        return db.query(models.Pessoa).filter(models.Pessoa.idealizador == True).filter(models.Pessoa.id.notin_(pessoas_selecionadas)).all()


def create_pessoa(db: Session, pessoa: schemas.PessoaCreate) -> schemas.Pessoa:
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


def delete_pessoa(db: Session, pessoa_id: int):
    pessoa = get_pessoa(db, pessoa_id)
    if not pessoa:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="pessoa não encontrada"
        )
    db.delete(pessoa)
    db.commit()
    return pessoa


async def edit_pessoa(
    db: Session, pessoa_id: int, pessoa: schemas.PessoaEdit
) -> schemas.Pessoa:
    """
    Edits pessoa on database.

    Tries to find the person in the database, if it finds, updates each field
    that was send with new information to the database.

    Args:
        db: Database Local Session. sqlalchemy.orm.sessionmaker instance.
        pessoa_id: Integer representing the pessoa id. Integer.
        pessoa: New data to use on update of pessoa. Schema from PessoaEdit.

    Returns:
        A dict of pessoa with the updated values. For example:
        old_pessoa: {
            id: 1,
            nome: "Lucas"
        }
        db_pessoa: {
            id: 1,
            nome: "Luis"
        }

    Raises:
        HTTPException: No person corresponds to pessoa_id in the database.
    """
    db_pessoa = get_pessoa(db, pessoa_id)
    if not db_pessoa:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="pessoa não encontrada"
        )
    update_data = pessoa.dict(exclude_unset=True)

    if "senha" in update_data.keys():
        update_data["senha"] = get_password_hash(pessoa.senha)
        del update_data["senha"]
    if "email" in update_data.keys():
        filtro = db.query(models.Pessoa)\
        .filter(models.Pessoa.email == update_data["email"])\
        .first()
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
