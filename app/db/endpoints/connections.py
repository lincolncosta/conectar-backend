from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t

from datetime import datetime
from db import models
from db.pessoa_projeto.crud import get_pessoa_projeto
from db.pessoa_projeto import schemas


'''

    PENDENTE_IDEALIZADOR -> PENDENTE_COLABORADOR -> ACEITE_COLABORADOR -> FINALIZADO
    PENDENTE_COLABORADOR -> RECUSA_COLABORADOR -> PENDENTE_IDEALIZADOR
'''


def pessoa_projeto_aceite(db: Session, pessoa_projeto_id: int):

    pessoa_projeto = get_pessoa_projeto(db, pessoa_projeto_id)

    if pessoa_projeto.situacao == 'ACEITE_COLABORADOR':
        pessoa_projeto.situacao = "FINALIZADO"

    if pessoa_projeto.situacao == 'PENDENTE_COLABORADOR':
        pessoa_projeto.situacao = "ACEITE_COLABORADOR"

    if pessoa_projeto.situacao == 'PENDENTE_IDEALIZADOR':
        pessoa_projeto.situacao = "PENDENTE_COLABORADOR"


    db.add(pessoa_projeto)
    db.commit()
    db.refresh(pessoa_projeto)

    return pessoa_projeto


def pessoa_projeto_recusa(db: Session, pessoa_projeto_id: int):

    pessoa_projeto = get_pessoa_projeto(db, pessoa_projeto_id)

    if pessoa_projeto.situacao == 'PENDENTE_COLABORADOR':
        pessoa_projeto.situacao = "PENDENTE_IDEALIZADOR"

    db.add(pessoa_projeto)
    db.commit()
    db.refresh(pessoa_projeto)

    return pessoa_projeto


def pessoa_projeto_pendente_colaborador_time(db: Session, pessoa_projeto_id: int):

    '''
    Get a pessoa_projeto by id and update situação to pendente_idealizador
    if time limit reached (5 days)
    '''

    pessoa_projeto = get_pessoa_projeto(db, pessoa_projeto_id)

    if pessoa_projeto.situacao != 'PENDENTE_COLABORADOR':
        return pessoa_projeto

    today = datetime.today()
    
    if (today.day - pessoa_projeto.data_atualizacao.day) > 5:
        pessoa_projeto.situacao = "PENDENTE_IDEALIZADOR"
        
        db.add(pessoa_projeto)
        db.commit()
        db.refresh(pessoa_projeto)

    else:
        print("Você possui apenas " + 
        str(pessoa_projeto.data_atualizacao.day + 5 - today.day) + 
        " dias para responder esse convite")

    return pessoa_projeto
    