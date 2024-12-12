from pydantic import BaseModel


class Meta(BaseModel):
    new_value: float
    ind: int
    prf: int


class Regua(BaseModel):
    new_value: str
    ind: int
    prf: int
