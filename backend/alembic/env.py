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