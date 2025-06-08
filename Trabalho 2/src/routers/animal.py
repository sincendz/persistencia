from fastapi import APIRouter , Depends , HTTPException
from sqlmodel import Session , select
from src.Models.models import Animal , AnimalBase
from src.Models.models import Client
from src.core.database import get_session

router = APIRouter(prefix="/animals", tags=["animals"])

@router.get("/", response_model=list[Animal])
def read_animals(session: Session = Depends(get_session)):
    return session.exec(select(Animal)).all()

@router.get("/{animal_id}", response_model=Animal)
def search_animal(animal_id: int, session : Session = Depends(get_session)):
    animal = session.get(Animal, animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal não encontrado.")
    return animal

@router.post("/", response_model=Animal)
def create_animal(animal:AnimalBase, session : Session = Depends(get_session)):
    # Pode ser que não precise 
    client = session.get(Client,animal.client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Id de cliente passado não existe!")
    db_animal = Animal.from_orm(animal)
    session.add(db_animal)
    session.commit()
    session.refresh(db_animal)
    return db_animal

@router.put("/{animal_id}", response_model=Animal)
def update_animal(animal_id : int, animal : AnimalBase, session : Session = Depends(get_session)):
    db_animal = session.get(Animal, animal_id)
    if not db_animal:
        raise HTTPException(status_code=404, detail="Animal não encontrado.")
    for key , value in animal.dict().items():
        setattr(db_animal,key,value)
    session.add(db_animal)
    session.commit()
    session.refresh(db_animal)
    return db_animal
    

@router.delete("/{animal_id}")
def delete_animal(animal_id : int, session : Session = Depends(get_session)):
    animal = session.get(Animal, animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal não encontrado!")
    session.delete(animal)
    session.commit()
    return {"msg" : "Animal deletado."}