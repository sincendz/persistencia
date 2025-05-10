from instanciaLogs import Logs , logging
from pathlib import Path
from pydantic import BaseModel
from models import *

log = Logs()

# Checa se a pasta db existe, se não existir ela é criada
PATH = Path('db')
PATH.mkdir(exist_ok=True)

# Caminho até o csv
CLIENTES = PATH / 'clientes.csv'
ANIMAIS = PATH / 'animais.csv'
SERVICOS = PATH / 'servicos.csv'

paths = [CLIENTES,ANIMAIS,SERVICOS]


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

def read_csv(path_index:int):
    path = paths[path_index]
    data = []
    with open(path, 'r') as file:
        logging.info("Leitura do csv.")
        lines = file.readlines()
        for line in lines:
            data.append(line.strip())
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


def write_csv_list_cliente(clientes):
    logging.debug(clientes)
    with open(CLIENTES, 'w') as file:
        file.write('id,nome,idade,telefone,email\n')  # adicionei \n
        for p in clientes:
            id,nome,idade,telefone,email = p.split(",")
            file.write(f"{id},{nome},{idade},{telefone},{email}\n")
    logging.info("CSV mudado")

