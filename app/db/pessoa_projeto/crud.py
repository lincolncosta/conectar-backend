from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
import typing as t

from db import models
from . import schemas
from db.pessoa.crud import get_pessoa, get_pessoas, get_pessoas_by_papel
from db.projeto.crud import get_projeto
from db.notificacao.crud import create_notificacao_vaga
from db.utils.extract_areas import append_areas
from db.utils.extract_habilidade import append_habilidades
from db.utils import similaridade


def get_pessoa_projeto(
    db: Session, pessoa_projeto_id: int
) -> schemas.PessoaProjeto:

    pessoa_projeto = (
        db.query(models.PessoaProjeto)
        .filter(models.PessoaProjeto.id == pessoa_projeto_id)
        .first()
    )
    if not pessoa_projeto:
        raise HTTPException(
            status_code=404, detail="pessoa_projeto não encontrada"
        )

    return pessoa_projeto


async def get_all_pessoas_projeto(db: Session) -> t.List[schemas.PessoaProjeto]:
    pessoas_projeto = db.query(models.PessoaProjeto).all()
    if not pessoas_projeto:
        raise HTTPException(
            status_code=404, detail="Não há pessoas_projeto cadastradas"
        )

    return pessoas_projeto


async def get_similaridade_pessoas_projeto(
    db: Session, pessoa_logada: models.Pessoa, id_projeto: int
) -> schemas.Pessoa:

    pessoas_vagas = {}

    # Com o id do projeto, buscar as vagas disponíveis
    vagas_projeto = await get_vagas_by_projeto(db, id_projeto)
    pessoas_selecionadas = [pessoa_logada.id]
    similaridades_retorno = {}

    # Iterar em cada vaga, buscando o papel
    for vaga in vagas_projeto:
        papel = vaga.papel_id

        # Extração de informações de habilidades e áreas da vaga
        habilidades_areas_vaga = []

        habilidades_projeto = vaga.habilidades
        areas_projeto = vaga.areas

        for habilidade_projeto in habilidades_projeto:
            habilidades_areas_vaga.append(habilidade_projeto.nome)

        for area_projeto in areas_projeto:
            habilidades_areas_vaga.append(area_projeto.descricao)

        # Precisamos criar um filtro para buscar somente pessoas que ainda não foram selecionadas
        pessoas = get_pessoas_by_papel(db, papel, pessoas_selecionadas)
        habilidades_areas = []
        similaridades_pessoa = {}

        for pessoa in pessoas:
            if pessoa not in similaridades_pessoa:
                habilidades = pessoa.habilidades
                areas = pessoa.areas

                for habilidade in habilidades:
                    habilidades_areas.append(habilidade.nome)

                for area in areas:
                    habilidades_areas.append(area.descricao)

                similaridades_pessoa[pessoa] = similaridade.calcula_similaridade_vaga_pessoa(
                    '. '.join(habilidades_areas_vaga), '. '.join(habilidades_areas))

        similaridades_retorno = dict(
            sorted(similaridades_pessoa.items(), key=lambda item: item[1], reverse=False))

        pessoa_selecionada = next(iter(similaridades_retorno))
        await atualiza_match_vaga(db, vaga, pessoa_selecionada)

        pessoas_vagas[vaga.id] = pessoa_selecionada
        pessoas_selecionadas.append(pessoa_selecionada.id)

    if not pessoas:
        raise HTTPException(status_code=404, detail="pessoas não encontradas")

    return pessoas_vagas


async def atualiza_match_vaga(db, vaga, pessoa):
    vagaEdit = schemas.PessoaProjetoEdit()
    vagaEdit.pessoa_id = pessoa.id
    vagaEdit.situacao = "PENDENTE_IDEALIZADOR"

    await edit_pessoa_projeto(db, vaga.id, vagaEdit)


async def get_vagas_by_projeto(
    db: Session, id_projeto: int

) -> t.List[schemas.PessoaProjeto]:
    pessoa_projeto = (
        db.query(models.PessoaProjeto)
        .filter(models.PessoaProjeto.projeto_id == id_projeto)
        .filter(models.PessoaProjeto.pessoa_id == None)
        .all()
    )
    if not pessoa_projeto:
        raise HTTPException(
            status_code=404, detail="pessoa_projeto não encontrada"
        )
    return pessoa_projeto


async def get_pessoa_projeto_by_projeto(
    db: Session, id_projeto: int
) -> t.List[schemas.PessoaProjeto]:
    pessoa_projeto = (
        db.query(models.PessoaProjeto)
        .filter(models.PessoaProjeto.projeto_id == id_projeto)
        .all()
    )
    if not pessoa_projeto:
        raise HTTPException(
            status_code=404, detail="pessoa_projeto não encontrada"
        )
    return pessoa_projeto


async def create_pessoa_projeto(
    db: Session, pessoa_projeto: schemas.PessoaProjetoCreate
) -> schemas.PessoaProjeto:

    try:
        projeto = get_projeto(db, pessoa_projeto.projeto_id)
        if pessoa_projeto.pessoa_id:
            pessoa = get_pessoa(db, pessoa_projeto.pessoa_id)

            db_pessoa_projeto = models.PessoaProjeto(
                pessoa=pessoa,
                projeto=projeto,
                descricao=pessoa_projeto.descricao,
                situacao=pessoa_projeto.situacao,
                titulo=pessoa_projeto.titulo,
                remunerado=pessoa_projeto.remunerado,
                papel_id=pessoa_projeto.papel_id,
                tipo_acordo_id=pessoa_projeto.tipo_acordo_id,
            )
        else:
            db_pessoa_projeto = models.PessoaProjeto(
                projeto=projeto,
                descricao=pessoa_projeto.descricao,
                situacao=pessoa_projeto.situacao,
                titulo=pessoa_projeto.titulo,
                remunerado=pessoa_projeto.remunerado,
                papel_id=pessoa_projeto.papel_id,
                tipo_acordo_id=pessoa_projeto.tipo_acordo_id,
            )

    except HTTPException as e:
        raise e

    db.add(db_pessoa_projeto)
    db.commit()
    db.refresh(db_pessoa_projeto)

    return db_pessoa_projeto
    # db_vaga = db_pessoa_projeto.__dict__
    # return {"id": db_vaga["id"]}


async def edit_pessoa_projeto(
    db: Session,
    pessoa_projeto_id: int,
    pessoa_projeto: schemas.PessoaProjetoEdit,
    pessoa_logada: schemas.Pessoa
) -> schemas.PessoaProjeto:
    db_pessoa_projeto = get_pessoa_projeto(db, pessoa_projeto_id)
    if not db_pessoa_projeto:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="pessoa_projeto não encontrada"
        )
    update_data = pessoa_projeto.dict(exclude_unset=True)

    await append_areas(update_data, db)
    await append_habilidades(update_data, db)

    if "situacao" in update_data.keys():
        create_notificacao_vaga(db, pessoa_logada.id, db_pessoa_projeto)

    for key, value in update_data.items():
        setattr(db_pessoa_projeto, key, value)

    db.add(db_pessoa_projeto)
    db.commit()
    db.refresh(db_pessoa_projeto)

    return db_pessoa_projeto


def delete_pessoa_projeto(db: Session, pessoa_projeto_id: int):
    pessoa_projeto = get_pessoa_projeto(db, pessoa_projeto_id)
    if not pessoa_projeto:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="pessoa_projeto não encontrada"
        )
    db.delete(pessoa_projeto)
    db.commit()
    return pessoa_projeto
