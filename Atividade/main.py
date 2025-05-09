from instanciaLogs import Logs , logging
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from csvFunctions import read_csv,write_csv_cliente,write_csv_animal, write_csv_servico, write_csv_list_cliente
from models import Cliente, Animal, Servico


app = FastAPI()
log = Logs() # Instancia o arquivo de logs

class Pessoa(BaseModel):
    id: int
    name : str
    age : int
    
@app.get("/")
def root():
    logging.info("Acesso ao endpoint root.")
    return {'msg':'Hello, World!!'}
    
    
@app.get("/clientes")
def pessoas():
    logging.info("Endpoint GET Clientes chamado")
    clientes = read_csv(0) # path_index 0 = clientes
    if len(clientes) > 0:
        clientes.pop(0)
        return clientes
    logging.info("Lista de clientes está vazia.")
    return "Lista vazia."

@app.post("/clientes")
def add_pessoa(cliente:Cliente):
    
    clientes = read_csv(0)
    clientes.pop(0)
    
    logging.info(f"Checando se {cliente.id} já existe no sistema. ")
    for p in clientes:
        id_csv , _ , _ , _ , _ = p.split(",")
        logging.debug((int(id_csv),cliente.id))
        if int(id_csv) == cliente.id:
            logging.info(f"ID {cliente.id} já existe no sistema. Não é possível cadastrar.")
            raise HTTPException(status_code=404, detail="ID já existe no sistema")
    
    try:
        write_csv_cliente(cliente)
        logging.info("Novo cliente cadastrado")
    except Exception as e:
        logging.warning(f"Erro ao salvar no csv: {e} ")
        raise HTTPException(status_code=404, detail="Erro ao salvar no csv")
    
    return {"msg": "cliente cadastrado com sucesso!", "cliente": cliente}

@app.delete("/clientes/id")
def delete_by_id(id:int):
    logging.info(f"Função de chamar chamada para id : {id}")
    clientes = read_csv(0)
    clientes.pop(0)
    change = False
    new_list = []
    logging.debug(f"Tamanho clientes: {len(clientes)}")
    if len(clientes) > 0:
        for c in clientes:
            id_csv , _ , _ , _ , _ = c.split(',')
            if int(id_csv) == id:
                change = True
            else:
                new_list.append(c)
        if change:
            write_csv_list_cliente(new_list)
        else:
            logging.info(f"Delete nao mudou a lista, id {id} não encontrado.")      
    return new_list

@app.get('/animais/')
def animais():
    logging.info("Endpoint GET Animais chamado")
    animais = read_csv(1) # path_index 1 = animais
    if len(animais) > 0:
        animais.pop(0)
        return animais
    logging.info("Lista de animais está vazia.")
    return "Lista vazia."

@app.post('/animais/')
def add_animal(animal:Animal):
    animais = read_csv(1)
    animais.pop(0)
    
    logging.info(f"Checando se {animal.id} já existe no sistema. ")
    for p in animais:
        id_csv , _ , _ , _ , _ = p.split(",")
        logging.debug((int(id_csv),animal.id))
        if int(id_csv) == animal.id:
            logging.info(f"ID {animal.id} já existe no sistema. Não é possível cadastrar.")
            raise HTTPException(status_code=404, detail="ID já existe no sistema")
    
    try:
        write_csv_animal(animal)
        logging.info("Novo animal cadastrado")
    except Exception as e:
        logging.warning(f"Erro ao salvar no csv: {e} ")
        raise HTTPException(status_code=404, detail="Erro ao salvar no csv")
    
    return {"msg": "animal cadastrado com sucesso!", "animal": animal}






