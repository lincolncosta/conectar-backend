from pydantic import BaseModel
import typing as t
from datetime import datetime
from db.habilidade.schemas import PessoaHabilidadeCreate
from db.area.schemas import ProjetoAreaCreate
from db.reacoes.schemas import Reacoes


class ProjetoBase(BaseModel):
    nome: str
    descricao: str
    mural: str
    visibilidade: bool
    objetivo: str
    pessoa_id: t.Optional[int] = None
    foto_capa: t.Optional[str] = None
    areas: t.Optional[t.List[ProjetoAreaCreate]] = None
    habilidades: t.Optional[t.List[PessoaHabilidadeCreate]] = None


class ProjetoOut(ProjetoBase):
    pass


class ProjetoCreate(ProjetoBase):
    class Config:
        orm_mode = True


class ProjetoEdit(ProjetoBase):
    nome: t.Optional[str] = None
    descricao: t.Optional[str] = None
    mural: t.Optional[str] = None
    visibilidade: t.Optional[bool] = None
    objetivo: t.Optional[str] = None

    class Config:
        orm_mode = True


class Projeto(ProjetoBase):
    id: int
    projeto_reacoes: t.Optional[t.List[Reacoes]] = None
    data_criacao: datetime

    class Config:
        orm_mode = True
