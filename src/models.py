from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base

class Ricette(Base):
    __tablename__ = "ricette"

    nome_ricetta = Column(String, primary_key=True, unique=True, index=True)
    ingredienti = Column(String, nullable=True, index=True)
    kcal = Column(Integer, index=True)
    todos =relationship("Todo_Ricette", back_populates="relazione_ricette")


class Todo_Ricette(Base):
    __tablename__ = "ricette_todos"

    id = Column(Integer, primary_key=True, index=True)
    ricetta = Column(String, ForeignKey("ricette.nome_ricetta"))
    mise_en_place = Column(String, index=True)
    fase = Column(Integer, index=True)
    procedimento = Column(String, index=True)
    completato = Column(Boolean, default=False)
    relazione_ricette = relationship("Ricette", back_populates="todos")












