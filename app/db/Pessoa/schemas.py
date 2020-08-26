from pydantic import BaseModel
import typing as t
from datetime import date


class PessoaBase(BaseModel):
    senha: str
    data_nascimento: t.Optional[date] = None
    email: str
    ativo: bool = True
    # superusuario: bool = False
    nome: t.Optional[str] = None
    telefone: t.Optional[str] = None
    colaborador_id: t.Optional[int] = None
    idealizador_id: t.Optional[int] = None
    aliado_id: t.Optional[int] = None

class PessoaOut(PessoaBase):
    pass


class PessoaCreate(PessoaBase):
    usuario: str

    class Config:
        orm_mode = True


class PessoaEdit(PessoaBase):
    senha: t.Optional[str] = None

    class Config:
        orm_mode = True


class Pessoa(PessoaBase):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str = None
    permission: str = "user"
