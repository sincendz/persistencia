# 🐶 Sistema de Gerenciamento Veterinário

**Projeto 1** desenvolvido durante a disciplina **Desenvolvimento de Software para Persistência**.

## 📖 Descrição

Neste trabalho, foi desenvolvida uma aplicação que simula o serviço de uma clínica veterinária. O sistema possui três modelos principais:

- **Cliente**
- **Animal**
- **Serviço**

O objetivo do projeto é criar uma API capaz de persistir os dados desses modelos em arquivos **CSV**.

## ⚙️ Funcionalidades

A aplicação disponibiliza endpoints de **CRUD** para cada modelo, além de funcionalidades extras:

- 🔍 Busca de registros por nome
- 📝 Geração do **hash** dos arquivos CSV
- 📦 Compactação dos arquivos em **ZIP**
- 📄 Conversão dos dados para **XML** para download

## 🛠️ Tecnologias Utilizadas

- **Python**
- **FastAPI** — criação da API
- **Uvicorn** — servidor ASGI
- **Pydantic BaseModel** — definição e validação dos modelos de dados
- **PyYAML** - usado para ler o arquivo de log

---

## 📦 Instalação

Para rodar este projeto, é necessário ter o **Python 3.7+** instalado e as seguintes bibliotecas:

- **FastAPI**
- **Uvicorn**
- **PyYAML**
- **Pydantic**

Apesar de não ser obrigatório, é recomendado rodar em um ambiente virtual (venv).
### 🔧 Passos para instalação:
Instale as bibliotecas:
```bash
pip install fastapi uvicorn PyYAML pydantic
```

Para rodar o projeto:

```bash
uvicorn main:app --reload
```
A documentação interativa estará disponível após rodar o projeto, acessando:
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Autores

- [@Mário Aragão](https://github.com/sincendz)

- [@Gustavo de Freitas](https://github.com/gustavo-codes)