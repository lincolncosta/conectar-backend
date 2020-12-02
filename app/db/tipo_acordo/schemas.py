from pydantic import BaseModel
import typing as t

class TipoAcordoBase(BaseModel):

    descricao: str
    projeto_id: int

class TipoAcordoOut(TipoAcordoBase):
    pass

class TipoAcordoCreate(TipoAcordoBase):

    class Config:
        orm_mode = True


class TipoAcordoEdit(TipoAcordoBase):

    descricao: t.Optional[str] = None

    class Config:
        orm_mode = True  

class TipoAcordo(TipoAcordoBase):
    id: int

    class Config:
        orm_mode = True  