from pydantic import BaseModel
import typing as t
from datetime import date
from app.db.area.schemas import PessoaAreaCreate
from app.db.habilidade.schemas import PessoaHabilidadeCreate 

class PessoaBase(BaseModel):
    data_nascimento: t.Optional[date] = None
    email: str
    ativo: bool = True
    nome: t.Optional[str] = None
    telefone: t.Optional[str] = None
    colaborador: t.Optional[bool] = None
    idealizador: t.Optional[bool] = None
    aliado: t.Optional[bool] = None
    foto_perfil: t.Optional[str] = None
    habilidades: t.Optional[t.List[PessoaHabilidadeCreate]] = None
    areas: t.Optional[t.List[PessoaAreaCreate]] = None

class PessoaOut(PessoaBase):
    pass


class PessoaCreate(PessoaBase):
    senha: str
    superusuario: t.Optional[bool] = False
    usuario: str

    class Config:
        orm_mode = True


class PessoaEdit(PessoaBase):
    senha: t.Optional[str] = None
    email: t.Optional[str] = None


    class Config:
        orm_mode = True


class Pessoa(PessoaBase):
    id: int
    data_criacao: date
    data_atualizacao: t.Optional[date] = None

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str = None
    permission: str = "user"
