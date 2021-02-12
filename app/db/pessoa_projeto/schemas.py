from pydantic import BaseModel
import typing as t
from datetime import date
from db.area.schemas import Area
from db.habilidade.schemas import Habilidades, PessoaHabilidadeCreate
from db.pessoa.schemas import Pessoa
from db.projeto.schemas import Projeto


class PessoaProjetoBase(BaseModel):
    projeto_id: int
    pessoa_id: t.Optional[int] = None
    papel_id: t.Optional[int]
    tipo_acordo_id: t.Optional[int]
    descricao: t.Optional[str] = None
    situacao: t.Optional[str] = "enviado"
    colaborador: t.Optional[bool] = True


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
    projeto_id: int

    class Config:
        orm_mode = True
