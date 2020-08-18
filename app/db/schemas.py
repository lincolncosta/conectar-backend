from pydantic import BaseModel
import typing as t


class PessoaBase(BaseModel):
    email: str
    is_active: bool = True
    is_superuser: bool = False
    nome: t.Optional[str] = None
    telefone: t.Optional[str] = None


class PessoaOut(PessoaBase):
    pass


class PessoaCreate(PessoaBase):
    username: str
    password: str

    class Config:
        orm_mode = True


class PessoaEdit(PessoaBase):
    password: t.Optional[str] = None

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
    permissions: str = "user"
