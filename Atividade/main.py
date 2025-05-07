from instanciaLogs import Logs , logging
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from csvFunctions import read_csv,write_csv, write_csv_list


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
    
    
@app.get("/pessoas")
def pessoas():
    logging.info("Endpoint GET Pessoas chamado")
    pessoas = read_csv()
    if len(pessoas) > 0:
        pessoas.pop(0)
        return pessoas
    logging.info("Lista de pessoas está vazia.")
    return "Lista vazia."

@app.post("/pessoas")
def add_pessoa(pessoa:Pessoa):
    
    pessoas = read_csv()
    pessoas.pop(0)
    
    logging.info(f"Checando se {pessoa.id} já existe no sistema. ")
    for p in pessoas:
        id_csv, _, _ = p.split(",")
        logging.debug((int(id_csv),pessoa.id))
        if int(id_csv) == pessoa.id:
            logging.info(f"ID {pessoa.id} já existe no sistema. Não é possível cadastrar.")
            raise HTTPException(status_code=404, detail="ID já existe no sistema")
    
    try:
        write_csv(pessoa)
        logging.info("Nova pessoa cadastrada")
    except Exception as e:
        logging.warning(f"Erro ao salvar no csv: {e} ")
        raise HTTPException(status_code=404, detail="Erro ao salvar no csv")
    
    return {"msg": "Pessoa cadastrada com sucesso!", "pessoa": pessoa}

    
@app.delete("/pessoas/id")
def delete_by_id(id:int):
    logging.info(f"Função de chamar chamada para id : {id}")
    pessoas = read_csv()
    pessoas.pop(0)
    change = False
    new_list = []
    logging.debug(f"Tamanho pessoas: {len(pessoas)}")
    if len(pessoas) > 0:
        for p in pessoas:
            id_csv , _ , _ = p.split(',')
            if int(id_csv) == id:
                change = True
            else:
                new_list.append(p)
        if change:
            write_csv_list(new_list)
        else:
            logging.info(f"Delete nao mudou a lista, id {id} não encontrado.")      
    return new_list     