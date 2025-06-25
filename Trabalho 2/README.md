# Sistema de Gestão para Clínica Veterinária - API

Este projeto consiste em uma **API RESTful** para gerenciar as operações de uma clínica veterinária. Foi desenvolvido utilizando um conjunto de tecnologias modernas de Python para garantir performance, manutenibilidade e facilidade de desenvolvimento.

---

## ✨ Tecnologias Principais

* **Python 3.12**: A linguagem de programação base, escolhida por sua simplicidade e ecossistema robusto.
* **FastAPI**: Framework web de alta performance para a construção de APIs, com geração automática de documentação interativa (Swagger UI).
* **SQLModel**: Biblioteca que combina **SQLAlchemy** e **Pydantic** para definir modelos de dados que servem tanto para a validação da API quanto para o mapeamento objeto-relacional (ORM).
* **SQLite**: Banco de dados relacional leve, baseado em arquivo, ideal para desenvolvimento e prototipagem.
* **Alembic**: Ferramenta de migração de banco de dados para gerenciar a evolução do schema de forma versionada.
* **Uvicorn**: Servidor web ASGI (Asynchronous Server Gateway Interface) de alta velocidade, recomendado para rodar aplicações FastAPI.

---

## 🗂️ Modelos de Dados

A API gerencia um conjunto de entidades inter-relacionadas que representam o núcleo de uma clínica veterinária:

* **Client**: Representa os donos dos animais.
* **Animal**: Representa os pacientes da clínica. Cada animal está associado a um `Client` (relação 1-N).
* **Veterinary**: Modela os veterinários da clínica.
* **CRMV**: Armazena as informações do Conselho Regional de Medicina Veterinária, com cada `Veterinary` possuindo um registro (relação 1-1).
* **Service**: Descreve os serviços oferecidos, como "Consulta", "Vacinação" ou "Cirurgia".
* **Consultation**: Registra uma consulta, ligando um `Animal`, um `Veterinary` e múltiplos `Service` (relação N-N com Serviços).

---

## 🚀 Funcionalidades Principais

### **CRUD Completo**
Para todos os modelos (`Client`, `Animal`, `Veterinary`, etc.), existem endpoints para **Criar**, **Ler**, **Atualizar** e **Deletar** registros.

### **Busca de Texto Parcial (Case-Insensitive)**
Endpoints de busca permitem encontrar registros de forma flexível. Por exemplo, uma requisição para `/animals/search_name/rex` retornará todos os animais cujo nome contenha "rex", "Rex", "reX", etc.

### **Paginação**
Para evitar o retorno de grandes volumes de dados de uma só vez, os endpoints de listagem (`/clients/page`, `/animals/page`, etc.) são paginados.
* **Uso**: `GET /clients/page?page=1&page_size=10`
* **Resposta**: O JSON de resposta inclui a lista de registros da página, o número total de registros, o total de páginas e a página atual.

### **Consultas Complexas e Relatórios**
Endpoints específicos foram criados para extrair informações de negócio:
* Listar todos os animais de um cliente específico.
* Listar todas as consultas que ainda estão em aberto para um determinado veterinário.
* Calcular e retornar o valor total dos serviços realizados em uma única consulta.

### **Gerenciamento de Relacionamentos**
A API permite gerenciar as associações entre as entidades, como:
* Adicionar um ou mais serviços a uma consulta existente (relação N-N).
* Finalizar uma consulta, preenchendo a data de saída (`data_out`).

### **Utilitários de Desenvolvimento**
* **`GET /create_db`**: Endpoint para criar todas as tabelas no banco de dados.
* **`POST /populate`**: Endpoint para popular o banco com um conjunto de dados de exemplo (clientes, animais, serviços, etc.), facilitando testes e demonstrações.

---

## 🛠️ Como Executar o Projeto

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/sincendz/persistencia.git
    cd Trabalho\ 2
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Inicie o servidor:**
    ```bash
    uvicorn main:app --reload
    ```

5.  **Acesse a documentação da API:**
    Abra seu navegador e acesse [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) para ver a documentação interativa do Swagger UI e testar os endpoints.

---

## Autores

- [@Mário Aragão](https://github.com/sincendz)

- [@Gustavo de Freitas](https://github.com/gustavo-codes)