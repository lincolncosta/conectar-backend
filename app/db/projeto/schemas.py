from pydantic import BaseModel
import typing as t
from datetime import date
from app.db.area.schemas import ProjetoAreaCreate

class ProjetoBase(BaseModel):
    nome: str
    descricao: str
    visibilidade: bool
    objetivo: str
    areas: t.Optional[t.List[ProjetoAreaCreate]] = None

class ProjetoOut(ProjetoBase):
    pass    

class ProjetoCreate(ProjetoBase):

    class Config:
        orm_mode = True     

class Projeto(ProjetoBase):
    id: int

    class Config:
        orm_mode = True               
