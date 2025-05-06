from instanciaLogs import Logs , logging
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from csvFunctions import read_csv,write_csv


app = FastAPI()
log = Logs() # Instancia o arquivo de logs


@app.get("/")
def root():
    logging.info("Acesso ao endpoint root.")
    return {'msg':'Hello, World!!'}
    
    
@app.get("/pessoas")
def pessoas():
    logging.info("Endpoint GET Pessoas chamado")
    pessoas = read_csv()
    pessoas.pop(0)
    return pessoas

@app.post("/pessoas")
def add_pessoa(id,name,age):
    
    pessoas = read_csv()
    
    logging.info(f"Checando se {id} já existe no sistema. ")
    for pessoa in pessoas:
        i,_,_ = pessoa.split(',')
        if i == id:
            logging.info(f"{id, name, age} id já existe no sistema. Não é possivel cadastrar")
            raise HTTPException(status_code=404, detail="ID já existe no sistema")
    
    logging.info("Nova pessoa cadastrada")
    pessoa = f"{id},{name},{age},"
    try:
        write_csv(pessoa)
    except Exception as e:
        logging.warning(f"Erro ao salvar no csv: {e} ")
        raise HTTPException(status_code=404, detail="Erro ao salvar no csv")
    
    