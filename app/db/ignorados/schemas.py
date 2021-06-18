from pydantic import BaseModel
import typing as t
from datetime import date

class PessoaIgnoradaVagaBase(BaseModel):
  pessoa_id: int
  pessoa_projeto_id: int

class PessoaIgnoradaVagaCreate(PessoaIgnoradaVagaBase):

  class Config:
        orm_mode = True

class PessoaIgnoradaVaga(PessoaIgnoradaVagaBase):
  id: int

  class Config:
        orm_mode = True

class PessoaIgnoradaVagaEdit(PessoaIgnoradaVagaBase):

  class Config:
        orm_mode = True

