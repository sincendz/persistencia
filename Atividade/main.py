from instanciaLogs import Logs , logging
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from csvFunctions import read_csv,write_csv_cliente,write_csv_animal, write_csv_servico, write_csv_list
from models import Cliente, Animal, Servico


app = FastAPI()
log = Logs() # Instancia o arquivo de logs


@app.get("/")
def root():
    logging.info("Acesso ao endpoint root.")
    return {'msg':'Hello, World!!'}
    
#-----------------------------------Cliente--------------------------------------    
@app.get("/clientes")
def clientes():
    logging.info("Endpoint GET Clientes chamado")
    clientes = read_csv(0) # path_index 0 = clientes
    if len(clientes) > 0:
        return clientes
    logging.info("Lista de clientes está vazia.")
    return "Lista vazia."

@app.post("/clientes")
def add_cliente(cliente:Cliente):
    
    clientes = read_csv(0)

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


@app.put("/clientes/id")
def update_client_by_id(id_cliente:int, cliente:Cliente):
    logging.info(f"Função de atulizar cliente foi chamada para: {cliente}")
    clientes = read_csv(0)
    change = False
    new_list = []
    if len(clientes) > 0:
        for c in clientes:
            logging.info(f"Checando se cliente de id : {cliente.id} existe.")
            id_csv,_,_,_,_ = c.split(",")
            if(int(id_csv) == id_cliente):
                logging.info("Cliente encontrado.")
                change = True
                if id_cliente != int(cliente.id):
                    cliente.id = id_cliente
                    logging.info(f"ID passado para atualizar {id_cliente} foi diferente de id :{cliente.id} passado na requisição.")
                cliente_atualizado = f'{cliente.id},{cliente.nome},{cliente.idade},{cliente.telefone}, {cliente.email}'
                new_list.append(cliente_atualizado)
            else:
                new_list.append(c)
        if change:
            logging.info("Cliente encontado, chamando a função para alterar csv.")
            write_csv_list(0,new_list)
            return new_list
        else:
            logging.info(f"Cliente de id: {id_cliente} não foi encontrado.")
            raise HTTPException(status_code=404,detail=f"Cliente de id: {id_cliente} não foi encontrado.")
    raise HTTPException(status_code=404,detail="Lista vazia, impossivel atualizar.")   
            
@app.delete("/clientes/id")
def delete_by_id(id:int):
    logging.info(f"Função de chamar chamada para id : {id}")
    clientes = read_csv(0)

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
            write_csv_list(0,new_list)
        else:
            logging.info(f"Delete nao mudou a lista, id {id} não encontrado.")  
            raise HTTPException(status_code=404, detail=f"ID {id}, não foi encontrado.")    
    return new_list

#-----------------------------------Animal--------------------------------------    
@app.get('/animais/')
def animais():
    logging.info("Endpoint GET Animais chamado")
    animais = read_csv(1) # path_index 1 = animais
    if len(animais) > 0:
        return animais
    logging.info("Lista de animais está vazia.")
    return "Lista vazia."

@app.post('/animais/')
def add_animal(animal:Animal):
    animais = read_csv(1)
    clientes = read_csv(0)
    client_exist = False
    
    logging.info(f"Checando se {animal.id} já existe no sistema. ")
    for p in animais:
        id_csv , _ , _ , _ , _ = p.split(",")
        logging.debug((int(id_csv),animal.id))
        if int(id_csv) == animal.id:
            logging.info(f"ID {animal.id} já existe no sistema. Não é possível cadastrar.")
            raise HTTPException(status_code=404, detail="ID já existe no sistema")
    
    #Checar se o id do cliente existe no sistema
    logging.info(f"Checando se o cliente de ID: {animal.cliente_id} existe no sistema. ")
    for p in clientes:
        id_csv , _ , _ , _ , _ = p.split(",")
        if int(id_csv) == animal.cliente_id:
            client_exist = True
            logging.info(f"Cliente de ID: {animal.cliente_id} existe no sistema.")
    
    if client_exist:
        try:
            write_csv_animal(animal)
            logging.info("Novo animal cadastrado")
        except Exception as e:
            logging.warning(f"Erro ao salvar no csv: {e} ")
            raise HTTPException(status_code=404, detail="Erro ao salvar no csv")
        return {"msg": "Animal cadastrado com sucesso!", "animal": animal}
    else:
        logging.info(f"Cliente não existe no sistema, não foi possivel cadastrar animal.")
        raise HTTPException(status_code=404,detail=f"Cliente de id: {animal.cliente_id} não existe no sistema, não foi possivel cadastrar animal de id: {animal.id}")

@app.put("/animais/id")
def update_animal_by_id(id_animal:int, animal:Animal):
    pass

@app.delete("/animais/id")
def delete_animal_by_id(id_animal:int):
    logging.info(f"Função de deletar animal chamada para id: {id_animal}")
    animais = read_csv(1)
    new_list = []
    change = False
    
    for animal in animais:
        id_csv,_,_,_,_ = animal.split(",")
        if(int(id_csv) != id_animal ):
            new_list.append(animal)
        else:
            logging.debug(f"Animal de {id_animal} encontrado.")
            change = True
    if change:
        try:
            logging.info("Delete animais alterou a lista.")
            write_csv_list(1,new_list)
            return new_list
        except Exception as e:
            logging.warning(f"Problema ao salvar lista de animais : {e}")
            raise HTTPException(status_code=404,detail=f'Não foi possivel deletar o animal de id {id_animal}, erro {e}')
    logging.info(f"Animal de id {id_animal} não foi encontrado.")
    raise HTTPException(status_code=404,detail=f"Animal de id {id_animal} não foi encontrado.")
    