from fastapi import FastAPI
from src.routers.client import router as client_router
from src.routers.animal import router as animal_router
from src.routers.service import router as service_router
from src.core.database import create_db_and_tables
from src.core.loggingInit import Logs, logging

routs = [client_router,animal_router,service_router]

app = FastAPI()
log = Logs()


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
    
for rout in routs:
    app.include_router(rout)    