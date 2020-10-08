from pydantic import BaseModel
import typing as t
from datetime import date

class HabilidadesBase(BaseModel):
  nome: str

class HabilidadesOut(HabilidadesBase):
    pass

class HabilidadesCreate(HabilidadesBase):
  nome: str

  class Config:
        orm_mode = True

class Habilidades(HabilidadesCreate):
  id: int

  class Config:
        orm_mode = True
        
class PessoaHabilidadeCreate(Habilidades):
    nome: t.Optional[str] = None

    class Config:
        orm_mode = True

class HabilidadesEdit(HabilidadesCreate):
  nome: str

  class Config:
        orm_mode = True

