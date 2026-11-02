from app.api.v1.endpoints import alunos, avaliacoes, mensalidades, treinos
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(alunos.router, prefix="/alunos", tags=["Alunos"])
api_router.include_router(
    treinos.router, prefix="/treinos", tags=["Treinos & Exercícios"]
)
api_router.include_router(avaliacoes.router, prefix="/avaliacoes", tags=["Avaliações"])
api_router.include_router(mensalidades.router, prefix="/mensalidades", tags=["Mensalidades"])
