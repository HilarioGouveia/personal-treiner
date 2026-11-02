from app.api.v1.router import api_router
from app.core.config import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="API de Gestão - Personal Trainer",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configuração de CORS (permite requisições do Streamlit / Frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, restringir para o domínio do frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas da versão 1 da API
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def read_root():
  return {
      "status": "online",
      "message": "API de Gestão para Personal Trainer em execução",
  }