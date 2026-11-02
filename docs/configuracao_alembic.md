# Configuração

Para configurar o **Alembic** e gerenciar as migrações do banco de dados (integrado ao SQLAlchemy que definimos anteriormente), siga o passo a passo prático abaixo.

---

## Passo 1: Instalação do Alembic

Caso ainda não tenha instalado no seu ambiente virtual Python (`venv`), execute no terminal dentro da pasta `/backend`:

```bash
pip install alembic

```

---

## Passo 2: Inicialização do Alembic

Na raiz da pasta `/backend`, execute o comando de inicialização:

```bash
alembic init alembic

```

Isso criará uma pasta chamada `alembic/` e o arquivo de configuração `alembic.ini` na raiz do backend.

---

## Passo 3: Configurar o `alembic/env.py`

Para que o Alembic saiba quais tabelas criar, ele precisa importar a classe `Base` e todos os seus modelos do SQLAlchemy.

Abra o arquivo `backend/apresenta_alembic/env.py` (ou `backend/alembic/env.py`) e faça as seguintes alterações:

1. Importar o `Base` dos seus modelos.
2. Atribuir o `target_metadata`.
3. Injetar a URL do banco de dados a partir das configurações do projeto.

Veja como o trecho principal do arquivo `env.py` deve ficar:

```python
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# --- IMPORTAÇÕES DO SEU PROJETO ---
from app.core.config import settings  # Suas configurações de ambiente
from app.models.models import Base    # Seu arquivo de modelos SQLAlchemy

# Interpretador de configuração do Alembic
config = context.config

# Sobrescreve a URL do banco de dados no alembic.ini usando a config do FastAPI (.env)
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Define o metadata para o Alembic rastrear as tabelas automaticamente
target_metadata = Base.metadata

# (Mantenha o restante das funções run_migrations_offline e run_migrations_online geradas pelo alembic)

```

---

## Passo 4: Gerar a Primeira Migração (Baseline)

Com os modelos mapeados e o Alembic configurado, certifique-se de que o seu `.env` possui a variável `DATABASE_URL` (ex: `sqlite:///./app.db`) e execute o comando para gerar o primeiro script de migração automático:

```bash
alembic revision --autogenerate -m "initial_schema"

```

O Alembic vai analisar todas as classes (`Usuario`, `Aluno`, `FichaTreino`, `Exercicio`, etc.) e gerar um arquivo de migração dentro de `backend/alembic/versions/` contendo os comandos `op.create_table(...)`.

---

## Passo 5: Aplicar a Migração no Banco de Dados

Por fim, aplique a migração gerada para criar as tabelas fisicamente no banco de dados (SQLite ou PostgreSQL):

```bash
alembic upgrade head

```

Pronto! Seu banco de dados está criado, versionado e pronto para receber dados através da sua API FastAPI. Sempre que você alterar uma classe no SQLAlchemy, basta repetir os **Passos 4 e 5** para atualizar o banco de forma limpa.

---
