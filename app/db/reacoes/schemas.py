from pydantic import BaseModel
import typing as t
from datetime import date


class ReacoesBase(BaseModel):
    reacao: str = "Interesse"


class ReacoesCreate(ReacoesBase):
    pessoa_id: int
    projeto_id: int

    class Config:
        orm_mode = True


class ReacoesEdit(ReacoesBase):
    class Config:
        orm_mode = True


class Reacoes(ReacoesCreate):
    class Config:
        orm_mode = True