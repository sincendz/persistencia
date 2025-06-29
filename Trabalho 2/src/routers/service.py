from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from src.Models.models import Service, ServiceBase
from src.core.database import get_session
import math
import logging

router = APIRouter(prefix="/services", tags=["services"])


@router.get("/", response_model=list[Service])
def read_services(session: Session = Depends(get_session)):
    logging.info("Endpoint GET chamado para serviços")
    return session.exec(select(Service)).all()


@router.get("/search/{service_id}", response_model=Service)
def search_service_by_id(service_id: int, session: Session = Depends(get_session)):
    service = session.get(Service, service_id)
    if not service:
        logging.error("Serviço não encontrado")
        raise HTTPException(status_code=404, detail="Serviço não encontrado.")
    logging.info(f"Serviço retornado {service}")
    return service


@router.get("/search_by_name/{name}", response_model=list[Service])
def search_service_by_name(name_service: str, session: Session = Depends(get_session)):
    services = session.exec(
        select(Service).where(Service.service_name.ilike(f"%{name_service}%"))
    ).all()

    if not services:
        raise HTTPException(status_code=404, detail="Nenhum serviço encontrado.")

    return services


@router.get("/services_length")
def length_service(session: Session = Depends(get_session)):
    logging.info("Quantidade de serviços chamado")
    return {"Quantidade ": len(session.exec(select(Service)).all())}


@router.get("/services/page")
def service_page(
    page: int = 1, page_size: int = 10, session: Session = Depends(get_session)
):
    total_services = len(session.exec(select(Service)).all())
    total_pages = math.ceil(total_services / page_size)
    offset = (page - 1) * page_size
    data = session.exec(select(Service).offset(offset).limit(page_size)).all()
    logging.info("GET serviços com paginação chamado")
    return {
        "data": data,
        "total_records": total_services,
        "total_pages": total_pages,
        "current_page": page,
    }


@router.post("/", response_model=Service)
def create_service(service: ServiceBase, session: Session = Depends(get_session)):
    db_service = Service.from_orm(service)
    session.add(db_service)
    session.commit()
    session.refresh(db_service)
    logging.info(f"Serviço criado {db_service}")
    return db_service


@router.put("/{service_id}", response_model=Service)
def update_service(
    service_id: int, service: ServiceBase, session: Session = Depends(get_session)
):
    db_service = session.get(Service, service_id)
    if not db_service:
        logging.error("Serviço não encontrado")
        raise HTTPException(status_code=404, detail="Serviço não encontrado.")
    for key, value in service.dict().items():
        setattr(db_service, key, value)
    session.add(db_service)
    session.commit()
    session.refresh(db_service)
    logging.info(f"Serviço {service_id} atualizado: {db_service}")
    return db_service


@router.delete("/{service_id}")
def delete_service(service_id: int, session: Session = Depends(get_session)):
    service = session.get(Service, service_id)
    if not service:
        logging.error("Serviço não encontrado")
        raise HTTPException(status_code=404, detail="Serviço não encontrado.")
    session.delete(service)
    session.commit()
    logging.info(f"Serviço {service_id} deletado: {service}")
    return {"msg": "Serviço deletado."}
