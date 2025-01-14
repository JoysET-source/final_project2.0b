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
        fase=todo.fase,
        mise_en_place=todo.mise_en_place,
        procedimento=todo.procedimento,
        completato=todo.completato
    )

    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo









