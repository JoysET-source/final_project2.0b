from fastapi import FastAPI
from src.routes import router as router_ricette
from src.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router_ricette)

@app.get("/")
async def root():
    return {"message": "Welcome to K.R.O. kitchen recipes organizer API"}
