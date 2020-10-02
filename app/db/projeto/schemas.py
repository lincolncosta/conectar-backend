from pydantic import BaseModel
import typing as t
from datetime import date


class ProjetoBase(BaseModel):
    nome: str
    descricao: str
    visibilidade: bool
    objetivo: str

class ProjetoOut(ProjetoBase):
    pass    

class ProjetoCreate(ProjetoBase):
    nome: str

    class Config:
        orm_mode = True     

class Projeto(ProjetoBase):
    id: int

    class Config:
        orm_mode = True               
