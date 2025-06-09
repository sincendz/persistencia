from fastapi import APIRouter , Depends , HTTPException
from sqlmodel import Session, select
from src.Models.models import Crmv, CrmvBase
from src.core.database import get_session
import math
import logging

router = APIRouter(prefix="/crmvs", tags=["crmvs"])

@router.get("/", response_model=list[Crmv])
def read_crmvs(session : Session = Depends(get_session)):
    logging.info('Endpoint GET chamado para CRMVs')
    return session.exec(select(Crmv)).all()

@router.get("/search/{crmv_id}", response_model=Crmv)
def search_crmvs(crmv_id, session : Session = Depends(get_session)):
    crmv = session.get(Crmv, crmv_id)
    if not crmv:
        logging.error('CRMV não encontrado.')
        raise HTTPException(status_code=404, detail="CRMV não existe!")
    logging.info(f'CRMV retornado {crmv}')
    return crmv

@router.get("/crmvs_length")
def length_crmvs(session : Session = Depends(get_session)):
    logging.info('Quantidade de CRMVs chamado')
    return {"Quantidade " : len(session.exec(select(Crmv)).all())}

@router.get("/page")
def crmvs_page(page:int = 1, page_size:int = 10, session : Session = Depends(get_session)):
    total_crmvs = len(session.exec(select(Crmv)).all())
    total_pages = math.ceil(total_crmvs/page_size)
    offset = (page - 1) * page_size
    data = session.exec(
        select(Crmv).offset(offset).limit(page_size)
    ).all()
    logging.info('GET CRMVs com paginação chamado')
    return {
        "data" : data,
        "total_records" : total_crmvs,
        "total_pages" : total_pages,
        "current_page": page
    }

@router.post("/", response_model=Crmv)
def create_crmv(crmv:CrmvBase, session : Session = Depends(get_session)):
    db_crmv = Crmv.from_orm(crmv)
    session.add(db_crmv)
    session.commit()
    session.refresh(db_crmv)
    logging.info(f'CRMV criado {db_crmv}')
    return db_crmv

@router.put("/{crmv_id}", response_model=Crmv)
def update_crmv(crmv_id:int, crmv: CrmvBase,  session : Session = Depends(get_session)):
    db_crmv = session.get(Crmv,crmv_id)
    if not db_crmv:
        logging.error('CRMV não encontrado')
        raise HTTPException(status_code=404,detail="CRMV não existe.")
    for key , value in crmv.dict().items():
        setattr(db_crmv, key, value)
    session.add(db_crmv)
    session.commit()
    session.refresh(db_crmv)
    logging.info(f'CRMV {crmv_id} atualizado: {db_crmv}')
    return db_crmv

@router.delete("/{crmv_id}")
def delete_crmv(crmv_id : int, session : Session = Depends(get_session)):
    crmv = session.get(Crmv, crmv_id)
    if not crmv:
        logging.error('CRMV não encontrado')
        raise HTTPException(status_code=404, detail="CRMV com esse id não existe.")
    session.delete(crmv)
    session.commit()
    logging.info(f'CRMV {crmv_id} deletado: {crmv}')
    return {"msg" : "CRMV deletado com sucesso!"}
    
