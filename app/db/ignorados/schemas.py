from pydantic import BaseModel


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

