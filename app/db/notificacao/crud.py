from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t
from datetime import datetime

from app.db import models
from app.db.notificacao import schemas
from app.db.pessoa_projeto.schemas import PessoaProjeto
from app.db.pessoa.crud import get_pessoa
from app.db.projeto.crud import get_projeto
from app.db.utils.pdfs import createPDF


def get_notificacao_by_id(db: Session, notificacao_id: int):
    notificacao = db.query(models.Notificacao)\
                    .filter(models.Notificacao.id == notificacao_id)\
                    .first()

    if not notificacao:
        raise HTTPException(
            status_code=404, detail="notificacao não encontrada")
    return notificacao


def get_notificacao_by_destinatario(db: Session, destinatario_id: int):

    notificacao = db.query(models.Notificacao)\
                    .filter(models.Notificacao.destinatario_id == destinatario_id)\
                    .all()

    if not notificacao:
        raise HTTPException(
            status_code=404, detail="notificacao não encontrada")
    return notificacao


def create_notificacao_vaga(db: Session,
                            remetente_id: int,
                            pessoa_projeto: PessoaProjeto):

    hoje = datetime.today()

    projeto_id = pessoa_projeto.projeto_id
    projeto = get_projeto(db, projeto_id)
    pessoa = get_pessoa(db, remetente_id)

    if pessoa_projeto.situacao == "PENDENTE_IDEALIZADOR":
        situacao = "Finalize o cadastro do projeto " + \
            projeto.nome + " e encontre o time ideal"
        destinatario_id = remetente_id

    elif pessoa_projeto.situacao == "RECUSADO":
        situacao = pessoa.nome + " recusou seu convite para o projeto " + \
            projeto.nome + ". Realize uma nova busca"
        destinatario_id = projeto.pessoa_id

    elif pessoa_projeto.situacao == "ACEITO":
        situacao = pessoa.nome + " aceitou seu convite para o projeto " + \
            projeto.nome + ". Finalize o acordo e preencha essa vaga!"
        destinatario_id = projeto.pessoa_id

    elif pessoa_projeto.situacao == "PENDENTE_COLABORADOR":
        if(hoje.day == pessoa_projeto.data_atualizacao.day):
            situacao = pessoa.nome + " te fez um convite para o projeto " + \
                projeto.nome + ". Confira!"
            destinatario_id = pessoa_projeto.pessoa_id

    db_notificacao = models.Notificacao(
        remetente_id=remetente_id,
        destinatario_id=destinatario_id,
        projeto_id=projeto_id,
        pessoa_projeto_id=pessoa_projeto.id,
        situacao=situacao,
        lido=False,
    )

    db.add(db_notificacao)
    db.commit()
    db.refresh(db_notificacao)
    return db_notificacao


def finaliza_notificacao_vaga(db: Session, pessoa_projeto: PessoaProjeto):

    vaga = pessoa_projeto

    if (vaga.situacao != "FINALIZADO"):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Vaga não finalizada",
        )

    notificacao = []

    link = createPDF(db, vaga)

    colab = get_pessoa(db, vaga.pessoa_id)
    proj = get_projeto(db, vaga.projeto_id)
    idealizador = get_pessoa(db, proj.pessoa_id)

    # notificacao idealizador
    db_notificacao = models.Notificacao(
        remetente_id=colab.id,
        destinatario_id=idealizador.id,
        projeto_id=vaga.projeto_id,
        pessoa_projeto_id=vaga.id,
        situacao=link,
        lido=False,
    )

    db.add(db_notificacao)
    db.commit()
    db.refresh(db_notificacao)

    notificacao.append(db_notificacao)

    # notificacao colab
    db_notificacao = models.Notificacao(
        remetente_id=idealizador.id,
        destinatario_id=colab.id,
        projeto_id=vaga.projeto_id,
        pessoa_projeto_id=vaga.id,
        situacao=link,
        lido=False,
    )
    db.add(db_notificacao)
    db.commit()
    db.refresh(db_notificacao)

    notificacao.append(db_notificacao)

    return notificacao


def check_notificacao_vaga(db: Session):

    hoje = datetime.today()

    vagas = db.query(models.PessoaProjeto)\
        .filter(models.PessoaProjeto.situacao == "PENDENTE_COLABORADOR")\
        .all()

    notificacao = []

    for vaga in vagas:
        projeto = get_projeto(db, vaga.projeto_id)
        att_str = datetime.strftime(vaga.data_atualizacao, "%Y-%m-%d")
        att = datetime.strptime(att_str, "%Y-%m-%d")

        diff = hoje - att

        if(diff.days < 6):
            remetente = get_pessoa(db, projeto.pessoa_id)
            situacao = "Você tem " + str(6-diff.days) + " dias para responder ao convite de " + \
                remetente.nome + " para o projeto " + projeto.nome,
            destinatario_id = vaga.pessoa_id

            filtro = db.query(models.Notificacao)\
                .filter(models.Notificacao.destinatario_id == destinatario_id)\
                .filter(models.Notificacao.situacao == situacao)\
                .first()

            if not filtro:
                db_notificacao = models.Notificacao(
                    remetente_id=remetente.id,
                    destinatario_id=destinatario_id,
                    projeto_id=vaga.projeto_id,
                    pessoa_projeto_id=vaga.id,
                    situacao=situacao,
                    lido=False,
                )

                db.add(db_notificacao)
                db.commit()
                db.refresh(db_notificacao)

                notificacao.append(db_notificacao)

        elif(diff.days == 6):
            remetente = get_pessoa(db, vaga.pessoa_id)
            situacao = "O prazo de resposta de " + \
                remetente.nome + " expirou! Faça uma nova busca."
            destinatario_id = projeto.pessoa_id

            filtro = db.query(models.Notificacao)\
                .filter(models.Notificacao.destinatario_id == destinatario_id)\
                .filter(models.Notificacao.situacao == situacao)\
                .first()

            if not filtro:
                db_notificacao = models.Notificacao(
                    remetente_id=remetente.id,
                    destinatario_id=destinatario_id,
                    projeto_id=vaga.projeto_id,
                    pessoa_projeto_id=vaga.id,
                    situacao=situacao,
                    lido=False,
                )

                db.add(db_notificacao)
                db.commit()
                db.refresh(db_notificacao)

                notificacao.append(db_notificacao)

    return notificacao


def edit_notificacao(
    db: Session, notificacao_id, notificacao: schemas.NotificacaoEdit
) -> schemas.Notificacao:

    db_notificacao = get_notificacao_by_id(db, notificacao_id)
    if not db_notificacao:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="notificacao não encontrada",
        )
    update_data = notificacao.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_notificacao, key, value)

    db.add(db_notificacao)
    db.commit()
    db.refresh(db_notificacao)
    return db_notificacao


def delete_notificacao(db: Session, notificacao_id: int):
    notificacao = get_notificacao_by_id(db, notificacao_id)
    if not notificacao:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="notificacao não encontrada",
        )
    db.delete(notificacao)
    db.commit()
    return notificacao
