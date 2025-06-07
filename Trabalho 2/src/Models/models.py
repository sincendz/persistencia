from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import date
from enum import Enum
from __future__ import annotations

# from pydantic import EmailStr -> Caso a gente queira validar email

# CLIENTE 1 - N ANIMAL -> OK
# ANIMAL 1 - N ATENDIMENTO ok
# VETERINARIO 1 - N ATENDIMENTO OK
# VETERINARIO 1 - 1 CRMV OK
# ATENDIMENTO N - M SERVICOS OK


class StatusEnum(Enum):
    ATIVO = "ativo"
    INATIVO = "inativo"
    SUSPENSO = "suspenso"


# Classe Default para cliente e veterinário
class Person(SQLModel):
    name: str
    age: int
    phone_number: str
    email: str


class Client(Person, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Relacionamento Cliente 1-N Animal -> Um cliente pode ter vários animais
    # um animal pertence a apenas um cliente
    animals: List["Animal"] = Relationship(back_populates="client")


class Animal(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    client_id: int = Field(foreign_key="client.id")
    name: str
    age: str
    species: str
    breed: str

    client: Optional["Client"] = Relationship(back_populates="animals")
    consultations: List["Consultation"] = Relationship(back_populates="animal")


class ConsultationServiceLink(SQLModel, table=True):
    consultation_id: Optional[int] = Field(default=None, foreign_key="consultation.id", primary_key=True)
    service_id: Optional[int] = Field(default=None, foreign_key="service.id", primary_key=True)


class Service(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    service_name: str
    type_service: str
    price: float
    description: str
    
    consultations = List["Consultation"] = Relationship(back_populates="services", link_model=ConsultationServiceLink)


class Consultation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    animal_id: int = Field(foreign_key="animal.id")
    vet_id: int = Field(foreign_key="veterinary.id")
    notes: str
    # Quem sabe um data-in e data-out

    animal = Optional["Animal"] = Relationship(back_populates="consultations")
    vet = Optional["Veterinary"] = Relationship(back_populates="consultations")
    services = List["Service"] = Relationship(back_populates="consultations", link_model= ConsultationServiceLink)


class Veterinary(Person, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    crmv_id: int = Field(foreign_key="crmv.id")
    specialization: Optional[str] = None

    crmv: Optional["Crmv"] = Relationship(back_populates="veterinary")
    consultations: List["Consultation"] = Relationship(back_populates="veterinary")


class Crmv(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cpf: str
    graduation_institution: str
    year_of_graduation: str
    status: StatusEnum

    veterinary: Optional["Veterinary"] = Relationship(back_populates="crmv")
