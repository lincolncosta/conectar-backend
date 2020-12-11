from pydantic import BaseModel
import typing as t
from datetime import date
from db.area.schemas import Area
from db.habilidade.schemas import Habilidades 
from db.pessoa.schemas import Pessoa
from db.projeto.schemas import Projeto

class PessoaProjetoBase(BaseModel):
    projeto: int
    pessoa: t.Optional[Pessoa] = None
    habilidades: t.Optional[t.List[Habilidades]] = None
    areas: t.Optional[t.List[Area]] = None
    # papel_id: t.Optional[int]
    # tipo_acordo_id: t.Optional[int]
    descricao: t.Optional[str] = None
    situacao: t.Optional[str] = "enviado"

class PessoaProjetoOut(PessoaProjetoBase):
    pass


class PessoaProjetoCreate(PessoaProjetoBase):
    pessoa: t.Optional[int] = None
    class Config:
        orm_mode = True


class PessoaProjetoEdit(PessoaProjetoBase):

    class Config:
        orm_mode = True     

class PessoaProjeto(PessoaProjetoBase):
    id: int
    projeto: Projeto

    class Config:
        orm_mode = True               
