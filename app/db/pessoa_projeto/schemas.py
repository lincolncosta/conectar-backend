from pydantic import BaseModel
import typing as t
from datetime import date
from app.db.area.schemas import Area
from app.db.habilidade.schemas import Habilidades 
from app.db.pessoa.schemas import Pessoa
from app.db.projeto.schemas import Projeto

class PessoaProjetoBase(BaseModel):

    projeto: Projeto
    pessoa: t.Optional[Pessoa] = None
    habilidades: t.Optional[t.List[Habilidades]] = None
    areas: t.Optional[t.List[Area]] = None
    #papel_id: t.Optional[int]
    #tipo_acordo_id: t.Optional[int]
    descricao: t.Optional[str] = None
    situacao: t.Optional[str] = "enviado"

class PessoaProjetoOut(PessoaProjetoBase):
    pass

class PessoaProjetoCreate(PessoaProjetoBase):

    class Config:
        orm_mode = True


class PessoaProjetoEdit(PessoaProjetoBase):

    projeto: t.Optional[Projeto] = None

    class Config:
        orm_mode = True     

class PessoaProjeto(PessoaProjetoBase):
    id: int

    class Config:
        orm_mode = True               
