from instanciaLogs import Logs , logging
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from csvFunctions import read_csv,write_csv_cliente,write_csv_animal, write_csv_servico, write_csv_list,xml
from models import Cliente, Animal, Servico
import zipfile as zip


app = FastAPI()
log = Logs() # Instancia o arquivo de logs

CLIENT = 0
ANIMAL = 1
SERVICE = 2


@app.get("/")
def root():
    logging.info("Acesso ao endpoint root.")
    return {'msg':'Hello, World!!'}
    
#-----------------------------------Cliente--------------------------------------    
@app.get("/client")
def clientes():
    logging.info("Endpoint GET Clientes chamado.")
    clients = read_csv(CLIENT,to_json=True) # path_index 0 = clientes
    if not clients:
        logging.info("Lista de clientes está vazia.")
        return {"msg":"Lista vazia."}
    return clients

@app.get("/client/filter/id")
def clientes_filtro_id(id:int):
    logging.info(f"Endpoint GET Clientes filtro de id {id} chamado.")
    clients = read_csv(CLIENT,to_json=True) # path_index 0 = clientes
    if not clients:
        logging.info("Lista de clientes está vazia.")
        return {"msg":"Lista vazia."}
    
    filtered_clients = [c for c in clients if c['id'] ==id]
    if not filtered_clients:
        return {'msg':'Nenhuma pessoa encontrada com esse id'}
    return filtered_clients

@app.get("/client/filter/nome")
def clientes_filtro_nome(nome:str):
    logging.info(f"Endpoint GET Clientes filtro de nome {nome} chamado.")
    clients = read_csv(CLIENT,to_json=True) # path_index 0 = clientes
    if not clients:
        logging.info("Lista de clientes está vazia.")
        return {"msg":"Lista vazia."}
    
    filtered_clients = [c for c in clients if c['nome'].capitalize() ==nome.capitalize()]
    if not filtered_clients:
        return {'msg':'Nenhuma pessoa encontrada com esse nome'}
    return filtered_clients

@app.get("/client/filter/idade")
def clientes_filtro_idade(idade:int):
    logging.info(f"Endpoint GET Clientes filtro de idade {idade} chamado.")
    clients = read_csv(CLIENT,to_json=True) # path_index 0 = clientes
    if not clients:
        logging.info("Lista de clientes está vazia.")
        return {"msg":"Lista vazia."}
    
    filtered_clients = [c for c in clients if int(c['idade'])==idade]
    if not filtered_clients:
        return {'msg':'Nenhuma pessoa encontrada com essa idade'}
    return filtered_clients

@app.get("/client/filter/telefone")
def clientes_filtro_telefone(telefone:str):
    logging.info(f"Endpoint GET Clientes filtro de telefone {telefone} chamado.")
    clients = read_csv(CLIENT,to_json=True) # path_index 0 = clientes
    if not clients:
        logging.info("Lista de clientes está vazia.")
        return {"msg":"Lista vazia."}
    
    logging.debug(telefone == '123')
    
    filtered_clients = [c for c in clients if str(c['telefone']) ==telefone]
    if not filtered_clients:
        return {'msg':'Nenhuma pessoa encontrada com esse telefone'}
    return filtered_clients

@app.get("/client/filter/email")
def clientes_filtro_email(email:str):
    logging.info(f"Endpoint GET Clientes filtro de email {email} chamado.")
    clients = read_csv(CLIENT,to_json=True) # path_index 0 = clientes
    if not clients:
        logging.info("Lista de clientes está vazia.")
        return {"msg":"Lista vazia."}
    
    filtered_clients = [c for c in clients if c['email'].capitalize() ==email.capitalize()]
    if not filtered_clients:
        return {'msg':'Nenhuma pessoa encontrada com esse email'}
    return filtered_clients


@app.get("/client/hash")
def clientes():
    logging.info("Endpoint GET Clientes chamado.")
    clients = read_csv(CLIENT,to_hash=True) # path_index 0 = clientes
    if not clients:
        logging.info("Lista de clientes está vazia.")
        return {"msg":"Lista vazia."}
    return clients

@app.get("/client/qtd")
def clientes():
    logging.info("Endpoint GET Clientes chamado.")
    clients = read_csv(CLIENT,to_json=True) # path_index 0 = clientes
    if not clients:
        logging.info("Lista de clientes está vazia.")
        return {"msg":"Lista vazia."}
    return {"Quantidade":len(clients)}

@app.get("/client/zip")
def clientes():
    logging.info("Endpoint GET ZIP Clientes chamado.")
    clients = read_csv(CLIENT,to_zip=True) # path_index 0 = clientes
    return clients

@app.get("/client/xml")
def cliente_xml():
    logging.info("Endpoint GET XML clientes foi chamado.")
    try:
        return xml(CLIENT)
    except Exception as e:
        logging.warning(f"Erro ao processar o xml de cliente: {e}")
    

@app.post("/clients")
def add_client(client:Cliente):
    logging.info("Endpoint POST clientes chamado.")
    clients = read_csv(CLIENT)

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
    clients = read_csv(CLIENT)
    change = False
    new_list = []
    if len(clients) > 0:
        for c in clients:
            logging.info(f"Checando se cliente de id : {id_client} existe.")
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
    clients = read_csv(CLIENT)

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
    animals = read_csv(ANIMAL,to_json=True) # path_index 1 = animals
    if not animals:
        logging.info("Lista de animais está vazia.")
        return {"msg" : "Lista vazia."}
    return animals


@app.get('/animals/filter/id')
def animals_filter_id(id:int):
    logging.info("Endpoint GET animais filtrados por id chamado")
    animals = read_csv(ANIMAL,to_json=True) # path_index 1 = animals
    if not animals:
        logging.info("Lista de animais está vazia.")
        return {"msg" : "Lista vazia."}
    
    filtered_animals = [a for a in  animals if int(a['id']) == id]

    if not filtered_animals:
        return {'msg': 'Nenhum animal com esse id encontrado'}
    return filtered_animals

@app.get('/animals/filter/client_id')
def animals_filter_client_id(client_id:int):
    logging.info("Endpoint GET animais filtrados por cliente id chamado")
    animals = read_csv(ANIMAL,to_json=True) # path_index 1 = animals
    if not animals:
        logging.info("Lista de animais está vazia.")
        return {"msg" : "Lista vazia."}
    
    filtered_animals = [a for a in  animals if int(a['cliente_id']) == client_id]

    if not filtered_animals:
        return {'msg': 'Nenhum animal com esse id de cliente encontrado'}
    return filtered_animals


@app.get('/animals/filter/nome')
def animals_filter_nome(nome:str):
    logging.info("Endpoint GET animais filtrados por nome chamado")
    animals = read_csv(ANIMAL,to_json=True) # path_index 1 = animals
    if not animals:
        logging.info("Lista de animais está vazia.")
        return {"msg" : "Lista vazia."}
    
    filtered_animals = [a for a in  animals if a['nome'].capitalize()== nome.capitalize()]

    if not filtered_animals:
        return {'msg': 'Nenhum animal com esse nome encontrado'}
    return filtered_animals

@app.get('/animals/filter/especie')
def animals_filter_especie(especie:str):
    logging.info("Endpoint GET animais filtrados por especie chamado")
    animals = read_csv(ANIMAL,to_json=True) # path_index 1 = animals
    if not animals:
        logging.info("Lista de animais está vazia.")
        return {"msg" : "Lista vazia."}
    
    filtered_animals = [a for a in  animals if a['especie'].capitalize()== especie.capitalize()]

    if not filtered_animals:
        return {'msg': 'Nenhum animal dessa especie encontrado'}
    return filtered_animals

@app.get('/animals/filter/raca')
def animals_filter_raca(raca:str):
    logging.info("Endpoint GET animais filtrado por raça chamado")
    animals = read_csv(ANIMAL,to_json=True) # path_index 1 = animals
    if not animals:
        logging.info("Lista de animais está vazia.")
        return {"msg" : "Lista vazia."}
    
    filtered_animals = [a for a in  animals if a['raca'].capitalize()== raca.capitalize()]

    if not filtered_animals:
        return {'msg': 'Nenhum animal dessa raca encontrado'}
    return filtered_animals

@app.get('/animals/hash')
def animals():
    logging.info("Endpoint GET animais Hash chamado")
    animals = read_csv(ANIMAL,to_hash=True) # path_index 1 = animals
    if not animals:
        logging.info("Lista de animais está vazia.")
        return {"msg" : "Lista vazia."}
    return animals

@app.get('/animals/qtd')
def animals():
    logging.info("Endpoint GET animais quantidade chamado")
    animals = read_csv(ANIMAL,to_json=True) # path_index 1 = animals
    if not animals:
        logging.info("Lista de animais está vazia.")
        return {"msg" : "Lista vazia."}
    return {"Quantidade" :len(animals)}

@app.get("/animals/xml")
def animal_xml():
    logging.info("Endpoint GET XML animais foi chamado.")
    try:
        return xml(ANIMAL)
    except Exception as e:
        logging.warning(f"Erro ao processar o xml de animal: {e}")

@app.get('/animals/zip')
def animals():
    logging.info("Endpoint GET ZIP animais chamado")
    animals = read_csv(ANIMAL,to_zip=True) # path_index 1 = animals
    return animals

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
    clients = read_csv(CLIENT)
    animals = read_csv(SERVICE)
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
    animals = read_csv(ANIMAL)
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
    
#------------------------------------Serviços--------------------------------------
@app.get("/service")
def service():
    logging.info("Endpoint GET serviços chamado.")
    services = read_csv(SERVICE, to_json=True)
    if not services:
        logging.info("Lista de serviços está vazia.")
        return {"msg" :"Lista de serviços vazia."}
    #raise HTTPException(status_code=204,detail="Lista de serviços está vazia.")
    logging.info("Lista de serviços será retornada.")
    return {'Serviços':services}

@app.get('/service/filter/id')
def service_filter_id(id:int):
    logging.info("Endpoint GET serviços filtrados por id chamado")
    service = read_csv(SERVICE,to_json=True)
    if not service:
        logging.info("Lista de serviços está vazia.")
        return {"msg" : "Lista vazia."}
    try:
        filtered_service = [a for a in service if int(a['id']) == id]
    except Exception as e:
        logging.warning(e)

    if not filtered_service:
        return {'msg': 'Nenhum serviço para esse id encontrado'}
    return filtered_service

@app.get('/service/filter/nome')
def service_filter_nome(nome:str):
    logging.info("Endpoint GET serviços filtrados por nome chamado")
    service = read_csv(SERVICE,to_json=True) 
    if not service:
        logging.info("Lista de serviços está vazia.")
        return {"msg" : "Lista vazia."}
    
    filtered_service = [a for a in  service if a['nome'].capitalize()== nome.capitalize()]

    if not filtered_service:
        return {'msg': 'Nenhum serviço com esse nome encontrado'}
    return filtered_service

@app.get('/service/filter/client_id')
def service_filter_client_id(client_id:int):
    logging.info("Endpoint GET serviços filtrados por id do cliente chamado")
    service = read_csv(SERVICE,to_json=True)
    if not service:
        logging.info("Lista de serviços está vazia.")
        return {"msg" : "Lista vazia."}
    try:
        filtered_service = [a for a in service if int(a['cliente_id']) == client_id]
    except Exception as e:
        logging.warning(e)

    if not filtered_service:
        return {'msg': 'Nenhum serviço para o id de cliente encontrado'}
    return filtered_service

@app.get('/service/filter/animal_id')
def service_filter_animal_id(animal_id:int):
    logging.info("Endpoint GET serviços filtrados por id  do animal chamado")
    service = read_csv(SERVICE,to_json=True)
    if not service:
        logging.info("Lista de serviços está vazia.")
        return {"msg" : "Lista vazia."}
    try:
        filtered_service = [a for a in service if int(a['animal_id']) == animal_id]
    except Exception as e:
        logging.warning(e)

    if not filtered_service:
        return {'msg': 'Nenhum serviço para o animal desse id  encontrado'}
    return filtered_service

@app.get("/service/filter/price")
def service_filter_price(price:float):
    logging.info("Endpoint GET serviços filtrados por preço chamado.")
    services = read_csv(SERVICE, to_json=True)
    if not services:
        logging.info("Lista de serviços está vazia.")
        return {"msg" :"Lista de serviços vazia."}
    #raise HTTPException(status_code=204,detail="Lista de serviços está vazia.")
    logging.info("Lista de serviços será retornada.")
    filtered_services = [s for s in services if s['preco'] >= price]
    if not filtered_services:
        return {'msg':'Nenhum serviço encontrado'}
    return filtered_services





@app.get("/service/hash")
def service():
    logging.info("Endpoint GET serviços chamado.")
    services = read_csv(SERVICE, to_hash=True)
    if not services:
        logging.info("Lista de serviços está vazia.")
        return {"msg" :"Lista de serviços vazia."}
    #raise HTTPException(status_code=204,detail="Lista de serviços está vazia.")
    logging.info("Lista de serviços será retornada.")
    return services


@app.get("/service/qtd")
def service():
    logging.info("Endpoint GET serviços chamado.")
    services = read_csv(SERVICE, to_json=True)
    if not services:
        logging.info("Lista de serviços está vazia.")
        return {"msg" :"Lista de serviços vazia."}
    #raise HTTPException(status_code=204,detail="Lista de serviços está vazia.")
    logging.info("Lista de serviços será retornada.")
    return {'Quantidade':len(services)}

@app.get("/service/zip")
def service():
    logging.info("Endpoint GET serviços chamado.")
    services = read_csv(SERVICE, to_zip=True)
    return services

@app.get("/service/xml")
def servico_xml():
    logging.info("Endpoint GET XML animais foi chamado.")
    try:
        return xml(SERVICE)
    except Exception as e:
        logging.warning(f"Erro ao processar o xml de servico: {e}")

@app.post("/service")
def add_service(service:Servico):
    logging.info("Endpoint POST de serviço chamado.")
    
    clients = read_csv(CLIENT)
    animals = read_csv(ANIMAL)
    services = read_csv(SERVICE)
    
    service_exist = False
    animal_exist = False
    client_exist = False
      
    #Checar se id do serviço ja existe
    for s in services:
        id_service,_,_,_,_ = s.split(",")
        if int(id_service) == service.id:
            logging.info(f"Serviço de id {id_service} já existe.")
            service_exist = True
    
    if service_exist:
        raise HTTPException(status_code=409,detail=f"Serviço de ID:{service.id} já existe.")

    logging.info(f"Checando se cliente de id {service.cliente_id} existe.")
    for c in clients:
        id_client,_,_,_,_ = c.split(",")
        if int(id_client) == service.cliente_id:
            client_exist = True
            logging.info(f"Cliente encontrado.")
            
    if client_exist == False:
        raise HTTPException(status_code=404,detail=f"Cliente de id {service.cliente_id} não foi encontrado.")
    
    logging.info(f"Checando se animal de id {service.animal_id} existe.")
    for a in animals:
        id_animal,_,_,_,_ = a.split(",")
        if int(id_animal) == service.animal_id:
            logging.info("Animal encontrado.")
            animal_exist = True
    
    if animal_exist == False:
        raise HTTPException(status_code=404,detail=f"Animal de id {service.animal_id} não foi encontrado.")
    
    
    try:
        logging.info("Salvando seriço no csv.")
        write_csv_servico(service)
        logging.info("Serviço salvo.")
        return {"Serviço cadastrado com sucesso":service}
    except Exception as e:
        logging.warning(f"Erro ao salvar no csv : {e}")
        

@app.put("/service/{id}")
def update_service_by_id(id_service:int,service:Servico):
    logging.info("Endpoint put de serviço chamado.")
    clients = read_csv(CLIENT)
    animals = read_csv(ANIMAL)
    services = read_csv(SERVICE)
    
    change = False
    service_exist = False
    client_exist = False
        
    new_list = []
    
    logging.info(f"Checando se serviço de id:{id_service} existe.")
    for s in services:
        id,_,_,_,_ = s.split(",")
        if int(id) == id_service:
            logging.info("Serviço encontrado.")
            service_exist = True
            if id_service != service.id:
                service.id = id_service
                logging.info("ID passado como parametro tem número diferente de id do objeto. Valor do objeto alterado.")
            logging.info(f"Checando se cliente de id {service.cliente_id} existe.")
            for c in clients:
                id_client,_,_,_,_ = c.split(",")
                if int(id_client) == service.cliente_id:
                    logging.info("Cliente encontrado.")
                    client_exist = True
                    logging.info(f"Checando se animal de id {service.animal_id} existe.")
                    for a in animals:
                        id_animal,_,_,_,_ = a.split(",")
                        if int(id_animal) == service.animal_id:
                            logging.info("Animal encontrado.")
                            new_list.append(f"{service.id},{service.nome},{service.cliente_id},{service.animal_id},{service.preco}")
                            change = True
        else:
            new_list.append(s)
                
    if service_exist == False:
        raise HTTPException(status_code = 404, detail = f"Serviço de id: {id_service} não encontrado.")
    
    if client_exist == False:
        raise HTTPException(status_code = 404, detail=f"Serviço de id {id_service} encontrado. Cliente de id {service.cliente_id} não encontrado.")
    
    if change:
        try:
            logging.info("Lista de serviços será alterada.")
            write_csv_list(SERVICE,new_list)
            logging.info("Lista de serviço alterada.")
            return {"Lista atualizada":new_list}
        except Exception as e:
            pass
    else:
        raise HTTPException(status_code = 404, detail=f"Serviço de id {id_service} encontrado. Cliente de id {service.cliente_id} encontrado. Animal de id {service.animal_id} não encontrado.")
        
       
@app.delete("/service/{id}")
def delete_service_by_id(id_service:int):
    logging.info("Endpoint delete de serviço chamado.")
    
    services = read_csv(SERVICE)
    new_list = []
    change = False
    
    for s in services:
        id,_,_,_,_ = s.split(",")
        if int(id) != id_service:
            new_list.append(s)
        else:
            logging.info(f"Serviço de id {id_service} achado.")
            change = True
    if change:
        try:
            logging.info("Salvando nova lista de serviços.")    
            write_csv_list(SERVICE,new_list)
            return {"Nova lista" : new_list}
        except Exception as e:
            raise HTTPException(status_code=500,detail=f"Erro ao salvar no csv: {e}")
    logging.info(f"Lista de serviços não foi alterada. Serviço de id: {id_service} não foi encontrado.")
    return {"msg": f"Lista de serviços não foi alterada. Serviço de id: {id_service} não foi encontrado."}