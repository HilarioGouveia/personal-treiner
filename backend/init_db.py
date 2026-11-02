"""Cria as tabelas ausentes no banco configurado, sem apagar dados existentes.

Execute a partir de backend: python init_db.py
"""

from app.core.database import engine
from app.models.models import Base


def main():
    Base.metadata.create_all(bind=engine)
    print("Tabelas do banco inicializadas.")


if __name__ == "__main__":
    main()
