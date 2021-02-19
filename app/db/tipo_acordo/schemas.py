from pydantic import BaseModel
import typing as t


class TipoAcordoBase(BaseModel):
    descricao: str

class TipoAcordoOut(TipoAcordoBase):
    pass


class TipoAcordoCreate(TipoAcordoBase):
    pass


class TipoAcordoEdit(TipoAcordoBase):
    descricao: t.Optional[str] = None

    class Config:
        orm_mode = True


class TipoAcordo(TipoAcordoBase):
    id: int

    class Config:
        orm_mode = True
