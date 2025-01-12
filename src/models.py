from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base

class Ricette(Base):
    __tablename__ = "ricette"
    nome_ricetta = Column(String, primary_key=True, index=True)
    ingredienti = Column(String, nullable=True, index=True)
    kcal = Column(Integer, unique=True, index=True)

