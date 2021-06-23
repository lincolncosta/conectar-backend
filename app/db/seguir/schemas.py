from pydantic import BaseModel


class Seguir(BaseModel):
    id: int
    seguido_id: int
    seguidor_id: int
