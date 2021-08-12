from fastapi import FastAPI, BackgroundTasks, UploadFile, File, Form
from sqlalchemy.orm.session import Session
from starlette.responses import JSONResponse
from starlette.requests import Request
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from pydantic import BaseModel, EmailStr
from typing import List
import uuid
import datetime
from fastapi import HTTPException, status

from db.pessoa.crud import get_pessoa_by_email, edit_pessoa

from db import models

import os

class Envs:
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_FROM = os.getenv('MAIL_FROM')
    MAIL_PORT = int(os.getenv('MAIL_PORT'))
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_FROM_NAME = os.getenv('MAIN_FROM_NAME')

class EmailSchema(BaseModel):
    email: List[EmailStr]

conf = ConnectionConfig(
    MAIL_USERNAME=Envs.MAIL_USERNAME,
    MAIL_PASSWORD=Envs.MAIL_PASSWORD,
    MAIL_FROM=Envs.MAIL_FROM,
    MAIL_PORT=Envs.MAIL_PORT,
    MAIL_SERVER=Envs.MAIL_SERVER,
    MAIL_FROM_NAME=Envs.MAIL_FROM_NAME,
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True
    # TEMPLATE_FOLDER='templates/'
)

async def envia_email_senha(
    background_tasks: BackgroundTasks,
    db: Session, 
    email_para: str,
):

    filtro = db.query(models.Pessoa).filter(models.Pessoa.email == email_para)

    if not filtro:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="Email Não Cadastrado!"
        )

    pessoa = get_pessoa_by_email(db, email_para)

    if not pessoa.token_senha or datetime.date.today() > pessoa.expiracao_token + datetime.timedelta(days=1):
        
        pessoa.token_senha = str(uuid.uuid4().hex)
        pessoa.expiracao_token = datetime.date.today() + datetime.timedelta(days=1)

        db.add(pessoa)
        db.commit()
        db.refresh(pessoa)

    url = 'http://boraconectar.com/esqueci-senha/' + pessoa.token_senha

    message = MessageSchema(
        subject='Esqueci a senha',
        recipients=[email_para],
        template_body={'name':pessoa.nome, 'token': pessoa.token_senha, 'UrlToken': url},
    )
    

    fm = FastMail(conf)
    background_tasks.add_task(
        fm.send_message, message, template_name='email.html')