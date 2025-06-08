from fastapi import FastAPI
from src.routers.client import router as client_router
from src.routers.animal import router as animal_router
from src.core.database import create_db_and_tables

app = FastAPI()

@app.get("/root")
def hello_world():
    return {"msg": "Hello world!!"}
@app.get("/create_db")
def create_db():
    try:
        create_db_and_tables()
        return {"msg" : "Banco de dado e tabelas criadas"}
    except Exception as e:
        return {"Erro" : str(e)}
    
app.include_router(client_router)
app.include_router(animal_router)