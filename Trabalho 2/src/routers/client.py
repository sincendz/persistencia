from fastapi import APIRouter , Depends , HTTPException
from sqlmodel import Session, select
from src.Models.models import Client , ClientBase
from src.core.database import get_session

router = APIRouter(prefix="/clients", tags=["clients"])

@router.get("/", response_model=list[Client])
def read_clients(session : Session = Depends(get_session)):
    return session.exec(select(Client)).all()

@router.get("/{client_id}", response_model=Client)
def search_client(client_id, session : Session = Depends(get_session)):
    client = session.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não existe!")
    return client

@router.post("/", response_model=Client)
#Client é do tipo person pois a gente nao vai passar o id
def create_client(client:ClientBase, session : Session = Depends(get_session)):
    db_client = Client.from_orm(client)
    session.add(db_client)
    session.commit()
    session.refresh(db_client)
    return db_client

@router.put("/{client_id}", response_model=Client)
def update_client(client_id:int, client: ClientBase,  session : Session = Depends(get_session)):
    db_client = session.get(Client,client_id)
    if not db_client:
        raise HTTPException(status_code=404,detail="Cliente não existe.")
    for key , value in client.dict().items():
        setattr(db_client, key, value)
    session.add(db_client)
    session.commit()
    session.refresh(db_client)
    return db_client
    
@router.delete("/{client_id}")
def delete_client(client_id : int, session : Session = Depends(get_session)):
    client = session.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente com esse id não existe.")
    session.delete(client)
    session.commit()
    return {"msg" : "Cliente deletado com sucesso!"}