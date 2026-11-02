![Personal Trainer Banner](./docs/personal-treiner_banner.jpg)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Alembic](https://img.shields.io/badge/Alembic-DB4437?style=for-the-badge)

---

# 🏋️‍♂️ Personal Trainer - App de Gestão Exclusiva

Plataforma de gestão personalizada para consultoria de Personal Trainers. Desenvolvida sob demanda como alternativa de código aberto e independente a plataformas comerciais terceirizadas, com controle total sobre branding, precificação e metodologia dos treinos.

---


## 📌 Principais Módulos

* **👥 Gestão de Alunos:** Cadastro centralizado, anamnese, histórico e perfil restrito.
* **🏋️‍♂️ Construtor de Treinos:** Montagem visual de fichas (A/B/C/D), prescrição de cargas, séries, repetições e vinculação com vídeos explicativos.
* **📈 Avaliação Física & Evolução:** Registro antropométrico flexível (dobras, medidas) e geração gráfica de métricas de evolução temporal.
* **💰 Controle Financeiro:** Controle de mensalidades, histórico de vencimentos e baixa rápida de pagamentos.

---

## 🏗️ Visão Geral da Arquitetura

O sistema adota uma arquitetura desacoplada (Client-Server Architecture) de alta performance:

```
[ Frontend (Streamlit) ]  <--- HTTP/REST (JSON) --->  [ Backend API (FastAPI) ]
                                                               |
                                                          (SQLAlchemy ORM)
                                                               |
                                                       [ Database PostgreSQL / SQLite ]
```

* **Backend (FastAPI):** API RESTful assíncrona responsável por regras de negócio, autenticação JWT, validação de esquemas (Pydantic) e persistência de dados.
* **Frontend (Streamlit Multi-Page):** Interface interativa rica para o personal trainer gerenciar todos os aspectos da consultoria sem complexidade de deploy de frameworks JavaScript pesados.
* **Camada de Dados:** ORM SQLAlchemy integrado ao **Alembic** para versionamento seguro das tabelas do banco de dados (SQLite em desenvolvimento, PostgreSQL em produção).

---

## 🗄️ Modelo de Dados Relacional (ERD)

```text
       +-------------------+
       |     usuarios      |
       +-------------------+
       | PK  id            |
       |     email         |
       |     senha_hash    |
       |     perfil        |
       |     ativo         |
       +---------+---------+
                 | 1:1
                 v
       +-------------------+               +----------------------+
       |      alunos       | 1:N           |  avaliacoes_fisicas  |
       +-------------------+--------------->+----------------------+
       | PK  id            |               | PK  id               |
       | FK  usuario_id    |               | FK  aluno_id         |
       |     nome          |               |     data_avaliacao   |
       |     data_nasc     |               |     peso_kg          |
       |     objetivo      |               |     dobras_cutaneas  |
       |     obs_medicas   |               |     medidas_json     |
       +---------+---------+               +----------------------+
                 |
        +--------+--------+
        | 1:N             | 1:N
        v                 v
+---------------+ +------------------+
| fichas_treino | |   mensalidades   |
+---------------+ +------------------+
| PK  id        | | PK  id           |
| FK  aluno_id  | | FK  aluno_id     |
|     titulo    | |     data_venc    |
|     descricao | |     valor        |
|     ativa     | |     status       |
+-------+-------+ +------------------+
        |
        | 1:N
        v
+-----------------------+                  +------------------+
|     itens_treino      | N:1              |    exercicios    |
+-----------------------+----------------->+------------------+
| PK  id                |                  | PK  id           |
| FK  ficha_id          |                  |     nome         |
| FK  exercicio_id      |                  |     grupo_musc   |
|     divisao (A/B/C)   |                  |     url_video    |
|     series            |                  +------------------+
|     repeticoes        |
|     carga_kg          |
|     descanso_seg      |
|     ordem             |
+-----------------------+
```

---

## 📂 Estrutura de Pastas

```text
meu_app_personal/
├── backend/
│   ├── alembic/              # Scripts e configurações de migração de banco
│   ├── app/
│   │   ├── api/v1/endpoints/ # Rotas divididas por domínio (alunos, treinos, etc.)
│   │   ├── core/             # Conexão DB e variáveis globais
│   │   ├── models/           # Mapeamento ORM SQLAlchemy
│   │   └── schemas/          # Schemas Pydantic de validação
│   ├── main.py               # Ponto de entrada do FastAPI
│   └── requirements.txt
└── frontend/
    ├── pages/                # Páginas funcionais Streamlit
    ├── services/             # Cliente de comunicação HTTP REST
    ├── app.py                # Tela inicial e fluxo de autenticação
    └── requirements.txt
```

---

## 🚀 Como Executar o Projeto

### 1. Clonar o Repositório

```bash
git clone https://github.com/seu-usuario/meu-app-personal.git
cd meu-app-personal
```

### 2. Configurar e Executar o Backend (FastAPI)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Ou `venv\Scripts\activate` no Windows

pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

*A documentação interativa da API estará disponível em `http://localhost:8000/docs`.*

### 3. Configurar e Executar o Frontend (Streamlit)

Em um novo terminal:

```bash
cd frontend
python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
streamlit run app.py

```

*A interface web será aberta automaticamente no endereço `http://localhost:8501`.*

---

## 🛡️ Licença

Este projeto é distribuído sob a licença **MIT**. Veja o arquivo `LICENSE` para mais detalhes.
