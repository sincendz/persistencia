from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from src.Models.models import (
    Consultation,
    ConsultationBase,
    Animal,
    Veterinary,
    Service,
)
from src.core.database import get_session
from datetime import date
import math
import logging

router = APIRouter(prefix="/consultation", tags=["consultation"])


@router.get("/", response_model=list[Consultation])
def read_consultation(session: Session = Depends(get_session)):
    logging.info("Endpoint GET chamado para consultas")
    return session.exec(select(Consultation)).all()


@router.get("/search/{consultation_id}", response_model=Consultation)
def search_consultation_by_id(
    consultation_id: int, session: Session = Depends(get_session)
):
    consultation = session.get(Consultation, consultation_id)
    if not consultation:
        logging.error("Consulta não encontrada.")
        raise HTTPException(status_code=404, detail="Consulta não encontrada.")
    logging.info(f"Consulta retornada {consultation}")
    return consultation


@router.get("/consultation_services/{consultation_id}")
def consultation_services(
    consultation_id: int, session: Session = Depends(get_session)
):
    consult = session.get(Consultation, consultation_id)
    if not consult:
        logging.error("Consulta não encontrada.")
        raise HTTPException(status_code=404, detail="Consulta não encontrada.")
    total = 0
    for service in consult.services:
        total += service.price
    pago = "Não" if consult.data_out == None else "Sim"
    logging.info("Endpoint GET chamado para consultas e serviços")
    return {"Serviços": consult.services, "Preço total": total, "Pago ": pago}


@router.get("/length_consultation")
def consultation_length(session: Session = Depends(get_session)):
    logging.info("Quantidade de consultas chamado")
    return {"Quantidade": len(session.exec(select(Consultation)).all())}


@router.get("/page")
def consultation_page(
    page: int = 1, page_size: int = 10, session: Session = Depends(get_session)
):
    total_consultation = len(session.exec(select(Consultation)).all())
    total_page = math.ceil(total_consultation / page_size)
    offset = (page - 1) * page_size
    data = session.exec(select(Consultation).offset(offset).limit(page_size)).all()
    logging.info("GET consultas com paginação chamado")
    return {
        "data": data,
        "total_records": total_consultation,
        "total_pages": total_page,
        "current_page": page,
    }


@router.post("/{consultation_id}/add_service/{service_id}")
def add_service_to_consultation(
    consultation_id: int, service_id: int, session: Session = Depends(get_session)
):
    consultation = session.get(Consultation, consultation_id)
    if not consultation:
        logging.error("Consulta não encontrada.")
        raise HTTPException(status_code=404, detail="Consulta não encontrada.")
    service = session.get(Service, service_id)
    if not service:
        logging.error("Serviço não encontrado.")
        raise HTTPException(status_code=404, detail="Serviço não encontrado.")
    consultation.services.append(service)
    session.add(consultation)
    session.commit()
    session.refresh(consultation)
    logging.info(f"Serviço {service} adicionado a consulta {consultation}")
    return {"Consulta ": consultation, "Serviços": consultation.services}


@router.post("/", response_model=Consultation)
def create_consultation(
    consultation: ConsultationBase, session: Session = Depends(get_session)
):
    animal = session.get(Animal, consultation.animal_id)
    if not animal:
        logging.error("Animal não encontrado.")
        raise HTTPException(status_code=404, detail="Animal não encontrado.")
    vet = session.get(Veterinary, consultation.vet_id)
    if not vet:
        logging.error("Veterinário não encontrado.")
        raise HTTPException(status_code=404, detail="Veterinário não encontrado.")
    consultation = Consultation.from_orm(consultation)
    session.add(consultation)
    session.commit()
    session.refresh(consultation)
    logging.info(f"Consulta criada {consultation}")
    return consultation


@router.put("/{consultation_id}", response_model=Consultation)
def update_consultation(
    consultation_id: int,
    consultation: ConsultationBase,
    session: Session = Depends(get_session),
):
    db_consultation = session.get(Consultation, consultation_id)
    if not db_consultation:
        logging.error("Consulta não encontrada.")
        raise HTTPException(status_code=404, detail="Consulta não encontrada.")
    if db_consultation.data_out != None:
        logging.error("Consulta não encerrada não alterada.")
        raise HTTPException(
            status_code=403,
            detail="Não é possivel alterar uma consulta que já foi encerrada.",
        )
    for key, value in consultation.dict().items():
        setattr(db_consultation, key, value)
    db_consultation.updated_at = date.today()
    session.add(db_consultation)
    session.commit()
    session.refresh(db_consultation)
    logging.info(f"Consulta {consultation_id} atualizado: {db_consultation}")
    return db_consultation


@router.delete("/{consultation_id}")
def delete_consultation(consultation_id: int, session: Session = Depends(get_session)):
    consultation = session.get(Consultation, consultation_id)
    if not consultation:
        logging.error("Consulta não encontrada.")
        raise HTTPException(status_code=404, detail="Consulta não encontrada.")
    session.delete(consultation)
    session.commit()
    logging.info(f"Consulta {consultation_id} deletada: {consultation}")
    return {"msg": "Consulta apagada!"}


@router.put("/end/{consultation_id}", response_model=Consultation)
def end_consultation(consultation_id: int, session: Session = Depends(get_session)):
    consultation = session.get(Consultation, consultation_id)
    if not consultation:
        logging.error("Consulta não encontrada.")
        raise HTTPException(status_code=404, detail="Consulta não encontrada.")
    consultation.data_out = date.today()
    session.add(consultation)
    session.commit()
    session.refresh(consultation)
    logging.info(f"Data de término {date.today()} adicionado a consulta {consultation}")
    return consultation
