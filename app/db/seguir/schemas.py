from pydantic import BaseModel

class SeguirCreate(BaseModel):
    seguido_id: int
    seguidor_id: int

class Seguir(BaseModel):
    id: int
    
