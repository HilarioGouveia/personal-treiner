import os
from typing import List, Union
from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "API de Gestão - Personal Trainer"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # JWT Settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "SUA_CHAVE_SECRETA_SUPER_SEGURA_AQUI_CHANGE_IN_PRODUCTION")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 dias

    # Database Settings
    # SQLite por padrão para MVP local; pode ser substituído por PostgreSQL via variável de ambiente
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")

    # CORS Settings
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:8501",  # Streamlit Frontend
        "http://127.0.0.1:8501",
        "http://localhost:8000",
    ]

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()