from pydantic import BaseModel

class TodoBase(BaseModel):
    mise_en_place: str
    procedimento: str
    completato: bool = False

class TodoCreate(TodoBase):
    ricetta: str
    fase: int

class Todo(TodoBase):
    ricetta: str

    class Config:
        orm_mode = True








