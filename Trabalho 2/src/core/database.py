from sqlmodel import SQLModel, create_engine, Session
from src.Models.models import Client

engine = create_engine("sqlite:///src/core/vetclin.db")


def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
