from fastapi import APIRouter , HTTPException , Depends
from sqlmodel import Session , select
from src.Models.models import Service, ServiceBase
from src.core.database import get_session

router = APIRouter(prefix="/services", tags=["services"])

@router.get("/", response_model=list[Service])
def read_services(session : Session = Depends(get_session)):
    return session.exec(select(Service)).all()

@router.get("/seatch/{service_id}", response_model=Service)
def search_service(service_id : int, session: Session = Depends(get_session)):
    service = session.get(Service,service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Serviço não encontrado.")
    return service

@router.get("/services_length")
def length_service(session: Session = Depends(get_session)):
    return {"Quantidade " : len(session.exec(select(Service)).all())}

@router.post("/", response_model=Service)
def create_service(service:ServiceBase, session: Session = Depends(get_session)):
    db_service = Service.from_orm(service)
    session.add(db_service)
    session.commit()
    session.refresh(db_service)
    return db_service

@router.put("/{service_id}", response_model=Service)
def update_service(service_id:int, service:ServiceBase, session:Session = Depends(get_session)):
    db_service = session.get(Service,service_id)
    if not db_service:
        raise HTTPException(status_code=404, detail="Serviço não encontrado.")
    for key , value in service.dict().items():
        setattr(db_service,key,value)
    session.add(db_service)
    session.commit()
    session.refresh(db_service)
    return db_service
        

@router.delete("/{service_id}")
def delete_service(service_id:int,session:Session = Depends(get_session)):
    service = session.get(Service,service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Serviço não encontrado.")
    session.delete(service)
    session.commit()
    return {"msg" : "Serviço deletado."}