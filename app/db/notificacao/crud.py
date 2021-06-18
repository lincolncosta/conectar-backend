from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t
from datetime import datetime

from app.db import models
from app.db.notificacao import schemas
from app.db.pessoa_projeto.schemas import PessoaProjeto
from app.db.pessoa.crud import get_pessoa_by_id
from app.db.projeto.crud import get_projeto
from app.db.ignorados.crud import delete_pessoas_ignoradas_by_vaga
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
                    .order_by(models.Notificacao.data_criacao.desc())\
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
                    .order_by(models.Notificacao.data_criacao.desc())\
                    .all()

    if not notificacao:
        raise HTTPException(
            status_code=404, detail="notificacao não encontrada")

    return notificacao


def get_notificacao_lida_by_destinatario(
    db: Session,
    destinatario_id: int,
    lido: bool
):
    '''
        Busca uma notificacao a partir do ID do destinatario e se foi lida

        Entrada: ID

        Saída: Esquema da notificacao correspondente

        Exceções: Não existe notificacao correspondente ao ID inserido
    '''

    notificacao = db.query(models.Notificacao)\
                    .filter(models.Notificacao.destinatario_id == destinatario_id)\
                    .filter(models.Notificacao.lido == lido)\
                    .order_by(models.Notificacao.data_criacao.desc())\
                    .all()

    if not notificacao:
        raise HTTPException(
            status_code=404, detail="notificacao não encontrada")

    return notificacao


def notificacao_pendente_idealizador(
    db: Session
):
    '''
        Cria notificacoes periodicamente para PessoaProjetos com situacao PENDENTE_IDEALIZADOR

        Entrada:

        Saída: lista de Esquemas das notificacoes criadas

        Exceções: Item Necessário Faltante
    '''

    pessoa_projetos = db.query(models.PessoaProjeto)\
        .filter(models.PessoaProjeto.situacao == "PENDENTE_IDEALIZADOR")\
        .all()

    # garante que somente uma notificacao será enviada para cada projeto
    projetos = []

    notificacao = []

    for pessoa_projeto in pessoa_projetos:
        if pessoa_projeto.projeto_id in projetos:
            continue

        projeto_id = pessoa_projeto.projeto_id
        projeto = get_projeto(db, projeto_id)

        projetos.append(pessoa_projeto.projeto_id)

        situacao = "<strong>Existem pessoas a serem avaliadas para o projeto "\
                + projeto.nome + "</strong>. Dê uma olhada!"

        if existe_notificacao(db, situacao, projeto.pessoa_id):
                continue

        try:
            db_notificacao = models.Notificacao(
                remetente_id=projeto.pessoa_id,
                destinatario_id=projeto.pessoa_id,
                projeto_id=projeto_id,
                pessoa_projeto_id=pessoa_projeto.id,
                situacao=situacao,
                foto=projeto.foto_capa,
                lido=False,
            )        
        except:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                detail="Item necessário faltante")

        db.add(db_notificacao)
        db.commit()
        db.refresh(db_notificacao)

        notificacao.append(db_notificacao)

    return notificacao


def notificacao_pendente_colaborador(
    db: Session,
    idealizador_id: int,
    pessoa_projeto: PessoaProjeto
):
    '''
        Cria uma notificacao baseada na situacao PENDENTE_COLABORADOR da PessoaProjeto

        Entrada: Esquema de PessoaProjeto, ID do idealizador

        Saída: Esquemas da notificaca criada

        Exceções: PessoaProjeto não pendente_colaborador
                  Item Necessário faltante
    '''

    if (pessoa_projeto.situacao != "PENDENTE_COLABORADOR"):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="PessoaProjeto não pendente_colaborador",
        )

    projeto_id = pessoa_projeto.projeto_id
    projeto = get_projeto(db, projeto_id)
    idealizador = get_pessoa_by_id(db, idealizador_id)

    situacao = "<strong>" + idealizador.nome + " te fez um convite</strong> para o projeto " + \
            projeto.nome + ". Confira!",

    if existe_notificacao(db, situacao, pessoa_projeto.pessoa_id):
        return

    try:
        db_notificacao = models.Notificacao(
            remetente_id=idealizador_id,
            destinatario_id=pessoa_projeto.pessoa_id,
            projeto_id=projeto_id,
            pessoa_projeto_id=pessoa_projeto.id,
            situacao=situacao,
            foto=projeto.foto_capa,
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


def notificacao_aceito_recusado(
    db: Session,
    colaborador_id: int,
    pessoa_projeto: PessoaProjeto
):
    '''
        Cria uma notificacao baseada na situação de PessoaProjeto

        Entrada: ID do remetente, esquema de PessoaProjeto

        Saída: Esquema da notificacao criada

        Exceções: PessoaProjeto não recusado/aceito
                  Item Necessário faltante
    '''

    if pessoa_projeto.situacao != "RECUSADO" and pessoa_projeto.situacao != "ACEITO":
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="PessoaProjeto não recusado/aceito",
        )

    projeto_id = pessoa_projeto.projeto_id
    projeto = get_projeto(db, projeto_id)
    colaborador = get_pessoa_by_id(db, colaborador_id)

    if pessoa_projeto.situacao == "RECUSADO":
        situacao = "<strong>" + colaborador.nome + \
            " recusou seu convite</strong>  para o projeto " + \
            projeto.nome + ". Realize uma nova busca."

    elif pessoa_projeto.situacao == "ACEITO":
        situacao = "<strong>" + colaborador.nome + \
            " aceitou seu convite</strong> para o projeto " + \
            projeto.nome + ". Finalize o acordo e preencha essa vaga!"

    if existe_notificacao(db, situacao, projeto.pessoa_id):
        return

    try:
        db_notificacao = models.Notificacao(
            remetente_id=colaborador_id,
            destinatario_id=projeto.pessoa_id,
            projeto_id=projeto_id,
            pessoa_projeto_id=pessoa_projeto.id,
            situacao=situacao,
            foto=colaborador.foto_perfil,
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


def notificacao_finalizado(
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

    anexo = createPDF(db, pessoa_projeto)

    colaborador = get_pessoa_by_id(db, pessoa_projeto.pessoa_id)
    projeto = get_projeto(db, pessoa_projeto.projeto_id)
    idealizador = get_pessoa_by_id(db, projeto.pessoa_id)

    # notificacao idealizador
    db_notificacao = models.Notificacao(
        remetente_id=colaborador.id,
        destinatario_id=idealizador.id,
        projeto_id=pessoa_projeto.projeto_id,
        pessoa_projeto_id=pessoa_projeto.id,
        situacao="<strong>Seu acordo foi finalizado!</strong> Clique aqui e veja seu PDF top!",
        foto=projeto.foto_capa,
        anexo=anexo,
        lido=False,
    )

    db.add(db_notificacao)
    db.commit()
    db.refresh(db_notificacao)

    notificacao.append(db_notificacao)

    # notificacao colab
    db_notificacao = models.Notificacao(
        remetente_id=idealizador.id,
        destinatario_id=colaborador.id,
        projeto_id=pessoa_projeto.projeto_id,
        pessoa_projeto_id=pessoa_projeto.id,
        situacao="<strong>Seu acordo foi finalizado!</strong> aqui e veja seu PDF top!",
        foto=projeto.foto_capa,
        anexo=anexo,
        lido=False,
    )

    db.add(db_notificacao)
    db.commit()
    db.refresh(db_notificacao)

    notificacao.append(db_notificacao)

    delete_pessoas_ignoradas_by_vaga(db, pessoa_projeto.id)

    return notificacao


def notificacao_checagem(
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
        att_str = datetime.strftime(
            pessoa_projeto.data_atualizacao, "%Y-%m-%d")
        att = datetime.strptime(att_str, "%Y-%m-%d")

        diff = hoje - att

        if(diff.days < 6):
            remetente = get_pessoa_by_id(db, projeto.pessoa_id)
            situacao = "<strong>Se liga:</strong> você tem " + str(6-diff.days) + " dias para responder ao convite de " + \
                remetente.nome + " para o projeto " + projeto.nome + ".",
            destinatario_id = pessoa_projeto.pessoa_id

            if existe_notificacao(db, db_notificacao.situacao, db_notificacao.destinatario_id):
                continue

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
                remetente.nome + " expirou!</strong> Realize uma nova busca e complete seu time!"
            destinatario_id = projeto.pessoa_id

            if existe_notificacao(db, db_notificacao.situacao, db_notificacao.destinatario_id):
                continue

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


def notificacao_checagem_projeto(
    db: Session
):

    projetos = db.query(models.Projeto)\
        .filter(models.Projeto.areas == None, models.Projeto.habilidades == None)\
        .join(models.Habilidades, models.Projeto.habilidades, full=True, isouter=True)\
        .join(models.Area, models.Projeto.areas, full=True, isouter=True)\
        .all()

    notificacao = []

    # projetos a serem ignorados na verificação das vagas
    projetos_ignorados = []

    for projeto in projetos:

        projetos_ignorados.append(projeto.id)

        db_notificacao = models.Notificacao(
            remetente_id=projeto.pessoa_id,
            destinatario_id=projeto.pessoa_id,
            projeto_id=projeto.id,
            pessoa_projeto_id=None,
            situacao="<strong>Finalize o cadastro do projeto " +
            projeto.nome + "</strong> e encontre o time ideal!",
            foto=projeto.foto_capa,
            lido=False,
        )

        if existe_notificacao(db, db_notificacao.situacao, db_notificacao.destinatario_id):
            continue

        db.add(db_notificacao)
        db.commit()
        db.refresh(db_notificacao)

        notificacao.append(db_notificacao)

    vagas = db.query(models.PessoaProjeto)\
        .filter(models.PessoaProjeto.areas == None, models.PessoaProjeto.habilidades == None)\
        .filter(models.PessoaProjeto.projeto_id.notin_(projetos_ignorados))\
        .join(models.Habilidades, models.PessoaProjeto.habilidades, full=True, isouter=True)\
        .join(models.Area, models.PessoaProjeto.areas, full=True, isouter=True)\
        .all()

    for vaga in vagas:
        if vaga.projeto_id in projetos_ignorados:
            break

        projetos_ignorados.append(vaga.projeto_id)

        projeto = get_projeto(db, vaga.projeto_id)

        db_notificacao = models.Notificacao(
            remetente_id=projeto.pessoa_id,
            destinatario_id=projeto.pessoa_id,
            projeto_id=projeto.id,
            pessoa_projeto_id=None,
            situacao="<strong>Finalize o cadastro das vagas do projeto " +
            projeto.nome + "</strong> e encontre o time ideal!",
            foto=projeto.foto_capa,
            lido=False,
        )

        if existe_notificacao(db, db_notificacao.situacao, db_notificacao.destinatario_id):
            continue

        db.add(db_notificacao)
        db.commit()
        db.refresh(db_notificacao)

        notificacao.append(db_notificacao)

    return notificacao

def notificacao_favorito(
    db: Session,
    remetente_id: int,
    projeto_id: int
):

    projeto = get_projeto(db, projeto_id)
    remetente = get_pessoa_by_id(db, remetente_id)

    db_notificacao = models.Notificacao(
        remetente_id=remetente_id,
        destinatario_id=projeto.pessoa_id,
        projeto_id=projeto.id,
        pessoa_projeto_id=None,
        situacao = "<strong>" + remetente.nome + " favoritou</strong> o projeto " + projeto.nome + "!",
        foto=projeto.foto_capa,
        lido=False,
    )

    if existe_notificacao(db, db_notificacao.situacao, db_notificacao.destinatario_id):
        return

    db.add(db_notificacao)
    db.commit()
    db.refresh(db_notificacao)

def notificacao_interesse(
    db: Session,
    remetente_id: int,
    projeto_id: int
):

    projeto = get_projeto(db, projeto_id)
    remetente = get_pessoa_by_id(db, remetente_id)

    db_notificacao = models.Notificacao(
        remetente_id=remetente_id,
        destinatario_id=projeto.pessoa_id,
        projeto_id=projeto.id,
        pessoa_projeto_id=None,
        situacao = "<strong>" + remetente.nome + " demonstrou interesse</strong> no projeto " + projeto.nome + "!",
        foto=projeto.foto_capa,
        lido=False,
    )

    if existe_notificacao(db, db_notificacao.situacao, db_notificacao.destinatario_id):
        return

    db.add(db_notificacao)
    db.commit()
    db.refresh(db_notificacao)

def existe_notificacao(
    db: Session,
    situacao: str,
    destinatario_id: int
):

    '''
    Verifica se existe uma notificacao com mais de 4 dias com aquela mesma situação
    para a mesma pessoa
    '''

    filtro = db.query(models.Notificacao)\
                .filter(models.Notificacao.situacao == situacao)\
                .filter(models.Notificacao.destinatario_id == destinatario_id)\
                .filter(models.Notificacao.lido == False)\
                .order_by(models.Notificacao.data_criacao.desc())\
                .first()


    if filtro:
        
        data1 = datetime.date(filtro.data_criacao)

        data2 = datetime.date(datetime.today())

        data2-data1

        diferenca = data2-data1

        if diferenca.days > 4:
            return False
        return True
    else:
        return False

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


def ler_todas_notificacao(
    db: Session,
    destinatario_id: int
):
    db.query(models.Notificacao).filter(models.Notificacao.destinatario_id ==
                                        destinatario_id).update({models.Notificacao.lido: True})
    db.commit()                                            
