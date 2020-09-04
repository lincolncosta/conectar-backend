from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t

from db import models
from . import schemas
from app.core.security.passwords import get_password_hash


def get_pessoa(db: Session, pessoa_id: int) -> schemas.Pessoa:
    pessoa = db.query(models.Pessoa)\
        .filter(models.Pessoa.id == pessoa_id).first()
    if not pessoa:
        raise HTTPException(status_code=404, detail="pessoa não encontrada")
    return pessoa


def get_pessoa_by_email(db: Session, email: str) -> schemas.Pessoa:
    return db.query(models.Pessoa).filter(models.Pessoa.email == email).first()


def get_pessoa_by_username(db: Session, usuario: str) -> schemas.Pessoa:
    return db.query(models.Pessoa).filter(models.Pessoa.usuario == usuario)\
        .first()


def get_pessoas(
    db: Session, skip: int = 0, limit: int = 100
) -> t.List[schemas.PessoaOut]:
    return db.query(models.Pessoa).offset(skip).limit(limit).all()


def create_pessoa(db: Session, pessoa: schemas.PessoaCreate) -> schemas.Pessoa:
    password = get_password_hash(pessoa.senha)
    try:
        db_pessoa = models.Pessoa(
            nome=pessoa.nome,
            email=pessoa.email,
            telefone=pessoa.telefone,
            usuario=pessoa.usuario,
            ativo=pessoa.ativo,
            superusuario=pessoa.superusuario,
            senha=password,
            data_nascimento=pessoa.data_nascimento
        )
    except Exception as e:
        print(e)
    db.add(db_pessoa)
    db.commit()
    db.refresh(db_pessoa)
    return db_pessoa


def delete_pessoa(db: Session, pessoa_id: int):
    pessoa = get_pessoa(db, pessoa_id)
    if not pessoa:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="pessoa não encontrada")
    db.delete(pessoa)
    db.commit()
    return pessoa


def edit_pessoa(
    db: Session, pessoa_id: int, pessoa: schemas.PessoaEdit
) -> schemas.Pessoa:
    '''
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
    '''
    db_pessoa = get_pessoa(db, pessoa_id)
    if not db_pessoa:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="pessoa não encontrada")
    update_data = pessoa.dict(exclude_unset=True)

    if "senha" in update_data:
        update_data["senha"] = get_password_hash(pessoa.senha)
        del update_data["senha"]

    for key, value in update_data.items():
        setattr(db_pessoa, key, value)

    db.add(db_pessoa)
    db.commit()
    db.refresh(db_pessoa)
    return db_pessoa
