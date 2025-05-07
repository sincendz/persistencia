from instanciaLogs import Logs , logging
from pathlib import Path
from pydantic import BaseModel

log = Logs()

# Checa se a pasta db existe, se não existir ela é criada
PATH = Path('db')
PATH.mkdir(exist_ok=True)

# Caminho até o csv
PESSOAS = PATH / 'pessoas.csv'

class Pessoa(BaseModel):
    id: int
    name: str
    age: int

# Checa se o csv existe. Se não, cria com cabeçalho
if not PESSOAS.exists():
    logging.warning("PESSOAS.csv não existia. Criando arquivo com cabeçalho.")
    with open(PESSOAS, 'w') as f:
        f.write("id,name,age\n")

def read_csv():
    pessoas = []
    with open(PESSOAS, 'r') as file:
        logging.info("Leitura do csv.")
        lines = file.readlines()
        for line in lines:
            pessoas.append(line.strip())
    return pessoas

def write_csv(person: Pessoa):
    logging.info(f"Dado que chegou para ser salvo no CSV: {person}")
    with open(PESSOAS, 'a') as file:
        file.write(f"{person.id},{person.name},{person.age}\n")
        logging.info("Arquivo CSV modificado.")


def write_csv_list(pessoas):
    logging.debug(pessoas)
    with open(PESSOAS, 'w') as file:
        file.write('id,nome,idade\n')  # adicionei \n
        for p in pessoas:
            id,name,idade = p.split(",")
            file.write(f"{id},{name},{idade}\n")
    logging.info("CSV mudado")

