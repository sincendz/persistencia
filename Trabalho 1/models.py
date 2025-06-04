from pydantic import BaseModel

class Cliente(BaseModel):
    id:int
    nome:str
    idade:int
    telefone:str
    email:str

class Animal(BaseModel):
    id:int
    nome:str
    cliente_id:int
    especie:str
    raca:str

class Servico(BaseModel):
    id:int
    nome:str
    cliente_id:int
    animal_id:int
    preco:float


