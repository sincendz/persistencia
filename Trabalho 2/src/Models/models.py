from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import date
from enum import Enum


class StatusEnum(Enum):
    ATIVO = "ativo"
    INATIVO = "inativo"
    SUSPENSO = "suspenso"


# Classe base para cliente e veterinário
class Person(SQLModel):
    name: str
    age: int
    phone_number: str
    email: str


class Client(Person, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    animals: List["Animal"] = Relationship(back_populates="client")


class ClientBase(Person):
    pass


class AnimalBase(SQLModel):
    client_id: int = Field(foreign_key="client.id")
    name: str
    age: str
    species: str
    breed: str


class Animal(AnimalBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    client: Optional[Client] = Relationship(back_populates="animals")

    consultations: List["Consultation"] = Relationship(
        back_populates="animal"
    )



class ConsultationServiceLink(SQLModel, table=True):
    consultation_id: Optional[int] = Field(
        default=None, foreign_key="consultation.id", primary_key=True
    )
    service_id: Optional[int] = Field(
        default=None, foreign_key="service.id", primary_key=True
    )


class ServiceBase(SQLModel):
    service_name: str
    type_service: str
    price: float
    description: str

class Service(ServiceBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    consultations: List["Consultation"] = Relationship(
        back_populates="services", link_model=ConsultationServiceLink
    )


class ConsultationBase(SQLModel):
    animal_id: int = Field(foreign_key="animal.id")
    vet_id: int = Field(foreign_key="veterinary.id")
    notes: str

class Consultation(ConsultationBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    data_in: date = Field(default_factory=date.today)
    updated_at : date = Field(default_factory=date.today)
    data_out : Optional[date] = Field(default=None)
    animal: Optional["Animal"] = Relationship(back_populates="consultations")
    veterinary: Optional["Veterinary"] = Relationship(back_populates="consultations")
    services: List["Service"] = Relationship(
        back_populates="consultations", link_model=ConsultationServiceLink
    )

class VeterinaryBase(Person):
    crmv_id: int = Field(foreign_key="crmv.id")
    specialization: Optional[str] = None

class Veterinary(VeterinaryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    crmv: Optional["Crmv"] = Relationship(back_populates="veterinary")
    consultations: List["Consultation"] = Relationship(
        back_populates="veterinary"
    )

class CrmvBase(SQLModel):
    cpf: str
    graduation_institution: str
    year_of_graduation: str
    status: StatusEnum

class Crmv(CrmvBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    veterinary: Optional["Veterinary"] = Relationship(back_populates="crmv")
