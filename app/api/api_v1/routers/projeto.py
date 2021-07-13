from fastapi import (
    APIRouter,
    Request,
    Depends,
    Response,
    UploadFile,
    File,
    Form,
    HTTPException,
    status
)
import typing as t

from db.session import get_db
from db.projeto.crud import (
    create_projeto,
    get_projetos,
    get_projeto,
    get_projeto_reacao,
    delete_projeto,
    edit_projeto,
    edit_foto_projeto,
    get_projetos_destaque,
    get_projeto_participando,
)
from db.projeto.schemas import Projeto, ProjetoEdit
from core.auth import get_current_active_pessoa

projeto_router = r = APIRouter()


@r.get(
    "/projetos",
    response_model=t.List[Projeto],
    response_model_exclude_none=True,
)
async def projetos_list(
    response: Response,
    db=Depends(get_db),
    visibilidade: t.Optional[bool] = True,
    skip: t.Optional[int] = 0,
    limit: t.Optional[int] = 100,
    pessoa_id: t.Optional[int] = None
):
    """
    Get all projetos
    """
    projetos = get_projetos(db, skip, limit, visibilidade, pessoa_id)
    # This is necessary for react-admin to work
    # response.headers["Content-Range"] = f"0-9/{len(projetos)}"
    return projetos


@r.get(
    "/projeto/{projeto_id}",
    response_model=Projeto,
    response_model_exclude_none=True,
)
async def projeto_details(
    request: Request,
    projeto_id: int,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Get any pessoa details
    """
    projeto = get_projeto(db, projeto_id)
    return projeto

@r.get(
    "/projeto/participando/{participante_id}",
    response_model=t.List[Projeto],
    response_model_exclude_none=True,
)
async def projeto_colaborador(
    request: Request,
    participante_id: int,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    
    return await get_projeto_participando(db, participante_id)


@r.get(
    "/projeto/destaque/{qtd_projetos}",
    response_model=t.List[Projeto],
    response_model_exclude_none=True,
)
async def projetos_destaque(
    request: Request,
    qtd_projetos: int,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Get N projetos destaque
    """
    projetos = get_projetos_destaque(db, qtd_projetos)    
    return projetos

@r.get(
    "/projeto/reacao/{pessoa_id}",
    response_model=t.List[Projeto],
    response_model_exclude_none=True,
)
async def projeto_reacoes(
    request: Request,
    pessoa_id: int,
    reacao: str,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    
    projetos = get_projeto_reacao(db, pessoa_id, reacao)
    
    return projetos


@r.post("/projeto", response_model_exclude_none=True)
async def projeto_create(
    request: Request,
    db=Depends(get_db),
    nome: str = Form(...),
    descricao: str = Form(...),
    visibilidade: bool = Form(...),
    objetivo: str = Form(...),
    pessoa_id: int = Form(None),
    foto_capa: t.Optional[UploadFile] = File(None),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Create a new projeto
    """
    try:
        projeto = await create_projeto(
            db,
            nome=nome,
            descricao=descricao,
            visibilidade=visibilidade,
            objetivo=objetivo,
            foto_capa=foto_capa,
            pessoa_id=pessoa_id,
        )
        return projeto
    except Exception as e:
        raise e


@r.put(
    "/projeto/{projeto_id}",
    response_model=Projeto,
    response_model_exclude_none=True,
)
async def projeto_edit(
    request: Request,
    projeto: ProjetoEdit,
    projeto_id: int,
    db=Depends(get_db)
):

    return await edit_projeto(db, projeto_id, projeto)

@r.put(
    "/projeto/foto/{projeto_id}",
    response_model=Projeto,
    response_model_exclude_none=True,
)
async def projeto_foto_edit(
    request: Request,
    projeto_id: int,
    foto_capa: UploadFile = File(...),
    db=Depends(get_db)
):

    return await edit_foto_projeto(db, projeto_id, foto_capa)

@r.delete(
    "/projeto/{projeto_id}",
    response_model=Projeto,
    response_model_exclude_none=True,
)
async def projeto_delete(
    request: Request,
    projeto_id: int,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Delete existing projeto
    """
    projeto = get_projeto(db, projeto_id)
    if projeto.pessoa_id == current_pessoa.id:
        return delete_projeto(db, projeto_id)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Este projeto não é seu!'
        )
