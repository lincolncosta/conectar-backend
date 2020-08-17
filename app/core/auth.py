import jwt
from fastapi import Depends, HTTPException, status
from jwt import PyJWTError

from app.db import models, schemas, session
from app.db.crud import get_pessoa_by_email, create_pessoa, get_pessoa_by_username
from app.core import security


async def get_current_pessoa(
    db=Depends(session.get_db), token: str = Depends(security.oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, security.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        permissions: str = payload.get("permissions")
        token_data = schemas.TokenData(email=email, permissions=permissions)
    except PyJWTError:
        raise credentials_exception
    pessoa = get_pessoa_by_email(db, token_data.email)
    if pessoa is None:
        raise credentials_exception
    return pessoa


async def get_current_active_pessoa(
    current_pessoa: models.Pessoa = Depends(get_current_pessoa),
):
    if not current_pessoa.is_active:
        raise HTTPException(status_code=400, detail="Inactive pessoa")
    return current_pessoa


async def get_current_active_superuser(
    current_pessoa: models.Pessoa = Depends(get_current_pessoa),
) -> models.Pessoa:
    if not current_pessoa.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_pessoa


def authenticate_pessoa(db, email: str, password: str):
    pessoa = get_pessoa_by_email(db, email)
    pessoa_username = get_pessoa_by_username(db, email)

    if not pessoa:
        if not pessoa_username:
            return False
        if not security.verify_password(password, pessoa_username.password):
            return False
        else:
            return pessoa_username
    if not security.verify_password(password, pessoa.password):
        return False
    return pessoa


def sign_up_new_pessoa(db, email: str, password: str, telefone: str, nome: str, username: str):
    pessoa = get_pessoa_by_email(db, email)
    pessoa_username = get_pessoa_by_username(db, username)

    if pessoa and pessoa_username:
        return False  # Pessoa already exists
    new_pessoa = create_pessoa(
        db,
        schemas.PessoaCreate(
            email=email, telefone=telefone, nome=nome, username=username,
            password=password, is_active=True, is_superuser=False,
        ),
    )
    return new_pessoa
