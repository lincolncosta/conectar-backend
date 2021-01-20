from pydantic import BaseModel
import typing as t
from datetime import date

class PapelBase(BaseModel):
  descricao: str

class PapelCreate(PapelBase):

  class Config:
        orm_mode = True

class Papel(PapelBase):
  id: int

  class Config:
        orm_mode = True

class PapelEdit(PapelBase):

  class Config:
        orm_mode = True

