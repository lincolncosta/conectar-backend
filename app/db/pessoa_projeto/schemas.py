from pydantic import BaseModel
import typing as t
from datetime import datetime
from db.area.schemas import Area
from db.habilidade.schemas import Habilidades, PessoaHabilidadeCreate
from db.pessoa.schemas import Pessoa
from db.projeto.schemas import Projeto


class PessoaProjetoBase(BaseModel):
    projeto_id: t.Optional[int]
    pessoa_id: t.Optional[int] = None
    papel_id: t.Optional[int]
    tipo_acordo_id: t.Optional[int]
    remunerado: t.Optional[bool]
    descricao: t.Optional[str] = None
    titulo: t.Optional[str]
    situacao: t.Optional[str] = "PENDENTE_IDEALIZADOR"
    habilidades: t.Optional[t.List[PessoaHabilidadeCreate]] = None
    areas: t.Optional[t.List[Area]] = None
    data_criacao: t.Optional[datetime]
    data_atualizacao: t.Optional[datetime]
    

class PessoaProjetoOut(PessoaProjetoBase):
    habilidades: t.Optional[t.List[PessoaHabilidadeCreate]] = None
    areas: t.Optional[t.List[Area]] = None
    pass


class PessoaProjetoCreate(PessoaProjetoBase):
    class Config:
        orm_mode = True


class PessoaProjetoEdit(PessoaProjetoOut):
    class Config:
        orm_mode = True


class PessoaProjeto(PessoaProjetoOut):
    id: int
    projeto_id: t.Optional[int]

    class Config:
        orm_mode = True
