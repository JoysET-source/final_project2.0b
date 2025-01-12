from pydantic import BaseModel

class RicettaBase(BaseModel):
    nome_ricetta: str
    ingredienti: str
    kcal: int

class RicettaCreate(RicettaBase):
    nome_ricetta: str

class Ricetta(RicettaBase):
    nome_ricetta: str


