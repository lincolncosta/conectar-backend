from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t

from . import models, schemas
from app.core.security import get_password_hash


def get_pessoa(db: Session, pessoa_id: int):
    pessoa = db.query(models.Pessoa)\
        .filter(models.Pessoa.id == pessoa_id).first()
    if not pessoa:
        raise HTTPException(status_code=404, detail="pessoa not found")
    return pessoa


def get_pessoa_by_email(db: Session, email: str) -> schemas.PessoaBase:
    return db.query(models.Pessoa).filter(models.Pessoa.email == email).first()


def get_pessoa_by_username(db: Session, username: str) -> schemas.PessoaBase:
    return db.query(models.Pessoa).filter(models.Pessoa.username == username)\
        .first()


def get_pessoas(
    db: Session, skip: int = 0, limit: int = 100
) -> t.List[schemas.PessoaOut]:
    return db.query(models.Pessoa).offset(skip).limit(limit).all()


def create_pessoa(db: Session, pessoa: schemas.PessoaCreate):
    password = get_password_hash(pessoa.password)
    db_pessoa = models.Pessoa(
        nome=pessoa.nome,
        email=pessoa.email,
        telefone=pessoa.telefone,
        username=pessoa.username,
        is_active=pessoa.is_active,
        is_superuser=pessoa.is_superuser,
        password=password,
    )
    db.add(db_pessoa)
    db.commit()
    db.refresh(db_pessoa)
    return db_pessoa


def delete_pessoa(db: Session, pessoa_id: int):
    pessoa = get_pessoa(db, pessoa_id)
    if not pessoa:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="pessoa not found")
    db.delete(pessoa)
    db.commit()
    return pessoa


def edit_pessoa(
    db: Session, pessoa_id: int, pessoa: schemas.PessoaEdit
) -> schemas.Pessoa:
    db_pessoa = get_pessoa(db, pessoa_id)
    if not db_pessoa:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="pessoa not found")
    update_data = pessoa.dict(exclude_unset=True)

    if "password" in update_data:
        update_data["password"] = get_password_hash(pessoa.password)
        del update_data["password"]

    for key, value in update_data.items():
        setattr(db_pessoa, key, value)

    db.add(db_pessoa)
    db.commit()
    db.refresh(db_pessoa)
    return db_pessoa
