import jwt
from fastapi import Depends, HTTPException, status, File, UploadFile
from jwt import PyJWTError

from db.utils.salvar_imagem import store_image
from db import models, session

from db.pessoa import schemas

from db.pessoa.crud import (
    get_pessoa_by_email,
    create_pessoa,
    get_pessoa_by_username,
)
from core.security import handle_jwt, passwords

from typing import Optional

from datetime import date

from google.oauth2 import id_token
from google.auth.transport import requests

from pathlib import Path
from dotenv import load_dotenv
import os

env = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env)


async def get_current_pessoa(
    db=Depends(session.get_db), token: str = Depends(handle_jwt.oauth2_scheme)
):
    """
    Get the current logged in user.

    Validates the jwt token and returns the user data from database.

    Args:
        db: Database Local Session. sqlalchemy.orm.sessionmaker instance
        token: The JWT token using the oauth2_scheme from security.passwords

    Returns:
        A Pessoa object from database. Each object is represented as a
        dict.
        For example:
        {
            id: 1,
            nome: Lucas,
            email: lucas@email.com
        }

    Raises:
        credentials_exception: HTTPException status 401. If token is invalid or is not
        present
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, passwords.ACCESS_TOKEN, algorithms=[
                passwords.ALGORITHM], options={"verify_exp": True}
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        permissions: str = payload.get("permissions")
        token_data = schemas.TokenData(email=email, permissions=permissions)

    except jwt.exceptions.ExpiredSignatureError as expired:
        print("Expired")
        raise credentials_exception
    except PyJWTError as e:
        print(f'PYJWTERROR {e}')
        raise credentials_exception
    pessoa = get_pessoa_by_email(db, token_data.email)
    if pessoa is None:
        raise credentials_exception
    return pessoa


async def get_current_token(
    token: str = Depends(handle_jwt.oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, passwords.ACCESS_TOKEN, algorithms=[
                passwords.ALGORITHM], options={"verify_exp": True}
        )
        return token
        # email: str = payload.get("sub")
        # if email is None:
        #     raise credentials_exception
        # permissions: str = payload.get("permissions")
        # token_data = schemas.TokenData(email=email, permissions=permissions)
    except PyJWTError:
        raise credentials_exception


async def get_current_active_pessoa(
    current_pessoa: models.Pessoa = Depends(get_current_pessoa),
):
    if not current_pessoa.ativo:
        raise HTTPException(status_code=400, detail="Pessoa Inativa")
    return current_pessoa


async def get_current_active_superuser(
    current_pessoa: models.Pessoa = Depends(get_current_pessoa),
) -> models.Pessoa:
    if not current_pessoa.superusuario:
        raise HTTPException(
            status_code=403,
            detail="A pessoa não tem os privilégios necessarios",
        )
    return current_pessoa


async def authenticate_pessoa(db, email: str, senha: str):
    pessoa = get_pessoa_by_email(db, email)
    pessoa_username = get_pessoa_by_username(db, email)

    username_message = {"message": "Nome de usuário incorreto"}
    password_message = {"message": "Senha incorreta"}

    if not pessoa:
        if not pessoa_username:
            return username_message
        if not passwords.verify_password(senha, pessoa_username.senha):
            return password_message
        else:
            return pessoa_username
    if not passwords.verify_password(senha, pessoa.senha):
        return password_message
    return pessoa


async def sign_up_new_pessoa(
    db,
    email: str,
    senha: str,
    usuario: str,
    telefone: Optional[str] = None,
    nome: Optional[str] = None,
    data_nascimento: Optional[date] = None,
    foto_perfil: UploadFile = File(None)
):
    pessoa = get_pessoa_by_email(db, email)
    pessoa_username = get_pessoa_by_username(db, usuario)

    if pessoa or pessoa_username:
        return False  # Pessoa already exists

    path = None
    if foto_perfil:
        contents = await foto_perfil.read()
        path = store_image(contents, foto_perfil.filename)

    new_pessoa = create_pessoa(
        db,
        schemas.PessoaCreate(
            data_nascimento=data_nascimento,
            email=email,
            telefone=telefone,
            nome=nome,
            senha=senha,
            usuario=usuario,
            ativo=True,
            superusuario=False,
            foto_perfil=path
        ),
    )

    return new_pessoa


def authenticate_google(db, token: str):
    try:
        credentialsException = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Não foi possível validar as credenciais",
            headers={"WWW-Authenticate": "Bearer"},
        )

        GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(
            token, requests.Request(), GOOGLE_CLIENT_ID)
        issuers = ['accounts.google.com', 'https://accounts.google.com']
        if idinfo['iss'] not in issuers:
            raise ValueError('Wrong issuer.')
        # Get user info
        email, name, picture = idinfo['email'], idinfo['name'], idinfo['picture']
        # Checking if the user is already in the system
        pessoa = get_pessoa_by_email(db, email)
        pessoa = get_pessoa_by_username(db, name)
        password = passwords.get_password_hash(passwords.get_random_string())
        if pessoa is None:
            # User not registered, creating a new account
            new_pessoa = create_pessoa(
                db,
                schemas.PessoaCreate(
                    email=email,
                    nome=name,
                    usuario=name,
                    senha=password,
                    ativo=True,
                    superusuario=False,
                )
            )
            return new_pessoa
        else:
            # User is already registered, returning
            return pessoa
    except ValueError:
        raise credentialsException


def authenticate_facebook(
    db,
    pessoa: schemas.PessoaCreateFacebook
):
    try:
        credentialsException = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Não foi possível validar as credenciais",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        db_pessoa = get_pessoa_by_email(db, pessoa.email)
        db_pessoa = get_pessoa_by_username(db, pessoa.nome)
        password = passwords.get_password_hash(passwords.get_random_string())
        if db_pessoa is None:
            # User not registered, creating a new account
            new_pessoa = create_pessoa(
                db,
                schemas.PessoaCreate(
                    email=pessoa.email,
                    nome=pessoa.nome,
                    usuario=pessoa.nome,
                    senha=password,
                    ativo=True,
                    superusuario=False,
                )
            )
            return new_pessoa
        else:
            # User is already registered, returning
            return db_pessoa
    except ValueError:
        raise credentialsException
