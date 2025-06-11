from fastapi import FastAPI, Depends
from sqlmodel import Session
from src.routers.client import router as client_router
from src.routers.animal import router as animal_router
from src.routers.service import router as service_router
from src.routers.veterinary import router as veterinary_router
from src.routers.crmv import router as crmv_router
from src.routers.consultation import router as consultation_router
from src.core.database import create_db_and_tables
from src.core.loggingInit import Logs, logging
from src.core.database import get_session
from src.Models.models import *

routs = [
    client_router,
    animal_router,
    service_router,
    veterinary_router,
    crmv_router,
    consultation_router,
]

app = FastAPI()
log = Logs()


@app.get("/root")
def populate_db(session: Session = Depends(get_session)):
    # CRMV
    crmv1 = Crmv(
        cpf="12345678900",
        graduation_institution="UFC",
        year_of_graduation="2015",
        status="ATIVO",
    )
    session.add(crmv1)
    session.commit()
    session.refresh(crmv1)

    # Clientes
    client1 = Client(
        name="João Silva", age=35, phone_number="11999999999", email="joao@email.com"
    )
    client2 = Client(
        name="Maria Souza", age=28, phone_number="11888888888", email="maria@email.com"
    )
    session.add_all([client1, client2])
    session.commit()
    session.refresh(client1)
    session.refresh(client2)

    # Animais
    animal1 = Animal(
        client_id=client1.id, name="Rex", age="5", species="Cachorro", breed="Vira-lata"
    )
    animal2 = Animal(
        client_id=client2.id, name="Mimi", age="3", species="Gato", breed="Siamês"
    )
    animal3 = Animal(
        client_id=client1.id, name="Thor", age="2", species="Cachorro", breed="Poodle"
    )
    session.add_all([animal1, animal2, animal3])
    session.commit()
    session.refresh(animal1)
    session.refresh(animal2)
    session.refresh(animal3)

    # Veterinário
    vet1 = Veterinary(
        name="Dr. Pedro",
        age=40,
        phone_number="11777777777",
        email="pedro@vet.com",
        crmv_id=crmv1.id,
        specialization="Clínica Geral",
    )
    session.add(vet1)
    session.commit()
    session.refresh(vet1)

    # Serviços
    service1 = Service(
        service_name="Vacinação",
        type_service="PREVENCAO",
        price=100.0,
        description="Vacina V8",
    )
    service2 = Service(
        service_name="Consulta",
        type_service="CONSULTA",
        price=80.0,
        description="Consulta geral",
    )
    service3 = Service(
        service_name="Cirurgia",
        type_service="CIRURGIA",
        price=500.0,
        description="Cirurgia de castração",
    )
    session.add_all([service1, service2, service3])
    session.commit()
    session.refresh(service1)
    session.refresh(service2)
    session.refresh(service3)

    return {
        "msg": "Banco populado com sucesso!",
        "crmvs": [crmv1],
        "clients": [client1, client2],
        "animals": [animal1, animal2, animal3],
        "veterinaries": [vet1],
        "services": [service1, service2, service3],
    }


@app.get("/create_db")
def create_db():
    try:
        create_db_and_tables()
        return {"msg": "Banco de dado e tabelas criadas"}
    except Exception as e:
        return {"Erro": str(e)}


for rout in routs:
    app.include_router(rout)
