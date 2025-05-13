from instanciaLogs import Logs , logging
from pathlib import Path
from pydantic import BaseModel
from models import *
import pandas as pd
import zipfile
from fastapi.responses import FileResponse
from hashlib import sha256
import xml.etree.ElementTree as ET

log = Logs()

# Checa se a pasta db existe, se não existir ela é criada
PATH = Path('db')
PATH.mkdir(exist_ok=True)

# Caminho até o csv
CLIENTES = PATH / 'clientes.csv'
ANIMAIS = PATH / 'animais.csv'
SERVICOS = PATH / 'servicos.csv'

CLIENTESZIP = PATH / 'clientes.zip'
ANIMAISZIP = PATH / 'animais.zip'
SERVICOSZIP = PATH / 'servicos.zip'

paths = [CLIENTES,ANIMAIS,SERVICOS]
zippaths = [CLIENTESZIP,ANIMAISZIP,SERVICOSZIP]


# Checa se o csv existe. Se não, cria com cabeçalho
for p in paths:
    if not p.exists():
        logging.warning(f"{p} não existia. Criando arquivo com cabeçalho.")
        with open(p, 'w') as f:
            if(p == CLIENTES):
                f.write("id,nome,idade,telefone,email\n")
            if(p == ANIMAIS):
                f.write("id,nome,cliente_id,especie,raca\n")
            if(p == SERVICOS):
                f.write("id,nome,cliente_id,animal_id,preco\n")
# 0-> Clientes
# 1-> Animais
# 2 -> Servicos
def read_csv(path_index:int, to_json = False, to_zip = False, to_hash=False):
    path = paths[path_index]
    zippath = zippaths[path_index]
    filenames = ['clientes','animais','servicos']
    data = []
    if to_hash:
        with open(path,'r') as file:
            return sha256(file.read().encode()).hexdigest()
    elif to_zip:
        with zipfile.ZipFile(zippath,'w',zipfile.ZIP_DEFLATED) as file:
            file.write(path)
        return FileResponse(path=zippath,filename=filenames[path_index]+'.zip', media_type = 'application/zip')
    elif to_json:
        df = pd.read_csv(path)
        return df.to_dict(orient='records')
    else:
        with open(path, 'r') as file:
            logging.info("Leitura do csv.")
            lines = file.readlines()
            for line in lines:
                data.append(line.strip())
        data.pop(0) # Remove o cabeçalho 
        return data

def write_csv_cliente(cliente:Cliente):
    logging.info(f"Dado que chegou para ser salvo no CSV: {cliente}")
    with open(CLIENTES, 'a') as file:
        file.write(f"{cliente.id},{cliente.nome},{cliente.idade},{cliente.telefone},{cliente.email}\n")
        logging.info("Arquivo CSV modificado.")

def write_csv_animal(animal:Animal):
    logging.info(f"Dado que chegou para ser salvo no CSV: {animal}")
    with open(ANIMAIS, 'a') as file:
        file.write(f"{animal.id},{animal.nome},{animal.cliente_id},{animal.especie},{animal.raca}\n")
        logging.info("Arquivo CSV modificado.")

def write_csv_servico(servico:Servico):
    logging.info(f"Dado que chegou para ser salvo no CSV: {servico}")
    with open(SERVICOS, 'a') as file:
        file.write(f"{servico.id},{servico.nome},{servico.cliente_id},{servico.animal_id},{servico.preco}\n")
        logging.info("Arquivo CSV modificado.")


def write_csv_list(path_index:int,new_list):
    logging.info(f"Write csv chamado com index = {path_index} e list = {new_list}")
    if path_index == 0:
        logging.info("CSV CLIENTES")
        try:
            with open(CLIENTES, 'w') as file:
                file.write('id,nome,idade,telefone,email\n')  # adicionei \n
                for cliente in new_list:
                    id,nome,idade,telefone,email = cliente.split(",")
                    file.write(f"{id},{nome},{idade},{telefone},{email}\n")
        except Exception as e:
            logging.warning(f"Erro em write client: {e}")
            
    elif path_index == 1:
        logging.info("CSV ANIMAIS")
        try:
            with open(ANIMAIS, 'w') as file:
                file.write('id,nome,cliente_id,especie,raca\n')
                for animal in new_list:
                    id,nome,cliente_id,especie,raca = animal.split(",")
                    file.write(f"{id},{nome},{cliente_id},{especie},{raca}\n")
        except Exception as e:
            logging.warning(f"Erro em write animais: {e}")    
        logging.info("CSV clientes mudou.")

    elif path_index == 2:
        logging.info("CSV SERVIÇOS")
        try:
            with open(SERVICOS, 'w') as file:
                file.write('id,nome,cliente_id,animal_id,preco\n')
                for servico in new_list:
                    id,nome,cliente_id,animal_id,preco = servico.split(",")
                    file.write(f"{id},{nome},{cliente_id},{animal_id},{preco}\n")
        except Exception as e:
            logging.warning(f"Erro em write serviços: {e}")    
        logging.info("CSV serviços mudou.")
    
    else:
        logging.info(f"Write csv index de valor {path_index} não existe.")
        return {"msg" : f"Path index {path_index} não existe."}
    
def xml(index_path:int):
    logging.info(f"Arquivo de xml chamado para path de index: {index_path}")
    
    PATH = Path('xml')
    PATH.mkdir(exist_ok=True)
    
    if index_path == 0:
        logging.info("XML Clientes")
        clientes = ET.Element("clientes")
        clients = read_csv(0)
        for c in clients:
            id,nome,idade,telefone,email = c.split(",")
            cli = ET.SubElement(clientes,"cliente")
            id_cliente = ET.SubElement(cli,"id")
            id_cliente.text = id
            nome_cliente = ET.SubElement(cli,"nome")
            nome_cliente.text = nome
            idade_cliente = ET.SubElement(cli,"idade")
            idade_cliente.text = idade
            telefone_cliente = ET.SubElement(cli,"telefone")
            telefone_cliente.text = telefone
            email_cliente = ET.SubElement(cli,"email")
            email_cliente.text = email 
        arvore = ET.ElementTree(clientes)
        arvore.write("xml/clientes.xml", encoding="utf-8", xml_declaration=True)
        return FileResponse("xml/clientes.xml", media_type="application/xml", filename="clientes.xml")
    
    if index_path == 1:
        logging.info("XML Animais")
        animais = ET.Element("animais")
        animals = read_csv(1)
        for c in animals:
            id,nome,cliente_id,especie,raca = c.split(",")
            ani = ET.SubElement(animais,"animal")
            id_animal = ET.SubElement(ani,"id")
            id_animal.text = id
            nome_animal = ET.SubElement(ani,"nome")
            nome_animal.text = nome
            cliente_id_animal = ET.SubElement(ani,"cliente_id")
            cliente_id_animal.text = cliente_id
            especie_animal = ET.SubElement(ani,"especie")
            especie_animal.text = especie
            raca_animal = ET.SubElement(ani,"raca")
            raca_animal.text = raca 
        arvore = ET.ElementTree(animais)
        arvore.write("xml/animais.xml", encoding="utf-8", xml_declaration=True)
        return FileResponse("xml/animais.xml", media_type="application/xml", filename="animais.xml")
    
    if index_path == 2:
        logging.info("XML serviços")
        servicos = ET.Element("serviços")
        services = read_csv(2)
        for c in services:
            id,nome,cliente_id,animal_id,preco = c.split(",")
            serv = ET.SubElement(servicos,"serviço")
            id_servico = ET.SubElement(serv,"id")
            id_servico.text = id
            nome_servico = ET.SubElement(serv,"nome")
            nome_servico.text = nome
            cliente_id_servico = ET.SubElement(serv,"cliente_id")
            cliente_id_servico.text = cliente_id
            animal_id_servico = ET.SubElement(serv,"animal_id")
            animal_id_servico.text = animal_id
            preco_servico = ET.SubElement(serv,"preco")
            preco_servico.text = preco 
        arvore = ET.ElementTree(servicos)
        arvore.write("xml/servico.xml", encoding="utf-8", xml_declaration=True)
        return FileResponse("xml/servico.xml", media_type="application/xml", filename="servico.xml")

    logging.warning(f"Index path chamado nao existe: {index_path}")