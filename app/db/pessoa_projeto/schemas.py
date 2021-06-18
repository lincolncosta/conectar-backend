from pydantic import BaseModel
import typing as t
from datetime import datetime
from db.area.schemas import Area, PessoaAreaCreate
from db.habilidade.schemas import Habilidades, PessoaHabilidadeCreate
from db.pessoa.schemas import Pessoa
from db.projeto.schemas import Projeto


class PessoaProjetoBase(BaseModel):
    projeto_id: int
    remunerado: bool
    titulo: str
    papel_id: t.Optional[int]
    tipo_acordo_id: t.Optional[int]
    pessoa_id: t.Optional[int] = None
    descricao: t.Optional[str] = None
    situacao: t.Optional[str] = "CRIADO"


class PessoaProjetoOut(PessoaProjetoBase):
    habilidades: t.Optional[t.List[PessoaHabilidadeCreate]] = None
    areas: t.Optional[t.List[PessoaAreaCreate]] = None

    class Config:
        orm_mode = True


class PessoaProjetoCreate(PessoaProjetoBase):
    class Config:
        orm_mode = True


class PessoaProjetoEdit(PessoaProjetoOut):
    situacao: t.Optional[str]
    projeto_id: t.Optional[int] = None
    remunerado: t.Optional[bool] = None
    titulo: t.Optional[str] = None
    pessoa_id: t.Optional[int] = None
    
    class Config:
        orm_mode = True


class PessoaProjeto(PessoaProjetoOut):
    id: int
    data_criacao: datetime
    data_atualizacao: t.Optional[datetime] = None

    class Config:
        orm_mode = True
