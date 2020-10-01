from pydantic import BaseModel
import typing as t
from datetime import date


class ExperienciaBase(BaseModel):
    """Common experiencia base"""

    descricao: str
    data_inicio: date
    data_fim: t.Optional[date] = None


class ExperienciaOut(ExperienciaBase):
    pass


class ExperienciaProfCreate(ExperienciaBase):
    cargo: t.Optional[str] = None
    organizacao: t.Optional[str] = None
    vinculo: t.Optional[str] = None

    class Config:
        orm_mode = True


class ExperienciaProfEdit(ExperienciaProfCreate):
    class Config:
        orm_mode = True


class ExperienciaProf(ExperienciaProfCreate):
    id: int
    pessoa_id: int

    class Config:
        orm_mode = True


class ExperienciaAcadCreate(ExperienciaBase):
    escolaridade: str
    instituicao: str
    curso: str
    situacao: t.Optional[str] = None

    class Config:
        orm_mode = True


class ExperienciaAcadEdit(ExperienciaAcadCreate):
    class Config:
        orm_mode = True


class ExperienciaAcad(ExperienciaAcadCreate):
    id: int
    pessoa_id: int

    class Config:
        orm_mode = True


class ExperienciaProjCreate(ExperienciaBase):
    nome: str
    situacao: t.Optional[str] = None
    cargo: t.Optional[str] = None
    
    class Config:
        orm_mode = True


class ExperienciaProjEdit(ExperienciaProjCreate):
    class Config:
        orm_mode = True


class ExperienciaProj(ExperienciaProjCreate):
    id: int
    pessoa_id: int

    class Config:
        orm_mode = True
