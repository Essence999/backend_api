from pydantic import BaseModel


class Card(BaseModel):
    cd: int
    name: str
    vl: float
    qt: float
    meta: float
    version: int
