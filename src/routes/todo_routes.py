from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.database import get_db
from src.models import Todo_Ricette, Ricette
from src.schemas.todo_schemas import TodoCreate, Todo as TodoSchema
from src.schemas.user_schemas import Ricetta

router = APIRouter(prefix="/todo", tags=["TODOS"])


@router.post("/", response_model=TodoSchema)
def crea_todo(ricetta: str, todo: TodoCreate, db: Session = Depends(get_db)):
    db_ricetta = db.query(Ricette).filter(Ricette.nome_ricetta == ricetta).first()
    if not db_ricetta:
        raise HTTPException(status_code=400, detail="Ricetta non trovata nel database")
    db_todo = db.query(Todo_Ricette).filter(Todo_Ricette.ricetta == ricetta, Todo_Ricette.fase == todo.fase).first()
    if db_todo:
        raise HTTPException(status_code=400, detail="Fase gia creata!")

    db_todo = Todo_Ricette(
        ricetta=ricetta,
        mise_en_place=todo.mise_en_place,
        fase=todo.fase,
        procedimento=todo.procedimento,
        completato=todo.completato
    )

    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


@router.get("/fasi ricetta", response_model=List[TodoSchema])
def show_todos(ricetta: str, db: Session = Depends(get_db)):
    db_todo = db.query(Todo_Ricette).filter(Todo_Ricette.ricetta == ricetta).all()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Ricetta e fasi non trovate")
    return db_todo


@router.get("/singola fase ricetta", response_model=TodoSchema)
def show_fase(ricetta: str, fase: int, db: Session = Depends(get_db)):
    db_ricetta = db.query(Ricette).filter(Ricette.nome_ricetta == ricetta).first()
    if not db_ricetta:
        raise HTTPException(status_code=400, detail="Ricetta non trovata nel database")
    db_todo = db.query(Todo_Ricette).filter(Todo_Ricette.ricetta == ricetta, Todo_Ricette.fase == fase).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Fase non trovata")
    return db_todo


@router.put("/ricetta", response_model=TodoSchema)
def modifica_todo(ricetta: str, fase: int, todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = db.query(Todo_Ricette).filter(Todo_Ricette.ricetta == ricetta, Todo_Ricette.fase == fase).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Ricetta non trovata")

    for key, value in fase.dict().items():
        setattr(db_todo, key, value)

    db.commit()
    db.refresh(db_todo)
    return db_todo


@router.delete("/{ricetta}")
def delete_todo(ricetta: str, db: Session = Depends(get_db)):
    db_todo = db.query(Todo_Ricette).filter(Todo_Ricette.ricetta == ricetta).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Ricetta non esiste")

    db.delete(db_todo)
    db.commit()
    return {"message": "Ricetta cancellata"}


@router.delete("/cancella fase/ricetta/fase")
def delete_fase(ricetta: str, fase: int, db: Session = Depends(get_db)):
    db_todo = db.query(Todo_Ricette).filter(Todo_Ricette.ricetta == ricetta, Todo_Ricette.fase == fase).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Fase non trovata!")

    db.delete(db_todo)
    db.commit()
    return {"message": "Fase cancellata"}


































































