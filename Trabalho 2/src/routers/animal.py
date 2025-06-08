from fastapi import APIRouter , Depends , HTTPException
from sqlmodel import Session , select
from src.Models.models import Animal , AnimalBase
from src.Models.models import Client
from src.core.database import get_session
import math
import logging

router = APIRouter(prefix="/animals", tags=["animals"])

@router.get("/", response_model=list[Animal])
def read_animals(session: Session = Depends(get_session)):
    logging.info('Endpoint GET chamado para animais')
    return session.exec(select(Animal)).all()

@router.get("/animals_length")
def length_animals(session : Session = Depends(get_session)):
    logging.info('Quantidade de animais chamado')
    quantidade = session.exec(select(Animal)).all()
    return {"Quantidade" : len(quantidade) }

@router.get("/{animal_id}", response_model=Animal)
def search_animal(animal_id: int, session : Session = Depends(get_session)):
    animal = session.get(Animal, animal_id)
    if not animal:
        logging.error('Animal não encontrado.')
        raise HTTPException(status_code=404, detail="Animal não encontrado.")
    logging.info(f'Animal retornado {animal}')
    return animal

@router.get("/animal/page")
def animal_page(page : int = 1 , page_size:int = 10 , session : Session = Depends(get_session)):
    total_animals = len(session.exec(
        select(Animal)
    ).all())
    total_pages = math.ceil(total_animals/page_size)
    offset = (page - 1) * page_size
    data = session.exec(
        select(Animal).offset(offset).limit(page_size)
    ).all()
    logging.info('GET animais com paginação chamado')
    return{
        "data" : data,
        "total_records" : total_animals,
        "total_pages" : total_pages,
        "current_page" : page
    }

@router.post("/", response_model=Animal)
def create_animal(animal:AnimalBase, session : Session = Depends(get_session)):
    # Pode ser que não precise 
    client = session.get(Client,animal.client_id)
    if not client:
        logging.error('Animal com dono inválido')
        raise HTTPException(status_code=404, detail="Id de cliente passado não existe!")
    db_animal = Animal.from_orm(animal)
    session.add(db_animal)
    session.commit()
    session.refresh(db_animal)
    logging.info(f'Animal criado {db_animal}')
    return db_animal

@router.put("/{animal_id}", response_model=Animal)
def update_animal(animal_id : int, animal : AnimalBase, session : Session = Depends(get_session)):
    db_animal = session.get(Animal, animal_id)
    if not db_animal:
        logging.error('Animal não encontrado')
        raise HTTPException(status_code=404, detail="Animal não encontrado.")
    for key , value in animal.dict().items():
        setattr(db_animal,key,value)
    session.add(db_animal)
    session.commit()
    session.refresh(db_animal)
    logging.info(f'Animal {animal_id} atualizado: {db_animal}')
    return db_animal
    

@router.delete("/{animal_id}")
def delete_animal(animal_id : int, session : Session = Depends(get_session)):
    animal = session.get(Animal, animal_id)
    if not animal:
        logging.error('Animal não encontrado')
        raise HTTPException(status_code=404, detail="Animal não encontrado!")
    session.delete(animal)
    session.commit()
    logging.info(f'Animal {animal_id} deletado: {animal}')
    return {"msg" : "Animal deletado."}