from pydantic import BaseModel


class ReacoesBase(BaseModel):
    reacao: str = "FAVORITO"


class ReacoesCreate(ReacoesBase):
    pessoa_id: int
    projeto_id: int

    class Config:
        orm_mode = True


class ReacoesEdit(ReacoesBase):
    class Config:
        orm_mode = True


class Reacoes(ReacoesCreate):

    id: int

    class Config:
        orm_mode = True