from pydantic import BaseModel


class Meta(BaseModel):
    new_value: float
    ind: int
    prf: int


class Regua(BaseModel):
    vl: float
    qt: float
    ind: int
    prf: int
