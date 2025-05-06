from instanciaLogs import Logs,logging
import os, csv
from pathlib import Path

log = Logs()

# Checa se a pasta db existe, se não existir ela é criada
PATH = Path('db')
PATH.mkdir(exist_ok=True)

# Caminho até o csv
ANIMAIS = PATH / 'animais.csv'

#Checa se o csv existe.
if not ANIMAIS.exists():
    logging.warning("Animais.csv não existia.")
    ANIMAIS.touch()

def read_csv():
    animais = []
    with open(ANIMAIS,'r') as file:
        logging.info("Leitura do csv")
        line = file.readlines()
        for i in line:
            animais.append(i.strip())
    #animais.pop(0) # Remove os indices da tabela
    return animais
        
    
def write_csv(person):
    logging.info(f"Dado que chegou para ser salvo no CSV : {person}")
    pessoas = read_csv()
    pessoas.append(person)
    with open(ANIMAIS , 'a') as file:
        file.write(person)
        logging.info("Arquivo de CSV modificado")
        
