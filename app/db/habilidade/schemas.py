from pydantic import BaseModel
import typing as t
from datetime import date


class HabilidadesBase(BaseModel):
    nome: str


class HabilidadesCreate(HabilidadesBase):
    class Config:
        orm_mode = True


class Habilidades(HabilidadesBase):
    id: int

    class Config:
        orm_mode = True


class PessoaHabilidadeCreate(HabilidadesBase):
    id: t.Optional[int] = None
    nome: t.Optional[str] = None

    class Config:
        orm_mode = True


class HabilidadesEdit(HabilidadesBase):
    class Config:
        orm_mode = True
