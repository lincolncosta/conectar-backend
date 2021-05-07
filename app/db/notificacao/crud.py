from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t
from datetime import datetime

from app.db import models
from app.db.notificacao import schemas
from app.db.pessoa_projeto.schemas import PessoaProjeto
from app.db.pessoa.crud import get_pessoa_by_id
from app.db.projeto.crud import get_projeto
from app.db.utils.pdfs import createPDF 


def get_notificacao_by_id(
    db: Session,
    notificacao_id: int
    ):

    '''
        Busca uma notificacao a partir do ID da mesma

        Entrada: ID

        Saída: Esquema da notificacao correspondente

        Exceções: Não existe notificacao correspondente ao ID inserido
    '''

    notificacao = db.query(models.Notificacao)\
                    .filter(models.Notificacao.id == notificacao_id)\
                    .first()

    if not notificacao:
        raise HTTPException(
            status_code=404, detail="notificacao não encontrada")

    return notificacao


def get_notificacao_by_destinatario(
    db: Session,
    destinatario_id: int
    ):

    '''
        Busca uma notificacao a partir do ID do destinatario

        Entrada: ID

        Saída: Esquema da notificacao correspondente

        Exceções: Não existe notificacao correspondente ao ID inserido
    '''

    notificacao = db.query(models.Notificacao)\
                    .filter(models.Notificacao.destinatario_id == destinatario_id)\
                    .all()

    if not notificacao:
        raise HTTPException(
            status_code=404, detail="notificacao não encontrada")

    return notificacao


def create_notificacao_vaga(
    db: Session,
    remetente_id: int,
    pessoa_projeto: PessoaProjeto
    ):

    '''
        Cria uma notificacao baseada na situação de PessoaProjeto

        Entrada: ID, esquema de PessoaProjeto

        Saída: Esquema da notificacao criada

        Exceções: PessoaProjeto não pode gerar notificação
    '''

    projeto_id = pessoa_projeto.projeto_id
    projeto = get_projeto(db, projeto_id)
    pessoa = get_pessoa_by_id(db, remetente_id)

    if pessoa_projeto.situacao == "PENDENTE_IDEALIZADOR":
        situacao = "<strong>Finalize o cadastro do projeto " + \
            projeto.nome + "</strong> <span> e encontre o time ideal</span>"
        destinatario_id = remetente_id
        foto = projeto.foto_capa

    elif pessoa_projeto.situacao == "RECUSADO":
        situacao = "<strong>" + pessoa.nome + " recusou seu convite</strong> <span> para o projeto " + \
            projeto.nome + ". Realize uma nova busca</span>"
        destinatario_id = projeto.pessoa_id
        foto = pessoa.foto_perfil

    elif pessoa_projeto.situacao == "ACEITO":
        situacao = "<strong>" + pessoa.nome + " aceitou seu convite</strong> <span> para o projeto " + \
            projeto.nome + ". Finalize o acordo e preencha essa vaga!</span>"
        destinatario_id = projeto.pessoa_id
        foto = pessoa.foto_perfil

    elif pessoa_projeto.situacao == "PENDENTE_COLABORADOR":
        situacao = "<strong>" + pessoa.nome + " te fez um convite</strong> <span> para o projeto " + \
            projeto.nome + ". Confira!</span>"
        destinatario_id = pessoa_projeto.pessoa_id
        foto = projeto.foto_capa

    try:
        db_notificacao = models.Notificacao(
            remetente_id=remetente_id,
            destinatario_id=destinatario_id,
            projeto_id=projeto_id,
            pessoa_projeto_id=pessoa_projeto.id,
            situacao=situacao,
            foto=foto,
            lido=False,
        )
    except:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Item necessário faltante")

    db.add(db_notificacao)
    db.commit()
    db.refresh(db_notificacao)

    return db_notificacao


def finaliza_notificacao_vaga(
    db: Session,
    pessoa_projeto: PessoaProjeto
    ):

    '''
        Cria uma notificacao baseada na situacao FINALIZADO da PessoaProjeto

        Entrada: Esquema de PessoaProjeto

        Saída: Dois Esquemas das notificacoes criadas

        Exceções: PessoaProjeto não finalizada
    '''

    if (pessoa_projeto.situacao != "FINALIZADO"):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="PessoaProjeto não finalizada",
        )

    notificacao = []

    link = createPDF(db, pessoa_projeto)

    colaborador = get_pessoa_by_id(db, pessoa_projeto.pessoa_id)
    projeto = get_projeto(db, pessoa_projeto.projeto_id)
    idealizador = get_pessoa_by_id(db, projeto.pessoa_id)

    #notificacao idealizador
    db_notificacao = models.Notificacao(
                    remetente_id = colaborador.id,
                    destinatario_id = idealizador.id,
                    projeto_id = pessoa_projeto.projeto_id,
                    pessoa_projeto_id = pessoa_projeto.id,
                    situacao = "<strong>Seu acordo foi finalizado!</strong> <span> Clique aqui e veja seu PDF top!</span>",
                    foto = projeto.foto_capa,
                    link = link,
                    lido = False,
                    )
                    
    db.add(db_notificacao)
    db.commit()
    db.refresh(db_notificacao)

    notificacao.append(db_notificacao)

    #notificacao colab
    db_notificacao = models.Notificacao(
                    remetente_id = idealizador.id,
                    destinatario_id = colaborador.id,
                    projeto_id = pessoa_projeto.projeto_id,
                    pessoa_projeto_id = pessoa_projeto.id,
                    situacao = "<strong>Seu acordo foi finalizado!</strong> <span> Clique aqui e veja seu PDF top!</span>",
                    foto = projeto.foto_capa,
                    link = link,
                    lido = False,
                    )

    db.add(db_notificacao)
    db.commit()
    db.refresh(db_notificacao)

    notificacao.append(db_notificacao)

    return notificacao


def check_notificacao_vaga(
    db: Session
    ):

    '''
        Cria notificacoes periodicamente para PessoaProjetos com situacao PENDENTE_COLABORADOR

        Entrada:

        Saída: lista de Esquemas das notificacoes criadas

        Exceções: 
    '''

    hoje = datetime.today()

    pessoa_projetos = db.query(models.PessoaProjeto)\
        .filter(models.PessoaProjeto.situacao == "PENDENTE_COLABORADOR")\
        .all()

    notificacao = []

    for pessoa_projeto in pessoa_projetos:
        projeto = get_projeto(db, pessoa_projeto.projeto_id)
        att_str = datetime.strftime(pessoa_projeto.data_atualizacao, "%Y-%m-%d")
        att = datetime.strptime(att_str, "%Y-%m-%d")

        diff = hoje - att

        if(diff.days < 6):
            remetente = get_pessoa_by_id(db, projeto.pessoa_id)
            situacao = "<strong>Se liga:</strong> <span> você tem " + str(6-diff.days) + " dias para responder ao convite de " + \
                remetente.nome + " para o projeto " + projeto.nome + ".</span>",
            destinatario_id = pessoa_projeto.pessoa_id

            filtro = db.query(models.Notificacao)\
                .filter(models.Notificacao.destinatario_id == destinatario_id)\
                .filter(models.Notificacao.situacao == situacao)\
                .first()

            if not filtro:
                db_notificacao = models.Notificacao(
                    remetente_id=remetente.id,
                    destinatario_id=destinatario_id,
                    projeto_id=pessoa_projeto.projeto_id,
                    pessoa_projeto_id=pessoa_projeto.id,
                    situacao=situacao,
                    foto=remetente.foto_perfil,
                    lido=False,
                )

                db.add(db_notificacao)
                db.commit()
                db.refresh(db_notificacao)

                notificacao.append(db_notificacao)

        elif(diff.days == 6):
            remetente = get_pessoa_by_id(db, pessoa_projeto.pessoa_id)
            situacao = "<strong>O prazo de resposta de " + \
                remetente.nome + " expirou!</strong> <span> Realize uma nova busca e complete seu time!</span>"
            destinatario_id = projeto.pessoa_id

            filtro = db.query(models.Notificacao)\
                .filter(models.Notificacao.destinatario_id == destinatario_id)\
                .filter(models.Notificacao.situacao == situacao)\
                .first()

            if not filtro:
                db_notificacao = models.Notificacao(
                    remetente_id=remetente.id,
                    destinatario_id=destinatario_id,
                    projeto_id=pessoa_projeto.projeto_id,
                    pessoa_projeto_id=pessoa_projeto.id,
                    situacao=situacao,
                    foto=remetente.foto_perfil,
                    lido=False,
                )

                db.add(db_notificacao)
                db.commit()
                db.refresh(db_notificacao)

                notificacao.append(db_notificacao)

    return notificacao


def edit_notificacao(
    db: Session,
    notificacao_id: int,
    notificacao: schemas.NotificacaoEdit
    ) -> schemas.Notificacao:

    '''
        Edita notificacao 

        Entrada: ID, esquema de notificacao

        Saída: Esquemas da notificacao editada

        Exceções: Notificacao não encontrada
    '''

    db_notificacao = get_notificacao_by_id(db, notificacao_id)

    update_data = notificacao.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_notificacao, key, value)

    db.add(db_notificacao)
    db.commit()
    db.refresh(db_notificacao)

    return db_notificacao


def delete_notificacao(
    db: Session,
    notificacao_id: int
    ):

    '''
        Deleta notificacao 

        Entrada: ID

        Saída: Esquemas da notificacao deletada

        Exceções: Notificacao não encontrada
    '''

    notificacao = get_notificacao_by_id(db, notificacao_id)
    
    db.delete(notificacao)
    db.commit()

    return notificacao