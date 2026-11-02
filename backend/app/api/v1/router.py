from app.api.v1.endpoints import alunos, treinos  # Importa o módulo de treinos
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(alunos.router, prefix="/alunos", tags=["Alunos"])
api_router.include_router(
    treinos.router, prefix="/treinos", tags=["Treinos & Exercícios"]
)