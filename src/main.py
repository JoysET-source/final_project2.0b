from fastapi import FastAPI

from src.routes.user_routes import router as router_ricette_users
from src.routes.todo_routes import router as router_ricette_todo
from src.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router_ricette_users)
app.include_router(router_ricette_todo)

@app.get("/")
async def root():
    return {"message": "Welcome to K.R.O. kitchen recipes organizer API"}
