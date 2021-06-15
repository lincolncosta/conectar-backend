from fastapi import HTTPException, status, UploadFile
from sqlalchemy.orm import Session
import typing as t
from sqlalchemy.sql import func
from random import shuffle
from db import models
from db.utils.extract_areas import append_areas
from db.utils.extract_habilidade import append_habilidades
from db.utils.salvar_imagem import store_image, delete_image
from . import schemas

def get_projeto_by_username(db: Session, usuario: str) -> schemas.Projeto:
    return (
        db.query(models.Projeto).filter(models.Projeto.nome == usuario).first()
    )


def get_projeto(db: Session, projeto_id: int) -> schemas.Projeto:
    projeto = (
        db.query(models.Projeto).filter(models.Projeto.id == projeto_id).first()
    )
    if not projeto:
        raise HTTPException(status_code=404, detail="projeto não encontrado")
    return projeto

def get_projetos_destaque(db: Session, qtd_projetos: int):
    projetos = db.query(models.Reacoes.projeto_id, func.count(models.Reacoes.projeto_id).label('qtd'))\
                .group_by(models.Reacoes.projeto_id)\
                .order_by('qtd')\
                .limit(10)\
                .all()

    shuffle(projetos)

    projetos_return = []

    for i in range(qtd_projetos):
        projeto_id = projetos[i][0]
        projeto = get_projeto(db, projeto_id)
        projetos_return.append(projeto)

    return projetos_return

def get_projetos(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    visibilidade: bool = True,
    pessoa_id: t.Optional[int] = None,
) -> t.List[schemas.ProjetoOut]:
    if pessoa_id:
        return (
            db.query(models.Projeto)
            .filter(
                models.Projeto.pessoa_id == pessoa_id,
                models.Projeto.visibilidade == visibilidade,
            )
            .order_by(models.Projeto.data_criacao.desc())\
            .offset(skip)
            .limit(limit)            
            .all()
        )
    return (
        db.query(models.Projeto)
        .filter(
            models.Projeto.visibilidade == visibilidade,
        )
        .order_by(models.Projeto.data_criacao.desc())\
        .offset(skip)
        .limit(limit)        
        .all()
    )

def get_projeto_reacao(
    db: Session,
    pessoa_id: int,
    reacao: str
):

    reacoes = db.query(models.Reacoes)\
        .filter(models.Reacoes.pessoa_id == pessoa_id,
                models.Reacoes.reacao == reacao)\
        .order_by(models.Reacoes.data_criacao.desc())\
        .all()

    projetos = []

    for reacao in reacoes:
        projetos.append(get_projeto(db, reacao.projeto_id))

    return projetos

async def edit_projeto(
    db: Session,
    projeto_id: int,
    projeto: schemas.ProjetoEdit,
    foto_capa: t.Optional[UploadFile] = None,
) -> schemas.Projeto:

    db_projeto = get_projeto(db, projeto_id)
    if not db_projeto:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="projeto não encontrado"
        )
    update_data = projeto.dict(exclude_unset=True)


    await append_areas(update_data, db)
    await append_habilidades(update_data, db)

    for key, value in update_data.items():
        setattr(db_projeto, key, value)

    db.add(db_projeto)
    db.commit()
    db.refresh(db_projeto)
    return db_projeto

async def edit_foto_projeto(
    db: Session,
    projeto_id: int,
    foto_capa: UploadFile
):

    contents = await foto_capa.read()
    db_projeto = get_projeto(db, projeto_id)

    if delete_image(db_projeto.foto_capa):
        db_projeto.foto_capa = store_image(contents)

    db.add(db_projeto)
    db.commit()
    db.refresh(db_projeto)
    return db_projeto

async def create_projeto(
    db: Session,
    nome: str,
    descricao: str,
    visibilidade: bool,
    objetivo: str,
    pessoa_id: t.Optional[int] = None,
    foto_capa: t.Optional[UploadFile] = None,
):

    path = None
    if foto_capa:
        contents = await foto_capa.read()
        path = store_image(contents)

    db_projeto = models.Projeto(
        nome=nome,
        descricao=descricao,
        visibilidade=visibilidade,
        objetivo=objetivo,
        pessoa_id=pessoa_id,
        foto_capa=path,
    )

    db.add(db_projeto)
    db.commit()
    db.refresh(db_projeto)

    db_proj = db_projeto.__dict__
    return {"id": db_proj["id"]}


def delete_projeto(db: Session, projeto_id: int):
    projeto = get_projeto(db, projeto_id)
    if not projeto:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="projeto não encontrado"
        )

    if projeto.foto_capa:
        delete_image(projeto.foto_capa)

    db.delete(projeto)
    db.commit()
    return projeto


def get_habilidades_projeto(db: Session, projeto_id: int):
    projeto = get_projeto(db, projeto_id)
    if not projeto:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="projeto não encontrada"
        )
    habilidade = projeto.habilidades

    return habilidade


def get_areas_projeto(db: Session, projeto_id: int):
    projeto = get_projeto(db, projeto_id)
    if not projeto:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="projeto não encontrada"
        )
    area = projeto.areas

    return area