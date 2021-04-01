from pydantic import BaseModel
import typing as t

class NotificacaoBase(BaseModel):
    remetente_id: int
    destinatario_id: int
    projeto_id: int
    pessoa_projeto_id: int
    situacao: str
    lido: bool

class NotificacaoCreate(NotificacaoBase):
    situacao: t.Optional[str]

    class Config:
        orm_mode = True

class Notificacao(NotificacaoBase):
    id: int

    class Config:
        orm_mode = True

class NotificacaoEdit(NotificacaoBase):
    remetente_id: t.Optional[int]
    destinatario_id: t.Optional[int]
    projeto_id: t.Optional[int]
    pessoa_projeto_id: t.Optional[int]
    situacao: t.Optional[str]
    lido: t.Optional[bool]

    class Config:
        orm_mode = True