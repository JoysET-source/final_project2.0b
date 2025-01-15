from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.database import get_db
from src.schemas.user_schemas import RicettaCreate, Ricetta as RicetteSchema
from src.models import Ricette

router = APIRouter(prefix="/Ricetta", tags=["RICETTE"])

@router.post("/", response_model=RicetteSchema)
def scrivi_ricetta(ricetta: RicettaCreate, db: Session = Depends(get_db)):
    db_ricetta = db.query(Ricette).filter(Ricette.nome_ricetta == ricetta.nome_ricetta).first()
    if db_ricetta:
        raise HTTPException(status_code=400, detail="Ricetta gia esistente")
    db_ricetta = Ricette(
        nome_ricetta=ricetta.nome_ricetta,
        ingredienti=ricetta.ingredienti,
        kcal=ricetta.kcal
    )
    db.add(db_ricetta)
    db.commit()
    db.refresh(db_ricetta)
    return db_ricetta

@router.get("/tutte ricette", response_model=List[RicetteSchema])
def elenco_ricette(db: Session = Depends(get_db)):
    db_ricetta = db.query(Ricette).all()
    if not db_ricetta :
        raise HTTPException(status_code=404, detail="Non ci sono ricette nel tuo organizer")
    return db_ricetta


@router.get("/cerca ricetta", response_model=RicetteSchema)
def trova_ricetta(nome_ricetta: str, db: Session = Depends(get_db)):
    db_ricetta = db.query(Ricette).filter(Ricette.nome_ricetta == nome_ricetta).first()
    if db_ricetta is None:
        raise HTTPException(status_code=404, detail="Ricetta non trovata")
    return db_ricetta


@router.get("/{nome_ricetta}", response_model=List[RicetteSchema])
def apporto_calorie(kcal: int, db: Session = Depends(get_db)):
    db_ricetta = db.query(Ricette).filter(Ricette.kcal == kcal).all()
    if not db_ricetta :
        raise HTTPException(status_code=404, detail="Non ci sono ricette con le kcal specificate")
    return db_ricetta


@router.put("/{nome_ricetta}", response_model=RicetteSchema)
def modifica_ricetta(nome_ricetta: str, ricetta: RicettaCreate, db: Session = Depends(get_db)):
    db_ricetta = db.query(Ricette).filter(Ricette.nome_ricetta == nome_ricetta).first()
    if db_ricetta is None:
        raise HTTPException(status_code=404, detail="Ricetta non trovata")

    for key, value in ricetta.dict().items():
        setattr(db_ricetta, key, value)

    db.commit()
    db.refresh(db_ricetta)
    return db_ricetta

@router.delete("/{nome_ricetta}")
def cancella_ricetta(nome_ricetta: str, db: Session = Depends(get_db)):
    db_ricetta = db.query(Ricette).filter(Ricette.nome_ricetta == nome_ricetta).first()
    if db_ricetta is None:
        raise HTTPException(status_code=404, detail="Ricetta non trovata")

    db.delete(db_ricetta)
    db.commit()
    return {"message": "Ricetta cancellata"}


















