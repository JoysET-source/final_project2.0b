from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.database import get_db
from src.models import Todo_Ricette
from src.schemas.todo_schemas import TodoCreate, Todo as TodoSchema


router = APIRouter(prefix="/todo", tags=["TODOS"])


@router.post("/", response_model=TodoSchema)
def crea_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = db.query(Todo_Ricette).filter(Todo_Ricette.ricetta == todo.ricetta, Todo_Ricette.fase == todo.fase).first()
    if db_todo:
        raise HTTPException(status_code=400, detail="todo esistente per questa ricetta e fase")

    db_todo = Todo_Ricette(
        ricetta=todo.ricetta,
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
    db_todo = db.query(Todo_Ricette).filter(Todo_Ricette.ricetta == todo.ricetta).all()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Ricetta e fasi non trovate")
    return db_todo


@router.get("/singola fase ricetta", response_model=TodoSchema)
def show_fase(ricetta: str, fase: int, db: Session = Depends(get_db)):
    db_todo = db.query(Todo_Ricette).filter(Todo_Ricette.ricetta == todo.ricetta, Todo_Ricette.fase == todo.fase).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Fase non trovata")
    return db_todo


@router.put("/{ricetta}", response_model=TodoSchema)
def modifica_ricetta(ricetta: str, db: Session = Depends(get_db)):
    pass



@router.delete("/{ricetta}")
def delete_ricetta(ricetta: str, db: Session = Depends(get_db)):
    db_todo = db.query(Todo_Ricette).filter(Todo_Ricette.ricetta == ricetta).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Ricetta non esiste")

    db.delete(db_todo)
    db.commit()
    return {"message": "Ricetta cancellata"}


@router.delete("/cancella fase/{ricetta}")
def delete_fase(ricetta: str, fase: int, db: Session = Depends(get_db)):
    db_todo = db.query(Todo_Ricette).filter(Todo_Ricette.ricetta == ricetta, Todo_Ricette.fase == fase).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Fase non trovata!")

    db.delete(db_todo)
    db.commit()
    return {"message": "Fase cancellata"}





























































