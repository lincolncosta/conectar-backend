from pydantic import BaseModel
import typing as t
from datetime import date


class AreaBase(BaseModel):
    descricao: str


class AreaCreate(AreaBase):
    area_pai_id: t.Optional[int] = None

    class Config:
        orm_mode = True

class AreaEdit(AreaCreate):
    pass

class Area(AreaBase):
    id: int
    area_pai_id: t.Optional[int] = None

    class Config:
        orm_mode = True