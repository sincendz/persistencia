from fastapi import APIRouter , Depends , HTTPException
from sqlmodel import Session, select
from src.Models.models import Veterinary, VeterinaryBase, Crmv , Consultation
from src.core.database import get_session
import math
import logging

router = APIRouter(prefix="/veterinarios", tags=["veterinarios"])

@router.get("/", response_model=list[Veterinary])
def read_veterinaries(session : Session = Depends(get_session)):
    logging.info('Endpoint GET chamado para veterinarios')
    return session.exec(select(Veterinary)).all()

@router.get("/search/{veterinary_id}", response_model=Veterinary)
def search_veterinary_by_id(veterinary_id, session : Session = Depends(get_session)):
    veterinary = session.get(Veterinary, veterinary_id)
    if not veterinary:
        logging.error('Veterinário não encontrado.')
        raise HTTPException(status_code=404, detail="Veterinário não existe!")
    logging.info(f'Veterinário retornado {veterinary}')
    return veterinary

@router.get("/search_name/{vet_name}", response_model=list[Veterinary])
def search_veterinary_by_name(vet_name: str, session : Session = Depends(get_session)):
    vets = session.exec(
        select(Veterinary).where(Veterinary.name.ilike(f"%{vet_name}%"))
    ).all()
    if not vets:
        raise HTTPException(status_code=404, detail="Veterinario não encontrado.")
    return vets

@router.get("/veterinaries_length")
def length_veterinaries(session : Session = Depends(get_session)):
    logging.info('Quantidade de veterinários chamado')
    return {"Quantidade " : len(session.exec(select(Veterinary)).all())}

@router.get("/page")
def veterinaries_page(page:int = 1, page_size:int = 10, session : Session = Depends(get_session)):
    total_veterinaries = len(session.exec(select(Veterinary)).all())
    total_pages = math.ceil(total_veterinaries/page_size)
    offset = (page - 1) * page_size
    data = session.exec(
        select(Veterinary).offset(offset).limit(page_size)
    ).all()
    logging.info('GET veterinários com paginação chamado')
    return {
        "data" : data,
        "total_records" : total_veterinaries,
        "total_pages" : total_pages,
        "current_page": page
    }
    
@router.get("/veterinaries/consultations/{veterinary_id}")
def open_consultations_for_a_vet(veterinary_id:int, session : Session = Depends(get_session)):
    if not session.get(Veterinary,veterinary_id):
        logging.error('Veterinário não encontrado.')
        raise HTTPException(status_code=404, detail ="Veterinário não encontrado.")
    logging.info(f'Retornado as consultas com o veterinário {veterinary_id}')
    return session.exec(
        select(Consultation).where(Consultation.vet_id == veterinary_id).where(Consultation.data_out == None)
    ).all()

@router.post("/", response_model=Veterinary)
def create_veterinary(veterinary:VeterinaryBase, session : Session = Depends(get_session)):
    
    db_veterinary = Veterinary.from_orm(veterinary)
    logging.info(veterinary.crmv_id)
    crmv = session.get(Crmv,veterinary.crmv_id)
    crmv_vet = session.exec(
        select(Veterinary).where(Veterinary.crmv_id == veterinary.crmv_id)
    ).first()

    if not crmv:
        logging.error('Veterinário com crmv inválido')
        raise HTTPException(status_code=404, detail="Crmv de veterinário passado não existe!")

    if crmv_vet:
        logging.info("CRMV já atrelado a um veterinario")
        raise HTTPException(status_code=403, detail="CRMV já pertence a outro veterinário.")
    
    session.add(db_veterinary)
    session.commit()
    session.refresh(db_veterinary)
    logging.info(f'Veterinário criado {db_veterinary}')
    return db_veterinary

@router.put("/{veterinary_id}", response_model=Veterinary)
def update_veterinary(veterinary_id:int, veterinary: VeterinaryBase,  session : Session = Depends(get_session)):
    
    db_veterinary = session.get(Veterinary,veterinary_id)
    
    crmv = session.get(Crmv,veterinary.crmv_id)
    
    if not db_veterinary:
        logging.error('Veterinário não encontrado')
        raise HTTPException(status_code=404,detail="Veterinário não existe.")
    
    if not crmv:
        logging.error('Veterinário com crmv inválido')
        raise HTTPException(status_code=404, detail="Crmv de veterinário passado não existe!")
    
    for key , value in veterinary.dict().items():
        setattr(db_veterinary, key, value)
    session.add(db_veterinary)
    session.commit()
    session.refresh(db_veterinary)
    logging.info(f'Veterinário {veterinary_id} atualizado: {db_veterinary}')
    return db_veterinary

@router.delete("/{veterinary_id}")
def delete_veterinary(veterinary_id : int, session : Session = Depends(get_session)):
    veterinary = session.get(Veterinary, veterinary_id)
    if not veterinary:
        logging.error('Veterinário não encontrado')
        raise HTTPException(status_code=404, detail="Veretinário com esse id não existe.")
    session.delete(veterinary)
    session.commit()
    logging.info(f'Veterinário {veterinary_id} deletado: {veterinary}')
    return {"msg" : "Veterinário deletado com sucesso!"}