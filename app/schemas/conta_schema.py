from pydantic import BaseModel

class ContaCreate(BaseModel):
    id: int
    nome: str
    saldo: float = 0.0


class ContaResponse(BaseModel):
    id: int
    nome: str
    saldo: float

    class Config:
        from_attributes = True