from pydantic import BaseModel
import typing as t
from datetime import date
from db.area.schemas import Area
from db.habilidade.schemas import Habilidades 
from db.pessoa.schemas import Pessoa
from db.projeto.schemas import Projeto

class PessoaProjetoBase(BaseModel):

    projeto_id: int
    pessoa_id: t.Optional[int] = None
    habilidades: t.Optional[t.List[Habilidades]] = None
    areas: t.Optional[t.List[Area]] = None
    # papel_id: t.Optional[int]
    # tipo_acordo_id: t.Optional[int]
    descricao: t.Optional[str] = None
    situacao: t.Optional[str] = "enviado"

class PessoaProjetoOut(PessoaProjetoBase):
    pass


class PessoaProjetoCreate(PessoaProjetoBase):
    
    class Config:
        orm_mode = True

class PessoaProjetoEdit(PessoaProjetoBase):

    pessoa_id: t.Optional[int] = None
    habilidades: t.Optional[t.List[Habilidades]] = None
    areas: t.Optional[t.List[Area]] = None
    descricao: t.Optional[str] = None

    class Config:
        orm_mode = True     
    
class PessoaProjeto(PessoaProjetoBase):
    id: int
    projeto_id: int

    class Config:
        orm_mode = True               
