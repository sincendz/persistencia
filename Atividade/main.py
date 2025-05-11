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
@app.get("/client")
def clientes():
    logging.info("Endpoint GET Clientes chamado.")
    clients = read_csv(0) # path_index 0 = clientes
    if len(clients) > 0:
        return clients
    logging.info("Lista de clientes está vazia.")
    return {"msg":"Lista vazia."}

@app.post("/clients")
def add_client(client:Cliente):
    logging.info("Endpoint POST clientes chamado.")
    clients = read_csv(0)

    logging.info(f"Checando se cliente de id: {client.id} já existe no sistema. ")
    for p in clients:
        id_csv , _ , _ , _ , _ = p.split(",")
        logging.debug((int(id_csv),client.id))
        if int(id_csv) == client.id:
            logging.info(f"ID {client.id} já existe no sistema. Não é possível cadastrar.")
            raise HTTPException(status_code=409, detail="ID já existe no sistema")
    
    try:
        write_csv_cliente(client)
        logging.info("Novo cliente cadastrado.")
    except Exception as e:
        logging.warning(f"Erro ao salvar no csv: {e} ")
        raise HTTPException(status_code=404, detail="Erro ao salvar no csv")
    
    return {"msg": "cliente cadastrado com sucesso!", "cliente": client}


@app.put("/clients/{id}")
def update_client_by_id(id_client:int, client:Cliente):
    logging.info("Endpoint PUT chamado para clientes.")
    logging.info(f"Função de atulizar cliente foi chamada para: {client}")
    clients = read_csv(0)
    change = False
    new_list = []
    if len(clients) > 0:
        for c in clients:
            logging.info(f"Checando se cliente de id : {client.id} existe.")
            id_csv,_,_,_,_ = c.split(",")
            if(int(id_csv) == id_client):
                logging.info("Cliente encontrado.")
                change = True
                if id_client != int(client.id):
                    client.id = id_client
                    logging.info(f"ID passado para atualizar {id_client} foi diferente de id :{client.id} passado na requisição.")
                client_atualizado = f'{client.id},{client.nome},{client.idade},{client.telefone},{client.email}'
                new_list.append(client_atualizado)
            else:
                new_list.append(c)
        if change:
            logging.info("Cliente encontado, chamando a função para alterar csv.")
            write_csv_list(0,new_list)
            return {"Lista de clientes atualizada" : new_list}
        else:
            logging.info(f"Cliente de id: {id_client} não foi encontrado.")
            raise HTTPException(status_code=404,detail=f"Cliente de id: {id_client} não foi encontrado.")
    raise HTTPException(status_code=404,detail="Lista vazia, impossivel atualizar.")   
            
@app.delete("/clients/{id}")
def delete_by_id(id:int):
    logging.info("Endpoint delete chamado para cliente.")
    logging.info(f"Função de chamar chamada para id : {id}")
    clients = read_csv(0)

    change = False
    new_list = []
    logging.debug(f"Tamanho clients: {len(clients)}")
    if len(clients) > 0:
        for c in clients:
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
    return {"Nova lista apos delete: " : new_list}

#-----------------------------------Animal--------------------------------------    
@app.get('/animals/')
def animals():
    logging.info("Endpoint GET animais chamado")
    animals = read_csv(1) # path_index 1 = animals
    if len(animals) > 0:
        return animals
    logging.info("Lista de animais está vazia.")
    return {"msg" : "Lista vazia."}

@app.post('/animais/')
def add_animal(animal:Animal):
    animais = read_csv(1)
    clients = read_csv(0)
    client_exist = False
    
    logging.info(f"Checando se {animal.id} já existe no sistema. ")
    for p in animais:
        id_csv , _ , _ , _ , _ = p.split(",")
        logging.debug((int(id_csv),animal.id))
        if int(id_csv) == animal.id:
            logging.info(f"ID {animal.id} já existe no sistema. Não é possível cadastrar.")
            raise HTTPException(status_code=409, detail="ID já existe no sistema")
    
    #Checar se o id do cliente existe no sistema
    logging.info(f"Checando se o cliente de ID: {animal.cliente_id} existe no sistema. ")
    for p in clients:
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

@app.put("/animais/{id}")
def update_animal_by_id(id_animal:int, animal:Animal):
    logging.info(f"Função para alterar animal de id {id_animal} chamada com {animal}")
    clients = read_csv(0)
    animals = read_csv(1)
    new_list = []
    animal_exist = False
    client_exist = False
    
    #Checar se id existe na lista de animais
    logging.info(f"Checando se {id_animal} existe em {animals}")
    for a in animals:
        id_csv,_,_,_,_ = a.split(',')
        if int(id_csv) == id_animal:
            logging.info("Animal encontrado!")
            animal_exist = True
            if id_animal != animal.id:
                animal.id = id_animal
                logging.info(f"ID passado como paramentro {id_animal} é diferente do id do objeto animal. Alteração feita.")
            #Checar se o ID do Cliente existe
            for cliente in clients:
                logging.info(f"Checando se cliente de id {animal.cliente_id} existe.")
                id_client,_,_,_,_ = cliente.split(",")
                if(int(id_client) == animal.cliente_id):
                    logging.info(f"Cliente de id {animal.cliente_id} encontrado.")
                    client_exist = True
                    new_animal = f'{animal.id},{animal.nome},{animal.cliente_id},{animal.especie},{animal.raca}'
                    new_list.append(new_animal)     
        else:
            new_list.append(a)
    if client_exist:
        logging.info("Alterações no CSV animais.")
        write_csv_list(1,new_list)
        return new_list
    if animal_exist:
        logging.info(f"ID do animal existe mas cliente de id {animal.cliente_id} não foi encontrado")
        raise HTTPException(status_code=404,detail=f"ID do animal existe mas cliente de id {animal.cliente_id} não foi encontrado")
    logging.info(f"Animal de id {id_animal} não foi encontrado.")
    raise HTTPException(status_code=404,detail=f"Animal de id {id_animal} não foi encontrado.")  

@app.delete("/animals/{id}")
def delete_animal_by_id(id_animal:int):
    logging.info("Endpoint delete chamado para animais.")
    logging.info(f"Função de deletar animal chamada para id: {id_animal}")
    animals = read_csv(1)
    new_list = []
    change = False
    
    for animal in animals:
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
    